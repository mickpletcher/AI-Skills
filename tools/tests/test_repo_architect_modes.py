"""Synthetic invariants and source propagation; no model or GitHub execution."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import generate_master_skills as generator


def contract_errors(case, response):
    errors = []
    if response['mode'] != case['mode']:
        errors.append('mode changed')
    if response['files'] and not case['allow_files']:
        errors.append('unauthorized file write')
    for setting in response['settings']:
        if setting['status'] in ('applied-and-verified', 'attempted-but-unverified'):
            action = {key: setting.get(key) for key in ('repository', 'branch', 'name', 'desired')}
            approved = any(json.dumps(action, sort_keys=True) == json.dumps(item, sort_keys=True)
                           for item in case['authorized'])
            if case['mode'] != 'configure GitHub' or not approved or not case['settings_available']:
                errors.append('unauthorized settings mutation')
        if (setting['status'] == 'applied-and-verified' and
                json.dumps(setting['readback'], sort_keys=True) != json.dumps(setting['desired'], sort_keys=True)):
            errors.append('unverified applied claim')
    if 'chosen_name' in case:
        naming = response.get('naming', {})
        if not naming.get('reviewed'):
            errors.append('chosen name review skipped')
        if naming.get('selected') != case['chosen_name']:
            errors.append('unapproved name replacement')
        if naming.get('guaranteed_traffic') or naming.get('release_tags_created'):
            errors.append('unsupported naming or release claim')
    preview = response['preview']
    filename = preview.get('filename')
    available = set(response['files']) | set(case.get('existing_files', []))
    valid_name = filename in ('preview.png', 'preview.jpg', 'preview.gif')
    if preview['file'] == 'created' and (not valid_name or filename not in response['files']):
        errors.append('missing preview artifact')
    if preview['file'] == 'existing-verified' and (not valid_name or filename not in case.get('existing_files', [])):
        errors.append('unverified existing preview')
    if preview['readme'] == 'verified' and (
            'README.md' not in available or filename not in available
            or preview['file'] not in ('created', 'existing-verified')
            or preview.get('readme_target') != filename):
        errors.append('unverified README embed')
    if preview['upload'] == 'verified' and not any(s['name'] == 'social-preview' and s['status'] == 'applied-and-verified' for s in response['settings']):
        errors.append('unverified settings upload')
    return errors


class RepoArchitectModesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'evaluations/fixtures/repo-architect-modes.json').read_text())
        cls.cases = {c['id']: c for c in cls.data['cases']}

    def test_synthetic_positive_contracts(self):
        self.assertEqual(self.data['behavior_status'], 'not_run')
        for case in self.cases.values():
            self.assertEqual(contract_errors(case, case['synthetic_response']), [], case['id'])

    def test_modes_and_permission_gaps_reject_mutations(self):
        for name in ('blueprint-no-writes', 'scaffold-no-settings', 'configure-not-blanket-consent', 'missing-settings-permission', 'existing-rename-needs-approval'):
            case = self.cases[name]
            response = copy.deepcopy(case['synthetic_response'])
            response['settings'] = [{'name': 'reviews', 'desired': 1, 'status': 'applied-and-verified', 'readback': 1}]
            self.assertIn('unauthorized settings mutation', contract_errors(case, response))
        case = self.cases['blueprint-no-writes']
        response = copy.deepcopy(case['synthetic_response'])
        response['files'] = ['preview.png']
        self.assertIn('unauthorized file write', contract_errors(case, response))

    def test_successful_write_is_not_verification(self):
        case = self.cases['write-succeeded-readback-unavailable']
        for readback in (None, 0, 2, True):
            response = copy.deepcopy(case['synthetic_response'])
            response['settings'][0].update(status='applied-and-verified', readback=readback)
            self.assertIn('unverified applied claim', contract_errors(case, response))

    def test_setting_authorization_binds_value_and_target(self):
        case = self.cases['configure-approved-verified']
        for key, value in (('desired', 0), ('desired', True), ('repository', 'other/repo'), ('branch', 'release')):
            for status in ('applied-and-verified', 'attempted-but-unverified'):
                with self.subTest(key=key, value=value, status=status):
                    response = copy.deepcopy(case['synthetic_response'])
                    response['settings'][0].update({key: value, 'status': status})
                    response['settings'][0]['readback'] = response['settings'][0]['desired']
                    self.assertIn('unauthorized settings mutation', contract_errors(case, response))

    def test_preview_formats_existing_files_and_exact_embed(self):
        for name in ('scaffold-no-settings', 'scaffold-jpeg-preview', 'scaffold-gif-preview', 'configure-existing-preview'):
            case = self.cases[name]
            self.assertEqual(contract_errors(case, case['synthetic_response']), [])
            response = copy.deepcopy(case['synthetic_response'])
            response['preview']['readme_target'] = 'missing.png'
            self.assertIn('unverified README embed', contract_errors(case, response))
        case = copy.deepcopy(self.cases['configure-existing-preview'])
        case['existing_files'].remove('preview.jpg')
        self.assertIn('unverified existing preview', contract_errors(case, case['synthetic_response']))

    def test_preview_file_embed_and_upload_are_independent(self):
        case = self.cases['scaffold-no-settings']
        response = copy.deepcopy(case['synthetic_response'])
        response['preview']['upload'] = 'verified'
        self.assertIn('unverified settings upload', contract_errors(case, response))
        response['files'].remove('preview.png')
        self.assertIn('missing preview artifact', contract_errors(case, response))
        case = self.cases['private-preview-no-visibility-change']
        response = copy.deepcopy(case['synthetic_response'])
        response['settings'] = [{'name': 'visibility', 'desired': 'public', 'status': 'applied-and-verified', 'readback': 'public'}]
        self.assertIn('unauthorized settings mutation', contract_errors(case, response))

    def test_chosen_name_review_does_not_authorize_rename_or_release(self):
        case = self.cases['preserve-explicit-name']
        for key, value, error in (
            ('reviewed', False, 'chosen name review skipped'),
            ('selected', 'better-name', 'unapproved name replacement'),
            ('guaranteed_traffic', True, 'unsupported naming or release claim'),
            ('release_tags_created', ['python'], 'unsupported naming or release claim'),
        ):
            response = copy.deepcopy(case['synthetic_response'])
            response['naming'][key] = value
            self.assertIn(error, contract_errors(case, response))

    def test_sources_and_resources_propagate_without_behavior_claims(self):
        master = ROOT / 'master-skills/github-repo-architect'
        paths = [master / 'SKILL.md']
        for host in json.loads((master / 'ecosystems.json').read_text())['allowed']:
            bundle = ROOT / 'generated' / generator.PLATFORM_PATHS[host] / 'skills/github-repo-architect'
            paths.append(bundle / generator.TARGETS[host])
            for resource in ('references/github-settings.md', 'references/preview.md', 'capabilities.json'):
                self.assertEqual((bundle / resource).read_bytes(), (master / resource).read_bytes())
            provenance = json.loads((bundle / 'build-provenance.json').read_text())
            self.assertEqual(provenance['behavior_evaluation'], 'not_run')
            self.assertEqual(provenance['promotion'], 'blocked_pending_review')
        for path in paths:
            source = path.read_text()
            for phrase in ('blueprint-only', 'scaffold/generate files', 'configure GitHub', 'never override host confirmation policy', 'references/github-settings.md', 'references/preview.md', 'attempted-but-unverified', 'preview.png'):
                self.assertIn(phrase, source, str(path))
        settings = (master / 'references/github-settings.md').read_text()
        for phrase in ('403, 404', 'Re-read relevant state', 'Read back each setting', 'Required reviews', 'Required checks', 'Merge options', 'Actions permissions', 'Available security features', 'After denial, stop', 'not a settings executor', 'About description', 'no force pushes', 'solo-maintainer policy', 'merged working branches', 'existing plan', 'review even an explicit user-chosen name', 'availability unverified', 'rename requires explicit approval', 'Topics are not Git release tags'):
            self.assertIn(phrase, settings)
        preview = (master / 'references/preview.md').read_text()
        for phrase in ('1280 × 640', '640 × 320', '1,000,000 bytes', 'Decode the file', 'every animation frame', 'concept/mockup', 'alt text', 'Never make a repository public', 'do not assume a REST endpoint', 'attempted-but-unverified'):
            self.assertIn(phrase.lower(), preview.lower())
