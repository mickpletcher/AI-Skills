<!-- markdownlint-disable MD013 -->

# 002 Completed Changes Rollup Tasks

## Completed Tasks

- [x] T001 Audit the current Claude skill folders, local planning files, and README upgrade sections.
  - Files: `claude/skills/*`, `claude/scripts/Update-FutureUpgrades.ps1`
  - Verification: manual repo inspection

- [x] T002 Create the numbered spec package for the migration.
  - Files: `specs/002-completed-changes-rollup/*.md`
  - Verification: all four files present

## Completed Migration Tasks

- [x] T003 Create `completedchanges.md` in every Claude skill folder.
  - Files: `claude/skills/*/completedchanges.md`
  - Verification: one file exists per Claude skill

- [x] T004 Move completed work out of local `future-upgrades.md` files.
  - Files: local `claude/skills/*/future-upgrades.md`
  - Verification: completed history replaced by a pointer

- [x] T005 Update every Claude skill README upgrade section.
  - Files: `claude/skills/*/README.md`
  - Verification: each README links `completedchanges.md`

- [x] T006 Update the future-upgrades refresh script and its README.
  - Files: `claude/scripts/Update-FutureUpgrades.ps1`, `claude/scripts/README.md`
  - Verification: script output keeps future planning only

- [x] T007 Update repo level docs and change log.
  - Files: `README.md`, `changelog.md`, `shared/platform-organization.md`
  - Verification: docs reflect the new tracked and local split

## Follow-Up Backlog

- [ ] T008 Decide whether a tracked helper should generate `completedchanges.md` from `upgrades.md` for future repo maintenance.
  - Files: likely `claude/scripts/`
  - Verification: future updates can stay consistent without manual copy work

## Verification Notes

- This migration is documentation and maintenance workflow work.
- No Claude skill prompt behavior changes are intended in this spec.

<!-- markdownlint-enable MD013 -->
