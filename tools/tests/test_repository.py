import hashlib
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import skill_repository as repo

class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / 'schemas').mkdir()
        shutil.copy(repo.ROOT / 'schemas/skill-frontmatter.schema.json', self.root / 'schemas')
        self.folder = self.root / 'claude/skills/example'
        self.folder.mkdir(parents=True)
        self.source = self.folder / 'SKILL.md'
        self.source.write_text('---\nname: example\ndescription: Example purpose\nversion: 1.0.0\n---\n' + ''.join('\n## '+s+'\n\nExample.\n' for s in repo.SECTIONS))
        (self.folder / 'README.md').write_text('[Source](SKILL.md)\n')
        (self.folder / 'completedchanges.md').write_text('# History\n')
        self.build()

    def build(self):
        (self.folder / 'example.skill').write_bytes(repo.package_bytes(self.folder))

    def issues(self):
        return repo.validate(self.root)[1]

    def test_valid_fixture(self):
        self.assertEqual(self.issues(), [])

    def test_openai_discovery_keeps_target_ids_and_nested_catalog_paths(self):
        folder = self.root / 'openai/chatgpt/skills/example'
        folder.mkdir(parents=True)
        (folder / 'instructions.md').write_bytes(self.source.read_bytes())
        (folder / 'README.md').write_text('[Source](instructions.md)\n')
        legacy = self.root / 'chatgpt/skills/obsolete'
        legacy.mkdir(parents=True)
        self.assertEqual(self.issues(), [])
        records = json.loads(repo.generated(self.root)['catalog.json'])['skills']
        self.assertEqual({r['id'] for r in records}, {'claude/example', 'chatgpt/example'})
        target = next(r for r in records if r['platform'] == 'chatgpt')
        self.assertEqual(target['source'], 'openai/chatgpt/skills/example/instructions.md')
        self.assertEqual(target['installation'], 'docs/installation.md#chatgpt')

    def test_microsoft_discovery_keeps_copilot_ids_and_excludes_reserved_studio(self):
        folder = self.root / 'microsoft/copilot/skills/example'
        folder.mkdir(parents=True)
        (folder / 'instructions.md').write_bytes(self.source.read_bytes())
        (folder / 'README.md').write_text('[Source](instructions.md)\n')
        for unsupported in ('copilot/skills/obsolete', 'microsoft/copilot-studio/skills/reserved'):
            target = self.root / unsupported
            target.mkdir(parents=True)
            (target / 'instructions.md').write_bytes(self.source.read_bytes())
        self.assertEqual(self.issues(), [])
        records = json.loads(repo.generated(self.root)['catalog.json'])['skills']
        self.assertEqual({r['id'] for r in records}, {'claude/example', 'copilot/example'})
        entry = next(r for r in records if r['platform'] == 'copilot')
        self.assertEqual(entry['source'], 'microsoft/copilot/skills/example/instructions.md')
        self.assertEqual(entry['installation'], 'docs/installation.md#copilot')

    def test_empty_repository_and_folder_root_fail(self):
        shutil.rmtree(self.root / 'claude')
        self.assertIn('No skills checked', '\n'.join(self.issues()))
        empty = self.root / 'empty'; empty.mkdir()
        self.assertTrue(repo.validate(empty, True)[1])

    def test_missing_source_not_silently_skipped(self):
        self.source.unlink()
        self.assertIn('missing exact-case file SKILL.md', '\n'.join(self.issues()))

    def test_case_sensitive_source_on_any_filesystem(self):
        self.source.rename(self.folder / 'temporary')
        (self.folder / 'temporary').rename(self.folder / 'skill.md')
        self.assertIn('missing exact-case file SKILL.md', '\n'.join(self.issues()))
        self.assertTrue(repo.validate(self.folder.parent, True)[1])

    def test_missing_readme_package_and_history(self):
        for name in ('README.md', 'example.skill', 'completedchanges.md'):
            (self.folder / name).unlink()
        errors = '\n'.join(self.issues())
        for name in ('README.md', 'example.skill', 'completedchanges.md'):
            self.assertIn('missing exact-case file '+name, errors)

    def test_invalid_yaml_schema(self):
        for content in ('name: example\ndescription: [a, b]', 'name: wrong\ndescription: x',
                        'name: example\nname: example\ndescription: x',
                        'name: example\ndescription: x\nversion: 1.2',
                        'name: example\ndescription: x\nunknown: value',
                        'name: example\ndescription: [broken'):
            self.source.write_text('---\n'+content+'\n---\n')
            with self.assertRaises((ValueError, repo.yaml.YAMLError)):
                repo.frontmatter(self.source, self.root)

    def test_missing_version_is_not_invented(self):
        self.source.write_text(self.source.read_text().replace('version: 1.0.0\n', ''))
        self.build()
        manifest = json.loads(repo.generated(self.root)['catalog.json'])
        self.assertIsNone(manifest['skills'][0]['version'])
        self.assertIsNone(manifest['skills'][0]['last_model_evaluation'])

    def test_content_changes_detected_without_timestamp_assumptions(self):
        self.source.write_text(self.source.read_text()+'\nChanged behavior.\n')
        self.assertIn('package/source bytes differ', '\n'.join(self.issues()))

    def test_missing_extra_and_corrupt_archive_entries(self):
        package = self.folder / 'example.skill'
        with zipfile.ZipFile(package, 'w') as z:
            z.writestr('extra.txt', 'bad')
        self.assertIn('package file set differs', '\n'.join(self.issues()))
        package.write_bytes(b'not a ZIP')
        self.assertIn('unreadable package', '\n'.join(self.issues()))

    def test_reproducible_build_normalizes_lines_not_mtime(self):
        before = repo.package_bytes(self.folder)
        self.source.write_bytes(self.source.read_bytes().replace(b'\r\n', b'\n').replace(b'\n', b'\r\n'))
        self.assertEqual(before, repo.package_bytes(self.folder))
        (self.folder / 'future-upgrades.md').write_text('local planning, not shipped')
        self.assertEqual(before, repo.package_bytes(self.folder))

    def test_package_member_order_is_case_sensitive_on_every_host(self):
        for name in ('Z.txt', 'a.txt'):
            (self.folder / name).write_text(name)
        import io
        with zipfile.ZipFile(io.BytesIO(repo.package_bytes(self.folder))) as archive:
            self.assertEqual(archive.namelist(), sorted(archive.namelist()))

    def test_broken_links_anchors_and_case(self):
        (self.folder / 'README.md').write_text('[bad](missing.md) [case](skill.md) [anchor](SKILL.md#missing) [drive](C:/Users/a.md)')
        self.assertEqual(len(repo.link_errors(self.root)), 4)

    def test_valid_reference_links_encoded_names_and_anchors(self):
        (self.folder / 'a b.md').write_text('# Hello World\n')
        (self.folder / 'README.md').write_text('[hello][ref]\n\n[ref]: a%20b.md#hello-world\n[Source](SKILL.md#use-when)\n```md\n[example](not-real.md)\n```\n')
        self.assertEqual(repo.link_errors(self.root), [])

    def test_undefined_reference_link(self):
        (self.folder / 'README.md').write_text('[hello][missing]\n')
        self.assertIn('missing link definition', '\n'.join(repo.link_errors(self.root)))

    def test_case_colliding_archive_entries(self):
        with zipfile.ZipFile(self.folder / 'example.skill', 'w') as z:
            z.writestr('SKILL.md', 'one'); z.writestr('skill.md', 'two')
        self.assertIn('duplicate archive entries', '\n'.join(self.issues()))

    def test_schema_extension_fails_closed(self):
        with self.assertRaises(ValueError):
            repo.schema_check('x', {'type': 'string', 'unsupported': True})

class MovedReferenceTests(unittest.TestCase):
    def test_moved_workflow_sections_are_unchanged(self):
        moves = json.loads((repo.ROOT/'docs/reference-moves.json').read_text())['moves']
        for move in moves:
            content = repo.canonical_bytes(repo.ROOT/move['reference'])
            self.assertEqual(hashlib.sha256(content).hexdigest(), move['sha256'], move['reference'])

if __name__ == '__main__':
    unittest.main()
