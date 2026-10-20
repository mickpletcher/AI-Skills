import csv
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

try:
    import yaml
except ImportError:
    yaml = None
from PIL import Image
try:
    from astropy.io import fits
except ImportError:
    fits = None

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / 'master-skills'
PWSH = shutil.which('pwsh')


class RemainingHelperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def run_python(self, skill, helper, *args):
        return subprocess.run([sys.executable, str(MASTER / skill / 'scripts' / helper), *map(str, args)],
                              capture_output=True, text=True, encoding='utf-8', timeout=60)

    def run_ps(self, content):
        wrapper = self.root / 'wrapper.ps1'
        wrapper.write_text(content, encoding='utf-8')
        return subprocess.run([PWSH, '-NoProfile', '-File', str(wrapper)], capture_output=True,
                              text=True, encoding='utf-8', timeout=90)

    def test_image_readonly_metadata_and_missing_input(self):
        image = self.root / 'sample.png'
        Image.new('RGB', (30, 20), (20, 40, 60)).save(image)
        before = image.read_bytes()
        result = self.run_python('astrophotography-processing', 'image_stats_preview.py', self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('size=30x20', result.stdout)
        self.assertIn('mean=40.00', result.stdout)
        self.assertEqual(image.read_bytes(), before)
        self.assertEqual({p.name for p in self.root.iterdir()}, {'sample.png'})
        self.assertEqual(self.run_python('astrophotography-processing', 'image_stats_preview.py', self.root / 'missing').returncode, 2)

    def test_preview_collisions_repeat_and_source_preservation(self):
        for folder, color in [('one', 'red'), ('two', 'blue')]:
            (self.root / folder).mkdir()
            Image.new('RGB', (30, 20), color).save(self.root / folder / 'same.png')
        command = [self.root, '--write-preview', '--preview-max-size', '10']
        before = {p: p.read_bytes() for p in self.root.rglob('*.png')}
        result = self.run_python('astrophotography-processing', 'image_stats_preview.py', *command)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        previews = list((self.root / 'process').rglob('*.png'))
        self.assertEqual(len(previews), 2)
        for path in previews:
            with Image.open(path) as image:
                self.assertEqual(image.size, (10, 7))
        snapshot = {p: p.read_bytes() for p in self.root.rglob('*.png')}
        self.assertEqual(self.run_python('astrophotography-processing', 'image_stats_preview.py', *command).returncode, 1)
        self.assertEqual({p: p.read_bytes() for p in self.root.rglob('*.png')}, snapshot)
        self.assertTrue(all(p.read_bytes() == data for p, data in before.items()))

    def test_bad_images_invalid_size_and_outward_preview_directory(self):
        (self.root / 'bad.png').write_bytes(b'not an image')
        self.assertEqual(self.run_python('astrophotography-processing', 'image_stats_preview.py', self.root).returncode, 1)
        self.assertEqual(self.run_python('astrophotography-processing', 'image_stats_preview.py', self.root, '--write-preview', '--preview-max-size', '0').returncode, 2)
        outside = self.root / 'outside'
        outside.mkdir()
        inputs = self.root / 'inputs'
        inputs.mkdir()
        Image.new('RGB', (20, 20)).save(inputs / 'good.png')
        link = inputs / 'process'
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError:
            result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(outside)], capture_output=True)
            self.assertEqual(result.returncode, 0)
        self.assertEqual(self.run_python('astrophotography-processing', 'image_stats_preview.py', inputs, '--write-preview').returncode, 2)
        self.assertFalse(list(outside.iterdir()))

    @unittest.skipIf(fits is None, 'Astropy is unavailable; real FITS runtime remains unverified')
    def test_fits_real_headers_compression_errors_and_preservation(self):
        import numpy as np
        hdu = fits.PrimaryHDU(np.zeros((3, 4), dtype=np.uint16))
        hdu.header['EXPOSURE'] = 2.5
        hdu.header['INSFLNAM'] = 'L'
        hdu.header['OBJECT'] = 'Synthetic target'
        hdu.writeto(self.root / 'sample.fits.gz')
        path = self.root / 'sample.fits.gz'
        before = path.read_bytes()
        result = self.run_python('astrophotography-processing', 'fits_audit.py', self.root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('3x4\t2.5\tL', result.stdout)
        self.assertIn('Synthetic target', result.stdout)
        self.assertEqual(path.read_bytes(), before)
        (self.root / 'bad.fits').write_bytes(b'not FITS')
        self.assertEqual(self.run_python('astrophotography-processing', 'fits_audit.py', self.root).returncode, 1)
        self.assertEqual(self.run_python('astrophotography-processing', 'fits_audit.py', self.root / 'missing').returncode, 2)

    def test_apple_notes_platform_guard_and_mocked_handoff_cleanup(self):
        path = MASTER / 'idea-forge/scripts/save_to_apple_notes.py'
        spec = importlib.util.spec_from_file_location('notes_helper', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        body = self.root / 'body.txt'
        body.write_text('Synthetic <analysis> & details', encoding='utf-8')
        args = [str(path), '--folder', 'Synthetic', '--title', 'Résumé', '--body-file', str(body)]
        if sys.platform != 'darwin':
            with patch.object(sys, 'argv', args):
                self.assertEqual(module.main(), 1)
        script_paths = []

        def handoff(command, **kwargs):
            script_paths.append(Path(command[1]))
            self.assertTrue(script_paths[-1].exists())
            self.assertEqual(command[0], 'osascript')
            self.assertEqual(command[2:5], ['Synthetic', 'Résumé', str(body.resolve())])
            return subprocess.CompletedProcess(command, 0, stdout='', stderr='')

        with patch.object(sys, 'argv', args), patch.object(sys, 'platform', 'darwin'), patch.object(module.subprocess, 'run', side_effect=handoff):
            self.assertEqual(module.main(), 0)
        self.assertFalse(script_paths[0].exists())
        self.assertEqual(body.read_text(encoding='utf-8'), 'Synthetic <analysis> & details')
        def failure(command, **kwargs):
            script_paths.append(Path(command[1]))
            raise subprocess.CalledProcessError(3, command, stderr='Synthetic handoff failure')
        with patch.object(sys, 'argv', args), patch.object(sys, 'platform', 'darwin'), patch.object(module.subprocess, 'run', side_effect=failure):
            self.assertEqual(module.main(), 3)
        self.assertFalse(script_paths[-1].exists())

    @unittest.skipIf(yaml is None, 'PyYAML unavailable; YAML round-trip remains unverified locally')
    def test_resume_refresh_yaml_and_existing_candidate_preservation(self):
        tips = self.root / 'tips'
        tips.mkdir()
        sources = [{'name': 'Synthetic Coach', 'platform': 'Example', 'discoveryUrl': 'https://example.invalid', 'focus': ['clarity'], 'notes': 'Synthetic', 'active': True}]
        (tips / 'sources.json').write_text(json.dumps(sources))
        fields = ['source_name', 'source_type', 'title', 'published_at', 'url', 'topics', 'confidence', 'summary', 'tip_1', 'tip_2']
        row = dict.fromkeys(fields, '')
        row.update(source_name='Synthetic: Coach', source_type='post', title='Resume: Example', published_at='2026-10-19', url='https://example.invalid', topics='clarity;examples', confidence='high', summary='Synthetic', tip_1='Use facts', tip_2='Keep scope')
        csv_path = self.root / 'input.csv'
        with csv_path.open('w', newline='', encoding='utf-8') as output:
            writer = csv.DictWriter(output, fieldnames=fields)
            writer.writeheader()
            writer.writerow(row)
        helper = MASTER / 'resume-writer/scripts/Invoke-ResumeTipsRefresh.ps1'
        command = f"& '{helper.as_posix()}' -SkillRoot '{self.root.as_posix()}' -ReviewDate '2026-10-19' -SubmissionCsvPath '{csv_path.as_posix()}'"
        result = self.run_ps(command)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        note = next((tips / 'inbox').glob('*.md'))
        header = yaml.safe_load(note.read_text(encoding='utf-8').split('---', 2)[1])
        self.assertEqual(header['source_name'], 'Synthetic: Coach')
        self.assertEqual(header['topics'], ['clarity', 'examples'])
        before = note.read_bytes()
        self.assertEqual(self.run_ps(command).returncode, 0)
        self.assertEqual(note.read_bytes(), before)
        self.assertEqual(json.loads((tips / 'sources.json').read_text()), sources)

    def test_scheduler_mocked_creation_whatif_and_existing_refusal(self):
        skill = MASTER / 'resume-writer'
        helper = skill / 'scripts/Register-ResumeTipsRefreshTask.ps1'
        common = '''$ErrorActionPreference='Stop'
$global:registered=0
function New-ScheduledTaskAction { [pscustomobject]@{Kind='Action'} }
function New-ScheduledTaskTrigger { [pscustomobject]@{Kind='Trigger'} }
function New-ScheduledTaskSettingsSet { [pscustomobject]@{Kind='Settings'} }
function Register-ScheduledTask { $global:registered++; if ($args -contains '-Force') { throw 'Force is forbidden in this test' } }
'''
        for existing, whatif, expected in [(False, '', 1), (False, '-WhatIf', 0), (True, '', 0)]:
            with self.subTest(existing=existing, whatif=whatif):
                query = "[pscustomobject]@{TaskName='Synthetic'}" if existing else '$null'
                call = f"& '{helper.as_posix()}' -SkillRoot '{skill.as_posix()}' -TaskName 'Synthetic' {whatif}"
                caught = '$global:failure=$_.Exception.Message' if existing else 'throw'
                content = common + f'function Get-ScheduledTask {{ {query} }}\ntry {{ {call} | Out-Null }} catch {{ {caught} }}\n'
                content += f"if ($global:registered -ne {expected}) {{ throw 'Unexpected mutation count' }}\n"
                if existing:
                    content += "if ($global:failure -notlike '*already exists*') { throw 'Existing task was not refused' }\n"
                result = self.run_ps(content)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_public_demo_builder_and_exporter_with_browser_stubs(self):
        skill = self.root / 'itinerary'
        shutil.copytree(MASTER / 'trip-email-html-itinerary', skill)
        exporter = skill / 'scripts/Export-PublicDemoJpegs.ps1'
        real_exporter = exporter.read_text(encoding='utf-8')
        exporter.write_text("param($HtmlPath,$OutputDirectory,$BrowserChannel)\n& (Join-Path $PSScriptRoot 'Test-ItineraryHtml.ps1') -Path $HtmlPath -PublicDemo -FailOnWarnings\n", encoding='utf-8')
        output = self.root / 'output'
        builder = skill / 'scripts/New-PublicDemoItinerary.ps1'
        result = self.run_ps(f"& '{builder.as_posix()}' -OutputDirectory '{output.as_posix()}' -KeepHtml")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        html_path = output / 'public-demo-render-source.html'
        html = html_path.read_text(encoding='utf-8')
        self.assertIn('PUBLIC DEMO', html)
        self.assertNotIn('{{', html)
        result = self.run_ps(f"& '{builder.as_posix()}' -OutputDirectory '{output.as_posix()}' -KeepHtml")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(html_path.read_text(encoding='utf-8'), html)
        exporter.write_text(real_exporter, encoding='utf-8')
        jpeg = self.root / 'synthetic.jpg'
        Image.effect_noise((1080, 1350), 100).convert('RGB').save(jpeg, quality=85)
        slides = self.root / 'slides'
        content = f'''$ErrorActionPreference='Stop'
$global:calls=0
function Get-Command {{ param($Name) if ($Name -eq 'pwsh') {{ [pscustomobject]@{{Source='Invoke-FakeValidator'}} }} elseif ($Name -eq 'npx.cmd') {{ [pscustomobject]@{{Source='Invoke-FakeBrowser'}} }} else {{ throw 'Unexpected tool' }} }}
function Invoke-FakeValidator {{ $global:LASTEXITCODE=0 }}
function Invoke-FakeBrowser {{ $global:calls++; Copy-Item -LiteralPath '{jpeg.as_posix()}' -Destination $args[-1]; $global:LASTEXITCODE=0 }}
& '{exporter.as_posix()}' -HtmlPath '{html_path.as_posix()}' -OutputDirectory '{slides.as_posix()}' | Out-Null
if ($global:calls -ne 10) {{ throw 'Expected ten stub calls' }}
'''
        result = self.run_ps(content)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(len(list(slides.glob('*.jpg'))), 10)
        self.assertEqual(html_path.read_text(encoding='utf-8'), html)
        failed_validation = content.replace('$global:LASTEXITCODE=0 }', '$global:LASTEXITCODE=1 }', 1)
        result = self.run_ps(failed_validation)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Public demo validation failed', result.stderr)
        snapshot = {p: p.read_bytes() for p in slides.glob('*.jpg')}
        result = self.run_ps(content)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Output already exists', result.stderr)
        self.assertTrue(all(p.read_bytes() == value for p, value in snapshot.items()))
        jpeg.write_bytes(b'not a JPEG')
        result = self.run_ps(content.replace(slides.as_posix(), (self.root / 'invalid-slides').as_posix()))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Invalid JPEG output', result.stderr)


if __name__ == '__main__':
    print(json.dumps({'python': sys.version.split()[0], 'astropy': __import__('astropy').__version__ if fits is not None else None, 'Pillow': __import__('PIL').__version__, 'yaml': yaml.__version__ if yaml is not None else None, 'native_browser_or_scheduler_used': False}), flush=True)
    unittest.main(verbosity=2)
