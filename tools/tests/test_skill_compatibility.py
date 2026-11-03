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

    def test_status_table_has_all_ecosystems_and_valid_enums(self):
        self.assertEqual(len(maps.STATUS_ECOSYSTEMS), 12)
        self.assertEqual(len(maps.LABELS), 7)
        for source in (ROOT / 'master-skills').glob('*/COMPATIBILITY.md'):
            text = source.read_text().split('## Ecosystem status at a glance')[1].split('### Scope of Yes ratings')[0]
            rows = [line.split('|')[1:-1] for line in text.splitlines() if line.startswith('| ')][2:]
            self.assertEqual([r[0].strip() for r in rows], list(maps.STATUS_ECOSYSTEMS.values()))
            for _, compatibility, status in rows:
                self.assertIn(compatibility.strip(), ('Yes', 'No', 'Unknown'))
                self.assertIn(status.strip(), ('Implemented', 'Planned', 'Not targeted'))
            for label in ('Microsoft Copilot (consumer)', 'Microsoft 365 Copilot', 'Microsoft Copilot Studio', 'Amazon Q Developer', 'Grok'):
                self.assertIn(f'| {label} | Unknown | Not targeted |', text)

    def test_implementation_status_does_not_imply_compatibility(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            placement = {'allowed': {'codex': 'Explicit intent'}, 'skipped': {}}
            self.assertEqual(maps.implementation_status(root, 'demo', 'codex', placement), 'Planned')
            self.assertEqual(maps.implementation_status(root, 'demo', 'gemini', placement), 'Not targeted')
            p = root / 'generated/openai/codex/skills/demo/SKILL.md'
            p.parent.mkdir(parents=True); p.write_text('unverified')
            self.assertEqual(maps.implementation_status(root, 'demo', 'codex', placement), 'Implemented')
            self.assertEqual(maps.verified_scopes(root, 'demo', None), {})

    def test_yes_requires_retained_matching_evidence(self):
        import copy
        rows = json.loads((ROOT / maps.COVERAGE).read_text())['rows']
        evidence = next(r for r in rows if r['skill'] == 'blog-to-social')
        self.assertIn('chatgpt', maps.verified_scopes(ROOT, 'blog-to-social', evidence))
        changed = copy.deepcopy(evidence)
        changed['current_chatgpt_instruction_sha256'] = '0' * 64
        self.assertNotIn('chatgpt', maps.verified_scopes(ROOT, 'blog-to-social', changed))
        changed = copy.deepcopy(evidence)
        changed['current_instruction_hash_present_in_selected_evidence'] = False
        self.assertNotIn('chatgpt', maps.verified_scopes(ROOT, 'blog-to-social', changed))
        changed = copy.deepcopy(evidence)
        changed = next(r.copy() for r in rows if r['skill'] == 'github-repo-architect')
        changed['codex_host18'] = {**changed['codex_host18'], 'status': 'UNASSESSED'}
        self.assertNotIn('codex', maps.verified_scopes(ROOT, 'blog-to-social', changed))

        changed = copy.deepcopy(evidence)
        changed['bounded_native_acceptance'] = 'Not accepted'
        self.assertNotIn('chatgpt', maps.verified_scopes(ROOT, 'blog-to-social', changed))

    def test_product_mention_without_host_metadata_does_not_grant_yes(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'native-batch9.json'
            path.write_text(json.dumps({'prompt': 'ChatGPT native', 'hash': 'abc'}))
            self.assertFalse(maps.native_chatgpt_evidence(path, 'abc', 'demo'))
            record = {'host': 'ChatGPT native web UI', 'cases': [{'skill': 'demo', 'resources_sha256': {'instructions.md': 'abc'}, 'status': 'bounded_pass'}]}
            path.write_text(json.dumps(record))
            self.assertTrue(maps.native_chatgpt_evidence(path, 'abc', 'demo'))
            self.assertFalse(maps.native_chatgpt_evidence(path, 'different', 'demo'))

            record['cases'][0]['status'] = 'not_submitted'
            path.write_text(json.dumps(record))
            self.assertFalse(maps.native_chatgpt_evidence(path, 'abc', 'demo'))

            photo = Path(temp) / 'photo-native.json'
            record = {'candidate_target': 'chatgpt', 'candidate_sha256': 'abc',
                      'native_retry': {'host': 'ChatGPT native Chrome UI', 'copy': {'status': 'passed'}}}
            photo.write_text(json.dumps(record))
            self.assertTrue(maps.native_chatgpt_evidence(photo, 'abc', 'photo-rename'))
            record['native_retry']['copy']['status'] = 'not_submitted'
            photo.write_text(json.dumps(record))
            self.assertFalse(maps.native_chatgpt_evidence(photo, 'abc', 'photo-rename'))
