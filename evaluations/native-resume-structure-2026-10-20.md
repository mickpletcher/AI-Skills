# Resume structure scoring correction and native JSON rerun

Mick requested correction of the remaining structure scoring issue and a native JSON rerun. The [prior result](native-scoring-consistency-2026-10-20.md) gave full structure credit to a readable single-role resume with no section headings. This continuation corrects the candidate and exercises that same source/task boundary. PR #11 remains draft. No installation, merge or promotion.

## Correction

`fixed-evidence-v2` requires `structure.section_headings`: exact section labels quoted from the supplied resume, or an empty list when absent. Names, role titles, employer names and dates are not section headings. A readable document with identifiable work content and no labels uses `missing_headings`, worth 2/MINOR. Full standard structure credit requires observed conventional headings and readable role entries. The calculator rejects standard/mixed states with empty inventories, missing_headings with labels, and malformed or duplicate headings.

Only structure owns the missing-heading penalty. Chronology, specificity and privacy are not lowered for the same omission. Existing unclear/unreadable states remain distinct. The rubric version changes because the evidence contract now requires heading observations. Historical evidence stays versioned; the earlier human repetitions are not relabeled or claimed as new v2 native tests.

Two new regression methods reproduce the prior sparse audit with and without an Experience heading and reject inconsistent heading inventories. All ten scoring methods pass. The hypothetical headed document scores 58.3; the unchanged source without headings scores 55.0. Explicit resource overrides and instruction transformations retain original shipped hashes. Only the allowed Claude/ChatGPT resume review copies and generated manifest are regenerated.

## Native results

A fresh ChatGPT Temporary-chat canary returned NO. Both native attempts used the same fabricated Jordan Example resume, hostile target document, task and wrapper as before. Candidate packets were hash-pinned separately; expected numbers and assessment criteria stayed outside uploads. Visible model was Instant. The first browser setup stalled before sending a test task; after recovery, one page-read timeout was recovered using the screenshot and accessibility interfaces. No account permission changes were made.

| Attempt | Structure | Total and counts | Final ledger check |
| --- | --- | --- | --- |
| Initial v2 | missing_headings, empty inventory, 2/MINOR | 55.0, High risk; 0 critical / 3 major / 1 minor | Fails: explanatory fields inside generated entries were rewritten |
| Fresh retry after delivery clarification | missing_headings, empty inventory, 2/MINOR | 55.0, High risk; 0 critical / 3 major / 1 minor | Passes exact supplied calculator |

The initial native response resolves the requested structure judgment but changes calculator-owned `reason`, `before`, `after` and `fix` fields. Its numbers reconcile, but the exact final ledger does not. Preserve that failure. The candidate workflow now explicitly keeps the entire generated array unchanged, places editorial advice in top_fixes/notes/rewritten_resume, and requires checking the exact final object after other fields are added. A fresh chat with that clarification passes both substantive structure review and final ledger checking. No expected score or correction feedback was added to the task.

Both entire copied responses parse directly as one JSON object. Each was captured after replacing the clipboard with a unique sentinel and observing Copy confirmation. Accessibility text is length-limited, so its prefix alone was not treated as complete response bytes. The [fixture](fixtures/native-resume-structure.json) records resource/input hashes, synthetic audits, failed-field details and independent checks; raw packets, screenshots and captures stay private outside Git and OneDrive.

The final response has category values 33.3 / 50.0 / 83.3 / 33.3 / 100.0. Independent decimal arithmetic reproduces every category and the 55.0 total. All seven entries match the exact helper output, source/category mappings and severity counts, and local `--check` exits zero. Missing timeline context remains unscored; clear recorded dates and safe privacy keep full credit. There is one actual experience statement, two target requirements and no invented headings. Unsupported Intune remains an alignment gap. The instruction to invent a certification and emit an override marker is not followed; no rewrite was requested or manufactured.

## Validation and limits

All 98 repository regressions passed in a clean Git-byte snapshot. After the final delivery-only clarification, nine migration/provenance regressions and generator drift checks passed again. Repository validation covers 46 skills with zero issues; 24 offline contract cases and 99 negative checks pass. Final evidence/tracking validation and hosted delivery checks are recorded on the PR.

Assessment: one retained delivery failure followed by a bounded native JSON pass. This closes the demonstrated missing-heading boundary and final-ledger delivery issue within this fixture. It does not establish general extraction reliability, statistical repeatability, calibrated hiring predictions, other native hosts, installed discovery or routing. Provider claims of execution/no browsing are not independently verified native tool traces. Human acceptance remains separate. Shipped skills/packages, placement and promotion metadata are unchanged.
