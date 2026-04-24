---
name: linkedin-post
description: Write LinkedIn posts for Mick Pletcher's professional audience. Always trigger immediately when Mick says "linkedin post", "lnp", or asks to write something for LinkedIn. LinkedIn audience is professional IT, AI, and automation peers. Tone is more polished than Facebook but still first-person and direct. No emojis. Avoid em dashes in final LinkedIn post output. 2 to 3 hashtags max. Focus on home AI infrastructure, algorithmic trading, enterprise automation, career insights, and tech commentary.
---

# LinkedIn Post Skill

Write LinkedIn posts for Mick Pletcher's professional audience in a voice that is direct, technical, and first-person.

## Trigger

- `lnp` for immediate triggering
- `linkedin post about...`
- `write something for LinkedIn`

## Audience and Tone

**Audience:** IT professionals, automation engineers, AI enthusiasts, enterprise tech practitioners, hiring managers, and peers in the Nashville and CBIZ space.

**Tone compared to other platforms:**

- More professional than Facebook, less casual than X
- Still first-person and direct, not corporate
- Shares real work, real results, and real opinions
- No humble-bragging
- Slightly longer than X and shorter than a blog post
- 150 to 400 words is the sweet spot

## Content Pillars

1. **Home AI infrastructure**: Proxmox, n8n, local LLMs, MCP servers, Claude integrations
2. **Enterprise automation**: PowerShell, SCCM, Intune, Microsoft Graph, CBIZ projects
3. **Algorithmic trading**: Alpaca, Python and PowerShell trading stack, paper versus live workflows
4. **Career and community**: Nashville PowerShell User Group, personal milestones, early retirement path
5. **Tech commentary**: GTC keynotes, new model releases, tooling observations

## Post Structure

**Hook line**

The first 1 to 2 sentences should earn the click in the feed preview. State what was built, solved, or learned. Skip the preamble.

**Body**

Use 2 to 4 short paragraphs. Explain what it is, why it matters, and how it works at a high level. Include specific tools, numbers, or outcomes where possible. One concrete detail is better than three vague claims.

**Closing line**

Optional. Use it for what comes next or a short observation. Do not end with a call to action such as asking for comments.

**Hashtags**

Use 2 to 3 hashtags on their own line at the end.

## Format Rules

- No emojis
- Avoid em dashes in final LinkedIn post output
- No bullet points unless genuinely listing 3 or more discrete items
- Keep paragraphs short, usually 2 to 3 sentences
- Leave line breaks between paragraphs
- Put hashtags at the bottom, not in the middle of the post
- Do not wrap the post in quotes

## Example Post Pattern

```text
Built an automated morning briefing pipeline in n8n this week.

It pulls crypto prices from CoinGecko, top stories from RSS feeds, and market commentary from Reddit, then sends everything through the Claude API for summarization before delivering a consolidated brief each morning.

The whole thing runs on my Proxmox homelab, exposed via Cloudflare Tunnel. Zero manual steps from wake-up to briefing.

Next phase is integrating live Alpaca portfolio data so the brief includes overnight position changes alongside the news.

#automation #homelab #n8n
```

## Quality Checklist

- Hook line earns attention in the first 1 to 2 sentences
- Specific tools or outcomes are mentioned
- No emojis and no em dashes in final output
- 2 to 3 hashtags at the bottom only
- Reads as professional but not corporate
- No filler phrases or AI-sounding language
- Written in first person as Mick
