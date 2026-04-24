# github-readme

A Claude skill for writing polished `README.md` files for GitHub repositories in a direct, technical, practitioner-focused voice.

## Source of Truth

Use [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/github-readme/SKILL.md) as the canonical source for this skill. The packaged [github-readme.skill](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/github-readme/github-readme.skill) file is the Claude-ready export built from it.

## Trigger

Start any message with `readme` or `gr` to activate this skill immediately. It also applies to natural-language requests to write, rewrite, or document a repository README.

```text
readme [paste repo description, file list, or context]
gr [GitHub URL or repo name + description]
write a readme
generate readme
readme for this repo
document this repo
rewrite my readme
```

## What It Does

Reads the repository context you provide and produces a complete, repo-specific `README.md`. The output should match the actual project instead of falling back to a generic template.

The skill should:

- identify the repository type before writing
- pull source material from the repo tree, existing docs, URLs, or user-provided context
- choose only the sections that fit the repo
- write in a plain, technical voice without filler or marketing language

## Style Rules

- No emojis
- Avoid em dashes in final README output
- No marketing language such as "powerful", "robust", "seamless", "cutting-edge", "game-changing", or "leverages"
- No motivational sign-offs
- Use short sentences, active voice, and practitioner tone
- Use tables for structured data
- Use code blocks for runnable commands and config
- Include an MIT license section when the repo uses MIT
- Include an annotated file tree when the repo structure is large enough to benefit from it

## File Structure

```text
github-readme/
|-- README.md
|-- SKILL.md
`-- github-readme.skill
|-- upgrades.md
```

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `github-readme.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
