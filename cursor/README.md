# Cursor

This folder is reserved for Cursor specific reusable rules and coding assistant instructions.

## Intended Use

Use this platform area for Cursor focused rule files, scoped coding instructions, and setup notes for project or user level Cursor rules.

## Current State

Current Cursor skills:

- [pr-review](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/cursor/skills/pr-review/README.md)
- [workflow-debugger](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/cursor/skills/workflow-debugger/README.md)
- [repo-assessment](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/cursor/skills/repo-assessment/README.md)
- [spec-writer](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/cursor/skills/spec-writer/README.md)

## Suggested Pattern

```text
cursor/
`-- skills/
    `-- skill-name/
        |-- README.md
        `-- instructions.md
```

## Beginner Note

When Cursor skills are added, each skill folder should explain:

1. which file is the editable source
2. whether the instructions belong in project rules, user rules, or chat context
3. how to test the setup with one simple task
