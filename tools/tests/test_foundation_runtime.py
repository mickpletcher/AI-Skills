import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from run_foundation_runtime import materialize


class ReadmeModeFixtureTests(unittest.TestCase):
    def test_state_column_is_required_only_for_active_filtering(self):
        fixture = json.loads((ROOT / 'evaluations/fixtures/foundation-tool-workflows.json').read_text(encoding='utf-8'))
        files = next(case['files'] for case in fixture['cases'] if case['skill'] == 'github-readme')
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder) / 'repository'
            materialize(work, {name: {'text': text, 'sha256': hashlib.sha256(text.encode()).hexdigest()}
                               for name, text in files.items()})
            sample = work / 'no-state.csv'
            original = b'Name\nalpha\nbeta\n'
            sample.write_bytes(original)
            env = os.environ.copy()
            env.update(PYTHONPATH=str(work / 'src'), PYTHONDONTWRITEBYTECODE='1')
            env.pop('INVENTORY_STATE', None)
            command = [sys.executable, '-B', '-c', 'from inventory_summary.cli import main; raise SystemExit(main())',
                       '--input', str(sample), '--state']
            all_rows = subprocess.run(command + ['all'], cwd=work, env=env, capture_output=True, text=True)
            self.assertEqual(all_rows.returncode, 0, all_rows.stderr)
            self.assertEqual(all_rows.stdout.strip(), 'Devices: 2')
            filtered = subprocess.run(command + ['active'], cwd=work, env=env, capture_output=True, text=True)
            self.assertNotEqual(filtered.returncode, 0)
            self.assertIn("KeyError: 'State'", filtered.stderr)
            self.assertEqual(sample.read_bytes(), original)


class FoundationRuntimeTests(unittest.TestCase):
    def test_reviewed_artifact_hashes_and_case_coverage(self):
        data = json.loads((ROOT / 'evaluations/fixtures/foundation-runtime/projects.json').read_text(encoding='utf-8'))
        self.assertEqual({p['id'] for p in data['projects']},
                         {f'{name}-r{i}' for name in ('readme', 'architect', 'regression') for i in (1, 2)})
        with tempfile.TemporaryDirectory() as folder:
            for project in data['projects']:
                materialize(Path(folder) / project['id'], project['files'])
        captures = json.loads((ROOT / 'evaluations/fixtures/foundation-runtime/captures.json').read_text(encoding='utf-8'))
        self.assertEqual(len(captures), 12)
        self.assertEqual({c['condition'] for c in captures}, {'original', 'candidate', 'without-skill'})

    def test_hash_mismatch_stops_execution(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                materialize(Path(folder), {'sample.py': {'text': 'changed', 'sha256': '0' * 64}})

    def test_unsafe_artifact_paths_are_rejected(self):
        entry = {'text': '', 'sha256': hashlib.sha256(b'').hexdigest()}
        with tempfile.TemporaryDirectory() as folder:
            for name in ('../escape.py', '/escape.py', 'C:/escape.py', 'sub\\escape.py'):
                with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'Unsafe'):
                    materialize(Path(folder), {name: entry})
