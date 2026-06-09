# Facebook Reply Claude Skill

Claude-specific skill package for writing replies to Facebook comments in Mick's voice.

This skill now uses a checked-in source file instead of the older `skill.md` plus `skill.zip` layout.

## Files

```text
claude/skills/facebook-reply/
|-- README.md
|-- SKILL.md
`-- facebook-reply.skill
|-- upgrades.md
```

## Source Of Truth

- Claude runtime source: [`SKILL.md`](./SKILL.md)

Update `SKILL.md` when the Facebook reply workflow changes, then rebuild `facebook-reply.skill` so the packaged export stays in sync.

## What This Skill Covers

- Writing direct, paste-ready replies to Facebook comments
- Adjusting tone for support, questions, skepticism, or general comments
- Switching between appreciative, clarifying, humorous, and boundary setting reply modes
- Using the original post topic and commenter context when it changes how the reply should land
- Choosing concise or fuller replies based on the comment depth
- Handling criticism, skepticism, hostility, and off-topic comments without escalating
- Writing distinct replies for batches of comments from the same post
- Drafting one pinned clarification reply when the same question keeps repeating
- Tagging sentiment before replying so hostile, neutral, skeptical, and supportive comments get different treatment
- Preserving Mick's casual, confident voice without sounding canned

## Related Skill

- [facebook-post](../facebook-post/README.md)

## Behavior

- `fbr` triggers the skill immediately
- The skill infers a tone mode unless you specify one
- The skill infers concise or fuller reply depth unless you specify one
- The skill uses the original post topic and commenter context when provided
- The skill can produce separate replies for multiple comments on the same post
- The skill can draft one pinned clarification reply for repeated questions in a thread

## Supported Tone Modes

- `appreciative`
- `clarifying`
- `humorous`
- `boundary setting`

## Supported Reply Depth

- `concise`
- `fuller`

## Example Prompts

```text
fbr reply to this supportive comment about my off grid build

fbr use a clarifying reply to answer this question about my Intune automation post

fbr give me concise replies for these 4 comments on the same post and keep them distinct

fbr summarize the repeated battery questions in this thread and draft one pinned clarification reply

fbr reply to this skeptical comment without escalating
```

## Installation

Package `SKILL.md` into `facebook-reply.skill`, then install it with your normal Claude skill workflow.

## Upgrade Log

See [upgrades.md](upgrades.md) for the structured upgrade log and [completedchanges.md](completedchanges.md) for tracked completed changes.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `facebook-reply.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.

