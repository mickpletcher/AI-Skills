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
