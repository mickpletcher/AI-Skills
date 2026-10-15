# AI Skills

[![Repository validation](https://github.com/mickpletcher/AI-Skills/actions/workflows/validate.yml/badge.svg?branch=main&event=push)](https://github.com/mickpletcher/AI-Skills/actions/workflows/validate.yml?query=branch%3Amain)
[![Installer regression tests](https://github.com/mickpletcher/AI-Skills/actions/workflows/installer-tests.yml/badge.svg?branch=main&event=push)](https://github.com/mickpletcher/AI-Skills/actions/workflows/installer-tests.yml?query=branch%3Amain)
[![Master skill generation validation](https://github.com/mickpletcher/AI-Skills/actions/workflows/master-skills-validation.yml/badge.svg?branch=main&event=push)](https://github.com/mickpletcher/AI-Skills/actions/workflows/master-skills-validation.yml?query=branch%3Amain)
[![License](https://img.shields.io/github/license/mickpletcher/AI-Skills)](./LICENSE)

A shared home for AI skills organized by platform. Skills live under the platform they are written for. Shared docs cover conventions and repo guidance only.

See [completed-projects.md](./completed-projects.md) for completed repo additions.
See [completed-upgrades.md](./completed-upgrades.md) for completed repo upgrades.
See [changelog.md](./changelog.md) for the repo change history.
See [skill-improvement-assessment.md](./skill-improvement-assessment.md) for the current skill quality review.

Current repo social preview asset:

- [.github/github-social-preview.jpg](./.github/github-social-preview.jpg)

## Start Here If You Are New

Use this repo in this order:

1. Pick the platform you want to use first.
2. Open that platform's skill folder.
3. Read the skill `README.md` before anything else.
4. Open the main source file for that skill.
5. Copy the skill into the target app using the platform steps below.
6. Test it with one simple prompt before relying on it.

If you are not sure which file is the source of truth:

- Claude skills usually use `SKILL.md`
- ChatGPT skills usually use `instructions.md`
- Copilot skills should use the main instruction file stored in that skill folder
- Gemini skills will usually use `instructions.md`
- Perplexity skills will usually use `SKILL.md`
- Cursor skills will usually use `instructions.md`

## How To Implement A Skill In Each Ecosystem

These steps are written for a first time user.

### Claude

Claude skills in this repo live under `claude/skills/<skill-name>/`.

What to open:

1. Open the skill folder.
2. Read `README.md`.
3. Open `SKILL.md`.
4. If the folder includes a `.skill` file, that is the packaged Claude import file.

How to implement it:

1. Open Claude.
2. If you use packaged imports, import the `.skill` file from that skill folder.
3. If you manage Claude skills manually, place the skill files in the local Claude skills location you use on your machine.
4. Refresh Claude or start a new chat so the skill is available.
5. Test it with one of the example prompts from the skill `README.md` or `SKILL.md`.

What to expect:

- `SKILL.md` is the editable source
- `.skill` is the install or import artifact
- `README.md` explains what the skill does and how to test it

If you change a Claude skill:

1. Edit `SKILL.md` first.
2. Update `README.md` if the setup or behavior changed.
3. Rebuild the `.skill` package so the import file matches the source.
4. Test again in Claude.

### ChatGPT

ChatGPT skills in this repo live under `chatgpt/skills/<skill-name>/`.

What to open:

1. Open the skill folder.
2. Read `README.md`.
3. Open `instructions.md`.

How to implement it with a custom GPT:

1. Open ChatGPT.
2. Create a new custom GPT, or edit an existing one.
3. Copy the full contents of `instructions.md`.
4. Paste that content into the GPT instructions area.
5. Save the GPT.
6. Test it with one of the prompts from the skill `README.md`.

How to implement it with Custom Instructions:

1. Open ChatGPT.
2. Open `Settings`.
3. Open `Custom Instructions`.
4. Copy the full contents of `instructions.md`.
5. Paste it into the instruction area that controls how ChatGPT should respond.
6. Save changes.
7. Start a new chat and test it.

What to expect:

- `instructions.md` is the editable source
- `README.md` explains where to paste it and how to test it
- A custom GPT is usually the safer option because it does not affect unrelated chats

### GitHub Copilot

Copilot skills in this repo live under `copilot/skills/<skill-name>/`.

What to open:

1. Open the skill folder.
2. Read `README.md`.
3. Open the main instruction file for that skill, usually `instructions.md`.

How to implement it:

1. Decide where you want Copilot to use the skill:
   - repo level instructions
   - a prompt file
   - a one time chat paste
2. Copy the full contents of the skill instruction file.
3. Paste it into the Copilot surface you are using.
4. If the target repo already has instructions, merge carefully instead of overwriting unrelated rules.
5. Test it with a small real task.

What to expect:

- Copilot skills are instruction driven, not packaged like Claude `.skill` files
- The exact place you paste the instructions depends on the Copilot surface you use
- The skill folder should still contain a beginner friendly `README.md` and one clear source file

Current example:

- [copilot/skills/pr-review](./copilot/skills/pr-review/)

### Gemini

Gemini skills in this repo will live under `gemini/skills/<skill-name>/`.

What to open:

1. Open the skill folder.
2. Read `README.md`.
3. Open the main instruction file, usually `instructions.md`.

How to implement it:

1. Open Gemini.
2. Create or edit the Gem or reusable assistant setup you want to use.
3. Copy the full contents of the skill instruction file.
4. Paste that content into the Gemini instruction area.
5. Save the Gem or assistant.
6. Test it with one simple prompt from the skill README.

What to expect:

- Gemini skills are instruction driven
- The skill folder should explain the exact Gemini surface it targets
- This repo does not yet include a live Gemini skill example

### Perplexity

Perplexity skills in this repo will live under `perplexity/skills/<skill-name>/`.

What to open:

1. Open the skill folder.
2. Read `README.md`.
3. Open the main source file, usually `SKILL.md`.

How to implement it:

1. Open Perplexity.
2. Create a new skill or edit an existing one.
3. Copy the full contents of the source file, or upload the packaged artifact if that skill README calls for it.
4. Save the skill.
5. Test it with one prompt from the skill README.

What to expect:

- Perplexity is the closest match to a true skill workflow outside Claude in this repo plan
- The skill README should say whether to paste Markdown directly or upload a file
- This repo does not yet include a live Perplexity skill example

### Cursor

Cursor skills in this repo will live under `cursor/skills/<skill-name>/`.

What to open:

1. Open the skill folder.
2. Read `README.md`.
3. Open the main instruction file, usually `instructions.md`.

How to implement it:

1. Open Cursor.
2. Decide whether the instructions belong in project rules, user rules, or a one time chat context.
3. Copy the full contents of the skill instruction file.
4. Paste it into the chosen Cursor rule or instruction surface.
5. Test it on a small real coding task.

What to expect:

- Cursor skills are reusable coding rules rather than packaged skill files
- The skill folder should say whether the instructions are meant for project scope or user scope

Current examples:

- [cursor/skills/pr-review](./cursor/skills/pr-review/)
- [cursor/skills/workflow-debugger](./cursor/skills/workflow-debugger/)
- [cursor/skills/repo-assessment](./cursor/skills/repo-assessment/)
- [cursor/skills/spec-writer](./cursor/skills/spec-writer/)

## Platform Quick Map

| Platform | Skill folder | Main source file | How you usually apply it |
| ----- | ----- | ----- | ----- |
| Claude | `claude/skills/<skill-name>/` | `SKILL.md` | Import or install the `.skill` package, then test in Claude |
| ChatGPT | `chatgpt/skills/<skill-name>/` | `instructions.md` | Paste into a custom GPT or ChatGPT Custom Instructions |
| Copilot | `copilot/skills/<skill-name>/` | platform instruction file | Paste into the Copilot instruction surface used by that repo or workflow |
| Gemini | `gemini/skills/<skill-name>/` | `instructions.md` | Paste into a Gemini Gem or equivalent Gemini instruction surface |
| Perplexity | `perplexity/skills/<skill-name>/` | `SKILL.md` | Paste Markdown directly or upload the skill file, depending on the skill README |
| Cursor | `cursor/skills/<skill-name>/` | `instructions.md` | Paste into project rules, user rules, or chat context in Cursor |

## Complete Skill Catalog

Use the [generated catalog](CATALOG.md) for every shipped skill across all platforms, including purpose, installation, declared prerequisites, package links, and versions. [catalog.json](catalog.json) provides the machine-readable manifest and [SHA256SUMS](SHA256SUMS) records package hashes. Undeclared versions/prerequisites and model-evaluation dates are never invented.

See [platform installation](docs/installation.md), [dependencies](docs/dependencies.md), [contributing](CONTRIBUTING.md), [behavioral evaluations](evaluations/README.md), and [distribution and licensing](docs/distribution.md).

## Repository Structure

- `shared/`: repo-wide guidance, standards, and naming rules
- `templates/`: starter templates for new skills
- `claude/`: Claude-specific skills, scripts, and metadata
- `chatgpt/`: ChatGPT-specific instructions, prompts, and schemas
- `copilot/`: GitHub Copilot instructions and prompts
- `gemini/`: Gemini-specific instructions and Gem-ready skill content
- `perplexity/`: Perplexity-specific skill files and setup notes
- `cursor/`: Cursor-specific rules and coding assistant instructions

## Working Model

1. Pick the target platform first.
2. Write the skill in that platform's folder as the source of truth.
3. Use `shared/` for naming, structure, and repo-level guidance only.
4. Record checks with [templates/test-template.md](./templates/test-template.md).

For Claude skills, keep tracked shipped history in `completedchanges.md` and keep local `future-upgrades.md` files focused on future planning only.

## Spec Workflow

Use [`specs/`](./specs/) for non-trivial repo work such as shared conventions, packaging rules, cross-skill changes, or shared script updates.

Skip it for small single-skill wording edits or minor doc cleanup.

## Start Here

- [shared/skill-standard.md](./shared/skill-standard.md) before creating a new skill
- [shared/platform-organization.md](./shared/platform-organization.md) for folder intent
- [templates/skill-template.md](./templates/skill-template.md) as the base template
- [templates/chatgpt-skill-template.md](./templates/chatgpt-skill-template.md) for ChatGPT specific instruction wrappers
- [specs/001-skill-repo-workflow/](./specs/001-skill-repo-workflow/) for the repo-level spec baseline
- [claude/scripts/Update-FutureUpgrades.ps1](./claude/scripts/Update-FutureUpgrades.ps1) to create or refresh skill `future-upgrades.md` files from `upgrades.md`

## License

Licensed under the [MIT License](LICENSE), copyright 2026 Mick Pletcher. Existing third-party licenses and attribution notices remain applicable.
