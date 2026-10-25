"""Recheck sanitized synthetic artifacts; never run a model or reproduce native claims."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class NativeQualityEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = (ROOT / 'evaluations/fixtures/native-quality-2026-10-25.json').read_text()
        cls.data = json.loads(cls.raw)
        cls.cases = {c['id']: c for c in cls.data['cases']}

    def test_hashes_changes_loading_and_cleanup(self):
        self.assertEqual(self.data['session_count'], 3)
        for case in self.cases.values():
            native = case['native_execution']
            self.assertEqual(native['exit'], 0)
            for key in ('turn_completed', 'full_skill_body_observed', 'chatgpt_auth_observed', 'plugins_disabled_observed'):
                self.assertTrue(native[key])
            self.assertFalse(native['firecrawl_or_handshake_marker'])
            before, after = case['baseline_sha256'], case['after_sha256']
            changed = sorted(p for p in set(before) | set(after) if before.get(p) != after.get(p))
            self.assertEqual(changed, native['changed_files'])
            self.assertEqual(set(changed), set(case['outputs']))
            for path, output in case['outputs'].items():
                self.assertEqual(hashlib.sha256(output['text'].encode()).hexdigest(), output['sanitized_sha256'])
                self.assertEqual(output['original_sha256'], after[path])
            for path, text in case['inputs'].items():
                self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), before[path])
            source = ROOT / 'generated/openai/codex/skills' / case['skill'] / 'SKILL.md'
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), native['instruction_sha256'])
            self.assertTrue(case['cleanup']['placement_absent'])
            self.assertTrue(case['cleanup']['fresh_catalog_absent'])
            self.assertTrue(case['cleanup']['artifact_bytes_preserved_after_cleanup'])

    def test_archive_links_reuse_and_traceability(self):
        case = self.cases['R1'];text = case['outputs']['README.md']['text']
        links = re.findall(r'\]\(([^)]+)\)', text)
        included = json.loads(case['inputs']['release-files.json'])
        for link in links:
            if not link.startswith('https://'):
                self.assertIn(link, case['inputs'])
                self.assertIn(link, included)
        self.assertIn('docs/guide.md', links)
        self.assertIn('https://github.com/example/synthetic-paperclip/blob/main/master/design.md', links)
        self.assertNotIn('master/design.md', included)
        case = self.cases['S1'];prefix = 'specs/007-retry-export/'
        self.assertEqual(set(case['outputs']), {prefix + p for p in ('requirements.md', 'plan.md', 'tasks.md')})
        req = case['outputs'][prefix + 'requirements.md']['text']
        tasks = case['outputs'][prefix + 'tasks.md']['text']
        self.assertTrue(req.startswith('Status: draft\n'))
        for line in ('Owner constraint: at most three retries.', 'Owner constraint: never retry authentication failures.'):
            self.assertIn(line, req)
        self.assert_traceability(req, tasks)
        self.assertNotIn('- [x]', tasks)
        conflict = self.cases['S2']
        self.assertEqual(conflict['outputs'], {})
        self.assertIn('008-cache', conflict['response_excerpt'])
        self.assertIn('would you prefer another destination?', conflict['response_excerpt'])

    def assert_traceability(self, req, tasks):
        criteria = set(re.findall(r'^- (AC-\d+):', req, re.M))
        rows = re.findall(r'^\| (AC-\d+) \| ([^|]+) \| ([^|]+) \|', tasks, re.M)
        self.assertEqual(criteria, {row[0] for row in rows})
        ids = set(re.findall(r'^- \[ \] (V\d+)', tasks, re.M))
        for criterion, validation, expected in rows:
            referenced_ids = set(re.findall(r'V\d+', validation))
            self.assertTrue(referenced_ids, f'{criterion} has no validation-task IDs')
            self.assertLessEqual(referenced_ids, ids)
            self.assertTrue(expected.strip())

    def test_blank_validation_cell_is_rejected(self):
        outputs = self.cases['S1']['outputs']
        req = outputs['specs/007-retry-export/requirements.md']['text']
        tasks = outputs['specs/007-retry-export/tasks.md']['text']
        mutated, count = re.subn(r'^(\| AC-1 \| )[^|]+( \|)', r'\1 \2', tasks, count=1, flags=re.M)
        self.assertEqual(count, 1)
        self.assert_traceability(req, tasks)
        with self.assertRaises(AssertionError):
            self.assert_traceability(req, mutated)

    def test_public_evidence_excludes_private_trace_and_paths(self):
        for marker in ('/Users/', '/home/', '/opt/homebrew/', 'auth.json', 'access_token', 'refresh_token', 'thread_id', 'events.jsonl', 'stderr.txt'):
            self.assertNotIn(marker, self.raw)
        self.assertIn('unknown', self.data['model_identity'])
        self.assertTrue(self.data['limitations'])
