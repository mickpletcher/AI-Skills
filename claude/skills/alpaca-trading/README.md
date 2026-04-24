# Alpaca Trading Claude Skill

Claude-specific skill package for working safely in the `Trading` repository and its Alpaca-related workflows.

This skill now uses a checked-in source file instead of relying only on the packaged `.skill` export.

## Files

```text
claude/skills/alpaca-trading/
|-- README.md
|-- SKILL.md
`-- alpaca-trading.skill
```

## Source Of Truth

- Claude runtime source: [`SKILL.md`](./SKILL.md)

Update `SKILL.md` when the workflow changes, then rebuild `alpaca-trading.skill` so the packaged export stays in sync.

## What This Skill Covers

- Safe work on the mixed Python and PowerShell `Trading` repository
- Alpaca paper-trading helpers under `Alpaca/`
- Strategy work under `Backtesting/`
- Journal flows under `Journal/`
- PowerShell module work under `src/`
- Existing GitHub Spec workflow already present in the Trading repo

## Installation

Package `SKILL.md` into `alpaca-trading.skill`, place the file where your Claude skill installer expects it, then reload Claude Desktop.
