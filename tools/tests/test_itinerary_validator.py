import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / 'master-skills/trip-email-html-itinerary/scripts/Test-ItineraryHtml.ps1'
PWSH = shutil.which('pwsh')
PAGE = '''<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width">
<style>@media(max-width:430px){{}} @media(prefers-reduced-motion:reduce){{}}
a:focus-visible{{outline:2px solid}} a{{min-height:44px}}</style></head><body>
Destination Sequence Action Items Flights Day-by-Day Itinerary Booking References
Booking Checklist Travel Admin Emergency Replacement {addresses} {links}</body></html>'''
ADDRESS = '<div class="info-card-address">{}</div>'
MAPS = '<a href="https://maps.apple.com/?q=24%20Example%20Quay">Apple</a><a href="https://www.google.com/maps/search/?api=1&amp;query=24%20Example%20Quay">Google</a>'


@unittest.skipUnless(PWSH, 'PowerShell is required for validator execution')
class ItineraryValidatorTests(unittest.TestCase):
    def run_validator(self, addresses, links=''):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'trip.html'
            path.write_text(PAGE.format(addresses=addresses, links=links), encoding='utf-8')
            return subprocess.run([PWSH, '-NoProfile', '-File', str(VALIDATOR),
                                   '-Path', str(path), '-FailOnWarnings'],
                                  capture_output=True, text=True, timeout=30)

    def test_pending_addresses_do_not_require_invented_map_links(self):
        for text in ('Address pending — verify before travel',
                     '<strong>HOTEL / STATIONS</strong> · Address pending &mdash; verify before travel. Station not identified.',
                     '<strong>ADDRESS</strong>: Address pending - verify before travel'):
            with self.subTest(address=text):
                result = self.run_validator(ADDRESS.format(text))
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn('Warnings: 0', result.stdout)

    def test_supported_addresses_still_require_both_map_services(self):
        supported = ADDRESS.format('<strong>ADDRESS</strong> · 24 Example Quay, Demo City')
        for links in ('', MAPS.split('<a href="https://www.google.com')[0]):
            with self.subTest(links=links):
                result = self.run_validator(supported, links)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn('Google Maps', result.stdout)
        self.assertEqual(self.run_validator(supported, MAPS).returncode, 0)

    def test_mixed_pending_and_supported_addresses_only_count_supported(self):
        addresses = ADDRESS.format('Address pending — verify before travel')
        addresses += ADDRESS.format('24 Example Quay, Demo City')
        self.assertEqual(self.run_validator(addresses, MAPS).returncode, 0)
        self.assertEqual(self.run_validator(addresses).returncode, 1)

    def test_later_pending_note_does_not_exempt_a_supported_address(self):
        addresses = ADDRESS.format('24 Example Quay. Pickup: Address pending — verify before travel')
        self.assertEqual(self.run_validator(addresses).returncode, 1)

    def test_absent_address_blocks_still_fail(self):
        result = self.run_validator('')
        self.assertEqual(result.returncode, 1)
        self.assertIn('No plain-text address blocks', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
