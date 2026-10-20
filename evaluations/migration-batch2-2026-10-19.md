# Second migration batch, 2026-10-19

Mick authorized six bounded synthetic cases for `spec-writer`, `pihole-csv-analyzer` and `photo-rename`. This assessment is separate from the accepted foundation results. PR #11 remains draft; no merge, installation, promotion or ecosystem placement change is authorized.

## Inputs and isolation

The [fixture](fixtures/migration-batch2.json) records task inputs, assessment criteria, source commit and candidate hashes. Instructions are pinned to `9174be155d47b65fffc5ec004c9318ede55b2bd2`. Each session gets only its selected generated candidate, capability contract, task and synthetic workspace. Assessment criteria and previous outcomes remain outside the agent context.

`spec-writer` and `pihole-csv-analyzer` use their generated Codex candidates. `photo-rename` has approved candidate placements only for ChatGPT and Claude. Its generated ChatGPT instructions are forced through the CLI as a behavioral proxy. These runs cannot certify native ChatGPT/Claude tools, image handling or routing, and do not approve a Codex placement.

The runner uses the existing signed-in Codex CLI account, requested `gpt-6.1-sol`, medium reasoning, a separate process-local profile, fixed base instructions and fresh ephemeral workspaces. Complete initial client contexts are audited before each inference; only workspace-path differences are normalized when comparing infrastructure. Provider-owned hidden context and an unreported backend model snapshot are not claimed. No original/control comparison or repeated sampling is included.

Shell/file tools are enabled, with network access configured off. App integrations, plugins, delegation, memory consumption/generation and unrelated skills are disabled. A real write/read canary gates domain sessions. Photos are deterministic local drawings with no EXIF, not personal photos. DNS data uses reserved example names and a documentation IPv6 address; no live Pi-hole or external lookup is available.

All profile and evidence directories were created in local AppData outside the repository and sync roots before provisioning the temporary login copy. The copy receives the original credential ACL and is removed in the outer `finally` block. Shared account/profile configuration is not changed. This protocol follows the [official non-interactive guidance](https://learn.chatgpt.com/docs/non-interactive-mode) and the repository's [isolation protocol](model-runner-setup.md#replacement-run-isolation).

## Results

All six scenarios passed bounded assistant assessment. Seven domain responses were captured: the original six plus a fresh explicit-image preview rerun. Use the rerun for the visual assessment; the first preview's file-preservation checks passed, but its event log does not establish image delivery. One shell/file canary also completed. Human acceptance is pending.

| Case | Result and independent evidence |
| --- | --- |
| `spec-new` | Created only the three planning files under `011-queue-dry-run`; preserved existing specs and source. Draft state, date, feature variant, sized unchecked tasks and measurable compatibility criteria are present. The plan identifies the minimal existing implementation and leaves unsupported operation/API choices explicit. |
| `spec-existing` | Updated only the three existing `007-retry-queue` documents; corrected the false done state to draft, created no duplicate and changed no implementation. Bounded attempts, narrow exception handling, iteration behavior and validation are concrete. Proposed defaults are labeled assumptions and require confirmation before implementation. |
| `csv-mixed` | Independent row aggregation matches the report: 12 queries, 5 allowed, 5 blocked, 2 unknown; clients have 6/4/2 queries. `portal.example` has 3 allowed and `ads.example` 3 blocked. Unknown `99` and blank statuses remain unknown. Percentages distinguish all rows from classified rows. Both candidate files contain comments only; no unsupported device identity, breakage or policy claims. |
| `csv-incomplete` | Correctly reports 2 status-less query rows without inventing allowance/blocking. Separately ranks valid aggregate counts 5 and 3, excludes `oops` and labels 8 as a partial subtotal. Does not add exports together. Creates separate comment-only candidate pairs for each export. |
| `photo-preview-attached` | All three initial PNG attachments exactly match fixture bytes. Proposes consistent `red_mug_01.png` and `red_mug_02.png`; gives the gray image an unidentified fallback. Correctly omits unsupported place, event and capture date, and distinguishes subject confidence from location certainty. Creates only the report; original paths and hashes are unchanged. |
| `photo-copy` | Runs a PowerShell copy workflow for the approved mapping. Creates `red_mug_01.png` and `red_mug_02.png`, skips the third image, preserves all originals and the pre-existing `red_mug.png`, and records the actual mapping. Independent hashes match each copy to its source. A separately reviewed replay passes; repeat execution exits 1 because the report exists and changes no files. |

Supplied files and final capture manifests were independently hash-checked in all seven domain workspaces. Only the existing-spec case changes supplied files, limited to its three authorized planning documents. Generated planning and narrative outputs were read and assessed separately from file checks; no wording-only test is presented as evidence of semantic quality.

## Intermediate failures and harness correction

- The first setup attempt assumed a Codex photo bundle and stopped before credentials or model calls when that file was absent. The corrected setup selects the existing ChatGPT candidate without changing suitability maps.
- The incomplete CSV session's first calculation used incorrect PowerShell header access and emitted nonterminating errors despite exit 0. The agent corrected its calculation before delivering the accurate final report. The failed intermediate output remains in the trace.
- The first photo preview's Python launcher was unavailable. It used local PowerShell/.NET for dimensions and PNG metadata instead. Correct-looking names alone were insufficient evidence of visual input, so that capture is retained but excluded from the visual conclusion.
- An audit-only explicit-image render revealed that the variadic image flag consumed the comma-containing task text as extra image paths. No inference ran from that render. The corrected invocation places `--` before the task/stdin argument and audits the exact prompt, image path markers and decoded image bytes before inference. A clean input passed and five mutations were rejected: wrong pixels, outside path marker, missing image, altered task and extra content.
- Offline generator/self-test invocations initially failed because the sandbox denied uv cache writes. The same checks passed after approved access to the existing offline cache. This is an environment failure, not a skill result.

No remaining demonstrated defect justifies changing the master instructions. No master, generated bundle, ecosystem map, model profile or shipped skill was modified.

## Provenance and review

The requested runtime was Codex CLI `0.163.0-alpha.10.2`, `gpt-6.1-sol`, medium reasoning. All inference contexts share normalized client-infrastructure SHA256 `bb6f60b94cd0f540df53e53868f644027f45bc16b910207e5face85ef521ddc3`. Attachment hashes and generated candidate hashes are recorded in the fixture. Raw contexts, events, final outputs, manifests, independent results, the rejected attachment render and a human review packet remain private in local non-synced evaluation storage.

Temporary login copies were removed after both the main batch and attachment work. The main batch verified the original credential hash unchanged. No credentials entered the checkout. This batch does not resolve the historical foundation run's unverified OneDrive sync limitation.

## Repository validation

- All 72 Python unit tests passed in a clean Git-byte snapshot on Windows with Python 3.12.
- Generator drift check passed without regeneration; the offline fixture self-test passed 24 cases and 99 negative checks without model calls.
- All 22 installer regressions passed using temporary test libraries, not installed user skills.
- Final repository/documentation and PowerShell quality checks passed: 46 shipped skills with zero issues. Exact-case folder checks passed for 35 Claude skills with zero issues. Validation used a clean Git-byte snapshot with only the intended documentation/fixture overlay.

## Remaining scope

Human review must assess these actual planning/report/copy artifacts before accepting the batch. Native ChatGPT/Claude photo execution, real travel photos/EXIF/GPS, online research, larger datasets, natural routing, repeated trials, other models and cross-platform execution remain untested here. This is a Windows CLI behavioral proxy for the photo candidate and bounded CLI tool evidence for the two Codex candidates. It is not broad host certification or permission to merge or promote anything.
