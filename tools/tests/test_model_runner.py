import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
import run_powershell_behavior as runner


def response(text='ok'):
    return io.BytesIO(json.dumps({'choices': [{'message': {'content': text}}]}).encode())


class ModelRunnerTests(unittest.TestCase):
    def run_cases(self, root, responses, dry=False):
        fixture = root/'fixtures.json'
        fixture.write_text(json.dumps({'cases': [
            {'id': str(i), 'prompt': 'Review', 'input_script': ''} for i in range(2)]}))
        skill = root/'SKILL.md'
        skill.write_text('Synthetic instructions')
        output = root/'results.json'
        opener = Mock()
        opener.open.side_effect = responses
        argv = ['runner', '--skill', str(skill), '--model', 'synthetic-model', '--output', str(output)]
        if dry:
            argv.append('--dry-run')
        with patch.object(runner, 'FIXTURES', fixture), patch.object(sys, 'argv', argv), \
             patch.dict(os.environ, {'MODEL_API_URL': 'https://api.example.test/chat', 'MODEL_API_KEY': 'synthetic-secret'}), \
             patch.object(runner.urllib.request, 'build_opener', return_value=opener) as build, \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            result = runner.main()
        return result, json.loads(output.read_text()), opener, build

    def test_success_and_dry_run(self):
        for dry in (False, True):
            with self.subTest(dry=dry), tempfile.TemporaryDirectory() as tmp:
                result, document, opener, build = self.run_cases(Path(tmp), [response('one'), response('two')], dry)
                self.assertEqual(result, 0)
                self.assertEqual(document['status'], 'completed')
                self.assertEqual([c['response'] for c in document['cases']], [None, None] if dry else ['one', 'two'])
                if dry:
                    build.assert_not_called()
                else:
                    self.assertEqual(opener.open.call_count, 2)
                    request = opener.open.call_args_list[0].args[0]
                    self.assertEqual(request.get_header('Authorization'), 'Bearer synthetic-secret')
                    self.assertEqual(json.loads(request.data)['model'], 'synthetic-model')

    def test_later_failure_keeps_prior_response_and_redacts_error(self):
        failures = [urllib.error.URLError('synthetic-secret'), io.BytesIO(b'invalid json'),
                    io.BytesIO(b'{"choices": []}'), response(None), KeyboardInterrupt()]
        for failure in failures:
            with self.subTest(failure=type(failure).__name__), tempfile.TemporaryDirectory() as tmp:
                result, document, opener, _ = self.run_cases(Path(tmp), [response('paid response'), failure])
                self.assertEqual(result, 1)
                self.assertEqual(document['status'], 'partial')
                self.assertEqual(document['failed_case_id'], '1')
                self.assertEqual(document['cases'][0]['response'], 'paid response')
                self.assertEqual(len(document['cases']), 1)
                self.assertNotIn('synthetic-secret', json.dumps(document))
                self.assertEqual(opener.open.call_count, 2)

    def test_first_failure_is_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, document, _, _ = self.run_cases(Path(tmp), [urllib.error.URLError('failure')])
            self.assertEqual(result, 1)
            self.assertEqual(document['status'], 'error')
            self.assertEqual(document['cases'], [])

    def test_replace_failure_preserves_previous_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)/'results.json'
            runner.save_checkpoint(output, {'cases': ['saved']})
            with patch.object(runner.os, 'replace', side_effect=OSError('disk failure')):
                with self.assertRaises(OSError):
                    runner.save_checkpoint(output, {'cases': ['new']})
            self.assertEqual(json.loads(output.read_text()), {'cases': ['saved']})
            self.assertEqual(list(Path(tmp).iterdir()), [output])

    def test_actual_opener_never_follows_redirects(self):
        # Replace only the transport; real urllib redirect/error dispatch runs offline.
        class Transport(urllib.request.HTTPSHandler):
            def https_open(self, req):
                requests.append(req)
                result = io.BytesIO(b'')
                result.code = code
                result.msg = 'Redirect'
                result.info = lambda: {'Location': target}
                return result

        for code in (301, 302, 303, 307, 308):
            for target in ('https://attacker.test/steal', 'http://attacker.test/steal', '/same-host'):
                with self.subTest(code=code, target=target):
                    requests = []
                    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), Transport(), runner.NoRedirects())
                    req = urllib.request.Request('https://api.example.test/chat', data=b'{}',
                                                 headers={'Authorization': 'Bearer synthetic-secret'})
                    with self.assertRaises(urllib.error.HTTPError):
                        opener.open(req)
                    self.assertEqual(len(requests), 1)

    def test_existing_output_is_preserved_before_requests(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root/'results.json'
            output.write_bytes(b'previous paid responses')
            with self.assertRaises(SystemExit) as failure:
                self.run_cases(root, [urllib.error.URLError('must not run')])
            self.assertEqual(failure.exception.code, 2)
            self.assertEqual(output.read_bytes(), b'previous paid responses')
