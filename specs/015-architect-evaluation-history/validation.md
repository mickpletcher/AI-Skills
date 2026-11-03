# Architect evaluation history: validation

2026-11-02, Linux cloud checkout based on ab0d902.

- Full Python suite: 166 tests, OK (7 existing environment-dependent skips).
- Focused architect evidence-index checks: 2 passed, including negative mutations for invented backend/current behavior, wrong cases/results, fixture hash and historical path drift.
- Repository validation: 46 skills, zero issues.
- Package/catalog regeneration: no shipped package or catalog changes.
- Candidate generation/drift: passed; only architect history/build-provenance and resource-manifest metadata changed.
- Offline behavioral self-test: 24 cases and 99 negative checks passed; zero actual model evaluations.
- Historical instruction paths and SHA-256 pins independently checked with git show at each cited source commit; no instruction/support bytes changed.
- git diff --check: passed.

PowerShell is unavailable locally, so its folder/quality/installer entry points were not run here; the PR CI matrix supplies those checks. No new native-host testing, installation, compatibility rollout, merge, release or promotion. Historical failures and private raw captures remain unchanged. Draft PR CI is tracked separately from these local checks.
