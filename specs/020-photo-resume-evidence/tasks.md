# Validation tasks

- Photo collisions, occupied suffixes, case-only requests: synthetic temp-folder helper tests.
- Photo containment, linked paths, retained hashes, truthful partial failure: synthetic temp-folder helper tests.
- Resume estimated versus rendered counts and missing renderer: focused pagination regressions.
- Candidate drift/provenance and shipped-source preservation: generation check, migration tests, repository validator, and diff inspection.
- Aggregate regressions: full tools unittest suite and offline evaluation self-test. PowerShell/Windows checks only if available; never relabel an unavailable platform as passing.
- Independent review and correction before final local commit.
