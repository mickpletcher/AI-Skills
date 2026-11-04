# n8n security reviewer: bounded embedded JSON

Date: 2026-11-04. Base: `53b82454e5462e151798672978593e1080e1f84a`. Candidate version 0.2.0, helper output schema 2. Canonical repository-only source: `master-skills/n8n-security-reviewer/scripts/review_export.py`. These are offline implementation checks, not native host/model acceptance, live n8n compatibility, installation or promotion.

## Change

- Parse one strict JSON layer in the two allowlisted HTTP header/body fields. Preserve fixed, value-free locations, conditional findings and runtime uncertainty.
- Keep expressions unevaluated. Separate `coverage` unknowns from secret candidates, with explicit partial status, resource consumption and truncation metadata.
- Bound each field and the whole review; separate finding and coverage caps prevent warnings from consuming finding capacity. Retain raw-marker checks and document overlapping marker counts.
- Use low priority for generic body-name heuristics and medium for decoded header/signature observations. References, placeholders and expressions are not automatically classified as embedded credentials.
- Document the schema-v2 consumer migration, deliberate limits and no-security-pass boundary. Regenerate four candidate bundles; preserve shipped skills and Unknown compatibility status.

## Verification

- All 30 new public-contract regressions passed, alongside the existing 17 focused helper tests. Coverage includes strict/invalid JSON, escaped keys/values, lone-surrogate rejection, valid surrogate pairs, conditional priorities, placeholders and benign references, unknown expressions, literal siblings, custom-node and one-layer scope, shared budgets, output caps, redaction, nonmutation, no execution/network/writes, and CLI provenance.
- Final aggregate suite: **312 tests, 305 passed, seven skipped**, no failures/errors. Five skips need unavailable PowerShell; two require Windows junction semantics. Those checks are not claimed passed.
- Repository validation: 46 shipped skills, zero issues. Generator freshness, all 38 compatibility maps, and whitespace checks passed. Offline evaluation self-test: 24 synthetic contracts and 99 negative checks passed, zero model evaluations.
- All four generated helper/contract/README copies match canonical resources. Only n8n-security-reviewer entries changed in the generated resource manifest; unrelated generated and shipped skills remain unchanged.
- An additional deterministically seeded 3,000-case mutation run against the implemented helper found no exceptions, tested-canary disclosure or input mutation. Instrumentation blocked dynamic compilation/execution, network, subprocess and filesystem events during review; none occurred. This is bounded generated coverage, not exhaustive fuzzing or a hardened sandbox.

## Independent review and repairs

Independent tests identified decoded unpaired surrogate keys/values that were not marked unsupported. The helper now checks decoded string/key UTF-8 validity and returns value-free `unsupported_unicode` coverage; paired-surrogate controls pass.

Independent read-only diff review found no blocking correctness, redaction, resource-boundary or scope defect. It independently exercised actual default 100-record/128-attempt boundaries, exact field-size limits, oversized integers, deep nesting and escaped expressions. Its optional recommendation for permanent real-default cap coverage was added; the final aggregate run includes that regression. The helper bytes did not change after this review.

The initial original-test run occurred before generation and failed only generated-resource equality. Regenerating candidates resolved that expected staging mismatch. No assertions were weakened to claim native/runtime behavior.

Reviewed helper SHA-256: `1e01d3eeb03cc224bb98ac81e4ac524ffaa20cf4bac4bf0a8842076e8a43b2f9`. Final new test SHA-256: `9f5c96cab0789dae01d8ca7602dc3eef2e44bb3b9656b84c505fa7d502896313`.

## Limits

No real credentials, production workflows, workflow execution, endpoint calls, installations, settings changes, remote publication or merge occurred. Native host activation, real n8n import/runtime semantics, downstream schema-v2 consumers and hosted Windows/PowerShell CI remain unverified. A completed scan with no candidates is not a security pass; partial coverage and truncation must remain visible to consumers. Previous evaluation records remain historical and unchanged.

## Hosted-review correction before merge

The original published head `a238942` passed all eight Windows/Linux CI jobs and its Codex review. Copilot then identified a valid coverage-reporting edge case: angle-bracket placeholder matching suppressed wrapped expression references before ordinary parameter coverage could mark them unknown. Both reported parameter shapes were independently reproduced with empty coverage and `completed_within_scope`.

Expression markers now take precedence over placeholder suppression. The narrow regression covers direct secret fields and Authorization name/value pairs, plus plain-placeholder controls. Independent read-only review verified the repair; restoring the old precedence in memory causes six regression failures. Wrapped references produce unknown coverage, not secret findings, and no execution authority was added. All four generated helper and contract copies match the corrected source.

Correction validation: 31 new focused tests pass; the complete local suite passes **313 tests with seven platform/PowerShell skips** (306 executed passes). The 3,000-case bounded mutation run, repository validation, generation/compatibility checks, whitespace and synthetic evaluation self-test also pass. These results supersede the initial source/test fingerprints above for the corrected snapshot, without extending native-host or live n8n acceptance. Hosted checks on the correction must be verified separately before merge.

Corrected helper SHA-256: `1e1db6d790689929ccab6540cd06e3cc277942c006be4f26d0999a875a9da55f`. Corrected new test SHA-256: `085bbd65b2ceb69a1662a32ae993612338d12dd21aec7b5f907a00673a221bbd`.
