# Synthetic Test Data Generator: bounded V1 validation

Baseline: `ab0d902903b2b13eb582c88ca5ba6b5e66d6957c`. New independent master: `master-skills/synthetic-test-data-generator`. No migrated source or existing shipped package changed. Claude, ChatGPT, Cursor and Codex are proposed candidate placements only.

## Scope and artifacts

The skill generates fictional test fixtures from schemas/test goals or analysis of another skill's entrypoint, contracts, resources and evaluation history. It records explicit, derived, historical and unresolved requirements, source fingerprints, case mappings and expected-outcome sources. It does not execute the skill being analyzed or infer permission for external actions.

The standard-library helper creates bounded deterministic JSON and CSV-with-sidecar fixtures. The fictional customer/orders example contains fourteen record cases (seven valid and seven invalid) plus a malformed JSON wire case. Seed 42, complete configuration and generator/configuration hashes support exact reruns. CSV labels retain original types and missing/null/empty distinctions; the CSV alone is not a lossless or application-specific import contract.

The Pi-hole pilot has thirteen traced requirements and twelve scenarios. The materializer verifies the actual bytes of three pinned sources before writing eleven CSV inputs and a JSON manifest. A no-data scenario intentionally has no input file. The fixed seed 20261103 describes the reviewed recipe; it is not a claim of random sampling. All records are fabricated, use reserved example domains/documentation addresses, and remain separate from live Pi-hole data.

## Independent forward review

A separate reviewer received the skill, fictional forward-use requests and repository location, without this test suite or evaluation rubrics. It exercised JSON/CSV generation, reconstructed every payload from CSV/sidecar, and generated a separate twelve-case scenario pack from the fictional target example with source fingerprints and explicit/derived/unresolved outcomes. These are bounded agent workflow observations, not native host acceptance or a comparative skill-quality study.

The first review found three issues, preserved rather than overwritten:

1. Serializing configuration with sorted keys lost the original CSV header order, so replay from embedded configuration changed bytes while keeping the same configuration hash. Fixed by defining and using canonical sorted field-name order.
2. An enum container of the wrong type produced `enum` rather than the documented precedence of `type`. Fixed by checking member types before membership.
3. A finite float wrong-type mutation could be represented in JSON but CSV rejected it with misleading nested-value guidance. Fixed by supporting finite scalar float cells and retaining their type in the sidecar.

Independent rechecks passed all three exact reproductions. Added regressions cover the repaired behaviors. No prior failing artifact was treated as a pass.

## Pi-hole numeric and staleness checks

Independent CSV parsing and arithmetic confirm:

- Mixed query data: 12 rows = 5 allowed + 5 blocked + 2 unknown; top allowed portal 3, top blocked ads 3; client counts 6, 4 and 2.
- Complete declared numeric-status matrix: 20 rows = 6 allowed + 12 blocked + 2 unknown; two clients have 10 rows each.
- No-blocked case: 3 rows, all allowed; no fabricated blocked candidates.
- Partial top-domain aggregate: two valid counts 5 and 3, subtotal 8, one invalid count; three CSV records are not three queries.
- Top clients: counts 9, 4 and 2, total 15. Adlists: two enabled, one disabled under the case's explicit 1/0 convention.
- Missing status and ambiguous text statuses retain unavailable/uncertain splits. Empty file and header-only input remain distinct. Python's strict CSV parser rejects the unterminated fixture; target recovery remains unspecified.

Two independent Pi-hole materializations matched file hashes. A copied target entrypoint was edited while its path and recorded revision stayed unchanged: the materializer rejected stale source content before creating output. Source fingerprints establish only the inspected files, not external dependencies or current official Pi-hole behavior.

## Limits

No native target-host routing evaluation, Pi-hole Analyzer model execution, live Pi-hole query, DNS change, endpoint contact, external upload, installation, packaging promotion, publication or merge was performed. Qualitative target response behavior, exact errors, current Pi-hole-version compatibility and application imports remain untested. This is not evidence of anonymization, statistical representativeness, broad security assurance or an independent implementation of the target application's validator. I/O interruption can leave a partial newly created output directory; existing destinations are refused, not overwritten.

Change-aware fixture regeneration beyond stale-source detection and failure minimization are deferred roadmap items, not part of this V1.

Repository-wide command results are recorded in the associated spec validation file after the final run.
