# github-repo-architect

A Claude skill for turning a rough project idea into a complete GitHub repository architecture.

## Source of Truth

Use [SKILL.md](SKILL.md) as the canonical source for this skill. The packaged [github-repo-architect.skill](github-repo-architect.skill) file is the Claude-ready export built from it.

## Overview

This skill converts a project idea into a ready-to-implement GitHub repository blueprint. It detects the project type, extracts requirements, and returns a complete folder layout, README, CI pipeline, issue templates, development prompts, and setup commands.

## How To Use

Start your message with `repo`, `gra`, or `architect repo` to activate immediately. Natural language requests also trigger it.

### Example prompts

```text
repo PowerShell module that wraps the Intune Graph API
gra Python FastAPI service with JWT auth and PostgreSQL
architect repo n8n self-hosted workflow automation helper
build a repo structure for a React dashboard that reads from a REST API
scaffold this repository: [paste notes or spec]
turn this idea into a repo: [paste rough requirements]
```

### What you get back

Every blueprint includes:

1. Repository name and one-sentence purpose
2. Stated assumptions
3. Annotated folder layout
4. Generated file list with descriptions
5. Full README.md tailored to the project
6. Development prompts (implementation, test, review, release)
7. GitHub Actions CI workflow for the detected stack
8. Setup commands
9. Next implementation tasks
10. Security notes when the project involves secrets, credentials, or scraping

For specific ideas, starter file contents are included. For broader planning requests, filenames and descriptions are provided instead.

### Project types

The skill adapts the output structure to the repo type:

| Type | Examples |
| --- | --- |
| Claude or Codex skill | Content writer, resume auditor, automation helper |
| CLI tool | PowerShell module, Python utility, Node script |
| API service | FastAPI, Express, Flask, webhook receiver |
| Web app | React, Next.js, static dashboard |
| MCP server | Home Assistant MCP, Pi-hole MCP |
| Automation repo | Playwright scraper, scheduled task, n8n helper |
| Data project | ETL, analysis notebook, report generator |
| Infrastructure repo | Docker, Proxmox, Terraform, Ansible |

## Core Files

- [SKILL.md](SKILL.md): triggers, project type detection, workflow steps, output rules, and guardrails

## File Structure

```text
github-repo-architect/
|-- README.md
|-- SKILL.md
|-- upgrades.md
|-- future-upgrades.md
`-- github-repo-architect.skill
```

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `github-repo-architect.skill` from the current source files.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases from this README.
