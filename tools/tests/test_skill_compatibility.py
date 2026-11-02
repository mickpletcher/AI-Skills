"""Map integrity checks, not native host tests."""
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import skill_compatibility as maps


class CompatibilityTests(unittest.TestCase):
    def test_all_masters_current(self):
        self.assertEqual(maps.generate(ROOT, check=True), len(list((ROOT / 'master-skills').glob('*/SKILL.md'))))

    def test_links_and_generated_copies(self):
        for source in (ROOT / 'master-skills').glob('*/COMPATIBILITY.md'):
            for path in re.findall(re.escape(maps.URL) + r'([^\s)]+)', source.read_text()):
                self.assertTrue((ROOT / path).exists(), path)
            decisions = json.loads(source.with_name('ecosystems.json').read_text())
            for target in decisions['allowed']:
                dest = ROOT / 'generated' / maps.PLATFORM_PATHS[target] / 'skills' / source.parent.name / source.name
                self.assertEqual(source.read_bytes(), dest.read_bytes())

    def test_support_boundaries(self):
        food = (ROOT / 'master-skills/food-analyzer/COMPATIBILITY.md').read_text()
        self.assertIn('openai/chatgpt/skills/food-analyzer/instructions.md', food)
        self.assertIn('| Cursor | Skipped:', food)
        self.assertNotIn('generated/cursor/skills/food-analyzer/', food)
        for source in (ROOT / 'master-skills').glob('*/COMPATIBILITY.md'):
            for clause in ('OpenAI ChatGPT', 'OpenAI Codex', 'GitHub Copilot', 'Microsoft 365 Copilot is not established',
                           'not whole-skill or cross-ecosystem certification', 'Historical results do not certify current bytes',
                           'Do not overwrite shipped variants'):
                self.assertIn(clause, source.read_text())

    def fixture(self, root):
        for path in ('master-skills/example-skill', 'catalog.json', maps.COVERAGE):
            dest = root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            if (ROOT / path).is_dir():
                shutil.copytree(ROOT / path, dest)
            else:
                shutil.copyfile(ROOT / path, dest)
        for target, filename in maps.TARGETS.items():
            p = root / 'generated' / maps.PLATFORM_PATHS[target] / 'skills/example-skill' / filename
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('fixture')

    def test_missing_and_stale_maps(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            maps.generate(root)
            p = root / 'master-skills/example-skill/COMPATIBILITY.md'
            p.write_text('stale')
            with self.assertRaises(ValueError): maps.generate(root, check=True)
            self.assertEqual(p.read_text(), 'stale')
            p.unlink()
            with self.assertRaises(ValueError): maps.generate(root, check=True)
            self.assertFalse(p.exists())

    def test_changed_decisions_and_new_platform_copy(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            maps.generate(root)
            p = root / 'master-skills/example-skill/ecosystems.json'
            data = json.loads(p.read_text()); data['allowed']['codex'] = 'Changed reason.'
            p.write_text(json.dumps(data))
            with self.assertRaises(ValueError): maps.generate(root, check=True)
            maps.generate(root)
            p = root / 'microsoft/copilot/skills/example-skill/instructions.md'
            p.parent.mkdir(parents=True); p.write_text('fixture')
            with self.assertRaises(ValueError): maps.generate(root, check=True)
            maps.generate(root)
            self.assertIn('microsoft/copilot/skills/example-skill/instructions.md',
                          (root / 'master-skills/example-skill/COMPATIBILITY.md').read_text())

    def test_missing_candidate_fails_before_writing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); self.fixture(root)
            p = root / 'master-skills/example-skill/COMPATIBILITY.md'; before = p.read_bytes()
            (root / 'generated/openai/codex/skills/example-skill/SKILL.md').unlink()
            with self.assertRaisesRegex(ValueError, 'Missing allowed candidate'): maps.generate(root)
            self.assertEqual(p.read_bytes(), before)

    def test_new_target_requires_review(self):
        with patch.dict(maps.TARGETS, {'gemini': 'instructions.md'}):
            with self.assertRaisesRegex(ValueError, 'Generator targets changed'):
                maps.render(ROOT, ROOT / 'master-skills/example-skill/SKILL.md')
