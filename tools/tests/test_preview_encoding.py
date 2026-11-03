"""Real JPEG encoding checks, not model/host evaluations. No network needed."""
import contextlib
import importlib.util
import io
from pathlib import Path
import random
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
try:
    from PIL import Image
except ImportError:
    Image = None


@unittest.skipIf(Image is None, 'Pillow optional helper dependency unavailable')
class PreviewEncodingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / 'master-skills/github-social-preview/scripts/generate_preview.py'
        spec = importlib.util.spec_from_file_location('preview_encoding_subject', path)
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def noise(self):
        image = Image.frombytes('RGB', (1280, 640), random.Random(42).randbytes(1280 * 640 * 3))
        image.info['footer_layout'] = {'tags': [], 'language': None, 'tags_requested': 0}
        return image

    def test_forced_compression_encodes_exact_dimensions_and_actual_bytes(self):
        m = self.module
        image = self.noise()
        sizes = []
        for quality in (92, 85, 75, 65, 55, 40):
            buf = io.BytesIO()
            image.save(buf, format='JPEG', quality=quality, optimize=True)
            sizes.append(len(buf.getvalue()))
        self.assertLess(sizes[-1], sizes[-2])
        with tempfile.TemporaryDirectory() as tmp, patch.object(m, 'MAX_BYTES', sizes[-2]):
            path = Path(tmp) / 'preview.jpg'
            size, quality = m.compress_to_limit(image, str(path))
            self.assertEqual(quality, 40)  # equality at quality 55 must not pass
            self.assertEqual(size, path.stat().st_size)
            self.assertLess(size, m.MAX_BYTES)
            with Image.open(path) as actual:
                actual.load()
                self.assertEqual(actual.size, (1280, 640))
                self.assertEqual(actual.format, 'JPEG')

    def test_failure_preserves_existing_destination_and_does_not_create_new(self):
        m = self.module
        with tempfile.TemporaryDirectory() as tmp, patch.object(m, 'MAX_BYTES', 1):
            for existing in (False, True):
                path = Path(tmp) / str(existing)
                if existing:
                    path.write_bytes(b'previous artifact')
                with self.assertRaisesRegex(ValueError, 'Destination unchanged'):
                    m.compress_to_limit(self.noise(), str(path))
                self.assertEqual(path.exists(), existing)
                if existing:
                    self.assertEqual(path.read_bytes(), b'previous artifact')

    def test_wrong_dimensions_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'Expected 1280x640'):
                self.module.compress_to_limit(Image.new('RGB', (1152, 576)), str(Path(tmp) / 'x.jpg'))

    def run_cli(self, path, limit, image):
        m = self.module
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch('sys.argv', ['generate_preview.py', '--title', 'Synthetic', '--output', str(path)]), \
                patch.object(m, 'generate_image', return_value=image), patch.object(m, 'MAX_BYTES', limit), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                m.main()
                status = 0
            except SystemExit as exc:
                status = exc.code
        return status, stdout.getvalue(), stderr.getvalue()

    def test_cli_success_reports_decoded_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'preview.jpg'
            status, stdout, stderr = self.run_cli(path, 400000, self.noise())
            self.assertEqual(status, 0, stderr)
            with Image.open(path) as actual:
                self.assertIn(f'Dims:   {actual.width}x{actual.height}', stdout)
            self.assertIn(f'{path.stat().st_size:,} bytes', stdout)
            self.assertIn('dimensions: PASS', stdout)
            self.assertIn('file_size: PASS', stdout)
            self.assertIn('Format: JPEG', stdout)

    def test_cli_size_failure_is_nonzero_without_success_checklist(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'preview.jpg'
            status, stdout, stderr = self.run_cli(path, 1, self.noise())
            self.assertEqual(status, 1)
            self.assertIn('ERROR:', stderr)
            self.assertNotIn('PASS', stdout)
            self.assertFalse(path.exists())

    def test_cli_rechecks_saved_dimensions_not_original_canvas(self):
        m = self.module
        def wrong_output(image, path):
            Image.new('RGB', (1152, 576)).save(path, format='JPEG')
            return Path(path).stat().st_size, 40
        with tempfile.TemporaryDirectory() as tmp, patch.object(m, 'compress_to_limit', side_effect=wrong_output):
            status, stdout, stderr = self.run_cli(Path(tmp) / 'preview.jpg', 1000000, self.noise())
            self.assertEqual(status, 1)
            self.assertIn('Dims:   1152x576', stdout)
            self.assertIn('dimensions: FAIL', stdout)
            self.assertIn('ERROR:', stderr)
