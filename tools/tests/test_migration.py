import hashlib
import json
import sys
import tempfile
import unittest
import shutil
import contextlib
import io
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
import generate_master_skills as generator
from skill_repository import frontmatter, link_errors


class MigrationTests(unittest.TestCase):
    def test_all_shipped_claude_skills_have_masters_and_candidates(self):
        originals = {p.parent.name for p in (ROOT/'claude/skills').glob('*/SKILL.md')}
        masters = {p.parent.name for p in (ROOT/'master-skills').glob('*/SKILL.md')}
        self.assertEqual(masters, originals | {'example-skill'})
        catalog = json.loads((ROOT/'master-skills/catalog.json').read_text(encoding="utf-8"))
        self.assertEqual({entry['name'] for entry in catalog['skills']}, masters)
        for entry in catalog['skills']:
            self.assertEqual(entry['description'], frontmatter(ROOT/'master-skills'/entry['name']/'SKILL.md', ROOT)['description'])
            self.assertEqual(set(entry['targets']), set(generator.TARGETS))
        for name in masters:
            for platform, filename in generator.TARGETS.items():
                target = ROOT/'generated'/platform/'skills'/name/filename
                frontmatter(target, ROOT)
        self.assertTrue(all(entry['status'] == 'candidate' and entry['behavior_evaluation'] == 'not_run'
                            for entry in catalog['skills']))

    def test_migration_preserves_source_metadata_and_every_dependency(self):
        records = list((ROOT/'master-skills').glob('*/migration.json'))
        self.assertEqual(len(records), 32)
        for path in records:
            with self.subTest(skill=path.parent.name):
                record = json.loads(path.read_text(encoding="utf-8"))
                source = ROOT/record['source']
                self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), record['source_sha256'])
                self.assertEqual(frontmatter(source, ROOT), record['source_frontmatter'])
                original = source.read_text(encoding='utf-8-sig')
                for old, new in record['transformations'].items():
                    self.assertIn(old, original)
                    original = original.replace(old, new)
                candidate = (path.parent/'SKILL.md').read_text(encoding="utf-8")
                self.assertTrue(candidate.startswith(original + '\n## Host Capabilities\n'))
                actual = {p.relative_to(source.parent).as_posix() for p in source.parent.rglob('*')
                          if p.is_file() and p != source}
                self.assertEqual(actual, set(record['supporting_files_sha256']) | set(record['retained_in_original_sha256']))
                for rel, digest in record['supporting_files_sha256'].items():
                    data = (path.parent/rel).read_bytes()
                    self.assertEqual(hashlib.sha256(data).hexdigest(), digest)
                    self.assertEqual(data, (source.parent/rel).read_bytes())
                    for platform in generator.TARGETS:
                        self.assertEqual(data, (ROOT/'generated'/platform/'skills'/path.parent.name/rel).read_bytes())
                for rel, digest in record['retained_in_original_sha256'].items():
                    self.assertEqual(hashlib.sha256((source.parent/rel).read_bytes()).hexdigest(), digest)

    def test_bundle_links_resolve_in_each_target(self):
        for root in [ROOT, *(ROOT/'generated'/platform/'skills' for platform in generator.TARGETS)]:
            self.assertEqual(link_errors(root), [], str(root))

    def test_resources_detect_drift_removal_and_unmanaged_collision_without_writes(self):
        for mutation in ('drift', 'removed-source', 'unmanaged'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                shutil.copytree(ROOT/'schemas', root/'schemas')
                source = root/'master-skills/sample/SKILL.md'
                source.parent.mkdir(parents=True)
                source.write_text('---\nname: sample\ndescription: Test bundle\n---\nBody\n')
                resource = source.parent/'asset.bin'
                resource.write_bytes(b'\x00\xfforiginal')
                with patch.object(generator, 'ROOT', root), contextlib.redirect_stdout(io.StringIO()):
                    generator.generate()
                    target = root/'generated/claude/skills/sample/asset.bin'
                    if mutation == 'drift':
                        target.write_bytes(b'user edit')
                    elif mutation == 'removed-source':
                        resource.unlink()
                    else:
                        resource = source.parent/'new.bin'
                        resource.write_bytes(b'new resource')
                        (target.parent/'new.bin').write_bytes(b'user file')
                    before = {p: p.read_bytes() for p in (root/'generated').rglob('*') if p.is_file()}
                    with self.assertRaises((RuntimeError, SystemExit)):
                        generator.generate()
                    self.assertEqual(before, {p: p.read_bytes() for p in (root/'generated').rglob('*') if p.is_file()})
                    with self.assertRaises(SystemExit):
                        generator.generate(check=True)

    def test_resource_updates_and_missing_file_repair(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT/'schemas', root/'schemas')
            source = root/'master-skills/sample/SKILL.md'
            source.parent.mkdir(parents=True)
            source.write_text('---\nname: sample\ndescription: Test bundle\n---\nBody\n')
            resource = source.parent/'asset.bin'
            resource.write_bytes(b'old')
            with patch.object(generator, 'ROOT', root), contextlib.redirect_stdout(io.StringIO()):
                generator.generate()
                resource.write_bytes(b'new')
                (root/'generated/codex/skills/sample/asset.bin').unlink()
                generator.generate()
                generator.generate(check=True)
                for platform in generator.TARGETS:
                    self.assertEqual((root/'generated'/platform/'skills/sample/asset.bin').read_bytes(), b'new')
