import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import evaluate

class EvaluationTests(unittest.TestCase):
    def test_fixture_contracts_and_mutations(self):
        cases=evaluate.load_cases()
        self.assertEqual(len(cases),24)
        self.assertGreaterEqual(evaluate.self_test(cases),96)
    def test_no_responses_are_not_reported_as_passes(self):
        results=evaluate.run(evaluate.load_cases(),{})
        self.assertTrue(all(row['status']=='not_run' for row in results))
    def test_passing_mock_still_needs_human_review(self):
        case=evaluate.load_cases()[0]
        self.assertEqual(evaluate.run([case],{case['id']:case['synthetic_passing_response']})[0]['status'],'human_review_required')
    def test_unknown_ids_fail(self):
        with self.assertRaises(ValueError): evaluate.run(evaluate.load_cases(),{'typo':{}})

    def test_mutations_follow_fixture_limits_and_forbidden_tokens(self):
        import copy
        case = copy.deepcopy(evaluate.load_cases()[0])
        case['expected']['max_characters'] = 400
        case['expected']['forbidden'] = ['first forbidden', 'second forbidden']
        self.assertEqual(evaluate.self_test([case]), 6)
        case['expected']['max_characters'] = None
        case['expected']['forbidden'] = []
        self.assertEqual(evaluate.self_test([case]), 3)

    def test_cli_checks_survive_optimized_python(self):
        import json
        import os
        import subprocess
        script = '''import sys
sys.path.insert(0, sys.argv.pop(1))
import evaluate
mode = sys.argv.pop(1)
if mode == 'bad_passing':
    cases = evaluate.load_cases()
    cases[0]['synthetic_passing_response']['output'] = ''
    evaluate.load_cases = lambda: cases
elif mode == 'missed_mutation':
    evaluate.grade = lambda case, response: []
sys.argv = ['evaluate', 'self-test']
sys.exit(evaluate.main())
'''
        for optimized in ('normal', 'flag', 'environment'):
            env = os.environ.copy(); env.pop('PYTHONOPTIMIZE', None)
            flags = ['-O'] if optimized == 'flag' else []
            if optimized == 'environment': env['PYTHONOPTIMIZE'] = '1'
            for mode in ('good', 'bad_passing', 'missed_mutation'):
                with self.subTest(optimized=optimized, mode=mode):
                    result = subprocess.run([sys.executable, *flags, '-c', script,
                                             str(Path(evaluate.__file__).parent), mode],
                                            capture_output=True, text=True, env=env)
                    self.assertEqual(result.returncode, 0 if mode == 'good' else 1, result.stderr)
                    if mode == 'good':
                        self.assertEqual(json.loads(result.stdout)['negative_checks'], 99)
                    else:
                        self.assertIn('ERROR:', result.stderr)
                        self.assertNotIn('"status": "passed"', result.stdout)
