# AI Skills Changelog

Compiled from repo history and the current working tree.

## 2026-05-13

- Added `claude/skills/patentforge-provisional-skill` with source files, templates, schemas, docs, examples, and a packaged `.skill` export for provisional drafting support with legal safety boundaries
- Updated every skill `future-upgrades.md` file across `claude/skills` and `chatgpt/skills`
- Created the missing `chatgpt/skills/food-analyzer/future-upgrades.md`
- Improved `claude/scripts/Update-FutureUpgrades.ps1` so it can populate skill specific tier ideas, preserve existing tier content, and handle single skill roots
- Updated `claude/skills/idea-forge` to support Apple Notes output delivery on macOS and iOS handoff flows
- Updated `claude/skills/idea-forge` to support Obsidian `Ideas` folder output delivery on macOS and iOS handoff flows
- Added this root `changelog.md`
- Added root `README.md` link to the changelog
- Added `claude/scripts/Update-FutureUpgrades.ps1` to create and refresh skill `future-upgrades.md` files from `upgrades.md`
- Updated `claude/scripts/README.md` with the new maintenance script

## 2026-05-12

- Added the `idea-forge` Claude skill
- Added the packaged `idea-forge.skill` export
- Changed the `idea-forge` trigger word from `forge` to `idea`

## 2026-05-02

- Added `github-social-preview`

## 2026-04-27

- Added follow up tool selection maintenance work recorded in git history

## 2026-04-24

- Added `resume-writer` tips refresh automation
- Improved `resume-writer` README usage guidance and GitHub links
- Added Claude skill packs and reference libraries
- Updated `alpaca-trading` skill docs and template metadata
- Removed obsolete shared Alpaca skill source
- Reorganized skills as platform specific sources
- Added the Claude Alpaca Trading skill
- Defined the portable skill standard and starter templates
- Completed the initial folder setup
