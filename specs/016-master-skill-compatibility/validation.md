# Validation — 2026-11-02

Base `ab0d902903b2b13eb582c88ca5ba6b5e66d6957c`; isolated compatibility branch. Earlier unpublished local artifacts were lost during environment recycling; these maps and checks were reconstructed from the unchanged repository declarations and evidence, not recovered byte-identical artifacts.

- All 36 master maps and 96 generated copies are present.
- Seven focused regressions pass; full Python suite: 171 tests, 164 passed, seven skipped (five require unavailable PowerShell and two Windows junction semantics).
- Map freshness and candidate generation freshness pass; repository validator checks 46 skills with zero issues.
- Package/catalog rebuild leaves shipped packages, catalogs and checksums unchanged.
- Offline contract fixtures: 24 cases, 99 negative checks, zero actual model evaluations.
- Whitespace diff check passes. Existing instruction, capability/placement and historical evidence bytes are unchanged.

No native app tests, installations, model calls, promotion, merge or release occurred. PowerShell folder/quality/installer scripts were not run locally because PowerShell is unavailable. Hosted checks are separate evidence. New resources necessarily update generated provenance and the resource manifest.

Other Architect work is independent. Preserve both changelog entries and regenerate maps/candidates when combining capability changes; do not blindly select one manifest/provenance side.
