# n8n-workflow

A Claude skill for designing, building, and troubleshooting n8n automation workflows on Mick's self-hosted Proxmox stack.

## Source of Truth

Use [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/n8n-workflow/SKILL.md) as the canonical source for this skill. The packaged [n8n-workflow.skill](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/n8n-workflow/n8n-workflow.skill) file is the Claude-ready export built from it.

## What It Does

Generates complete n8n workflow designs including node configuration patterns, Claude API integration, webhook setups, error handling, and Cloudflare Tunnel guidance. It is tailored to Mick's Proxmox-hosted n8n environment rather than a generic hosted setup.

## Trigger Phrases

| Phrase | Action |
| --- | --- |
| `n8n workflow for...` | Design a workflow for the described use case |
| `automate [X] in n8n` | Build a pipeline for the given task |
| `n8n node for...` | Generate a specific node configuration |
| `debug my n8n workflow` | Troubleshoot a described issue |

## Infrastructure Preloaded

- Instance: Proxmox LXC CT 104 at `192.168.0.81:5678`
- External access: Cloudflare Tunnel
- Claude API: HTTP Request node pattern with the required headers and `content[0].text` extraction
- Known credentials: Anthropic, CoinGecko, Alpaca, Reddit, SMTP

## Design Principles

- One trigger and one purpose per workflow
- Error handling on every external call
- All API keys in the n8n credential store
- Set node used to normalize data between steps
- Static data pinning during development

## File Structure

```text
n8n-workflow/
|-- README.md
|-- SKILL.md
|-- upgrades.md
`-- n8n-workflow.skill
```

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `n8n-workflow.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
