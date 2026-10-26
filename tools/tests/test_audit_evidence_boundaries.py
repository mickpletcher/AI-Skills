"""Static instruction/fixture contracts; never execute fixture scripts or models."""
import ast
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


class AuditEvidenceBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads((ROOT / 'evaluations/fixtures/audit-evidence-boundaries.json').read_text())
        cls.cases = {case['id']: case for case in cls.fixture['cases']}

    def test_distinct_shipped_sources_cover_both_contracts(self):
        self.assertEqual(self.fixture['sources'], [
            'cursor/skills/repo-assessment/instructions.md',
            'microsoft/copilot/skills/repo-cleanup-audit/instructions.md'])
        for source in self.fixture['sources']:
            text = (ROOT / source).read_text()
            for requirement in (
                'Inspect proposed audit commands and their invoked scripts/configuration',
                'does not authorize those side effects', 'existing explicit authorization',
                'leave the command unrun', 'Continue independent read-only inspection',
                'commit SHA when available', 'staged, unstaged and untracked changes',
                'command/workflow, result and tested revision/local state',
                'Passing CI for an older revision does not validate the current tree',
                'compare the available revision/status with the initial snapshot',
                'mark affected findings stale', 'withhold the affected conclusion',
                'Do not overwrite, reset or discard concurrent user changes'):
                with self.subTest(source=source, requirement=requirement):
                    self.assertIn(requirement, text)

    def test_side_effect_fixture_contains_real_write_and_network_operations(self):
        case = self.cases['audit-command-effects']
        self.assertIn('python scripts/check.py', case['files']['Makefile'])
        tree = ast.parse(case['files']['scripts/check.py'])
        calls = [node.func for node in ast.walk(tree) if isinstance(node, ast.Call)]
        self.assertTrue(any(isinstance(f, ast.Attribute) and f.attr == 'write_text' for f in calls))
        self.assertTrue(any(isinstance(f, ast.Name) and f.id == 'urlopen' for f in calls))
        self.assertEqual(case['expected']['unrun'], ['make check'])
        self.assertIn('https://service.invalid/check', case['files']['scripts/check.py'])

    def test_snapshot_fixture_requires_revising_old_cleanup_conclusion(self):
        case = self.cases['audit-stale-snapshot']
        self.assertNotEqual(case['initial_revision'], case['current_revision'])
        self.assertEqual(case['historical_check']['revision'], case['initial_revision'])
        self.assertEqual(case['historical_check']['result'], 'passed')
        artifact = 'dist/template.json'
        self.assertNotIn(artifact, case['initial_files']['release-manifest.txt'])
        self.assertIn(artifact, case['files']['release-manifest.txt'])
        self.assertIn(' M release-manifest.txt', case['current_git_status'])
        self.assertIn('?? notes.md', case['current_git_status'])
        self.assertIn(artifact, case['expected']['preserve'])

    def test_scenarios_remain_unrun_and_preservation_paths_exist(self):
        self.assertEqual(self.fixture['behavior_status'], 'not_run')
        self.assertEqual(len(self.cases), 2)
        for case in self.cases.values():
            self.assertTrue(case['prompt'])
            self.assertGreaterEqual(len(case['expected']['rubric']), 3)
            self.assertLessEqual(set(case['expected']['preserve']), set(case['files']))
