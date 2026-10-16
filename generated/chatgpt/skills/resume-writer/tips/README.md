# Tips Staging Area

This folder keeps the `resume-writer` skill current without turning every new recruiter or hiring-manager post into a permanent rule.

## Purpose

Use `tips/` as a staging layer between fresh source material and the authoritative resume library:

- `insights/principles.md`: durable, reviewed principles used for normal audits
- `references/common-patterns.md`: fallback structural guidance
- `tips/`: newly collected posts, weekly review packets, and candidate advice that still needs judgment

## Folder Layout

```text
tips/
|-- README.md
|-- sources.json
|-- inbox/
|-- reviewed/
`-- archive/
```

- `sources.json`: curated source roster for the weekly refresh process
- `inbox/`: new candidate posts or summaries waiting for review
- `reviewed/`: worth keeping as context, but not yet promoted into `insights/principles.md`
- `archive/`: duplicates, stale items, or weak advice kept only for traceability

## Suggested Workflow

1. Run the weekly refresh helper.
2. Review the generated weekly packet and any new files in `inbox/`.
3. Move the strongest reusable items to `reviewed/`.
4. Promote only high-confidence patterns into `insights/principles.md`.

## Tip File Format

Each candidate tip file should follow this general shape:

```md
---
source_name: Example Recruiter
source_type: recruiter
source_url: https://example.com/post
published_at: 2026-04-24
captured_at: 2026-04-24
topics:
  - resume
  - keywords
status: suggested
confidence: medium
---

## Why it matters

One short paragraph explaining why the advice is relevant.

## Extracted resume tips

- Tip 1
- Tip 2

## Promotion recommendation

- [ ] Promote into insights/principles.md
- [ ] Keep in reviewed/
- [ ] Archive
```

## Guardrails

- Prefer concise summaries over full post copies.
- Keep source attribution and dates whenever possible.
- Do not treat `inbox/` items as authoritative resume principles by default.
- Promote only advice that is specific, repeatable, and useful beyond one viral post.
