#!/usr/bin/env python3
"""Materialize a reviewed fictional scenario recipe after verifying source hashes."""
import argparse
import hashlib
import re
from pathlib import Path, PurePosixPath

from generate_fixtures import MAX_OUTPUT, encode, keys, read_spec, require


def verify_sources(recipe, source_root):
    root = source_root.resolve(strict=True)
    require(root.is_dir(), 'Source root must be a directory')
    keys(recipe, {'schema_version', 'synthetic', 'seed', 'source_revision', 'sources', 'requirements', 'cases'})
    require(type(recipe['schema_version']) is int and recipe['schema_version'] == 1 and recipe['synthetic'] is True,
            'Expected a version-1 explicitly synthetic recipe')
    require(type(recipe['seed']) is int, 'Recipe seed must be an integer')
    require(isinstance(recipe['source_revision'], str), 'Expected source revision context')
    require(isinstance(recipe['sources'], list) and 1 <= len(recipe['sources']) <= 100, 'Expected bounded source list')
    names = set()
    for source in recipe['sources']:
        keys(source, {'path', 'sha256', 'role'})
        require(isinstance(source['path'], str), 'Source path must be text')
        rel = PurePosixPath(source['path'])
        require(not rel.is_absolute() and rel.parts and all(p not in ('.', '..') for p in rel.parts)
                and '\\' not in source['path'] and ':' not in source['path'], 'Source path must stay within root')
        require(source['path'] not in names, 'Duplicate source path')
        names.add(source['path'])
        require(isinstance(source['sha256'], str) and re.fullmatch('[0-9a-f]{64}', source['sha256']), 'Expected source SHA-256')
        current = root
        for part in rel.parts:
            current /= part
            require(not current.is_symlink(), 'Symlink source is not supported')
        require(current.resolve(strict=True).is_relative_to(root) and current.is_file(), 'Source is not a local file within root')
        require(current.stat().st_size <= 4 * 1024 * 1024, 'Source exceeds 4 MiB inspection limit')
        require(hashlib.sha256(current.read_bytes()).hexdigest() == source['sha256'],
                f"Stale source: {source['path']}; re-analyze affected requirements before reuse")


def artifacts(recipe, source_root):
    verify_sources(recipe, source_root)
    require(isinstance(recipe['requirements'], list) and 1 <= len(recipe['requirements']) <= 100, 'Expected requirements ledger')
    requirements = set()
    source_paths = {source['path'] for source in recipe['sources']}
    for item in recipe['requirements']:
        keys(item, {'id', 'source', 'location', 'basis', 'requirement'})
        require(isinstance(item['id'], str) and item['id'] not in requirements, 'Duplicate requirement ID')
        require(isinstance(item['source'], str) and item['source'] in source_paths, 'Requirement needs a declared source')
        require(item['basis'] in ('explicit', 'derived', 'unresolved', 'historical'), 'Invalid requirement basis')
        require(all(isinstance(item[k], str) and item[k] for k in ('location', 'requirement')), 'Empty requirement evidence')
        requirements.add(item['id'])
    require(isinstance(recipe['cases'], list) and 1 <= len(recipe['cases']) <= 100, 'Expected 1–100 scenarios')
    output = {}
    ids = set()
    for case in recipe['cases']:
        keys(case, {'id', 'prompt', 'requirements', 'files', 'expected', 'oracle_basis'})
        require(isinstance(case['id'], str) and re.fullmatch('[a-z][a-z0-9-]{0,63}', case['id']) and case['id'] not in ids, 'Invalid or duplicate scenario ID')
        ids.add(case['id'])
        require(isinstance(case['prompt'], str) and case['prompt'], 'Scenario needs a prompt')
        require(isinstance(case['requirements'], list) and case['requirements'] and all(isinstance(r, str) and r in requirements for r in case['requirements']), 'Unknown scenario requirement')
        require(isinstance(case['expected'], dict) and isinstance(case['oracle_basis'], dict), 'Expected oracle objects')
        require(isinstance(case['files'], dict) and len(case['files']) <= 20, 'At most 20 files per scenario')
        for name, contents in case['files'].items():
            require(isinstance(name, str) and re.fullmatch(r'[a-z][a-z0-9_-]{0,63}\.(csv|json|txt)', name), 'Unsafe or unsupported scenario filename')
            require(isinstance(contents, str), 'Scenario files must be UTF-8 text')
            output[f"{case['id']}/{name}"] = contents.encode('utf-8')
    manifest = {'recipe': recipe,
                'materializer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'recipe_sha256': hashlib.sha256(encode(recipe)).hexdigest(),
                'seed_note': 'Fixed reviewed scenario recipe; seed labels its design context, not random resampling.', 'source_hash_verification': 'passed for listed files only',
                'revision_note': 'Recorded revision is provenance context; content hashes, not Git status or current HEAD, are checked.',
                'target_execution': 'not_run', 'application_outcomes': 'expected only; not observed',
                'file_sha256': {path: hashlib.sha256(raw).hexdigest() for path, raw in sorted(output.items())}}
    output['manifest.json'] = encode(manifest)
    require(sum(map(len, output.values())) <= MAX_OUTPUT, 'Scenario output exceeds 20 MiB limit')
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recipe', required=True, type=Path)
    parser.add_argument('--source-root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        planned = artifacts(read_spec(args.recipe), args.source_root)
        args.output.mkdir()
        for name, raw in planned.items():
            path = args.output / name
            path.parent.mkdir(exist_ok=True)
            with path.open('xb') as stream:
                stream.write(raw)
        print(f'Created fictional scenario pack: {args.output}; target execution not run')
    except (OSError, ValueError, TypeError, RecursionError) as error:
        parser.exit(2, f'error: {error}\n')


if __name__ == '__main__':
    main()
