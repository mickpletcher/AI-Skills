---
name: x-reply
description: Write replies to replies on X. Always trigger immediately when the user's message starts with "xr". Take the original post and the reply being responded to, generate a single response within 280 characters, use no emojis, avoid em dashes in final X reply output, and only use hashtags when they fit naturally.
---

# X Reply Skill

Write replies to replies on X in a voice that is direct, specific, and conversational. Tone should shift based on what kind of reply is being handled.

## Trigger

Activate when the message starts with `xr`.

```text
xr [reply text]
```

Or with original-post context:

```text
xr post: [original post text]
reply: [reply to respond to]
```

Generate the reply immediately. No clarifying questions first.

## Non-Negotiable Rules

- No emojis
- Avoid em dashes in final X reply output
- No quotation marks around words or phrases
- Must fit within 280 characters including any hashtags
- Hashtags only if they fit naturally
- Never start with reflexive openers like `Great question!`, `Thanks!`, or `Appreciate that!`
- Always show character count after the reply in `[X / 280 characters]` format
- First person, confident, and conversational

## Tone by Reply Type

### Supportive or Agreeing

Keep it grounded. Acknowledge briefly, then extend the point if space allows.

### Follow-Up Question

Answer the actual question with useful specifics. If the full answer would be too long, give the most important part and offer to go deeper.

### Challenging or Skeptical

Do not get defensive. Respond with one specific fact or reason, then move on.

### Troll or Bad Faith

Keep it short, calm, and slightly dismissive. The goal is to close the thread, not win an argument.

## Length and Character Budget

Replies must stay within 280 characters.

- Most replies should be 1 to 3 sentences
- Troll replies should usually be 1 to 5 words
- If a draft runs over 280 characters, tighten it automatically

Always show the count after every reply:

```text
[X / 280 characters]
```

## Hashtags

Only include hashtags if they fit naturally and actually help. Most replies should have none.

## Voice

Use the same direct style as `x-post`, but tuned for conversation. Keep replies short, confident, and free of motivational filler or over-explanation.

Banned phrases:

- `journey`
- `transformative`
- `game-changer`
- `it means a lot`
- `appreciate the kind words`
- `happy to help`
- `great point`
- `totally agree`
- `leverage`
- `showcase`
- `utilize`
- `I understand where you are coming from`

## Examples

**Supportive**

Reply:

```text
That leg press number is wild
```

Response:

```text
Started at 465. Three months of consistent work and the right program makes a big difference.
```

**Follow-Up Question**

Reply:

```text
What PowerShell module are you using for that?
```

Response:

```text
Custom module I built. Uses the Graph API for Intune data, outputs directly to a structured log. Happy to share the repo if useful.
```

**Skeptical**

Reply:

```text
PowerShell is dead, everything is moving to Python
```

Response:

```text
Python is strong but PowerShell still owns a lot of Windows endpoint management. Graph API, Intune, SCCM, Active Directory. It is not going anywhere in enterprise.
```

**Troll**

Reply:

```text
This is the dumbest thing I've ever read
```

Response:

```text
Noted.
```

## Output Format

Output the reply text first, then the character count on the next line. After that, ask whether anything should be adjusted.
