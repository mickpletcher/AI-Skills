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
- Confidence labels that separate direct observations from weaker guesses
- Goal aware analysis for fat loss, endurance fueling, muscle gain, and blood sugar control
- Quick summary output before the deeper analysis
- Side by side comparison of two foods or meals with practical tradeoffs
- Glycemic and meal-timing assessment
- Meal timing guidance that changes for pre workout, post workout, bedtime, or general daily use
- Better ingredient risk grouping for additives, sweeteners, seed oils, and ultra-processed signals
- Meal history review across repeated analyses
- User preference memory for favorite foods, sensitivities, and recurring supplement interactions
- Medication and supplement interaction warnings
- Supplement stacking cautions when a stated meal and supplement combination creates practical issues
- NOVA ultra-processed food scoring
- Healthier swap suggestions when warranted

## Local Planning File

`future-upgrades.md` is intentionally kept as a local roadmap file for this skill and is ignored by git in this repository.

## Behavior

- `fa` and `food` trigger the skill immediately
- The skill can analyze one food, compare two foods, or review repeated meal patterns
- The skill starts with a quick summary before the deeper analysis
- The skill changes emphasis based on the likely goal mode

## Supported Goal Modes

- `fat loss`
- `endurance fueling`
- `muscle gain`
- `blood sugar control`

## Example Prompts

```text
fa analyze this meal for muscle gain

fa compare these two protein bars for blood sugar control

fa scan this label and tell me whether the confidence is high or low

fa review these 5 repeated breakfasts and find the pattern

fa analyze this meal as a pre workout option

fa check this breakfast with my pre-workout and magnesium for supplement stacking issues
```

## Installation

Package `SKILL.md` into `food-analyzer.skill`, then install it with your normal Claude skill workflow.

## Upgrade Log

See [upgrades.md](upgrades.md) for the structured upgrade log and [completedchanges.md](completedchanges.md) for tracked completed changes.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `food-analyzer.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.

