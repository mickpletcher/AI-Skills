import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from readme_delivery import readme_body, validate_readme


class ReadmeDeliveryTests(unittest.TestCase):
    def test_rejects_retained_failure_shape(self):
        with self.assertRaisesRegex(ValueError, 'final README heading'):
            validate_readme('# PebbleAudit\n## License\nBSD 3-Clause.\n### Changes and validation notes\nNot executed.\n')

    def test_unlabeled_fence_preserves_the_native_leading_blank_line(self):
        body = '\n# PebbleAudit\n## Usage\n```bash\npebble-audit --help\n```\n## License\nBSD 3-Clause.\n'
        self.assertEqual(readme_body('````\n' + body + '````\nReview notes (not part of README)\nDraft.'), body)

    def test_extracts_nested_examples_without_review_notes(self):
        body = '# PebbleAudit\n## Usage\n```powershell\n# Example heading\npebble-audit --help\n```\n## License\nBSD 3-Clause.\n'
        response = '````markdown\n' + body + '````\nReview notes (not part of README)\nDraft; not executed.\n'
        self.assertEqual(readme_body(response), body)

    def test_rejects_unbounded_or_unlabeled_delivery(self):
        for response in ('# Repo\n## License\nBSD.', '```markdown\n# Repo\n## License\nBSD.',
                         '```markdown\n# Repo\n## License\nBSD.\n```\nChanges and validation notes: not executed.'):
            with self.subTest(response=response), self.assertRaises(ValueError):
                readme_body(response)

    def test_rejects_premature_outer_fence_and_multiple_artifacts(self):
        for response in ('```markdown\n# Repo\n## Usage\n```\ncommand\n```\n## License\nBSD.\n```',
                         '```markdown\n# Repo\n## License\nBSD.\n```\n```md\n# Second\n```'):
            with self.subTest(response=response), self.assertRaises(ValueError):
                readme_body(response)

    def test_rejects_unclosed_example_and_post_license_heading(self):
        for body in ('# Repo\n## License\nBSD.\n```python\nprint(1)',
                     '# Repo\n## License\nBSD.\n## Review\nDone.'):
            with self.subTest(body=body), self.assertRaises(ValueError):
                validate_readme(body)
