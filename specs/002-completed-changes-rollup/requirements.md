<!-- markdownlint-disable MD013 -->

# 002 Completed Changes Rollup Requirements

## Change Summary

Move completed change history for every Claude skill out of local `future-upgrades.md` files and into tracked `completedchanges.md` files, then expose that tracked history from each skill `README.md`.

## Current Baseline

The repository currently uses:

- tracked `upgrades.md` files for implemented upgrade log entries
- ignored local `future-upgrades.md` files for planning
- skill `README.md` files that link only to `upgrades.md`

Several Claude skills currently store recent completed work inside `future-upgrades.md`, which mixes shipped history with local planning and makes that history easy to lose or hide.

## Functional Requirements

### FR-1 Tracked Completed History

Every Claude skill folder must contain a tracked `completedchanges.md` file.

### FR-2 Completed Work Migration

Any completed work currently listed under `## Recent Completed Work` in a Claude skill `future-upgrades.md` file must be moved into that skill's `completedchanges.md`.

### FR-3 Future File Cleanup

Each Claude skill `future-upgrades.md` file must remain focused on future planning after the migration rather than carrying the completed history forward.

### FR-4 README Discoverability

Each Claude skill `README.md` must link to `completedchanges.md` so the tracked change history is visible from the normal skill docs.

### FR-5 Script Alignment

The local maintenance script that refreshes `future-upgrades.md` files must stop repopulating completed history from `upgrades.md`.

### FR-6 Standards Alignment

Shared guidance and templates that describe skill folder structure should be updated so future skill work recognizes `completedchanges.md` as part of the expected tracked artifacts.

## Non-Functional Requirements

### NFR-1 Repeatability

The migration should be applied consistently across all Claude skills, not by one-off manual edits in only the recently changed folders.

### NFR-2 Boundary Clarity

Tracked history and local planning must stay clearly separated.

### NFR-3 Minimal Churn

The change should preserve the existing `upgrades.md` files rather than replacing them.

## Non-Goals

- changing ChatGPT skill folders in this pass
- deleting `upgrades.md`
- rebuilding `.skill` packages for unchanged skill prompts
- redesigning the root repo layout

## Acceptance Signals

1. Every Claude skill folder has `completedchanges.md`.
2. Every Claude skill `README.md` links to `completedchanges.md`.
3. Local `future-upgrades.md` files no longer act as the completed history source.
4. `Update-FutureUpgrades.ps1` no longer repopulates completed history into local planning files.

<!-- markdownlint-enable MD013 -->
