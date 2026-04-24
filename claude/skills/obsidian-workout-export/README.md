# obsidian-workout-export

A Claude skill for exporting logged workout sessions into Obsidian-ready Markdown files.

## Source of Truth

Use [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/obsidian-workout-export/SKILL.md) as the canonical source for this skill. The packaged [obsidian-workout-export.skill](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/obsidian-workout-export/obsidian-workout-export.skill) file is the Claude-ready export built from it.

## Trigger

Type `owd` in a Claude chat that contains workout data.

Additional triggers:

- `export workout`
- `obsidian workout`
- `save workout to obsidian`
- `workout to obsidian`
- `log to obsidian`

## What It Does

When triggered, the skill locates workout data, extracts the logged session details, and formats them as a clean Markdown file ready for an Obsidian `WorkoutData/` folder.

Data captured can include:

- exercises with weight, sets, and reps
- PR flags per exercise
- body stats such as bodyweight and body fat percentage
- session notes, regressions, injuries, and missed exercises

The output file should use the date of the chat that contained the workout data, not the current date.

## Rules

- Never fabricate data
- Omit empty sections instead of inventing placeholders
- Keep tables Dataview-compatible for Obsidian
- Keep the output factual and compact

## File Structure

```text
obsidian-workout-export/
|-- README.md
|-- SKILL.md
|-- upgrades.md
`-- obsidian-workout-export.skill
```

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `obsidian-workout-export.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
