# Tasks

- [x] Inventory 35 Claude skills and existing canonical foundation.
- [x] Add 32 masters and provenance with dependencies and license notices.
- [x] Generate four-target bundles without changing shipped trees.
- [x] Add migration catalog, ownership checks and regression tests.
- [x] Complete focused static review of generation, capability contracts and the three foundational masters.
- [x] Fix linked-parent/junction, destination type and portable filename collision gaps; add offline regressions and read-only generator workflow permissions.
- [x] Complete final local/CI verification of the review fixes.
- [ ] Complete target-host behavioral evaluation; the authorized foundation pilot is tracked below.
- [ ] Separately authorize promotion after behavior evidence and human review. No promotion is authorized by this pilot.

- [x] Audit three foundational masters against originals, restore portable requirements with provenance, and distinguish pasted-input modes from file operations in seven contracts.

## Review validation, 2026-10-19

- Clean Git snapshot plus the reviewed diff: all 66 Python unit tests passed on Windows with Python 3.12, including real symlink and junction fixtures. The new collision regressions also detected the original generator failures.
- Generator drift check, Python compilation, repository and PowerShell quality validation passed. Repository validation checked 46 shipped skills with zero issues; exact-case folder validation checked 35 Claude skills with zero issues.
- All 22 installer regressions passed under PowerShell 7 and Windows PowerShell 5.1 using temporary libraries.
- Synthetic fixture self-test passed 24 cases and 99 negative checks without model calls. Separate foundation model captures are tracked below.
- All six hosted checks passed for code commit `8b8e0b8349dc140531d15a3b704591bd484d0873`: [Windows/Linux validation](https://github.com/mickpletcher/AI-Skills/actions/runs/39272642478), [installer matrix](https://github.com/mickpletcher/AI-Skills/actions/runs/39272642167), and [generator drift](https://github.com/mickpletcher/AI-Skills/actions/runs/39272642211).
- Original shipped sources, packages, catalogs, checksums and the API runner are unchanged. Ignored local notes and the existing local itinerary-template line endings were preserved; validation used Git source bytes rather than rewriting the working files.
- PR #11 remains draft and unmerged. Host/model comparisons, helper certification, wider-distribution configuration review and promotion remain separate outstanding work.

## Foundation behavioral pilot, 2026-10-19

- [x] Prepare six synthetic cases for the three foundational skills, with comparison conditions, rubrics and hard failures.
- [x] Select the configured Codex CLI model/settings and verify a tool-disabled canary with unrelated skill descriptions removed. This did not establish complete context isolation.
- [x] Capture 36 responses: six scenarios, three instruction conditions and two fresh-session repetitions.
- [x] Record assistant triage, the line-count discrepancy, context contamination and coverage limits without claiming human approval.
- [x] Establish and audit a separate evaluation profile and fixed base instructions, then rerun every condition: 36 replacement responses, 37 context renders and eight offline context-gate regressions. Preserve the confounded first batch unchanged.
- [x] Complete evidence-backed assistant scoring: 172 applicable rubric items across all 36 replacement responses; all 12 candidates meet the bounded text-only rubrics. Record the original/control reporting gaps and scaffold planning-note failure in the [sanitized assessment](../../evaluations/foundation-pilot-2026-10-19.md).
- [x] Validate the replacement evidence: consistent host/base context, unchanged fixture/source hashes, zero observed profile/injection markers or tool events, 25 Python blocks and 12 PowerShell proposals parsed without execution, and five reported line counts checked accurately. All 66 repository regressions passed in a clean Git-byte snapshot.
- [x] Pin whitespace-only line semantics to `bool(line.strip())`, including Unicode whitespace, universal newlines and an unterminated final line. Add a seventh fixture scenario, six runtime oracles and three offline mutation regressions.
- [ ] Obtain human rubric review and acceptance. Assistant scores do not approve a skill or model profile.
- [ ] Complete the full host/tool/routing scenarios and human acceptance review before considering promotion.

## Initial runtime phase, 2026-10-19

- [x] Capture four targeted architect candidate responses under fixture revision 2 with five audited contexts. Preserve prior captures and remove temporary evaluation credentials.
- [x] Run the 12 prior PowerShell proposals through nine Pester tests on both PowerShell 7 and Windows PowerShell 5.1. Verify zero before/after analyzer findings with identical default settings.
- [x] Execute installation, text/JSON examples, help and unittest commands for both prior candidate README drafts in synthetic temporary repositories.
- [x] Execute both fresh architect scaffolds and both focused regression proposals: 65 generated pytest cases passed; all independent whitespace/error checks passed. Retain one original Ruff formatting failure among 70 Python command checks.
- [x] Verify a separate one-file, unchanged-AST formatting repair with lint, formatting and all ten affected pytest cases passing. Preserve original failures and exclude corrected harness attempts from model pass counts. See the [runtime assessment](../../evaluations/foundation-runtime-2026-10-19.md).
- [x] Validate the branch changes in a clean Git-byte snapshot: all 69 Python regressions, generator drift, repository/PowerShell quality, exact-case folders and the 24-case/99-negative-check offline self-test passed.
- [ ] Complete wider PowerShell/README scenarios, routing coverage and human acceptance. Linux replay and the bounded fresh agent cases are tracked below. The full revised comparison matrix has not been run.

## Architect delivery and Linux continuation

- [x] Require formatter application, formatting/lint/test gates and delivery of the exact final files in the architect master; regenerate all allowed review candidates while preserving the historical source audit.
- [x] Add reviewed, hash-pinned synthetic executable excerpts and a Linux runtime workflow with network-disabled execution, isolated projects and retained result artifacts. Keep raw model responses and personal context private.
- [x] Execute Linux PowerShell contracts and Python 3.11 through 3.14 replays for README and architect: nine Pester tests, 312 Python command checks and 65 pytest cases per Python version passed. Require the known original formatting failure, a one-file unchanged-AST repair, passing final gates and matching delivered file hashes.
- [x] Inspect all five uploaded execution ledgers and delivered files; record hosted results and limits in the [Linux assessment](../../evaluations/foundation-linux-runtime-2026-10-19.md). Fix the release-bundle documentation link found by hosted regression testing.
- [ ] Complete broader independent agent/tool scenarios and human review. The four fresh cases below establish bounded tool-workflow evidence separately from artifact replay. Human acceptance and promotion remain blocked.

## Fresh tool workflow testing

- [x] Prepare four isolated synthetic cases and verify a real shell/file canary. Pin candidate instructions to `5c0fa9364200c1a48348a809f7533fb4d70bedc8`; audit each session context and remove temporary evaluation credentials after capture.
- [x] Run a fresh architect agent through real creation, formatter application, failing-test feedback and final gates: 26 pytest cases and 31 independent command checks passed; final Python hashes match its delivery snapshot.
- [x] Run broader PowerShell deduplication and naming-only cases with repository analyzer settings. Seven and two final Pester tests passed; public metadata and 26 independent baseline probe groups match. Preserve and explain the naming-only case's existing warning.
- [x] Repair another synthetic repository's README with real file/tool access. Execute all seven documented code blocks and eight independent probes; verify source, tests, dependencies, examples and license are unchanged.
- [x] Complete bounded assistant assessment, preserve intermediate failures and prepare the local human review packet. See the [fresh workflow assessment](../../evaluations/foundation-tool-workflows-2026-10-19.md).
- [x] Relocate retained private evidence outside the checkout and sync roots after removing the temporary login copy. Clarify the profile-location requirement and include the credential-storage limitation in the private human review packet.
- [x] Obtain Mick's acceptance of the bounded results for all three skills, confirmed in this chat on 2026-10-19. This does not certify broader host/model/routing coverage or resolve the unverified credential sync status. PR #11 stays draft; merging and promotion remain unauthorized.
- [x] Select and scope the next small batch separately: Mick authorized `spec-writer`, `pihole-csv-analyzer` and `photo-rename` on 2026-10-19.

## Second migration batch

- [x] Prepare six synthetic scenarios with separate assessment criteria and preflight ecosystem placement. Use Codex candidates for spec/CSV and the ChatGPT photo candidate through the CLI only as a behavioral proxy; preserve the photo skill's existing placement exclusions.
- [x] Complete seven domain captures for six scenarios plus a real shell/file canary with audited client context. Preserve the first preview's image-evidence limit and use an explicit-image rerun for the visual assessment. Remove temporary evaluation logins outside the checkout and sync roots.
- [x] Independently verify metrics, actual file effects and preservation of supplied files; assess planning quality, uncertainty and candidate recommendations. Replay the reviewed copy script and verify repeat refusal without file changes.
- [x] Record results and limits in the [second batch assessment](../../evaluations/migration-batch2-2026-10-19.md). Correct attachment argument parsing and require exact image/prompt audit with five negative regressions. All six scenarios pass bounded assistant review; no demonstrated master instruction defect requires a change.
- [x] Complete final documentation/quality validation: 72 unit tests, 22 installer regressions, generator drift, 24 offline cases with 99 negative checks, repository/PowerShell quality and exact-case folders passed. Deliver the assessment and fixture through draft PR #11; no skill or placement changes.
- [x] Obtain Mick's acceptance of the six bounded scenarios, confirmed by his instruction to carry out acceptance, native photo follow-up and next-batch selection on 2026-10-19. Native host results and broader certification remain separate; merging, promotion and placement expansion remain unauthorized.

## OpenAI directory grouping

- [x] Group existing ChatGPT/Codex sources and generated candidates under `openai/`, preserving target IDs, suitability, skill bytes and promotion gates. See the [implementation and validation checklist](../006-openai-ecosystem-grouping/tasks.md). This structural change does not accept additional behavioral results.

## Native photo follow-up and third batch

- [x] Prepare three disposable JPEGs, two with verified fabricated capture-date/GPS EXIF and one without metadata, plus original-byte ZIP inputs and blinded assessment criteria. Pin the existing ChatGPT candidate and preserve account settings.
- [x] Attempt native ChatGPT testing after Mick's sign-in and extension setup. Verify successful synthetic attachment delivery and preserve two Instant response-load failures plus one Thinking failure. Record independent input hashes/EXIF checks and host limits in the [native record](../../evaluations/photo-native-2026-10-19.md).
- [x] Retry in a fresh native Temporary chat and assess actual preview content. Send the authorized copy follow-up, retain download-control failures and verify Mick's saved ZIP: three byte-identical JPEG copies with preserved EXIF/extensions plus correct mapping. Full native context/tool trace and no-browsing audit remain unverified; see the [bounded native result](../../evaluations/photo-native-2026-10-19.md).
- [x] Select and scope `github-social-preview`, `n8n-workflow` and `trip-email-html-itinerary` for the next synthetic batch. Record [six planned cases and execution gates](../../evaluations/migration-batch3-scope.md); no inference or live actions are claimed by this selection.
- [x] Validate the initial documentation/fixture overlay in a clean Git-byte snapshot: repository and PowerShell quality (46 skills, zero issues), generator drift and 24 offline cases/99 negative checks passed. Independently verify input ZIP, JPEG/EXIF hashes and candidate pins. Native output verification was subsequently completed for the downloaded copies as recorded above.

## Third migration batch execution

- [x] Run the six selected synthetic cases plus a shell canary with audited isolated client inputs. Preserve raw evidence outside sync roots and remove the temporary login; original login unchanged.
- [x] Independently verify two JPEG previews, preserved source bytes, inactive n8n graph structure and 135 pure-policy/embedded-code checks. Review both itinerary outputs for reconciliation/redaction, valid static navigation and no automatic external resources. Record the [assessment](../../evaluations/migration-batch3-2026-10-19.md) and [fixture](../../evaluations/fixtures/migration-batch3.json).
- [x] Replay strict itinerary validation: reconciliation case has zero errors/warnings; unknown-address redaction case has zero errors and two map warnings, exit 1. Preserve this defect rather than guessing addresses or bypassing validation.
- [x] Validate the evidence/tracking overlay in a clean Git-byte snapshot: repository and PowerShell quality (46 skills, zero issues), generator drift and 24 offline cases/99 negative checks passed. No candidate resource or shipped skill/package changed.
- [x] Correct the candidate map validator for pending addresses, retain supported-address checks and record an explicit provenance override. Five executable regressions pass; both unchanged itinerary artifacts pass strict replay with zero errors/warnings. Shipped skills/packages are unchanged. See the [follow-up assessment](../../evaluations/itinerary-validator-2026-10-19.md).
- [x] Perform four offline visual checks at desktop and phone widths using an allowed standalone renderer. Three bounded passes; reconciliation phone table clips where horizontal scrolling is unsupported. Preserve the unresolved result and original artifacts.
- [x] Validate the candidate correction and evidence overlay in a clean Git-byte snapshot: 79 unit tests, generator drift, repository/PowerShell quality, exact-case folders and 24 offline cases/99 negative checks passed. Shipped source/package/catalog/checksum files are unchanged.
- [ ] Deferred at Mick's request: verify every reconciliation booking-table column in a permitted native phone renderer. Browser policy rejected local file URLs; the offline renderer cannot establish scrolling, iPhone/Apple Notes or print behavior. Deferral is not a pass or acceptance.
- [ ] Obtain human acceptance of the third batch and bounded native photo result. Keep PR #11 draft; no merging, installation or promotion.

## Candidate helper and deployment follow-up

- [x] Reproduce Obsidian silent overwrites and vault traversal with disposable files; preserve real notes and shipped helpers.
- [x] Correct candidate note creation and folder containment, add seven executable regression methods and record an explicit resource override plus instruction transformation.
- [x] Review and correct the Proxmox candidate: confirmed deployment inputs, dedicated application identity, virtual environment, exclusive config creation and conditional external exposure. Preserve original source provenance; no live infrastructure changes.
- [x] Correct stale coverage/acceptance and byte-preservation claims in the canonical README and generic audit. Record the [assessment and limits](../../evaluations/candidate-followup-2026-10-19.md).
- [x] Complete clean Git-byte snapshot validation: all 86 unit tests, generator drift, repository/PowerShell quality, exact-case folders and 24 offline cases/99 negative checks passed. Check all five Proxmox Bash blocks, unit consistency and exclusive config creation with synthetic inputs. Deliver only candidate resources, provenance, regressions and docs through draft PR #11; shipped source/packages and ecosystem placement are unchanged.
- [x] Resolve generated Codex frontmatter rejection through a target-specific name/description header while preserving full canonical metadata in source and build provenance. Audit all 12 allowed candidates and baseline/named-model behavior. Native runtime certification remains separate.

## Compatibility, helper runtime and remaining skills

- [x] Audit Codex headers and preserve source metadata without changing other targets or suitability. Add structural and named-model regressions.
- [x] Exercise remaining helpers with synthetic inputs and mocked scheduler, Apple Notes and browser boundaries. Correct preview collisions/reprocessing, failure statuses, resume YAML quoting and forced task replacement. Record original helper hashes and candidate overrides.
- [x] Complete dependency-provisioned helper testing in hosted CI: all eight methods passed without skips, including real compressed FITS parsing with Astropy 8.0.2 and Pillow 12.3.0. Retain the failed local download and explicit local skips. [Hosted helper job](https://github.com/mickpletcher/AI-Skills/actions/runs/39373559695).
- [x] Complete local regression/quality checks and deliver commit `24c20b4962899046febcf32765b622ce5eadb2a0` through draft PR #11. All 12 hosted jobs passed, including both full 88-test repository jobs and helper runtime.
- [x] Run and assess two isolated cases for each of the 26 remaining domain skills: 52 captures, all input-preservation/client-context audits passed. Final review records 46 bounded passes, five response/contract failures and one fixture-limited result; preserve original captures. See the [assessment](../../evaluations/migration-batch4-2026-10-20.md).
- [x] Correct four candidate writing masters with exact provenance: final-text counting, evidence-scoped preservation claims and clear default website length variants. Run 30 targeted cases plus four final website cases, with two repetitions. Retain intermediate format gaps, original failures and the canary wording correction; verify input preservation and credential cleanup. Conversational runs remain CLI proxies.
- [x] Complete final source/provenance/quality validation and deliver the behavioral assessment and candidate corrections through draft PR #11. Nine migration regressions, generator drift, repository/PowerShell quality (46 skills, zero issues) and 24 offline cases/99 negative checks passed in the final clean snapshot. Hosted full regression checks are tracked on the delivery commit.
- [x] Mick accepted the bounded remaining-skill behavioral results on 2026-10-20 and authorized targeted native testing. Acceptance includes the documented initial failures, fixture limits and follow-up scope; it does not certify native hosts or authorize installation, merging, placement expansion or promotion. See the [native continuation](../../evaluations/native-writing-2026-10-20.md).

## Targeted native writing continuation

- [x] Run four selected ChatGPT candidates in fresh native Temporary chats using pinned synthetic packets and an availability canary. Keep criteria outside packets and record Instant/backend/context limits; no installation or routing claim.
- [x] Preserve native X count and website attribution failures. Correct two candidate masters with exact source transformations and run three fresh correction checks. Final observed X count, website attribution/lengths and grounding checks pass; intermediate website failure remains recorded. See [seven native executions](../../evaluations/native-writing-2026-10-20.md).
- [x] Preserve complete visible response records privately, check transcription integrity and packet hashes, and publish only bounded assessment metadata. Retain the initial blank-tab interruption and reject stale clipboard capture.
- [x] Complete final validation and publish acceptance/native evidence through draft PR #11. Nine migration regressions, generator drift, repository/PowerShell quality (46 skills, zero issues) and 24 offline cases/99 negative checks passed. Hosted delivery checks are tracked on the PR commit.
- [x] Mick accepted the bounded native-writing results on 2026-10-20 and authorized the next targeted batch. Retain the three failed captures and all limits. Broader native ecosystems, installed discovery/routing and remaining earlier gates are not certified; no merging or promotion.

## Second targeted native batch

- [x] Select and pin six synthetic cases across pihole-csv-analyzer, resume-writer and github-social-preview at source commit `5040dd57e4f78bbdab6a0d858eba524e78a58f4f`. Use native ChatGPT instruction packets, disposable file artifacts and criteria outside the uploaded packets; no infrastructure, applications, library updates or publication.
- [x] Execute six native cases plus two CSV delivery follow-ups. Independently inspect actual ZIP, Markdown and JPEG bytes, CSV counts and resume arithmetic; record three bounded passes and three failures. Retain recovered download-event/link limitations separately from artifact verification. See the [assessment](../../evaluations/native-batch2-2026-10-20.md).
- [x] Correct resume score/severity reconciliation and scoring-map/library attribution, then rerun human and JSON native cases. Deterministic ledger calculator and eight regressions pass. Native human qualitative fallback and final pure JSON rerun pass bounded review; retain the intermediate JSON code-block failure. Native human numeric scoring remains unexercised. See the [repair assessment](../../evaluations/native-batch2-repairs-2026-10-20.md).
- [x] Correct social-preview tag/language-badge overlap, add a layout regression and rerun the long-title native case. Three rendering regressions pass. Actual 1280x640, 98,802-byte JPEG has separated topic pills and Python badge; truncation is disclosed.
- [x] Validate and publish the bounded assessment through draft PR #11. Repository/PowerShell quality (46 skills, zero issues), generator drift and 24 offline cases/99 negative checks passed. No candidate/source changes, installation, merging, placement expansion or promotion; hosted delivery checks are tracked on the PR commit.
- [ ] Obtain separate human acceptance of the second native batch.

## Native human numeric scoring continuation

- [x] Test the previously unexercised human numeric path in two fresh native chats using unchanged candidates and identical synthetic resume/task inputs. Independently check actual ZIPs, four ledgers, source citations, displayed category/severity values and calculator outputs. Both runs pass bounded delivery/reconciliation checks. See the [assessment](../../evaluations/native-human-numeric-2026-10-20.md).
- [x] Assess repeatability separately from arithmetic. The identical original scores 54.5 versus 71.4 across verdict bands. Record changing principle selection, unconstrained common-pattern category assignment and possible duplicate timeline penalties. Preserve prior failures/fallbacks; do not treat this as rubric acceptance.
- [x] Define the fixed seven-criterion evidence rubric, canonical source/category mapping and single ownership of overlapping findings. Regenerate allowed resume candidates and rerun two same-original native human cases: both score 76.7, with both rewrites at 85.0. Verify actual ZIPs, four ledgers, displays and provider logs. See the [correction assessment](../../evaluations/native-scoring-consistency-2026-10-20.md).
- [x] Run a fresh strict JSON/source-injection regression: parsing, fixed-ledger calculation, missing-timeline ownership and injection boundaries pass. Preserve its unsupported full structure credit and an interrupted human attempt; neither is a full substantive pass.
- [x] Define readable missing-heading structure as 2/MINOR with a required quoted heading inventory and versioned evidence contract. Add paired headed/heading-free and malformed-inventory regressions. Rerun native JSON: retain the initial edited-ledger failure, clarify immutable-ledger delivery and verify a fresh final 55.0 audit with exact helper replay. See the [structure correction](../../evaluations/native-resume-structure-2026-10-20.md). The calculator still cannot verify observation truth from resume text.
- [ ] Obtain separate acceptance of the bounded scoring-consistency results; keep broader reliability, native-host and promotion gates open.

## Resume v2 consolidated native review

- [x] Repeat human numeric testing twice with the unchanged final v2 candidate and identical task/source bytes. Verify actual ZIPs, four ledgers, displayed categories/severity, provider log outputs and preserved facts. Both originals score 76.7 and both rewrites 85.0; retain original heading-inventory scope drift.
- [x] Execute generic, mixed-heading, missing-start-date and contradictory-date native cases with a fresh missing-date host retry. Record three strict JSON delivery failures, one unassessed host load failure and the passing 90.0/Strong contradictory-date cap. Diagnostic quote repairs are not original-response passes. See the [consolidated review](../../evaluations/native-resume-v2-review-2026-10-20.md).
- [x] Correct final JSON serialization, immutable-ledger delivery and context-heading scope. Three final native copied JSON audits pass exact checks at 93.3/96.7/93.3; both human heading inventories and all four ledgers reconcile. Retain intermediate Copy failures and two unassessed host failures. See the [repair assessment](../../evaluations/native-resume-v2-repairs-2026-10-21.md).
- [x] Correct experience activity/result grouping and exclusion of embedded fixture notes with the v3 source-block/context-note contract and two regression methods. Two fresh same-original native human runs now agree at 76.7/85.0; actual ZIPs, four ledgers, source partitions and human tables reconcile. Retain the earlier v2 10-point spread. See the [grouping assessment](../../evaluations/native-resume-grouping-2026-10-21.md). Broader extraction reliability and separate acceptance remain open.
- [ ] Obtain separate human review of the consolidated v2 results and retained failures. Keep all broader host/routing and promotion gates open.

## Resume v3 consolidated review

- [x] Rerun generic, mixed-heading, missing-start-date and contradictory-date native JSON boundaries against unchanged committed v3 resources. All four entire Copy exports parse directly, equal rendered JSON and pass exact ledgers/Decimal replay at 93.3/96.7/93.3/90.0; the critical chronology case is capped at Strong. No retries or new failures.
- [x] Consolidate the four fresh JSON cases with the two earlier v3 human runs. Verify identical resource hashes and replay all four actual human ZIP ledgers. Preserve the v1/v2 failure history and distinguish earlier human observations from fresh boundary executions. See the [v3 review](../../evaluations/native-resume-v3-boundaries-2026-10-21.md).
- [x] Mick accepted the consolidated bounded resume v3 results in this chat on 2026-10-21 and authorized the next targeted native batch. Acceptance covers the documented six native executions/eight audits and their limits. Earlier failed captures remain failed; broader extraction reliability, document formats, native hosts/models/routing and all promotion gates remain open.

## Third targeted native batch

- [x] Select spec-writer, idea-forge and obsidian-workout-export using existing allowed ChatGPT candidates. Pin six synthetic cases and candidate/input hashes, with assessment criteria outside uploads. Keep filesystem work inside disposable chat repositories/vaults; no real app, infrastructure, installation, publication or promotion.
- [x] Execute six primary cases and two duplicate/correction follow-up turns. Independently verify four actual ZIPs, spec source preservation, 52.5/55 score arithmetic and safe helper replay. Record four bounded passes and two workout delivery failures: unscoped combined duration and leading blank lines in native Copy-code frontmatter. See the [assessment](../../evaluations/native-batch3-2026-10-21.md).
- [x] Correct combined-duration scope and add a read-only boundary/scope validator with six regression methods. Two actual native combined ZIPs pass date, source and scoped-duration checks; both duplicate/correction workflows preserve content and ask before re-exporting. See the [repair review](../../evaluations/native-workout-repairs-2026-10-21.md).
- [x] Retain the remaining inline delivery failures: three of four exact native Copy exports begin with LF despite plain text code delivery. Require validated canonical downloads for every permitted file-capable initial/corrected export and disclose unverified inline Copy. No failed copy is normalized into a pass.
- [x] Resume after sign-in and verify the final revision's actual 743-byte combined ZIP. Exact frontmatter boundary, full YAML, source/date preservation and scoped ride duration pass; candidate/input hashes are unchanged. Retain three duplicate primary/regeneration host load failures as unassessed.
- [x] Rerun the sequence, retain another Instant host failure and a separate Medium template-source failure, then remove the hardcoded program example and regenerate allowed candidates. Latest Medium checks verify a source-faithful 895-byte combined ZIP, duplicate confirmation and exact 324-byte corrected/recovered downloads equal to native Copy. One explicit original-source recovery turn is labelled separately; initial response load failures remain unassessed.
- [x] Consolidate the exact artifacts, raw copies, source comparison and mode/host limits for bounded acceptance review. No failed initial delivery or unlogged-program note is converted into a pass.
- [ ] Verify cold-start initial delivery/repeatability and Instant recovery; separate recovery exports do not satisfy those gates. Real Obsidian ingestion and broader host/model/routing compatibility remain unverified.
- [x] Mick explicitly accepted the bounded workout results on 2026-10-21 and authorized the next untested native batch. Acceptance covers the observed combined, duplicate and corrected/recovered delivery paths in Medium. Cold-start initial delivery, repeatability, Instant recovery, real Obsidian ingestion and broader compatibility stay open; earlier failed artifacts remain failed. Acceptance of spec-writer/idea-forge is not inferred from this workout-specific instruction.


## Fourth targeted native batch

- [x] Select travel-research, travel-planning and travel-itinerary from skills without targeted native records. Pin six fabricated cases and exact existing candidate/input hashes; keep criteria outside uploads. No real trips, browsing, bookings or app writes.
- [x] Execute six fresh Instant Temporary chats without domain retries. Independently replay weighted scores and budgets, verify month/year boundaries, traveler presence, missing-input placeholders, source isolation and master/mobile agreement. Retain exact native whole-response Copy exports and private captures. See the [assessment](../../evaluations/native-batch4-2026-10-21.md).
- [x] Record six bounded passes and the first research response's explained mixed rounding (8.0/8 display versus exact 7.95). Retain streaming/clipboard timing limits without inventing extra model attempts or artifact-download claims. No candidate changes.
- [x] Complete clean tracked-byte snapshot validation: 108 regressions, generator drift, repository/PowerShell quality (46 skills, zero issues), exact-case folders and 24 offline cases/99 negative checks pass. Deliver the seven review/tracking files through draft PR #11; hosted checks are tracked on the delivery commit.
- [x] Mick explicitly accepted the six bounded travel results, including the explained display-precision caveat, on 2026-10-21 and authorized the next untested native batch. Live research, standalone file/Obsidian/mobile/print ingestion, repeatability, broader hosts/models/routing and earlier gates remain open. Workout initial delivery stays open; no merging, installation or promotion.


## Fifth targeted native batch

- [x] Select blog-post, linkedin-post and astrophotography-processing from skills without targeted native records. Pin six fabricated cases, exact existing candidate resources and synthetic PNG/FITS inputs; keep criteria outside uploads.
- [x] Execute seven fresh Instant conversations: six completed domain responses plus one retained unassessed LinkedIn host load failure. Its one fresh unchanged retry passes; no answer hints or duplicate blog submissions after browser control reset.
- [x] Independently count drafts/variants (388/440/219/193/201 words), compare exact supplied code, inspect the synthetic preview and reconcile actual FITS headers/all three returned member hashes. Record four bounded passes and two source-grounding failures in the [assessment](../../evaluations/native-batch5-2026-10-21.md). No candidate changes.
- [x] Candidate chronology/hashtag corrections implemented and affected native tests rerun. LinkedIn passes. The intermediate blog timing failure and subsequent host failures remain retained; the unchanged final blog passes bounded verification in native-batch13 on 2026-10-22. Separate human acceptance remains open.
- [x] Complete clean tracked-byte validation: 108 regressions, generator drift, repository/PowerShell quality (46 skills, zero issues), exact-case folders and 24 offline cases/99 negative checks pass. Deliver seven review/tracking files through draft PR #11; hosted checks are tracked on the delivery commit.
- [ ] Obtain separate bounded acceptance after reviewing this batch and its failed outputs. Keep workout initial delivery, broader hosts/models/routing, real astronomy processing and all earlier gates open. No merging, installation or promotion.


## Fifth-batch writing correction continuation

- [x] Correct supported-source requirements for blog titles/openers/main first-person chronology and LinkedIn technology hashtags. Record three exact original-source transformations and regenerate only existing allowed candidates/provenance; preserve shipped source/package bytes and placement.
- [x] Rerun unchanged original task/source packets with only candidate instructions replaced. Retain the 446-word intermediate blog failure; verify the 222-word LinkedIn native Copy and supported topic hashtags. See the [repair review](../../evaluations/native-batch5-grounding-repairs-2026-10-21.md).
- [x] Attempt final blog verification twice in Instant and once separately in Medium. Retain all three response-load failures as unassessed, preserve exact input pins, stop bounded retries and restore Instant. No host failure or static check is a native pass.
- [x] Run all 108 regressions on both candidate revisions and final generator drift. Retain identical pre-existing version-frontmatter rejection in four baseline/corrected generic-validator pairs; intended-target checks remain separate.
- [x] Complete final clean-snapshot repository/PowerShell quality (46 skills, zero issues), exact-case folders (35 skills), and 24 offline cases/99 negative checks. Deliver candidate corrections, exact provenance and retained native evidence through draft PR #11; hosted checks tracked on the delivery commit.
- [x] Verify final blog source fidelity/format against an assessable unchanged native response in native-batch13 on 2026-10-22. Earlier failures remain unchanged.
- [ ] Obtain separate bounded blog human review. Workout initial delivery and all other unresolved gates remain open. No merge, install or promotion.

- [x] Rerun the unchanged final blog candidate in two fresh Instant chats with identical packet/resource hashes. Retain both blank completed responses as unassessed delivery failures; no draft is available and final verification remains open.
- [x] Check hosted CI on a51fd90: all five workflows completed successfully; eleven checks succeeded and helpers retains inconsistent in-progress status despite successful workflow/steps. PR remains draft and workout initial delivery remains open.

## Sixth targeted native batch

- [x] Check CI on 20ee994: all five workflows and all twelve individual checks completed successfully. Keep blog verification and workout initial delivery open; PR stays draft.
- [x] Select facebook-post, x-post and proxmox-lxc without prior targeted native records. Pin six synthetic cases and exact existing candidate hashes before execution; keep criteria outside uploads and infrastructure work as proposals only.
- [x] Execute three authenticated Instant primary cases. Retain a Facebook standard-format failure, a passing cross-platform bundle with a 219-character X body, and one unassessed X host response-load failure. See the [assessment](../../evaluations/native-batch6-2026-10-21.md).
- [x] Restore ChatGPT sign-in and execute the three unsubmitted cases plus one fresh unchanged X retry. Both Proxmox plans pass bounded review; X one-liner is 166 versus reported 162 and exceeds under140, while X-count is 232 versus reported 228. Keep original host failure unassessed; signed-out tabs add no executions.
- [x] Correct Facebook paragraph counting/final format checks, retain an intermediate runtime-review scope failure, then preserve diff-review scope explicitly. Fresh unchanged final retry passes two-paragraph/source checks; retain its primary host failure as unassessed. See the [repair assessment](../../evaluations/native-batch6-repairs-2026-10-21.md).
- [x] Correct final X measurement/recount and selected-preset rules. Both original native tasks pass exact Copy/rendered counts at 234 and 136; one-liner is below140. Original failures and external criteria remain unchanged; actual provider counter execution remains unaudited.
- [x] Consolidate all six cases: seven attempts, six completed responses, three bounded passes, three formatting/count failures and one unassessed host failure. No candidate changes. On 481d9fe all twelve checks pass; master-generation workflow summary remains running despite its successful job/steps.
- [x] Mick explicitly accepted the bounded sixth-batch results, including final repair reruns and retained failure limits, on 2026-10-21 and authorized the next untested native batch. Earlier failed/unassessed outputs remain unchanged. Blog verification, workout initial delivery, broader native coverage and all promotion gates remain open. No merge, installation or promotion.

- [x] Validate both writing correction revisions with 108 regressions each. Final generator drift (805 files), repository/PowerShell quality (46 skills, zero issues), exact-case folders (35 skills) and 24 offline cases/99 negative checks pass. Retain identical pre-existing version-frontmatter rejection in four baseline/corrected schema pairs. Keep acceptance and earlier open gates separate.

## Seventh targeted native batch

- [x] Check CI on 5d2c453: all five workflows and twelve individual checks passed; PR remains draft. Sixth-batch acceptance does not close blog verification or workout initial delivery.
- [x] Select n8n-workflow, pihole-blocklist and container-home without prior targeted native records. Pin six fabricated cases, exact existing candidate resources and criteria outside uploads. Keep operations as offline source review and proposals only.
- [x] Execute six fresh Instant Temporary chats without retries. Verify complete native copies, exact 3.55/5 rubric arithmetic, 100=70+30 domains and 12-2=10 trim inventory. Retain three bounded passes, two n8n policy/test-matrix inconsistencies and one home source-scope failure. See the [assessment](../../evaluations/native-batch7-2026-10-21.md).
- [x] Correct n8n retry-policy/test consistency and rerun both original native cases. The design now gives the lost-response case one attempt/no retry. Existing-workflow review returns two Instant and one separate Medium host failures; keep those unassessed and restore Instant. See the [repair assessment](../../evaluations/native-batch7-repairs-2026-10-21.md).
- [x] Correct fictional/alternate-project isolation and aligned constraints/checklist in container-home. Its unchanged fresh Instant retry preserves supplied data/gates and omits historical location, retirement/solo history and extra structures; retain its primary host failure.
- [x] Verify corrected n8n existing-workflow review against an assessable unchanged Instant response in native-batch13 on 2026-10-22. Original policy failures and unassessed attempts remain unchanged; no engine execution certified.
- [ ] Obtain separate bounded seventh-batch acceptance after reviewing retained failures. Keep blog verification, workout initial delivery, broader native coverage and all promotion gates open. No merge, installation or promotion.

- [x] Validate the unchanged-candidate evidence overlay in a clean tracked snapshot: repository/PowerShell quality (46 skills, zero issues), exact-case folders (35 skills), generator drift and 24 offline cases/99 negative checks pass. Deliver only nine review/tracking files through draft PR #11.

- [x] Validate seventh-batch candidate repairs: 108 regressions, generator drift for 805 files, repository/PowerShell quality (46 skills, zero issues), exact-case folders (35 skills), and 24 offline cases/99 negative checks pass. Codex n8n generic schema passes; four master/ChatGPT pairs retain identical pre-existing version rejection. Keep native verification/acceptance and earlier gates separate.

- [x] Rerun the remaining n8n review against unchanged candidate/task/source/wrapper/criteria at e4cbe18 in one fresh Instant Temporary chat. Retain another unassessed response-load failure; verification and acceptance remain open. Confirm all five workflows and twelve individual CI checks passed on e4cbe18. Keep blog verification and workout initial delivery open; PR stays draft without merging or promotion.

## Eighth targeted native batch

- [x] Check CI on 3e4682b: all five workflows and twelve individual checks passed. Preserve n8n workflow-review verification, blog verification, workout initial delivery and seventh-batch acceptance as open gates; PR stays draft.
- [x] Select fitness-log, fitness-programming and food-analyzer without prior targeted native records. Pin six fabricated text cases, exact candidate resources and packet hashes before submission. Keep external criteria outside uploads and real health/tracker actions out of scope.
- [x] Execute six fresh Instant Temporary chats plus one unchanged missing-image retry. Five assessable responses pass bounded source/arithmetic/planning checks. Retain both blank completed responses and zero-byte copies as unassessed, not content passes. See the [assessment](../../evaluations/native-batch8-2026-10-21.md).
- [x] Independently verify candidate/packet hashes, actual dashboard/food-log YAML parsing, 3/4 sessions,105minutes,27reps, strict-versus-assisted boundaries,37/36minute session totals, single-variable adjustment and food scaling/daily values. Preserve whole-response Copy flattening separately from the working dashboard Copy.
- [x] Validate the six-file evidence overlay in a clean tracked snapshot: repository/PowerShell quality (46 skills, zero issues), exact-case Claude folders (35 skills, zero issues), generator drift and 24 offline cases/99 negative checks pass. Full regressions remain covered by passing source CI; no candidate changes. Delivery CI is tracked separately.
- [ ] Verify food-analyzer missing-image behavior against an assessable response using unchanged inputs. No image-recognition, medication-interaction or real training-suitability claim.
- [ ] Obtain separate bounded eighth-batch acceptance. Keep all earlier open gates, broader hosts/models/routing and promotion gates open. No merging, installation or promotion.

- [x] Rerun food-analyzer missing-image verification once in a fresh Instant Temporary chat at e466a54 with unchanged candidate/task/source/wrapper/criteria and packet bytes. Retain the initially blank state and settled host response-load failure with exact Copy/evidence hashes. No assessable food response; verification and acceptance remain open. All five workflows/twelve checks passed on e466a54. Keep n8n/blog verification and workout initial delivery open; PR stays draft without merging or promotion.

## Ninth targeted native batch

- [x] Check CI on b6c2fe9: all five workflows and twelve individual checks passed. Keep food-analyzer, n8n and blog verification and workout initial delivery open. No seventh/eighth acceptance inferred; PR stays draft.
- [x] Select market-brief, crypto-listings and crypto-research without prior targeted native records. Pin six fabricated offline source-review/missing-live-data cases and unchanged candidate resources before submission. Keep rubrics outside uploads, financial accounts/orders and current external retrieval out of scope.
- [x] Execute six fresh Instant Temporary chats plus one identical ambiguous-token retry. Retain five bounded passes, one listings date-window failure and one unassessed primary host failure. See the [assessment](../../evaluations/native-batch9-2026-10-21.md).
- [x] Independently verify all input/resource pins, exact follow-up, quote-change math, UTC half-open boundary memberships, duplicate/venue counts and supply ratios. Preserve native output and unknown risk fields; do not convert host failures or partial screens to passes.
- [x] Validate the six-file evidence overlay in a clean tracked snapshot: repository/PowerShell quality (46 skills, zero issues), exact-case Claude folders (35 skills, zero issues), generator drift and 24 offline cases/99 negative checks pass. Source CI covers full regressions; delivery CI tracked separately.
- [x] Correct crypto-listings missing-anchor fallback/checklist with exact provenance and rerun the original scenario. Two corrected-candidate host failures remain unassessed; the later unchanged Instant continuation passes all three original criteria after sign-in. Preserve the original failed output and criteria. See the [correction review](../../evaluations/native-batch9-window-repair-2026-10-21.md). Separate human acceptance and live retrieval remain open.
- [ ] Obtain separate bounded ninth-batch human review. Keep actual live retrieval, broader hosts/models/routing, earlier verification/delivery and all promotion gates open. No merging, installation or promotion.

## Crypto-listings UTC-window correction

- [x] Correct the master workflow and checklist with two exact source transformations. Require an exact timestamp/timezone before deriving windows, filters and counts; otherwise leave them unestablished. Preserve current-source verification as a separate requirement and regenerate only existing Claude/ChatGPT review targets.
- [x] Pin the corrected candidate and prove packet reversal restores the original bytes. Original task/source/wrapper/external criteria and capability bytes remain unchanged; criteria stay outside uploads.
- [x] Rerun the original missing-live-data case in a fresh Instant Temporary chat and one identical fresh retry. Retain both host response-load failures as unassessed; no regeneration, mode change or feedback. Original failure stays failed.
- [x] Validate the corrected candidate in a clean tracked snapshot: 108 regressions, generator drift for 805 files, repository/PowerShell quality (46 skills, zero issues), exact-case Claude folders (35 skills) and 24 offline cases/99 negative checks pass. Master/ChatGPT generic validator pairs retain identical pre-existing version rejection. Source CI on 6b2973f passes all five workflows/twelve checks; delivery CI tracked separately.
- [x] Verify the unchanged corrected crypto-listings native fallback after sign-in in Instant Temporary chat. The anchor and both UTC windows remain Not established; counts unavailable, not zero. TOKENZ stays a Notes rumor and requests for timestamped official sources remain explicit. All original criteria score 2/2/2; candidate/task/source/wrapper/criteria/packet bytes unchanged. Source CI on 7af1216 passes all five workflows/twelve checks. Earlier failed/unassessed responses stay intact.
- [x] Record Mick's bounded crypto-listings acceptance only. Retain original failed/unassessed results; supplied-source and corrected fallback acceptance does not close live retrieval, broader ninth-batch or other acceptance gates. Food-analyzer, n8n and blog verification and workout initial delivery stay open. No merge, installation or promotion.

## Tenth targeted native batch

- [x] Verify all five workflows/twelve checks pass on 95a8bd5; record bounded crypto-listings acceptance only.
- [x] Pin six synthetic cases for previously untested alpaca-trading, patentforge-provisional and trip-email-html-itinerary. Keep external rubrics outside uploads and all actual broker/legal/travel actions out of scope.
- [x] Execute six fresh Instant Temporary chats plus two unchanged itinerary host retries. Retain two bounded passes, two partial responses, one incomplete package and three unassessed host failures. See the [assessment](../../evaluations/native-batch10-2026-10-21.md).
- [x] Independently verify inputs/resources/retry equality, patent section cutoff, proposed test count and intake redaction. Clean tracked overlay passes repository validation (46 skills, zero issues), generator drift and 24 offline cases/99 negative checks. Preserve exact raw evidence privately; candidates unchanged.
- [x] Address explicit remaining-fill and Spec-context coverage; both original Alpaca native cases pass 2/2/2 with exact original task/source/criteria. Proposed tests remain unexecuted.
- [ ] Establish complete 14-section patent package delivery with upfront required boundaries and confidentiality flag/replacement review; rerun the original case without changing task/source/criteria.
- [x] Obtain an assessable unchanged trip HTML-fragment native review (2/2/2), with independent static fragment checks. Retain minor priority-badge discrepancy; full artifact generation/rendering remains outside this batch.
- [ ] Obtain separate bounded tenth-batch human review. Keep food-analyzer, n8n and blog verification, workout initial delivery, earlier unaccepted scopes and all promotion gates open. PR stays draft; no merge, installation or promotion.

## Tenth-batch correction validation

- [x] Record three exact candidate transformations and regenerate only existing allowed review targets. Preserve shipped packages, versions, original source hashes, capabilities and promotion/placement metadata.
- [x] Preserve all original and intermediate outputs and pin every revision/retry separately. See the [correction assessment](../../evaluations/native-batch10-repairs-2026-10-21.md).
- [x] Validate the final correction in a clean tracked snapshot: 108 regressions, repository/PowerShell quality 46 skills/zero issues, folders 35 skills, generator 805 files and offline 24 cases/99 negative checks. Generic version-frontmatter limitation remains unchanged. Baseline CI on 9e926ee passes five workflows/twelve checks; delivery CI separate.
- [ ] Verify complete native delivery of the final plain-Markdown patent package. Bounded host retries exhausted; do not mark failed/unassessed outputs passed.
- [ ] Obtain separate bounded human review. Food-analyzer, n8n and blog verification and workout initial delivery remain open. Keep PR draft; no merge, installation or promotion.

- [x] Run one unchanged final patent continuation after Mick reported connection readiness. The unchanged final patent continuation again returns a host response-load error and remains unassessed. Patent verification stays open; no further retry. CI on 9b14219 passes all five workflows/twelve checks.

## Eleventh targeted native batch

- [x] Verify all five workflows/twelve checks pass on 59a69d4. Keep patent/food/n8n/blog verification and workout initial delivery open; no earlier acceptance inferred.
- [x] Select the foundation trio with prior CLI/tool/Linux coverage but no targeted ChatGPT native packet records. Pin six synthetic tasks/sources/candidates and keep external criteria outside uploads.
- [x] Run six fresh Instant Temporary chats plus one identical architect-security retry. Five bounded passes and two unassessed host errors retained. See the [assessment](../../evaluations/native-batch11-2026-10-21.md).
- [x] Independently verify all pins, README artifact license placement, naming-only diff/count and local toy PowerShell arithmetic/pipeline/WhatIf/Confirm behavior. Native analyzer/tests remain unexecuted; no real removal or infrastructure action.
- [x] Obtain an assessable Repository Architect native security-prerequisite response against the unchanged candidate and original case in native-batch13 on 2026-10-22. Original host failures remain unassessed; close only bounded clarification verification.
- [ ] Obtain separate bounded eleventh-batch human review. Keep patent/food/n8n/blog verification, workout initial delivery, earlier unaccepted scopes and all promotion gates open. PR remains draft; no merge, installation or promotion.
- [x] Validate the clean tracked evidence overlay: repository 46 skills/zero issues, generator drift and offline 24 cases/99 negative checks pass; zero offline model evaluations. Delivery CI checked separately.

- [x] Rerun the unchanged architect security case once in a fresh Instant Temporary chat. The unchanged architect security-prerequisite continuation returns another host response-load error and remains unassessed. Verification stays open; no further retry. All five CI workflows/twelve checks pass on 6e6d0ca; patent/food/n8n/blog verification and workout initial delivery remain open.

## Consolidated coverage, delivery diagnostic and example-skill

- [x] Consolidate one 36-row [native coverage/acceptance matrix](../../evaluations/native-coverage-2026-10-21.md) with machine-readable current instruction/evidence pins, thirteen scoped native acceptances and 23 pending native reviews. Preserve historical failures and later acceptance scope without rewriting fixtures or granting promotion.
- [x] Run the pre-pinned four-cell inline/upload short/full-packet diagnostic, one attempt per cell without retries. Inline canary and both full-packet cells complete; short upload fails to load. Restore long inline text from automatic pasted-attachment conversion before Send. Neutral diagnostic wrapper differs from the official wrapper; no causal root cause or gate closure claimed.
- [x] Run both example-skill cases with unchanged candidate instructions. Three-step plan/verification passes 2/2/2; missing-objective case returns a host response-load error and remains unassessed. No retry or false acceptance.
- [x] Verify all five source CI workflows and twelve checks pass on d6a3949. Keep all six existing architect/patent/food/n8n/blog/workout verification or delivery issues open; no candidate, placement, merge, installation or promotion change.
- [x] Obtain an assessable unchanged example-skill missing-objective native response in native-batch13 on 2026-10-22. Original host failure remains unassessed; diagnostic successes alone close no official gate.
- [ ] Review pending bounded native acceptance scopes separately. Do not infer acceptance from this matrix or diagnostic work.
- [x] Validate the clean tracked eight-file matrix/evidence overlay: repository 46 skills/zero issues, generator drift and offline 24 cases/99 negative checks pass. Independently confirm 36 unique rows, 13 scoped acceptances/23 pending reviews and zero promotions; delivery CI separate.

## Controlled delivery comparison and seven-path assessment

- [x] Verify all twelve CI checks pass on ab06c0b and PR #11 remains draft.
- [x] Pin fixed architect packet/upload/Instant conditions and original/neutral/neutral/original wrappers. All four diagnostic responses complete; no cause or repeated reliability established. Preserve timed-out-click readback and authentication interruption without resubmission.
- [x] Pin and rerun all seven original cases without candidate changes, feedback, regeneration or retries. Preserve workout's original Medium/files wrapper and two uploads; other cases use Instant. See the [assessment](../../evaluations/native-batch13-2026-10-22.md).
- [x] Independently assess complete responses and close only bounded architect security, n8n existing-workflow review, blog final draft and example missing-objective verification. Original failures remain unchanged; no human acceptance inferred.
- [ ] Resolve patent delivery word limits: all 14 sections now arrive, but total 1409 and section10 prose 342 exceed 1200/300.
- [ ] Resolve food missing-image response scope: grounding works, but 296-word report does not meet concise clarification criterion.
- [ ] Resolve workout initial native Copy boundary: correct first-response note arrives, but exact 325-byte Copy starts with a blank line and fails validation. No normalization or recovery counted as a pass.
- [x] Review all 23 pending native acceptance scopes with current instruction/evidence hash equality. Recommend 21 bounded scopes for human review and hold two incomplete scopes. Preserve 13 earlier acceptances; grant none new.
- [ ] Obtain explicit scoped human acceptance; no merging, installation or promotion.
- [x] Validate the clean tracked evidence overlay: repository 46/zero issues, generator drift and offline 24/99 pass. Source CI on ab06c0b passes all 12 checks. Delivery CI tracked separately.
- [x] Prepare concise PR review summary and retained-evidence links for publication with this delivery; keep PR draft.


## Patent, food and workout delivery repairs

- [x] Add read-only patent 14-section/word-limit validation and exact workout inline serialization with meaningful boundary regressions. Keep source hashes, versions, capabilities, placement and shipped packages unchanged; regenerate only existing review targets.
- [x] Pin every revision and retain intermediate failures. Final patent package passes 1114/1200 total and 289/300 in section 10; food missing-image intake is two concise sentences. See the [assessment](../../evaluations/native-batch14-2026-10-22.md).
- [x] Finish workout initial, duplicate and authorized correction native checks. Initial/corrected Copy each 290 exact bytes, byte-zero frontmatter, unchanged validator pass; duplicate asks overwrite/skip; corrected row with four sets preserves all other source data.
- [x] Consolidate exact inputs/resources/Copy/UI hashes and current review recommendations without accepting new revisions or rewriting historical fixtures.
- [x] Complete final-byte food supplied-label control. Later readback proves the original submission completed without resend; arithmetic and source boundaries pass.
- [x] Run pinned final-byte patent interview control. One substantive mechanism question and all five boundaries pass. V1 controls remain historical only.
- [ ] Obtain separate human review of repaired scopes. Keep repeated reliability, actual integrations, provider traces, other hosts/models/routing and all promotion gates open. PR stays draft; no merge or promotion.

- [x] Final clean tracked validation passes all 117 regressions, repository 46 skills/zero issues, generator 807 files and offline 24 cases/99 negative checks. Source CI 12 checks green; delivery CI tracked against new commit.


## Pending-scope review and unchanged native repeats

- [x] Review all 23 pending scopes against original criteria, retained outcomes and current resources. Preserve 13 historical accepted scopes and all 23 pending human reviews. No new acceptance.
- [x] Identify four historical-pass controls not repeated after instruction/helper changes: blog how-to, home update, LinkedIn variants and preview README fallback. Hold their complete current sampled scopes; recorded subsets remain reviewable. See the [assessment](../../evaluations/native-batch15-2026-10-22.md).
- [x] Pin and execute five unchanged final-case repeats with original modes/transport/wrappers and no feedback/regeneration. Patent 1140/290 and food/control cases pass; workout content and duplicate/correction semantics pass but initial/corrected Copy each 332 bytes fail byte-zero frontmatter.
- [ ] Correct and verify reliable workout initial/corrected native Copy delivery. Reopened by batch15; do not substitute trimming or prior passing copies.
- [ ] Run the four original current-resource controls and inspect actual preview JPEG. Keep original inputs/criteria unchanged.
- [ ] Obtain human review of pending scopes and the repaired workout revision. Keep real integrations, routing/hosts/models, provider traces, repeatability and promotion gates open. PR remains draft; no merge or promotion.

- [x] Final evidence-overlay validation passes repository46/zero issues, generator807files, offline24cases/99negative checks, exact pins and actual food-log YAML. All12 source CI checks pass; delivery CI checked separately.
