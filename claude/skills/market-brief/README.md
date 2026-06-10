# Market Brief Claude Skill

Claude-specific skill package for generating a current market brief from live market data and current headlines.

## Files

```text
claude/skills/market-brief/
|-- README.md
|-- SKILL.md
|-- completedchanges.md
|-- future-upgrades.md
|-- upgrades.md
`-- market-brief.skill
```

## Source Of Truth

- Claude runtime source: [`SKILL.md`](./SKILL.md)

Update `SKILL.md` when the briefing workflow changes, then rebuild `market-brief.skill` so the packaged export stays in sync.

## What This Skill Covers

- Morning market briefs for Mick's default equity, macro, and crypto watchlist
- `mb` shortcut handling
- Temporary ticker appends and `only:` overrides
- Current prices, session labels, headlines, sources, and flags
- Optional `+depth` sections for sector performance, earnings, and economic calendar events

## Installation

Package the folder into `market-brief.skill`, then install it with your normal Claude skill workflow.

## Upgrade Log

See [upgrades.md](upgrades.md) for the structured upgrade log and [completedchanges.md](completedchanges.md) for tracked completed changes.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `market-brief.skill` from the current source files.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills.
5. Test with `mb`.
