---
name: "github-repo-architect"
description: "Design a practical, testable Git repository architecture from a project idea, including documentation, CI, starter files and previews; also guide scoped GitHub settings configuration with permission and verification boundaries."
---
<!-- GENERATED CANDIDATE: edit master-skills or adapters, not this file -->
# Git Repository Architect

## Purpose
Turn a software or automation idea into an implementable repository blueprint. Work across languages and AI hosts; never assume a particular tool or repository permission exists.

## Activate when
The user asks to configure GitHub repository settings, or to design, scaffold, or architect a new repository, or uses a shorthand such as "repo", "gra", or "architect repo" followed by an idea.

## Do not activate when
- The user asks to audit or refactor an existing repository: use an assessment workflow, except a scoped GitHub settings configuration request.
- The user only needs a README for a known layout: use a README-writing workflow.
- There is no concrete project idea for a new architecture: request the minimum useful description; settings-only requests need a repository target instead.
- The project handles credentials or sensitive infrastructure and its security requirements are unclear: clarify security boundaries first.

## Choose an execution mode

State the selected mode before work. Honor an explicit choice; if the request is ambiguous, offer **blueprint-only**, **scaffold/generate files**, or **configure GitHub** and proceed only with a non-mutating blueprint until the scope is clear. Modes can be combined only when requested; none grants authority for the others.

- **blueprint-only**: propose structure, file contents, commands and settings; do not write files or change GitHub. Mark everything proposed and checks not run.
- **scaffold/generate files**: create only requested files at the agreed destination using available, authorized file tools. Inspect existing files and preserve user edits. Inline contents are not saved artifacts. Run applicable checks when permitted; this mode does not authorize remote publication or GitHub settings changes.
- **configure GitHub**: inspect the named repository, recommend settings, obtain action-specific authorization as required by the host, apply only the requested and permitted changes, then read back the resulting state. It does not authorize scaffolding, publishing, merging, installation or release.

For any GitHub settings advice or configuration, read [GitHub settings workflow](references/github-settings.md) before proceeding. A configuration-only request for an existing repository belongs here; an architecture audit still belongs in an assessment workflow. If no project idea is needed for that settings-only task, do not demand one.

Tool access is not consent. These instructions never override host confirmation policy. Security, access and visibility changes require appropriate approval for the exact target and change, even when the user selected configure GitHub. A denied operation stops that operation; do not switch tools, identities or permission scopes to bypass it.

## Project preview

Automatically include a root-level project preview in the architecture: `preview.png` by default (`preview.jpg` is a photographic alternative; `preview.gif` is optional for a README motion demo). Read [Preview workflow](references/preview.md) for mode-aware creation, safety, image validation, README embedding and separately authorized GitHub Social preview setup. A blueprint plans this artifact without writing it; a requested scaffold includes it when supported tools are available, otherwise reports it pending. Never fabricate a functioning demo.

## Final handoff

Finish every mode with a short, evidence-based handoff:

1. **Artifacts**: proposed versus actually created/changed files, with paths or links; identify unsaved inline content.
2. **Checks**: exact commands, actual pass/fail/not-run results and the revision or final files checked; distinguish local checks from remote CI.
3. **GitHub settings**: separate recommended, applied-and-verified, attempted-but-unverified, blocked and unchanged settings. If none were applied, explicitly say so. A generated workflow does not establish required checks or branch protection.
4. **Preview**: report root image, README embed and GitHub Social preview upload as three independent states, each with verification or a pending reason.
5. **Needs attention**: unresolved decisions, capability/permission gaps, failed checks and concrete manual follow-ups with the responsible owner where known. Never claim a setting is applied from a recommendation, script, successful write response alone, or unavailable read-back.

## Repository name and metadata

Automatically review the project/repository name, even when already chosen, for clarity, relevant search terms, brevity, spelling and misleading claims. Offer a better alternative with rationale when useful; never promise traffic or ranking and preserve the user's final choice. Verify namespace availability when access permits, otherwise mark it unknown. Derive a concise About description and relevant GitHub topics from actual purpose/language/technology. In blueprint/scaffold mode these are proposals; apply metadata only within authorized configure GitHub scope. Existing repository renames require explicit approval and integration-impact review. Topics are not release tags.

## Inputs
Identify the goal, intended users, stack, runtime, inputs and outputs, integrations, secrets, deployment environment, tests, and licensing. Distinguish facts supplied by the user from assumptions. Ask only about missing decisions that materially change the architecture.

## Decision process
1. Classify the project: CLI, API, web app, AI skill, automation, data pipeline, infrastructure, or mixed stack.
2. Choose the smallest maintainable architecture for the stated needs; avoid speculative services and unnecessary layers.
3. Choose appropriate language tooling and testing frameworks. Prefer project conventions when known.
4. Design the directory tree, module responsibilities, configuration, and deployment strategy.
5. Define security boundaries: credential storage, permissions, least privilege, private data handling, and safe defaults.
6. Produce implementation-ready documentation, starter files when requested, CI, and a test plan.
7. Verify the output is internally consistent and executable in the user's stated environment.
8. If tools are available and authorized, use them to inspect or create files; otherwise provide an actionable blueprint and clearly label it as proposed, not implemented.

## Output contract
For architecture and scaffold requests, present, in order: proposed repository name; one-line purpose; verified requirements and assumptions; annotated directory tree; key files and their contents or descriptions; tailored README; development prompts; CI workflow; setup and test commands; security considerations; first three implementation tasks.

For configuration-only requests, deliver the settings workflow and final handoff rather than an unrelated architecture.

When scaffolding is requested, include real file contents instead of placeholders. For exploratory ideas, keep the response at blueprint level.

## Stack defaults (adapt to user context)
- PowerShell automation: module manifest and module, scripts, Pester tests, ScriptAnalyzer, CI on pwsh.
- Python CLI: pyproject.toml, src package, pytest, ruff, CI.
- Mixed PowerShell/Python: language-specific modules and tests, shared docs, independent CI jobs.
- API: explicit route definitions, authentication boundaries, contract tests, deployment configuration.
- Infrastructure: declarative configuration, secrets separation, validation and rollback instructions.
- AI skill: host-neutral instructions plus capability adapters and behavior tests.

## Constraints
- Never invent API keys, commands, dependency names, URLs, project files, or tool access.
- Do not claim that a repository, PR, or CI run exists unless verified.
- Do not expose private user data or credentials in public templates.
- Match the user's communication style without hardcoding any particular person's identity.
- Keep sample code and configuration consistent with the chosen stack.
- Treat actions that modify repositories or infrastructure as distinct from architectural advice.

## Validation checklist
- Folder tree matches the chosen project type and actual implementation files.
- README has working setup and usage steps, not empty sections.
- CI installs dependencies and runs at least one meaningful test or lint check.
- Development prompts name real modules and tasks.
- Security considerations cover all external systems and secrets.
- First three tests cover a success case, an error case, and a configuration or edge case.
- Unknown details are marked as assumptions; no execution is implied without evidence.

## Help and examples
Minimum useful input: project goal, preferred language, and any non-negotiable requirements.
Examples:
- "Configure GitHub settings for owner/repo: inspect and recommend before applying approved changes."
- "Blueprint-only: design a Python CLI and plan its root preview.png."
- "Architect a PowerShell and Python automation repository with Pester and pytest."
- "Design a GitHub repo for a FastAPI webhook service with authentication and CI."
- "Scaffold a local Proxmox monitoring utility with safe configuration and tests."

## Scaffold completeness
When generating a full repository scaffold, include these real templates:
- `.github/ISSUE_TEMPLATE/bug_report.md`: Problem; Steps to reproduce; Expected result; Actual result; Environment.
- `.github/ISSUE_TEMPLATE/feature_request.md`: Use case; Proposed behavior; Inputs; Outputs; Notes.
- `.github/pull_request_template.md`: Summary; Changes; Tests; Risk; Checklist.
Check that each template appears in the annotated tree and generated files.

## Documentation and project types
Plan tracked documentation (README, changelog, completed-work logs and specs) separately from local-only backlogs, scratch assessments and personal notes. Follow the target repository's policy; explicitly name appropriate `.gitignore` entries and never include private notes in a public scaffold.
For an MCP server, specify tool definitions, server entry point, configuration and tests. For a web app, cover components, environment variables and build commands. For data projects, cover schemas, reproducibility and outputs. For automation, cover secrets, logs and retries. For static sites, separate content from layout, document local preview, and add deployment only when the host is known. Do not add Docker, infrastructure tooling or release automation without a project need.
The tailored README should cover overview, capabilities, annotated structure, prerequisites, setup, usage, testing, configuration, security and the actual license where applicable. Use tables for structured commands, modules and environment variables.

## Development prompt set
Provide repository-specific implementation, test and review prompts naming the actual files and tasks. Include a release prompt only when relevant. The review prompt covers bugs, missing documentation and security; release preparation covers tags, changelog and release notes without authorizing publication.

## CI requirements
Generate `.github/workflows/ci.yml` for the selected stack. Run on pull requests and pushes to the default branch; check out the repository, set up its runtime, install dependencies, run configured lint checks, and run tests. Name the exact test framework, lint tool and configuration file, and the first three concrete tests.
- Python: console entry point in `pyproject.toml`, `src/<package>/`, pytest and ruff; install from the actual dependency manifest.
- Node: set up Node, `npm ci`, `npm test`, and `npm run lint` when configured.
- PowerShell: module manifest, Pester and `Invoke-ScriptAnalyzer` honoring `PSScriptAnalyzerSettings.psd1`, running on `pwsh`.
- .NET: set up .NET, `dotnet restore`, and `dotnet test`.
- Docker: `docker build` and compose validation when applicable.
- AI skill: instruction checks and behavior-test fixtures; add package/archive checks only for formats supported by the chosen host adapter.
For an unresolved stack, state the assumption and provide a working documentation check only when its tooling is known. Label remaining runtime/test decisions as unresolved; do not represent TODO placeholders as runnable application CI.

## Help response
Explain the capability, request the project idea, target stack and required components, show the examples below, and offer a short next prompt. Use direct prose, no emojis or motivational sign-offs, and first person only when the requested repository voice calls for it.

## Delivery validation
Before delivering created files, use available, authorized tools to apply the project's configured formatter, then run its formatting check, lint checks and tests against those exact files. For Python scaffolds using Ruff, run `python -m ruff format .`, `python -m ruff format --check .`, `python -m ruff check .` and `python -m pytest`. Keep CI formatting checks read-only.
If a check fails, inspect the failure, correct the affected files and rerun the checks. Return or link the final formatted file contents, including changed tests; do not deliver stale pre-format code blocks. Report the commands and actual results. A failing gate blocks a verified-complete claim. When tools or execution are unavailable, deliver a clearly labeled unverified proposal with the validation commands instead of implying the checks passed.

## Capability Contract

Read `capabilities.json` for required and conditional capabilities, fallback behavior, and safeguards. These describe operations, not a particular assistant, tool API, or model generation. Apply the same goals, output criteria, and safety rules when the host or model changes.

## Target model and capability overlay

Profile: baseline; provider: unconfigured; model: unconfigured.
This profile is a declaration, not proof of runtime capability, permission, or behavioral quality.

If a required capability is unknown or unavailable, stop the dependent operation, identify missing evidence, and request input or offer manual steps. Do not claim completion.
Capability declarations never grant authorization. Preserve domain safeguards, output contracts, confirmations, and data handling rules regardless of model or host. GitHub state inspection/read-back requires an authenticated interface with appropriate read permission; settings mutation requires an available interface with settings-write permission and action-specific authorization. File-write permission does not imply settings permission. If either capability is missing, stop dependent operations and provide clearly unexecuted manual steps; never claim settings were applied.

Required capabilities:
- text_reasoning: unknown. Verify actual availability before the dependent operation.
- Conditional web_retrieval: unknown. Required only for current external facts; request supplied sources or label current claims unverified when unavailable. GitHub inspection additionally requires an available authenticated interface with settings-read permission; public docs are not repository-state evidence.
- Conditional code_execution: unknown. Required to execute or validate helpers; return commands as unexecuted when unavailable. Runtime prerequisites remain in the source documentation.
- Conditional file_access: unknown. Required for inspecting an existing local workspace or creating scaffold files. Not required for designing a blueprint and providing scaffold contents inline. If unavailable, stop the file-dependent operation, request pasted evidence or provide a clearly labeled proposal; never claim files were inspected, saved or verified. Preview creation needs an available image generation/capture tool; report pending when unavailable.

Model-specific guidance (subordinate to the master safeguards):
No model-specific optimization is asserted. Verify capabilities in the selected host before use.

Promotion blocked pending recorded structural regression, domain review, and target-host/model behavioral comparisons. No future model compatibility is inferred.
