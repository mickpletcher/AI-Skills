"""Static contracts and synthetic content comparison, not native host evaluation."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


class AuditContentSnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = json.loads((ROOT / 'evaluations/fixtures/audit-content-snapshot.json').read_text())

    def test_both_shipped_contracts_require_content_evidence(self):
        self.assertEqual(self.case['sources'], [
            'cursor/skills/repo-assessment/instructions.md',
            'microsoft/copilot/skills/repo-cleanup-audit/instructions.md'])
        for source in self.case['sources']:
            text = (ROOT / source).read_text()
            for clause in ('Capture content fingerprints', 'at the time of inspection',
                           'including already-modified and untracked files',
                           'compare that evidence with their current contents',
                           'unchanged commit SHA and Git status do not prove unchanged contents',
                           'if comparison is unavailable or the files keep changing',
                           'keep affected conclusions provisional',
                           'Treat missing or newly relevant paths as changed evidence',
                           'preserve concurrent user edits',
                           'Limit capture to the authorized inspection scope',
                           'do not publish sensitive file contents'):
                with self.subTest(source=source, clause=clause):
                    self.assertIn(clause, text)

    def test_identical_git_evidence_masks_two_content_changes(self):
        case = self.case
        self.assertEqual(case['initial_revision'], case['current_revision'])
        self.assertEqual(case['initial_git_status'], case['current_git_status'])
        self.assertIn(' M release-manifest.txt', case['current_git_status'])
        self.assertIn('?? notes.md', case['current_git_status'])
        before, after = case['initial_files'], case['current_files']
        digest = lambda text: hashlib.sha256(text.encode()).hexdigest()
        changed = sorted(p for p in set(before) | set(after)
                         if p not in before or p not in after or digest(before[p]) != digest(after[p]))
        self.assertEqual(changed, case['expected']['changed'])
        self.assertEqual(sorted(set(before) - set(changed)), case['expected']['unchanged'])
        self.assertNotIn('dist/template.json', before['release-manifest.txt'])
        self.assertIn('dist/template.json', after['release-manifest.txt'])
        self.assertIn('Preserve template', after['notes.md'])

    def test_fixture_is_unrun_and_preserves_current_evidence(self):
        case = self.case
        self.assertEqual(case['behavior_status'], 'not_run')
        self.assertEqual(set(case['expected']['preserve']), set(case['current_files']))
        self.assertGreaterEqual(len(case['expected']['rubric']), 4)
        self.assertTrue(any('unavailable' in rule and 'provisional' in rule
                            for rule in case['expected']['rubric']))
