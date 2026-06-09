# Platform Organization

Use this guide to decide where files belong in this repository.

## Main Rule

Put a skill under the platform that owns it.

Examples:

- Claude skills go under `claude/`
- ChatGPT skills go under `chatgpt/`
- GitHub Copilot skills go under `copilot/`
- Gemini skills go under `gemini/`
- Perplexity skills go under `perplexity/`
- Cursor skills go under `cursor/`

## What Belongs In `shared/`

`shared/` is for repo-wide guidance such as:

- naming rules
- skill authoring standards
- folder conventions
- review checklists that apply across the repo

Do not put a skill's only source of truth in `shared/`.

## What Belongs In Platform Folders

Platform folders should contain:

- the editable source for the skill
- platform-specific metadata
- packaged exports
- platform-specific examples, prompts, or schemas
- installation notes for that platform
- beginner friendly implementation steps for that platform

## When Shared Content Is Acceptable

Shared content is useful when it is guidance about how to organize or write skills.

Shared content is not the right place for the actual working definition of a Claude-only, ChatGPT-only, or Copilot-only skill.

## Suggested Pattern

For a Claude skill:

```text
claude/
`-- skills/
    `-- skill-name/
        |-- README.md
        |-- SKILL.md
        |-- completedchanges.md
        `-- skill-name.skill
```

Apply the same idea to `chatgpt/` and `copilot/`, using the file formats those platforms expect.

## Beginner Implementation Rule

Every skill folder should make it obvious how a new user actually turns the files in this repo into a working skill.

At minimum, the skill folder `README.md` should answer:

1. Which file is the source of truth
2. Where the user must paste, import, or install that content
3. What file is the packaged artifact, if one exists
4. How to run one simple validation test after setup

Use plain language. Do not assume the reader already knows where Claude, ChatGPT, or Copilot stores instructions.

## Platform Expectations

### Claude

- Source file is usually `SKILL.md`
- Packaged artifact is usually `<skill-name>.skill`
- `README.md` should explain how to import or install the `.skill` file and how to test it

### ChatGPT

- Source file is usually `instructions.md`
- `README.md` should explain how to use the file in a custom GPT and in ChatGPT Custom Instructions

### Copilot

- Source file should be a clear instruction file in the skill folder
- `README.md` should explain which Copilot instruction surface the content is meant for
- If the repo does not yet have a live Copilot example, say that plainly instead of implying a finished workflow exists
- This repo now includes `copilot/skills/pr-review/` as the first concrete Copilot example

### Gemini

- Source file will usually be `instructions.md`
- `README.md` should explain whether the content is meant for a Gemini Gem or another Gemini instruction surface
- If the repo does not yet have a live Gemini example, say that plainly

### Perplexity

- Source file will usually be `SKILL.md`
- `README.md` should explain whether the content should be pasted as Markdown or uploaded as a file
- If the repo does not yet have a live Perplexity example, say that plainly

### Cursor

- Source file will usually be `instructions.md`
- `README.md` should explain whether the content is meant for project rules, user rules, or temporary chat context
- If the repo does not yet have a live Cursor example, say that plainly
- This repo now includes `cursor/skills/pr-review/`, `cursor/skills/workflow-debugger/`, `cursor/skills/repo-assessment/`, and `cursor/skills/spec-writer/` as concrete Cursor examples
