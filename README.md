# AI Skills

This repository is a shared home for reusable AI skills that can be adapted for Claude, ChatGPT, and VS Code GitHub Copilot.

The goal is to keep each skill portable at its core, then add tool-specific wrappers only where a platform genuinely needs them.

## Repository Structure

- `shared/`: cross-platform standards, naming rules, and portability guidance
- `templates/`: starter templates for portable skills and platform-specific variants
- `claude/`: Claude-oriented skill implementations and examples
- `chatgpt/`: ChatGPT-oriented skill implementations and support material
- `copilot/`: GitHub Copilot-oriented instructions and prompts
- `docs/`: supporting documentation and future process docs

## Working Model

Create skills in this order:

1. Define the portable intent of the skill.
2. Capture the shared contract in a platform-neutral format.
3. Add Claude, ChatGPT, and Copilot variants only where behavior or packaging differs.
4. Test the skill against representative prompts before treating it as reusable.

## Start Here

- Read [shared/skill-standard.md](./shared/skill-standard.md) before creating a new skill.
- Use [templates/portable-skill-template.md](./templates/portable-skill-template.md) for the canonical source.
- Use the platform templates in `templates/` only after the portable version is clear.
- Record checks with [templates/test-template.md](./templates/test-template.md).

## Current Recommendation

This repo does not need GitHub Spec yet.

The better first step is to stabilize the portable skill standard and keep new skills consistent. If the standard becomes complex, gains automation, or needs strict change control, GitHub Spec will start making sense.
