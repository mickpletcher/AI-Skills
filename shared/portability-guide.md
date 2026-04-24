# Portability Guide

Use this guide when adapting a skill across Claude, ChatGPT, and GitHub Copilot.

## Portability First

Start from the portable skill, not from a vendor-specific prompt.

Before creating a platform variant, ask:

- Is the underlying capability the same?
- Is the difference only packaging or metadata?
- Can the shared workflow stay identical?

If the answer is yes, keep one portable source and write a thin platform wrapper.

## What Should Stay Shared

These parts should usually remain identical across platforms:

- intent
- use cases
- workflow
- constraints
- examples
- tests

## What Can Vary

These parts may need adaptation:

- metadata format
- invocation syntax
- tool registration format
- system-prompt or instruction wrapper
- schema shape required by a platform
- file placement conventions

## Drift Warnings

Skills become hard to maintain when:

- each platform copy is edited separately
- examples diverge for no reason
- one platform gains rules that never flow back to the portable source
- naming differs between the same logical skill

When this happens, update the portable source first, then regenerate or revise platform variants.

## Adaptation Pattern

Use this pattern for every new skill:

1. Write the portable skill.
2. Mark which parts are universal and which are platform-specific.
3. Create platform wrappers.
4. Run the same test cases against each variant.
5. Fix drift in the portable source before fixing individual copies.

## Good Reason To Fork

Create a truly separate platform skill only when:

- the platform supports a different capability surface
- the interaction model is materially different
- required tooling changes the workflow itself

Different metadata alone is not a good enough reason to fork the skill.
