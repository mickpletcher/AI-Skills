---
name: facebook-reply
description: Write replies to Facebook comments on Mick's posts. Trigger on requests to reply to a Facebook comment, especially when the user starts with `fbr`.
version: 1.0.0
---

# Facebook Reply

Write replies to Facebook comments in Mick's direct, casual voice. Adjust the tone based on whether the comment is supportive, a question, skepticism, or something more general.

## Trigger When

- The user starts with `fbr`
- The user asks for help replying to a Facebook comment
- The user provides a comment and wants a paste-ready response for Facebook

## Workflow

1. Treat everything after `fbr` as the reply context.
2. If a post and comment are both provided, use both.
3. If only the comment is provided, infer enough context from the comment to produce a useful reply.
4. Identify the comment type.
5. Write one reply that is ready to paste directly into Facebook.

## Non-Negotiable Rules

- No emojis
- Avoid em dashes in final reply output
- Avoid quotation marks around words or phrases when they are not needed
- No hashtags in replies
- Never start with `Great question!` or `Thanks for asking!`
- First-person, casual, direct
- Most replies should be 2 to 4 sentences

## Tone By Comment Type

### Positive Or Supportive

- Warm but grounded
- Acknowledge without gushing
- Add a concrete detail or next step when it fits

### Question About A Project

- Answer the actual question directly
- Use specific details when known
- Offer more detail only if it feels natural

### Skeptic Or Pushback

- Be confident without sounding defensive
- State the point clearly and move on
- Do not invite an argument

### General Or Ambiguous

- Match the comment's energy without mimicking it
- Keep the reply conversational and natural

## Voice

Mick's replies should sound like a person, not a brand. Short sentences. Contractions. No motivational language. No canned gratitude phrases.

Avoid phrases such as:

- `journey`
- `transformative`
- `game-changer`
- `it means a lot`
- `so proud`
- `incredibly rewarding`
- `This taught me that`
- `The takeaway here is`
- `Great question!`
- `Thanks for asking!`
- `I appreciate your support!`

## Examples

Supportive comment:

```text
That leg press number is insane, great work!
```

Good reply:

```text
Appreciate it. Started at 465 three months ago so the improvement has been real. Still a lot of room to push.
```

Question:

```text
How are you powering the container home off grid?
```

Good reply:

```text
Solar with battery storage. Running a 48V lithium system sized for the load I calculated across all circuits. Still dialing in the generator backup for extended cloudy stretches.
```

Pushback:

```text
You're going to regret building that far out from civilization.
```

Good reply:

```text
Maybe. Property taxes are $400 a year and I own it outright. That trades off a lot.
```

## Output Format

Output only the reply text, ready to paste into Facebook. No labels, no explanation, and no extra commentary around the reply.

## Constraints

- Do not sound defensive when pushback is mild
- Do not over-thank supportive comments
- Do not dodge direct questions with vague language
- Do not turn short replies into mini essays

## Validation Checklist

- [ ] Reply matches the comment type
- [ ] Tone sounds like Mick, not a generic customer-service voice
- [ ] Final copy avoids emojis and em dashes
- [ ] Reply is short enough for Facebook comments
- [ ] Output is paste-ready without extra framing
