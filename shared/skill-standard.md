# Skill Authoring Standard

This document defines the minimum standard for writing a skill in this repository.

Skills should be authored inside the platform folder they belong to. A Claude skill belongs in `claude/`, a ChatGPT skill belongs in `chatgpt/`, and a Copilot skill belongs in `copilot/`.

Additional supported platform areas in this repo include `gemini/`, `perplexity/`, and `cursor/`.

## Purpose

A skill should describe a repeatable capability in a way that is:

- clear to a human editor
- usable by the target platform
- testable with example inputs
- maintainable as the platform-specific source of truth

## Source Of Truth

Each skill should have one primary editable source in its platform folder.

That source should capture:

- the skill name
- the problem it solves
- when to use it
- when not to use it
- the expected workflow
- important constraints and safety boundaries
- what to do when the user asks for help
- examples
- validation or review checks

Each skill should also include a beginner friendly implementation path in its platform `README.md`.

## Recommended Sections

Most skills in this repo should include these sections:

1. `Name` or platform metadata header
2. `Intent`
3. `Trigger When` or `Use When`
4. `Do Not Use When`
5. `Workflow`
6. `Constraints`
7. `Help Response`
8. `References`
9. `Examples`
10. `Validation Checklist` or `Test Cases`

## Section Guidance

### Name

Use a short, stable name that describes the capability rather than the implementation.

### Intent

Describe the user problem the skill solves in 2-4 sentences.

### Trigger When Or Use When

List the situations where the skill is appropriate.

### Do Not Use When

Call out nearby scenarios that should use another skill or manual handling.

### Workflow

Document the repeatable process the skill should follow.

### Constraints

Capture important limits, safety boundaries, formatting rules, and things the skill must avoid.

### Help Response

Define the fallback behavior when the user says they do not know how to use the skill or asks for examples.

At minimum, the skill should:

- explain what it can do in plain language
- state the minimum useful input
- show realistic example prompts
- offer the fastest next prompt the user can send

### References

Link the repo docs, files, or external references that the skill depends on.

### Examples

Provide realistic prompts and expected behavior.

### Validation Checklist Or Test Cases

List the checks that confirm the skill still matches the real platform workflow and any live repo dependencies.

## Minimum Quality Bar

A skill is ready to reuse when:

- its intent is specific
- its workflow is concrete
- its constraints are explicit
- it contains an explicit help path for unsure users
- it includes at least 2 examples or equivalent usage guidance
- it includes at least 3 validation checks or test cases
- a novice user can tell where to paste, import, or install it
- the setup steps are written plainly enough to follow without prior repo knowledge

## README Requirement

Each platform skill folder should include a `README.md` that explains:

1. which file is the editable source of truth
2. how to implement the skill in the target ecosystem
3. how to test the setup with one or more simple prompts

If the target ecosystem has more than one reasonable setup path, document the common options directly.

Examples:

- Claude: import the `.skill` file or install the local files manually
- ChatGPT: use a custom GPT or ChatGPT Custom Instructions
- Copilot: place the instruction content into the intended Copilot instruction surface
- Gemini: place the instruction content into a Gemini Gem or equivalent Gemini setup surface
- Perplexity: paste Markdown directly or upload the skill file, depending on the platform workflow
- Cursor: place the instruction content into project rules, user rules, or chat context

## Design Principle

Keep shared guidance in `shared/`, but keep the actual skill definition in the platform folder that owns it.
