# Resume v2 human and boundary testing review

Mick authorized two v2 human reruns and generic, heading and date boundary tests, consolidated for review. This assessment uses the unchanged candidate at `81a5b4a3ce6cde0e4fa04c57d6e5ff03e32c0a73`. No candidate instructions, calculator, shipped skills, placement or promotion metadata changed. PR #11 remains draft. No installation, merge or promotion.

## Review result

The human numeric path repeats consistently within this small test: both originals score 76.7 and both rewritten documents score 85.0. Actual ZIPs, four ledgers, human category/severity tables and provider log outputs reconcile. The contradictory-date case also passes strict JSON, scoring and verdict-cap checks. The boundary round does not pass overall: generic, mixed-heading and the missing-date retry deliver invalid JSON with overescaped quotes. The mixed-heading diagnostic ledger additionally changes a calculator-owned reason. Keep full v2 acceptance open.

| Case | Delivered result | Assessment |
| --- | --- | --- |
| Human v2 repetition 1 | Original 76.7, Good but inconsistent; rewrite 85.0, Strong | Bounded numeric pass; heading inventory includes one fixture note |
| Human v2 repetition 2 | Original 76.7, Good but inconsistent; rewrite 85.0, Strong | Bounded numeric pass |
| Generic review | Reported 93.3, Excellent | Strict JSON failure; diagnostic repair reconciles generic weights and alignment |
| Mixed headings | Reported 96.7, Excellent | Strict JSON failure; diagnostic repair exposes a changed privacy reason and final-check failure |
| Missing start date, initial | ChatGPT response could not load | Host failure; underlying task outcome unassessed |
| Missing start date, fresh retry | Reported 93.3, Excellent | Strict JSON failure; diagnostic repair reconciles one chronology penalty |
| End before start | 90.0, Strong; one critical issue | Bounded strict JSON and verdict-cap pass |

Six planned cases required seven native attempts. Three completed attempts support bounded numeric/strict-delivery passes, three fail strict JSON delivery, and one host response is unassessed. The human inventory note is retained rather than treating equal numbers as perfect extraction repeatability. Reported numbers in failed rows are not accepted numeric deliverables.

## Inputs and capture

Every case ran in a separate ChatGPT Temporary chat with explicit candidate instructions, capability contract, references and exact Python calculator. The two human tasks and original resume bytes are identical to each other and to the previous human task/source. Boundary inputs are a fabricated Taylor Example resume with one SQL import-job achievement, supplied 100-records-daily throughput and a readable role entry. The generic case adds an unsupported Python skill without an external target. Targeted cases use the same Data Engineer/SQL target and independently change only the experience heading, omit the start date or put the start after the end.

Expected states/numbers and grading criteria stayed outside uploads. Input/resource hashes are pinned in the [fixture](fixtures/native-resume-v2-review.json). A separate fresh control returned NO to the prior-context availability question. This does not prove full effective-context isolation. Visible model was Instant; exact backend identity and complete provider context were unavailable.

A browser-control timeout after generic submission was recovered by checking the existing conversation; no duplicate generic task was submitted. The initial missing-date page displayed “This response couldn’t load.” Its bytes/capture remain retained. The fresh retry received identical packet/source bytes. Copy capture used a fresh sentinel, source Copy action and observed confirmation; an initial contradictory-case copy confirmation was delayed, so a second sentinel/Copy action established freshness. Native AX text is truncated; full copied responses were preserved separately. Raw chats, screenshots, ZIPs and logs stay private outside Git and OneDrive.

## Human numeric checks

The downloaded ZIPs are 7,436 and 7,540 bytes, each with exactly rewritten_resume.md, original_audit.json, rewritten_audit.json and execution_log.txt. Each original/rewrite ledger passes the exact v2 helper's final check and independent decimal calculation of all five categories and the total. Human tables and displayed final score headings match the artifacts. The four provider-supplied log outputs per run record zero exits and equal the delivered ledgers. These are provider-supplied traces, not independent observation of native tool execution.

Both originals use category values 66.7 / 83.3 / 100.0 / 33.3 / 100.0 and counts 0 critical / 1 major / 2 minor. Both rewrites use 100.0 / 83.3 / 100.0 / 33.3 / 100.0 and 0 / 1 / 1. The seven criterion identities and mappings match. Missing Graph experience affects alignment only; missing Intune measurements affect measurements only. Unknown post-May 2025 context does not lower chronology or privacy. The same-original spread is zero in this pair. Rewrites differ in wording, so their equal totals are not a same-document repetition control.

Both actual Markdown rewrites preserve Alex's identity/email, Example Labs role, Jun 2022 to May 2025 dates, degree/institution/year, 400 devices and 3-hour to 45-minute result. No Graph experience, certification, later employment, leadership or gap explanation is invented.

Repetition 1 lists Experience, Education and Target requirements as original section headings; repetition 2 lists only Experience and Education. The first ledger itself calls Target requirements a source note. This does not change the standard structure score because the two conventional resume sections are present, but it exposes inventory-scope drift on the identical source. Excluding fixture/task notes from the resume heading inventory needs an explicit boundary and follow-up test. Neither the helper nor equal totals establish observation truth.

## Boundary checks and retained failures

The generic, mixed-heading and missing-date retry responses contain two backslashes before embedded double quotes where a JSON string escape requires one. Their entire copied outputs fail ordinary JSON parsing and the unchanged calculator rejects each original with exit 2. Do not strip fences, normalize escaping or replace their results to count them as passed. Native displayed/copy delivery is what failed; raw backend generation and the exact serialization layer responsible are not available for attribution.

For diagnosis only, reducing those particular quote escapes once makes the three objects parse. These repaired copies are explicitly named diagnostic in private/public records and never substitute for original deliverables. Generic and missing-date diagnostic copies pass local final checking. Mixed-heading diagnosis still fails: its privacy criterion reason differs from scoring_evidence. All three diagnostic category/total calculations reconcile independently. This separates arithmetic and anchor observations from strict delivery and exact-ledger failures.

- Generic diagnosis uses the generic 25/35/20/10/10 profile, inventories SQL as supported and Python as unsupported, and maps alignment to common-patterns § Skills keyword dumps with weight 1.0. The unsupported skill affects alignment once; no external target is invented.
- Mixed-heading diagnosis records the actual Summary, Where I Made Things Work and Skills labels and assigns mixed structure 2/MINOR. Chronology and privacy keep full numeric credit. Its reason edit violates immutable-ledger delivery despite unchanged arithmetic.
- Missing-date diagnosis records missing_dates chronology 1/MAJOR for the absent start date, with standard headings and safe privacy. It requests verification and does not invent a replacement date. An unknown interval remains a separate unscored flag.
- The original contradictory-date response parses directly, matches the entire helper-derived ledger and passes local final checking. Jan 2025 to Dec 2024 receives chronology 0/CRITICAL; ATS is 50.0 and other categories are 100.0. The 90.0 total would ordinarily reach Excellent, but one critical issue correctly caps it at Strong. There is no extra trust penalty or guessed date correction.

Some targeted inventories include the target role title alongside SQL; both are supported in these fixtures, so this does not change their category result. The tests establish these observed outcomes rather than broad inventory completeness or invariance across different requirement representations.

## Consolidated review and next correction

The earlier [numeric assessment](native-human-numeric-2026-10-20.md) retained a 16.9-point original-score spread, arbitrary selected principles, category drift and duplicate timeline penalties. The [fixed-rubric correction](native-scoring-consistency-2026-10-20.md) fixed selection/mapping/ownership and produced consistent v1 human numbers. The [structure correction](native-resume-structure-2026-10-20.md) added v2 heading evidence and a passing sparse JSON observation after a retained ledger-editing failure. The present unchanged-v2 round adds human evidence and exposes JSON delivery failures under other inputs. Earlier failures and version distinctions remain intact.

Recommended next correction: serialize and validate the exact final JSON response, including embedded quotes, and preserve every calculator-owned field. Add a native fixture with quoted evidence. Clarify exclusion of task/fixture labels from heading inventories. Then rerun the three failed boundary deliveries and the affected inventory check. Keep acceptance pending until those failures are addressed or Mick explicitly accepts their documented bounds.

## Validation and limits

Independent checks cover all input/resource hashes, actual ZIP members and hashes, four original human ledgers, displayed table values, provider log/output equality, source-fact preservation and the strict contradictory-date ledger. Three invalid original JSON responses are rejected; diagnostic replays remain labeled. Local generator drift, repository/PowerShell quality (46 skills, zero issues) and 24 offline cases/99 negative checks passed in a clean Git-byte snapshot. Hosted delivery checks are tracked on the PR. Hosted structural tests cannot turn native failures into passes.

Only this assessment, its synthetic evidence fixture and tracking documents change. Broader extraction states, documents, repetitions, native hosts, installed discovery/routing, provider tool/no-network traces and calibrated hiring predictions remain unverified. Existing acceptance for other batches does not accept this round. No merge, installation or promotion.
