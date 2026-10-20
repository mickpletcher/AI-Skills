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
- [ ] Prepare a candidate-only map-validator fix and regression for pending addresses while retaining checks for supported addresses, migration provenance and unchanged shipped skills/packages. No helper change or full batch pass is claimed yet.
- [ ] Complete itinerary visual/phone review in an allowed renderer. Browser policy rejected local file URLs; static checks do not fulfill this gate.
- [ ] Obtain human acceptance of the third batch and bounded native photo result. Keep PR #11 draft; no merging, installation or promotion.
