#!/usr/bin/env python3
"""Prepare a deterministic local bundle. No network, Git operations or publishing."""
import argparse
import hashlib
import io
import os
import stat
import re
import sys
import zipfile
from pathlib import Path
import skill_repository as repo

RELEASE_ROOTS = ['claude','openai/chatgpt','microsoft/copilot','cursor','gemini','perplexity','shared','templates',
                 'docs','tools','evaluations','schemas','specs']
RELEASE_FILES = ['LICENSE','README.md','openai/README.md','microsoft/README.md','CATALOG.md','catalog.json','SHA256SUMS','CONTRIBUTING.md','requirements-dev.txt','changelog.md','completed-projects.md',
                                  'completed-upgrades.md','skill-improvement-assessment.md',
                                  '.github/github-social-preview.jpg','.github/workflow-templates/release.yml',
                                  '.github/workflows/resume-writer-tips-refresh.yml','.github/workflows/validate.yml']

def assert_release_source(root, path):
    """Reject links in every component below the canonical checkout boundary."""
    try:
        relative = path.relative_to(root)
    except ValueError:
        raise ValueError(f'Release input outside repository: {path}') from None
    if '..' in relative.parts:
        raise ValueError(f'Release input outside repository: {path}')
    current = root
    for part in relative.parts:
        current = current/part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            continue  # Missing required files are handled by validation/the read.
        if stat.S_ISLNK(metadata.st_mode) or getattr(metadata, 'st_reparse_tag', 0) == 0xA0000003:
            raise ValueError(f'Symlink or junction in release source: {relative}')
    if not path.resolve().is_relative_to(root):
        raise ValueError(f'Release input outside repository: {path}')

def preflight_sources(root):
    # Check explicit hidden inputs and all visible validation inputs before any
    # content read. Hidden anchor targets are checked at the validator read site.
    for name in RELEASE_FILES:
        assert_release_source(root, root/name)
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [name for name in dirs if not name.startswith('.')]
        for name in dirs + [name for name in files if not name.startswith('.')]:
            assert_release_source(root, Path(directory)/name)

def prepare(root, version, output):
    root = root.resolve()
    if not re.fullmatch(r'v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)', version):
        raise ValueError('Use an explicit vMAJOR.MINOR.PATCH repository version')
    preflight_sources(root)
    if not (root/'LICENSE').read_text(encoding='utf-8').strip():
        raise ValueError('Owner decision required: LICENSE is empty; release preparation blocked')
    count, errors = repo.validate(root, source_guard=lambda path: assert_release_source(root, path))
    for name, content in repo.generated(root).items():
        if not (root/name).exists() or (root/name).read_bytes() != content.encode():
            errors.append(f'{name} is stale')
    if errors:
        raise ValueError('Repository validation failed: '+'; '.join(errors))
    output = output.resolve()
    if output.exists() or output.is_relative_to(root):
        raise ValueError('Use a new output directory outside the source repository')
    files = [root/name for name in RELEASE_FILES]
    roots = RELEASE_ROOTS
    for name in roots:
        for path in (root/name).rglob('*'):
            rel = path.relative_to(root)
            if any(part.startswith('.') or part=='__pycache__' for part in rel.parts): continue
            if path.name=='future-upgrades.md' or path.suffix in ('.pyc','.pyo'): continue
            if path.is_symlink(): raise ValueError(f'Symlink in release source: {rel}')
            if path.is_file(): files.append(path)
    memory = io.BytesIO()
    with zipfile.ZipFile(memory,'w',compression=zipfile.ZIP_STORED) as archive:
        for path in sorted(set(files), key=lambda path: path.relative_to(root).as_posix()):
            assert_release_source(root, path)
            info=zipfile.ZipInfo(path.relative_to(root).as_posix(),(1980,1,1,0,0,0))
            info.create_system=3; info.external_attr=0o100644<<16
            archive.writestr(info,repo.canonical_bytes(path))
    data=memory.getvalue()
    output.mkdir(parents=True)
    name=f'ai-skills-{version}.zip'
    (output/name).write_bytes(data)
    (output/'SHA256SUMS').write_bytes(f'{hashlib.sha256(data).hexdigest()}  {name}\n'.encode('utf-8'))
    return count

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version',required=True)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    try:
        count=prepare(repo.ROOT,args.version,args.output)
        print(f'Prepared local bundle with {count} skills. Nothing published.')
        return 0
    except (OSError,ValueError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
