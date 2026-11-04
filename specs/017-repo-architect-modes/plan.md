# Plan

1. Add explicit mode and handoff contracts and conditional settings/preview references.
2. Add synthetic permission, mode, evidence and preview-state regressions.
3. Regenerate existing candidates and validate repository, packages, catalog and tests.
4. Review the reconciled local candidate. Publish a separate draft PR and verify exact-head CI only after separate user authorization; no merge or installation.

## Acceptance traceability

| Criterion | Validation task | Check | Expected result |
| --- | --- | --- | --- |
| AC-1 | V1 | Synthetic mode and permission mutations | Unauthorized file/settings changes rejected |
| AC-2 | V2 | Source workflow assertions and read-back negative cases | Required settings categories present; unverified claim rejected |
| AC-3 | V3 | Handoff source checks | Artifacts, checks, settings, preview and follow-ups separated |
| AC-4 | V4 | Preview resource assertions and independent-state mutations | Format/size/dimensions and no public-visibility shortcut; file is not upload evidence |
| AC-5 | V5 | Generator check and provenance/resource comparison | Four variants consistent; behavior remains not_run |
| AC-6 | V6 | Chosen-name negative mutations and metadata guidance | Review is not skipped; no silent replacement, traffic promise or release tags |
