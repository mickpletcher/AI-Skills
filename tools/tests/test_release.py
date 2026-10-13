import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import prepare_release
import skill_repository as repo

class ReleaseTests(unittest.TestCase):
    def test_empty_license_blocks_before_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'source'; root.mkdir()
            (root/'LICENSE').write_text('')
            output=Path(tmp)/'release'
            with self.assertRaisesRegex(ValueError,'LICENSE is empty'):
                prepare_release.prepare(root,'v1.2.3',output)
            self.assertFalse(output.exists())

    def test_invalid_version_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            for version in ('main','v01.2.3','v1.2','../bad'):
                with self.assertRaisesRegex(ValueError,'version'):
                    prepare_release.prepare(repo.ROOT,version,Path(tmp)/'release')

    def test_fixture_bundle_is_deterministic_and_does_not_overwrite(self):
        # A fixture string exercises the nonempty-file gate. It supplies no
        # license terms to the actual repository and is never distributed.
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)
            source=base/'source'
            shutil.copytree(repo.ROOT,source,ignore=shutil.ignore_patterns('.git','.venv','__pycache__'))
            (source/'LICENSE').write_text('TEST FIXTURE ONLY; not repository licensing terms.\n')
            first,second=base/'first',base/'second'
            prepare_release.prepare(source,'v1.2.3',first)
            prepare_release.prepare(source,'v1.2.3',second)
            self.assertEqual((first/'ai-skills-v1.2.3.zip').read_bytes(),(second/'ai-skills-v1.2.3.zip').read_bytes())
            self.assertEqual((first/'SHA256SUMS').read_bytes(),(second/'SHA256SUMS').read_bytes())
            extracted=base/'extracted'
            with zipfile.ZipFile(first/'ai-skills-v1.2.3.zip') as archive:
                archive.extractall(extracted)  # our own deterministic fixture bundle
            self.assertEqual(repo.validate(extracted.resolve())[1], [])
            with self.assertRaisesRegex(ValueError,'new output directory'):
                prepare_release.prepare(source,'v1.2.3',first)
