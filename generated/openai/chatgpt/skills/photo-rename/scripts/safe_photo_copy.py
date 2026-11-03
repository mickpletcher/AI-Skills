#!/usr/bin/env python3
"""Plan or explicitly copy flat photo batches; never delete or rename originals.

For a trusted, quiescent local directory only. This is not a sandbox against
concurrent directory replacement. Stop other writers before applying a plan.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import unicodedata


def key(name):
    return unicodedata.normalize('NFC', name).casefold()


def linked(path):
    info = path.lstat()
    # Covers Windows junctions/reparse points on Python 3.10/3.11 too.
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, 'st_file_attributes', 0) & 0x400)


def folder(value):
    path = Path(value).absolute()
    for part in (path, *path.parents):
        if linked(part):
            raise ValueError('Linked directories are not supported')
    if not path.is_dir():
        raise ValueError('Folder must already exist')
    return path.resolve(strict=True)


def basename(name):
    if not isinstance(name, str) or not name or name in ('.', '..') or any(c in name for c in '/\\:') or any(ord(c) < 32 for c in name):
        raise ValueError('Expected a plain filename, not a path')
    if name.endswith((' ', '.')):
        raise ValueError('Trailing spaces and dots are not supported')
    return name


def source_file(root, name):
    p = root / basename(name)
    if linked(p) or not stat.S_ISREG(p.lstat().st_mode):
        raise ValueError('Source must be a regular, non-linked file')
    if p.resolve(strict=True).parent != root:
        raise ValueError('Source escaped its folder')
    return p


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def plan(source, destination, requests):
    src, dst = folder(source), folder(destination)
    occupied = {key(p.name) for p in dst.iterdir()}
    seen = set()
    rows = []
    for old, proposed in requests:
        p = source_file(src, old)
        if key(old) in seen:
            raise ValueError('Duplicate or case-ambiguous source')
        seen.add(key(old))
        basename(proposed)
        ext = p.suffix
        if not re.fullmatch(r'\.[A-Za-z0-9]+', ext) or Path(proposed).suffix != ext:
            raise ValueError('Preserve the exact source extension')
        stem = proposed[:-len(ext)]
        if not re.fullmatch(r'[a-z0-9]+(?:_[a-z0-9]+)*', stem) or stem.upper() in {'CON','PRN','AUX','NUL', *(f'COM{i}' for i in range(1,10)), *(f'LPT{i}' for i in range(1,10))}:
            raise ValueError('Use a portable snake_case basename')
        target, n = proposed, 1
        while key(target) in occupied:
            target = f'{stem}_{n:02d}{ext}'
            n += 1
        occupied.add(key(target))
        rows.append({'source': old, 'destination': target, 'sha256': sha(p), 'status': 'planned'})
    return {'source_folder': str(src), 'destination_folder': str(dst), 'operation': 'copy', 'files': rows}


def apply(plan_data):
    """Revalidate entire plan before writes, then return honest per-file outcomes."""
    src, dst = folder(plan_data['source_folder']), folder(plan_data['destination_folder'])
    rows = plan_data['files']
    # Re-plan to validate filenames, duplicates, containment, hashes and collisions.
    checked = plan(src, dst, [(r['source'], r['destination']) for r in rows])
    if checked != plan_data:
        raise ValueError('Plan changed, destination occupied, or source hash changed; replan and review')
    results = []
    for row in rows:
        result = dict(row, status='not_copied')
        try:
            folder(src); folder(dst)
            original = source_file(src, row['source'])
            if sha(original) != row['sha256']:
                raise ValueError('Source changed since review')
            if key(row['destination']) in {key(p.name) for p in dst.iterdir()}:
                raise ValueError('Destination became occupied; no overwrite')
            target = dst / basename(row['destination'])
            # Exclusive creation refuses an existing file, directory, or symlink.
            with original.open('rb') as reader, target.open('xb') as writer:
                result['status'] = 'incomplete_copy'
                for block in iter(lambda: reader.read(1024 * 1024), b''):
                    writer.write(block)
            if sha(target) != row['sha256'] or sha(original) != row['sha256']:
                raise ValueError('Hash verification failed; original not deleted')
            result['status'] = 'copied_verified'
        except (OSError, ValueError) as exc:
            result['error'] = str(exc)
        results.append(result)
        if 'error' in result:
            results.extend(dict(r, status='not_attempted') for r in rows[len(results):])
            break
    return dict(plan_data, files=results)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('plan')
    p.add_argument('source_folder'); p.add_argument('destination_folder')
    p.add_argument('requests', help='JSON array of [source filename, proposed filename] pairs')
    p = sub.add_parser('copy')
    p.add_argument('plan_file'); p.add_argument('--approved', action='store_true', required=True)
    args = parser.parse_args()
    if args.command == 'plan':
        result = plan(args.source_folder, args.destination_folder, json.loads(Path(args.requests).read_text()))
    else:
        result = apply(json.loads(Path(args.plan_file).read_text()))
    print(json.dumps(result, indent=2))
    return int(any('error' in r for r in result['files']))


if __name__ == '__main__':
    raise SystemExit(main())
