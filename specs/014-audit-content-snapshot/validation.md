# Local validation — 2026-10-26

Baseline: `76888358cfcd0d7a508c9d89cf30ecce81a56c5e`; branch: `codex/audit-content-snapshot`. Remote main rechecked unchanged before publication.

- Eleven focused tests passed, including prior audit safeguards and three new content-snapshot checks.
- Full Python 3.11 suite: 164 tests, 162 passed and two platform-specific skips.
- Repository validator: 46 skills, zero issues; folder validator: 35 skills, zero issues; quality validator: 46 skills, zero issues.
- Package/catalog rebuild and generator freshness passed. Packages, catalog, checksums and generated candidates unchanged.
- Offline contracts: 24 cases and 99 negative checks passed, zero model evaluations.
- PowerShell installer regressions: all 22 passed in temporary libraries; expected recovery-path diagnostics belong to passing failure cases.
- Diff whitespace check passed. Byte comparison confirmed existing instruction text unchanged outside the new clauses; historical fixtures/evidence unchanged.

The new fixture deliberately has identical revision/status but different contents for both a modified manifest and untracked notes. Deterministic SHA-256 comparison detects exactly those two edits, leaving the artifact unchanged; the manifest now includes that artifact. Contract checks require unavailable-comparison/provisional guidance. These are static checks and synthetic expected behavior, not observed native Cursor/Copilot results. No new model run or active installation occurred. Hosted checks are reported on the draft PR; no merge, promotion or release is authorized.
