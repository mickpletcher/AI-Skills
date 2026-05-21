# Cursor Skill: workflow-debugger

Use this skill when a CI workflow, automation pipeline, script run, or local repro path is failing and the goal is to isolate the real blocker quickly. Focus on evidence, local reproduction, and the smallest fix that resolves the failure.

## Use When

- A CI workflow is failing
- A GitHub Actions job broke after a code or config change
- A local script or command fails and needs a focused debug loop
- You need a structured path from logs to repro to fix

## Do Not Use When

- The user wants a broad architecture redesign
- There is no failure output, command, or workflow context
- The main task is code review rather than debugging

## Workflow

1. Read the failing output first.
2. Identify the exact failing step, command, or assertion.
3. Separate signal from noise.
4. Build the shortest possible local repro path.
5. Check recent changed files that could affect:
   - workflow config
   - environment variables
   - paths
   - dependency installation
   - test setup
   - build outputs
6. State the most likely root cause.
7. Suggest the smallest fix and the validation step.

## Output Format

```text
Failure Point

- Exact step or command that failed

Likely Cause

- Most probable root cause

Local Repro

1. ...
2. ...

Fix Plan

1. ...
2. ...

Validation

- ...
```

## Constraints

- Do not guess wildly when logs are missing
- Prefer a local repro over generic advice
- Keep the fix small and testable

## Example Prompts

```text
Use workflow-debugger on this failing GitHub Actions job and give me the shortest local repro path.
```

```text
Debug this script failure. Isolate the real blocker and show the smallest fix.
```
