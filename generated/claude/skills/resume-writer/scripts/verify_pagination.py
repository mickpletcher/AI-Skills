#!/usr/bin/env python3
"""Render a PDF snapshot and count its pages; never infer pagination from text.

No DOCX conversion or visual-quality certification. Requires Poppler's pdfinfo and
pdftoppm on PATH. JSON evidence applies only to the SHA-256-identified PDF bytes.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


def verify(pdf):
    path = Path(pdf)
    result = dict(status='unverified', artifact=str(path), sha256=None,
                  rendered_pages=None, within_two_pages=None,
                  renderer='Poppler pdfinfo + pdftoppm', limitations=[])
    try:
        if path.suffix.lower() != '.pdf':
            raise ValueError('PDF required: export the intended DOCX/document layout first; no conversion was performed.')
        data = path.read_bytes()
        result['sha256'] = hashlib.sha256(data).hexdigest()
        if not data.startswith(b'%PDF-'):
            raise ValueError('Input is not a PDF.')
        info, render = shutil.which('pdfinfo'), shutil.which('pdftoppm')
        if not info or not render:
            raise ValueError('Missing renderer tools: ' + ', '.join(name for name, tool in [('pdfinfo', info), ('pdftoppm', render)] if not tool))
        with tempfile.TemporaryDirectory(prefix='resume-pagination-') as tmp:
            snapshot = Path(tmp) / 'artifact.pdf'
            snapshot.write_bytes(data)
            env = dict(os.environ, LC_ALL='C', LANG='C')
            counted = subprocess.run([info, str(snapshot)], capture_output=True, text=True, timeout=90, check=True, env=env)
            match = re.search(r'^Pages:\s+(\d+)\s*$', counted.stdout, re.M)
            if not match or int(match[1]) < 1:
                raise ValueError('pdfinfo did not provide a positive page count.')
            count = int(match[1])
            rendered = subprocess.run([render, '-r', '36', '-png', str(snapshot), str(Path(tmp) / 'page')], capture_output=True, text=True, timeout=90, check=True, env=env)
            pages = list(Path(tmp).glob('page-*.png'))
            if len(pages) != count or any(p.stat().st_size == 0 for p in pages):
                raise ValueError('Rendered page images do not match the PDF page count.')
            warnings = (counted.stderr + rendered.stderr).strip()
            if warnings:
                raise ValueError('Renderer warnings require review before verification: ' + warnings[:2000])
            result.update(status='rendered', rendered_pages=count, within_two_pages=count <= 2)
            result['limitations'].append('Count applies only to this PDF snapshot; DOCX pagination, font fidelity, clipping, readability and visual layout are not certified. Inspect the final artifact visually; rerun after edits.')
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        result['limitations'].append(str(exc))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf')
    args = parser.parse_args()
    result = verify(args.pdf)
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'rendered' else 2


if __name__ == '__main__':
    raise SystemExit(main())
