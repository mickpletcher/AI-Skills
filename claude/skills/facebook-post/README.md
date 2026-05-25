# Facebook Post Claude Skill

Claude-specific skill package for writing and polishing Facebook posts in Mick's voice.

This skill now uses a checked-in source file instead of the older `skill.md` plus `skill.zip` layout.

## Files

```text
claude/skills/facebook-post/
|-- README.md
|-- SKILL.md
`-- facebook-post.skill
|-- upgrades.md
```

## Source Of Truth

- Claude runtime source: [`SKILL.md`](./SKILL.md)

Update `SKILL.md` when the Facebook post workflow changes, then rebuild `facebook-post.skill` so the packaged export stays in sync.

## What This Skill Covers

- Rewriting rough drafts into polished Facebook posts
- Preserving specific facts, numbers, and context
- Applying Mick's direct, conversational tone
- Inferring the right post mode for personal updates, technical lessons, project progress, or opinion posts
- Choosing a fitting length from short update, standard, or story
- Building a stronger opening hook without drifting into promotional language
- Adjusting the wording for friends and family, technical peers, or mixed audiences
- Matching the caption to build photos, screenshots, or workout images when that context is present
- Avoiding forced engagement bait when a question would weaken the post
- Repurposing a finished Facebook post into a matching X post
- Producing Facebook, X, and LinkedIn versions from one source draft
- Learning from prior high performing post patterns when you provide them
- Adding relevant hashtags without turning the post into spam

## Behavior

- `fbp` triggers the skill immediately
- The skill infers a post mode unless you specify one
- The skill infers a length preset unless you specify one
- The skill infers an audience mode unless you specify one
- The skill generates a few hook approaches internally, then returns the strongest final draft
- The skill keeps engagement prompts natural and skips them when they would feel forced
- The skill adjusts captions when the draft is tied to a photo, screenshot, or workout image
- The skill can also produce a matching X version when you ask for repurpose mode
- The skill can produce a labeled Facebook, X, and LinkedIn bundle when you ask for cross-platform output
- The skill can use prior post performance signals to improve the next draft when you provide examples or notes
- It returns one finished Facebook post by default rather than a menu of options

## Supported Modes

- `personal update`
- `technical lesson`
- `project progress`
- `opinion`
- `repurpose to X`
- `cross-platform bundle`
- `feedback guided`

## Supported Length Presets

- `short update`
- `standard`
- `story`

## Supported Audience Modes

- `friends and family`
- `technical peers`
- `mixed audience`

If you want a specific result, include the mode, length, or audience in your prompt. Example: `fbp turn this into a short technical lesson post for mixed audience`.

## Example Prompts

```text
fbp automated Intune compliance reporting for 4,000 endpoints and cut a 2 hour process down to 3 minutes

fbp make this a short project progress post about welding the container corner reinforcements today

fbp rewrite this as an opinion post about why simple PowerShell automation still beats overbuilt tooling

fbp make this fit a screenshot post for technical peers without adding a forced question at the end

fbp turn this into a friends and family update that matches a workout photo

fbp repurpose this Facebook post into a matching X post

fbp make this one source draft into Facebook, X, and LinkedIn versions

fbp use the hook style from my prior high comment project posts and rewrite this update
```

## Installation

Package `SKILL.md` into `facebook-post.skill`, then install it with your normal Claude skill workflow.

## Upgrade Log

See [upgrades.md](upgrades.md) for the structured upgrade log and [completed-changes.md](completed-changes.md) for tracked completed changes.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `facebook-post.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.

