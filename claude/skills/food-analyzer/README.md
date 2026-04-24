# Food Analyzer Claude Skill

Claude-specific skill package for analyzing food photos, nutrition labels, and ingredient lists with nutrition, glycemic, processing, timing, and interaction context.

This skill now uses a checked-in source file instead of the older `skill.md` plus `skill.zip` layout.

## Files

```text
claude/skills/food-analyzer/
|-- README.md
|-- SKILL.md
|-- food-analyzer.skill
`-- future-upgrades.md   # local planning file, ignored by git
|-- upgrades.md
```

## Source Of Truth

- Claude runtime source: [`SKILL.md`](./SKILL.md)

Update `SKILL.md` when the analysis workflow changes, then rebuild `food-analyzer.skill` so the packaged export stays in sync.

## What This Skill Covers

- Food photo analysis
- Nutrition label extraction
- Ingredient-list flagging
- Glycemic and meal-timing assessment
- Medication and supplement interaction warnings
- NOVA ultra-processed food scoring
- Healthier swap suggestions when warranted

## Local Planning File

`future-upgrades.md` is intentionally kept as a local roadmap file for this skill and is ignored by git in this repository.

## Installation

Package `SKILL.md` into `food-analyzer.skill`, then install it with your normal Claude skill workflow.

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `food-analyzer.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
