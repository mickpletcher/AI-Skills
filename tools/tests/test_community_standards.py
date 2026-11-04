"""Offline community-file and issue-form checks, not hosted GitHub UI validation."""
from pathlib import Path
import re
import sys
import unittest
from urllib.parse import parse_qs, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from skill_repository import UniqueLoader
import yaml


class CommunityStandardsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = ROOT / '.github/ISSUE_TEMPLATE'
        cls.forms = {
            path.name: yaml.load(path.read_text(encoding='utf-8'), Loader=UniqueLoader)
            for path in cls.folder.glob('*.yml') if path.name != 'config.yml'
        }

    def test_required_files_are_discoverable_and_nonempty(self):
        for name in ('CODE_OF_CONDUCT.md', 'SECURITY.md', 'ACCESSIBILITY.md',
                     'SUPPORT.md', 'CONTRIBUTING.md', 'LICENSE', 'README.md',
                     '.github/PULL_REQUEST_TEMPLATE.md'):
            with self.subTest(path=name):
                self.assertTrue((ROOT / name).read_text(encoding='utf-8').strip())

    def test_issue_form_subset_matches_github_schema(self):
        self.assertEqual(set(self.forms), {'bug_report.yml', 'feature_request.yml',
                                         'documentation.yml', 'accessibility.yml', 'question.yml'})
        names = set()
        for filename, form in self.forms.items():
            with self.subTest(form=filename):
                self.assertEqual(set(form), {'name', 'description', 'title', 'body'})
                for key in ('name', 'description', 'title'):
                    self.assertIsInstance(form[key], str)
                    self.assertTrue(form[key].strip())
                self.assertNotIn(form['name'], names)
                names.add(form['name'])
                self.assertIsInstance(form['body'], list)
                self.assertTrue(form['body'])
                ids, labels = set(), set()
                required_inputs = 0
                for field in form['body']:
                    kind = field['type']
                    self.assertIn(kind, ('markdown', 'input', 'textarea'))
                    if kind == 'markdown':
                        self.assertEqual(set(field), {'type', 'attributes'})
                        self.assertIsInstance(field['attributes']['value'], str)
                        continue
                    self.assertEqual(set(field), {'type', 'id', 'attributes', 'validations'})
                    self.assertRegex(field['id'], r'^[A-Za-z0-9_-]+$')
                    self.assertNotIn(field['id'], ids)
                    ids.add(field['id'])
                    for key in ('label', 'description'):
                        self.assertIsInstance(field['attributes'][key], str)
                        self.assertTrue(field['attributes'][key])
                    self.assertNotIn(field['attributes']['label'], labels)
                    labels.add(field['attributes']['label'])
                    self.assertEqual(set(field['validations']), {'required'})
                    self.assertIsInstance(field['validations']['required'], bool)
                    required_inputs += field['validations']['required']
                self.assertGreater(required_inputs, 0)

    def test_forms_warn_about_public_reports_and_link_security_policy(self):
        for filename, form in self.forms.items():
            with self.subTest(form=filename):
                intro = form['body'][0]['attributes']['value']
                self.assertIn('public', intro)
                self.assertIn('credentials', intro)
                self.assertIn('/blob/main/SECURITY.md', intro)
                self.assertIn('/blob/main/CODE_OF_CONDUCT.md', intro)

    def test_configuration_preserves_blank_issue_alternative(self):
        config = yaml.load((self.folder / 'config.yml').read_text(encoding='utf-8'), Loader=UniqueLoader)
        self.assertEqual(set(config), {'blank_issues_enabled', 'contact_links'})
        self.assertIs(config['blank_issues_enabled'], True)
        self.assertTrue(config['contact_links'])
        for link in config['contact_links']:
            self.assertEqual(set(link), {'name', 'url', 'about'})
            self.assertTrue(all(isinstance(v, str) and v for v in link.values()))

    def test_embedded_repository_links_and_template_targets_exist(self):
        paths = list(self.folder.glob('*.yml')) + [ROOT / '.github/PULL_REQUEST_TEMPLATE.md']
        paths += [ROOT / name for name in ('CODE_OF_CONDUCT.md', 'SECURITY.md',
                                         'ACCESSIBILITY.md', 'SUPPORT.md')]
        prefix = 'https://github.com/mickpletcher/AI-Skills/'
        for path in paths:
            for url in re.findall(r'https://[^\s)]+', path.read_text(encoding='utf-8')):
                if not url.startswith(prefix):
                    continue
                parsed = urlsplit(url)
                if '/blob/main/' in parsed.path:
                    target = unquote(parsed.path.split('/blob/main/', 1)[1])
                    self.assertTrue((ROOT / target).is_file(), (path.name, url))
                for template in parse_qs(parsed.query).get('template', []):
                    self.assertIn(template, self.forms, (path.name, url))

    def test_accessibility_environment_is_optional_and_claims_are_bounded(self):
        environment = next(f for f in self.forms['accessibility.yml']['body']
                           if f.get('id') == 'environment')
        self.assertIs(environment['validations']['required'], False)
        statement = (ROOT / 'ACCESSIBILITY.md').read_text(encoding='utf-8')
        self.assertIn('No repository-wide assistive-technology audit', statement)
        self.assertIn('blank issue', statement)
        policy = (ROOT / 'SECURITY.md').read_text(encoding='utf-8')
        self.assertIn('does not mean it is enabled', policy)
        self.assertIn('Include no vulnerability details', policy)


if __name__ == '__main__':
    unittest.main()
