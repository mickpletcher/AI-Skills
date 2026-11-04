"""Offline fixture contracts, not model behavior or detection-effectiveness tests."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / 'master-skills/room-privacy-inspector'


def validate_manifest(data):
    if data.get('schema_version') != 1 or data.get('synthetic') is not True:
        raise ValueError('synthetic manifest version required')
    cases = data.get('cases', [])
    if not cases or len({c['id'] for c in cases}) != len(cases):
        raise ValueError('unique nonempty cases required')
    if not {'benign', 'suspicious', 'ambiguous', 'false_positive'} <= {c['category'] for c in cases}:
        raise ValueError('required coverage absent')
    for c in cases:
        if c.get('synthetic') is not True or c.get('model_run_status') != 'not_run':
            raise ValueError('unexecuted synthetic fixture must not claim a pass')
        if not c.get('prompt') or c.get('input_kind') != 'text-only scenario; not actual media':
            raise ValueError('text-only input boundary required')
        for field in ('observed', 'unknown', 'required_behaviors', 'forbidden_behaviors'):
            if not c.get('oracle', {}).get(field):
                raise ValueError('evidence and behavior oracles required')
    return cases


class RoomPrivacyTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((SKILL / 'fixtures/scenarios.json').read_text())

    def test_coverage_and_evidence_contract(self):
        self.assertEqual(len(validate_manifest(self.data)), 16)

    def test_missing_unknowns_rejected(self):
        self.data['cases'][0]['oracle']['unknown'] = []
        with self.assertRaises(ValueError):
            validate_manifest(self.data)

    def test_false_execution_claim_rejected(self):
        self.data['cases'][0]['model_run_status'] = 'passed'
        with self.assertRaises(ValueError):
            validate_manifest(self.data)

    def test_actual_media_claim_rejected(self):
        self.data['cases'][0]['input_kind'] = 'viewed photo'
        with self.assertRaises(ValueError):
            validate_manifest(self.data)

    def test_duplicate_ids_rejected(self):
        self.data['cases'].append(self.data['cases'][0])
        with self.assertRaises(ValueError):
            validate_manifest(self.data)

    def test_missing_false_positive_coverage_rejected(self):
        self.data['cases'] = [c for c in self.data['cases'] if c['category'] != 'false_positive']
        with self.assertRaises(ValueError):
            validate_manifest(self.data)

    def test_only_conversational_candidates_proposed(self):
        targets = json.loads((SKILL / 'ecosystems.json').read_text())
        self.assertEqual(set(targets['allowed']), {'claude', 'chatgpt'})
        self.assertEqual(set(targets['skipped']), {'cursor', 'codex'})
        self.assertEqual(targets['review_status'], 'proposed')

    def test_generated_resources_match_master(self):
        for target in ('claude', 'openai/chatgpt'):
            dest = ROOT / 'generated' / target / 'skills/room-privacy-inspector'
            for folder in ('references', 'fixtures'):
                for source in (SKILL / folder).iterdir():
                    self.assertEqual(source.read_bytes(), (dest / folder / source.name).read_bytes())


if __name__ == '__main__':
    unittest.main()
