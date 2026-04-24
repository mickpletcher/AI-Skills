---
name: x-post
description: Write posts for X on tech, PowerShell, IT automation, and fitness topics. Always trigger immediately when the user's message starts with "xp". Produce a single post within 280 characters, no emojis, avoid em dashes in final X post output, and use 2 to 3 hashtags maximum.
---

# X Post Skill

Write posts for X on tech, PowerShell, IT automation, and fitness. The voice should stay direct, specific, and compressed. Every post must fit within a single 280-character post including hashtags.

## Trigger

Activate when the message starts with `xp`. Everything after it is the draft or topic. Rewrite it immediately. No clarifying questions first.

```text
xp just automated Intune compliance reporting, cut a 2 hour manual process down to 3 minutes
xp hit 790 on leg press today, started at 465 three months ago
```

## Non-Negotiable Rules

- No emojis
- Avoid em dashes in final X post output
- No quotation marks around words or phrases
- Single post only
- Must fit within 280 characters including hashtags
- Use 2 to 3 hashtags maximum, placed at the end
- First person, confident, and conversational
- Always show the character count after the post

## Character Budget

280 characters total. Hashtags count toward that total.

- Two hashtags usually consume about 20 to 30 characters
- Leave enough space for the body before adding hashtags
- If the draft is too long, cut adjectives first, then restructure instead of truncating mid-thought

Always show the count in this format:

```text
[X / 280 characters]
```

If the post is over 280 characters, flag it and provide a tighter version automatically.

## Voice and Tone

X rewards punchy, opinionated, specific posts. Use the same direct voice as the Facebook writing skills, but more compressed. Lead with the most interesting detail first.

Banned phrases:

- `journey`
- `transformative`
- `game-changer`
- `next level`
- `cutting-edge`
- `excited to share`
- `proud to announce`
- `diving deep`
- `leverage`
- `showcase`
- `utilize`
- `The takeaway here is...`

### What works on X

- Specific numbers over vague claims
- Plainly stated opinions
- Process details that show expertise
- Before and after contrast

### What does not work on X

- Anything that sounds like a LinkedIn post
- Motivational sign-offs
- Vague humble-brags without specifics
- Asking people to like or repost

## Hashtag Strategy

Always use 2 to 3 hashtags and place them at the end.

**Tech / PowerShell / IT**

`#PowerShell #ITAutomation #Intune #Azure #SCCM #EndpointManagement #Microsoft #SysAdmin`

**Fitness**

`#StrengthTraining #MuscleBuilding #FitnessProgress #Lifting #NaturalStrength`

For topics not listed, choose 2 to 3 specific hashtags that fit real X communities.

## Post Structure

```text
[Hook with the most specific or interesting detail first]
[Optional supporting sentence if budget allows]
#Hashtag1 #Hashtag2
```

## Examples

**Tech**

Draft:

```text
just automated Intune compliance reporting, cut a 2 hour manual process down to 3 minutes
```

Post:

```text
Automated Intune compliance reporting across 4,000 endpoints. What took 2 hours manually now runs as a scheduled job in 3 minutes. #PowerShell #ITAutomation
```

**Fitness**

Draft:

```text
hit 790 on leg press today, started at 465 three months ago
```

Post:

```text
790 lbs on leg press today. Started at 465 three months ago. 75% improvement and still climbing. #StrengthTraining #MuscleBuilding
```

**Bad**

```text
So excited to share that I've been absolutely crushing my fitness goals lately! This journey has been so rewarding! #FitnessJourney #Blessed
```

## Output Format

Output the post text first, then the character count on the next line. After that, ask whether anything should be adjusted.
