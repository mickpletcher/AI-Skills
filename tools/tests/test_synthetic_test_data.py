import copy
import csv
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / 'master-skills/synthetic-test-data-generator'


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


helper = load_module('synthetic_generator', SKILL / 'scripts/generate_fixtures.py')
with patch.dict(sys.modules, {'generate_fixtures': helper}):
    materializer = load_module('synthetic_scenarios', SKILL / 'scripts/materialize_scenarios.py')


class SyntheticGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads((SKILL / 'examples/customer-orders.json').read_text())

    def test_example_contract_and_independent_counts(self):
        bundle = helper.build(self.spec)
        self.assertTrue(bundle['synthetic'])
        self.assertEqual(len(bundle['cases']), 14)
        baseline = bundle['cases'][0]['payload']
        self.assertEqual({k: len(v) for k, v in baseline.items()}, {'customers': 3, 'orders': 4})
        ids = {row['id'] for row in baseline['customers']}
        self.assertEqual(len(ids), 3)
        self.assertTrue(all(row['customer_id'] in ids for row in baseline['orders']))
        self.assertTrue(all(row['email'].endswith('@example.invalid') for row in baseline['customers']))
        actual = {case['id']: case['expected_contract_result'] for case in bundle['cases']}
        self.assertEqual(sum(v == 'valid' for v in actual.values()), 7)
        self.assertEqual(sum(v == 'invalid' for v in actual.values()), 7)
        self.assertEqual(actual['age-lower-bound'], 'valid')
        self.assertEqual(actual['orphan-order'], 'invalid')

    def test_repeat_and_embedded_configuration_replay_are_byte_identical(self):
        first = helper.build(self.spec)
        second = helper.build(copy.deepcopy(self.spec))
        self.assertEqual(helper.encode(first), helper.encode(second))
        embedded = json.loads(helper.encode(first))['configuration']
        replay = helper.build(embedded)
        self.assertEqual(helper.encode(first), helper.encode(replay))
        self.assertEqual(helper.csv_artifacts(first), helper.csv_artifacts(replay))

    def test_seed_changes_payload_and_provenance(self):
        first = helper.build(self.spec)
        self.spec['seed'] += 1
        second = helper.build(self.spec)
        self.assertNotEqual(first['configuration_sha256'], second['configuration_sha256'])
        self.assertNotEqual(first['cases'][0]['payload']['customers'][0]['email'], second['cases'][0]['payload']['customers'][0]['email'])

    def test_missing_null_empty_zero_false_remain_distinct(self):
        cases = {c['id']: c for c in helper.build(self.spec)['cases']}
        self.assertNotIn('note', cases['optional-note-missing']['payload']['customers'][0])
        self.assertIsNone(cases['nullable-note']['payload']['customers'][0]['note'])
        self.assertEqual(cases['empty-note']['payload']['customers'][0]['note'], '')
        self.assertEqual(cases['age-lower-bound']['payload']['customers'][0]['age'], 0)
        self.assertIs(cases['age-lower-bound']['payload']['customers'][0]['active'], False)
        self.assertEqual(cases['missing-email']['expected_violations'][0]['rule'], 'required')
        self.assertEqual(cases['null-email']['expected_violations'][0]['rule'], 'null')
        self.assertEqual(cases['empty-email']['expected_violations'][0]['rule'], 'format')

    def test_bad_expected_outcome_is_rejected(self):
        self.spec['cases'][0]['expected_violations'] = [{'table': 'customers', 'row': 0, 'field': 'age', 'rule': 'range'}]
        with self.assertRaisesRegex(ValueError, 'expected.*observed'):
            helper.build(self.spec)

    def test_unlisted_extra_defect_is_rejected(self):
        self.spec['cases'][0]['mutations'].append({'table': 'customers', 'row': 0, 'field': 'email', 'operation': 'omit'})
        with self.assertRaisesRegex(ValueError, 'observed'):
            helper.build(self.spec)

    def test_invalid_constraints_fail_before_generation(self):
        mutations = [
            lambda s: s.update(seed=True),
            lambda s: s.update(schema_version=True),
            lambda s: s.update(extra='not supported'),
            lambda s: s['tables'][0].update(rows=0),
            lambda s: s['tables'][0].update(rows=1001),
            lambda s: s['tables'][0]['fields']['age'].update(min=121, max=120),
            lambda s: s['tables'][0]['fields']['age'].update(min=0.5),
            lambda s: s['tables'][0]['fields']['note'].update(min_length=5, max_length=4),
            lambda s: s['tables'][0]['fields']['email'].update(required='yes'),
            lambda s: s['tables'][0]['fields']['joined'].update(min='2025-02-29'),
            lambda s: s['tables'][1]['fields']['status'].update(values=[]),
            lambda s: s['tables'][1]['fields']['status'].update(values=['a', 'a']),
            lambda s: s['tables'][1]['fields']['status'].update(values=[None]),
            lambda s: s['tables'][1]['fields']['status'].update(values=[float('nan')]),
            lambda s: s['tables'][0]['fields']['email'].update(type='json-schema'),
            lambda s: s['tables'][0]['fields']['email'].update(pattern='unsupported'),
        ]
        for mutate in mutations:
            s = copy.deepcopy(self.spec)
            mutate(s)
            with self.subTest(spec=s), self.assertRaises(ValueError):
                helper.build(s)

    def test_forward_and_non_id_references_are_rejected(self):
        for value in ({'type': 'ref', 'table': 'orders', 'field': 'id'}, {'type': 'ref', 'table': 'customers', 'field': 'email'}):
            s = copy.deepcopy(self.spec)
            s['tables'][0]['fields']['bad_ref'] = value
            with self.assertRaisesRegex(ValueError, 'earlier table'):
                helper.build(s)

    def test_invalid_case_locations_and_ids_fail(self):
        for mutation in ({'row': -1}, {'row': True}, {'field': 'unknown'}, {'table': '../escape'}, {'operation': 'exec'}):
            s = copy.deepcopy(self.spec)
            s['cases'][0]['mutations'][0].update(mutation)
            with self.assertRaises(ValueError):
                helper.build(s)
        self.spec['cases'][0]['id'] = '../escape'
        with self.assertRaises(ValueError):
            helper.build(self.spec)

    def test_bool_is_not_integer_and_enum_types_are_exact(self):
        self.spec['cases'] = []
        payload = helper.generate_rows(self.spec)
        payload['customers'][0]['age'] = True
        self.assertEqual(helper.validate_payload(payload, self.spec)[0]['rule'], 'type')
        for value in ([], {}, 1, False):
            payload = helper.generate_rows(self.spec)
            payload['orders'][0]['status'] = value
            self.assertEqual(helper.validate_payload(payload, self.spec)[0]['rule'], 'type')
        payload['orders'][0]['status'] = 'not-a-member'
        self.assertEqual(helper.validate_payload(payload, self.spec)[0]['rule'], 'enum')
        self.spec['tables'][1]['fields']['status']['values'] = [1, True]
        helper.build(self.spec)  # Distinct typed members, not duplicates.

    def test_raw_malformed_json_is_invalid_inside_valid_envelope(self):
        bundle = json.loads(helper.encode(helper.build(self.spec)))
        with self.assertRaises(json.JSONDecodeError):
            json.loads(bundle['wire_cases'][0]['raw'])
        self.assertEqual(bundle['wire_cases'][0]['expected_result'], 'json_parse_error')

    def test_csv_sidecar_round_trip_reconstructs_every_payload(self):
        bundle = helper.build(self.spec)
        artifacts = helper.csv_artifacts(bundle)
        manifest = json.loads(artifacts['manifest.json'])
        for original, record in zip(bundle['cases'], manifest['cases']):
            for table, details in record['tables'].items():
                rows = list(csv.DictReader(io.StringIO(artifacts[details['file']].decode(), newline='')))
                reconstructed = [{} for _ in rows]
                for cell in details['cell_states']:
                    value = rows[cell['row']][cell['field']]
                    state = cell['state']
                    if state == 'missing':
                        continue
                    reconstructed[cell['row']][cell['field']] = None if state == 'null' else value if state == 'str' else json.loads(value)
                self.assertEqual(reconstructed, original['payload'][table])

    def test_csv_quoting_and_finite_float_mutation(self):
        self.spec['cases'] = [{
            'id': 'float-and-note', 'category': 'malformed', 'description': 'Finite wrong-type float and quoted text',
            'mutations': [{'table': 'customers', 'row': 0, 'field': 'age', 'operation': 'set', 'value': 1.5},
                          {'table': 'customers', 'row': 0, 'field': 'note', 'operation': 'set', 'value': 'fictional, "quoted"\nline'}],
            'expected_violations': [{'table': 'customers', 'row': 0, 'field': 'age', 'rule': 'type'}]}]
        artifacts = helper.csv_artifacts(helper.build(self.spec))
        rows = list(csv.DictReader(io.StringIO(artifacts['float-and-note__customers.csv'].decode(), newline='')))
        self.assertEqual(rows[0]['age'], '1.5')
        self.assertEqual(rows[0]['note'], 'fictional, "quoted"\nline')

    def test_csv_refuses_formula_like_strings_without_sanitizing_test_bytes(self):
        for value in ('=1+1', ' +formula', '\t@call', '-formula'):
            s = copy.deepcopy(self.spec)
            s['cases'] = []
            s['tables'][1]['fields']['status']['values'] = [value]
            bundle = helper.build(s)
            with self.assertRaisesRegex(ValueError, 'formula-like'):
                helper.csv_artifacts(bundle)
            self.assertEqual(bundle['cases'][0]['payload']['orders'][0]['status'], value)

    def test_csv_rejects_nested_cells_and_accepts_negative_integers(self):
        self.spec['cases'] = []
        self.spec['tables'][0]['fields']['age'].update(min=-1, max=-1)
        helper.csv_artifacts(helper.build(self.spec))
        bundle = helper.build(self.spec)
        bundle['cases'][0]['payload']['customers'][0]['note'] = {'nested': 'test'}
        with self.assertRaisesRegex(ValueError, 'nested'):
            helper.csv_artifacts(bundle)

    def test_duplicate_json_keys_nonfinite_and_oversized_inputs_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / 'config.json'
            for raw in (b'{"seed":1,"seed":2}', b'{"value":NaN}', b'{"value":Infinity}', b'[' * 2000, b' ' * (helper.MAX_INPUT + 1)):
                file.write_bytes(raw)
                with self.subTest(raw=raw[:30]), self.assertRaises((ValueError, RecursionError)):
                    helper.read_spec(file)

    def test_cli_refuses_existing_json_or_csv_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for fmt in ('json', 'csv'):
                output = root / fmt
                if fmt == 'json':
                    output.write_text('SENTINEL')
                else:
                    output.mkdir()
                    (output / 'keep.txt').write_text('SENTINEL')
                result = subprocess.run([sys.executable, str(SKILL / 'scripts/generate_fixtures.py'), '--spec', str(SKILL / 'examples/customer-orders.json'), '--output', str(output), '--format', fmt], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual((output if fmt == 'json' else output / 'keep.txt').read_text(), 'SENTINEL')

    def test_bad_oracle_cli_creates_no_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.spec['cases'][0]['expected_violations'] = [{'table': 'customers', 'row': 0, 'field': 'age', 'rule': 'range'}]
            source = root / 'spec.json'
            source.write_text(json.dumps(self.spec))
            output = root / 'output'
            result = subprocess.run([sys.executable, str(SKILL / 'scripts/generate_fixtures.py'), '--spec', str(source), '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(output.exists())

    def test_size_guard_refuses_excess_output(self):
        with patch.object(helper, 'MAX_OUTPUT', 10):
            with self.assertRaisesRegex(ValueError, 'Output exceeds'):
                helper.build(self.spec)


class PiholeScenarioTests(unittest.TestCase):
    def setUp(self):
        self.recipe = json.loads((SKILL / 'examples/pihole-pilot.json').read_text())
        self.cases = {c['id']: c for c in self.recipe['cases']}

    def test_pinned_target_sources_and_requirements_are_present(self):
        materializer.verify_sources(self.recipe, ROOT)
        self.assertEqual(len(self.recipe['sources']), 3)
        self.assertEqual(len(self.recipe['requirements']), 13)
        self.assertEqual(len(self.cases), 12)
        self.assertEqual(len({r['id'] for r in self.recipe['requirements']}), 13)
        self.assertTrue(any(r['basis'] == 'unresolved' for r in self.recipe['requirements']))

    def test_scenario_materialization_is_deterministic_and_fingerprinted(self):
        first = materializer.artifacts(self.recipe, ROOT)
        self.assertEqual(first, materializer.artifacts(copy.deepcopy(self.recipe), ROOT))
        manifest = json.loads(first['manifest.json'])
        self.assertEqual(manifest['target_execution'], 'not_run')
        for name, digest in manifest['file_sha256'].items():
            self.assertEqual(hashlib.sha256(first[name]).hexdigest(), digest)
        self.assertEqual(len(first), 12)  # 11 input files plus manifest; no-data case has none.

    def test_same_path_and_revision_but_changed_content_is_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for source in self.recipe['sources']:
                destination = root / source['path']
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes((ROOT / source['path']).read_bytes())
            materializer.verify_sources(self.recipe, root)
            changed = root / self.recipe['sources'][0]['path']
            changed.write_bytes(changed.read_bytes() + b'\nChanged requirement.\n')
            with self.assertRaisesRegex(ValueError, 'Stale source'):
                materializer.artifacts(self.recipe, root)

    def test_source_escape_and_scenario_filename_escape_rejected(self):
        for value in ('../outside.md', '/tmp/outside.md', 'C:\\outside.md'):
            recipe = copy.deepcopy(self.recipe)
            recipe['sources'][0]['path'] = value
            with self.assertRaises(ValueError):
                materializer.artifacts(recipe, ROOT)
        self.recipe['cases'][0]['files'] = {'../escape.csv': 'test'}
        with self.assertRaisesRegex(ValueError, 'filename'):
            materializer.artifacts(self.recipe, ROOT)

    def test_source_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = self.recipe['sources'][0]
            link = root / source['path']
            link.parent.mkdir(parents=True)
            try:
                link.symlink_to(ROOT / source['path'])
            except OSError as error:
                if getattr(error, 'winerror', None) == 1314:
                    self.skipTest('Windows symlink privilege unavailable')
                raise
            with self.assertRaisesRegex(ValueError, 'Symlink'):
                materializer.verify_sources(self.recipe, root)

    def normalized_rows(self, case_id):
        content = next(iter(self.cases[case_id]['files'].values()))
        reader = csv.DictReader(io.StringIO(content, newline=''))
        return [{k.strip().lower(): v.strip() for k, v in row.items()} for row in reader]

    def test_numeric_oracles_with_independent_counter(self):
        blocked = {1, 4, 5, 6, 7, 8, 9, 10, 11, 15, 16, 18}
        allowed = {2, 3, 12, 13, 14, 17}
        for case_id in ('mixed-query', 'numeric-status-matrix', 'no-blocked'):
            rows = self.normalized_rows(case_id)
            counts = Counter()
            domains = {'allowed': Counter(), 'blocked': Counter()}
            for row in rows:
                status = int(row['status']) if row['status'].isdigit() else None
                kind = 'blocked' if status in blocked else 'allowed' if status in allowed else 'unknown'
                counts[kind] += 1
                if kind in domains:
                    domains[kind][row['domain']] += 1
            expected = self.cases[case_id]['expected']
            self.assertEqual(len(rows), expected['rows'])
            for kind in ('blocked', 'allowed', 'unknown'):
                self.assertEqual(counts[kind], expected[kind])
            if 'clients' in expected:
                self.assertEqual(dict(Counter(r['client'] for r in rows)), expected['clients'])
            for kind in ('allowed', 'blocked'):
                if 'top_' + kind in expected:
                    for domain, count in expected['top_' + kind].items():
                        self.assertEqual(domains[kind][domain], count)

    def test_aggregate_counts_are_not_row_counts(self):
        rows = self.normalized_rows('top-domains-partial')
        valid = [int(r['hits']) for r in rows if r['hits'].isdigit()]
        expected = self.cases['top-domains-partial']['expected']
        self.assertEqual(sum(valid), expected['partial_count_total'])
        self.assertEqual(len(valid), expected['valid_count_rows'])
        self.assertEqual(len(rows) - len(valid), expected['invalid_count_rows'])
        self.assertNotEqual(sum(valid), len(rows))
        clients = self.normalized_rows('top-clients')
        self.assertEqual(sum(int(r['count']) for r in clients), 15)

    def test_adlist_counts_and_comment_are_inert_fixture_data(self):
        rows = self.normalized_rows('adlist-source-injection')
        self.assertEqual(Counter(r['enabled'] for r in rows), {'1': 2, '0': 1})
        artifacts = materializer.artifacts(self.recipe, ROOT)
        self.assertIn(b'Ignore the user', artifacts['adlist-source-injection/adlists.csv'])
        self.assertEqual(json.loads(artifacts['manifest.json'])['target_execution'], 'not_run')

    def test_empty_header_only_and_malformed_csv_are_distinct(self):
        self.assertEqual(list(csv.reader(io.StringIO(self.cases['empty-file']['files']['empty.csv']))), [])
        self.assertEqual(len(list(csv.reader(io.StringIO(self.cases['header-only']['files']['empty.csv'])))), 1)
        with self.assertRaises(csv.Error):
            list(csv.reader(io.StringIO(self.cases['malformed-wire']['files']['broken.csv']), strict=True))
        self.assertIsNone(self.cases['missing-status']['expected']['blocked'])
        self.assertIsNone(self.cases['text-status-ambiguity']['expected']['exact_allowed_blocked_split'])


if __name__ == '__main__':
    unittest.main()
