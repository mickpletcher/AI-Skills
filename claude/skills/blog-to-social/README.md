# Blog To Social Claude Skill

Claude-specific skill package for converting a finished blog post into Facebook, X, and LinkedIn posts in one pass.

This skill now uses a checked-in source file instead of relying on the Anthropic-style `skill.md` plus `skill.zip` layout.

## Files

```text
claude/skills/blog-to-social/
|-- README.md
|-- SKILL.md
|-- upgrades.md
`-- blog-to-social.skill
```

## Source Of Truth

- Claude runtime source: [`SKILL.md`](./SKILL.md)

Update `SKILL.md` when the social-post guidance changes, then rebuild `blog-to-social.skill` so the packaged export stays in sync.

## What This Skill Covers

- Converting one finished blog post into Facebook, X, and LinkedIn posts
- Writing all three in one pass
- Keeping each platform version native instead of reusing the same copy
- Preserving Mick's direct, practical tone across all three outputs

## Installation

Package `SKILL.md` into `blog-to-social.skill`, then install it with your normal Claude skill workflow.

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `blog-to-social.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
