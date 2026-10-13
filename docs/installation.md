# Platform installation

Use the [generated catalog](../CATALOG.md) to choose a skill and read its README first. Installation surfaces vary by host/version; use the instruction mechanism available in your app. No repository script automatically installs into your accounts, grants tools, or publishes content.

## Claude

Import the skill's `.skill` archive through a host that supports skill imports, or copy its whole source directory into the skills directory configured by your Claude host. Retain `references/`, scripts, templates, and assets: `SKILL.md` may load these selectively. The repository's PowerShell installer uses its own configurable local library; that library is not claimed to be auto-discovered by every Claude product.

Preview a repository install into an explicitly chosen local library:

```powershell
./claude/scripts/Initialize-ClaudeSkills.ps1 -RepoPath . -SkillsRoot ./local-library -WhatIf
```

Review the destinations before removing `-WhatIf`. See the [installer documentation](../claude/scripts/README.md#initialize-claudeskillsps1) for source precedence and recovery. Verify package hashes against [SHA256SUMS](../SHA256SUMS) using `Get-FileHash -Algorithm SHA256` or `sha256sum -c SHA256SUMS` from the repository root. Hashes establish byte agreement with the manifest, not publisher authenticity or safety.

## ChatGPT

Read the skill's `instructions.md`. Copy it into a dedicated custom GPT's instructions when that feature is available, or use a scoped conversation instruction. Custom Instructions affect broader conversations, so review the scope before using that surface. Upload supporting files only when needed and authorized. No API key is needed to read or copy the instructions.

## Copilot

Read the skill's `instructions.md`, then merge applicable guidance into your repository's supported Copilot instruction or prompt surface. Preserve existing repository instructions. A direct chat paste is also possible for a single task. These source files are not executable plugins and do not grant repository write permission.

## Cursor

Use the skill's `instructions.md` in the supported project-rule or chat instruction surface. Keep it scoped to the matching project/task and preserve existing rules. Supporting files remain in the repository; references to them require workspace access.

## Gemini

There are currently no shipped Gemini skills. When adding one, use a Gem or supported instruction surface and document where `instructions.md` and any support files belong. Do not assume a Claude `.skill` archive imports unchanged.

## Perplexity

There are currently no shipped Perplexity skills. Future skills must document the supported instruction/upload surface and the role of `SKILL.md`; the repository does not claim compatibility with any particular packaged import mechanism yet.

## Verify a setup

Start with a synthetic prompt from the skill README. Confirm it selects the right workflow, requests missing inputs, and preserves its constraints. Use the [behavioral evaluation guide](../evaluations/README.md) to record actual model behavior separately from structural/package checks. Never test with real credentials, production commands, or personal health records merely to verify installation.
