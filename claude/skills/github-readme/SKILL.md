---
name: github-readme
description: Generate polished GitHub README.md files for Mick's repositories in his established voice and structure. Always trigger immediately when the user's message starts with "readme" or "gr". Also trigger on "write a readme", "generate readme", "readme for this repo", "document this repo", or any request to create or rewrite a GitHub README. Produces a complete, repo-specific README with the right sections for the project instead of a generic template.
---

# GitHub README Skill

Write polished, complete `README.md` files for GitHub repositories in a direct, technical, practitioner-focused voice.

## Primary Triggers

Use this skill when the user starts with `readme` or `gr`, or asks to write, rewrite, or document a repository README.

```text
readme [paste repo description, file list, or context]
gr [GitHub URL or repo name + description]
write a readme
generate readme
readme for this repo
document this repo
rewrite my readme
```

## Workflow

### 1. Identify the repo type

Choose the closest repo type before writing anything. That choice determines the section set.

| Type | Examples | Typical Sections |
| --- | --- | --- |
| Skills or config library | Anthropic, PiHole blocklists | Overview, contents table, install, repo structure, related repos |
| Code toolkit or multi-module repo | AlpacaTrading, SafeSend | Overview, what it does, feature table, repo structure, setup, env vars, usage by module, errors, license |
| Single script or utility | PowerShell automation scripts | Overview, what it does, prerequisites, usage, parameters, examples, license |
| MCP server | homeassistant-mcp, pihole-mcp | Overview, what it does, tools table, install and config, usage, notes, license |
| API integration or webhook | SafeSend webhooks | Overview, what it does, endpoint table, auth, payload schemas, setup, examples, license |

If the repo does not fit neatly, pick the closest type and drop irrelevant sections.

### 2. Extract source material

Pull from the best available source in this order:

1. Repository file tree or local files
2. Existing `README.md`
3. User-provided repo description or context
4. GitHub URL or repo name when the user provides one

Extract the repo purpose, languages, major folders and scripts, dependencies, setup steps, intended audience, and any non-obvious constraints.

When current details matter and a URL is provided, verify them before writing.

### 3. Write the README

Build a complete `README.md` that fits the repo instead of filling a fixed template.

## Universal Rules

- No emojis anywhere in the document
- Avoid em dashes in final README output
- No marketing language such as "powerful", "robust", "seamless", "cutting-edge", "game-changing", "leverages", or "revolutionary"
- No motivational sign-offs
- Use plain prose with short sentences and active voice
- Use tables for structured data such as modules, env vars, errors, parameters, or tools
- Use code blocks for commands, paths, config snippets, and examples
- Include an MIT license section when the repo uses MIT
- Include an annotated repo structure when it adds clarity
- Never include empty sections

## Section Building Blocks

Use only the sections that fit the repo.

### `# [Repo Title]`

Use a readable H1 that matches the repo name. Do not add a marketing tagline.

Example:

```markdown
# Alpaca Trading Toolkit
```

### Description line

Put one plain sentence under the H1 explaining what the repo is and what it does.

### `## Overview`

Write 2 to 4 sentences describing what the repo contains and who it is for. Do not put setup steps here.

### `## What This Does`

Use for toolkits or multi-module repos when a plain overview is not enough.

### `## Skills`, `## Modules`, or `## Tools`

Use a table when the repo has multiple components.

Skills example:

```markdown
| Skill | Trigger | Description |
| --- | --- | --- |
| [skill-name](link) | `trigger` | What it does in one sentence |
```

Code toolkit example:

```markdown
| Module | Purpose | Typical User | Main Outputs |
| --- | --- | --- | --- |
| `src/` | PowerShell module suite for the Alpaca API | PowerShell engineers | account objects, order results |
```

MCP server example:

```markdown
| Tool | Description |
| --- | --- |
| `tool_name` | What the tool does |
```

### `## Repository Structure`

Use an annotated file tree when the repo shape matters.

```text
RepoName/
|-- README.md
|-- module/
|   |-- file.ps1    # What this file does
|   `-- file.py     # What this file does
```

For larger repos, annotate folders instead of every file.

### `## Prerequisites`

Use a short list of required software, tools, accounts, or versions. Do not put setup steps here.

### `## Installation` or `## Setup`

Use numbered steps with exact commands. Avoid vague instructions.

For skills repos, include the relevant skills path and installation flow only if the repo really needs them.

For code repos, include clone, environment setup, dependency install, and config setup when applicable.

### `## Environment Variables`

Use a table with `Variable | Required | Example | What It Controls` when the repo uses environment-based config.

### `## Usage`

Show the safest, simplest command first. For multi-module repos, use one subsection per major component when needed.

### `## Common Errors`

Use a `Problem | Likely Cause | Fix` table only when the repo has non-obvious failure modes.

### `## Security Notes`

Use a short factual list for repos that handle credentials, keys, or sensitive data.

### `## Related Repositories`

Add a `Repo | Description` table when related repos help orient the reader.

### `## Blog`

Use only when it clearly helps a public-facing repo. Keep it to one line.

### `## License`

Keep it last. Match the actual repo license.

Example:

```markdown
## License

This project is licensed under the MIT License. See `LICENSE` for the full text.
```

## Voice Reference

The tone should be direct, technical, and practical. It should sound like someone who has used the repo, not like product copy.

What it should sound like:

- "This project gives you a step by step workflow for learning systematic trading with Alpaca."
- "Beginner friendly trading tools for learning strategy testing, paper trading, scheduling, and trade review without risking real money."
- "Skills are organized around three areas: content creation, technical automation, and infrastructure and project work."

What it should not sound like:

- "This powerful, cutting-edge toolkit leverages the Alpaca API to supercharge your trading workflow."
- "Feel free to explore the modules and happy coding."

## Output Expectations

Produce the complete `README.md` content directly in the response unless the user specifically asks for a file edit in a local repo.

If the user is asking about a real local repository, base the README on the actual repo structure and docs instead of guessing.

When you finish, briefly confirm:

- the repo name
- the repo type you used
- any major sections you intentionally included or omitted
