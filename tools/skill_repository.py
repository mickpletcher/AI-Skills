#!/usr/bin/env python3
"""Offline repository validation, catalog generation and deterministic packaging."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import os
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit
import yaml

ROOT = Path(__file__).resolve().parents[1]
PLATFORMS = {p: ('SKILL.md' if p in ('claude', 'perplexity') else 'instructions.md')
             for p in ('claude', 'chatgpt', 'copilot', 'cursor', 'gemini', 'perplexity')}
TEXT_SUFFIXES = {'.md', '.json', '.yaml', '.yml', '.txt', '.py', '.ps1', '.html', '.css', '.js', '.csv'}
SECTIONS = {
    'Intent': 'Intent|Purpose|Overview|What This Skill Does|Role',
    'Use When': 'Use When|Trigger When|When To Use|Primary Triggers|Trigger',
    'Do Not Use When': 'Do Not Use When|Do Not Use|When Not To Use|Out Of Scope',
    'Workflow': 'Workflow|Process|Operating Procedure|Step-by-Step Workflow|Invention Intake Workflow',
    'Constraints': 'Constraints|Rules|Safety Rules|Safety|Guardrails|Required Safety Rules|Hard Constraints',
    'Help And Examples': 'Help And Examples|Help Response|Help|Examples|Example Prompts',
    'Validation Checklist': 'Validation Checklist|Validation|Test Cases|Quality Checklist|Quality Checks|Testing',
}

class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise ValueError(f'duplicate or non-string YAML key: {key!r}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

def schema_check(value, schema):
    """Evaluate exactly the JSON Schema keywords used by our frontmatter schema.

    Fail closed on unsupported keywords so extending the schema cannot silently
    weaken validation. Not a general purpose JSON Schema implementation.
    """
    supported = {'$schema', 'title', 'type', 'required', 'additionalProperties', 'properties', 'pattern', 'minLength'}
    if set(schema) - supported:
        raise ValueError('unsupported frontmatter schema keyword')
    if schema['type'] == 'object':
        if not isinstance(value, dict):
            raise ValueError('frontmatter must be a mapping')
        missing = set(schema.get('required', [])) - set(value)
        if missing:
            raise ValueError(f'missing frontmatter fields: {sorted(missing)}')
        for key, item in value.items():
            if key not in schema['properties']:
                if not schema.get('additionalProperties', True):
                    raise ValueError(f'unknown frontmatter field: {key}')
            else:
                schema_check(item, schema['properties'][key])
    elif schema['type'] == 'string':
        if not isinstance(value, str) or not value.strip():
            raise ValueError('frontmatter fields must be nonempty strings')
        if len(value) < schema.get('minLength', 0) or ('pattern' in schema and not re.fullmatch(schema['pattern'], value)):
            raise ValueError(f'invalid frontmatter value: {value!r}')
    else:
        raise ValueError('unsupported frontmatter schema type')

def frontmatter(path, root=ROOT):
    text = path.read_text(encoding='utf-8-sig')
    match = re.match(r'\A---\s*\n(.*?)\n---\s*(?:\n|$)', text, re.S)
    if not match:
        raise ValueError('missing YAML frontmatter')
    data = yaml.load(match[1], Loader=UniqueLoader)
    schema_check(data, json.loads((root / 'schemas/skill-frontmatter.schema.json').read_text()))
    if data['name'] != path.parent.name:
        raise ValueError('frontmatter name must equal skill directory name')
    return data

def skills(root):
    return [(platform, d) for platform in PLATFORMS
            for d in sorted((root / platform / 'skills').glob('*'))
            if d.is_dir() and not d.name.startswith('.')]

def exact_file(folder, name):
    return any(p.name == name and p.is_file() for p in folder.iterdir())

def payload_files(folder):
    files = []
    for p in sorted(folder.rglob('*'), key=lambda path: path.relative_to(folder).as_posix()):
        rel = p.relative_to(folder)
        if any(part.startswith('.') or part == '__pycache__' for part in rel.parts):
            continue
        if p.name == 'future-upgrades.md' or p.suffix in ('.skill', '.pyc', '.pyo'):
            continue
        if p.is_symlink():
            raise ValueError(f'package source may not be a symlink: {p}')
        if p.is_file():
            files.append(p)
    return files

def canonical_bytes(path):
    data = path.read_bytes()
    return data.replace(b'\r\n', b'\n') if path.suffix.lower() in TEXT_SUFFIXES else data

def package_bytes(folder):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_STORED) as archive:
        for p in payload_files(folder):
            info = zipfile.ZipInfo(p.relative_to(folder).as_posix(), (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, canonical_bytes(p))
    return out.getvalue()

def package_errors(folder):
    package = folder / (folder.name + '.skill')
    expected = {p.relative_to(folder).as_posix(): canonical_bytes(p) for p in payload_files(folder)}
    try:
        with zipfile.ZipFile(package) as archive:
            names = archive.namelist()
            if len(names) != len(set(n.lower() for n in names)):
                return ['duplicate archive entries']
            actual = {n: archive.read(n) for n in names}  # checks ZIP CRC on every member
        errors = []
        if set(actual) != set(expected):
            errors.append(f'package file set differs: missing={sorted(set(expected)-set(actual))}, extra={sorted(set(actual)-set(expected))}')
        mismatches = [n for n in expected.keys() & actual.keys() if expected[n] != actual[n]]
        if mismatches:
            errors.append(f'package/source bytes differ: {sorted(mismatches)}')
        if package.read_bytes() != package_bytes(folder):
            errors.append('package is not the reproducible build; run package')
        return errors
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError) as exc:
        return [f'unreadable package: {exc}']

def prose(text):
    # Fenced code and inline code are examples, not navigable Markdown links.
    text = re.sub(r'(?ms)^\s*(`{3,}|~{3,}).*?^\s*\1\s*$', '', text)
    return re.sub(r'`+[^`]*`+', '', text)

def anchors(text):
    found = set(re.findall(r'\b(?:id|name)=["\']([^"\']+)["\']', text))
    counts = {}
    for heading in re.findall(r'(?m)^#{1,6}\s+(.+?)(?:\s+#+)?$', text):
        heading = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', heading)
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        found.add(slug + (f'-{count}' if count else ''))
    return found

def exact_path(root, path):
    try:
        relative = path.relative_to(root)
    except ValueError:
        return False
    current = root
    for name in relative.parts:
        if not current.is_dir() or name not in {p.name for p in current.iterdir()}:
            return False
        current = current / name
    return current.exists()

def link_errors(root, source_guard=None):
    errors = []
    for path in sorted(root.rglob('*.md')):
        if any(part.startswith('.') for part in path.relative_to(root).parts):
            continue
        if source_guard:
            source_guard(path)
        text = prose(path.read_text(encoding='utf-8-sig'))
        targets = re.findall(r'!?\[[^\]]*\]\(<?([^\s)>]+)>?(?:\s+"[^"]*")?\)', text)
        targets += re.findall(r'(?m)^\s*\[[^\]]+\]:\s*<?([^\s>]+)>?', text)
        definitions = {key.lower() for key in re.findall(r'(?m)^\s*\[([^\]]+)\]:', text)}
        for label, ref in re.findall(r'!?\[([^\]]+)\]\[([^\]]*)\]', text):
            if (ref or label).lower() not in definitions:
                errors.append(f'{path.relative_to(root)}: missing link definition {ref or label}')
        for target in targets:
            parsed = urlsplit(target)
            if re.match(r'^[A-Za-z]:[/\\]', target) or target.startswith('file:'):
                errors.append(f'{path.relative_to(root)}: machine-specific link {target}')
                continue
            if parsed.scheme or parsed.netloc:
                continue  # No external requests; external link health is not claimed.
            local = unquote(parsed.path)
            dest = Path(os.path.abspath(path.parent / local)) if local else path
            if not exact_path(root, dest):
                errors.append(f'{path.relative_to(root)}: broken/case-mismatched internal link {target}')
            elif parsed.fragment and dest.suffix == '.md':
                if source_guard:
                    source_guard(dest)
                if unquote(parsed.fragment) not in anchors(dest.read_text(encoding='utf-8-sig')):
                    errors.append(f'{path.relative_to(root)}: missing anchor {target}')
    return errors

def validate(root, folders_only=False, source_guard=None):
    errors, count = [], 0
    items = [('claude', d) for d in sorted(root.iterdir()) if d.is_dir() and not d.name.startswith('.')] if folders_only else skills(root)
    for platform, folder in items:
        count += 1
        required = ['README.md', PLATFORMS[platform]]
        if platform == 'claude':
            required += [folder.name + '.skill', 'completedchanges.md']
        for name in required:
            if not exact_file(folder, name):
                errors.append(f'{folder}: missing exact-case file {name}')
        if folders_only:
            continue
        source = folder / PLATFORMS[platform]
        if not exact_file(folder, source.name):
            continue
        text = source.read_text(encoding='utf-8-sig')
        if platform in ('claude', 'perplexity'):
            try:
                frontmatter(source, root)
            except (ValueError, yaml.YAMLError) as exc:
                errors.append(f'{source}: {exc}')
        for name, rule in SECTIONS.items():
            if not re.search(r'^##\s+(?:' + rule + r')\b', text, re.M | re.I):
                errors.append(f'{source}: missing section {name}')
        if platform == 'claude' and exact_file(folder, folder.name + '.skill'):
            errors += [f'{folder}: {e}' for e in package_errors(folder)]
    if not count:
        errors.append('No skills checked; refusing an empty validation result')
    if not folders_only:
        errors += link_errors(root, source_guard=source_guard)
    return count, errors

def purpose(source, data):
    if data:
        return data['description'].split('. ')[0].strip()
    text = source.read_text(encoding='utf-8-sig')
    match = re.search(r'^## Intent\s*\n+([^\n]+)', text, re.M)
    return match[1] if match else 'See skill README for purpose.'

def generated(root):
    records = []
    for platform, folder in skills(root):
        source = folder / PLATFORMS[platform]
        data = frontmatter(source, root) if platform in ('claude', 'perplexity') else {}
        readme = folder / 'README.md'
        text = readme.read_text(encoding='utf-8-sig')
        prereq = re.search(r'^## (?:Prerequisites|Requirements)\s*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
        declared = prereq[1].strip() if prereq else None
        package = folder / (folder.name + '.skill') if platform == 'claude' else None
        records.append({
            'id': f'{platform}/{folder.name}', 'platform': platform, 'name': folder.name,
            'purpose': purpose(source, data), 'source': source.relative_to(root).as_posix(),
            'readme': readme.relative_to(root).as_posix(), 'version': data.get('version'),
            'installation': f'docs/installation.md#{platform}',
            'prerequisites': declared, 'prerequisites_source': readme.relative_to(root).as_posix(),
            'package': package.relative_to(root).as_posix() if package else None,
            'sha256': hashlib.sha256(package.read_bytes()).hexdigest() if package else None,
            'last_model_evaluation': None,
        })
    manifest = json.dumps({'schema_version': 1, 'skills': records}, indent=2, ensure_ascii=False) + '\n'
    lines = ['# Skill Catalog', '', 'Generated by `python tools/skill_repository.py catalog`. Do not edit by hand.', '',
             'All shipped skills are listed below. Versions and prerequisites absent from source are marked “not declared”; model evaluation dates are not inferred from commits or structural checks. See [manifest](catalog.json) for package hashes and full declared prerequisites, [installation](docs/installation.md), and [dependencies](docs/dependencies.md).', '',
             '| Platform / skill | Purpose | Install | Prerequisites | Package / version |', '| --- | --- | --- | --- | --- |']
    for row in records:
        name = f"[{row['id']}]({row['readme']})"
        p = row['purpose'].replace('|', '\\|').replace('\n', ' ')
        prereq = f"[Declared in README]({row['readme']})" if row['prerequisites'] else f"[Not declared; review README]({row['readme']})"
        package = f"[.skill]({row['package']})" if row['package'] else 'Instruction source'
        lines.append(f"| {name} | {p} | [{row['platform']}]({row['installation']}) | {prereq} | {package}; {row['version'] or 'version not declared'} |")
    checksums = ''.join(f"{r['sha256']}  {r['package']}\n" for r in records if r['package'])
    return {'catalog.json': manifest, 'CATALOG.md': '\n'.join(lines) + '\n', 'SHA256SUMS': checksums}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'folders', 'package', 'catalog'])
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.command in ('validate', 'folders'):
            count, errors = validate(root, args.command == 'folders')
            if args.command == 'validate' and not errors:
                errors += [f'{name} is stale; run catalog' for name, value in generated(root).items()
                           if not (root / name).exists() or (root / name).read_bytes() != value.encode()]
            print(f'Checked {count} skills; {len(errors)} issue(s).')
            for error in errors:
                print(error)
            return bool(errors)
        if args.command == 'package':
            count = 0
            for platform, folder in skills(root):
                if platform != 'claude':
                    continue
                count += 1
                output = folder / (folder.name + '.skill')
                value = package_bytes(folder)
                if args.check:
                    if not output.exists() or output.read_bytes() != value:
                        raise ValueError(f'non-reproducible package: {output}')
                else:
                    output.write_bytes(value)
            if not count:
                raise ValueError('No packages found')
            print(f'{count} packages {"verified" if args.check else "built"}.')
        else:
            for name, value in generated(root).items():
                output = root / name
                if args.check:
                    if not output.exists() or output.read_bytes() != value.encode():
                        raise ValueError(f'stale generated file: {name}')
                else:
                    output.write_bytes(value.encode())
            print('Catalog, manifest and checksums verified.' if args.check else 'Catalog, manifest and checksums generated.')
        return 0
    except (OSError, ValueError, yaml.YAMLError, zipfile.BadZipFile) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
