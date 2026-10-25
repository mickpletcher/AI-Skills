"""Offline fixture/evidence and contract regressions, never model evaluations."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from skill_repository import link_errors
import generate_master_skills as generator


class QualityImprovementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads((ROOT / 'evaluations/fixtures/first-quality-improvements.json').read_text())
        cls.cases = {case['id']: case for case in cls.fixture['cases']}

    def test_checkout_success_does_not_imply_archive_success(self):
        case = self.cases['readme-distribution']
        with tempfile.TemporaryDirectory() as tmp:
            checkout, archive = Path(tmp) / 'checkout', Path(tmp) / 'archive'
            for root, paths in ((checkout, case['files']), (archive, case['release_files'])):
                for name in paths:
                    path = root / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(case['files'][name])
                self.assertEqual(link_errors(root), [])
            target = case['expected']['preserve_remote_target']
            for root in (checkout, archive):
                readme = root / 'README.md'
                readme.write_text(readme.read_text().replace(
                    'https://github.com/example/sample/blob/main/' + target, target))
            self.assertEqual(link_errors(checkout), [])
            errors = link_errors(archive)
            self.assertEqual(len(errors), 1)
            self.assertIn(target, errors[0])

    def test_fixture_evidence_is_concrete_and_behavior_remains_unrun(self):
        self.assertEqual(self.fixture['behavior_status'], 'not_run')
        self.assertEqual(len(self.cases), 4)
        for case in self.cases.values():
            self.assertTrue((ROOT / case['source']).is_file())
            self.assertTrue(case['prompt'])
            self.assertGreaterEqual(len(case['expected']['rubric']), 3)
            for category in ('keep', 'owner_review', 'preserve'):
                for path in case['expected'].get(category, []):
                    self.assertIn(path, case['files'])
        files = self.cases['cleanup-consumers']['files']
        self.assertIn('dist/template.json', files['release-manifest.txt'])
        self.assertIn("Path('plugins').glob('*.json')", files['loader.py'])
        self.assertIn("Path('tests/fixtures').glob('*.json')", files['tests/test_snapshots.py'])
        self.assertIsNone(self.cases['cleanup-missing-git']['git_status'])

    def test_distribution_contract_reaches_each_generated_host(self):
        master = ROOT / 'master-skills/github-readme'
        paths = [master / 'SKILL.md']
        for host in json.loads((master / 'ecosystems.json').read_text())['allowed']:
            bundle = ROOT / 'generated' / generator.PLATFORM_PATHS[host] / 'skills/github-readme'
            paths.append(bundle / ('SKILL.md' if host in ('claude', 'codex') else 'instructions.md'))
        for path in paths:
            text = path.read_text()
            for contract in ('packaging inclusion/exclusion rules', 'extracted-archive checks',
                             'Do not publish a release to validate links',
                             'Offline path checks do not establish external URL availability'):
                self.assertIn(contract, text, str(path))

    def test_auditors_retain_distinct_boundaries(self):
        general = (ROOT / 'cursor/skills/repo-assessment/instructions.md').read_text()
        cleanup = (ROOT / 'microsoft/copilot/skills/repo-cleanup-audit/instructions.md').read_text()
        for contract in ('Check git status', 'provisional assessment', 'paths and line numbers',
                         'unrun checks', 'conversation by default',
                         "authorized by the user's request", 'Do not implement recommendations'):
            self.assertIn(contract, general)
        for contract in ('dynamic discovery', 'fixtures and examples', 'intentionally shipped',
                         'inventory provisional', 'Needs owner review',
                         'Do not delete or move files unless the user explicitly asks'):
            self.assertIn(contract, cleanup)
        self.assertFalse((ROOT / 'master-skills/repo-assessment').exists())
        self.assertFalse((ROOT / 'master-skills/repo-cleanup-audit').exists())
