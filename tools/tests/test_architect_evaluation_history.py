"""Offline evidence-index checks, not native skill/model evaluations."""
import copy
import hashlib
import json
import unittest
from pathlib import Path

from test_selected_evaluation_history import evidence_path, validate_schema
import generate_master_skills as generator

ROOT = Path(__file__).resolve().parents[2]


def validate_history(record):
    validate_schema(record, json.loads((ROOT / 'schemas/skill-model-history.schema.json').read_text()))
    if record['development_history'] or record['review']['original_authoring_model'] != 'unknown':
        raise ValueError('unverified authoring provenance')
    if len(record['evaluations']) != 3:
        raise ValueError('selected history must retain three bounded entries')
    for entry in record['evaluations']:
        if entry['backend_snapshot'] != 'unknown' or entry['applies_to_current_behavior']:
            raise ValueError('unverified backend/current behavior')
        if entry['result'] != 'pass' or not entry['limitations']:
            raise ValueError('missing bounded result or limits')
        evidence = evidence_path(entry['evidence'])
        revision = entry['tested_revision']
        expected_path = ('generated/codex/skills/github-repo-architect/SKILL.md'
                         if entry['test_suite'] == 'foundation-tool-workflows' else
                         'generated/openai/chatgpt/skills/github-repo-architect/instructions.md')
        if revision['instruction_file'] != expected_path:
            raise ValueError('incorrect historical instruction path')
        if entry['test_suite'] == 'foundation-tool-workflows':
            report = evidence.read_text()
            fixture = evidence_path(entry['fixture'])
            if hashlib.sha256(fixture.read_bytes()).hexdigest() != entry['fixture_sha256']:
                raise ValueError('fixture hash drift')
            for pin in (revision['source_commit'], entry['session_manifest_sha256'],
                        entry['fixture_sha256'], entry['model'], entry['host_version']):
                if pin not in report:
                    raise ValueError('tool workflow report mismatch')
            if (entry['fixture_pointer'] != '/cases/0' or
                    entry['case_ids'] != [json.loads(fixture.read_text())['cases'][0]['id']]):
                raise ValueError('wrong tool case')
            if entry['model_identity_kind'] != 'requested_alias_not_immutable_backend':
                raise ValueError('alias is not backend identity')
        else:
            fixture = json.loads(evidence.read_text())
            _, collection, index = entry['evidence_pointer'].split('/')
            case = fixture[collection][int(index)]
            if (entry['case_ids'] != [case['id']] or
                    case['status'] not in ('bounded_blueprint_pass', 'bounded_security_boundary_pass') or
                    revision['source_commit'] != fixture['source_commit'] or
                    revision['instruction_sha256'] != case['resources_sha256']['instructions.md']):
                raise ValueError('native case/revision/result mismatch')
            if entry['model'] != 'unknown' or entry['visible_model_label'] != 'Instant':
                raise ValueError('visible mode is not backend identity')
        # The historical Codex payload and ChatGPT packets share these exact bytes.
        # Historical path regrouping/header changes do not imply a fresh host rerun.
        if revision['instruction_sha256'] != hashlib.sha256(
                (ROOT / 'generated/openai/chatgpt/skills/github-repo-architect/instructions.md').read_bytes()).hexdigest():
            raise ValueError('instruction pin drift: review historical applicability')


class ArchitectHistoryTests(unittest.TestCase):
    def setUp(self):
        self.master = ROOT / 'master-skills/github-repo-architect'
        self.record = json.loads((self.master / 'model-history.json').read_text())

    def test_committed_evidence_and_metadata_propagation(self):
        validate_history(self.record)
        review = self.record['review']
        self.assertEqual(review['status'], 'review-needed')
        self.assertNotIn('awaiting modernization', review['reason'])
        self.assertEqual(review['current_instruction_sha256'],
                         hashlib.sha256((self.master / 'SKILL.md').read_bytes()).hexdigest())
        for key in ('preserved_unassessed_evidence', 'deterministic_evidence'):
            evidence_path(review[key])
        for host in json.loads((self.master / 'ecosystems.json').read_text())['allowed']:
            target = ROOT / 'generated' / generator.PLATFORM_PATHS[host] / 'skills/github-repo-architect/model-history.json'
            self.assertEqual((self.master / 'model-history.json').read_bytes(), target.read_bytes())

    def test_reject_invented_provenance_or_wrong_evidence(self):
        for key, value in [('model', 'gpt-invented'), ('backend_snapshot', 'invented'),
                           ('applies_to_current_behavior', True), ('case_ids', ['wrapper-1']),
                           ('result', 'fail'), ('evidence_pointer', '/cases/0')]:
            with self.subTest(key=key):
                record = copy.deepcopy(self.record)
                record['evaluations'][2][key] = value
                with self.assertRaises(ValueError):
                    validate_history(record)
        record = copy.deepcopy(self.record)
        record['evaluations'][1]['tested_revision']['instruction_file'] = 'generated/chatgpt/skills/github-repo-architect/instructions.md'
        with self.assertRaises(ValueError):
            validate_history(record)
        record = copy.deepcopy(self.record)
        record['evaluations'][0]['fixture_sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            validate_history(record)
        record = copy.deepcopy(self.record)
        record['development_history'] = [{'date': '2026-10-19', 'model': 'invented', 'change': 'authored'}]
        with self.assertRaises(ValueError):
            validate_history(record)
