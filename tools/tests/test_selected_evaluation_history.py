"""Offline schema and committed-evidence checks for two skill history indexes."""
import copy
import datetime
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import generate_master_skills as generator


def validate_schema(value, schema):
    # Only the keywords present in this repository schema; fail closed on expansion.
    supported = {'$schema', 'title', 'type', 'required', 'properties',
                 'additionalProperties', 'items', 'enum', 'format'}
    if set(schema) - supported:
        raise ValueError('unsupported schema keyword')
    kind = schema.get('type')
    types = {'object': dict, 'array': list, 'string': str}
    if kind and (kind not in types or not isinstance(value, types[kind])):
        raise ValueError('incorrect type')
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError('invalid enum')
    if 'format' in schema:
        if schema['format'] != 'date' or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
            raise ValueError('invalid date format')
        datetime.date.fromisoformat(value)
    if kind == 'object':
        if set(schema.get('required', [])) - set(value):
            raise ValueError('missing required property')
        properties = schema.get('properties', {})
        for key, item in value.items():
            if key in properties:
                validate_schema(item, properties[key])
            elif schema.get('additionalProperties') is False:
                raise ValueError('unknown property')
    elif kind == 'array':
        for item in value:
            validate_schema(item, schema['items'])


def evidence_path(url):
    parsed = urlsplit(url)
    match = re.fullmatch(r'/mickpletcher/AI-Skills/blob/([0-9a-f]{40})/(.+)', parsed.path)
    if parsed.scheme != 'https' or parsed.netloc != 'github.com' or not match:
        raise ValueError('evidence must use pinned public repository URL')
    path = ROOT / match[2]
    if not path.resolve().is_relative_to(ROOT.resolve()) or not path.is_file():
        raise ValueError('missing or outside evidence')
    return path


class SelectedHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((ROOT / 'schemas/skill-model-history.schema.json').read_text())
        cls.records = {name: json.loads((ROOT / 'master-skills' / name / 'model-history.json').read_text())
                       for name in ('github-readme', 'spec-writer')}

    def test_existing_schema_and_invalid_metadata(self):
        for record in self.records.values():
            validate_schema(record, self.schema)
        for mutation in ('missing', 'result', 'date', 'extra'):
            record = copy.deepcopy(self.records['github-readme'])
            if mutation == 'missing':
                del record['evaluations'][0]['model']
            elif mutation == 'result':
                record['evaluations'][0]['result'] = 'not_run'
            elif mutation == 'date':
                record['evaluations'][0]['date'] = '2026-02-31'
            else:
                record['invented'] = True
            with self.assertRaises(ValueError):
                validate_schema(record, self.schema)

    def test_links_revisions_and_results_bind_to_committed_evidence(self):
        for record in self.records.values():
            evidence_path(record['review']['deterministic_evidence'])
            for entry in record['evaluations']:
                fixture = json.loads(evidence_path(entry['evidence']).read_text())
                for key in ('host_evidence', 'acceptance_evidence'):
                    if key in entry:
                        evidence_path(entry[key])
                revision = entry['tested_revision']
                if entry['test_suite'] == 'native-quality-2026-10-25':
                    case = fixture['cases'][int(entry['evidence_pointer'].split('/')[-1])]
                    self.assertEqual(case['id'], entry['case_ids'][0])
                    self.assertEqual(case['result'], entry['result'])
                    self.assertEqual(revision['source_commit'], fixture['source_commit'])
                    self.assertEqual(revision['instruction_sha256'], case['native_execution']['instruction_sha256'])
                    self.assertEqual(entry['host_version'], fixture['cli_version'])
                    self.assertEqual(entry['model'], fixture['model_alias'])
                    self.assertTrue(entry['applies_to_current_behavior'])
                elif entry['test_suite'] == 'readme-mode26':
                    self.assertEqual(revision['basis_commit'], fixture['basis_commit'])
                    self.assertTrue(revision['basis_is_pre_repair'])
                    self.assertEqual(revision['instruction_sha256'], fixture['current_resources_sha256']['SKILL.md'])
                    self.assertEqual(entry['host_version'], fixture['inventory']['cli'])
                    cases = [c for c in fixture['cases'] if c['model_requested'] == entry['model']]
                    self.assertEqual(entry['case_ids'], [c['id'] for c in cases])
                    self.assertEqual(len(cases), 5)
                    self.assertTrue(all(c['reasoning_effort'] == entry['reasoning_effort'] for c in cases))
                    self.assertEqual({c['status'] for c in cases}, {'bounded_loading_observed', 'bounded_negative_pass'})
                else:
                    node = fixture
                    for part in entry['evidence_pointer'].strip('/').split('/'):
                        node = node[int(part)] if isinstance(node, list) else node[part]
                    self.assertEqual(revision['instruction_sha256'], node['resources_sha256']['instructions.md'])
                    pin = 'source_commit' if entry['test_suite'] == 'native-batch3' else 'basis_commit'
                    self.assertEqual(revision[pin], fixture[pin])
                    self.assertIn(node['status'], ('bounded_native_pass', 'bounded_native_delivery_pass'))
                    self.assertEqual(entry['model'], 'unknown')
                self.assertEqual(entry['result'], 'pass')
                self.assertEqual(entry['applies_to_current_behavior'], entry['test_suite'] == 'native-quality-2026-10-25')
                self.assertEqual(entry['backend_snapshot'], 'unknown')

    def test_current_limits_and_metadata_propagate_without_instruction_edits(self):
        for name, record in self.records.items():
            master = ROOT / 'master-skills' / name
            self.assertEqual(record['development_history'], [])
            self.assertEqual(record['review']['original_authoring_model'], 'unknown')
            self.assertEqual(record['review']['current_behavior_evaluation'], 'bounded_native_pass')
            self.assertEqual(record['review']['status'], 'review-needed')
            evidence_path(record['review']['current_native_evidence'])
            self.assertEqual(hashlib.sha256((master / 'SKILL.md').read_bytes()).hexdigest(),
                             record['review']['current_instruction_sha256'])
            for host in json.loads((master / 'ecosystems.json').read_text())['allowed']:
                target = ROOT / 'generated' / generator.PLATFORM_PATHS[host] / 'skills' / name
                self.assertEqual((master / 'model-history.json').read_bytes(), (target / 'model-history.json').read_bytes())

    def test_private_or_unpinned_links_rejected(self):
        for url in ('file:///tmp/report.md', 'https://github.com/mickpletcher/AI-Skills/blob/main/README.md',
                    'https://example.com/private-report'):
            with self.assertRaises(ValueError):
                evidence_path(url)
