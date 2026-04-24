# Facebook Reply Claude Skill

Claude-specific skill package for writing replies to Facebook comments in Mick's voice.

This skill now uses a checked-in source file instead of the older `skill.md` plus `skill.zip` layout.

## Files

```text
claude/skills/facebook-reply/
|-- README.md
|-- SKILL.md
`-- facebook-reply.skill
|-- upgrades.md
```

## Source Of Truth

- Claude runtime source: [`SKILL.md`](./SKILL.md)

Update `SKILL.md` when the Facebook reply workflow changes, then rebuild `facebook-reply.skill` so the packaged export stays in sync.

## What This Skill Covers

- Writing direct, paste-ready replies to Facebook comments
- Adjusting tone for support, questions, skepticism, or general comments
- Preserving Mick's casual, confident voice without sounding canned

## Related Skill

- [facebook-post](../facebook-post/README.md)

## Installation

Package `SKILL.md` into `facebook-reply.skill`, then install it with your normal Claude skill workflow.

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `facebook-reply.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
