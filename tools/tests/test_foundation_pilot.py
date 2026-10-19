import io
import json
import unittest
from pathlib import Path


FIXTURE = Path(__file__).resolve().parents[2]/'evaluations/fixtures/foundation-pilot.json'


class FoundationPilotTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads(FIXTURE.read_text(encoding='utf-8'))
        self.cases = {case['id']: case for case in self.fixture['cases']}

    def test_architect_contract_is_explicit_in_both_prompts(self):
        self.assertEqual(self.fixture['revision'], 2)
        self.assertEqual(len(self.cases), 7)
        for name in ('architect-scaffold', 'architect-whitespace-regression'):
            prompt = self.cases[name]['prompt']
            for term in ('bool(line.strip())', 'U+2003', 'U+00A0', 'trailing newline', 'CRLF'):
                self.assertIn(term, prompt)
            self.assertTrue(any('whitespace-only' in item for item in self.cases[name]['hard_failures']))

    def test_runtime_oracles_cover_boundary_cases(self):
        cases = self.cases['architect-whitespace-regression']['runtime_cases']
        expected = {'empty': 0, 'ascii-whitespace': 0, 'unicode-whitespace': 0,
                    'mixed-and-unterminated': 2, 'universal-newlines': 3,
                    'unterminated-single': 1}
        self.assertEqual({case['id']: case['expected_count'] for case in cases}, expected)
        for case in cases:
            with self.subTest(case=case['id']):
                lines = io.StringIO(case['input'], newline=None)
                self.assertEqual(sum(bool(line.strip()) for line in lines), case['expected_count'])

    def test_oracles_reject_prior_and_nearby_counting_regressions(self):
        cases = self.cases['architect-whitespace-regression']['runtime_cases']
        mutations = (
            lambda lines: sum(bool(line.rstrip('\r\n')) for line in lines),
            lambda lines: sum(bool(line.strip(' \t\r\n')) for line in lines),
            lambda lines: sum(bool(line.strip()) and line.endswith(('\r', '\n')) for line in lines),
        )
        for mutation in mutations:
            self.assertTrue(any(mutation(io.StringIO(case['input'], newline=None)) != case['expected_count']
                                for case in cases))


if __name__ == '__main__':
    unittest.main()
