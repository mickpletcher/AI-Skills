# Candidate compatibility and helper checks

Mick authorized the Codex frontmatter audit, remaining helper tests and subsequent behavioral testing of untested skills. PR #11 remains draft. Shipped skills/packages, ecosystem suitability and promotion metadata are unchanged. No live scheduler, browser, Apple Notes, infrastructure or publication action is part of these checks.

## Codex frontmatter

The generic validator rejects repository-specific top-level metadata such as `version`. Codex generation now emits only `name` and `description` in its entrypoint YAML. Complete source frontmatter remains unchanged in canonical sources and is recorded in Codex build provenance with policy `codex-name-description-v1`. Other targets retain their headers. Baseline and named-model builds use this policy; suitability is unchanged.

The [official skill guidance](https://learn.chatgpt.com/docs/build-skills) identifies the required name/description contract. This conservative format addresses the demonstrated validator rejection without claiming native runtime certification. Regressions cover all 12 allowed Codex candidates and a named-model fixture, source metadata preservation and unchanged body text.

## Remaining helpers

The durable [runtime checks](fixtures/check_remaining_helpers.py) use synthetic files and disposable directories. Image/FITS parsing runs when dependencies are available. Scheduler, Apple Notes and browser boundaries are mocked. A Windows CI job provisions dependencies and runs the same checks without activating any skill.

Demonstrated corrections:

- Image preview generation collapsed same-named source files into one preview, then processed previews again on repeat runs. Candidates now preserve relative directories and full source filenames, exclude the output tree, refuse existing files, reject outward output links and report invalid sizes/read failures through nonzero exits. Original image bytes remain unchanged.
- FITS auditing now returns nonzero when a file cannot be read instead of printing an error and returning success.
- Resume CSV values are quoted as YAML-compatible JSON strings. The original helper produced invalid frontmatter for `Synthetic: Coach`. Date-shaped review inputs are enforced; existing imported candidate notes remain unchanged on repeat runs.
- Scheduled-task registration supports `-WhatIf`, refuses an existing task and omits `-Force`. Tests replace scheduler cmdlets with local mocks; the real task store is never queried or modified.
- Public-demo HTML uses exclusive creation, and JPEG export refuses existing planned output names before invoking its renderer. Tests verify repeat refusal, preserved existing bytes, validation failure and invalid-JPEG failure with browser calls replaced.

Original shipped helper hashes remain in migration records. Explicit candidate resource overrides record corrected hashes and reasons. Generated resources must match the candidates; no shipped package is rebuilt or replaced.

Image tests inspect actual Pillow output and source preservation. FITS tests use a compressed synthetic image with known header aliases and malformed input. Apple Notes tests cover the non-macOS guard and mocked argument/temp-file handling; no AppleScript executes. Itinerary tests build synthetic public-demo HTML through the actual validator and exercise ten synthetic JPEG results with the browser command replaced. They do not open a local URL, bypass browser restrictions or certify rendering.

Initial local Astropy provisioning failed because the package-file host could not resolve after retries. Local runs explicitly skip real FITS testing when Astropy is absent; the dependency-provisioned hosted job is separate evidence. Failures and skips are not passes.

The generic validator originally rejected eight of the 12 Codex candidates for their `version` field. All 12 corrected entrypoints pass. The 88-test repository suite passed locally. Final helper resource changes are additionally checked by the helper runtime fixture, regeneration/provenance checks and hosted validation. The source-hash inventory and every ecosystem exclusion remain unchanged.

## Behavioral continuation

The nine previously exercised domain skills retain their existing records. The next round targets the other 26 domain skills, including IdeaForge and Proxmox, which have helper/static checks but no behavioral captures. Only allowed generated candidates are used. Conversational candidates tested through CLI are labeled proxies and do not establish Codex placement or native ChatGPT/Claude support.

Runs require an isolated context audit and a canary first. Synthetic prompts, source hashes, settings, captures and independent criteria are retained separately. Live browsing, deployment, account changes, purchases, medical/legal/financial decisions, publication and real note writes remain out of scope. Broader repetition/routing/native-host coverage and human acceptance remain separate.
