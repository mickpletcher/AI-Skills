<!-- markdownlint-disable MD013 -->

# 001 Skill Repo Workflow Spec

## Scope

Add a lightweight spec-first workflow for non-trivial `AI-Skills` repository changes while preserving the current skill authoring and packaging model.

## Baseline Architecture

The repository has these stable boundaries:

- `claude/skills/`: Claude skill source folders and packaged `.skill` exports
- `chatgpt/skills/`: ChatGPT skill source folders
- `shared/`: repo-wide standards and organization rules
- `templates/`: starter templates and verification templates
- `claude/scripts/`: maintenance scripts for local skill workflows
- root docs: `README.md`, `changelog.md`, `LICENSE`

The repo mixes tracked source files with intentionally ignored local planning files such as `claude/skills/*/future-upgrades.md`.

## Proposed Design

### 1. Numbered Spec Packages

Future non-trivial repo changes should start in numbered folders under `specs/`.

The minimum package is:

- `requirements.md`
- `spec.md`
- `plan.md`
- `tasks.md`

This keeps process lightweight but still gives a clear chain from intent to implementation.

### 2. When To Use The Workflow

Use the `specs/` workflow for changes such as:

- adding or changing shared repo conventions
- changing `.skill` packaging expectations
- adding or modifying shared scripts
- changing docs that affect multiple skills
- creating large new skills with supporting assets and cross-repo impact
- work that touches many skill folders in one pass

Do not require the workflow for:

- small wording edits in one skill
- one-off local backlog changes
- minor README corrections in one folder
- routine single-skill upgrades that do not alter repo conventions

### 3. Skill Lifecycle Coverage

The baseline workflow should explicitly account for the current repo lifecycle:

1. update the source files first
2. update tracked docs that should reflect the change
3. rebuild the packaged `.skill` when a Claude skill changed
4. update `future-upgrades.md` locally without treating it as tracked output
5. record the repo-visible change in `changelog.md`

### 4. Documentation Alignment

The root `README.md` should expose the spec workflow in the same way it already exposes repo standards and maintenance scripts.

## Impacted Files And Folders

- `README.md`
- `changelog.md`
- `specs/001-skill-repo-workflow/*.md`

## Control Flow

The new development process flow is:

1. define requirements for a non-trivial repo change
2. write the design in the numbered spec folder
3. break the work into a plan and tasks
4. implement the repo change
5. verify packaging, docs, and any relevant script behavior

## Risks

1. If the workflow is too heavy, contributors will ignore it.
2. If the workflow is too vague, it becomes another stale doc folder.
3. If the repo does not distinguish tracked and local artifacts clearly, future automation work will drift.

## Verification Strategy

### Required

- confirm the `specs/001-skill-repo-workflow/` folder exists with all four files
- confirm the root `README.md` links or points to the workflow
- confirm `changelog.md` records the addition

### Deferred

- reusable prompts or repo-level agent guidance under `.github/`
- CI enforcement for spec workflow adoption

## Out Of Scope

- changing skill content in this spec package
- adding repo-wide CI for every platform
- backfilling specs for every existing skill

<!-- markdownlint-enable MD013 -->
