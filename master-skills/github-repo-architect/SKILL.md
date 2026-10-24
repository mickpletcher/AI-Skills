---
name: github-repo-architect
description: Design a practical, testable Git repository architecture from a project idea, including documentation, CI, and starter files when appropriate.
---
# Git Repository Architect

## Purpose
Turn a software or automation idea into an implementable repository blueprint. Work across languages and AI hosts; never assume a particular tool or repository permission exists.

## Activate when
The user asks to design, scaffold, or architect a new repository, or uses a shorthand such as "repo", "gra", or "architect repo" followed by an idea.

## Do not activate when
- The user asks to audit or refactor an existing repository: use an assessment workflow.
- The user only needs a README for a known layout: use a README-writing workflow.
- There is no concrete project idea: request the minimum useful description.
- The project handles credentials or sensitive infrastructure and its security requirements are unclear: clarify security boundaries first.

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
Present, in order: proposed repository name; one-line purpose; verified requirements and assumptions; annotated directory tree; key files and their contents or descriptions; tailored README; development prompts; CI workflow; setup and test commands; security considerations; first three implementation tasks.

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
