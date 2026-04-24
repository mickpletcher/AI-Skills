# Blog Post Claude Skill

Claude-specific skill package for writing blog posts in Mick Pletcher's voice for `mickitblog.blogspot.com`.

This skill now uses a checked-in source file instead of relying only on the packaged `.skill` export.

## Files

```text
claude/skills/blog-post/
|-- README.md
|-- SKILL.md
|-- upgrades.md
`-- blog-post.skill
```

## Source Of Truth

- Claude runtime source: [`SKILL.md`](./SKILL.md)

Update `SKILL.md` when the writing guidance changes, then rebuild `blog-post.skill` so the packaged export stays in sync.

## What This Skill Covers

- Writing blog posts in Mick's first-person technical voice
- Problem-first post structure
- Honest project status reporting
- Practical technical explanations for other practitioners
- Repo or project links when relevant

## Installation

Package `SKILL.md` into `blog-post.skill`, then install it with your normal Claude skill workflow.

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `blog-post.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
