# x-post

A Claude skill for writing posts for X on tech, PowerShell, IT automation, and fitness topics.

## Source of Truth

Use [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/x-post/SKILL.md) as the canonical source for this skill. The packaged [x-post.skill](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/x-post/x-post.skill) file is the Claude-ready export built from it.

## Trigger

Start any message with `xp` to activate this skill. Everything after it is treated as the draft or topic.

## What It Does

This skill rewrites a draft into a single X post that:

- fits within 280 characters
- uses 2 to 3 relevant hashtags
- shows the final character count
- stays direct and specific instead of sounding like LinkedIn copy

## Related Skills

- [facebook-post](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/facebook-post/README.md)
- [facebook-reply](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/facebook-reply/README.md)

## File Structure

```text
x-post/
|-- README.md
|-- SKILL.md
`-- x-post.skill
|-- upgrades.md
```

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `x-post.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
