# photo-rename

A Claude skill for renaming photos to descriptive real-world names using image understanding, GPS metadata, and location context.

## Source of Truth

Use [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/photo-rename/SKILL.md) as the canonical source for this skill. The packaged [photo-rename.skill](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/photo-rename/photo-rename.skill) file is the Claude-ready export built from it.

## What It Does

This skill analyzes one or more photos and suggests descriptive filenames such as:

- `phantom_ranch_grand_canyon.jpg`
- `eiffel_tower_paris.jpg`

It combines:

1. image analysis
2. EXIF GPS metadata
3. reverse geocoding
4. web research when needed

## Trigger

Start the request with `rp`, or ask to rename, identify, or label uploaded photos by location or content.

## Naming Rules

- Use `snake_case`
- Prefer specific names over generic ones
- Keep names under 50 characters when practical
- Preserve the original file extension
- Add sequence suffixes such as `_01` when names would collide

## File Structure

```text
photo-rename/
|-- README.md
|-- SKILL.md
|-- upgrades.md
`-- photo-rename.skill
```

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `photo-rename.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
