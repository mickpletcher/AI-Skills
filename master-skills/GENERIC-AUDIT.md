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
