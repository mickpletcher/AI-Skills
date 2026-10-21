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
- [ ] Rerun the duplicate/correction sequence against the unchanged final canonical-file delivery revision when the native host can load a response. Verify actual initial/corrected downloads and Copy bytes. No final-revision duplicate workflow, inline Copy or real Obsidian ingestion pass is claimed.
- [ ] Obtain separate acceptance of the new native batch; no acceptance is inferred from authorization to test.
