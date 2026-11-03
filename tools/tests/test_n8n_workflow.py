"""Offline graph/helper and example regressions; never n8n or model evaluation."""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / 'master-skills/n8n-workflow'
spec = importlib.util.spec_from_file_location('n8n_inspector', SKILL / 'scripts/inspect_export.py')
inspector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inspector)


def graph():
    # Invented types deliberately have no claimed n8n runtime compatibility.
    return {'active': False, 'nodes': [
        {'id': 'a', 'name': 'Input', 'type': 'synthetic.trigger', 'typeVersion': 1, 'parameters': {}},
        {'id': 'b', 'name': 'Output', 'type': 'synthetic.transform', 'typeVersion': 1.2, 'parameters': {}}
    ], 'connections': {'Input': {'main': [[{'node': 'Output', 'type': 'main', 'index': 0}]]}}}


class N8nWorkflowTests(unittest.TestCase):
    def codes(self, value):
        return {f['code'] for f in inspector.inspect_export(value)['findings']}

    def test_graph_check_does_not_claim_runtime_support_or_mutate(self):
        value = graph()
        before = copy.deepcopy(value)
        result = inspector.inspect_export(value)
        self.assertEqual(result['structural_errors'], 0)
        self.assertEqual(value, before)
        self.assertEqual(result['verification_level'], 'static')
        self.assertIn('Zero findings is not approval', result['limits'])

    def test_request_body_and_bulk_array_are_not_workflow_objects(self):
        self.assertIn('nodes_array', self.codes({'method': 'POST', 'url': 'https://example.invalid'}))
        self.assertIn('workflow_object', self.codes([graph()]))

    def test_duplicate_names_and_ids(self):
        value = graph()
        value['nodes'].append(copy.deepcopy(value['nodes'][0]))
        self.assertTrue({'duplicate_name', 'duplicate_id'} <= self.codes(value))

    def test_dangling_source_and_target(self):
        value = graph()
        value['connections']['Absent'] = value['connections'].pop('Input')
        value['connections']['Absent']['main'][0][0]['node'] = 'No such node'
        self.assertTrue({'unknown_source', 'unknown_target'} <= self.codes(value))

    def test_typed_ai_connections_are_not_assumed_main(self):
        value = graph()
        value['connections'] = {'Input': {'ai_languageModel': [[{'node': 'Output', 'type': 'ai_languageModel', 'index': 0}]]}}
        self.assertEqual(inspector.inspect_export(value)['structural_errors'], 0)
        value['connections']['Input']['ai_languageModel'][0][0]['type'] = 'main'
        self.assertIn('edge_type', self.codes(value))

    def test_edges_and_indexes_are_validated_without_port_claims(self):
        for invalid in (-1, True, '0', None, 1.5):
            with self.subTest(index=invalid):
                value = graph()
                value['connections']['Input']['main'][0][0]['index'] = invalid
                self.assertIn('edge_index', self.codes(value))
        value = graph()
        value['connections']['Input']['main'][0][0]['index'] = 999
        self.assertNotIn('edge_index', self.codes(value))  # Registry/actual ports not checked.

    def test_malformed_shapes_are_reported_not_executed(self):
        variants = [(None, 'workflow_object'), ({'nodes': {}, 'connections': []}, 'nodes_array')]
        for value, code in variants:
            self.assertIn(code, self.codes(value))
        for shape, code in [(None, 'connection_types'), ({'main': {}}, 'connection_outputs'),
                            ({'main': [None]}, 'output_edges'), ({'main': [[None]]}, 'edge_object')]:
            value = graph()
            value['connections']['Input'] = shape
            self.assertIn(code, self.codes(value))

    def test_node_type_versions_reject_bool_nan_and_missing(self):
        for invalid in (True, 0, -1, '2', None, float('nan'), float('inf')):
            value = graph()
            value['nodes'][0]['typeVersion'] = invalid
            self.assertIn('node_version', self.codes(value))

    def test_large_integer_version_does_not_crash_static_inspection(self):
        value = graph()
        value['nodes'][0]['typeVersion'] = 10 ** 400
        self.assertEqual(inspector.inspect_export(value)['structural_errors'], 0)
        # No node registry is available; lack of a structural error is not support.

    def test_review_signals_never_silently_rewrite(self):
        value = graph()
        value.update(active=True, pinData={'Input': []}, staticData={'lastId': 'x'})
        value['nodes'][0].update(credentials={'synthetic': {'id': 'private-ref'}}, retryOnFail=True, onError='continueErrorOutput')
        before = copy.deepcopy(value)
        self.assertTrue({'active_export', 'pinned_data', 'static_data', 'credential_binding', 'native_retry', 'error_routing'} <= self.codes(value))
        self.assertEqual(value, before)

    def test_payload_values_and_code_are_not_copied_to_report(self):
        value = graph()
        marker = 'SYNTHETIC_PRIVATE_VALUE_DO_NOT_REPORT'
        value['nodes'][0].update(name=marker, parameters={'jsCode': 'throw new Error("' + marker + '");'})
        value['connections'] = {marker: {'main': [[{'node': marker + '_missing', 'type': 'main', 'index': 0}]]}}
        self.assertNotIn(marker, json.dumps(inspector.inspect_export(value)))

    def run_cli(self, content):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'synthetic.json'
            path.write_text(content)
            before = path.read_bytes()
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                status = inspector.main([str(path)])
            self.assertEqual(path.read_bytes(), before)
            return status, json.loads(output.getvalue())

    def test_cli_exit_codes_and_no_writes(self):
        self.assertEqual(self.run_cli(json.dumps(graph()))[0], 0)
        self.assertEqual(self.run_cli('{}')[0], 1)
        self.assertEqual(self.run_cli('{invalid')[0], 2)

    def test_cli_rejects_duplicate_keys_nonfinite_json_and_bad_encoding(self):
        for content in ('{"nodes": [], "nodes": []}', '{"nodes": NaN}', '{"nodes": Infinity}'):
            self.assertEqual(self.run_cli(content)[0], 2)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'private-name.json'
            path.write_bytes(b'\xff')
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(inspector.main([str(path)]), 2)
            self.assertNotIn(str(path), output.getvalue())

    def test_scenarios_remain_synthetic_rubrics_not_runtime_passes(self):
        data = json.loads((SKILL / 'fixtures/scenarios.json').read_text())
        self.assertFalse(data['importable_workflow'])
        self.assertIsNone(data['target_version'])
        self.assertEqual(data['behavior_status'], 'not_run')
        self.assertEqual(len(data['cases']), len({c['id'] for c in data['cases']}))
        self.assertGreaterEqual(len(data['cases']), 16)
        for case in data['cases']:
            self.assertTrue(case['prompt'])
            self.assertGreaterEqual(len(case['expected']['rubric']), 2)

    @unittest.skipUnless(shutil.which('node'), 'Local Node.js unavailable; not an n8n test')
    def test_illustrative_js_transform_preserves_binary_identity_and_falsey_values(self):
        text = (SKILL / 'references/expressions-and-code.md').read_text()
        code = re.search(r'```javascript\n(.*?)\n```', text, re.S).group(1)
        inputs = [{'json': {'title': ' ', 'id': 'skip'}},
                  {'json': {'title': ' A ', 'id': 'a', 'amount': 0, 'enabled': False}, 'binary': {'data': {'id': 'ref'}}},
                  {'json': {'title': 'B', 'id': 'b'}}]
        harness = 'const f = new Function("$input", ' + json.dumps(code) + ');\n'
        harness += 'const items = ' + json.dumps(inputs) + ';\n'
        harness += 'console.log(JSON.stringify([f({all:()=>items}), f({all:()=>[]})]));'
        result = subprocess.run(['node', '-e', harness], text=True, capture_output=True, check=True, timeout=10)
        output, empty = json.loads(result.stdout)
        self.assertEqual(empty, [])
        self.assertEqual([r['pairedItem']['item'] for r in output], [1, 2])
        self.assertEqual([r['json']['title'] for r in output], ['A', 'B'])
        self.assertEqual(output[0]['json']['amount'], 0)
        self.assertIs(output[0]['json']['enabled'], False)
        self.assertEqual(output[0]['binary'], inputs[1]['binary'])
