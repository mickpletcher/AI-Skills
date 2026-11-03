"""Synthetic artifact checks, not native-model or DOCX-layout certification."""
import hashlib
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / 'master-skills/resume-writer'
spec = importlib.util.spec_from_file_location('verify_pagination', SKILL / 'scripts/verify_pagination.py')
pagination = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pagination)


def make_pdf(path, count):
    """Small real PDF with explicit pages and vector content (no font dependency)."""
    pages = [4 + 2 * i for i in range(count)]
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>',
               f'<< /Type /Pages /Kids [{" ".join(f"{p} 0 R" for p in pages)}] /Count {count} >>'.encode(),
               b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>']
    for i, page in enumerate(pages):
        objects.append(f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << >> /Contents {page + 1} 0 R >>'.encode())
        stream = f'0 0 0 rg 72 {720 - i * 10} 120 2 re f'.encode()
        objects.append(f'<< /Length {len(stream)} >>\nstream\n'.encode() + stream + b'\nendstream')
    data = b'%PDF-1.4\n'
    offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(data))
        data += f'{i} 0 obj\n'.encode() + obj + b'\nendobj\n'
    xref = len(data)
    data += f'xref\n0 {len(offsets)}\n0000000000 65535 f \n'.encode()
    data += b''.join(f'{offset:010d} 00000 n \n'.encode() for offset in offsets[1:])
    data += f'trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode()
    path.write_bytes(data)
    return data


class ResumePaginationTests(unittest.TestCase):
    def test_missing_renderer_is_not_a_fit_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'resume.pdf'
            make_pdf(path, 2)
            with patch.object(pagination.shutil, 'which', return_value=None):
                result = pagination.verify(path)
            self.assertEqual(result['status'], 'unverified')
            self.assertIsNone(result['rendered_pages'])
            self.assertIsNone(result['within_two_pages'])
            self.assertIn('Missing renderer tools', result['limitations'][0])

    def test_docx_and_invalid_pdf_are_not_estimated_as_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ('resume.docx', 'resume.pdf'):
                path = Path(tmp) / name
                path.write_bytes(b'Only 100 words; not pagination evidence')
                result = pagination.verify(path)
                self.assertEqual(result['status'], 'unverified')
                self.assertIsNone(result['within_two_pages'])

    def test_failed_render_is_unverified(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'resume.pdf'
            make_pdf(path, 2)
            with patch.object(pagination.shutil, 'which', return_value='tool'), patch.object(pagination.subprocess, 'run', side_effect=subprocess.TimeoutExpired('tool', 90)):
                result = pagination.verify(path)
            self.assertEqual(result['status'], 'unverified')
            self.assertIsNone(result['rendered_pages'])

    def test_renderer_warnings_and_missing_pages_stay_unverified(self):
        for warning, image_count in [('font substitution warning', 2), ('', 1)]:
            with self.subTest(warning=warning, image_count=image_count), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / 'resume.pdf'
                make_pdf(path, 2)
                def run(args, **kwargs):
                    if '-png' not in args:
                        return subprocess.CompletedProcess(args, 0, 'Pages: 2\n', '')
                    for index in range(image_count):
                        Path(args[-1] + f'-{index + 1}.png').write_bytes(b'synthetic image bytes')
                    return subprocess.CompletedProcess(args, 0, '', warning)
                with patch.object(pagination.shutil, 'which', return_value='tool'), patch.object(pagination.subprocess, 'run', side_effect=run):
                    result = pagination.verify(path)
                self.assertEqual(result['status'], 'unverified')
                self.assertIsNone(result['within_two_pages'])

    @unittest.skipUnless(shutil.which('pdfinfo') and shutil.which('pdftoppm'), 'Optional Poppler renderer unavailable')
    def test_actual_pdf_render_counts_and_source_preservation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'resume.pdf'
            for count in (1, 2, 3):
                with self.subTest(count=count):
                    data = make_pdf(path, count)
                    result = pagination.verify(path)
                    self.assertEqual(result['status'], 'rendered', result)
                    self.assertEqual(result['rendered_pages'], count)
                    self.assertEqual(result['within_two_pages'], count <= 2)
                    self.assertEqual(result['sha256'], hashlib.sha256(data).hexdigest())
                    self.assertEqual(path.read_bytes(), data)
                    self.assertEqual(list(Path(tmp).iterdir()), [path])

    def test_workflow_evidence_boundary_and_json_compatibility(self):
        text = (SKILL / 'references/enhance-workflow.md').read_text(encoding='utf-8')
        self.assertNotIn('Resume already fits two pages', text)
        for phrase in ('Estimation is not pagination evidence', 'original never verifies the rewrite',
                       'intended fonts', 'actual pagination remains unverified',
                       'existing `notes` string array', 'Rerender and recount after any content or layout change'):
            self.assertIn(phrase, text)


if __name__ == '__main__':
    unittest.main()
