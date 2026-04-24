# Crypto Research Claude Skill

Claude-specific skill package for doing structured due diligence on a specific cryptocurrency.

This skill now uses a checked-in source file instead of the older `skill.md` plus `skill.zip` layout.

## Files

```text
claude/skills/crypto-research/
|-- README.md
|-- SKILL.md
|-- upgrades.md
`-- crypto-research.skill
```

## Source Of Truth

- Claude runtime source: [`SKILL.md`](./SKILL.md)

Update `SKILL.md` when the research workflow changes, then rebuild `crypto-research.skill` so the packaged export stays in sync.

## What This Skill Covers

- Researching one crypto asset at a time
- Building a structured due diligence report
- Checking tokenomics, team, liquidity, roadmap, adoption, and risks
- Producing a factual research summary without giving financial advice

## Installation

Package `SKILL.md` into `crypto-research.skill`, then install it with your normal Claude skill workflow.

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `crypto-research.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
