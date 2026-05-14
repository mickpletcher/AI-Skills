# github-social-preview

A Claude skill that generates a professional GitHub repository social preview image.

## Source of Truth

Use [SKILL.md](SKILL.md) as the canonical source for this skill.

## Overview

GitHub lets you set a custom social preview image (1280x640 px) on every repository. That image shows up when the repo link is shared on Twitter, LinkedIn, Slack, and anywhere else that renders Open Graph metadata. Most repos skip it and get a generic GitHub placeholder.

This skill generates a clean social preview image from a repository URL in seconds. It fetches the repo name, description, topics, and primary language, then renders a properly sized JPEG ready to upload directly to GitHub's repository settings.

## How To Use

Start your message with `gsp` followed by a GitHub repository URL.

```text
gsp https://github.com/user/repo
gsp https://github.com/org/project
generate github social preview https://github.com/user/repo
create repo preview image https://github.com/user/repo
gsp https://github.com/user/repo use the docs-blue theme with a logo
```

### What you get back

- `github-social-preview.jpg` — 1280x640 JPEG, under 1 MB
- A confirmation with final file size and JPEG quality used
- Notes on any fallbacks applied (missing description, missing topics, etc.)
- A local preview checklist for contrast, crop safety, and file size

### Uploading to GitHub

1. Open your repository on GitHub
2. Go to **Settings** (the gear icon on the repo page)
3. Scroll to **Social preview**
4. Click **Edit** and upload `github-social-preview.jpg`
5. Click **Save changes**

GitHub displays the image at roughly 1280x640 in link previews.

## Prerequisites

- Python 3.7 or later
- Pillow library: `pip install Pillow`
- Internet access (to fetch repo metadata from GitHub)

## File Structure

```text
github-social-preview/
|-- README.md
|-- SKILL.md
|-- scripts/
|   `-- generate_preview.py
|-- templates/
|   `-- design_config.json
`-- examples/
    `-- example_usage.md
```

## Core Files

- [SKILL.md](SKILL.md): triggers, full workflow, design spec, and fallback rules
- [scripts/generate_preview.py](scripts/generate_preview.py): image generation and compression script
- [templates/design_config.json](templates/design_config.json): color, font, and layout configuration
- [examples/example_usage.md](examples/example_usage.md): worked examples with expected output

## Design

The generated image supports multiple theme presets:

- `github-dark`
- `docs-blue`
- `builder-green`
- `launch-warm`

It can also take optional logo, screenshot, or custom background art assets when they improve the final layout.

## Constraints

| Constraint | Value |
| --- | --- |
| Output size | 1280x640 pixels |
| Output format | JPEG |
| Maximum file size | 1 MB |
| Auto-compression | Yes, down to quality 55 before canvas scaling |

## Smarter Fitting

- Long repo names are wrapped and then truncated only when needed
- Long descriptions are fitted to the available width
- Long topic sets are shortened cleanly instead of overflowing

## Local Preview Checks

Before final output the generator now reports:

- title contrast check
- subtitle contrast check
- crop safety check
- file size check

## Fallback Behavior

The skill degrades gracefully when metadata is missing:

- No description: uses first sentence of README
- No README: infers from repo name and topics
- No topics: extracts keywords from README headings
- No language: omits language badge
- No metadata at all: renders title-only design
- Long text: fits to width first, then truncates with ellipsis if needed
- Missing assets: skips logo, screenshot, or background art cleanly

## Upgrade Log

See [upgrades.md](upgrades.md) for the structured upgrade log and [completedchanges.md](completedchanges.md) for tracked completed changes.

## Implement In Claude

1. Place this skill folder in your local Claude skills directory.
2. Confirm Pillow is installed in your Python environment.
3. Start a new Claude chat or refresh available skills.
4. Test with `gsp https://github.com/user/any-repo`.
