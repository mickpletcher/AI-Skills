# Claude Scripts

PowerShell scripts for managing Claude skill installations and validating skill folder structure on Windows.

## Scripts

| Script | Purpose |
| ------ | ------- |
| [Initialize-ClaudeSkills.ps1](#initialize-claudeskillsps1) | Install, update, remove, and list skills in the Claude Desktop library |
| [Update-FutureUpgrades.ps1](#update-futureupgradesps1) | Create or refresh local `future-upgrades.md` files while preserving future planning tiers |
| [Validate-SkillFolders.ps1](#validate-skillfoldersps1) | Audit skill folders for missing required files |
| [Validate-SkillQuality.ps1](#validate-skillqualityps1) | Audit skill source sections and stale Claude packages |

---

## Initialize-ClaudeSkills.ps1

Manages the Claude Skills library. Scans a source directory for `.skill` files and installs them into the Claude Desktop user skills directory.

### Requirements

- Windows PowerShell 5.1 or PowerShell 7+
- Claude Desktop installed
- Skills directory at `$env:USERPROFILE\OneDrive\Documents\Claude\Skills\` (created automatically on first run)

### Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `-SkillsRoot` | String | Override the default Skills library path |
| `-SourcePath` | String | Override the default source path (defaults to Downloads) |
| `-RepoPath` | String | Path to a cloned repo with `.skill` files under a `\skills\` subfolder |
| `-SkillName` | String | Target a single skill by name (without `.skill` extension) |
| `-Remove` | Switch | Remove a skill. Requires `-SkillName` |
| `-UpdateOnly` | Switch | Only reinstall already-installed skills. Skips new ones |
| `-List` | Switch | Display all installed skills and exit |
| `-WhatIf` | Switch | Dry run — shows what would happen without making changes |

### Source Path Resolution

The script resolves the skill source in this order:

1. `-RepoPath\skills\` if `-RepoPath` is specified and the folder exists
2. `-SourcePath` if explicitly provided
3. `$env:USERPROFILE\Downloads` by default

If `-RepoPath` is given but `\skills\` is not found, it falls back to Downloads with a warning.

### Examples

```powershell
# Install all skills from Downloads
.\Initialize-ClaudeSkills.ps1

# Install a single skill
.\Initialize-ClaudeSkills.ps1 -SkillName "blog-post"

# Install directly from this cloned repo
.\Initialize-ClaudeSkills.ps1 -RepoPath "C:\Repos\AI-Skills"

# Update already-installed skills only
.\Initialize-ClaudeSkills.ps1 -UpdateOnly

# Remove a skill
.\Initialize-ClaudeSkills.ps1 -Remove -SkillName "blog-post"

# List all installed skills
.\Initialize-ClaudeSkills.ps1 -List

# Dry run
.\Initialize-ClaudeSkills.ps1 -WhatIf
```

### Output

New installs are tagged `[NEW]` in green. Updates are tagged `[UPDATED]` in cyan. Skipped or failed items are logged in yellow or red. A full list of installed skills is printed at the end of every run.

### Directory Structure Created

```text
$env:USERPROFILE\OneDrive\Documents\Claude\Skills\
├── user\       ← installed skills live here
└── public\     ← reserved for public/shared skills
```

Each `.skill` file is a zip archive extracted into its own subdirectory under `user\`.

After running, restart Claude Desktop to load any newly installed or updated skills.

---

## Update-FutureUpgrades.ps1

Creates or refreshes `future-upgrades.md` files under `claude/skills`. The script preserves any existing Tier 1, Tier 2, and Tier 3 planning bullets already present in the local file and keeps the `Recent Completed Work` section pointed at tracked `completedchanges.md` history instead of rebuilding shipped changes into the local planning file.

This is intended for local maintenance. The repo `.gitignore` already excludes `claude/skills/*/future-upgrades.md`.

### Update-FutureUpgrades Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `-SkillsRoot` | String | Root skill folder to scan. Defaults to `.\claude\skills` from the current repo root |
| `-WhatIf` | Switch | Show which files would be refreshed without writing changes |

### Update-FutureUpgrades Examples

```powershell
# Refresh every skill future-upgrades file
.\Update-FutureUpgrades.ps1

# Preview changes only
.\Update-FutureUpgrades.ps1 -WhatIf

# Target a specific skill root
.\Update-FutureUpgrades.ps1 -SkillsRoot "C:\Repos\AI-Skills\claude\skills"
```

### Update-FutureUpgrades Output

Prints the number of processed skill folders and the number of `future-upgrades.md` files that were written.

---

## Validate-SkillFolders.ps1

Audits skill folders under a given root path and reports any that are missing required files (`README.md`, `SKILL.md`). Useful for catching incomplete skill packages before committing or deploying.

### Validate-SkillFolders Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `-Root` | String | Root path to scan. Defaults to current directory |
| `-FailOnIssues` | Switch | Exit with code 1 if any issues are found. Useful in CI pipelines |
| `-RepairHints` | Switch | Output `git mv` commands to fix casing issues on detected files |

A folder is treated as a skill candidate if it contains a `skill.md` or `skill.zip` file (case-insensitive detection handled by repair hints).

### Validate-SkillFolders Examples

```powershell
# Validate skills in the current directory
.\Validate-SkillFolders.ps1

# Validate a specific folder
.\Validate-SkillFolders.ps1 -Root "C:\Repos\AI-Skills\claude\skills"

# Fail with exit code 1 if issues are found (CI use)
.\Validate-SkillFolders.ps1 -Root ".\claude\skills" -FailOnIssues

# Show git mv commands to fix file casing problems
.\Validate-SkillFolders.ps1 -Root ".\claude\skills" -RepairHints
```

### Validate-SkillFolders Output

Prints a pass/fail summary with counts. On failure, outputs a table of affected folders and missing files. With `-RepairHints`, prints ready-to-run `git mv` commands for any fixable casing issues.

---

## Validate-SkillQuality.ps1

Audits skill source files across supported platform folders for the standard sections defined in `shared/skill-standard.md`. Also checks whether Claude `.skill` packages are older than their `SKILL.md` source files.

### Validate-SkillQuality Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `-Root` | String | Repo root path to scan. Defaults to current directory |
| `-FailOnIssues` | Switch | Exit with code 1 if any issues are found |

### Validate-SkillQuality Examples

```powershell
# Validate all platform skills from the repo root
.\claude\scripts\Validate-SkillQuality.ps1

# Fail with exit code 1 for CI use
.\claude\scripts\Validate-SkillQuality.ps1 -FailOnIssues
```

### Validate-SkillQuality Output

Prints a pass/fail summary with counts. On failure, outputs the platform, skill, issue, and affected file.
