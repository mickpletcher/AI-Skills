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
sys.path.insert(0, str(ROOT / 'tools'))
import generate_master_skills as generator
from skill_repository import frontmatter


class CodexFrontmatterTests(unittest.TestCase):
    def test_every_codex_entrypoint_has_portable_identity_and_preserved_metadata(self):
        targets = list((ROOT / 'generated/openai/codex/skills').glob('*/SKILL.md'))
        self.assertEqual(len(targets), 12)
        for target in targets:
            with self.subTest(skill=target.parent.name):
                original = frontmatter(ROOT / 'master-skills' / target.parent.name / 'SKILL.md', ROOT)
                actual = frontmatter(target, ROOT)
                self.assertEqual(actual, {key: original[key] for key in ('name', 'description')})
                self.assertLessEqual(len(actual['description']), 1024)
                self.assertLessEqual(len(actual['name']), 64)
                provenance = json.loads((target.parent / 'build-provenance.json').read_text())
                self.assertEqual(provenance['source_frontmatter'], original)
                self.assertEqual(provenance['frontmatter_policy'], 'codex-name-description-v1')

    def test_baseline_and_named_builds_adapt_only_codex_headers(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('schemas', 'model-profiles'):
                shutil.copytree(ROOT / name, root / name)
            skill = root / 'master-skills/example-skill'
            shutil.copytree(ROOT / 'master-skills/example-skill', skill)
            source = skill / 'SKILL.md'
            content = source.read_text(encoding='utf-8')
            content = content.replace('---\n', '---\nversion: 1.2.3\nargument-hint: "quote: value"\n', 1)
            source.write_text(content, encoding='utf-8')
            before = source.read_bytes()
            profile = json.loads((root / 'model-profiles/baseline.json').read_text())
            profile.update(id='synthetic-header', provider='synthetic', model_id='synthetic-v1')
            (root / 'model-profiles/synthetic-header.json').write_text(json.dumps(profile))
            with patch.object(generator, 'ROOT', root), contextlib.redirect_stdout(io.StringIO()):
                for name, output in [('baseline', root / 'generated'), ('synthetic-header', root / 'generated-models/synthetic-header')]:
                    generator.generate(model_profile=name)
                    generator.generate(check=True, model_profile=name)
                    codex = output / 'openai/codex/skills/example-skill/SKILL.md'
                    claude = output / 'claude/skills/example-skill/SKILL.md'
                    self.assertEqual(set(frontmatter(codex, root)), {'name', 'description'})
                    self.assertEqual(frontmatter(claude, root)['version'], '1.2.3')
                    self.assertIn(content.split('---', 2)[2].strip(), codex.read_text(encoding='utf-8'))
                    provenance = json.loads((codex.parent / 'build-provenance.json').read_text())
                    self.assertEqual(provenance['source_frontmatter']['argument-hint'], 'quote: value')
            self.assertEqual(source.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
