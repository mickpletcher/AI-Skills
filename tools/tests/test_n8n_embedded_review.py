"""Public-contract regressions for bounded, one-layer embedded JSON triage."""
import builtins
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / 'master-skills/n8n-security-reviewer/scripts/review_export.py'
spec = importlib.util.spec_from_file_location('n8n_embedded_review_test_subject', HELPER)
reviewer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reviewer)


def workflow(kind='n8n-nodes-base.httpRequest', **parameters):
    return {'nodes': [{'type': kind, 'parameters': parameters}]}


def embedded(report):
    return [item for item in report['candidates'] if item['rule'] == 'NSR-EMBEDDED-SECRET']


def reasons(report):
    return {item['reason'] for item in report['coverage']}


class EmbeddedReviewTests(unittest.TestCase):
    def assert_partial(self, report, reason):
        self.assertEqual(report['schema_version'], 2)
        self.assertEqual(report['embedded_review']['status'], 'partial')
        self.assertIn(reason, reasons(report))
        for item in report['coverage']:
            self.assertEqual(item['status'], 'unknown')

    def test_original_gap_and_unevaluated_body_are_separate(self):
        data = workflow(jsonHeaders='{"Authorization":"Bearer PRIVATE_HEADER_CANARY"}',
                        jsonBody='={{ { token: $credentials.apiKey } }}')
        report = reviewer.review(data)
        self.assertEqual(len(embedded(report)), 1)
        self.assertEqual(embedded(report)[0]['priority'], 'medium')
        self.assert_partial(report, 'unevaluated_expression')
        self.assertNotIn('PRIVATE_HEADER_CANARY', json.dumps(report))
        self.assertEqual(report['embedded_review']['counts']['decoded_fields'], 1)

    def test_supported_nodes_and_disabled_state(self):
        for kind in ('n8n-nodes-base.httpRequest', 'n8n-nodes-base.httpRequestTool'):
            data = workflow(kind, jsonHeaders='{"x-api-key":"PRIVATE_LITERAL"}')
            data['nodes'][0]['disabled'] = True
            report = reviewer.review(data)
            self.assertTrue(embedded(report))
            for item in embedded(report):
                self.assertTrue(item['disabled'])
                self.assertEqual(item['reachability'], 'not analyzed')
                self.assertEqual(item['classification'], 'conditional risk')

    def test_empty_scope_is_completed_not_a_security_pass(self):
        report = reviewer.review(workflow())
        self.assertEqual(report['schema_version'], 2)
        self.assertEqual(report['embedded_review']['status'], 'completed_within_scope')
        self.assertEqual(report['coverage'], [])
        self.assertFalse(report['embedded_review']['output_truncated'])
        self.assertIn('Empty candidates do not mean secure.', ' '.join(report['limits']))
        self.assertIn('budgets', report['embedded_review'])

    def test_decoded_unicode_keys_and_values(self):
        report = reviewer.review(workflow(jsonHeaders=r'{"\u0041uthorization":"caf\u00e9_PRIVATE_CANARY"}'))
        self.assertTrue(embedded(report))
        self.assertNotIn('PRIVATE_CANARY', json.dumps(report))
        self.assertEqual(report['coverage'], [])

    def test_header_object_pairs_and_unsupported_array_shape(self):
        report = reviewer.review(workflow(jsonHeaders=json.dumps(
            {'parameters': [{'name': 'Authorization', 'value': 'PAIR_CANARY'}]})))
        self.assertTrue(embedded(report))
        self.assertNotIn('PAIR_CANARY', json.dumps(report))
        report = reviewer.review(workflow(jsonHeaders=json.dumps(
            [{'name': 'x-api-key', 'value': 'PAIR_CANARY'}])))
        self.assertEqual(embedded(report), [])
        self.assert_partial(report, 'unsupported_header_shape')

    def test_nested_body_name_only_candidate_is_low_priority(self):
        report = reviewer.review(workflow(jsonBody=json.dumps({'outer': [{'password': 'BODY_CANARY'}]})))
        self.assertTrue(embedded(report))
        self.assertEqual({item['priority'] for item in embedded(report)}, {'low'})

    def test_known_token_signature_preserves_original_scan(self):
        token = 'ghp_' + 'SYNTHETIC_CANARY_1234567890'
        report = reviewer.review(workflow(jsonBody=json.dumps({'public': token})))
        self.assertIn('NSR-SECRET', {item['rule'] for item in report['candidates']})
        self.assertTrue(embedded(report))
        self.assertEqual({item['priority'] for item in embedded(report)}, {'medium'})
        self.assertGreater(report['embedded_review']['counts']['known_token_markers'], 0)
        self.assertNotIn(token, json.dumps(report))

    def test_placeholders_do_not_create_embedded_findings(self):
        for placeholder in ('', '  ', '[REDACTED]', '<token>', '***', 'changeme',
                            'Bearer [REDACTED]', 'Basic <redacted>'):
            with self.subTest(placeholder=placeholder):
                report = reviewer.review(workflow(jsonHeaders=json.dumps({'Authorization': placeholder})))
                self.assertEqual(embedded(report), [])
                self.assertEqual(report['coverage'], [])

    def test_reference_only_direct_and_pair_expressions_are_unknown_not_secrets(self):
        for expression in ('={{ $env.KEY }}', '{{ $credentials.apiKey }}',
                           '={{ $json.value }}', 'Bearer {{ $credentials.apiKey }}'):
            for params in ({'apiKey': expression},
                           {'headerParameters': {'parameters': [{'name': 'Authorization', 'value': expression}]}}):
                with self.subTest(expression=expression, params=params):
                    report = reviewer.review(workflow(**params))
                    self.assertEqual(report['candidates'], [])
                    self.assert_partial(report, 'expression_like_secret_value')

    def test_mixed_dynamic_and_literal_siblings_retain_literal(self):
        for value in ({'token': '${runtime}', 'password': 'SIBLING_CANARY'},
                      {'password': 'SIBLING_CANARY', 'token': '{{ runtime }}'}):
            report = reviewer.review(workflow(jsonBody=json.dumps(value)))
            self.assertTrue(embedded(report))
            self.assert_partial(report, 'dynamic_embedded_value')
            self.assertNotIn('SIBLING_CANARY', json.dumps(report))

    def test_placeholder_wrappers_cannot_hide_direct_expression_coverage(self):
        for expression in ('<{{ $env.KEY }}>', '<${runtime}>',
                           'Bearer <{{ $credentials.apiKey }}>',
                           'Basic <{{ $json.value }}>'):
            for params in ({'apiKey': expression},
                           {'headerParameters': {'parameters': [
                               {'name': 'Authorization', 'value': expression}]}}):
                with self.subTest(expression=expression, params=params):
                    report = reviewer.review(workflow(**params))
                    self.assertEqual(report['candidates'], [])
                    self.assert_partial(report, 'expression_like_secret_value')
                    self.assertNotIn(expression, json.dumps(report))
        for value in ('<token>', 'Bearer <token>', 'Basic <redacted>'):
            with self.subTest(placeholder=value):
                report = reviewer.review(workflow(jsonHeaders=json.dumps({'Authorization': value})))
                self.assertEqual(embedded(report), [])
                self.assertEqual(report['coverage'], [])

    def test_nonsecret_dynamic_string_still_limits_coverage(self):
        report = reviewer.review(workflow(jsonBody='{"description":"{{ $json.text }}"}'))
        self.assertEqual(embedded(report), [])
        self.assert_partial(report, 'dynamic_embedded_value')

    def test_opaque_javascript_is_never_coerced_into_json(self):
        for text in ('={{ /* password: "COMMENT_CANARY" */ $json }}',
                     '={{ `password: TEMPLATE_CANARY ${$json.x}` }}',
                     '={{ /password: REGEX_CANARY/.test($json.x) }}',
                     '={{ ({["pass" + "word"]: "JS_CANARY", ...$json}) }}'):
            with self.subTest(text=text):
                report = reviewer.review(workflow(jsonBody=text))
                self.assertEqual(embedded(report), [])
                self.assert_partial(report, 'unevaluated_expression')
                for canary in ('COMMENT_CANARY', 'TEMPLATE_CANARY', 'REGEX_CANARY', 'JS_CANARY'):
                    self.assertNotIn(canary, json.dumps(report))

    def test_exactly_one_layer_no_generic_string_deserialization(self):
        inner = json.dumps({'password': 'SECOND_LAYER_CANARY'})
        report = reviewer.review(workflow(jsonBody=json.dumps({'payload': inner}), other=inner))
        self.assertEqual(embedded(report), [])
        self.assertEqual(report['coverage'], [])
        self.assertEqual(report['embedded_review']['counts']['decoded_fields'], 1)

    def test_custom_and_unsupported_nodes_are_not_decoded(self):
        for kind in ('custom.httpRequest', 'n8n-nodes-base.set', 'n8n-nodes-base.httpRequestV99'):
            report = reviewer.review(workflow(kind, jsonHeaders='{"Authorization":"OUT_OF_SCOPE_CANARY"}'))
            self.assertEqual(embedded(report), [])
            self.assertEqual(report['embedded_review']['counts']['decoded_fields'], 0)

    def test_malformed_duplicate_and_nonfinite_fields_preserve_valid_sibling(self):
        cases = [('{BAD_CANARY}', 'not_strict_json'),
                 ('{"x":1,"x":2}', 'not_strict_json'),
                 ('{"x":NaN}', 'not_strict_json'),
                 ('{"x":Infinity}', 'not_strict_json'),
                 ('{"x":-Infinity}', 'not_strict_json'),
                 ('{"x":1e999}', 'nonfinite_number'),
                 (r'{"x":"\ud800"}', 'unsupported_unicode')]
        for text, reason in cases:
            with self.subTest(text=text):
                report = reviewer.review(workflow(jsonBody=text, jsonHeaders='{"Authorization":"GOOD_CANARY"}'))
                self.assert_partial(report, reason)
                self.assertTrue(embedded(report))
                self.assertNotIn('BAD_CANARY', json.dumps(report))
                self.assertNotIn('GOOD_CANARY', json.dumps(report))

    def test_surrogate_keys_and_raw_surrogates_are_unknown(self):
        for text in (r'{"\udfff":"value"}', '{"x":"' + chr(0xd800) + '"}'):
            with self.subTest(text=ascii(text)):
                report = reviewer.review(workflow(jsonBody=text))
                self.assert_partial(report, 'unsupported_unicode')
                self.assertEqual(embedded(report), [])

    def test_valid_escaped_surrogate_pair_is_supported(self):
        report = reviewer.review(workflow(jsonBody=r'{"note":"\ud83d\ude00","password":"UNICODE_CANARY"}'))
        self.assertTrue(embedded(report))
        self.assertEqual(report['coverage'], [])
        self.assertEqual(report['embedded_review']['status'], 'completed_within_scope')

    def test_dynamic_decoded_keys_are_unknown(self):
        report = reviewer.review(workflow(jsonBody='{"{{ $json.key }}":"public"}'))
        self.assert_partial(report, 'dynamic_embedded_value')
        self.assertEqual(embedded(report), [])

    def test_failed_parses_consume_shared_byte_and_field_budgets(self):
        for constant, limit, reason in (('EMBEDDED_TOTAL_BYTES', 3, 'total_parse_budget'),
                                        ('EMBEDDED_MAX_FIELDS', 1, 'total_field_budget')):
            with self.subTest(constant=constant), patch.object(reviewer, constant, limit):
                report = reviewer.review([workflow(jsonBody='bad'), workflow(jsonBody='{}')])
            self.assert_partial(report, reason)
            self.assertIn('not_strict_json', reasons(report))
            self.assertEqual(report['embedded_review']['counts']['decoded_fields'], 0)

    def test_unsupported_structured_field_and_header_shapes_are_unknown(self):
        for params, reason in (({'jsonBody': 42}, 'unsupported_field_shape'),
                               ({'jsonHeaders': '42'}, 'unsupported_header_shape'),
                               ({'jsonHeaders': '[1,2]'}, 'unsupported_header_shape')):
            report = reviewer.review(workflow(**params))
            self.assertEqual(embedded(report), [])
            self.assert_partial(report, reason)

    def test_locators_and_metadata_never_echo_names_keys_values_or_token_hashes(self):
        token = 'sk-' + 'PRIVATE_TOKEN_CANARY_1234567890'
        data = workflow(jsonBody=json.dumps({'PRIVATE_KEY_CANARY': {'password': token}}),
                        jsonHeaders='{"Authorization":"{{ PRIVATE_EXPRESSION_CANARY }}"}')
        data['name'] = 'PRIVATE_WORKFLOW_CANARY'
        data['nodes'][0]['name'] = 'PRIVATE_NODE_CANARY'
        report = reviewer.review(data)
        serialized = json.dumps(report)
        for marker in ('PRIVATE_KEY_CANARY', token, 'PRIVATE_EXPRESSION_CANARY',
                       'PRIVATE_WORKFLOW_CANARY', 'PRIVATE_NODE_CANARY',
                       hashlib.sha256(token.encode('utf-8')).hexdigest()):
            self.assertNotIn(marker, serialized)
        for item in embedded(report) + report['coverage']:
            self.assertRegex(item['location'], r'^workflows\[0\]\.nodes\[0\]\.parameters(?:\.|$)')

    def test_field_size_limit_is_utf8_bytes(self):
        text = json.dumps({'note': 'é' * 40}, ensure_ascii=False)
        self.assertLess(len(text), 70)
        self.assertGreater(len(text.encode('utf-8')), 70)
        with patch.object(reviewer, 'EMBEDDED_MAX_BYTES', 70):
            report = reviewer.review(workflow(jsonBody=text))
        self.assert_partial(report, 'field_size_limit')
        self.assertEqual(report['embedded_review']['counts']['decoded_fields'], 0)

    def test_total_parse_budget_is_shared_across_workflows(self):
        text = '{"password":"BUDGET_CANARY"}'
        with patch.object(reviewer, 'EMBEDDED_TOTAL_BYTES', len(text.encode('utf-8'))):
            report = reviewer.review([workflow(jsonBody=text), workflow(jsonBody=text)])
        self.assert_partial(report, 'total_parse_budget')
        self.assertEqual(report['embedded_review']['counts']['decoded_fields'], 1)
        self.assertTrue(embedded(report))

    def test_structural_depth_and_values_are_bounded(self):
        for constant, limit, text in (('EMBEDDED_MAX_DEPTH', 3, '{"a":{"b":{"c":{"d":0}}}}'),
                                      ('EMBEDDED_MAX_VALUES', 3, '[1,2,3,4]')):
            with self.subTest(constant=constant), patch.object(reviewer, constant, limit):
                report = reviewer.review(workflow(jsonBody=text))
            self.assert_partial(report, 'structure_limit')

    def test_total_value_and_field_limits_are_shared_across_workflows(self):
        cases = [('EMBEDDED_TOTAL_VALUES', 3, 'total_value_budget'),
                 ('EMBEDDED_MAX_FIELDS', 1, 'total_field_budget')]
        for constant, limit, reason in cases:
            with self.subTest(constant=constant), patch.object(reviewer, constant, limit):
                report = reviewer.review([workflow(jsonBody='{"password":"FIRST_CANARY"}'),
                                          workflow(jsonBody='{"password":"SECOND_CANARY"}')])
            self.assert_partial(report, reason)
            self.assertTrue(embedded(report))

    def test_coverage_cap_cannot_hide_later_findings(self):
        data = [workflow(jsonBody='={{ $json }}') for _ in range(5)]
        data.append(workflow(jsonHeaders='{"Authorization":"LATE_CANARY"}'))
        with patch.object(reviewer, 'EMBEDDED_MAX_COVERAGE', 2):
            report = reviewer.review(data)
        self.assertEqual(len(report['coverage']), 2)
        self.assertTrue(embedded(report))
        self.assertTrue(report['embedded_review']['output_truncated'])
        self.assertGreater(report['embedded_review']['counts']['suppressed_coverage'], 0)
        self.assertEqual(report['embedded_review']['status'], 'partial')

    def test_finding_cap_does_not_hide_coverage(self):
        data = [workflow(jsonBody='{"password":"CAP_CANARY"}') for _ in range(5)]
        data.append(workflow(jsonBody='={{ $json }}'))
        with patch.object(reviewer, 'EMBEDDED_MAX_FINDINGS', 2):
            report = reviewer.review(data)
        self.assertEqual(len(embedded(report)), 2)
        self.assert_partial(report, 'unevaluated_expression')
        self.assertTrue(report['embedded_review']['output_truncated'])
        self.assertGreater(report['embedded_review']['counts']['suppressed_findings'], 0)

    def test_default_caps_preserve_findings_after_coverage_saturation(self):
        self.assertEqual(reviewer.EMBEDDED_MAX_COVERAGE, 100)
        self.assertEqual(reviewer.EMBEDDED_MAX_FINDINGS, 100)
        self.assertEqual(reviewer.EMBEDDED_MAX_FIELDS, 128)
        data = [workflow(jsonBody='={{ $json }}') for _ in range(101)]
        data.extend(workflow(jsonHeaders='{"Authorization":"DEFAULT_CAP_CANARY"}')
                    for _ in range(129))
        report = reviewer.review(data)
        self.assertEqual(len(report['coverage']), 100)
        self.assertEqual(len(embedded(report)), 100)
        self.assertEqual(report['embedded_review']['budgets']['fields_consumed'], 128)
        self.assertEqual(report['embedded_review']['counts']['decoded_fields'], 128)
        self.assertGreater(report['embedded_review']['counts']['suppressed_findings'], 0)
        self.assertGreater(report['embedded_review']['counts']['suppressed_coverage'], 0)
        self.assertEqual(report['embedded_review']['status'], 'partial')
        self.assertTrue(report['embedded_review']['output_truncated'])
        self.assertNotIn('DEFAULT_CAP_CANARY', json.dumps(report))
        # The final budget gap is itself suppressed after coverage saturation.
        # Reorder the same workload to make that reason observable without
        # changing any configured cap or reducing the number of parse attempts.
        reordered = reviewer.review(data[101:] + data[:101])
        self.assertIn('total_field_budget', reasons(reordered))
        self.assertEqual(reordered['embedded_review']['budgets']['fields_consumed'], 128)
        self.assertEqual(len(embedded(reordered)), 100)

    def test_no_input_mutation_network_execution_or_file_writes(self):
        data = workflow(jsonHeaders='{"Authorization":"STATIC_CANARY"}',
                        jsonBody='={{ __import__("os").system("NEVER_RUN_CANARY") }}')
        before = copy.deepcopy(data)
        forbidden = AssertionError('Static review attempted an external effect')
        with patch.object(socket, 'socket', side_effect=forbidden), \
             patch.object(socket, 'create_connection', side_effect=forbidden), \
             patch.object(subprocess, 'Popen', side_effect=forbidden), \
             patch.object(os, 'system', side_effect=forbidden), \
             patch.object(builtins, 'eval', side_effect=forbidden), \
             patch.object(builtins, 'exec', side_effect=forbidden), \
             patch.object(builtins, 'open', side_effect=forbidden), \
             patch.object(io, 'open', side_effect=forbidden), \
             patch.object(os, 'open', side_effect=forbidden):
            report = reviewer.review(data)
        self.assertEqual(data, before)
        self.assertTrue(embedded(report))
        self.assert_partial(report, 'unevaluated_expression')

    def test_cli_inner_failure_is_partial_success_with_exact_outer_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'PRIVATE_FILENAME_CANARY.json'
            raw = json.dumps(workflow(jsonBody='{"x":NaN}',
                                      jsonHeaders='{"Authorization":"CLI_CANARY"}')).encode('utf-8')
            path.write_bytes(raw)
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = reviewer.main([str(path)])
            self.assertEqual(code, 0)
            self.assertEqual(err.getvalue(), '')
            report = json.loads(out.getvalue())
            self.assert_partial(report, 'not_strict_json')
            self.assertTrue(embedded(report))
            self.assertEqual(report['input_sha256'], hashlib.sha256(raw).hexdigest())
            self.assertEqual(path.read_bytes(), raw)
            self.assertNotIn('CLI_CANARY', out.getvalue())
            self.assertNotIn('PRIVATE_FILENAME_CANARY', out.getvalue())


if __name__ == '__main__':
    unittest.main()
