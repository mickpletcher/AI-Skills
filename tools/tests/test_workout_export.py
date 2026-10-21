import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'master-skills/obsidian-workout-export/scripts/validate_export.py'
spec = importlib.util.spec_from_file_location('validate_export', SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def note(kind='combined', duration=None, newline='\n'):
    lines=['---',f'type: {kind}']
    if duration is not None:lines.append(f'duration: {duration}')
    lines+=['activities:','  - type: ride','    duration_minutes: 50','---','# Workout Log','Ride: 50 minutes.']
    return (newline.join(lines)+newline).encode('utf-8')


class WorkoutExportTests(unittest.TestCase):
    def test_native_combined_partial_duration_is_rejected_without_losing_activity(self):
        fixture=json.loads((ROOT/'evaluations/fixtures/native-batch3.json').read_text(encoding='utf-8'))
        raw=next(case['delivered_note'] for case in fixture['cases'] if case['id']=='workout-combined')
        with self.assertRaisesRegex(ValueError,'whole-session total'):validator.validate(raw.encode())
        corrected=raw.replace('\nduration: 50\n','\n',1)
        validator.validate(corrected.encode())
        self.assertIn('duration_minutes: 50',corrected)
        self.assertIn('reps: "5-8"',corrected)

    def test_explicit_combined_total_must_match_and_be_finite(self):
        validator.validate(note(duration='90'),'90')
        for supplied in ('50','-1','NaN','Infinity','true'):
            with self.subTest(supplied=supplied), self.assertRaises(ValueError):validator.validate(note(duration='90'),supplied)

    def test_actual_native_code_copies_fail_strict_frontmatter_boundary(self):
        fixture=json.loads((ROOT/'evaluations/fixtures/native-batch3.json').read_text(encoding='utf-8'))
        copies=next(case['copied_notes'] for case in fixture['cases'] if case['id']=='workout-duplicate')
        for raw in copies.values():
            with self.assertRaisesRegex(ValueError,'byte zero'):validator.validate(raw.encode())
            validator.validate(raw.removeprefix('\n').encode())
        for prefix in (b'\n',b' ',b'\xef\xbb\xbf',b'```text\n',b'Note:\n'):
            with self.subTest(prefix=prefix), self.assertRaisesRegex(ValueError,'byte zero'):validator.validate(prefix+note())

    def test_single_activity_duration_and_crlf_are_supported(self):
        for kind in ('strength','ride','run'):
            validator.validate(note(kind,'50'))
            validator.validate(note(kind,'50','\r\n'))
        validator.validate(note())

    def test_invalid_metadata_and_incomplete_notes_are_rejected(self):
        for data in (note('unknown'),note(duration='NaN'),note(duration='-1'),note().replace(b'type: combined',b'type: combined\ntype: ride'),b'---\ntype: ride\n# Missing delimiter',b'---\ntype: ride\n---\n'):
            with self.subTest(data=data), self.assertRaises(ValueError):validator.validate(data)

    def test_cli_is_read_only_and_refuses_the_captured_failures(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'note.md'
            for data,args,expected in [(note(),[],0),(note(duration='90'),['--logged-total-minutes','90'],0),(note(duration='50'),[],2),(b'\n'+note('strength'),[],2)]:
                path.write_bytes(data)
                result=subprocess.run([sys.executable,str(SCRIPT),str(path),*args],capture_output=True)
                self.assertEqual(result.returncode,expected)
                self.assertEqual(path.read_bytes(),data)


if __name__ == '__main__':
    unittest.main()
