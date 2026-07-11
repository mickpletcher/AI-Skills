<!-- markdownlint-disable MD013 -->

# 003 Astrophotography Processing Phase 2 Tasks

## Research and Definition

- [x] T001 Review the existing skill, FITS audit script, repository standards, and Copilot upgrade prompt.
- [x] T002 Research the FITS Standard, Astropy FITS/HDU/checksum/WCS behavior, Siril and N.I.N.A. metadata conventions, XISF support, RAW metadata options, and dependency licenses.
- [x] T003 Define Phase 2 as a header-first FITS audit with optional XISF/RAW adapters and no pixel analysis.
- [x] T004 Define requirements, architecture, milestones, risks, acceptance signals, and authoritative references.

## Implementation Backlog

- [ ] T005 Create `scripts/audit_dataset.py` with CLI, capability detection, stable exit codes, and overwrite protection.
- [ ] T006 Implement file discovery, suffix handling, exclusions, and symlink policy.
- [ ] T007 Implement FITS HDU inventory and deterministic selected-HDU logic.
- [ ] T008 Implement optional FITS structure, checksum, and SHA-256 verification modes.
- [ ] T009 Implement the metadata alias registry, provenance records, conflict detection, and unit normalization.
- [ ] T010 Implement WCS presence/validity reporting without plate solving.
- [ ] T011 Implement frame classification with explicit evidence and confidence.
- [ ] T012 Implement deterministic frame grouping and integration summaries.
- [ ] T013 Implement group-level calibration compatibility and configurable tolerances.
- [ ] T014 Implement text and canonical JSON renderers.
- [ ] T015 Implement the CSV output bundle.
- [ ] T016 Add a compatibility wrapper or migration path for `fits_audit.py`.
- [ ] T017 Add temporary-directory unit and integration tests for all required fixtures and exit paths.
- [ ] T018 Add `references/calibration-validation.md` or merge equivalent non-duplicated guidance into the existing reference structure.
- [ ] T019 Update `SKILL.md` and README to invoke and interpret the audit.
- [ ] T020 Decide whether XISF metadata support ships in Phase 2.0 or is deferred to Phase 2.1 after license/runtime review.
- [ ] T021 Decide whether an ExifTool RAW adapter ships in Phase 2.0 or is deferred to Phase 2.1 based on target-environment availability.
- [ ] T022 Run compilation, pytest, CLI smoke tests, repository validators, and archive inspection.
- [ ] T023 Rebuild `astrophotography-processing.skill` only after all required validation passes.

## Required Verification Commands

Adapt commands to the actual implementation, but run at least:

```bash
python3 -m py_compile claude/skills/astrophotography-processing/scripts/*.py
python3 -m pytest claude/skills/astrophotography-processing/tests -q
python3 claude/skills/astrophotography-processing/scripts/audit_dataset.py --help
python3 claude/skills/astrophotography-processing/scripts/audit_dataset.py TEST_INPUT --format json
python3 claude/skills/astrophotography-processing/scripts/audit_dataset.py TEST_INPUT --format csv --output-dir TEST_OUTPUT
git diff --check -- claude/skills/astrophotography-processing specs/003-astrophotography-processing-phase-2
```

If PowerShell is available, inspect help and run the repository validators scoped as narrowly as possible. Report unrelated pre-existing findings without modifying them.

## Definition of Done

- [ ] FITS core requirements FR-1 through FR-16 are implemented and tested.
- [ ] Non-functional requirements NFR-1 through NFR-6 are demonstrated.
- [ ] The skill uses the audit as evidence and does not overstate compatibility.
- [ ] Optional adapters are either tested and documented or explicitly deferred.
- [ ] No original data is modified.
- [ ] The `.skill` package is rebuilt and verified after source validation.

<!-- markdownlint-enable MD013 -->
