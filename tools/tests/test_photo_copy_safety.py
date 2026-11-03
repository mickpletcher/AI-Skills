import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT/'master-skills/photo-rename/scripts/safe_photo_copy.py'
spec = importlib.util.spec_from_file_location('safe_photo_copy', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class PhotoCopySafetyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.src = self.root/'source'; self.src.mkdir()
        self.dst = self.root/'output'; self.dst.mkdir()
        (self.src/'IMG.jpg').write_bytes(b'synthetic photo bytes\x00\xff')
        (self.src/'IMG2.jpg').write_bytes(b'another synthetic fixture')

    def snapshot(self, folder):
        return {p.name: p.read_bytes() for p in folder.iterdir() if p.is_file()}

    def test_occupied_names_suffixes_case_and_hash_preservation(self):
        for n in ('BEACH.jpg', 'beach_01.jpg', 'beach_02.jpg'):
            (self.dst/n).write_bytes(b'pre-existing '+n.encode())
        before_src, before_dst = self.snapshot(self.src), self.snapshot(self.dst)
        plan = helper.plan(self.src, self.dst, [('IMG.jpg', 'beach.jpg'), ('IMG2.jpg', 'beach.jpg')])
        self.assertEqual([r['destination'] for r in plan['files']], ['beach_03.jpg','beach_04.jpg'])
        self.assertEqual(before_dst, self.snapshot(self.dst))
        result = helper.apply(plan)
        self.assertTrue(all(r['status'] == 'copied_verified' for r in result['files']))
        self.assertEqual(before_src, self.snapshot(self.src))
        for name, data in before_dst.items(): self.assertEqual((self.dst/name).read_bytes(), data)
        for r in result['files']:
            self.assertEqual(helper.sha(self.src/r['source']), r['sha256'])
            self.assertEqual(helper.sha(self.dst/r['destination']), r['sha256'])

    def test_case_only_same_folder_uses_free_suffix(self):
        plan = helper.plan(self.src, self.src, [('IMG.jpg','img.jpg')])
        self.assertEqual(plan['files'][0]['destination'], 'img_01.jpg')
        self.assertEqual(helper.apply(plan)['files'][0]['status'], 'copied_verified')
        self.assertTrue((self.src/'IMG.jpg').exists())

    def test_paths_and_nonportable_names_rejected_without_writes(self):
        for name in ('../escape.jpg', '/tmp/escape.jpg', 'C:\\escape.jpg', 'sub/name.jpg', 'sub\\name.jpg', 'con.jpg', 'x.JPG', 'x.jpg.', 'x\x00.jpg'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                helper.plan(self.src, self.dst, [('IMG.jpg',name)])
        with self.assertRaises(ValueError): helper.plan(self.src,self.dst,[('../escape.jpg','safe.jpg')])
        self.assertEqual(list(self.dst.iterdir()), [])

    def test_plan_tampering_and_changed_source_or_destination_fail_before_writes(self):
        for change in ('escape','hash','occupied','case'):
            plan = helper.plan(self.src,self.dst,[('IMG.jpg','beach.jpg')])
            if change == 'escape': plan['files'][0]['destination'] = '../escape.jpg'
            if change == 'hash': plan['files'][0]['sha256'] = 'bad'
            if change == 'occupied': (self.dst/'beach.jpg').write_bytes(b'keep')
            if change == 'case': (self.dst/'BEACH.jpg').write_bytes(b'keep')
            before = self.snapshot(self.dst)
            with self.assertRaises(ValueError): helper.apply(plan)
            self.assertEqual(before, self.snapshot(self.dst))
            for p in self.dst.iterdir(): p.unlink()

    def test_windows_reparse_attribute_rejected_on_older_python(self):
        with patch.object(Path, "lstat", return_value=SimpleNamespace(st_mode=0o40755, st_file_attributes=0x400)):
            with self.assertRaisesRegex(ValueError, "Linked"):
                helper.folder(self.dst)

    def test_symlinks_rejected_or_reserved(self):
        try: (self.root/'linked').symlink_to(self.dst, target_is_directory=True)
        except OSError: self.skipTest('Symlinks unavailable')
        with self.assertRaises(ValueError): helper.plan(self.src,self.root/'linked',[])
        (self.src/'linked.jpg').symlink_to(self.src/'IMG.jpg')
        with self.assertRaises(ValueError): helper.plan(self.src,self.dst,[('linked.jpg','safe.jpg')])
        (self.dst/'beach.jpg').symlink_to(self.root/'missing')
        plan = helper.plan(self.src,self.dst,[('IMG.jpg','beach.jpg')])
        self.assertEqual(plan['files'][0]['destination'],'beach_01.jpg')

    def test_execution_failure_is_not_reported_as_success(self):
        plan = helper.plan(self.src,self.dst,[('IMG.jpg','beach.jpg'),('IMG2.jpg','hill.jpg')])
        original = Path.open
        def fail(path, mode='r', *a, **kw):
            if mode == 'xb': raise PermissionError('synthetic denied write')
            return original(path, mode, *a, **kw)
        with patch.object(Path,'open',fail): result = helper.apply(plan)
        self.assertEqual([r['status'] for r in result['files']], ['not_copied','not_attempted'])
        self.assertIn('denied',result['files'][0]['error'])
        self.assertEqual(list(self.dst.iterdir()),[])


    def test_source_bytes_changed_after_plan_refuses_all_writes(self):
        plan = helper.plan(self.src, self.dst, [('IMG.jpg', 'beach.jpg')])
        changed = b'changed after review'
        (self.src/'IMG.jpg').write_bytes(changed)
        with self.assertRaisesRegex(ValueError, 'source hash changed'):
            helper.apply(plan)
        self.assertEqual((self.src/'IMG.jpg').read_bytes(), changed)
        self.assertEqual(list(self.dst.iterdir()), [])

    def test_occupied_directory_reserves_name(self):
        (self.dst/'beach.jpg').mkdir()
        (self.dst/'beach.jpg'/'keep').write_bytes(b'existing child')
        plan = helper.plan(self.src, self.dst, [('IMG.jpg', 'beach.jpg')])
        self.assertEqual(plan['files'][0]['destination'], 'beach_01.jpg')
        result = helper.apply(plan)
        self.assertEqual(result['files'][0]['status'], 'copied_verified')
        self.assertEqual((self.dst/'beach.jpg'/'keep').read_bytes(), b'existing child')

    def test_destination_created_immediately_before_exclusive_open_survives(self):
        plan = helper.plan(self.src, self.dst, [('IMG.jpg', 'beach.jpg')])
        before = self.snapshot(self.src)
        original = Path.open
        def occupy(path, mode='r', *a, **kw):
            if mode == 'xb':
                with original(path, 'wb') as stream:
                    stream.write(b'newly occupied')
            return original(path, mode, *a, **kw)
        with patch.object(Path, 'open', occupy):
            result = helper.apply(plan)
        self.assertEqual(result['files'][0]['status'], 'not_copied')
        self.assertIn('error', result['files'][0])
        self.assertEqual((self.dst/'beach.jpg').read_bytes(), b'newly occupied')
        self.assertEqual(before, self.snapshot(self.src))

    def test_mid_write_failure_retains_original_and_reports_partial_copy(self):
        plan = helper.plan(self.src, self.dst, [('IMG.jpg', 'beach.jpg'), ('IMG2.jpg', 'hill.jpg')])
        before = self.snapshot(self.src)
        original = Path.open
        class PartialWriter:
            def __init__(self, stream): self.stream = stream
            def __enter__(self): return self
            def __exit__(self, *args): self.stream.close()
            def write(self, data):
                self.stream.write(data[:3])
                self.stream.flush()
                raise OSError('synthetic disk full after partial write')
        def partial(path, mode='r', *a, **kw):
            stream = original(path, mode, *a, **kw)
            return PartialWriter(stream) if mode == 'xb' else stream
        with patch.object(Path, 'open', partial):
            result = helper.apply(plan)
        self.assertEqual([r['status'] for r in result['files']], ['incomplete_copy', 'not_attempted'])
        self.assertIn('disk full', result['files'][0]['error'])
        self.assertEqual((self.dst/'beach.jpg').read_bytes(), before['IMG.jpg'][:3])
        self.assertFalse((self.dst/'hill.jpg').exists())
        self.assertEqual(before, self.snapshot(self.src))


if __name__ == '__main__': unittest.main()
