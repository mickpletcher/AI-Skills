---
name: crypto-listings
description: Retrieve new cryptocurrency listings from the past 7 days and upcoming listings in the next 7 days across major exchanges. Trigger on requests about recently listed or soon-to-be-listed cryptocurrencies and verify current listings data before responding.
version: 1.0.0
---

# Crypto Listings

Retrieve and format new and upcoming cryptocurrency listings across major exchanges. This skill covers coins listed in the last 7 days and coins officially scheduled to list in the next 7 days.

## Trigger When

- The user starts with `cl`
- The user asks for crypto listings, new coins, or upcoming listings
- The user asks what cryptos just launched or what coins are coming soon

## Workflow

1. Verify current listings data before writing anything.
2. Use exact UTC windows for the last 7 days and next 7 days.
3. Separate recently listed items from upcoming officially confirmed listings.
4. Mark gaps honestly instead of filling them with rumor.
5. Output the brief in the required markdown format with sources for every row.

## Data To Collect

Always gather:

- recent listings across major exchanges
- upcoming listings with at least one official exchange announcement URL
- launch price when available
- current USD price when available
- timestamped price snapshot
- exchange-level activity summary
- notes for data gaps, notable listings, and rumored items

## Source Guidance

Prefer current information from:

- official exchange announcement pages
- CoinGecko new listings and market pages
- CoinMarketCap listing pages when needed
- other reputable aggregators only when official sources are incomplete

For upcoming listings, at least one official exchange announcement URL is required.

## Report Format

Use this structure:

```markdown
# Crypto Listings Brief [Month DD, YYYY]
*Past 7 days and next 7 days | Sources: [list sources used]*

## Recently Listed Last 7 Days

| Coin | Ticker | Listed Date | Exchange(s) | Category | Launch Price (USD) | Current Price (USD) | Price Timestamp (UTC) | Source(s) |

## Upcoming Listings Next 7 Days

| Coin | Ticker | Expected Date | Exchange(s) | Category | Notes | Source(s) |

## Exchange Activity Summary

| Exchange | Recent Listings (7d) | Upcoming (7d) |

## Notes
```

End with a short reminder to verify on the exchange before trading.

## Rules

- Verify current listings data before writing
- Use exact UTC windows
- Do not fabricate missing dates, prices, or sources
- Show all exchanges when a coin is multi-listed
- Do not provide price predictions or buy and sell commentary
- Flag Binance listings clearly when present
- Only include an item in Upcoming Listings when official confirmation exists
- Put unconfirmed items in Notes as `Rumored`
- Include source URLs for every row

## Category Labels

Use the most specific applicable category:

- Layer 1
- Layer 2
- DeFi
- DEX
- Lending
- Stablecoin
- Meme
- AI
- RWA
- Gaming or GameFi
- Infrastructure
- Privacy
- Oracle
- Bridge

## Extended Mode

If the request includes `+detail`, add a detail section for each recent listing with:

1. Project purpose
2. Chain or ecosystem
3. Token utility
4. Notable backers, partnerships, or launch metrics

Keep detail mode factual and avoid hype language.

## Validation Checklist

- [ ] Recent listings use the correct 7-day window
- [ ] Upcoming listings have official confirmation
- [ ] Every row includes at least one source URL
- [ ] Missing data is marked honestly
- [ ] Binance listings are clearly flagged when present
- [ ] Output stays informational and avoids trading advice
