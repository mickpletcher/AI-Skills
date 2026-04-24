# Crypto Listings Claude Skill

Claude-specific skill package for tracking recent and upcoming cryptocurrency listings across major exchanges.

This skill now uses a checked-in source file instead of the older `skill.md` plus `skill.zip` layout.

## Files

```text
claude/skills/crypto-listings/
|-- README.md
|-- SKILL.md
|-- upgrades.md
`-- crypto-listings.skill
```

## Source Of Truth

- Claude runtime source: [`SKILL.md`](./SKILL.md)

Update `SKILL.md` when the listings workflow changes, then rebuild `crypto-listings.skill` so the packaged export stays in sync.

## What This Skill Covers

- Recently listed coins over the last 7 days
- Officially announced upcoming listings over the next 7 days
- Exchange-by-exchange listing activity summaries
- Source-backed listing briefs without price predictions or trading advice

## Installation

Package `SKILL.md` into `crypto-listings.skill`, then install it with your normal Claude skill workflow.

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `crypto-listings.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
