---
name: blog-post
description: Write or draft a blog post for Mick's IT blog at mickitblog.blogspot.com. Trigger when Mick asks for a blog post or wants to document a technical solution, project, or finding in post format. Match Mick's writing style with plain first-person prose, practical focus, honest status notes, code blocks where relevant, and GitHub links when applicable.
version: 1.0.0
---

# Blog Post

## Do Not Use When

- Do not use for social-only posts, marketing copy that does not match Mick's voice, or topics with no source details.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

## Workflow

1. Identify the exact task and available source material.
2. Apply the domain rules and output format in this skill.
3. State assumptions, uncertainty, and missing inputs clearly.
4. Return the requested artifact, recommendation, or review in a practical format.
5. Check the result against the validation checklist before finishing.

Use this skill when the user wants a blog post written in Mick's style for `mickitblog.blogspot.com`.

## Trigger When

- The user says `blog post`, `write a post for my blog`, or mentions `mickitblog`.
- The request is to document a technical solution, project, migration, script, or finding in post format.
- The user already has notes and wants them turned into a publishable draft.

## Intent

Write ready-to-publish blog posts that sound like Mick wrote them: direct, first-person, practical, and honest about what is complete versus still in progress.

## Writing Style

- First-person voice as Mick
- Problem or context first, with no long preamble
- Technical but readable for other practitioners
- Practical focus over polished marketing language
- Typical length of 300 to 700 words unless the topic genuinely needs more
- Multi-line code always in fenced code blocks
- Plain GitHub URLs when a repo is relevant
- Honest wording about testing, limitations, and current status

## Tone Rules

- Do not use AI filler phrases such as `delve`, `dive into`, `game-changer`, `seamlessly`, `leverage` as a verb, or `robust`
- Do not start with a question
- Do not end with generic outreach language
- Do not use emojis
- Avoid em dashes in the final post
- Keep punctuation and phrasing plain instead of promotional

## Post Structure

Use this structure unless the topic clearly needs a small variation:

```markdown
## Topic: Specific Thing Done

Opening paragraph with the problem or project context.

## What It Contains

Main body explaining what was built, configured, or discovered.

## Current Status

Honest note on what is complete, partially tested, or still in progress.

## What Comes Next

Short paragraph or short list of next steps.

Plain GitHub URL if relevant.
```

## What To Capture

Extract these from the conversation if they are already present:

1. Topic
2. What was built, configured, or solved
3. Tools and technologies involved
4. Current status
5. Planned next steps
6. GitHub repo link, if one exists

Only ask for missing information that is necessary to write a useful draft.

## Constraints

- Do not sound like a content marketer
- Do not over-explain basic concepts to a technical audience
- Do not hide uncertainty or unfinished work
- Do not pad the post with background that does not help the reader

## Validation Checklist

- [ ] Written in first person as Mick
- [ ] Opens with the problem or context
- [ ] Uses practical technical language without AI filler
- [ ] Includes honest current status
- [ ] Uses fenced code blocks for multi-line code
- [ ] Includes a GitHub link when relevant
- [ ] Avoids em dashes and emojis in the final post

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- A topic plus rough notes, bullets, or source material.

Example prompts:

- `Use blog-post to turn these notes into a post for mickitblog about my Intune reporting script.`
- `Write a blog post in my style about fixing a PowerShell CI issue in one of my repos.`
- `Show me the fastest prompt to use when I have rough bullets and want a finished blog draft.`

