<!-- markdownlint-disable MD013 -->

# 002 Completed Changes Rollup Spec

## Scope

Normalize Claude skill change tracking so completed work lives in tracked `completedchanges.md` files and local `future-upgrades.md` files stay future-focused.

## Baseline Architecture

Each Claude skill folder currently centers around:

- `README.md`
- `SKILL.md`
- optional packaged `.skill`
- `upgrades.md`
- local-only `future-upgrades.md`

This change adds a new tracked file:

- `completedchanges.md`

## Proposed Design

### 1. Skill Level Completed History

Each Claude skill gets a `completedchanges.md` file.

For skills with migrated history, this file should capture the completed items that were previously sitting under `## Recent Completed Work` in `future-upgrades.md`.

For skills without recorded completed items, the file should still exist with a clear placeholder so the structure stays consistent across the repo.

### 2. README Upgrade Section Update

Each Claude skill `README.md` should keep the existing `upgrades.md` link and add a second link to `completedchanges.md`.

This keeps:

- `upgrades.md` as the structured implementation log
- `completedchanges.md` as the reader-friendly completed history

### 3. Future Planning File Refocus

`future-upgrades.md` should keep its planning tiers but replace the old completed history block with a pointer to `completedchanges.md`.

### 4. Script Behavior Change

`claude/scripts/Update-FutureUpgrades.ps1` should:

- preserve the tier planning sections
- write a stable note in `## Recent Completed Work`
- stop rebuilding that section from `upgrades.md`

### 5. Standards And Template Updates

Shared guidance and templates should mention `completedchanges.md` so future skills inherit the new structure.

## Impacted Files And Folders

- `claude/skills/*/README.md`
- `claude/skills/*/completedchanges.md`
- local `claude/skills/*/future-upgrades.md`
- `claude/scripts/Update-FutureUpgrades.ps1`
- `claude/scripts/README.md`
- `shared/platform-organization.md`
- root `README.md`
- `changelog.md`
- `specs/002-completed-changes-rollup/*.md`

## Control Flow

The normalized maintenance flow becomes:

1. shipped change is recorded in tracked docs
2. `completedchanges.md` carries the visible completed history
3. local `future-upgrades.md` carries only future planning tiers
4. the refresh script updates future planning files without reintroducing completed history

## Risks

1. If the script is not updated, the next local refresh will undo the migration.
2. If README files are not updated consistently, the new history files will exist but stay undiscoverable.
3. If templates are not updated, new skills will drift back to the old structure.

## Verification Strategy

### Required

- confirm every Claude skill folder has `completedchanges.md`
- confirm every Claude skill `README.md` links to `completedchanges.md`
- confirm `Update-FutureUpgrades.ps1` writes a completed-history pointer instead of regenerated bullet history

### Deferred

- automatic generation of `completedchanges.md` from `upgrades.md`

## Out Of Scope

- changing ChatGPT skill folders
- altering the contents of `SKILL.md` files
- repackaging `.skill` files for this documentation migration alone

<!-- markdownlint-enable MD013 -->
