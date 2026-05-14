# linkedin-post

A Claude skill for writing LinkedIn posts in Mick Pletcher's professional voice.

## Source of Truth

Use [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/linkedin-post/SKILL.md) as the canonical source for this skill. The packaged [linkedin-post.skill](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/linkedin-post/linkedin-post.skill) file is the Claude-ready export built from it.

## What It Does

Generates ready-to-post LinkedIn content for Mick's professional audience: IT peers, automation engineers, AI practitioners, and enterprise tech contacts. It should be more polished than Facebook, less casual than X, and always first-person and direct without corporate-speak.

It now supports explicit post modes, LinkedIn tuned hook styles, credibility checks, CTA styles, tone controls, and audience testing variants.

## Trigger Phrases

| Phrase | Action |
| --- | --- |
| `lnp` | Immediate trigger, write the post without asking follow-up questions |
| `linkedin post about...` | Write a post on the given topic |
| `write something for LinkedIn` | Draft from the provided context |

## Content Pillars

1. Home AI infrastructure
2. Enterprise automation
3. Algorithmic trading
4. Career and community
5. Tech commentary

## Supported Post Modes

- `career update`
- `technical lesson`
- `project breakdown`
- `opinion`

## Supported Tone Controls

- `practitioner`
- `leadership`
- `builder`

## Supported CTA Styles

- `hiring`
- `networking`
- `repo traffic`
- `discussion`
- `none`

## Format Rules

- No emojis
- Avoid em dashes in final LinkedIn post output
- No bullet points unless genuinely listing three or more discrete items
- 150 to 400 words
- Short paragraphs, 2 to 3 sentences each
- 2 to 3 hashtags at the bottom only
- No filler phrases or AI-sounding language

## Behavior

- `lnp` triggers the skill immediately
- The skill infers a post mode unless you specify one
- The skill checks for proof, outcome, and context before finalizing the draft
- The skill can apply a CTA style when it fits
- The skill can produce a more technical variant and a broader professional variant when asked

## Example Prompts

```text
lnp turn this into a technical lesson for practitioner audience

lnp write this as a project breakdown with a repo traffic CTA

lnp make this a leadership tone career update

lnp give me one technical version and one broader professional version

lnp rewrite this opinion post with a stronger LinkedIn hook and better proof
```

## File Structure

```text
linkedin-post/
|-- README.md
|-- SKILL.md
`-- linkedin-post.skill
|-- upgrades.md
```

## Upgrade Log

See [upgrades.md](upgrades.md) for the structured upgrade log and [completedchanges.md](completedchanges.md) for tracked completed changes.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `linkedin-post.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.

