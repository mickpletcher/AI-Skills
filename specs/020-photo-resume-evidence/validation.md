# Validation — 2026-11-03

Local Linux/Python 3.12.14; Poppler pdfinfo/pdftoppm 26.05.0. Synthetic fixtures only.

## Passed

- Full `python -m unittest discover -s tools/tests -v`: 181 tests, 174 passed, 7 skipped (platform-specific tests). Includes 11 Photo Copy tests and 6 Resume pagination tests.
- `python tools/generate_master_skills.py --check`: reproducible candidates. Only these two skills' allowed Claude/ChatGPT bundles changed, plus the resource manifest.
- `python tools/skill_repository.py validate`: 46 skills, zero issues.
- `python tools/evaluate.py self-test`: 24 synthetic contract cases, 99 negative checks, zero model evaluations.
- `git diff --check`; shipped platform-source/package/catalog trees unchanged.
- Independent review found an older-Python Windows junction-detection gap; corrected using Windows reparse attributes and a mocked regression. Reviewer verified correction, added four operation tests, independently ran 11 Photo Copy + 6 Resume tests, and reported no remaining blocking findings within the stated scope.

Photo fixtures cover occupied destination files/directories, numbered suffixes, case-only conflicts, path traversal/absolute paths, linked folders/sources, changed source bytes, stale/tampered plans, retained hashes, exclusive-create refusal after a destination appears, and truthful partial failure/not-attempted reporting. Prior prompt-supplied preservation tests passed; no historical overwrite failure is claimed.

Resume fixtures include actual rendering/counting of font-independent synthetic vector PDFs with 1, 2, and 3 pages, unchanged source hashes, missing tools, invalid inputs, warnings, timeout, page-count mismatch, and evidence/JSON compatibility assertions. Existing scoring regressions remain passing. These tests establish pagination mechanics, not resume visual quality or native model obedience.

The first aggregate run exposed a Photo migration transformation with an empty insertion anchor; fixed it to an explicit unique text anchor and regenerated. The final full suite passes; the failed intermediate run is not represented as passing.

## Exact limitations / not run

- Action: font-bearing PDF rendering. Target: local Poppler/Fontconfig cache `/workspace/var/cache/fontconfig`. Reason: renderer emitted `Fontconfig error: No writable cache directories`. Status: not certified; helper retained unverified result. No cache permission change, bypass or repeat of the failed write. Font-independent fixtures separately passed.
- Action: actual DOCX render/export. Target: local LibreOffice renderer. Reason: executable absent. Status: not run; no install attempted. Intended-font fidelity and visual resume inspection remain unverified.
- Action: PowerShell validators/installer tests and native Windows junction semantics. Target: local Linux executor. Reason: PowerShell executable unavailable; no Windows executor. Status: not run locally (Windows reparse logic has a mocked regression, not native certification).
- Native/paid model calls, personal photos/resumes, installations, promotion, publication, merge and live changes: not performed or claimed. The optional photo helper copies with approval and preserves originals; it does not implement in-place renames or protect against hostile concurrent directory replacement.
