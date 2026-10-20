# Foundation tool workflow assessment

Status: **four fresh cases passed bounded assistant review; human acceptance pending**. PR #11 remains draft. No skill or model profile was installed or promoted. Synthetic project installs stayed inside evaluation environments. Testing has not expanded to the remaining migrated skills.

## Scope and isolation

The [tool workflow fixture](fixtures/foundation-tool-workflows.json), revision 2, defines four cases: a fresh architect scaffold, PowerShell deduplication, PowerShell naming-only cleanup and a different README repository. These are fresh sessions with real file and shell tools, not replays of the earlier model outputs. Each case ran once with the generated Codex candidate from commit `5c0fa9364200c1a48348a809f7533fb4d70bedc8`.

Codex CLI 0.163.0-alpha.10.2 requested `gpt-6.1-sol` with medium reasoning. The backend snapshot and temperature were not reported. A separate profile, fixed base instructions, disabled memory/apps/plugins/delegation/web search, an empty skill catalog and per-call rendered-context audits were used. The candidate source bytes match the pinned commit. All four client contexts match after normalizing only the workspace paths, including XML-escaped paths. Provider-owned system context is not observable and is not claimed to have been audited.

Before evaluation, a canary created and read back a file using a real shell tool. The cases then used the native Windows MXC workspace sandbox with network access configured off, preprovisioned tools and offline project installs. The agent received only its task, selected skill, capability contract, tool availability and synthetic source repository. The independent baseline snapshots and assessment criteria stayed outside its workspace. Shared global instructions/configuration were not changed. The temporary login copy was removed after capture; full responses, traces, final projects and review diffs remain in an ignored local evaluation folder, outside published Git artifacts.

The CLI controls follow the [official non-interactive reference](https://learn.chatgpt.com/docs/non-interactive-mode) and [Windows sandbox documentation](https://learn.chatgpt.com/docs/windows/windows-sandbox). This is forced skill activation on one Windows host, not natural routing or broad host/model certification.

## Results

| Case | Agent execution | Independent assessment |
| --- | --- | --- |
| Architect, fresh scaffold | Created actual package, console entry point, CI, templates, README and development prompts. Applied Ruff formatting. Corrected five Windows newline test failures and six temporary-directory errors, then passed format/lint gates and all 26 pytest cases. | 31 command checks passed: final format/lint/tests, eight inputs through file/implicit stdin/explicit `-`, three error paths and console help. Final Python source hashes match the delivered snapshot. Required scaffold files exist. |
| PowerShell, deduplication | Consolidated the secondary probe into the existing primary retry loop; preserved public names and safety code. Original four tests passed; expanded seven-test suite passed before and after refactoring. One added-test binding mistake was corrected. | Seven final Pester tests passed. Exports, parameter metadata and 19 baseline probe groups match. Custom-settings analyzer findings remain 0 before/after. Caller, analyzer settings and tool/capability files are unchanged. |
| PowerShell, naming only | Renamed only the internal local variable. Kept both branches, duplicate output and interactive stream behavior. Two tests passed before/after. Reported the existing warning and its preservation reason. | Two final Pester tests passed. Exports, parameter metadata and seven baseline probe groups match. The one `PSAvoidUsingWriteHost` warning remains unchanged, with zero new findings. Only the module changed among supplied files. |
| README, inventory CSV CLI | Inspected real source and repaired stale setup, flags, environment configuration, tests and license. Offline install, help/examples/environment checks and one pytest smoke test passed. Accurately reported a temporary-directory install failure and local workaround. | All seven documented PowerShell code blocks and eight independent CLI probes passed. Only README.md changed among supplied source files. Application, tests, manifest, examples and license bytes remain unchanged. Local-data guidance is retained and MIT is last. |

PowerShell runs used version 7.6.7, Pester 5.7.1 and PSScriptAnalyzer 1.25.0. Python runs used 3.12.13, pytest 8.4.2, Ruff 0.16.6, setuptools 84.0.0, pip 26.2.1 and wheel 0.48.0. The naming-only module kept 11 lines; the deduplicated module changed from 27 to 25 lines. No performance improvement is inferred from line counts.

The 26 PowerShell probe groups cover output type/property/order, named/null/omitted/empty pipeline behavior, retry counts at valid limits, final error messages, invalid argument handling, multi-output success, confirmation metadata, duplicate branches and interactive output. Mocked tests verify WhatIf and confirmed removal behavior. No real removal operation was executed. The README probes cover default filtering, JSON, environment defaults, explicit overrides, invalid environment values, unsupported output formats and required arguments.

## Feedback and harness corrections

Initial failures remain in the immutable session traces. The architect agent corrected the newline assertions without changing the intended counting contract, used workspace-local temporary directories and reran all gates against the final files. Its formatter changed a file before the final checks. The README agent also recovered from the native sandbox's default temporary-directory restriction. These environment failures are not evidence of a domain defect; the observed recovery and accurate reporting are part of the tool-workflow evidence.

Before the naming-only model call, fixture preflight found that ScriptAnalyzer exempts `Show-*` functions from the Write-Host rule. The synthetic function was changed to `Write-ReportLabel`, and the intended baseline warning was verified before inference. This produced fixture revision 2; the other case inputs are unchanged. The preliminary zero-warning baseline remains private and is excluded from accepted counts.

The independent PowerShell wrapper initially required exactly the original test count and rejected the agent's larger passing suite. It was corrected to permit additional passing tests, then rerun into a new evidence file. The original baseline snapshots and exported API/probe comparisons were retained. The context comparison also needed XML-escaped workspace-path normalization. Neither correction changes model output or converts a failed model result into a pass.

## Evidence pins

Fixture SHA-256: `4b4435d53074cfd2942be20b4f4031b09ba14a41cdadc351376fe9f300794485`.

Normalized client-infrastructure SHA-256: `682c34a8b3981d690e44f6feafccddc8d6012ca717aaeca7956777fd2536dee1`.

| Case | Session manifest SHA-256 |
| --- | --- |
| Architect | `a48db39ad79123b8d0f6fb4156d648dc5ee8f4b9b2bcc94a99ff092792388702` |
| PowerShell deduplication | `3826796d3412ca1055f79cabe626383339fae96f17ff8346cdc2021b3ea8cabd` |
| PowerShell naming only | `2d28523cc305b399c9225c53d53c2408adc874924d02c57f9c7fe922072b3f2a` |
| README | `4912e6be25e5ff41584e7311752ecbf992a793c122a98415a2495f00b07ce87a` |

Manifests retain the exact input/context/output hashes, command results, file hashes, usage and settings. There were four domain sessions and one canary, with no original/control comparison arm. The four domain sessions completed 28 shell commands in total, including failed intermediate commands. That command count is not a count of unique passing tests.

## Assessment and acceptance

The updated architect delivery rule worked in this fresh case: the agent applied formatting, handled observed failures and checked the final files. PowerShell preserved the broader tested contracts and respected naming-only scope, including an explained remaining analyzer warning. The README agent grounded its repair in inspected source and kept application files unchanged. No additional skill instruction change is supported by these four cases.

A local review packet contains the final README/scaffold files, PowerShell diffs and independent evidence for human review. Mick's acceptance remains pending. Acceptance of this bounded assessment would not authorize merging or promotion.

Remaining limits: one repetition per case; Windows/Python 3.12/PowerShell 7 only for these fresh agents; preprovisioned tooling; no fresh Linux agent session, natural routing, broader repositories, other models/hosts or full comparison matrix. The earlier [Linux artifact replay](foundation-linux-runtime-2026-10-19.md) remains separate evidence. Obtain human acceptance before expanding the migrated-skill test batch.

## Repository validation

All 72 repository regressions passed locally in a Git-byte snapshot with the reviewed changes. Repository/PowerShell quality checked 46 shipped skills with zero issues; exact-case folder validation checked 35 Claude folders with zero issues. Generator drift and the 24-case/99-negative-check offline self-test passed. These offline checks are separate from the four fresh model/tool sessions. Hosted results are recorded in PR #11.
