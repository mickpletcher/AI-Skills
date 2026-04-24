---
name: crypto-research
description: Deep-dive research report on a specific cryptocurrency before trading or investing. Trigger on requests for a structured breakdown of a specific coin or token and verify current market, team, tokenomics, and project facts before responding.
version: 1.0.0
---

# Crypto Research

Generate a structured due diligence report on a specific cryptocurrency. This is a research tool for project quality and risk review, not a buy or sell recommendation engine.

## Trigger When

- The user starts with `cr` followed by a coin name or ticker
- The user asks for research, due diligence, or a full breakdown of a specific crypto asset
- The user asks whether a coin looks credible, risky, overvalued, or worth further review

Examples:

```text
cr ONDO
cr Solana
cr Sui
cr ai16z
```

## Workflow

1. Verify current facts before writing, especially price, supply, listings, team status, and recent news.
2. Gather enough source-backed information for each report section.
3. Mark unverifiable fields as `—` or `Not found` instead of guessing.
4. Write the report in the required format with a mandatory `Red Flags` section.
5. End with a research-only disclaimer and source list.

## Research Areas

Always cover:

1. Project overview and differentiators
2. Tokenomics and unlock risk
3. Team and backer credibility
4. Exchange listings and liquidity context
5. Price action and market context
6. Roadmap and development activity
7. Adoption signals and traction metrics
8. Red flags and green flags
9. Summary scorecard

## Search Guidance

Verify current information for:

- project overview and use case
- tokenomics, supply, and vesting schedule
- team and founder background
- roadmap and milestones
- current price and chart context
- exchange listings
- recent news
- risks, criticism, and controversies
- audit and security status
- market data from sources such as CoinGecko or CoinMarketCap

If search snippets are insufficient, open direct source pages for cleaner data.

## Report Format

Use this structure:

```markdown
# [Coin Name] ($TICKER) Research Report
*Generated [Month DD, YYYY] | Data as of [YYYY-MM-DD HH:MM UTC]*

## TL;DR

## Project Overview

## Tokenomics

## Team & Backers

## Exchange Listings

## Recent Price Action

## Roadmap & Development

## Use Case & Adoption

## Red Flags

## Green Flags

## Summary Scorecard

## Sources
```

## Rules

- Verify current facts before writing
- Use reliable and current sources
- Never fabricate missing data
- Keep language direct and factual
- Include a `Red Flags` section every time
- Do not provide financial advice
- Remove or mark any claim that cannot be sourced
- Avoid crypto hype language and marketing copy

## Scoring Guidance

Score these areas qualitatively:

- project fundamentals
- tokenomics
- team credibility
- exchange liquidity
- development activity
- overall risk level

Use the scorecard to summarize quality and risk, not to imply a trading signal.

## Validation Checklist

- [ ] Current price and market data are source-backed
- [ ] Tokenomics and unlock risk are addressed
- [ ] Team and backers are verified or marked unknown
- [ ] Red flags are explicit and not omitted
- [ ] Sources are included for all major populated sections
- [ ] Output stays research-only and avoids financial advice
