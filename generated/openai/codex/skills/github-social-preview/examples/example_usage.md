# Example Usage

Worked examples showing input, derived content, and expected output for the github-social-preview skill.

---

## Example 1 — Well-documented Python library

**Input:**

```text
gsp https://github.com/psf/requests
```

**Fetched metadata:**

| Field | Value |
| --- | --- |
| Title | requests |
| Description | A simple, yet elegant, HTTP library. |
| Topics | python, http, requests, client, web |
| Language | Python |

**Derived display content:**

| Element | Value |
| --- | --- |
| Title | Requests |
| Subtitle | A simple, yet elegant, HTTP library. |
| Tags | python, http, requests, client, web |
| Language badge | Python |

**Script call:**

```bash
python scripts/generate_preview.py \
  --title "Requests" \
  --subtitle "A simple, yet elegant, HTTP library." \
  --tags "python,http,requests,client,web" \
  --language "Python" \
  --output "github-social-preview.jpg"
```

**Expected output:**

```
Generating preview for: Requests
Output: github-social-preview.jpg
Size:   84.2 KB (quality 92)
Dims:   1280x640
```

---

## Example 2 — TypeScript CLI tool with no topics

**Input:**

```text
gsp https://github.com/user/turbo-deploy
```

**Fetched metadata:**

| Field | Value |
| --- | --- |
| Title | turbo-deploy |
| Description | Zero-config deployment CLI for Node.js apps |
| Topics | (none) |
| Language | TypeScript |

**Fallback applied:** No topics — extracted keywords from README headings: `deploy`, `cli`, `nodejs`, `zero-config`

**Derived display content:**

| Element | Value |
| --- | --- |
| Title | Turbo Deploy |
| Subtitle | Zero-config deployment CLI for Node.js apps |
| Tags | deploy, cli, nodejs, zero-config |
| Language badge | TypeScript |

**Script call:**

```bash
python scripts/generate_preview.py \
  --title "Turbo Deploy" \
  --subtitle "Zero-config deployment CLI for Node.js apps" \
  --tags "deploy,cli,nodejs,zero-config" \
  --language "TypeScript" \
  --output "github-social-preview.jpg"
```

**Expected output:**

```
Generating preview for: Turbo Deploy
Output: github-social-preview.jpg
Size:   76.5 KB (quality 92)
Dims:   1280x640
```

---

## Example 3 — Minimal repo with no description and no README

**Input:**

```text
gsp https://github.com/user/my-scripts
```

**Fetched metadata:**

| Field | Value |
| --- | --- |
| Title | my-scripts |
| Description | (none) |
| Topics | (none) |
| Language | Shell |

**Fallbacks applied:**

- No description: inferred from repo name tokens → "Personal script collection"
- No topics: derived from repo name tokens → `scripts`, `shell`, `automation`

**Derived display content:**

| Element | Value |
| --- | --- |
| Title | My Scripts |
| Subtitle | Personal script collection |
| Tags | scripts, shell, automation |
| Language badge | Shell |

**Script call:**

```bash
python scripts/generate_preview.py \
  --title "My Scripts" \
  --subtitle "Personal script collection" \
  --tags "scripts,shell,automation" \
  --language "Shell" \
  --output "github-social-preview.jpg"
```

**Expected output:**

```
Generating preview for: My Scripts
Output: github-social-preview.jpg
Size:   61.8 KB (quality 92)
Dims:   1280x640
```

---

## Example 4 — Completely empty repo (title only)

**Input:**

```text
gsp https://github.com/user/new-project
```

**Fetched metadata:**

| Field | Value |
| --- | --- |
| Title | new-project |
| Description | (none) |
| Topics | (none) |
| Language | (none) |
| README | (none) |

**Fallbacks applied:** All fields missing — render title-only minimal design.

**Derived display content:**

| Element | Value |
| --- | --- |
| Title | New Project |
| Subtitle | (none) |
| Tags | (none) |
| Language badge | (none) |

**Script call:**

```bash
python scripts/generate_preview.py \
  --title "New Project" \
  --output "github-social-preview.jpg"
```

**Expected output:**

```
Generating preview for: New Project
Output: github-social-preview.jpg
Size:   41.3 KB (quality 92)
Dims:   1280x640
```

---

## Running the script directly

You can call `generate_preview.py` independently of the skill to regenerate with custom values:

```bash
python scripts/generate_preview.py \
  --title "Your Project Name" \
  --subtitle "What it does in one sentence" \
  --tags "tag1,tag2,tag3" \
  --language "Go" \
  --output "github-social-preview.jpg"
```

All arguments except `--title` are optional. The script prints file size and quality to stdout and exits with code 1 if the file cannot be compressed below 1 MB.

---

## Customizing the design

Edit `templates/design_config.json` to change colors, font sizes, or supply a custom font path. The script reads this file at runtime — no code changes needed.

Example: switch to a lighter theme by changing `bg_start` and `bg_end` to lighter values and updating `text_primary` to a dark color.
