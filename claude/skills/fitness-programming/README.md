# fitness-programming

A Claude skill for building structured training plans, progression blocks, and season layouts for Mick's fitness goals.

## Source of Truth

Use [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/fitness-programming/SKILL.md) as the canonical source for this skill. The packaged [fitness-programming.skill](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/fitness-programming/fitness-programming.skill) file is the Claude-ready export built from it.

## What It Does

This skill extends the repo fitness area beyond workout logging and into planning. It is designed to:

- build goal-specific training blocks
- use presets for pull up focus, cycling power, triathlon base, and recomposition
- create strength, endurance, and hybrid season plans
- define progression logic clearly
- adapt weekly plans when fatigue or recovery drops
- suggest safer exercise substitutions tied to injuries and constraints
- add phased nutrition prompts for bulk, cut, endurance build, and race week priorities
- review whether the block is moving the intended benchmark metrics
- build annual season architecture and event countdown plans
- use `fitness-log` trends to guide the next programming adjustment
- adjust plans based on recovery, schedule, and safety constraints
- keep programming tied to real goals such as pull ups, cycling, triathlon, muscle gain, and cutting

## Trigger

Start the request with `program`, or ask for a training plan, progression block, race prep plan, hybrid season, or fitness programming adjustment.

## Example Requests

```text
program build me an 8 week pull up focused block that still keeps lower body strength moving
```

```text
program give me a 12 week hybrid strength and triathlon season with realistic recovery
```

```text
program restructure my weekly split for muscle gain while cutting and keep it back safe
```

```text
program use my recent fitness-log trends to adjust the next 4 weeks and tell me if the block is still moving the right metrics
```

## File Structure

```text
fitness-programming/
|-- README.md
|-- SKILL.md
|-- completedchanges.md
|-- upgrades.md
`-- fitness-programming.skill
```

## Upgrade Log

See [upgrades.md](upgrades.md) for the structured upgrade log and [completedchanges.md](completedchanges.md) for tracked completed changes.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `fitness-programming.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skill workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
