# AI Skills

This repository is a shared home for AI skills organized by platform.

Skills in this repo should live under the platform they are written for, such as `claude/`, `chatgpt/`, or `copilot/`. Shared docs are for conventions and repo guidance, not as a cross-platform source of truth for every skill.

## Repository Structure

- `shared/`: repo-wide guidance, standards, naming rules, and organization notes
- `templates/`: starter templates for new skills and validation notes
- `claude/`: Claude-specific skills, wrappers, metadata, and packaged exports
- `chatgpt/`: ChatGPT-specific instructions, prompts, schemas, and support material
- `copilot/`: GitHub Copilot-specific instructions and prompts
- `docs/`: supporting documentation and future process docs

## Working Model

Create skills directly inside the platform folder where they belong:

1. Pick the target platform first.
2. Write the skill in that platform's folder as the source of truth.
3. Use `shared/` for naming, structure, and repo-level guidance only.
4. Record checks with [templates/test-template.md](./templates/test-template.md).

## Start Here

- Read [shared/skill-standard.md](./shared/skill-standard.md) before creating a new skill.
- Read [shared/platform-organization.md](./shared/platform-organization.md) for folder intent.
- Use [templates/skill-template.md](./templates/skill-template.md) as the base template.
- Use platform-specific templates in `templates/` when needed.

## Current Recommendation

This repo still does not need GitHub Spec yet.

The higher-value step is to establish clean platform-specific skill conventions and keep each platform folder organized. If the repo later gains automation, schema validation, packaging pipelines, or a formal contribution workflow, GitHub Spec may become useful.
