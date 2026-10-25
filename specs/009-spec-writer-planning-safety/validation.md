# Local validation — 2026-10-25

Base: `834091d2d2ce1b7e23557f0bd259ec5202abea66`; branch: `codex/spec-writer-planning-safety`. Remote main rechecked unchanged before commit.

- Final Python unittest discovery: 149 tests run, 147 passed, 2 skipped for Windows junction semantics. Includes five new spec-planning tests, provenance reconstruction, shared-support integrity and existing extracted-release tests.
- Generator check passed: 813 expected files match. Only spec-writer's four candidate bundles and corresponding resource-manifest entries changed.
- Repository validation: 46 skills, zero issues. Package/catalog rebuild produced no package/catalog/checksum changes.
- Existing offline evaluation self-test: 24 cases and 99 negative checks passed, zero model calls.
- PowerShell folder validator: 35 skills, zero issues; quality validator: 46 skills, zero issues. All 22 installer regressions passed in disposable temporary libraries, without active skill installation. A process-local python function selected Homebrew Python; persistent configuration unchanged.
- Diff/whitespace review passed. Older shipped Claude/Cursor sources, model-history, audit skills and shared support-file bytes remain unchanged.

The four new model scenarios remain not run. Handcrafted response mutation checks establish only deterministic fixture invariants (including collisions, preservation, reuse and traceability), not natural-language truth, model compliance or host certification. Existing native evidence remains historical and scoped; no new native acceptance is claimed. Hosted CI and Windows-only checks were not run here. No publication, promotion, release or live model transmissions occurred.
