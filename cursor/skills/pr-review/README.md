# pr-review

A Cursor skill for reviewing pull requests and diffs with a focus on regressions, risk, and missing tests.

## Source of Truth

Use [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/cursor/skills/pr-review/instructions.md) as the editable source of truth for this skill.

## How To Implement In Cursor

### Option 1: Project Rules

Use this when you want the review behavior available inside one repo.

1. Open the target repo in Cursor.
2. Open the project rules surface you use for persistent repo instructions.
3. Copy the full contents of [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/cursor/skills/pr-review/instructions.md).
4. Paste the content into the project rules area.
5. Save the rule.
6. Test it against a small real diff.

### Option 2: One Time Chat Context

Use this when you only want the review behavior for one session.

1. Open Cursor Chat.
2. Paste the full contents of [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/cursor/skills/pr-review/instructions.md).
3. Paste the diff, changed files, or pull request context after it.
4. Ask for a strict review focused on findings.

## First Test

```text
Review this diff for regressions, practical risk, and missing tests. Lead with findings only.
```

## File Structure

```text
cursor/skills/pr-review/
|-- README.md
`-- instructions.md
```
