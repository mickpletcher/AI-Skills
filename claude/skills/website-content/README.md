# website-content

A Claude skill for writing and updating content for Mick Pletcher's personal website.

## Source of Truth

Use [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/website-content/SKILL.md) as the canonical source for this skill. The packaged [website-content.skill](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/website-content/website-content.skill) file is the Claude-ready export built from it.

## What It Does

This skill generates polished, first-person website copy for sections such as:

- About / Bio
- Projects
- Skills
- AI / Homelab
- Health / Sports
- Blog integration
- Contact
- SEO metadata

The tone should be polished and professional, but still first-person and direct.

## Reference File

Use [reference/copy-library.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/website-content/reference/copy-library.md) as the local copy-block library for reusable section content.

## File Structure

```text
website-content/
|-- README.md
|-- SKILL.md
|-- website-content.skill
`-- reference/
    `-- copy-library.md
|-- upgrades.md
```

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `website-content.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
