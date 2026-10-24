import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'master-skills/patentforge-provisional/scripts/validate_package.py'
spec = importlib.util.spec_from_file_location('validate_package', SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def package():
    return '# Working draft\n\n' + ''.join(f'## {n}. Section\n\nMechanism remains unverified.\n\n' for n in range(1, 15))


class PatentPackageTests(unittest.TestCase):
    def test_complete_short_package_and_crlf(self):
        text = package().replace('unverified', 'unverified caf\u00e9')
        self.assertEqual(validator.validate(text), validator.validate(text.replace('\n', '\r\n')))

    def test_total_limit_counts_entire_response(self):
        text = package()
        text += ' extra' * (1200 - len(text.split()))
        self.assertEqual(validator.validate(text)[0], 1200)
        with self.assertRaisesRegex(ValueError, 'package 1201/1200'):
            validator.validate(text + ' extra')

    def test_section_ten_limit_includes_subheadings(self):
        text = package().replace('## 11.', '### Abstract\n\nSummary.\n\n## 11.')
        draft = text.split('## 10.')[1].split('## 11.')[0]
        text = text.replace('### Abstract', 'word ' * (300 - len(('## 10.' + draft).split())) + '### Abstract')
        self.assertEqual(validator.validate(text)[1], 300)
        with self.assertRaisesRegex(ValueError, 'section 10 301/300'):
            validator.validate(text.replace('Summary.', 'Summary. extra'))

    def test_cutoffs_duplicates_and_empty_sections_fail(self):
        text = package()
        bad = [text.split('## 14.')[0], text.replace('## 14.', '## 13.'), text.replace('## 1.', '## 2.', 1), text.replace('Mechanism remains unverified.\n\n## 2.', '## 2.', 1)]
        for item in bad:
            with self.subTest(item=item), self.assertRaises(ValueError):
                validator.validate(item)

    def test_over_limit_capture_shape_and_explicit_user_limits(self):
        text = package().replace('## 11.', 'word ' * 370 + '\n\n## 11.')
        text += ' word' * (1409 - len(text.split()))
        with self.assertRaisesRegex(ValueError, 'package 1409/1200; section 10 376/300'):
            validator.validate(text)
        self.assertEqual(validator.validate(text, 1500, 400), (1409, 376))
        with self.assertRaisesRegex(ValueError, 'positive'):
            validator.validate(package(), 0, 300)

    def test_cli_reads_exact_file_without_mutation(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'package.md'
            for text, expected in [(package(), 0), (package() + ' word' * 1200, 2)]:
                data = text.encode('utf-8')
                path.write_bytes(data)
                result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True)
                self.assertEqual(result.returncode, expected)
                self.assertEqual(path.read_bytes(), data)


if __name__ == '__main__':
    unittest.main()
