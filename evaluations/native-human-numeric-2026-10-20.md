# Native human numeric resume scoring

The human resume rerun in the [previous repair assessment](native-batch2-repairs-2026-10-20.md) used qualitative fallback. Mick requested a direct test of numeric scoring on 2026-10-20. This continuation tests the existing candidate at `1b55d20c5dc2ad5d183f1885fb5d00b0882c12a4`; no candidate instructions, helpers, shipped skills or placement changed. PR #11 remains draft. No installation, merge or promotion.

## Test scope

Two independent fresh ChatGPT Temporary chats received identical task text and identical fictional Alex Example resume bytes. Each explicitly requested human output, numeric scores for the original and rewrite, separate source-backed ledgers, exact supplied calculator execution and final `--check`, and a downloadable ZIP with both audits, the rewritten Markdown and execution log. A qualitative fallback would leave this numeric test incomplete. The task did not supply expected scores or preferred judgments.

The selected instructions, capability contract, library, scoring references, JSON ledger schema and calculator were pinned before execution. A separate fresh isolation canary returned NO when asked whether prior evaluation context was present. Criteria stayed outside the uploaded packets. Visible model control was Instant; exact backend snapshot and full effective context were unavailable. This tests explicit candidate packets, not installed discovery or natural routing. The [fixture](fixtures/native-human-numeric.json) records source/input/resource hashes, synthetic scoring entries, captured display values and independent checks.

## Results

| Run | Original score and verdict | Rewrite score and verdict | Delivered ZIP |
| --- | --- | --- | --- |
| 1 | 54.5, High risk | 77.6, Good but inconsistent | 6,701 bytes, exactly four requested files |
| 2 | 71.4, Good but inconsistent | 84.9, Strong | 7,188 bytes, exactly four requested files |

Both runs complete the human numeric delivery and reconciliation path within these bounds:

- All four downloaded ledgers independently reproduce every category and total using decimal arithmetic and the documented targeted weights. All four also pass a local `--check` using the exact pinned candidate calculator.
- Captured human table cells match both supporting ledgers for all five categories and severity counts. Displayed totals and verdicts also match. Counts are 0/5/3 and 0/2/3 in run 1, and 0/4/4 and 0/2/2 in run 2, ordered critical/major/minor for original and rewrite.
- All cited library names exist with the mapped weights/categories; common-pattern headings exist and use weight 1.0. This mechanical attribution check does not establish that every chosen category is semantically appropriate.
- Both actual ZIPs contain `rewritten_resume.md`, `original_audit.json`, `rewritten_audit.json` and `execution_log.txt`. Both logs record four commands with exit code zero: scoring and final checking for each version. Their four captured JSON outputs agree with the delivered ledgers. Logs are provider-supplied artifacts, not independent native tool traces.
- Both rewritten files preserve the supplied identity, employer, historical title/dates, degree, 400-device scope and 3-hour to 45-minute result. The 75% reduction in run 2 is mathematically derived. Neither rewrite claims Graph experience, certifications, later employment, leadership or an invented gap explanation. Local source files remain byte-identical.

## Scoring quality concerns

Numeric delivery works, but the scores are not stable enough to treat as a repeatable quality rating. The identical original differs by 16.9 points and crosses verdict bands. The rewrites differ by 7.3 points and also cross verdict bands. The rewrites themselves differ, so their score difference is not a pure same-document repeatability measurement. The original-resume difference is the direct repeatability observation.

The ledgers expose concrete causes:

1. Source selection changes. Run 1 uses nine entries; run 2 uses eleven, adding a positioning principle and selecting different common patterns for Professionalism and Trust. The calculator normalizes whichever entries it receives, so it cannot enforce a stable assessed scope.
2. Category assignment for common patterns remains unconstrained. Run 2 puts `common-patterns § Action verb, object, outcome` in Professionalism and Trust. That pattern concerns bullet evidence and structure; the ledger does not justify its placement in trust scoring. Together with the no-personal-data pattern, this yields 83.3 and then 100.0 for that category. Run 1 instead uses the unexplained timeline and scores 33.3 for both versions.
3. Possible duplicate penalties remain. Run 1 counts the same missing post-May 2025 context under the library chronology principle and the common red-flags pattern across two categories. No fabricated gap story is added, but scoring the missing context twice needs a defined precedence rule.
4. Severity and evidence judgments vary. The same original bullet-specificity principle is scored 2/MINOR in run 1 and 3/INFO in run 2. Missing Graph evidence is 1/MAJOR versus 2/MAJOR. Deterministic aggregation cannot resolve differences in the supplied judgments.

Assessment: two bounded passes for human numeric delivery, calculation, source existence and factual preservation. Substantive scoring consistency is unresolved. This closes the unexercised human numeric delivery gap; it does not accept the overall scoring rubric or certify interview predictions. The next correction should define a stable assessed principle set, category mappings for scored common patterns, and treatment of overlapping findings and missing evidence. Then rerun the same original in fresh chats. Candidate changes are outside this assessment-only continuation.

## Evidence and validation

Full visible conversation/DOM captures, table cells, screenshots, downloaded ZIPs and execution logs stay private outside Git and OneDrive. Public fixtures contain synthetic source metadata, scoring entries, bounded results and hashes. Actual downloaded files were inspected; displayed links alone were not graded as delivery. A local replay initially decoded Windows output using the wrong encoding; rerunning the unchanged calculator with Python UTF-8 mode passed all four checks. This was an evaluator capture issue, not a candidate score failure.

The prior qualitative fallback, original scoring failures and intermediate JSON formatting failure remain recorded. No acceptance is inferred from this request. Exact provider tool execution, full no-network behavior, provider-side source preservation and other hosts remain unverified. Repository/document and generated-resource validation are recorded on the delivery commit; hosted structural checks do not establish scoring reliability.

Local validation passed: all four public fixture ledgers and pinned resources, nine migration/provenance regressions, generator drift and repository quality across 46 skills with zero issues. Only evidence, assessment and tracking files changed. Hosted checks are tracked on the PR delivery commit.
