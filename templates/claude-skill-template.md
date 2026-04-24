# Claude Skill Wrapper Template

Use this after the portable skill is defined.

## Skill Reference

- Portable source: `shared or canonical path here`
- Skill name: `skill-name`
- Claude surface: `skill file | instruction set | other`

## Claude-Specific Notes

- Note required Claude metadata or packaging.
- Keep the workflow aligned with the portable source.
- Only document differences that are specific to Claude.

## Metadata

```yaml
---
name: skill-name
description: Brief description of the skill
version: 1.0.0
---
```

## Adapted Instructions

```text
Insert the Claude-specific wrapper here.
Keep the shared intent, workflow, constraints, and examples aligned with the portable source.
```

## Validation

- Verified against the portable examples
- Verified against the portable test cases
- Claude-only differences documented
