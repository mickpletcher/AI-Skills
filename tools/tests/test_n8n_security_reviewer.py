import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / 'master-skills/n8n-security-reviewer'
FIXTURES = ROOT / 'evaluations/fixtures/n8n-security-reviewer'
spec = importlib.util.spec_from_file_location('n8n_security_review', SKILL / 'scripts/review_export.py')
reviewer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reviewer)


def workflow(kind='n8n-nodes-base.httpRequest', **parameters):
    return {'nodes': [{'type': kind, 'parameters': parameters}]}


class N8nSecurityReviewerTests(unittest.TestCase):
    def load(self, name):
        return json.loads((FIXTURES / name).read_text())

    def rules(self, report):
        return {item['rule'] for item in report['candidates']}

    def test_risky_fixture_reports_distinct_candidates_without_values(self):
        data = self.load('risky.json')
        report = reviewer.review(data)
        self.assertEqual(self.rules(report), {'NSR-AUTH', 'NSR-URL', 'NSR-SECRET', 'NSR-TLS', 'NSR-CODE', 'NSR-PIN', 'NSR-LOG'})
        serialized = json.dumps(report)
        for secret in ('SYNTHETIC_SECRET_DO_NOT_ECHO', 'example.invalid', 'Ignore the reviewer', '$json.body', 'Inbound'):
            self.assertNotIn(secret, serialized)
        command = next(f for f in report['candidates'] if f['rule'] == 'NSR-CODE')
        self.assertTrue(command['disabled'])
        self.assertEqual(command['classification'], 'hardening option')
        self.assertEqual(command['reachability'], 'not analyzed')

    def test_benign_credential_reference_does_not_create_secret_finding(self):
        report = reviewer.review(self.load('benign.json'))
        self.assertEqual(report['candidates'], [])
        self.assertEqual(report['credential_reference_count'], 1)
        self.assertIn('Empty candidates do not mean secure.', ' '.join(report['limits']))

    def test_explicit_config_flags_not_inferred_defaults(self):
        report = reviewer.review({'nodes': []}, self.load('config.json'))
        self.assertEqual(len(report['candidates']), 3)
        self.assertEqual(reviewer.review({'nodes': []}, {'environment': {}})['candidates'], [])
        enabled = {'environment': {'N8N_SSRF_PROTECTION_ENABLED': True, 'N8N_BLOCK_ENV_ACCESS_IN_NODE': True}}
        self.assertEqual(reviewer.review({'nodes': []}, enabled)['candidates'], [])

    def test_missing_auth_is_unknown_and_declared_auth_not_a_pass(self):
        for params, expected in (({}, 'NSR-AUTH-UNKNOWN'), ({'authentication': 'headerAuth'}, 'NSR-AUTH-REVIEW')):
            report = reviewer.review(workflow('n8n-nodes-base.webhook', **params))
            self.assertEqual(self.rules(report), {expected})
            self.assertEqual(report['candidates'][0]['classification'], 'unknown')

    def test_placeholder_and_expression_not_literal_but_real_value_detected(self):
        for value in ('', '[REDACTED]', '<token>', '***', '={{ $env.KEY }}', '{{ $credentials.x }}'):
            with self.subTest(value=value):
                self.assertNotIn('NSR-SECRET', self.rules(reviewer.review(workflow(apiKey=value))))
        self.assertIn('NSR-SECRET', self.rules(reviewer.review(workflow(apiKey='SYNTHETIC_ONLY_VALUE'))))

    def test_known_markers_and_name_value_pairs_detected(self):
        for params in ({'body': {'private': '-----BEGIN PRIVATE KEY-----'}},
                       {'headerParameters': {'parameters': [{'name': 'x-api-key', 'value': 'synthetic literal'}]}},
                       {'jsonBody': 'sk-abcdefghijklmnop123456'}):
            self.assertIn('NSR-SECRET', self.rules(reviewer.review(workflow(**params))))

    def test_transport_url_and_tls_false_control(self):
        self.assertIn('NSR-HTTP', self.rules(reviewer.review(workflow(url='http://example.invalid'))))
        self.assertIn('NSR-URL-SECRET', self.rules(reviewer.review(workflow(url='https://example.invalid?token=synthetic'))))
        self.assertIn('NSR-URL-SECRET', self.rules(reviewer.review(workflow(url='https://user:synthetic@example.invalid/'))))
        self.assertNotIn('NSR-TLS', self.rules(reviewer.review(workflow(options={'allowUnauthorizedCerts': False}))))

    def test_list_and_data_wrapper_equivalent(self):
        data = self.load('benign.json')
        expected = reviewer.review(data)
        self.assertEqual(reviewer.review([data]), expected)
        self.assertEqual(reviewer.review({'data': [data]}), expected)

    def test_ambiguous_wrapper_is_rejected(self):
        with self.assertRaises(reviewer.InputError):
            reviewer.review({'nodes': [], 'data': [workflow('n8n-nodes-base.webhook', authentication='none')]})

    def test_supplied_null_config_is_rejected_not_silently_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / 'config.json'
            config.write_text('null')
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = reviewer.main([str(FIXTURES / 'benign.json'), '--config', str(config)])
            self.assertEqual(code, 2)
            self.assertEqual(out.getvalue(), '')
            self.assertFalse(json.loads(err.getvalue())['review_completed'])

    def test_reject_bad_shapes_without_echoing_input(self):
        for data in ({}, [], {'nodes': 'secret'}, {'nodes': ['secret']}, {'nodes': [{'type': 'x', 'parameters': 'secret'}]}, {'nodes': [], 'settings': []}):
            with self.subTest(data=data), self.assertRaises(reviewer.InputError) as raised:
                reviewer.review(data)
            self.assertNotIn('secret', str(raised.exception))
        with self.assertRaises(reviewer.InputError):
            reviewer.review({'nodes': []}, {'environment': []})

    def test_parser_rejects_duplicates_nonfinite_deep_and_invalid_utf8(self):
        payloads = [b'{"nodes":[],"nodes":[]}', b'{"nodes":[],"x":NaN}', b'{"nodes":[],"x":Infinity}', b'{"nodes":[],"x":1e999}', b'\xff', b'{SYNTHETIC_SECRET}', b'[' * 90 + b'0' + b']' * 90]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'input.json'
            for raw in payloads:
                path.write_bytes(raw)
                with self.subTest(raw=raw[:20]), self.assertRaises(reviewer.InputError) as raised:
                    reviewer.read_json(path)
                self.assertNotIn('SYNTHETIC_SECRET', str(raised.exception))

    def test_limits_and_non_regular_paths_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'input.json'
            path.write_text('{"nodes":[]}')
            with patch.object(reviewer, 'MAX_BYTES', 2), self.assertRaises(reviewer.InputError):
                reviewer.read_json(path)
            with self.assertRaises(reviewer.InputError):
                reviewer.read_json(tmp)
            link = Path(tmp) / 'link.json'
            try:
                link.symlink_to(path)
            except OSError:
                return  # Link creation is unavailable on some Windows hosts.
            with self.assertRaises(reviewer.InputError):
                reviewer.read_json(link)
        with patch.object(reviewer, 'MAX_NODES', 0), self.assertRaises(reviewer.InputError):
            reviewer.review(workflow())
        with patch.object(reviewer, 'MAX_ITEMS', 1), self.assertRaises(reviewer.InputError):
            reviewer.review(workflow())

    def test_execution_network_and_writes_are_not_used(self):
        data = self.load('risky.json')
        before = json.dumps(data, sort_keys=True)
        with patch.object(socket, 'socket', side_effect=AssertionError('Network forbidden')), \
             patch.object(subprocess, 'run', side_effect=AssertionError('Execution forbidden')), \
             patch.object(Path, 'write_text', side_effect=AssertionError('Write forbidden')), \
             patch.object(Path, 'write_bytes', side_effect=AssertionError('Write forbidden')):
            reviewer.review(data)
        self.assertEqual(json.dumps(data, sort_keys=True), before)

    def test_cli_hashes_exact_bytes_and_preserves_inputs(self):
        path = FIXTURES / 'risky.json'
        before = path.read_bytes()
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = reviewer.main([str(path)])
        self.assertEqual(code, 0)
        self.assertEqual(err.getvalue(), '')
        report = json.loads(out.getvalue())
        self.assertEqual(report['input_sha256'], hashlib.sha256(before).hexdigest())
        self.assertEqual(path.read_bytes(), before)

    def test_cli_invalid_input_fails_without_secret_path_or_parser_echo(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'PRIVATE_FILENAME.json'
            path.write_text('{SYNTHETIC_SECRET}')
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = reviewer.main([str(path)])
            self.assertEqual(code, 2)
            self.assertEqual(out.getvalue(), '')
            self.assertNotIn('SYNTHETIC_SECRET', err.getvalue())
            self.assertNotIn('PRIVATE_FILENAME', err.getvalue())
            self.assertFalse(json.loads(err.getvalue())['review_completed'])

    def test_candidate_bundle_resources_match(self):
        for folder in ('claude', 'openai/chatgpt', 'cursor', 'openai/codex'):
            root = ROOT / 'generated' / folder / 'skills/n8n-security-reviewer'
            for relative in ('scripts/review_export.py', 'references/review-checklist.md', 'references/helper-contract.md', 'capabilities.json'):
                self.assertEqual((root / relative).read_bytes(), (SKILL / relative).read_bytes())


if __name__ == '__main__':
    unittest.main()
