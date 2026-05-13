# idea-forge

A Claude skill that runs raw ideas through a five-stage R&D pipeline and produces a structured invention plan with scoring, architecture, monetization paths, and an MVP roadmap.

## Source of Truth

Use [SKILL.md](SKILL.md) as the canonical source for this skill. The packaged [idea-forge.skill](idea-forge.skill) file is the Claude-ready export built from it.

## Overview

IdeaForge is a structured invention engine, not a note-taking tool. It takes any raw input — a sentence, a voice note transcript, a half-formed thought — and produces a fully developed engineering and commercialization plan.

The pipeline has five stages:

1. **Capture** — classify the idea type and extract the core problem
2. **Interpret** — assess feasibility, commercial viability, patent potential, and competition
3. **Expand** — generate missing features, integrations, business models, AI opportunities, and automation paths
4. **Score** — produce a weighted IdeaForge Score across seven metrics with a verdict
5. **Output** — structured document covering architecture, MVP roadmap, monetization, risks, and future expansion

## How To Use

Start any message with `forge` to activate immediately.

```text
forge [raw idea, rough concept, or messy note]
```

Messy input is fine. Part of the value is finding the real idea inside incomplete input.

---

### Modes

| Mode | Trigger | What runs |
| --- | --- | --- |
| Full Pipeline | `forge [idea]` | All five stages — full output document |
| Quick Assess | `forge quick [idea]` | Stages 1-2 — category, feasibility, commercial check |
| Score Only | `forge score [idea]` | Stages 1 and 4 — scoring table only |
| Expand Only | `forge expand [idea]` | Stages 1 and 3 — expansion without scoring |
| Commercialize | `forge commercialize [idea]` | Business models, monetization paths, and MVP |

---

### Example Prompts

```text
forge What if Home Assistant could detect behavioral fatigue from inactivity patterns and suggest wellness interventions automatically

forge quick Is there a market for a self-hosted AI writing coach that stores style preferences locally

forge score A PowerShell module that audits Intune device compliance and generates executive-ready PDF reports

forge expand An n8n workflow that monitors recruiter posts on LinkedIn and stages the best ones for review

forge commercialize A Claude skill that turns rough project ideas into complete GitHub repo architectures
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

## File Structure

```text
idea-forge/
|-- README.md
|-- SKILL.md
|-- scoring-model.md
|-- evaluation-framework.md
|-- output-template.md
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
4. Start a new Claude chat or refresh available skills, then test with `forge [any rough idea]`.
