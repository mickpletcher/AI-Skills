## Add Insight Workflow

### Step 1: Extract the source

- Paste text: use as-is
- Screenshot: OCR the image, read the text
- URL: fetch the URL if accessible

Capture: who said it (name, title if visible), platform, approximate date, and the raw text.

### Step 2: Extract the principle(s)

A single post may contain multiple principles. Extract each one separately. For each, identify:

- **Principle name** — short, memorable (e.g., "Lead with impact, not credentials")
- **The rule** — 1-2 sentences
- **Rationale** — why the source says it matters
- **Example violation** — quote the bad example if given, otherwise synthesize a realistic one
- **Example fix** — quote the good example if given, otherwise synthesize one
- **Source** — Name, Title, Platform, Date

Skip anything that is opinion without an actionable rule (e.g., "I prefer Helvetica" is too weak to be a principle unless it is part of a broader formatting rule).

### Step 3: Check for duplicates

Read the existing `insights/principles.md`. If a principle is already covered, either:

- **Skip it** and tell the user "already in library as '<existing principle name>'", OR
- **Merge it**: if the new post strengthens or adds nuance, append a new source line to the existing principle using the `(adds: <angle>)` inline format defined in `insights/principles.md`.

Never create near-duplicate entries.

### Step 4: Append to library

Add new principles to `insights/principles.md` using the format defined at the top of that file. Maintain the existing structure. Do not reorder existing entries.

If the environment cannot write to `insights/principles.md`, do not claim the library was updated. Instead return the exact principle text that should be appended manually.

### Step 5: Confirm

Tell the user exactly what was added, merged, or skipped:

```
Added 2 principles to the library:
1. [Name] — [1-sentence summary]
2. [Name] — [1-sentence summary]

Merged into existing: [Name of existing principle] — added source with angle: "<angle>"
Skipped (already covered): [Name]
```

---
