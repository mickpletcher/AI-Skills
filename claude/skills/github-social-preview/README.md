# github-social-preview

A Claude skill that generates a professional GitHub repository social preview image.

## Source of Truth

Use [SKILL.md](SKILL.md) as the canonical source for this skill.

## Overview

GitHub lets you set a custom social preview image (1280x640 px) on every repository. That image shows up when the repo link is shared on Twitter, LinkedIn, Slack, and anywhere else that renders Open Graph metadata. Most repos skip it and get a generic GitHub placeholder.

This skill generates a clean, GitHub-dark-themed preview image from a repository URL in seconds. It fetches the repo name, description, topics, and primary language, then renders a properly sized JPEG ready to upload directly to GitHub's repository settings.

## How To Use

Start your message with `gsp` followed by a GitHub repository URL.

```text
gsp https://github.com/user/repo
gsp https://github.com/org/project
generate github social preview https://github.com/user/repo
create repo preview image https://github.com/user/repo
```

### What you get back

- `github-social-preview.jpg` — 1280x640 JPEG, under 1 MB
- A confirmation with final file size and JPEG quality used
- Notes on any fallbacks applied (missing description, missing topics, etc.)

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

The generated image uses GitHub's dark theme palette:

- Background: dark gradient matching GitHub's `#0d1117` to `#161b22`
- Title: white bold text, large
- Subtitle: muted gray (`#8b949e`), smaller
- Tag pills: rounded, GitHub accent blue (`#58a6ff`)
- Language badge: colored dot + label, bottom-right corner
- GitHub Octocat mark: top-left watermark at low opacity
- No gradients on text, no drop shadows, no decorative clutter

## Constraints

| Constraint | Value |
| --- | --- |
| Output size | 1280x640 pixels |
| Output format | JPEG |
| Maximum file size | 1 MB |
| Auto-compression | Yes, down to quality 55 before canvas scaling |

## Fallback Behavior

The skill degrades gracefully when metadata is missing:

- No description: uses first sentence of README
- No README: infers from repo name and topics
- No topics: extracts keywords from README headings
- No language: omits language badge
- No metadata at all: renders title-only design

## Implement In Claude

1. Place this skill folder in your local Claude skills directory.
2. Confirm Pillow is installed in your Python environment.
3. Start a new Claude chat or refresh available skills.
4. Test with `gsp https://github.com/user/any-repo`.
