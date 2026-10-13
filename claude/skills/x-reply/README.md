# x-reply

A Claude skill for writing replies to replies on X.

## Source of Truth

Use [SKILL.md](SKILL.md) as the canonical source for this skill. The packaged [x-reply.skill](x-reply.skill) file is the Claude-ready export built from it.

## Trigger

Start any message with `xr` to activate this skill. Paste the reply being responded to after it. Original post context is optional but helpful.

## What It Does

This skill:

- identifies the reply type
- adjusts tone automatically
- generates a response within 280 characters
- shows the character count
- keeps the reply direct and thread-appropriate

## Related Skills

- [x-post](../x-post/README.md)
- [facebook-post](../facebook-post/README.md)
- [facebook-reply](../facebook-reply/README.md)

## File Structure

```text
x-reply/
|-- README.md
|-- SKILL.md
`-- x-reply.skill
|-- upgrades.md
```

## Upgrade Log

See [upgrades.md](upgrades.md) for the structured upgrade log and [completedchanges.md](completedchanges.md) for tracked completed changes.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `x-reply.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.

