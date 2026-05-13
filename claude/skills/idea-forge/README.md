# idea-forge

A Claude skill that runs raw ideas through a five-stage R&D pipeline and produces a structured invention plan with scoring, architecture, monetization paths, and an MVP roadmap.

## Source of Truth

Use [SKILL.md](SKILL.md) as the canonical source for this skill. The packaged [idea-forge.skill](idea-forge.skill) file is the Claude-ready export built from it.

## Overview

IdeaForge is a structured invention engine, not a note-taking tool. It takes any raw input — a sentence, a voice note transcript, a half-formed thought — and produces a fully developed engineering and commercialization plan.

It can also treat Apple Notes as a delivery target for the finished analysis when the user asks for that explicitly.
It can also save the finished analysis into an Obsidian `Ideas` folder when the user wants the result stored in a vault.

The pipeline has five stages:

1. **Capture** — classify the idea type and extract the core problem
2. **Interpret** — assess feasibility, commercial viability, patent potential, and competition
3. **Expand** — generate missing features, integrations, business models, AI opportunities, and automation paths
4. **Score** — produce a weighted IdeaForge Score across seven metrics with a verdict
5. **Output** — structured document covering architecture, MVP roadmap, monetization, risks, and future expansion

## How To Use

Start any message with `idea` to activate immediately.

```text
idea [raw idea, rough concept, or messy note]
```

Messy input is fine. Part of the value is finding the real idea inside incomplete input.

---

### Modes

| Mode | Trigger | What runs |
| --- | --- | --- |
| Full Pipeline | `idea [idea]` | All five stages — full output document |
| Quick Assess | `idea quick [idea]` | Stages 1-2 — category, feasibility, commercial check |
| Score Only | `idea score [idea]` | Stages 1 and 4 — scoring table only |
| Expand Only | `idea expand [idea]` | Stages 1 and 3 — expansion without scoring |
| Commercialize | `idea commercialize [idea]` | Business models, monetization paths, and MVP |

---

### Apple Notes Output

This skill can now target Apple Notes for the final analysis.

`macOS`

- Best path for direct save
- Expected flow is generate the analysis, then run `scripts/save_to_apple_notes.py`
- The packaged skill now includes a macOS Apple Notes helper script

`iOS`

- Not a direct write path from the skill runtime itself
- Expected flow is generate the analysis, then pass the title and body into Apple Notes through a Shortcut or share action

`Prompt examples`

```text
idea save to apple notes Build a self hosted intake tool for rough business ideas

idea save this analysis to apple notes folder Startup Ideas A local first AI planner for project scoping
```

If no Apple Notes folder is named, the skill should ask for one or use `IdeaForge` when a default has already been established.

---

### Obsidian Output

This skill can also target an Obsidian `Ideas` folder for the final analysis.

`macOS`

- Best path is direct Markdown write into the vault when the vault path is known
- Expected flow is generate the analysis, then run `scripts/save_to_obsidian.py`
- Alternate path is an Obsidian URL or Shortcut handoff

`iOS`

- Expected flow is generate the analysis, then pass the title and Markdown body into Obsidian through a Shortcut or share action

`Prompt examples`

```text
idea save to obsidian Build a local first project intake system for rough ideas

idea save this analysis to obsidian ideas folder A self hosted invention scoring tool
```

The destination folder defaults to `Ideas`. The vault name or path still needs to be known.

---

### Example Prompts

```text
idea What if Home Assistant could detect behavioral fatigue from inactivity patterns and suggest wellness interventions automatically

idea quick Is there a market for a self-hosted AI writing coach that stores style preferences locally

idea score A PowerShell module that audits Intune device compliance and generates executive-ready PDF reports

idea expand An n8n workflow that monitors recruiter posts on LinkedIn and stages the best ones for review

idea commercialize A Claude skill that turns rough project ideas into complete GitHub repo architectures
```

---

### What You Get Back

Full pipeline output includes:

| Section | Contents |
| --- | --- |
| Idea Summary | One-paragraph plain-language description |
| Core Problem | Specific pain point being solved |
| Proposed Solution | What it does and how |
| IdeaForge Score | Weighted score table with verdict and key signals |
| Technical Analysis | Stack, dependencies, hardest problems |
| AI Opportunities | Named model integrations and where they fit |
| Automation Opportunities | Triggers, autonomous steps, n8n/Home Assistant paths |
| Suggested Architecture | Component layout in plain text |
| Potential APIs and Integrations | Named services with integration angle |
| Privacy and Security Concerns | Specific risks and mitigations |
| Monetization Opportunities | Ranked paths from fastest to most ambitious |
| Patent Potential | Verdict with specific claim or no-claim reasoning |
| MVP Roadmap | Phased build plan — Phase 1 solo-completable in under 30 days |
| GitHub Repository Suggestions | Repo name, description, folder structure |
| Similar Existing Products | Named analogues with differentiators |
| Future Expansion Ideas | 3-5 next-level directions |
| Risk Assessment | Top 3 risks with likelihood and mitigation |
| Long-Term Strategic Value | What this becomes at scale |

When Apple Notes output is requested, the response should also include:

| Section | Contents |
| --- | --- |
| Apple Notes Delivery | Folder name, suggested note title, and platform specific save path |

When Obsidian output is requested, the response should also include:

| Section | Contents |
| --- | --- |
| Obsidian Delivery | Vault, `Ideas` folder, suggested note title, and platform specific save path |

Quick Assess returns sections 1-5 only.
Score Only returns the scoring table.
Expand Only returns sections 6-16.
Commercialize returns sections 1, 11, 12, 13, 17.

---

## Core Files

- [SKILL.md](SKILL.md): triggers, pipeline stages, mode definitions, constraints
- [scoring-model.md](scoring-model.md): metric definitions, weights, formula, and verdict bands
- [evaluation-framework.md](evaluation-framework.md): interpretation criteria for Stages 2 and 3
- [output-template.md](output-template.md): section definitions and formatting rules for Stage 5
- [scripts/save_to_apple_notes.py](scripts/save_to_apple_notes.py): macOS helper to create a note in Apple Notes
- [scripts/save_to_obsidian.py](scripts/save_to_obsidian.py): helper to write a Markdown note into an Obsidian vault
- Apple Notes delivery is a post-output step, not a replacement for the analysis itself
- Obsidian delivery is a post-output step, not a replacement for the analysis itself

## File Structure

```text
idea-forge/
|-- README.md
|-- SKILL.md
|-- scoring-model.md
|-- evaluation-framework.md
|-- output-template.md
|-- scripts/
|   |-- save_to_apple_notes.py
|   `-- save_to_obsidian.py
|-- upgrades.md
|-- future-upgrades.md
`-- idea-forge.skill
```

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `idea-forge.skill` from the current source files.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with `idea [any rough idea]`.
