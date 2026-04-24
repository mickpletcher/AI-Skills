---
name: facebook-post
description: Write and polish Facebook posts on any topic. Trigger on requests to draft, rewrite, polish, or improve a Facebook post, especially when the user starts with `fbp`.
version: 1.0.0
---

# Facebook Post

Write and polish Facebook posts for Mick in a direct, casual, first-person voice.

## Trigger When

- The user starts with `fbp`
- The user asks to write, draft, create, rewrite, or polish a Facebook post
- The user wants social copy that is clearly intended for Facebook

## Workflow

1. Treat everything after `fbp` as the draft.
2. Extract the specific facts, numbers, and claims from the draft.
3. Preserve those details while rewriting into cleaner post language.
4. Flag anything that seems off or unverifiable with a short note after the post.
5. Add relevant hashtags when they genuinely fit.
6. Optionally add a natural engagement question if the post would benefit from one.

## Non-Negotiable Rules

- No emojis
- Avoid em dashes in final post output
- Avoid quotation marks around words or phrases when they are not needed
- No bullet points or lists in the post body
- First-person, confident, conversational tone
- Use up to 6 hashtags when they are directly relevant

## Hashtag Strategy

Choose relevant hashtags rather than broad spammy ones. Prefer one or two broader tags plus the rest from the real niche community around the post topic.

Suggested pools:

- Tech / PowerShell / IT: `#PowerShell` `#Intune` `#SCCM` `#Azure` `#AzureAD` `#ITAutomation` `#EndpointManagement` `#Microsoft`
- Fitness: `#FitnessJourney` `#StrengthTraining` `#MuscleBuilding` `#Triathlon` `#Cycling` `#ActiveLifestyle`
- Container Home / Off-Grid / Retirement: `#ContainerHome` `#OffGrid` `#EarlyRetirement` `#SolarPower` `#GeographicArbitrage` `#FinancialFreedom` `#StewartCountyTN`
- DIY / Welding / Fabrication: `#DIY` `#Welding` `#MetalFabrication` `#MadeNotBought` `#DIYLife`
- Travel / Adventure: `#WorldTravel` `#Adventure` `#BucketList` `#Kilimanjaro`

## Voice And Tone

Mick's voice is casual, direct, and specific. Lead with the actual point instead of a warm-up. Keep the writing practical rather than polished for marketing.

Avoid phrases such as:

- `journey`
- `transformative`
- `game-changer`
- `next level`
- `cutting-edge`
- `I'm excited to share`
- `diving deep`
- `delve into`
- `leverage`
- `showcase`
- `utilize`

## Post Structure

Use this structure unless the draft clearly calls for a small variation:

```text
[Lead with the actual point]

[1 to 2 short paragraphs with specific details]

[Optional natural question]

#Hashtag1 #Hashtag2 #Hashtag3
```

## Topic Guidance

- Tech / IT: explain the problem, the approach, and the impact
- Fitness: lead with the number or milestone and the starting point
- Container home / off-grid: explain what was built or solved and how it fits the broader plan
- DIY / fabrication: focus on what was made, which tools mattered, and what was done solo
- Travel: keep it specific and vivid

## Constraints

- Do not water down specific facts into generic motivational copy
- Do not sound like a marketer or content team
- Do not add hype where the draft is simple and factual
- Do not force a question or hashtags if they clearly hurt the post

## Validation Checklist

- [ ] Keeps the original specific facts and numbers
- [ ] Sounds like Mick, not a content marketer
- [ ] Uses a direct first-person tone
- [ ] Avoids emojis and em dashes in final output
- [ ] Uses only relevant hashtags
