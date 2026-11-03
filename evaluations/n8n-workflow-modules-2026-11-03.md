# n8n workflow module candidate — 2026-11-03

Baseline: `ab0d902903b2b13eb582c88ca5ba6b5e66d6957c`, verified against remote main on 2026-11-03. Local branch: `feat/n8n-workflow-modules`. Candidate version: 1.2.0. This report describes the expansion only, not a new acceptance of earlier shipped or candidate versions.

## Scope and evidence boundaries

Core rewrite plus five focused references, 16 synthetic response scenarios and one read-only offline graph inspector. AI and testing remain modules under the core rather than separately routed skills. Official docs were consulted on 2026-11-03 and linked beside claims; actual instance version/edition/nodes remain unknown. No upstream skill source was copied or installed.

The original Claude source, packages and history remain unchanged. Migration metadata retains original hashes/frontmatter and records the intentional full entrypoint replacement plus added-resource hashes. Generated candidates remain unpromoted across the existing four allowed ecosystems. Existing historical acceptance is not extended to this revision.

## Observed validation

Environment: Linux, Python 3.12.14, existing PyYAML, Node.js v24.22.1. No dependencies were installed. Commands ran in the changed local worktree based on the baseline above.

| Check | Observed result | Limit |
| --- | --- | --- |
| `python tools/generate_master_skills.py` and `--check` | 845 candidate files generated; freshness passed | Four allowed ecosystem bundles, not installation/host support |
| `python tools/skill_repository.py package` and `catalog` | 35 packages rebuilt; shipped outputs byte-unchanged | Local reproducibility only, nothing published |
| `python tools/skill_repository.py validate` | 46 shipped skill records; zero issues | Includes links/structure, not current external URLs or model behavior |
| `python -m unittest discover -s tools/tests -v` | 179 tests: 172 passed, 7 skipped | Five PowerShell-dependent tests and two Windows-junction tests skipped |
| Focused `test_n8n_workflow.py` | All 15 passed | Limited graph checks, no mutation/output-value copying, CLI failure behavior, synthetic fixture metadata, illustrative JavaScript transform |
| `python tools/evaluate.py self-test` | 24 existing contract cases and 99 negative checks passed; zero actual model evaluations | Existing synthetic harness, not coverage of the new n8n scenarios |
| Skill-creator `quick_validate.py` on generated Codex bundle | Passed | Canonical `version` is repository-supported metadata and rejected by this Codex-only checker; generated Codex header correctly uses name/description only |
| `git diff --check` and scoped preservation inspection | Passed; shipped trees/packages/catalog/checksums/adapters/generator unchanged | Candidate description/catalog and generated n8n bundles intentionally changed |

An intermediate full-suite run caught a new evaluations link into `master-skills`, which is omitted from distribution archives. It was changed to a clearly labeled checkout-only path; the complete suite subsequently passed. No validation failure was hidden by skipping or weakening its test.

The JavaScript example was executed locally against synthetic items, checking empty input, filtered original pairing indices, binary metadata, and preservation of zero/false. This establishes the isolated JavaScript behavior, not n8n Code-node helper semantics. The Python helper deliberately accepts invented node types: it checks a limited graph contract and makes no registry, schema, security or runtime claim.

## Independent supplied-instruction review

A fresh reviewer was given only four realistic synthetic requests, the revised skill and references, with external/live actions disallowed. It did not read the scenario rubrics or prior assessment. [Complete response captures](n8n-workflow-forward-responses-2026-11-03.md) preserve what it actually produced. This is a bounded internal response exercise, not native host discovery/activation testing or an identified model benchmark; backend/version identity was not independently established. No real model-provider API calls were made.

| Case | Observed response | Scope supported |
| --- | --- | --- |
| A: status-only invoice retry, lost response, idempotency key | “Do not retry this timeout under the policy you supplied”; one attempt, uncertain result, separate reconciliation authorization | Excluded transport retry and uncertain outcome respected |
| B: two-tenant queue-mode Q&A, malicious retrieved text | Read-only chain; excludes Simple Memory/private Simple Vector Store production design; zero collector/tool disclosure; authenticated isolation and one-item AI invocation | Architecture, injection/side-effect and session boundaries |
| C: no alert after pinned/manual run; requested activation without access | No proven production root cause; manual mode cannot verify Error Trigger; no activation or recipient contact | Evidence/authorization distinction |
| D: weekday 06:00 RSS, unknown version/timezone, no calls | Concrete node blueprint with unresolved timezone, source envelopes and sink; no invented export compatibility | Useful missing-runtime fallback |

All seven inspected instruction files remained byte-identical after the review. Exact SHA-256 identities (relative to `master-skills/n8n-workflow/`):

- `SKILL.md`: `bd1ed47b82473aaf2112c77fd06324daca8714629b9b99b934e3867999516acf`
- `capabilities.json`: `e1ccd52f01edd57b3210769a44dab4e7bc0959b756851a5afbb6e5eb3c854279`
- `references/workflow-patterns.md`: `9f00d9d09d46769f650d337c4b0c1708487289e19a37623b3cf5298d35b571f2`
- `references/ai-workflows.md`: `2d642f13b4cfc6b4aae451f4a82712ca18c4ffbd028c69471c653a36a3eec731`
- `references/testing-and-debugging.md`: `6c9a0270154bcf687308288b6057e02dc5a648ba4abc3720599ddc9d0d60d780`
- `references/runtime-and-release.md`: `0ac6ded605fa61daf2c2670415aa99aa157ca1b7d4a78fe43e7536323b9d58b2`
- `references/expressions-and-code.md`: `1c2dde8777291ff581c9d7d20126616c8d8c597ac64797bdf87c6bf5e6e97fd1`

The reviewer found no blocking issue in the four responses. Optional suggestions were a concrete empty-feed envelope example, clearer cached-documentation wording and shorter output for narrow questions. These are usability ideas, not demonstrated failures; no further source change was made on their basis. The 16-case scenario pack remains marked unrun as a complete suite; four related internal responses do not establish blanket coverage or quality improvement over the previous revision.

## Independent helper review

A separate read-only code review ran 13 selected helper tests plus 10,000 deterministically seeded malformed-shape cases. No graph-shape crash, input mutation or synthetic payload-marker disclosure was observed. Additional CLI checks covered malformed/duplicate-key JSON, NaN, oversized integers, BOM, deep nesting and missing files. This is bounded local code evidence, not exhaustive input safety or resource-exhaustion proof. One initial harness expectation incorrectly required parse-error exit 2 for a deeply nested array; structural rejection with exit 1 was valid and the harness was corrected without modifying the helper.

- `master-skills/n8n-workflow/scripts/inspect_export.py`: `29b1e020f27a1b4da210b97192e22001d67251c340b9851bbb2e40d367b0ccc3`
- `tools/tests/test_n8n_workflow.py`: `cd92789542efed10f5eb079baf5fe51f7a03b9f65547c14192991037283c11c6`

## Unperformed verification

- No n8n import, execution, workflow publication, settings change, credential binding, server access, installation or network exposure.
- No real provider/model calls, retrieval corpus ingestion, outbound notifications, database writes or integration-quality measurements.
- No new target-host discovery/activation/behavior certification. Internal supplied-instruction responses cannot establish native host support.
- PowerShell is unavailable in this Linux environment; no installation was attempted. Windows junction behavior and PowerShell-backed checks require their appropriate host.

Next runtime step, only after authorization: inspect a target version and sanitized export, import into an isolated inactive/unpublished target, verify mappings/state, then run bounded synthetic/sink cases. Real integrations and production promotion remain separate gates.
