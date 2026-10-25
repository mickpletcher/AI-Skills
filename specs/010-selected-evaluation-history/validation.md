# Local validation — 2026-10-25

Base/current main checked: `1fd19e26e2970b2333dba2fd4d830857b3708e58`. Branch: `codex/readme-spec-evaluation-history`.

- Final aggregate: 153 Python tests, 151 passed and two Windows-junction skips. Four new focused tests validate the existing schema (including invalid mutations), pinned public evidence paths, tested revision/hash/model bindings, generated metadata copies and private/unpinned URL rejection.
- Existing extracted-release regression initially caught two new relative metadata links into excluded master-skills. Replaced them with explicitly checkout-only paths; final aggregate passed. No external URL health claim.
- Repository validator: 46 skills, zero issues. PowerShell folder validator: 35 skills, zero issues; quality wrapper: 46 skills, zero issues.
- Generator check: all 817 files match, including four new spec-writer metadata copies. Only the two skills' metadata/provenance and resource-manifest entries changed.
- Package/catalog rebuild: no package/catalog/checksum byte changes. Existing offline self-test: 24 cases and 99 negative checks passed, zero model calls.
- Diff whitespace check and instruction/support-byte comparison passed. All SKILL.md, instructions.md and shared skill-standard.md files remain unchanged from base. No other skill history changed.

Native evaluations, hosted CI, Windows-specific checks and standalone PowerShell installer regressions were not run for this metadata-only change. Private local evidence was neither copied nor publicly linked. No new model/version inference or development attribution was made. Historical bounded results remain separate from the current untested behavior and do not grant installation or promotion approval.
