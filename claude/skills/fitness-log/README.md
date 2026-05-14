# Fitness Log Claude Skill

Claude-specific skill package for tracking workouts, logging progress, adjusting the training program, and generating fitness-related Facebook posts.

This skill now uses a checked-in source file instead of the older `skill.md` plus `skill.zip` layout.

## Files

```text
claude/skills/fitness-log/
|-- README.md
|-- SKILL.md
`-- fitness-log.skill
|-- upgrades.md
```

## Source Of Truth

- Claude runtime source: [`SKILL.md`](./SKILL.md)

Update `SKILL.md` when the training profile or workflow changes, then rebuild `fitness-log.skill` so the packaged export stays in sync.

## What This Skill Covers

- Logging workouts and PRs
- Summarizing progress against baseline numbers
- Summarizing strength, endurance, consistency, and recovery trends across logged sessions
- Checking whether recent training matches stated goals such as pull ups, cycling, or triathlon
- Producing weekly reviews with wins, missed sessions, and next block focus
- Providing nutrition and timing prompts tied to workout type, duration, and recovery need
- Normalizing similar exercise names so progress reviews stay cleaner
- Building longer progression plans for race prep, strength cycles, and hybrid seasons
- Producing export friendly structured data for dashboards or Obsidian tracking
- Adjusting the training plan within safety constraints
- Writing Facebook posts from workout data in Mick's voice

## Behavior

- `fit` and `workout` trigger the skill immediately
- The skill can log sessions, summarize trends, and compare training against goals
- The skill can produce weekly review output for planning the next block
- The skill can add a compact structured data section for dashboard or note reuse

## Example Prompts

```text
fit summarize my strength and recovery trends from the last 2 weeks

fit compare my recent training against my pull up goal

fit give me a weekly review with wins, missed sessions, and next block focus

fit normalize these exercise names and show a cleaner progress summary

fit build a 12 week hybrid season plan for strength plus triathlon work

fit export this week in a dashboard friendly structure
```

## Installation

Package `SKILL.md` into `fitness-log.skill`, then install it with your normal Claude skill workflow.

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `fitness-log.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
