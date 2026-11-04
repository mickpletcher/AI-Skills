# Validation — 2026-11-02

Base: `ab0d902903b2b13eb582c88ca5ba6b5e66d6957c`, rechecked as remote main. Isolated candidate-only branch; no unmerged PR 20 or compatibility-map changes copied.

- Nine handcrafted response scenarios and six focused tests cover mode/permission boundaries, missing read-back, preview file/embed/upload independence, chosen-name review and unauthorized rename/release claims. These are deterministic synthetic checks, not model behavior.
- Aggregate Python suite: 170 tests, 163 passed and seven skipped (five require unavailable PowerShell; two are platform-specific).
- Repository validation: 46 skills, zero issues. Generator freshness and diff whitespace checks pass.
- Package/catalog rebuild completed; shipped packages, checksums and catalog unchanged. Candidate catalog description updated for settings-only activation.
- Four generated variants include settings/preview resources; provenance remains behavior_evaluation=not_run and promotion=blocked_pending_review.
- Foundation audit initially rejected intentional master edits. Appended reversible revision evidence and extended its regression to reconstruct the exact prior master without changing historical hashes/acceptance. Initial subsequent run also identified the stale candidate catalog description, corrected before final validation.
- Independent read-only review found the settings-only activation omission; description, activation and examples corrected. Changelog byte churn and unclear capability prose corrected.
- Final independent review found no material issues and independently passed all four foundation-audit checks; prior master reconstruction is byte-exact.
- Offline evaluation self-test: 24 synthetic cases and 99 negative checks passed, zero model evaluations.
- PowerShell folder/quality/installer entry points are not run locally because pwsh is unavailable; hosted CI must establish those results for the published head.

No native model evaluation, installed-skill update, real settings mutation, purchase, merge or release occurred. Settings guidance is recommended behavior only, not an applied repository policy. No project preview was fabricated for this instruction-only change. Public visibility, root-image creation, README embed and Social preview upload remain separate action-time decisions and evidence states.

## Current-main reconciliation — 2026-11-04

Locally reconciled feature `41de8a78ea9efdd2f3742092c17f88c41a9f7f55` with main `a83cd6f1b820ebe4ae6db28938efe2d3a6249e2e`. The original validation above remains historical evidence; this section records the current combined candidate.

- Resolved six merge conflicts: retained both changelog histories, then rebuilt the generated manifest and four provenance files from current tooling. Preserved all 38 master catalog entries and 104 generated bundles, including newer n8n, synthetic-data and Food Analyzer changes.
- Refreshed compatibility maps using generate → compatibility → generate. The old bounded Codex loading evidence does not match changed instruction bytes, so current Codex compatibility is Unknown rather than a stale Yes. Historical observations remain intact.
- Updated current review metadata without modifying any of the three historical evaluation entries. Reworked the history regression to bind historical instruction hashes to committed historical evidence, independently of the current master hash. Direct reads of the two pinned historical Git objects confirmed the recorded `2b88aa12…93f08` instruction hash.
- Independent review found and verified repairs for two synthetic test gaps: authorization now binds setting name, desired value, repository and branch; preview cases now cover PNG, JPEG, GIF, existing verified files and the exact README target. Read-back comparison also preserves JSON types. Twelve synthetic cases and eight mode tests are not native behavior evaluations.
- Final aggregate Python run: 280 tests, 273 passed and seven skipped. Five skips require unavailable PowerShell; two are platform-specific. No failures or errors.
- Repository validation: 46 shipped skills, zero issues. Generator freshness, all 38 compatibility maps, diff whitespace, and the 24-case/99-negative-check offline evaluation self-test passed. Package/catalog rebuilds leave shipped sources, packages, catalog and checksums unchanged. Only Repo Architect resources differ in the generated manifest.
- Independent read-only review passed four history tests, eight mode tests, compatibility/generator freshness and whitespace; no material outstanding finding. The additional boolean read-back negative case passed after review.

Limits: no hosted CI, Windows/PowerShell checks, fresh native-model evaluation, settings mutation, installation, publication or remote merge. The historical foundation runtime artifacts were not replayed in this environment because pytest/Ruff and PowerShell are unavailable; existing runtime regressions ran in the aggregate suite. Publication and exact-head hosted CI require separate user authorization.

### Windows CI encoding correction

The first published draft head (`705639d`) passed Linux validation and the generator, installer, helper and foundation-runtime workflows, but Windows validation failed while reading UTF-8 reference Markdown with the system CP1252 default. Explicit UTF-8 decoding now covers every text read in the modes test module. A legacy-locale regression passes with the correction and independently reproduces the original UnicodeDecodeError when implicit reads are restored in memory. The repaired local aggregate run passes 281 tests with seven expected skips; all nine focused mode tests pass. Skill instructions and generated bundles are unchanged by this test-only repair. Exact-head Windows CI must still verify the correction.
