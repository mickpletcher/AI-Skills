import hashlib
import json
import sys
import tempfile
import unittest
import shutil
import contextlib
import io
import subprocess
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
import generate_master_skills as generator
from skill_repository import frontmatter, link_errors


class MigrationTests(unittest.TestCase):
    def fixture(self, root):
        for folder in ('schemas', 'model-profiles'):
            shutil.copytree(ROOT/folder, root/folder)
        source = root/'master-skills/example-skill'
        shutil.copytree(ROOT/'master-skills/example-skill', source)
        return source

    def test_destination_type_collisions_fail_before_any_writes(self):
        for name in ('generated', 'generated/openai', 'generated/openai/chatgpt',
                     'generated/openai/chatgpt/skills/example-skill',
                     'generated/openai/chatgpt/skills/example-skill/instructions.md',
                     'generated/.resource-manifest.json'):
            with self.subTest(path=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp).resolve()
                self.fixture(root)
                destination = root/name
                destination.parent.mkdir(parents=True, exist_ok=True)
                if destination.suffix:
                    destination.mkdir()
                else:
                    destination.write_bytes(b'user file')
                for check in (False, True):
                    with patch.object(generator, 'ROOT', root), \
                         patch.object(Path, 'write_bytes', side_effect=AssertionError('Partial write')):
                        with self.assertRaisesRegex(ValueError, 'directory|file type'):
                            generator.generate(check=check)
                self.assertFalse((root/'generated/claude').exists())
                if destination.is_file():
                    self.assertEqual(destination.read_bytes(), b'user file')

    def test_portable_resource_collisions_fail_before_any_writes(self):
        for name in ('INSTRUCTIONS.md', 'Build-Provenance.json', 'instructions.md/asset.bin'):
            with self.subTest(path=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp).resolve()
                source = self.fixture(root)
                resource = source/name
                resource.parent.mkdir(parents=True, exist_ok=True)
                resource.write_bytes(b'fixture')
                with patch.object(generator, 'ROOT', root), \
                     patch.object(Path, 'write_bytes', side_effect=AssertionError('Partial write')):
                    with self.assertRaisesRegex(ValueError, 'colli'):
                        generator.generate()
                self.assertFalse((root/'generated').exists())

    def test_linked_inputs_and_outputs_are_rejected(self):
        cases = ('master-skills', 'master-skills/example-skill/SKILL.md',
                 'adapters/claude/example-skill/append.md', 'adapters/openai',
                 'adapters/openai/codex/example-skill/append.md', 'model-profiles',
                 'model-profiles/baseline.json', 'schemas', 'generated',
                 'generated/openai', 'generated/openai/chatgpt/skills/example-skill', 'generated/.resource-manifest.json')
        for name in cases:
            with self.subTest(path=name), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp).resolve()
                root = base/'source'
                self.fixture(root)
                link = root/name
                directory = not link.suffix
                target = base/'target'
                if link.exists():
                    shutil.move(str(link), str(target))
                elif directory:
                    target.mkdir()
                else:
                    target.write_bytes(b'external fixture')
                link.parent.mkdir(parents=True, exist_ok=True)
                try:
                    link.symlink_to(target, target_is_directory=directory)
                except OSError as exc:
                    if getattr(exc, 'winerror', None) == 1314:
                        self.skipTest('Windows symlink privilege unavailable')
                    raise
                with patch.object(generator, 'ROOT', root), \
                     patch.object(Path, 'write_bytes', side_effect=AssertionError('Partial write')):
                    for check in (False, True):
                        with self.assertRaisesRegex(ValueError, 'Symlink|junction'):
                            generator.generate(check=check)

    @unittest.skipUnless(sys.platform == 'win32', 'Windows junction semantics')
    def test_windows_junction_inputs_and_outputs_are_rejected(self):
        for name in ('master-skills', 'adapters', 'adapters/openai', 'model-profiles', 'schemas',
                     'generated', 'generated/openai', 'generated/openai/chatgpt/skills/example-skill',
                     'generated-models', 'generated-models/synthetic/openai'):
            with self.subTest(path=name), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp).resolve()
                root = base/'source'
                self.fixture(root)
                profile = json.loads((root/'model-profiles/baseline.json').read_text(encoding='utf-8'))
                profile.update(id='synthetic', provider='synthetic', model_id='fixture-v1')
                (root/'model-profiles/synthetic.json').write_text(json.dumps(profile), encoding='utf-8')
                link = root/name
                target = base/'target'
                if link.exists():
                    shutil.move(str(link), str(target))
                else:
                    target.mkdir()
                link.parent.mkdir(parents=True, exist_ok=True)
                result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(target)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                try:
                    with patch.object(generator, 'ROOT', root), \
                         patch.object(Path, 'write_bytes', side_effect=AssertionError('Partial write')):
                        for check in (False, True):
                            with self.assertRaisesRegex(ValueError, 'junction'):
                                generator.generate(check=check, model_profile='synthetic' if name.startswith('generated-models') else 'baseline')
                finally:
                    link.rmdir()

    def test_all_shipped_claude_skills_have_masters_and_candidates(self):
        originals = {p.parent.name for p in (ROOT/'claude/skills').glob('*/SKILL.md')}
        masters = {p.parent.name for p in (ROOT/'master-skills').glob('*/SKILL.md')}
        self.assertEqual(masters, originals | {'example-skill'})
        catalog = json.loads((ROOT/'master-skills/catalog.json').read_text(encoding="utf-8"))
        self.assertEqual({entry['name'] for entry in catalog['skills']}, masters)
        for entry in catalog['skills']:
            self.assertEqual(entry['description'], frontmatter(ROOT/'master-skills'/entry['name']/'SKILL.md', ROOT)['description'])
            self.assertEqual(set(entry['targets']), set(json.loads((ROOT/'master-skills'/entry['name']/'ecosystems.json').read_text(encoding='utf-8'))['allowed']))
        for name in masters:
            allowed = json.loads((ROOT/'master-skills'/name/'ecosystems.json').read_text(encoding='utf-8'))['allowed']
            for platform, filename in generator.TARGETS.items():
                if platform not in allowed:
                    self.assertFalse((ROOT/'generated'/generator.PLATFORM_PATHS[platform]/'skills'/name).exists())
                    continue
                target = ROOT/'generated'/generator.PLATFORM_PATHS[platform]/'skills'/name/filename
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
                    for platform in json.loads((path.parent/'ecosystems.json').read_text(encoding='utf-8'))['allowed']:
                        self.assertEqual(data, (ROOT/'generated'/generator.PLATFORM_PATHS[platform]/'skills'/path.parent.name/rel).read_bytes())
                for rel, digest in record['retained_in_original_sha256'].items():
                    self.assertEqual(hashlib.sha256((source.parent/rel).read_bytes()).hexdigest(), digest)

    def test_bundle_links_resolve_in_each_target(self):
        for root in [ROOT, *(ROOT/'generated'/generator.PLATFORM_PATHS[platform]/'skills' for platform in generator.TARGETS)]:
            self.assertEqual(link_errors(root), [], str(root))

    def test_resources_detect_drift_removal_and_unmanaged_collision_without_writes(self):
        for mutation in ('drift', 'removed-source', 'unmanaged'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                shutil.copytree(ROOT/'schemas', root/'schemas')
                shutil.copytree(ROOT/'model-profiles', root/'model-profiles')
                source = root/'master-skills/sample/SKILL.md'
                source.parent.mkdir(parents=True)
                source.write_text('---\nname: sample\ndescription: Test bundle\n---\nBody\n')
                shutil.copyfile(ROOT/'master-skills/example-skill/capabilities.json', source.parent/'capabilities.json')
                shutil.copyfile(ROOT/'master-skills/example-skill/ecosystems.json', source.parent/'ecosystems.json')
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
            shutil.copytree(ROOT/'model-profiles', root/'model-profiles')
            source = root/'master-skills/sample/SKILL.md'
            source.parent.mkdir(parents=True)
            source.write_text('---\nname: sample\ndescription: Test bundle\n---\nBody\n')
            shutil.copyfile(ROOT/'master-skills/example-skill/capabilities.json', source.parent/'capabilities.json')
            shutil.copyfile(ROOT/'master-skills/example-skill/ecosystems.json', source.parent/'ecosystems.json')
            resource = source.parent/'asset.bin'
            resource.write_bytes(b'old')
            with patch.object(generator, 'ROOT', root), contextlib.redirect_stdout(io.StringIO()):
                generator.generate()
                resource.write_bytes(b'new')
                (root/'generated/openai/codex/skills/sample/asset.bin').unlink()
                generator.generate()
                generator.generate(check=True)
                for platform in generator.TARGETS:
                    self.assertEqual((root/'generated'/generator.PLATFORM_PATHS[platform]/'skills/sample/asset.bin').read_bytes(), b'new')
