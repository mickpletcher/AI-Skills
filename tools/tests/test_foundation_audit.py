"""Offline requirement and provenance regressions, not behavioral evaluation."""
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
from model_profiles import load_contract, model_guidance, load_profile


class FoundationAuditTests(unittest.TestCase):
    def test_audit_pins_sources_and_preserves_prior_master(self):
        records = list((ROOT/'master-skills').glob('*/foundation-audit.json'))
        self.assertEqual({p.parent.name for p in records},
                         {'github-readme', 'github-repo-architect', 'powershell-refactor'})
        for path in records:
            record = json.loads(path.read_text(encoding='utf-8'))
            source = ROOT/record['source']
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), record['source_sha256'])
            self.assertEqual(re.findall(r'^## (.+)$', source.read_text(encoding='utf-8'), re.M),
                             record['audited_source_sections'])
            master = (path.parent/'SKILL.md').read_text(encoding='utf-8')
            for insertion in reversed(record.get('subsequent_insertions', [])):
                self.assertEqual(master.count(insertion['text']), 1)
                master = master.replace(insertion['text'], '')
                self.assertEqual(hashlib.sha256(master.encode()).hexdigest(),
                                 insertion['prior_master_sha256'])
            inserted = record['restored_text']
            self.assertEqual(master.count(inserted), 1)
            self.assertEqual(hashlib.sha256(master.replace(inserted, '').encode()).hexdigest(),
                             record['prior_master_sha256'])
            self.assertEqual(record['behavior_evaluation'], 'not_run')
            self.assertTrue(record['intentional_adaptations'])

    def test_scaffold_templates_and_ci_requirements_reach_every_candidate(self):
        required = [
            '.github/ISSUE_TEMPLATE/bug_report.md',
            'Problem; Steps to reproduce; Expected result; Actual result; Environment.',
            '.github/ISSUE_TEMPLATE/feature_request.md',
            'Use case; Proposed behavior; Inputs; Outputs; Notes.',
            '.github/pull_request_template.md', 'Summary; Changes; Tests; Risk; Checklist.',
            'pull requests and pushes to the default branch',
            'install dependencies, run configured lint checks, and run tests',
            'implementation, test and review prompts', '.gitignore',
            'do not represent TODO placeholders as runnable application CI',
        ]
        self.assert_requirements('github-repo-architect', required)

    def test_readme_and_refactor_requirements_reach_every_candidate(self):
        self.assert_requirements('github-readme', [
            'Variable | Required | Example | What It Controls',
            'Problem | Likely Cause | Fix', 'safest, simplest usage command first',
            'numbered setup steps', 'license last', 'placement notes',
            'complete README content in the response', 'roughly half or more is stale',
        ])
        self.assert_requirements('powershell-refactor', [
            'Never introduce new analyzer violations', 'PSScriptAnalyzerSettings.psd1',
            'list each remaining violation with a one-line reason',
            'mark this gate not verified', '## Refactor Summary',
            'measured before -> after, or not measured', 'Out of scope findings',
            'checking callers before deletion', 'pasted source is sufficient',
        ])

    def assert_requirements(self, name, requirements):
        folder = ROOT/'master-skills'/name
        paths = [folder/'SKILL.md']
        for platform in json.loads((folder/'ecosystems.json').read_text(encoding='utf-8'))['allowed']:
            generated = ROOT/'generated'/platform/'skills'/name
            paths.append(generated/('SKILL.md' if platform in ('claude', 'codex') else 'instructions.md'))
            self.assertEqual((folder/'foundation-audit.json').read_bytes(),
                             (generated/'foundation-audit.json').read_bytes())
        for path in paths:
            text = path.read_text(encoding='utf-8')
            for requirement in requirements:
                self.assertIn(requirement, text, str(path))

    def test_text_only_modes_keep_file_operations_gated(self):
        profile, _ = load_profile(ROOT, 'baseline')
        profile['capabilities']['file_access'] = 'unsupported'
        names = ('alpaca-trading', 'astrophotography-processing', 'github-readme',
                 'github-repo-architect', 'powershell-refactor', 'pihole-csv-analyzer', 'spec-writer')
        for name in names:
            contract = load_contract(ROOT/'master-skills'/name/'SKILL.md')
            self.assertNotIn('file_access', contract['required'])
            condition = contract['conditional']['file_access']
            for phrase in ('Required for', 'Not required for', 'stop the file-dependent operation',
                           'never claim files were inspected, saved or verified'):
                self.assertIn(phrase, condition)
            overlay = model_guidance(profile, contract)
            self.assertIn('Conditional file_access: unsupported.', overlay)
            self.assertIn(condition, overlay)
            self.assertIn('never grant authorization', overlay)
