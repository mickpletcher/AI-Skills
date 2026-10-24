## Refresh Tips Workflow

### Step 1: Load the tips workspace

Read these files when present:

- `tips/README.md`
- `tips/sources.json`
- `tips/inbox/`
- `tips/reviewed/`
- `tips/archive/`

Treat this workspace as a staging system:

- `tips/inbox/`: newly captured posts and candidate suggestions
- `tips/reviewed/`: reviewed notes worth keeping as reusable context
- `tips/archive/`: stale, duplicate, or superseded items

### Step 2: Classify the request

Choose the smallest matching action:

- **Refresh run**: create or update a dated weekly review packet, summarize new material, and prepare candidate tip files
- **Review run**: dedupe inbox items, score confidence, and move clear keepers to `reviewed/`
- **Promotion run**: convert reviewed tips into durable principles in `insights/principles.md`

### Step 3: Normalize each candidate tip

Each tip file should capture:

- source name
- source role or source type
- source URL
- published date when known
- fetched or reviewed date
- topic tags
- why it matters
- extracted resume advice
- promotion recommendation

Do not store a long verbatim copy of the full post when a concise summary is enough. Keep enough detail to recover the idea and source.

### Step 4: Evaluate trust level

For each candidate item, label it conceptually as one of:

- **Promote candidate**: specific, actionable, resume-relevant, and consistent with known recruiter behavior
- **Review later**: plausible but needs comparison against other sources
- **Archive**: weak, generic, contradictory, or not resume-focused

Fresh social posts are not automatically principles. If the advice is anecdotal, trendy, or overly specific to one recruiter's workflow, keep it in `tips/` instead of promoting it.

### Step 5: Produce the weekly result

For refresh and review runs, return:

- how many new candidates were added
- how many were moved to `reviewed/`
- how many were archived
- which items look strongest for promotion into `insights/principles.md`

If no new high-value advice was found, say so plainly and keep the workspace unchanged except for the dated review packet if one was requested.

---
