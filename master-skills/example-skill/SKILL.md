---
name: example-skill
description: Demonstrate a reusable cross-platform skill without accessing external systems.
---
# Example skill

## When to use
When a user asks for a concise task plan.

## Workflow
Ask for the objective if missing. Provide three actionable steps and one verification check.

## Constraints
Never claim to have performed an action without evidence.

## Capability Contract

Read `capabilities.json` for required and conditional capabilities, fallback behavior, and safeguards. These describe operations, not a particular assistant, tool API, or model generation. Apply the same goals, output criteria, and safety rules when the host or model changes.
