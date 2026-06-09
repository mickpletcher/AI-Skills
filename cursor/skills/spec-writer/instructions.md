# Cursor Skill: spec-writer

## Intent

Turn rough repository work into numbered specs with requirements, plan, and task files.

## Validation Checklist

- [ ] The output matches the skill's intended task and platform.
- [ ] Required inputs, assumptions, and uncertainty are explicit.
- [ ] Safety, scope, and source limits are respected.
- [ ] The response follows the requested format or the skill's default output format.
- [ ] The result is practical enough to use without another cleanup pass.

Use this skill when rough repo work needs to become a numbered spec before coding starts. The goal is to turn a change idea into a practical spec folder with requirements, plan, and tasks that another engineer can execute.

## Use When

- A repo change is large enough to need planning
- The user wants a numbered spec folder
- Requirements, plan, and tasks should be written before implementation
- The repo already uses a spec workflow

## Do Not Use When

- The change is too small to justify a spec
- The user wants direct implementation only
- There is not enough context to write honest requirements

## Workflow

1. Read the repo context first.
2. Identify the current spec folder pattern and numbering.
3. Pick the next available spec number unless the user supplied one.
4. Create a short folder name tied to the actual work.
5. Write:
   - `requirements.md`
   - `plan.md`
   - `tasks.md`
6. Make assumptions explicit.
7. Keep the tasks executable and ordered.

## What Good Output Looks Like

- Requirements define scope, constraints, and success criteria
- Plan explains touched areas, approach, risks, and validation
- Tasks break the work into real implementation steps

## Output Format

```text
Spec Folder

- specs/NNN-short-name/

Files To Create

- requirements.md
- plan.md
- tasks.md

Key Scope

- ...

Key Risks

- ...
```

## Constraints

- Do not pad the spec with boilerplate
- Match the repo's existing spec pattern
- Prefer concrete tasks over vague activity labels

## Example Prompts

```text
Use spec-writer to create the next numbered spec for this repo change.
```

```text
Turn this rough feature request into a requirements, plan, and tasks spec before coding starts.
```
