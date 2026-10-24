import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
import generate_master_skills as generator
from model_profiles import load_profile, load_contract, CAPABILITIES


class ModelProfileTests(unittest.TestCase):
    def fixture(self, root):
        for folder in ('schemas', 'model-profiles'):
            shutil.copytree(ROOT/folder, root/folder)
        target = root/'master-skills/example-skill'
        shutil.copytree(ROOT/'master-skills/example-skill', target)
        return target

    def test_every_master_has_generic_capability_contract(self):
        for source in (ROOT/'master-skills').glob('*/SKILL.md'):
            contract = load_contract(source)
            self.assertIn('text_reasoning', contract['required'])
            self.assertIn('capabilities.json', source.read_text(encoding='utf-8'))
            self.assertFalse(any(word in json.dumps(contract).lower() for word in ('claude', 'chatgpt', 'codex', 'cursor', 'gpt-')))

    def test_named_model_builds_are_isolated_and_provenance_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = self.fixture(root)
            data, _ = load_profile(root, 'baseline')
            data.update(id='synthetic-new-model', provider='synthetic-test', model_id='fictional-version-2')
            data['capabilities']['web_retrieval'] = 'unsupported'
            data['overlay'] = 'Synthetic offline fixture. No provider call.'
            profile = root/'model-profiles/synthetic-new-model.json'
            profile.write_text(json.dumps(data), encoding='utf-8')
            with patch.object(generator, 'ROOT', root), contextlib.redirect_stdout(io.StringIO()):
                generator.generate()
                baseline = {p: p.read_bytes() for p in (root/'generated').rglob('*') if p.is_file()}
                generator.generate(model_profile='synthetic-new-model')
                generator.generate(check=True, model_profile='synthetic-new-model')
                for target in ('chatgpt', 'codex'):
                    candidate = root/'generated-models/synthetic-new-model'/generator.PLATFORM_PATHS[target]/'skills/example-skill'
                    self.assertTrue(candidate.is_dir())
                    provenance = json.loads((candidate/'build-provenance.json').read_text())
                    self.assertEqual(provenance['ecosystem'], target)
                    self.assertEqual(provenance['promotion'], 'blocked_pending_review')
                    self.assertFalse((root/'generated-models/synthetic-new-model'/target).exists())
                folder = root/'generated-models/synthetic-new-model/claude/skills/example-skill'
                before = json.loads((folder/'build-provenance.json').read_text(encoding='utf-8'))
                self.assertEqual(before['model_id'], 'fictional-version-2')
                self.assertEqual(before['behavior_evaluation'], 'not_run')
                self.assertEqual(before['promotion'], 'blocked_pending_review')
                text = (folder/'SKILL.md').read_text(encoding='utf-8')
                self.assertIn('web_retrieval: unsupported', text)
                self.assertIn('stop the dependent operation', text)
                self.assertIn('never grant authorization', text)
                data['overlay'] += ' Revised hypothesis.'
                profile.write_text(json.dumps(data), encoding='utf-8')
                with self.assertRaises(SystemExit):
                    generator.generate(check=True, model_profile='synthetic-new-model')
                generator.generate(model_profile='synthetic-new-model')
                after = json.loads((folder/'build-provenance.json').read_text(encoding='utf-8'))
                self.assertNotEqual(before['model_profile_sha256'], after['model_profile_sha256'])
                (source/'SKILL.md').write_text((source/'SKILL.md').read_text(encoding='utf-8')+'\nTest revision\n', encoding='utf-8')
                generator.generate(model_profile='synthetic-new-model')
                changed = json.loads((folder/'build-provenance.json').read_text(encoding='utf-8'))
                self.assertNotEqual(after['master_revision'], changed['master_revision'])
                self.assertEqual(baseline, {p: p.read_bytes() for p in (root/'generated').rglob('*') if p.is_file()})

    def test_manual_instruction_edit_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            with patch.object(generator, 'ROOT', root), contextlib.redirect_stdout(io.StringIO()):
                generator.generate()
                target = root/'generated/claude/skills/example-skill/SKILL.md'
                target.write_bytes(target.read_bytes()+b'\nmanual edit\n')
                before = target.read_bytes()
                with self.assertRaises(RuntimeError):
                    generator.generate()
                self.assertEqual(target.read_bytes(), before)

    def test_unknown_or_malformed_profiles_fail_before_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            with patch.object(generator, 'ROOT', root):
                for name in ('../escape', 'missing-profile'):
                    with self.assertRaises((ValueError, FileNotFoundError)):
                        generator.generate(model_profile=name)
                data, _ = load_profile(root, 'baseline')
                data.update(id='bad-profile', provider='synthetic', model_id='v2')
                data['capabilities']['text_reasoning'] = 'probably'
                (root/'model-profiles/bad-profile.json').write_text(json.dumps(data), encoding='utf-8')
                with self.assertRaises(ValueError):
                    generator.generate(model_profile='bad-profile')
                self.assertFalse((root/'generated').exists())
                self.assertFalse((root/'generated-models').exists())

    def test_model_profile_cannot_override_food_analyzer_exclusion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for folder in ('schemas', 'model-profiles'):
                shutil.copytree(ROOT/folder, root/folder)
            shutil.copytree(ROOT/'master-skills/food-analyzer', root/'master-skills/food-analyzer')
            data, _ = load_profile(root, 'baseline')
            data.update(id='synthetic-all-capable', provider='synthetic', model_id='fictional-v3')
            data['capabilities'] = {c: 'supported' for c in CAPABILITIES}
            (root/'model-profiles/synthetic-all-capable.json').write_text(json.dumps(data), encoding='utf-8')
            with patch.object(generator, 'ROOT', root), contextlib.redirect_stdout(io.StringIO()):
                for profile, output in [('baseline', root/'generated'), ('synthetic-all-capable', root/'generated-models/synthetic-all-capable')]:
                    generator.generate(model_profile=profile)
                    generator.generate(check=True, model_profile=profile)
                    for platform in ('cursor', 'codex'):
                        self.assertFalse((output/generator.PLATFORM_PATHS[platform]/'skills/food-analyzer').exists())
                    for platform in ('claude', 'chatgpt'):
                        self.assertTrue((output/generator.PLATFORM_PATHS[platform]/'skills/food-analyzer').is_dir())
                    decisions = json.loads((output/'target-decisions.json').read_text(encoding='utf-8'))
                    self.assertIn('Explicit user exclusion', decisions['food-analyzer']['skipped']['cursor'])

    def test_missing_suitability_mapping_has_no_all_platform_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = self.fixture(root)
            (source/'ecosystems.json').unlink()
            with patch.object(generator, 'ROOT', root):
                with self.assertRaises(FileNotFoundError):
                    generator.generate()
            self.assertFalse((root/'generated').exists())

    def test_masters_do_not_require_host_specific_assistant_tools(self):
        for source in (ROOT/'master-skills').glob('*/SKILL.md'):
            text = source.read_text(encoding='utf-8')
            for phrase in ('What Claude', 'asks Claude', 'Use the `WebFetch` tool', 'claude/skills/', '/mnt/data/'):
                self.assertNotIn(phrase, text, str(source))
