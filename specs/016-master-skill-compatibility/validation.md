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

## Approved table-format revision — 2026-11-03

All 36 maps now show the same twelve ecosystem rows with separate compatibility and implementation enums. The first seven are existing repository target IDs; the five additional rows distinguish Microsoft products and reserved guides without creating target approval. A Yes is limited to its immediately documented historical scope and matching current instruction hash: 15 ChatGPT bounded packet cases with explicit host metadata and a matching passing case and ten Codex loading observations. All other rows remain Unknown; skipped placement is not a demonstrated incompatibility. No No ratings or speculative per-master plans are invented.

Eleven focused regressions check complete rows, enum values, implementation-vs-compatibility separation, missing/mismatched/unaccepted evidence and existing map integrity. Full suite: 175 tests, 168 passed and seven platform/runtime skips. Repository validation remains 46 skills, zero issues; map/candidate freshness and 24/99 offline contracts pass. No new model testing occurred. This revision updates the existing branch only; the prior draft PR denial remains respected.

An independent read-only review traced all fifteen affirmative ChatGPT ratings to actual skill-specific passing native cases. Matching-hash preparation or offline fixture content alone cannot grant Yes; regressions cover absent host metadata and not-submitted outcomes. Codex Yes remains loading-only.

## Combined integration validation — 2026-11-03

Reconciled PRs #20, #22, #23 and #24 before this compatibility rollout. The original 36-master/96-copy counts above describe the earlier standalone review; combined coverage is 38 master maps and 104 generated copies. Both new masters have twelve Unknown compatibility ratings and no inherited acceptance. The no-indexed-evidence path now explicitly disclaims whole-skill or cross-ecosystem certification and has a focused regression.

- Combined Python suite: 269 tests, passing with seven existing platform-dependent skips.
- Compatibility tests under simulated Windows cp1252 defaults: 12 passing.
- Repository structural validation: 46 shipped skills, zero issues.
- Map and candidate freshness, package/catalog regeneration, preserved shipped trees and whitespace checks: passed.
- Offline contracts: 24 cases, 99 negative checks; zero actual model evaluations.
- Hosted CI and merge results are tracked on the exact remote PR heads, separately from this local record. No new native-host, live-service or compatibility evidence is asserted.

Late #20/#22 review repairs are retained: exact Architect report-row manifest binding and bounded Poppler failure diagnostics, with focused negative regressions.
