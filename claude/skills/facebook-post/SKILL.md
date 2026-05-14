---
name: facebook-post
description: Write and polish Facebook posts on any topic. Trigger on requests to draft, rewrite, polish, or improve a Facebook post, especially when the user starts with `fbp`.
version: 1.2.0
---

# Facebook Post

Write and polish Facebook posts for Mick in a direct, casual, first-person voice.

## Trigger When

- The user starts with `fbp`
- The user asks to write, draft, create, rewrite, or polish a Facebook post
- The user wants social copy that is clearly intended for Facebook

Treat `fbp` as an immediate trigger. Do not ask clarifying questions first unless the draft is missing a critical fact that would change the post.

## Workflow

1. Treat everything after `fbp` as the draft.
2. Extract the specific facts, numbers, and claims from the draft.
3. Infer the best post mode and length preset from the draft unless the user already specified them.
4. Generate 2 to 3 possible hook approaches internally, then choose the strongest one that sounds natural.
5. Infer the right audience mode and media context from the draft unless the user specifies them.
6. Preserve the original details while rewriting into cleaner post language.
7. If the post includes a question or engagement prompt, make sure it sounds natural and not needy.
8. Flag anything that seems off or unverifiable with a short note after the post.
9. Add relevant hashtags when they genuinely fit.
10. Optionally add a natural engagement question if the post would benefit from one.

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

## Post Modes

Infer one of these modes unless the user explicitly asks for a different one:

- `personal update`: life event, milestone, trip, family, or broad personal update
- `technical lesson`: something built, learned, fixed, or automated with a practical takeaway
- `project progress`: container home, build work, DIY, or ongoing long term effort
- `opinion`: clear point of view, reaction, or lesson learned

### Mode Guidance

- `personal update`: sound relaxed and human. Keep it simple and specific.
- `technical lesson`: lead with the result or problem solved, then explain what mattered.
- `project progress`: make clear what changed today and how it fits the larger build or plan.
- `opinion`: state the point plainly. Back it with one or two concrete reasons.

## Length Presets

Infer one of these presets unless the user requests a specific length:

- `short update`: 2 to 4 sentences plus hashtags
- `standard`: 1 to 2 short paragraphs plus hashtags
- `story`: 3 to 5 short paragraphs when context or progression matters

Default to `standard`. Use `short update` when the draft is a quick result or milestone. Use `story` when the draft includes a sequence, contrast, or lesson that benefits from a little narrative room.

## Hook Strategy

The first sentence should earn attention without sounding promotional.

Build hook candidates around one of these angles:

- the clearest result
- the most specific number
- the problem that got solved
- the strongest opinion in the draft

Pick the best one and use it in the final post. Only show alternate hook options when the user asks for options.

## Audience Modes

Infer one of these modes unless the user explicitly asks for a different audience:

- `friends and family`: more personal, lighter context, less jargon
- `technical peers`: more specific, more direct, more comfortable with tool names and implementation detail
- `mixed audience`: plain enough for general readers while keeping the strongest useful specifics

### Audience Guidance

- `friends and family`: explain just enough context so the point lands without assuming deep technical background
- `technical peers`: keep the strongest implementation detail, results, and tool names instead of translating everything into general language
- `mixed audience`: use plain phrasing first, then one or two concrete specifics so both groups can follow it

## Photo Pairing Guidance

If the draft clearly relates to a photo, screenshot, or progress image, make the text match what the image is likely showing.

- build photos: mention what changed, what part of the build is visible, and why it mattered that day
- screenshots: reference the result, report, script, dashboard, or tool shown without overexplaining the obvious
- workout images: anchor the caption to the lift, session, pace, distance, or milestone the image supports

Do not describe visual details that were never stated or strongly implied. Use the image context to sharpen the caption, not to invent facts.

## Engagement Prompt Rules

Use engagement prompts sparingly.

- only add a question when the post naturally invites one
- prefer real prompts such as asking about similar experience, lessons learned, or a practical choice
- avoid generic bait such as `Anyone else?`, `Thoughts?`, or `Agree or disagree?` when they add no value
- skip the question entirely when the post lands better as a plain statement or update

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

[Body shaped by the inferred mode and length preset]

[Optional natural question]

#Hashtag1 #Hashtag2 #Hashtag3
```

## Topic Guidance

- Tech / IT: explain the problem, the approach, and the impact
- Fitness: lead with the number or milestone and the starting point
- Container home / off-grid: explain what was built or solved and how it fits the broader plan
- DIY / fabrication: focus on what was made, which tools mattered, and what was done solo
- Travel: keep it specific and vivid

## Output Rules

- Return one finished Facebook post by default
- Do not expose the inferred mode, length preset, or discarded hook options unless the user asks
- Do not expose the inferred audience mode unless the user asks
- If the draft is thin, strengthen the wording but do not invent facts
- If the user asks for choices, provide up to 3 hook options before the final full post

## Constraints

- Do not water down specific facts into generic motivational copy
- Do not sound like a marketer or content team
- Do not add hype where the draft is simple and factual
- Do not force a question or hashtags if they clearly hurt the post
- Do not add empty engagement bait just to manufacture comments
- Do not write captions that clash with the attached or implied image context

## Validation Checklist

- [ ] Keeps the original specific facts and numbers
- [ ] Sounds like Mick, not a content marketer
- [ ] Uses a direct first-person tone
- [ ] Avoids emojis and em dashes in final output
- [ ] Uses the right mode for the kind of post
- [ ] Uses the right length for the amount of source material
- [ ] Opens with a natural hook instead of filler
- [ ] Matches the right audience without losing the point
- [ ] Fits the photo or screenshot context when one is implied
- [ ] Avoids forced engagement bait
- [ ] Uses only relevant hashtags
