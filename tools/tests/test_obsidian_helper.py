import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HELPER = Path(__file__).resolve().parents[2] / 'master-skills/idea-forge/scripts/save_to_obsidian.py'


class ObsidianHelperTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.vault = self.root / 'vault'
        self.vault.mkdir()
        self.body = self.root / 'body.txt'
        self.body.write_text('Résumé idea\nSecond line\n', encoding='utf-8')

    def save(self, title='Sample', folder='Ideas', vault=None):
        return subprocess.run([sys.executable, str(HELPER), '--vault-path', str(vault or self.vault),
                               '--body-file', str(self.body), '--title', title, '--folder', folder],
                              capture_output=True, text=True, timeout=20)

    def test_new_nested_note_preserves_body_and_source(self):
        result = self.save(title='Résumé: /sample?', folder='Ideas/Nested')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.vault / 'Ideas/Nested/Résumé sample.md').read_text(encoding='utf-8'),
                         '# Résumé: /sample?\n\nRésumé idea\nSecond line\n')
        self.assertEqual(self.body.read_text(encoding='utf-8'), 'Résumé idea\nSecond line\n')

    def test_existing_note_and_sanitized_title_collision_are_preserved(self):
        self.assertEqual(self.save(title='Same:Title').returncode, 0)
        note = self.vault / 'Ideas/SameTitle.md'
        before = note.read_bytes()
        for title in ('Same:Title', 'Same?Title'):
            with self.subTest(title=title):
                result = self.save(title=title)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('already exists', result.stderr)
                self.assertEqual(note.read_bytes(), before)

    def test_absolute_drive_unc_and_parent_folders_fail_without_writes(self):
        for folder in ('../outside', 'Ideas/../../outside', '..\\outside', str(self.root / 'absolute'),
                       'C:\\outside', 'C:outside', '\\\\server\\share'):
            with self.subTest(folder=folder):
                result = self.save(folder=folder)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(list(self.vault.iterdir()))
                self.assertEqual({p.name for p in self.root.iterdir()}, {'vault', 'body.txt'})

    def test_vault_must_be_an_existing_directory(self):
        self.assertNotEqual(self.save(vault=self.root / 'missing').returncode, 0)
        self.assertNotEqual(self.save(vault=self.body).returncode, 0)

    def test_linked_folder_outside_vault_is_rejected(self):
        outside = self.root / 'outside'
        outside.mkdir()
        link = self.vault / 'Linked'
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError as error:
            if os.name != 'nt':
                raise
            result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(outside)],
                                    capture_output=True, text=True)
            if result.returncode:
                self.skipTest(f'Cannot create a symlink or junction: {error}')
        result = self.save(folder='Linked/Nested')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(list(outside.iterdir()))

    def test_existing_note_link_does_not_change_its_target(self):
        outside = self.root / 'original.md'
        outside.write_text('Existing content', encoding='utf-8')
        ideas = self.vault / 'Ideas'
        ideas.mkdir()
        try:
            (ideas / 'Sample.md').hardlink_to(outside)
        except OSError as error:
            self.skipTest(f'Hardlinks unavailable: {error}')
        self.assertNotEqual(self.save().returncode, 0)
        self.assertEqual(outside.read_text(encoding='utf-8'), 'Existing content')

    def test_concurrent_saves_have_one_winner(self):
        command = [sys.executable, str(HELPER), '--vault-path', str(self.vault),
                   '--body-file', str(self.body), '--title', 'Concurrent']
        processes = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        for process in processes:
            process.communicate(timeout=20)
        self.assertEqual(sorted(process.returncode for process in processes), [0, 1])
        self.assertEqual((self.vault / 'Ideas/Concurrent.md').read_text(encoding='utf-8'),
                         '# Concurrent\n\nRésumé idea\nSecond line\n')


if __name__ == '__main__':
    unittest.main()
