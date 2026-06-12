# workflow-debugger

A Cursor skill for debugging CI failures, local repro steps, and targeted fix loops in active codebases.

## Source of Truth

Use [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/cursor/skills/workflow-debugger/instructions.md) as the editable source of truth for this skill.

## How To Implement In Cursor

### Option 1: Project Rules

1. Open the target repo in Cursor.
2. Open the project rules surface you use for repo specific instructions.
3. Copy the full contents of [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/cursor/skills/workflow-debugger/instructions.md).
4. Paste the content into the project rule.
5. Save it.
6. Test it with a real failing command, workflow log, or CI error.

### Option 2: One Time Chat Context

1. Open Cursor Chat.
2. Paste the instruction content first.
3. Paste the failing output, command, or workflow file after it.
4. Ask for the shortest local repro path and likely cause.

## First Test

```text
Use workflow-debugger on this failing CI step. Identify the real failure point, give me a local repro path, and suggest the smallest fix.
```
