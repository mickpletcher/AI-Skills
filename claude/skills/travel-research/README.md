# travel-research

A Claude skill for deeper destination comparison before full trip planning starts.

## Source of Truth

Use [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/travel-research/SKILL.md) as the canonical source for this skill. The packaged [travel-research.skill](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/travel-research/travel-research.skill) file is the Claude-ready export built from it.

## What It Does

This skill is for the decision stage before detailed planning:

1. compares destinations with a direct scorecard
2. surfaces seasonal and budget tradeoffs
3. checks travel friction from BNA
4. weighs activity fit, climate fit, and value
5. recommends the best option and a fallback
6. hands off cleanly into `travel-planning` once a winner is chosen

## Use When

- The destination is not final yet
- The trip needs stronger research before booking or itinerary work
- The user wants destination comparison instead of a fixed plan
- Budget, climate, or logistics tradeoffs are the real decision point

## Related Skills

- [travel-planning](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/travel-planning/README.md)
- [travel-itinerary](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/travel-itinerary/README.md)

## File Structure

```text
travel-research/
|-- README.md
|-- SKILL.md
|-- completedchanges.md
|-- upgrades.md
`-- travel-research.skill
```

## Upgrade Log

See [upgrades.md](upgrades.md) for implemented changes to this skill.

## Completed Changes

See [completedchanges.md](completedchanges.md) for the tracked shipped history of this skill.

## Implement In Claude

1. Update the checked in source files for this skill first.
2. Rebuild `travel-research.skill` from the current source files.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Test it with a real destination comparison request before relying on it for a live trip decision.
