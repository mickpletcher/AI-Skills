# Portable Skill Standard

This document defines the minimum standard for a skill that should be adaptable across Claude, ChatGPT, and GitHub Copilot.

## Purpose

A portable skill should describe a repeatable capability in a way that is:

- clear to a human editor
- easy to adapt for multiple AI products
- testable with example inputs
- stable enough to evolve without rewriting from scratch per platform

## Canonical Source

Every skill should have one platform-neutral source of truth before tool-specific variants are created.

The canonical source should capture:

- the skill name
- the problem it solves
- when to use it
- required inputs and assumptions
- expected outputs
- workflow or execution steps
- constraints and safety boundaries
- examples
- test cases

## Required Sections

Each portable skill should include these sections in this order:

1. `Name`
2. `Intent`
3. `Use When`
4. `Do Not Use When`
5. `Inputs`
6. `Outputs`
7. `Workflow`
8. `Constraints`
9. `Platform Notes`
10. `Examples`
11. `Test Cases`
12. `Maintenance Notes`

## Section Guidance

### Name

Use a short, stable name that describes the capability rather than the implementation.

### Intent

Describe the user problem the skill solves in 2-4 sentences.

### Use When

List the situations where the skill is appropriate.

### Do Not Use When

Call out nearby scenarios that should use a different skill or a manual workflow.

### Inputs

List the minimum information the skill needs to work well.

### Outputs

Describe the expected shape of the result. Focus on user-visible outcomes, not internal reasoning.

### Workflow

Document the repeatable process the skill should follow. Keep this procedural and platform-neutral.

### Constraints

Capture important limits, safety boundaries, formatting rules, and things the skill must avoid.

### Platform Notes

Document only the differences that matter for Claude, ChatGPT, or Copilot. Avoid copying the whole skill into three separate notes when the core behavior is the same.

### Examples

Provide realistic examples of prompts and expected behavior.

### Test Cases

List checks that confirm the skill works as intended across platforms.

### Maintenance Notes

Note owners, drift risks, linked docs, or review triggers.

## Minimum Quality Bar

A skill is ready to reuse when:

- its intent is specific
- its workflow is concrete
- its constraints are explicit
- it includes at least 2 examples
- it includes at least 3 test cases
- platform differences are documented without forking the core logic

## Versioning Guidance

Increase the skill version when behavior changes in a user-visible way. Do not bump versions for minor wording cleanup unless the wording changes expected outcomes.

## Design Principle

Write once at the portable layer. Specialize only where a platform forces you to.
