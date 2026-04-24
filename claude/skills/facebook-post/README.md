# Facebook Post Claude Skill

Claude-specific skill package for writing and polishing Facebook posts in Mick's voice.

This skill now uses a checked-in source file instead of the older `skill.md` plus `skill.zip` layout.

## Files

```text
claude/skills/facebook-post/
|-- README.md
|-- SKILL.md
`-- facebook-post.skill
|-- upgrades.md
```

## Source Of Truth

- Claude runtime source: [`SKILL.md`](./SKILL.md)

Update `SKILL.md` when the Facebook post workflow changes, then rebuild `facebook-post.skill` so the packaged export stays in sync.

## What This Skill Covers

- Rewriting rough drafts into polished Facebook posts
- Preserving specific facts, numbers, and context
- Applying Mick's direct, conversational tone
- Adding relevant hashtags without turning the post into spam

## Installation

Package `SKILL.md` into `facebook-post.skill`, then install it with your normal Claude skill workflow.

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `facebook-post.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
