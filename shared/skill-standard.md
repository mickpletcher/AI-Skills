# Skill Authoring Standard

This document defines the minimum standard for writing a skill in this repository.

Skills should be authored inside the platform folder they belong to. A Claude skill belongs in `claude/`, a ChatGPT skill belongs in `chatgpt/`, and a Copilot skill belongs in `copilot/`.

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
- examples
- validation or review checks

## Recommended Sections

Most skills in this repo should include these sections:

1. `Name` or platform metadata header
2. `Intent`
3. `Trigger When` or `Use When`
4. `Do Not Use When`
5. `Workflow`
6. `Constraints`
7. `References`
8. `Examples`
9. `Validation Checklist` or `Test Cases`

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
- it includes at least 2 examples or equivalent usage guidance
- it includes at least 3 validation checks or test cases

## Design Principle

Keep shared guidance in `shared/`, but keep the actual skill definition in the platform folder that owns it.
