import contextlib
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
import generate_master_skills as generator


class MasterSkillTests(unittest.TestCase):
    def test_committed_candidates_match_without_writing(self):
        with patch.object(Path, 'write_text', side_effect=AssertionError('Check must not write')):
            generator.generate(check=True)

    def test_missing_and_drifted_candidates_fail_without_repair(self):
        for mutation in ('missing', 'drifted'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                for folder in ('master-skills', 'adapters', 'generated', 'schemas'):
                    shutil.copytree(ROOT/folder, root/folder)
                target = root/'generated/claude/skills/example-skill/SKILL.md'
                if mutation == 'missing':
                    target.unlink()
                else:
                    target.write_text(target.read_text() + '\nUNINTENDED DRIFT\n')
                before = target.read_bytes() if target.exists() else None
                with patch.object(generator, 'ROOT', root), contextlib.redirect_stdout(io.StringIO()):
                    with self.assertRaises(SystemExit) as failure:
                        generator.generate(check=True)
                    self.assertEqual(failure.exception.code, 1)
                self.assertEqual(target.read_bytes() if target.exists() else None, before)

    def test_ci_checks_pristine_checkout_and_triggers_on_generated_changes(self):
        workflow = yaml.load((ROOT/'.github/workflows/master-skills-validation.yml').read_text(), Loader=yaml.BaseLoader)
        self.assertIn('generated/**', workflow['on']['pull_request']['paths'])
        self.assertIn('main', workflow['on']['push']['branches'])
        commands = [step['run'] for step in workflow['jobs']['validate']['steps'] if 'run' in step]
        self.assertEqual(commands, ['python -m pip install -r requirements-dev.txt',
                                    'python -m py_compile tools/generate_master_skills.py',
                                    'python tools/generate_master_skills.py --check'])

    def test_every_candidate_has_valid_frontmatter(self):
        for platform, filename in generator.TARGETS.items():
            for target in (ROOT/'generated'/platform/'skills').glob('*/' + filename):
                with self.subTest(target=target):
                    generator.frontmatter(target, ROOT)
                    self.assertTrue(target.read_text().startswith('---\n'))

    def test_invalid_metadata_fails_before_writing(self):
        variants = ['name: [', 'description: valid', 'name: example-skill\ndescription: ""',
                    'name: wrong-name\ndescription: valid',
                    'name: example-skill\ndescription: "   "',
                    'name: example-skill\nname: example-skill\ndescription: valid']
        for metadata in variants:
            for check in (False, True):
                with self.subTest(metadata=metadata, check=check), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    shutil.copytree(ROOT/'schemas', root/'schemas')
                    source = root/'master-skills/example-skill/SKILL.md'
                    source.parent.mkdir(parents=True)
                    source.write_text('---\n' + metadata + '\n---\nBody\n')
                    with patch.object(generator, 'ROOT', root), patch.object(Path, 'write_text', side_effect=AssertionError('No writes')):
                        with self.assertRaises((ValueError, yaml.YAMLError)):
                            generator.generate(check=check)

    def test_deleted_or_renamed_master_reports_stale_without_changes(self):
        for rename in (False, True):
            with self.subTest(rename=rename), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                for folder in ('master-skills', 'adapters', 'generated', 'schemas'):
                    shutil.copytree(ROOT/folder, root/folder)
                source = root/'master-skills/example-skill/SKILL.md'
                if rename:
                    new = source.parent.with_name('renamed-skill')
                    source.parent.rename(new)
                    source = new/'SKILL.md'
                    source.write_text(source.read_text().replace('name: example-skill', 'name: renamed-skill'))
                else:
                    source.unlink()
                before = {p: p.read_bytes() for p in (root/'generated').rglob('*') if p.is_file()}
                for check in (False, True):
                    output = io.StringIO()
                    with patch.object(generator, 'ROOT', root), contextlib.redirect_stdout(output):
                        with self.assertRaises(SystemExit):
                            generator.generate(check=check)
                    self.assertIn('STALE GENERATED FILE', output.getvalue())
                    self.assertEqual(before, {p: p.read_bytes() for p in (root/'generated').rglob('*') if p.is_file()})

    def test_legacy_marker_migrates_but_unmanaged_files_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for folder in ('master-skills', 'adapters', 'generated', 'schemas'):
                shutil.copytree(ROOT/folder, root/folder)
            target = root/'generated/claude/skills/example-skill/SKILL.md'
            text = target.read_text()
            target.write_text(generator.MARKER + '\n' + text.replace(generator.MARKER + '\n', ''))
            with patch.object(generator, 'ROOT', root), contextlib.redirect_stdout(io.StringIO()):
                generator.generate()
                self.assertEqual(target.read_text(), text)
                target.write_text('User content\n' + generator.MARKER)
                with self.assertRaises(RuntimeError):
                    generator.generate()
                self.assertEqual(target.read_text(), 'User content\n' + generator.MARKER)
