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
                for folder in ('master-skills', 'adapters', 'generated'):
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
        self.assertEqual(commands, ['python -m py_compile tools/generate_master_skills.py',
                                    'python tools/generate_master_skills.py --check'])
