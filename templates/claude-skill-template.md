# Claude Skill Wrapper Template

Use this for a Claude-specific skill.

## Skill Reference

- Skill name: `skill-name`
- Claude surface: `skill file | instruction set | other`

## Claude-Specific Notes

- Note required Claude metadata or packaging.
- Keep the workflow aligned with the real task or repo context.
- Document the rules that are specific to Claude.
- Include a help response path for users who ask how to use the skill.

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
Keep the intent, workflow, constraints, and examples aligned with the real task this skill supports.
```

## Help Response

- Explain what the Claude skill can do in plain language.
- State the minimum useful input.
- Show realistic example prompts.
- Offer the fastest next prompt the user can send.

## Validation

- Verified against intended Claude examples
- Verified against test cases or validation checks
- Claude-specific rules documented
