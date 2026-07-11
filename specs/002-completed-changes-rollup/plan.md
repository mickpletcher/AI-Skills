<!-- markdownlint-disable MD013 -->

# 002 Completed Changes Rollup Plan

## Objective

Separate tracked completed history from local future planning across every Claude skill and align the repo tooling to keep that split intact.

## Assumptions

1. `future-upgrades.md` should remain ignored and local-only.
2. `completedchanges.md` should be tracked and visible from the normal README path.
3. Existing `upgrades.md` files remain useful and should not be removed.

## Phase 1 Repo Rule Alignment

### Work

- add the numbered spec package
- update shared or root guidance that describes the skill folder pattern

### Validation

- confirm the repo docs describe the new file structure accurately

## Phase 2 Skill Folder Migration

### Work

- create `completedchanges.md` in every Claude skill
- move completed history out of `future-upgrades.md`
- update every Claude skill `README.md` to link the new file

### Validation

- confirm every folder has the new file
- confirm README links exist everywhere

## Phase 3 Script Alignment

### Work

- update `Update-FutureUpgrades.ps1`
- update `claude/scripts/README.md`

### Validation

- run the script
- confirm it preserves future tiers and does not repopulate completed history

## Phase 4 Repo Log Updates

### Work

- update root `README.md`
- update `changelog.md`

### Validation

- confirm the repo level docs match the new pattern

## Safety Notes

- Do not delete `upgrades.md`.
- Do not rebuild skill packages for documentation-only changes unless a package actually depends on the updated docs.
- Do not change ignored-file boundaries for `future-upgrades.md`.

## Rollback Notes

If needed, the tracked `completedchanges.md` files can be removed and README links reverted without touching the skill prompts themselves.

<!-- markdownlint-enable MD013 -->
