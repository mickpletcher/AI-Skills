#!/usr/bin/env python3
"""Prepare a deterministic local bundle. No network, Git operations or publishing."""
import argparse
import hashlib
import io
import re
import sys
import zipfile
from pathlib import Path
import skill_repository as repo

def prepare(root, version, output):
    root = root.resolve()
    if not re.fullmatch(r'v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)', version):
        raise ValueError('Use an explicit vMAJOR.MINOR.PATCH repository version')
    if not (root/'LICENSE').read_text().strip():
        raise ValueError('Owner decision required: LICENSE is empty; release preparation blocked')
    count, errors = repo.validate(root)
    for name, content in repo.generated(root).items():
        if not (root/name).exists() or (root/name).read_bytes() != content.encode():
            errors.append(f'{name} is stale')
    if errors:
        raise ValueError('Repository validation failed: '+'; '.join(errors))
    output = output.resolve()
    if output.exists() or output.is_relative_to(root):
        raise ValueError('Use a new output directory outside the source repository')
    # Only reviewed repository surfaces; no hidden/local metadata or local planning.
    roots = ['claude','chatgpt','copilot','cursor','gemini','perplexity','shared','templates',
             'docs','tools','evaluations','schemas','specs']
    files = [root/name for name in ['LICENSE','README.md','CATALOG.md','catalog.json','SHA256SUMS','CONTRIBUTING.md','requirements-dev.txt','changelog.md','completed-projects.md',
                                  'completed-upgrades.md','skill-improvement-assessment.md',
                                  '.github/github-social-preview.jpg','.github/workflow-templates/release.yml',
                                  '.github/workflows/resume-writer-tips-refresh.yml','.github/workflows/validate.yml']]
    for name in roots:
        for path in (root/name).rglob('*'):
            rel = path.relative_to(root)
            if any(part.startswith('.') or part=='__pycache__' for part in rel.parts): continue
            if path.name=='future-upgrades.md' or path.suffix in ('.pyc','.pyo'): continue
            if path.is_symlink(): raise ValueError(f'Symlink in release source: {rel}')
            if path.is_file(): files.append(path)
    memory = io.BytesIO()
    with zipfile.ZipFile(memory,'w',compression=zipfile.ZIP_STORED) as archive:
        for path in sorted(set(files)):
            info=zipfile.ZipInfo(path.relative_to(root).as_posix(),(1980,1,1,0,0,0))
            info.create_system=3; info.external_attr=0o100644<<16
            archive.writestr(info,repo.canonical_bytes(path))
    data=memory.getvalue()
    output.mkdir(parents=True)
    name=f'ai-skills-{version}.zip'
    (output/name).write_bytes(data)
    (output/'SHA256SUMS').write_text(f'{hashlib.sha256(data).hexdigest()}  {name}\n')
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
