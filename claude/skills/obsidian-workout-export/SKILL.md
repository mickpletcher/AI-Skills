---
name: obsidian-workout-export
description: Export workout data to an Obsidian-formatted Markdown file. Always trigger immediately when the user types "owd". Also trigger on "export workout", "obsidian workout", "save workout to obsidian", or related requests to export workout data into Obsidian. Read the current conversation first before searching prior conversation history. Name the file after the date of the chat that contains the workout data.
---

# Obsidian Workout Export Skill

Export logged workout sessions into Markdown files for an Obsidian `WorkoutData/` folder.

## Primary Trigger

Use this skill immediately when the user types `owd` in a chat that contains workout data.

Other triggers:

- `export workout`
- `obsidian workout`
- `save workout to obsidian`
- `workout to obsidian`
- `log to obsidian`

## Workflow

### 1. Locate the workout data

Always check the current conversation first. If the current chat already contains logged workout data such as exercises, sets, reps, weights, or body stats, use it directly instead of searching older history.

If the current chat does not contain workout data, search the most recent prior session using workout-related terms such as:

- `workout log sets reps`
- `leg press chest press fitness`
- `Day 1 Day 2 upper lower workout`

Use the date of the chat that contains the workout data as the filename date.

### 2. Extract all available session data

Pull every logged data point that is actually present.

**Session info**

- workout date
- day number and focus, for example `Day 2: Lower A`

**Exercises**

- exercise name
- weight
- sets
- reps
- PR flag when present

**Body stats**

- bodyweight in pounds
- body fat percentage

**PRs hit**

- each PR with weight and reps when available

**Session notes and flags**

- regressions
- injuries
- missed exercises
- anything else explicitly flagged in the session

### 3. Build the Markdown file

Use the filename `YYYY-MM-DD.md` based on the date of the chat containing the workout data.

Recommended structure:

```markdown
# Workout Log - [DAY NAME AND FOCUS]
**Date:** YYYY-MM-DD
**Program:** 15 Percent Body Fat Project

## Body Stats
| Metric | Value |
| --- | --- |
| Bodyweight | XXX lbs |
| Body Fat | XX.X% |

## Session - [Day X: Focus]

| Exercise | Weight | Sets | Reps | PR? |
| --- | --- | --- | --- | --- |
| Exercise Name | XXX lbs | X | X | yes or no |

## PRs Hit
- Exercise: XXX lbs / X reps

## Notes and Flags
- factual session notes, regressions, or flags
```

Omit sections with no data. If there are no PRs, either omit the section or state `None this session`.

### 4. Output expectations

Produce the Markdown content directly unless the user specifically asks for a file to be created in a local repo or folder.

When you finish, confirm:

- the filename
- the session date used
- that the file is intended for the Obsidian `WorkoutData/` folder

## Rules

- Never fabricate data. If a field was not logged, omit it or mark it as unlogged.
- If sets or reps are ambiguous, preserve exactly what was logged.
- If weight is missing for an exercise, note it as `bodyweight` or `unlogged` when appropriate.
- Keep the output factual. It is a data record, not a journal entry.
- Tables should stay Dataview-compatible for Obsidian use.
