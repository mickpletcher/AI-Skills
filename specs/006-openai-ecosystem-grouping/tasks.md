# Tasks

- [x] Inventory current layout, consumers and release boundaries.
- [x] Relocate OpenAI source/candidate trees and preserve file bytes and local planning.
- [x] Update generator, ownership validation, catalog, release paths and navigation.
- [x] Add nested-path regression coverage and regenerate without promotion.
- [x] Run local validation and deliver through draft PR #11. Record latest hosted results in the PR description; keep it unmerged and preserve promotion gates.

## Validation

- All 74 Python regressions passed on Windows/Python 3.12 in a clean Git-byte snapshot, including nested OpenAI discovery, distinct adapters, named-model builds, manifest rejection, links/junctions and release boundaries.
- Repository and PowerShell quality checked 46 shipped skills with zero issues; exact-case checks covered 35 Claude folders with zero issues. All 22 installer regressions passed in temporary libraries.
- Generator drift, all 35 existing package byte checks, and the 24-case/99-negative-check offline evaluator passed. No model calls, installation or promotion occurred.
- All 416 relocated files matched their pre-move hashes before explicit edits. Final audit confirms 367 unchanged files, 48 updated moved provenance records and one README path edit. Candidate counts, package checksums, catalog IDs and suitability decisions are unchanged.
- Added the OpenAI guide to the release inputs while retaining the Codex scaffold/candidate exclusions. Reviewed the portable ZIP fixture change and updated its fixed cross-platform SHA256 to `234f237ad9f697a4774c379555e450a5875eb57b95cb1ff02b7e0b5117c811a9`; content, ordering and encoding assertions remain enforced. The initial expected-hash failure was corrected before the passing full run.
- Historical behavioral captures and source pins are unchanged. Hosted validation results are recorded against their exact commit on PR #11, separately from these local checks.
