# Validation — 2026-11-03

Base: `ab0d902903b2b13eb582c88ca5ba6b5e66d6957c`. Changes are limited to three canonical review candidates, their generated allowed-target bundles, regression fixtures/tests, and change/spec documentation. Shipped source and package bytes are unchanged; no promotion is claimed.

## Sources

- [FDA added sugars](https://www.fda.gov/food/nutrition-facts-label/added-sugars-nutrition-facts-label): checked 2026-11-03; total sugars has no FDA DV, added sugars uses 50 g.
- [Alpaca fractional trading](https://docs.alpaca.markets/us/docs/fractional-trading): checked 2026-11-03; documented fractional order support conflicts with a retained legacy market-only sentence. Instructions preserve this uncertainty and require current capability checks rather than broker-runtime certification.
- [Alpaca orders](https://docs.alpaca.markets/us/docs/orders-at-alpaca): checked 2026-11-03 for sessions, order classes and replacement restrictions.

## Passed local checks

- `python -m unittest discover -s tools/tests -v`: 174 total tests: 167 passed and 7 skipped.
- `python tools/generate_master_skills.py --check`: no drift after regeneration.
- `python tools/skill_repository.py validate`: 46 skills, zero issues.
- `python tools/evaluate.py self-test`: 24 synthetic cases and 99 negative checks; zero model evaluations.
- `python tools/skill_repository.py package` and `catalog`: reproducible, no shipped/catalog/checksum diff.
- Python compilation for changed helper and tests; `git diff --check`.
- Six new preview tests encode/decode actual JPEG bytes, including forced compression through quality 40, exact byte-ceiling equality rejection, dimension preservation, impossible-size failures preserving existing destinations, CLI nonzero failure, actual output reporting and wrong-dimension readback.
- Four new nutrition/broker tests inspect actual instructions and check four supplied-label arithmetic fixtures plus sixteen partial fractional-contract cases. These test-only oracles do not execute skills or validate broker responses.
- Independent reviewer additionally ran the unmocked preview CLI with synthetic metadata: JPEG 1280x640, 47,289 bytes, reported size and dimensions matched decoded output. Temporary artifact removed.

An intermediate aggregate run before candidate regeneration/provenance updates failed the expected stale-generated and migration-reconstruction checks (one error, three failures). These were resolved by recording exact transformations/override hashes and regenerating; final aggregate passed as above.

## Independent review

A separate read-only reviewer found no blocking issues after inspecting all three source diffs, provenance and generated boundaries. The reviewer independently reran the generator drift check, ten focused regressions and whitespace checks, and confirmed no shipped-tree/catalog/checksum diff.

## Limits and publication

Five PowerShell-dependent itinerary checks and two Windows-junction checks skipped in this Linux environment. PowerShell folder/quality/installer entry points were not run because `pwsh` is unavailable; no installation was attempted. Existing Pillow 13.0.0 and PyYAML 6.0.3 were used. No live model tests, native-host tests, broker calls, actual trades, personal nutrition/medical testing, CI runs, merge, release, settings changes or promotion occurred. Existing bounded acceptance records are not extended by these tests.

Publication is pending separate explicit authorization; this local implementation does not claim a push or PR. No attempt was made to bypass the earlier publication denial. The compatibility branch remains separate and untouched.
