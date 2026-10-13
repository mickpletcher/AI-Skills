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

    def test_symlinks_are_rejected_before_any_source_content_read(self):
        from unittest.mock import patch
        cases = [('LICENSE', False), ('README.md', False), ('catalog.json', False),
                 ('SHA256SUMS', False), ('.github/workflows/validate.yml', False),
                 ('.github', True), ('.github/workflows', True), ('docs', True),
                 ('schemas', True), ('claude/skills/example', True),
                 ('claude/skills/example/SKILL.md', False),
                 ('claude/skills/example/example.skill', False), ('extra.md', False)]
        for name, directory in cases:
            for target_kind in ('external', 'internal', 'missing'):
                with self.subTest(name=name, target=target_kind), tempfile.TemporaryDirectory() as tmp:
                    base = Path(tmp).resolve(); root = base/'source'; root.mkdir()
                    (root/'LICENSE').write_text('TEST FIXTURE ONLY')
                    target = (root if target_kind == 'internal' else base)/'target'
                    if target_kind != 'missing':
                        if directory: target.mkdir()
                        else: target.write_text('fixture data')
                    link = root/name; link.parent.mkdir(parents=True, exist_ok=True)
                    if link.exists(): link.unlink()
                    try: link.symlink_to(target, target_is_directory=directory)
                    except OSError as exc:
                        if getattr(exc, 'winerror', None) == 1314: self.skipTest('Windows symlink privilege unavailable')
                        raise
                    output = base/'release'
                    with patch.object(Path, 'read_text', side_effect=AssertionError('content read before preflight')), \
                         patch.object(Path, 'read_bytes', side_effect=AssertionError('content read before preflight')):
                        with self.assertRaisesRegex(ValueError, 'Symlink|outside'):
                            prepare_release.prepare(root, 'v1.2.3', output)
                    self.assertFalse(output.exists())

    def test_release_source_guard_rejects_outside_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()/'source'; root.mkdir()
            outside = root.parent/'outside'; outside.write_text('fixture')
            for path in (outside, root/'..'/'outside'):
                with self.assertRaisesRegex(ValueError, 'outside'):
                    prepare_release.assert_release_source(root, path)

    def test_hidden_markdown_anchor_target_is_guarded(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve(); root = base/'source'; root.mkdir()
            outside = base/'outside'; outside.mkdir()
            (outside/'target.md').write_text('# Secret heading\n')
            (root/'README.md').write_text('[target](.hidden/target.md#secret-heading)\n')
            try: (root/'.hidden').symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                if getattr(exc, 'winerror', None) == 1314: self.skipTest('Windows symlink privilege unavailable')
                raise
            with self.assertRaisesRegex(ValueError, 'Symlink|outside'):
                repo.link_errors(root, source_guard=lambda path: prepare_release.assert_release_source(root, path))

    def test_release_bytes_have_portable_order_and_encoding(self):
        import hashlib
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp); root = base/'source'; root.mkdir()
            for name in prepare_release.RELEASE_FILES:
                path = root/name; path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'fixture\n')
            (root/'docs').mkdir()
            for name in ('Z.txt', 'a.txt', 'caf\u00e9.txt'):
                (root/'docs'/name).write_bytes(b'content\r\n')
            output = base/'output'
            with patch.object(repo, 'validate', return_value=(1, [])), patch.object(repo, 'generated', return_value={}):
                prepare_release.prepare(root, 'v1.2.3', output)
            data = (output/'ai-skills-v1.2.3.zip').read_bytes()
            with zipfile.ZipFile(output/'ai-skills-v1.2.3.zip') as archive:
                self.assertEqual(archive.namelist(), sorted(archive.namelist()))
                self.assertEqual(archive.read('docs/caf\u00e9.txt'), b'content\n')
            self.assertEqual((output/'SHA256SUMS').read_bytes(),
                             (hashlib.sha256(data).hexdigest()+'  ai-skills-v1.2.3.zip\n').encode('utf-8'))
            # Same fixture checksum is required on every CI operating system.
            self.assertEqual(hashlib.sha256(data).hexdigest(), '98cdf0593c43ad3f42afb4787f8d9221bd4cde28cfceed51da3bb7c495c277ab')

    @unittest.skipUnless(sys.platform == 'win32', 'Windows junction semantics')
    def test_windows_junction_parent_is_rejected(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve(); root = base/'source'; root.mkdir()
            outside = base/'outside'; outside.mkdir()
            (outside/'input.md').write_text('fixture')
            junction = root/'docs'
            result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(junction), str(outside)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            with self.assertRaisesRegex(ValueError, 'junction|outside'):
                prepare_release.assert_release_source(root, junction/'input.md')
