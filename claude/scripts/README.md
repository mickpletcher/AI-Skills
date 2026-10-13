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

Manages the Claude Skills library. Scans a source directory recursively for `.skill` files and installs them into the Claude Desktop user skills directory.

### Requirements

- Windows PowerShell 5.1 or PowerShell 7+
- Claude Desktop installed
- Skills directory at `$env:USERPROFILE\OneDrive\Documents\Claude\Skills\` (created automatically on first run)

### Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `-SkillsRoot` | String | Override the default Skills library path |
| `-SourcePath` | String | Source directory to scan recursively (defaults to Downloads) |
| `-RepoPath` | String | Path to an AI-Skills clone with packages under `claude/skills/` (legacy `skills/` also supported) |
| `-SkillName` | String | Target a single skill by name (without `.skill` extension) |
| `-Remove` | Switch | Remove a skill. Requires `-SkillName` |
| `-UpdateOnly` | Switch | Only reinstall already-installed skills. Skips new ones |
| `-List` | Switch | Display all installed skills and exit |
| `-WhatIf` | Switch | Dry run — shows what would happen without making changes |

### Source Path Resolution

The script resolves the skill source in this order:

1. Explicit `-SourcePath`, scanned recursively.
2. `-RepoPath/claude/skills/`, or `-RepoPath/skills/` for legacy repositories.
3. `$env:USERPROFILE/Downloads` when neither override is supplied.

An invalid repository does not silently fall back to Downloads. Missing sources, zero matching packages (including an unmatched `-SkillName`), and duplicate package names produce a nonzero exit before the library is created. `-UpdateOnly` may successfully skip packages that are not already installed.

### Examples

```powershell
# Install all skills from Downloads
.\Initialize-ClaudeSkills.ps1

# Install a single skill
.\Initialize-ClaudeSkills.ps1 -SkillName "blog-post"

# Install directly from this cloned repo (including nested skill folders)
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

New installs are tagged `[NEW]`, updates `[UPDATED]`, and skipped packages produce a warning. Package failures include the source path and cause; the command exits nonzero if any package failed. Other successful package installations are retained.

### Package Resource Limits

Limits apply separately to each package. All are configurable positive integers; `MaxEntries` is at most 65,534. Byte values use PowerShell byte units (`1MB` = 1 MiB).

| Parameter | Default | Enforced boundary |
| --- | --- | --- |
| `-MaxArchiveBytes` | 64 MiB | File length before ZIP parsing |
| `-MaxEntries` | 1,024 | Independently counted directory records before .NET allocates entries; includes directories |
| `-MaxEntryBytes` | 32 MiB | Declared and actual expanded bytes per file |
| `-MaxExpandedBytes` | 128 MiB | Declared and actual expanded bytes across the package |
| `-MaxSourceBytes` | 1 MiB | Root `SKILL.md` bytes before extraction and text decoding |

Extraction checks actual bytes before every write using a fixed 64 KiB buffer, independently of declared sizes. Source validation scans bounded character buffers with BOM detection. Invalid metadata, contradictory counts, split archives, ZIP64 archives, and ambiguous end-record signatures in ZIP comments are rejected. Repack these as ordinary single-disk ZIP packages within the limits. Normal ZIP comments and a single bounded terminal central-directory digital-signature record are supported. Signature bytes are treated as metadata, not authenticated. Increasing byte limits does not enable ZIP64.

Rejected packages leave the previous installation intact and clean temporary staging; other valid packages in the batch still install. These quotas bound individual packages, not cumulative batch size or available disk space. The previous installation also occupies disk until replacement completes.

All 35 current packages fit the defaults: observed maxima were 1,208,803 compressed bytes, 20 entries, 197,993 bytes in one entry, 1,523,665 expanded bytes in a package, and 40,385 root source bytes. Rebuilt packages from the separate distribution branch also fit these defaults.

```powershell
# A deliberately stricter local source limit
.\Initialize-ClaudeSkills.ps1 -RepoPath "C:\Repos\AI-Skills" -MaxSourceBytes 512KB
```

The regression suite covers all repository packages, every quota at its boundary and one unit over, malformed counts and lengths, bounded streaming, source encodings, batch failures, and existing rollback/recovery behavior. Run `pwsh -NoProfile -File ./claude/scripts/tests/Initialize-ClaudeSkills.Tests.ps1`. All 21 regression groups passed locally with PowerShell 7.5.4 on macOS, including an independent reviewer run; the focused installer CI workflow also runs the suite on Linux PowerShell 7, Windows PowerShell 7, and Windows PowerShell 5.1. Check the pull request for the latest run results.

### Safe Updates And Recovery

Each package is extracted into a unique `.install-*` directory inside `SkillsRoot`, outside the `user` catalog. The package must be a readable ZIP containing a nonempty root `SKILL.md`. Extraction rejects traversal and absolute paths, Windows alternate streams/reserved names, links, special files, and duplicate paths (case-insensitively).

Only after validation does the installer rename the old installation into a backup and move the staged directory into place. If replacement fails, it restores the backup. If restoration fails too, it retains the backup and prints its exact recovery path. Do not delete that recovery directory until you have restored or copied the previous installation. Normal success and handled failures clean temporary files; cleanup failures report the retained directory.

A process or machine interruption between renames may also leave a recovery directory; there is no automatic crash recovery. Updates are per skill, not a transaction across the entire batch. `-WhatIf` previews discovery and destinations without creating directories or extracting packages. Skill names use letters, digits, hyphens, or underscores and must start with a letter or digit.

### Regression Tests

Run from the repository root:

```powershell
pwsh -NoProfile -File ./claude/scripts/tests/Initialize-ClaudeSkills.Tests.ps1
```

On Windows PowerShell 5.1, use `powershell.exe` instead of `pwsh`. The suite requires no Pester module and uses only unique temporary libraries, cleaned up afterward. It covers the actual repository packages, recursive and legacy discovery, source precedence, empty/invalid sources, duplicate names, dry runs, update-only behavior, invalid archives, and injected replacement/rollback failures.

The suite has been verified on macOS with PowerShell 7.5.4. Windows (including PowerShell 5.1) and Linux have not been executed in this environment. On non-Windows hosts, pass explicit `-SkillsRoot` and `-SourcePath` or `-RepoPath`; the default library and Downloads paths remain Windows-oriented.

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

Uses the shared Python validator to check every immediate skill directory, including directories missing their main source. Requires exact-case `README.md`, `SKILL.md`, `<name>.skill`, and `completedchanges.md`. Fails if no directories are checked. `-RepairHints` describes safe case-only renaming; it does not mutate files.

```powershell
./claude/scripts/Validate-SkillFolders.ps1 -Root ./claude/skills -FailOnIssues
```

## Validate-SkillQuality.ps1

Validates all platform skill directories: required files, parsed YAML frontmatter against the repository schema, required source sections, navigable local Markdown links/anchors, every package member against source content, deterministic archive bytes, and generated catalog/checksum freshness. Missing sources/packages and empty discovery are failures. Timestamps are not used.

```powershell
./claude/scripts/Validate-SkillQuality.ps1 -FailOnIssues
```

Both wrappers require Python 3.11+ and [requirements-dev.txt](../../requirements-dev.txt). Use `-Python /path/to/python` if the executable is not named `python`. `-FailOnIssues` remains accepted for existing callers; failures now always exit nonzero. `-Root` selects the folder root for folder validation or repository root for quality validation.

See [contribution checks](../../CONTRIBUTING.md) and [distribution rules](../../docs/distribution.md) for package/catalog rebuilding and the distinction between CI jobs and enforced required checks.
