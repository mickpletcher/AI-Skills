import unittest
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]

class WorkflowTests(unittest.TestCase):
    def test_pr_matrix_is_unconditional_read_only_and_runs_installer_tests(self):
        workflow=yaml.load((ROOT/'.github/workflows/validate.yml').read_text(),Loader=yaml.BaseLoader)
        self.assertIn('pull_request',workflow['on'])
        self.assertFalse(workflow['on']['pull_request'])
        self.assertEqual(workflow['permissions'],{'contents':'read'})
        job=workflow['jobs']['validate']
        self.assertEqual(set(job['strategy']['matrix']['os']),{'ubuntu-latest','windows-latest'})
        self.assertNotIn('if',job)
        self.assertNotIn('continue-on-error',job)
        commands='\n'.join(step.get('run','') for step in job['steps'])
        for command in ('unittest discover','skill_repository.py validate','Validate-SkillFolders.ps1',
                        'Validate-SkillQuality.ps1','Initialize-ClaudeSkills.Tests.ps1','evaluate.py self-test'):
            self.assertIn(command,commands)
        self.assertFalse(any('continue-on-error' in step for step in job['steps']))
        setup = next(step for step in job['steps'] if step.get('uses', '').startswith('actions/setup-python@'))
        self.assertEqual(setup['with']['cache-dependency-path'], 'requirements-dev.txt')

    def test_release_is_inactive_and_draft_only(self):
        self.assertFalse((ROOT/'.github/workflows/release.yml').exists())
        workflow=yaml.load((ROOT/'.github/workflow-templates/release.yml').read_text(),Loader=yaml.BaseLoader)
        commands='\n'.join(step.get('run','') for step in workflow['jobs']['draft']['steps'])
        self.assertIn('prepare_release.py',commands)
        self.assertIn('--draft --verify-tag',commands)
        self.assertNotIn('git push',commands)
