# Generic-master and suitability audit

Reviewed all 35 domain masters plus the scaffold for assistant-host assumptions. Masters retain goals, inputs/outputs, domain workflows, quality criteria and safeguards. Every master has capabilities.json and ecosystems.json; missing mappings fail generation. Exact provider/model selection belongs to model-profiles, and host tool names belong to adapters. Model profiles cannot override excluded ecosystems.

The eight recorded wording substitutions remove assistant identity/tool assumptions and hard-coded Claude skill paths. Existing foundational masters were already host-neutral; they now have the same capability and placement contracts. Remaining references to Claude/Anthropic in n8n-workflow, linkedin-post and idea-forge are API integration subjects or illustrative domain examples, not required assistant hosts. Historical model attribution and proposed compatibility labels in legacy metadata are provenance, not model requirements or placement decisions. The explicit ecosystems.json allowlist controls generation. Personal preferences remain unchanged source context.

## Unresolved adaptations before promotion

- General-purpose conversational placements (Claude/ChatGPT) still require attachment, browsing, storage and runtime availability checks; they are not blanket compatibility claims.
- Astrophotography, IdeaForge, photo renaming and resume workflows may have useful coding submodes, but their primary workflows do not justify coding-host placement in this batch. They are excluded from Cursor/Codex pending a separate mode-specific design.
- Repository preview generation and HTML itinerary generation have explicit script/template workflows and are proposed for coding hosts, but visual/file tooling and helper prerequisites remain unverified.
- Pi-hole curation is proposed for coding hosts as infrastructure-repository maintenance; review the intended usage mode.
- Apple Notes automation requires macOS permission; itinerary JPG helpers use Windows-oriented tooling; financial/live-source and imaging workflows require evidence unavailable to text-only models. These existing domain dependencies remain documented resources and conditional capabilities, not assumed host features.
- No model-specific workaround is certified. New model profiles are hypotheses requiring baseline/without-skill/with-skill reassessment; unknown future models are not supported by inference.

## Per-skill decisions

| Master | Allowed candidate targets | Skipped-target reason / adaptation |
| --- | --- | --- |
| alpaca-trading | claude, chatgpt, cursor, codex | Verify intended host capabilities and behavior before promotion. |
| astrophotography-processing | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| blog-post | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| blog-to-social | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| container-home | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| crypto-listings | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| crypto-research | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| example-skill | claude, chatgpt, cursor, codex | Verify intended host capabilities and behavior before promotion. |
| facebook-post | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| facebook-reply | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| fitness-log | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| fitness-programming | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| food-analyzer | claude, chatgpt | cursor: Explicit user exclusion: food/photo/nutrition analysis is not their Cursor coding workflow.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| github-readme | claude, chatgpt, cursor, codex | Verify intended host capabilities and behavior before promotion. |
| github-repo-architect | claude, chatgpt, cursor, codex | Verify intended host capabilities and behavior before promotion. |
| github-social-preview | claude, chatgpt, cursor, codex | Review mode-specific placement and helper availability before promotion. |
| idea-forge | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| linkedin-post | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| market-brief | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| n8n-workflow | claude, chatgpt, cursor, codex | Verify intended host capabilities and behavior before promotion. |
| obsidian-workout-export | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| patentforge-provisional | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| photo-rename | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| pihole-blocklist | claude, chatgpt, cursor, codex | Review mode-specific placement and helper availability before promotion. |
| pihole-csv-analyzer | claude, chatgpt, cursor, codex | Verify intended host capabilities and behavior before promotion. |
| powershell-refactor | claude, chatgpt, cursor, codex | Verify intended host capabilities and behavior before promotion. |
| proxmox-lxc | claude, chatgpt, cursor, codex | Verify intended host capabilities and behavior before promotion. |
| resume-writer | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| spec-writer | claude, chatgpt, cursor, codex | Verify intended host capabilities and behavior before promotion. |
| travel-itinerary | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| travel-planning | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| travel-research | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| trip-email-html-itinerary | claude, chatgpt, cursor, codex | Review mode-specific placement and helper availability before promotion. |
| website-content | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| x-post | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |
| x-reply | claude, chatgpt | cursor: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved.; codex: Primary workflow is domain advice, personal content or non-code analysis; no coding-target placement approved. |

## Foundational requirement repair

Compared github-readme, github-repo-architect and powershell-refactor with the original Claude sources pinned to main 1deaab97. Their previous summaries were portable but omitted requirements. Each now has foundation-audit.json recording the source and prior-master hashes, audited source sections, exact inserted requirements and intentional adaptations. Restored scaffold templates, CI and documentation planning, README section and delivery rules, and analyzer acceptance and summary requirements. Original source files remain unchanged. This is a selective portable audit, not a claim of lossless migration or measured behavior.

Reviewed file-access contracts across all 35 domain masters. Seven formerly mandatory declarations are now operation-specific: alpaca-trading, astrophotography-processing, github-readme, github-repo-architect, powershell-refactor, pihole-csv-analyzer and spec-writer. Pasted-input advice/drafts may proceed; actual file inspection, writes and verification still require file access and authorization. Repository numbering, analyzer execution, image analysis and live trading evidence are not inferred from pasted excerpts. Other capability contracts and every ecosystem mapping remain unchanged.

## Focused draft review, 2026-10-19

Reviewed generation and ownership checks, model profiles and capability overlays, proposed ecosystem decisions, and the three foundational masters against their pinned Claude sources. The foundational scaffold/CI, README evidence/delivery, and PowerShell scope/analyzer/safety requirements remain represented. This review is static and does not approve target-host behavior.

Fixed missing parent-path checks for master, adapter, profile, schema and output trees, including Windows junctions. Added preflight rejection of existing destination type conflicts and case-insensitive file/directory name collisions so these failures occur before candidate writes. Regression fixtures cover both generation and check mode, real symlinks and Windows junctions, and portable resource collisions. The generator workflow now declares read-only repository permissions and includes foundational regression changes in its path filter.

Validation used a clean Git snapshot with the reviewed diff. All 66 local Python regressions and six hosted checks passed; see the [migration task checklist](../specs/005-canonical-skill-migration/tasks.md) for commands, counts and CI evidence. Ignored local planning notes, retired local-only skill folders and existing checkout line-ending differences remain untouched and are not migration inputs.

Personal preferences, environment details and domain examples remain preserved source context. They are not newly verified configuration or general-purpose defaults. Review or parameterize them before wider distribution. Host/helper availability, model comparisons and promotion remain outstanding; every candidate stays unreviewed for promotion with behavior evaluation not run. No model calls, installs or promotion are part of this review.

Subsequent behavioral work is tracked separately in the [foundation pilot assessment](../evaluations/foundation-pilot-2026-10-19.md). The replacement run repaired inherited-context contamination and completed 36 text-only comparisons with assistant rubric scores. This does not change the static review above or authorize promotion. Scaffold semantics, execution, routing, broader host coverage and human acceptance remain open.

The [initial runtime phase](../evaluations/foundation-runtime-2026-10-19.md) subsequently pinned scaffold whitespace semantics and exercised synthetic PowerShell, README and architect artifacts on Windows. Counting/tests passed, while one scaffold failed its configured formatting check; a separate format-only repair passed. The original failure remains recorded. Full host/tool/routing coverage and human acceptance remain open, and no candidate or model profile was promoted.

## Linux runtime continuation

The architect master now requires formatter application, final format/lint/test gates and delivery of the validated file contents. All review candidates were regenerated without changing promotion or acceptance metadata. Historical audit provenance is retained with a separately pinned delivery insertion.

The [Linux assessment](../evaluations/foundation-linux-runtime-2026-10-19.md) records passing PowerShell contracts and Python 3.11 through 3.14 artifact replays for all three foundational skills. The original architect formatting failure reproduced, then a one-file unchanged-AST repair passed final gates and delivered-file hash checks. This does not establish independent model/tool behavior or human acceptance.

## Fresh agent tool workflows

Four [fresh tool-enabled cases](../evaluations/foundation-tool-workflows-2026-10-19.md) passed bounded assistant assessment against pinned Codex candidates: a new architect scaffold, PowerShell deduplication and naming-only scope, and a README repair against another synthetic repository. Actual file edits, formatter/test feedback, repository analyzer settings and independent baseline/command checks were exercised. These single-run Windows cases do not establish broader host/model/routing coverage. Mick accepted the bounded results on 2026-10-19. No promotion metadata changed.

## Subsequent batches and candidate corrections

Testing subsequently expanded to six more skills. Mick accepted the six bounded scenarios for spec-writer, pihole-csv-analyzer and photo-rename in the [second batch](../evaluations/migration-batch2-2026-10-19.md). The [third batch](../evaluations/migration-batch3-2026-10-19.md) covers github-social-preview, n8n-workflow and trip-email-html-itinerary; acceptance remains pending. The [native photo record](../evaluations/photo-native-2026-10-19.md) verifies downloaded output bytes with separate host/audit limits and pending acceptance. These records supersede earlier coverage snapshots without changing promotion metadata.

The [itinerary follow-up](../evaluations/itinerary-validator-2026-10-19.md) corrects a candidate helper with explicit override provenance. Both original itineraries pass strict replay. Offline visual review is bounded; native phone verification is deferred at Mick's request and remains open. The [candidate follow-up](../evaluations/candidate-followup-2026-10-19.md) records Obsidian write safeguards, parameterized Proxmox deployment guidance and documentation corrections. Shipped skills/packages and ecosystem placement are unchanged.

The [compatibility/helper continuation](../evaluations/candidate-compatibility-2026-10-19.md) resolves generated Codex header rejection while retaining full canonical metadata in provenance. Hosted helper checks cover real image/FITS processing with mocked app/scheduler/browser boundaries. The [remaining-skill round](../evaluations/migration-batch4-2026-10-20.md) adds 52 captures for the other 26 domain masters and 34 targeted follow-ups. All 35 domain masters now have some bounded captures. Five initial case failures, one fixture limitation, intermediate format gaps and the canary correction remain recorded; four writing candidates received narrow source-preserving corrections. This is not blanket host/model/routing certification or human acceptance. No promotion metadata changed.

Mick subsequently accepted the bounded remaining-skill results on 2026-10-20 and authorized [targeted native testing](../evaluations/native-writing-2026-10-20.md). That continuation tests the four corrected writers in ChatGPT with explicit candidate packets. Acceptance does not cover new native results or change promotion metadata. Candidate corrections preserve original source hashes and ecosystem placement.

Mick then accepted the bounded first native-writing results on 2026-10-20. The [next native batch](../evaluations/native-batch2-2026-10-20.md) tests Pi-hole CSV analysis, resume editing/auditing and social-preview delivery with six cases plus two packaging follow-ups. Actual downloaded files are verified. Three bounded passes and three scoring/attribution/layout failures remain recorded; resume reconciliation/source attribution and preview tag/badge separation require correction. New native acceptance is pending. No candidate resources, shipped skills/packages, placement or promotion metadata changed in this batch.

## Second native batch corrections

The [repair assessment](../evaluations/native-batch2-repairs-2026-10-20.md) records deterministic resume score/source reconciliation, an actual footer geometry regression and four fresh native reruns. Three final cases pass bounded review, with the intermediate JSON format failure retained. Human resume output used the explicit qualitative fallback; native human numeric scoring remains unexercised. Original native failures remain recorded, acceptance is pending and candidates remain unpromoted.

## Native human numeric scoring assessment

[Two fresh native human numeric runs](../evaluations/native-human-numeric-2026-10-20.md) exercise the previously untested delivery path with unchanged candidate resources. Four actual ledgers pass independent arithmetic/source/display checks. The same original scores 54.5 versus 71.4, revealing unstable assessed scope and common-pattern category choices. Numeric delivery is exercised; substantive rubric consistency and acceptance remain open. Prior failures/fallbacks remain recorded. No installation, merging or promotion.

## Fixed resume rubric and native rerun

The [consistency correction](../evaluations/native-scoring-consistency-2026-10-20.md) replaces arbitrary principle selection with seven calculator-owned criteria, fixed source/category mappings and single ownership of missing evidence. Two fresh human numeric runs now score the same original 76.7 and their rewrites 85.0; actual ZIPs, four ledgers, display values and provider log outputs reconcile. One interrupted attempt is unassessed. A strict JSON case passes parsing, calculation and source-injection checks but grants unjustified full structure credit to a resume without headings. That extraction/anchor boundary and separate acceptance remain open. The bounded repeatability observation does not certify general scoring reliability. Candidate provenance is retained; shipped skills, placement and promotion metadata remain unchanged.

## Resume structure boundary correction

The [structure follow-up](../evaluations/native-resume-structure-2026-10-20.md) adds a required quoted heading inventory and explicit 2/MINOR missing_headings state. Ten scoring regressions pass, including the prior sparse audit with and without a heading. The initial native rerun scores structure correctly but edits calculator-owned ledger fields; that failure remains recorded. An explicit immutable-ledger delivery rule and fresh JSON retry pass the exact final check at 55.0, with one structure penalty and unchanged chronology/privacy. Earlier v1 human results remain historical. Acceptance, general extraction reliability and broader host/routing gates remain separate; no shipped skill, placement or promotion changes.
