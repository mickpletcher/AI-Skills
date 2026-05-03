---
name: github-social-preview
description: Generates a professional GitHub repository social preview image sized 1280x640 pixels as a JPG under 1 MB. Always trigger immediately when the user's message starts with "gsp". Also trigger on "generate github social preview", "create repo preview image", or any request to generate a social preview or OG image for a GitHub repository.
version: 1.0.0
---

# GitHub Social Preview Skill

Generate a clean, professional 1280x640 social preview image for any GitHub repository and export it as a JPG under 1 MB.

## Primary Triggers

Use this skill when the user starts with `gsp`, or asks to create a social preview or Open Graph image for a GitHub repository.

```text
gsp <repo_url>
generate github social preview <repo_url>
create repo preview image <repo_url>
make social preview for <repo_url>
og image for <repo_url>
```

## Expected Inputs

- A GitHub repository URL (required)
- Optionally: a custom tagline, color scheme, or layout hint

## Expected Outputs

- File: `github-social-preview.jpg`
- Size: exactly 1280x640 pixels
- Format: JPEG
- File size: under 1 MB (auto-recompressed if needed)

## Workflow

### Step 1 — Fetch repository metadata

Using the GitHub URL, retrieve:

1. Repository name (from URL path)
2. Repository description (from GitHub page or API)
3. README content (for fallback description and keyword extraction)
4. Topics / tags (from GitHub topics)
5. Primary programming language
6. Owner or organization name

Use the `WebFetch` tool to read the GitHub repository page. Parse the HTML or JSON response for description, topics, and language. If a raw README is needed, fetch `https://raw.githubusercontent.com/<owner>/<repo>/main/README.md` (try `master` if `main` returns 404).

### Step 2 — Derive display content

Build the four visual elements from the metadata gathered:

| Element | Source | Fallback |
| --- | --- | --- |
| Title | Repository name, formatted (replace hyphens/underscores with spaces, title case) | Raw repo name |
| Subtitle | Repository description | First sentence of README |
| Tags | Topics list (up to 5 tags) | Top keywords extracted from README or repo name tokens |
| Language badge | Primary language | Omit if unknown |

If no description, README, or topics exist, generate a minimal clean design with the title only.

### Step 3 — Generate the image

Run `scripts/generate_preview.py` with the derived content as arguments. The script:

1. Creates a 1280x640 canvas with the configured background gradient
2. Renders the GitHub-style Octicon logo mark in the top-left corner
3. Renders the title as the dominant H1 text
4. Renders the subtitle as a smaller H2 line below the title
5. Renders tag pills at the bottom
6. Renders the language badge bottom-right if known
7. Exports as JPEG at quality 92

### Step 4 — Enforce size constraint

After generation, check the output file size.

- If under 1 MB: done
- If 1 MB or larger: re-run export at progressively lower JPEG quality (85, 75, 65, 55) until the file is under 1 MB
- If still over 1 MB at quality 55: scale the canvas to 90% and retry from quality 92

### Step 5 — Confirm output

Report back:

- Full path to `github-social-preview.jpg`
- Final file size
- JPEG quality used
- Any fallbacks applied (missing description, missing topics, etc.)

## Design Specification

See `templates/design_config.json` for the full color, font, and layout specification.

Summary:

- Background: dark gradient (#0d1117 to #161b22), GitHub dark theme
- Title: white, bold, 72pt equivalent
- Subtitle: muted gray (#8b949e), 36pt equivalent
- Tag pills: rounded rectangles, #21262d fill, #30363d border, #58a6ff text
- Language badge: colored dot + label, bottom-right
- GitHub mark: top-left, low-opacity white watermark
- No decorative clutter, no gradients on text, no drop shadows

## Fallback Behavior

| Condition | Behavior |
| --- | --- |
| No repository description | Use first non-heading sentence from README |
| README missing or too short | Infer from repo name tokens and topics |
| No topics | Extract top 3-5 keywords from README headings or repo name |
| No language detected | Omit language badge entirely |
| No metadata at all | Render title-only design with GitHub mark |
| Image over 1 MB after quality 55 | Scale canvas to 90% and retry |

## Limitations

- Requires Python 3 with Pillow installed (`pip install Pillow`)
- Font rendering depends on system fonts; the script falls back to Pillow's built-in font if no system font is found
- Does not authenticate with the GitHub API; rate limits on public pages may apply
- Topics are not always visible without authentication; the script falls back to README keywords if the topics section is empty
- JPEG compression removes alpha channel; transparency is not supported in the output format
- The generated image is saved to the current working directory as `github-social-preview.jpg`

## Script Reference

```text
scripts/generate_preview.py   — Main image generation and compression script
templates/design_config.json  — Color, font, and layout configuration
examples/example_usage.md     — Worked examples with sample outputs described
```
