# Local validation — 2026-10-25

Base: `5d5f168abae2c26fc2d7a63a56c83919d74a5a14`; branch: `codex/first-quality-improvements`. Remote main rechecked unchanged before commit.

- Python 3.11 unittest discovery: 144 tests run, 142 passed and 2 skipped (Windows junction semantics in migration and release tests). Includes four new quality regressions and existing extracted-release validation.
- Repository validation: 46 skills, zero issues.
- Generator check: passed; all 813 expected files match. Changes limited to the four github-readme candidates and their provenance/resource hashes.
- Package/catalog rebuild: successful; no package, catalog or checksum byte changes.
- Existing offline contract self-test: 24 cases, 99 negative checks passed, zero model evaluations.
- PowerShell folder validator: 35 skills, zero issues; quality entry point: 46 skills, zero issues.
- PowerShell installer regressions: all 22 passed in temporary libraries, no active skill installation. A process-local python function selected the available Homebrew Python; persistent configuration unchanged. Expected failure-path diagnostics belong to passing rollback tests.
- Diff whitespace check passed; inspected source, generated provenance and resource-manifest changes. Spec-writer, model-history, other candidates and existing acceptance evidence unchanged.

The four synthetic cases in `evaluations/fixtures/first-quality-improvements.json` remain behaviorally not run. Deterministic checks exercise the checkout/archive link failure, fixture evidence and instruction propagation; they do not establish model compliance, external URL availability, new host certification or promotion. No new model sessions, paid API calls, publication or release occurred. Windows-specific tests and hosted CI were not run locally.
