<!-- markdownlint-disable MD013 -->

# 001 Skill Repo Workflow Requirements

## Change Summary

Add a lightweight GitHub spec workflow to the `AI-Skills` repository so non-trivial repo changes have a consistent requirements, design, plan, and task trail.

## Current Baseline

The repository already contains:

- platform-specific skill sources under `claude/` and `chatgpt/`
- shared standards and templates under `shared/` and `templates/`
- Claude maintenance scripts under `claude/scripts/`
- a root `README.md` and `changelog.md`
- local-only `future-upgrades.md` files under skill folders that are intentionally ignored

The repository did not contain a root `specs/` workflow before this change.

## Functional Requirements

### FR-1 Numbered Spec Package

The repo must include a numbered spec package under `specs/` with:

- `requirements.md`
- `spec.md`
- `plan.md`
- `tasks.md`

### FR-2 Repo Workflow Guidance

The initial spec must define when spec workflow is required for this repo and when it is optional.

### FR-3 Skill Repo Scope

The spec must reflect the actual repo workflow for:

- skill source updates
- packaged `.skill` rebuilds
- tracked docs and changelog updates
- local-only `future-upgrades.md` handling
- shared script or convention changes

### FR-4 Minimal Adoption Friction

The workflow must stay lightweight enough to use for multi-file or cross-skill changes without turning small prompt edits into process overhead.

### FR-5 Root Doc Visibility

The root `README.md` must point contributors to the new `specs/` workflow so it is discoverable without searching the repo.

### FR-6 Change Logging

The root `changelog.md` must record the addition of the spec workflow baseline.

## Non-Functional Requirements

### NFR-1 Accuracy

The spec files must describe the repo as it exists today, not a future skill platform that is not present yet.

### NFR-2 Maintainability

The workflow must be readable by both human contributors and coding agents.

### NFR-3 Local Boundary Respect

The workflow must preserve the distinction between tracked repo artifacts and local-only planning files.

## Non-Goals

- adding CI for every skill
- redesigning the repo structure
- converting every past change into a retroactive spec
- forcing spec workflow on one-file wording tweaks

## Acceptance Signals

1. The repo contains `specs/001-skill-repo-workflow/` with the four baseline files.
2. The README explains when to use the spec workflow.
3. The changelog records the addition.
4. Future contributors have a concrete place to start for cross-skill or shared-repo work.

<!-- markdownlint-enable MD013 -->
