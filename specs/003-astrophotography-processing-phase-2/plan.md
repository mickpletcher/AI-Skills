<!-- markdownlint-disable MD013 -->

# 003 Astrophotography Processing Phase 2 Plan

## Objective

Deliver a tested, read-only `audit_dataset.py` capability and integrate it into the Claude skill without implementing pixel-level diagnostics or image processing.

## Assumptions

1. Phase 1 metadata/routing work should be complete before final Phase 2 skill integration, but the Phase 2 script can be developed independently.
2. Astropy is the only required non-standard runtime dependency.
3. XISF and camera RAW adapters are optional and may be deferred without blocking the FITS core.
4. Existing dirty-worktree changes belong to the user and must be preserved.

## Milestone 1: CLI Skeleton and Data Contracts

### Work

- define exit codes and CLI arguments;
- define report, file, group, and finding data structures;
- define canonical JSON schema version `1.0`;
- implement output overwrite protection;
- add `--help` and capability-reporting behavior.

### Validation

- CLI parser tests;
- deterministic serialization tests;
- overwrite and exit-code tests.

## Milestone 2: FITS Discovery and Reading

### Work

- implement supported suffix recognition and exclusions;
- implement symlink policy;
- open FITS read-only with lazy/memory-mapped behavior where available;
- inventory HDUs and deterministically select an image HDU;
- capture malformed-file errors without aborting the run;
- implement optional FITS/checksum verification.

### Validation

- primary, `SCI` extension, multi-extension, compressed, cube, malformed, and checksum fixtures.

## Milestone 3: Metadata Normalization

### Work

- implement alias registry;
- normalize values and units;
- retain provenance and conflicts;
- detect WCS presence/validity;
- classify frame types with evidence and confidence.

### Validation

- alias, conflict, unit, WCS, and classification tests.

## Milestone 4: Grouping and Compatibility

### Work

- derive sessions;
- build frame-type-specific deterministic group keys;
- summarize integration time;
- compare light/flat groups with candidate calibration groups;
- produce compatible, tolerance, mismatch, missing, and unknown findings.

### Validation

- group determinism and compatibility decision-table tests;
- missing metadata never becomes a hard mismatch or confirmed match.

## Milestone 5: Renderers

### Work

- render concise text;
- write canonical JSON;
- write the multi-file CSV bundle;
- keep machine-readable stdout clean;
- record effective options and capabilities.

### Validation

- JSON schema-content tests;
- CSV header/row tests;
- stdout/stderr separation tests.

## Milestone 6: Skill Integration

### Work

- update `SKILL.md` to use the new audit before recommending processing;
- add or update `references/calibration-validation.md` with interpretation rules;
- convert `fits_audit.py` to a wrapper or remove it only after caller search;
- declare dependencies without auto-installation;
- update the source README with a minimal audit example.

### Validation

- all referenced paths resolve;
- legacy invocation behavior is accounted for;
- repository skill validators are run without repairing unrelated findings.

## Milestone 7: Package Verification

### Work

- run Python compilation and pytest;
- exercise the CLI on a synthetic mixed dataset;
- rebuild the `.skill` archive only after validation;
- confirm archive content and exclusion rules.

### Validation

- source and package contain the intended runtime files;
- no cache, test output, local planning file, or `.DS_Store` is packaged;
- archive opens as ZIP and contains `SKILL.md` at the expected root.

## Deferred Work

- XISF adapter implementation if GPL/runtime distribution questions remain unresolved;
- camera RAW metadata adapter if ExifTool is unavailable in target environments;
- pixel statistics, histograms, and previews;
- subframe image-quality scoring;
- file organization or movement;
- parallel scanning until sequential correctness and cloud-volume behavior are proven.

## Rollback

The implementation must remain additive until integration tests pass. Roll back by restoring the old `SKILL.md` references, removing new audit files/tests, and retaining the existing `fits_audit.py`. Never alter user astronomical data during development or rollback.

<!-- markdownlint-enable MD013 -->
