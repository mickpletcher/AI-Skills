import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from activation_probe import nested_write_roots, observed_injections, observed_reads, resource_boundary


class ActivationProbeTests(unittest.TestCase):
    def test_profile_resources_are_allowed_without_allowing_the_parent_profile(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            work = root / 'repository'
            work.mkdir()
            skill = root / 'profile/skills/github-readme/SKILL.md'
            skill.parent.mkdir(parents=True)
            skill.write_text('name: github-readme')
            boundary = resource_boundary(work, [skill])
            allowed = [Path(line[2:]) for line in boundary.splitlines() if line.startswith('- ')]
            self.assertEqual(len(allowed), 1)
            self.assertTrue(allowed[0].samefile(skill.parent))
            self.assertFalse(allowed[0].samefile(root / 'profile'))
            self.assertNotIn('auth.json', boundary)
            self.assertIn('does not extend to parent profiles', boundary)

    def test_empty_duplicate_and_non_skill_catalogs_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            skill = root / 'github-readme/SKILL.md'
            skill.parent.mkdir()
            skill.write_text('body')
            other = skill.parent / 'auth.json'
            other.write_text('{}')
            for entries in ([], [skill, skill], [other]):
                with self.subTest(entries=entries), self.assertRaises(ValueError):
                    resource_boundary(root, entries)

    def test_nonexistent_resources_stop_before_inference(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(FileNotFoundError):
                resource_boundary(folder, [Path(folder) / 'missing/SKILL.md'])

    def test_only_completed_tool_output_with_full_body_proves_a_read(self):
        body = b'---\nname: github-readme\n---\n# Complete workflow\nPrivate canary 5c29\n'
        item = {'type': 'command_execution', 'exit_code': 0, 'aggregated_output': body.decode()}
        self.assertEqual(observed_reads([{'type': 'item.completed', 'item': item}], {'readme': body}), {'readme': True})
        for event in (
            {'type': 'item.started', 'item': item},
            {'type': 'item.completed', 'item': dict(item, type='agent_message')},
            {'type': 'item.completed', 'item': dict(item, exit_code=1, aggregated_output='Read failed: permission denied')},
            {'type': 'item.completed', 'item': dict(item, aggregated_output=body.decode()[:30])},
            {'type': 'item.completed', 'item': dict(item, aggregated_output='I used github-readme')},
        ):
            with self.subTest(event=event):
                self.assertEqual(observed_reads([event], {'readme': body}), {'readme': False})

    def test_compound_command_failure_does_not_erase_a_completed_body_read(self):
        body = b'# Workflow\nComplete instructions.\n'
        event = {'type': 'item.completed', 'item': {'type': 'command_execution', 'exit_code': 1,
                 'aggregated_output': body.decode() + '\nA later search returned no matches.\n'}}
        self.assertTrue(observed_reads([event], {'readme': body})['readme'])

    def test_windows_line_endings_do_not_hide_a_full_tool_read(self):
        body = b'# Workflow\nRead all of this.\n'
        event = {'type': 'item.completed', 'item': {'type': 'command_execution', 'exit_code': 0,
                 'aggregated_output': 'prefix\r\n# Workflow\r\nRead all of this.\r\nsuffix'}}
        self.assertTrue(observed_reads([event], {'readme': body})['readme'])

    def test_typed_invocation_needs_recorded_full_user_input_injection(self):
        body = b'# Workflow\nExact complete instructions.\n'
        text = '<skill>\n<name>github-readme</name>\n<path>/probe/SKILL.md</path>\n' + body.decode() + '</skill>'
        message = {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': text}]}
        self.assertTrue(observed_injections([message], {'github-readme': body})['github-readme'])
        for other in (
            dict(message, role='assistant'),
            {'type': 'skill', 'name': 'github-readme', 'path': '/probe/SKILL.md'},
            dict(message, content=[{'type': 'input_text', 'text': text.replace('Exact complete instructions.', '')}]),
            dict(message, content=[{'type': 'input_text', 'text': text.replace('github-readme', 'another-skill')}]),
        ):
            with self.subTest(other=other):
                self.assertFalse(observed_injections([other], {'github-readme': body})['github-readme'])

    def test_nested_write_scope_stays_inside_the_named_repository(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            work = root / 'repository'
            child = work / 'component'
            child.mkdir(parents=True)
            allowed = nested_write_roots(work, child, True)
            self.assertEqual(len(allowed), 1)
            self.assertTrue(Path(allowed[0]).samefile(work))
            self.assertEqual(nested_write_roots(work, child, False), [])
            self.assertEqual(nested_write_roots(work, work, True), [])
            with self.assertRaises(ValueError):
                nested_write_roots(work, root, True)

    def test_path_aliases_preserve_identity_without_expanding_write_scope(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            work = root / 'repository'
            child = work / 'component'
            child.mkdir(parents=True)
            allowed = nested_write_roots(work / '..' / 'repository', child / '..' / 'component', True)
            self.assertEqual(len(allowed), 1)
            self.assertTrue(Path(allowed[0]).samefile(work))
            with self.assertRaises(ValueError):
                nested_write_roots(work, child / '..' / '..', True)
