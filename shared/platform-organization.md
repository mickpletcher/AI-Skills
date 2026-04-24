# Platform Organization

Use this guide to decide where files belong in this repository.

## Main Rule

Put a skill under the platform that owns it.

Examples:

- Claude skills go under `claude/`
- ChatGPT skills go under `chatgpt/`
- GitHub Copilot skills go under `copilot/`

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
        `-- skill-name.skill
```

Apply the same idea to `chatgpt/` and `copilot/`, using the file formats those platforms expect.
