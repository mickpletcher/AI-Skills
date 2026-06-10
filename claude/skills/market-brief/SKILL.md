---
name: market-brief
description: >
  Generate a current morning market brief for Mick's equity, macro, and crypto
  watchlist. Trigger immediately when the user starts with "mb" or asks for a
  market brief, morning brief, market update, pre-market summary, market open
  summary, or asks what the market is doing. Always verify live prices, market
  session context, and news before answering. Never use memory for prices,
  levels, market status, or headlines.
version: 1.0.0
---

# Market Brief

## Intent

Generate a fast, structured market brief for Mick before or during the trading day. The brief covers index direction, watchlist prices, crypto, macro instruments, market-moving headlines, and only the flags that matter.

This is a situational awareness tool. It is not financial advice, trade execution guidance, or a signal service.

## Do Not Use When

- Do not use for buy, sell, hold, price target, or guaranteed performance advice.
- Do not use for a deep single-stock or single-crypto research report when a research skill is a better match.
- Do not answer from memory when current prices, market session state, economic events, or headlines are requested.
- Do not invent prices, changes, 52-week ranges, market hours, headlines, or sources.

## Trigger When

Trigger immediately, search first, and do not ask clarifying questions when the user starts with:

```text
mb
```

Also trigger on:

- `market brief`
- `morning brief`
- `market update`
- `pre-market summary`
- `market open summary`
- `what is the market doing`

Ticker modifiers:

- `mb + PLTR SOFI` means append those tickers to the default watchlist for this brief only.
- `mb only: NVDA TSLA BTC` means use only those tickers for this brief.
- `mb +depth` means add the optional depth sections after Headlines.

## Workflow

1. Parse the request for `+` tickers, `only:` override tickers, and `+depth`.
2. Determine the current market session: pre-market, regular session, after-hours, closed, weekend, or holiday if available.
3. Verify current data before writing. Use reliable finance, exchange, brokerage, or market data pages where available.
4. Gather price, dollar change, percent change, and 52-week range where available for equities and ETFs.
5. Gather BTC/USD and ETH/USD current price and 24-hour change.
6. Gather 3 to 5 market-moving headlines from current sources.
7. Populate only confirmed values. Use `--` for unavailable values.
8. Build the brief in the required markdown format.
9. Add Flags only when something is actually notable.
10. End with the required one-line follow-up.

## Default Watchlist

Use these by default unless the user gives `only:`.

### Indices

- SPY
- QQQ
- IWM
- VIX

### Equities

- AAPL
- MSFT
- NVDA
- TSLA
- AMZN

### Crypto

- BTC/USD
- ETH/USD

### Macro

- TLT
- DXY

## Source Priority

Prefer sources in this order:

1. Built-in finance or market data tools if available.
2. Exchange, ETF sponsor, brokerage, or official market data pages.
3. Major financial data sites such as Yahoo Finance, Nasdaq, MarketWatch, CNBC, Investing.com, TradingView, CoinMarketCap, or CoinGecko.
4. Major business news sources for headlines.

Use multiple sources when a value looks stale, contradictory, delayed, or out of session.

For economic calendar items, verify against a current economic calendar or official release source where possible.

## Data Requirements

For each index, equity, ETF, and macro instrument, try to capture:

- current or most recent price
- dollar change
- percent change
- session label if relevant
- 52-week high and low for watchlist equities if easily available

For crypto, capture:

- current price
- dollar change
- percent change
- 24-hour basis where available

For headlines, capture:

- source
- headline
- one plain-English sentence explaining why it matters

## Report Format

Use this exact structure. Keep tables compact. Do not add commentary outside these sections except the final follow-up line.

```markdown
# Market Brief - [Day, Month DD YYYY] [Time and timezone]

## Indices

| Ticker | Price | Change | % Change | Note |
| --- | ---: | ---: | ---: | --- |
| SPY | $XXX.XX | +$X.XX | +X.XX% | [Pre-market / Open / After-hours / Closed] |
| QQQ | $XXX.XX | +$X.XX | +X.XX% | |
| IWM | $XXX.XX | +$X.XX | +X.XX% | |
| VIX | XX.XX | +X.XX | +X.XX% | [Low <15 / Elevated 20-30 / High >30] |

## Watchlist

| Ticker | Price | Change | % Change | 52W High | 52W Low |
| --- | ---: | ---: | ---: | ---: | ---: |
| AAPL | $XXX.XX | +$X.XX | +X.XX% | $XXX.XX | $XXX.XX |
| MSFT | -- | -- | -- | -- | -- |

## Crypto

| Pair | Price | Change | % Change |
| --- | ---: | ---: | ---: |
| BTC/USD | $XX,XXX | +$XXX | +X.XX% |
| ETH/USD | $X,XXX | +$XX | +X.XX% |

## Macro

| Instrument | Price | Change | % Change |
| --- | ---: | ---: | ---: |
| TLT | $XXX.XX | +$X.XX | +X.XX% |
| DXY | XXX.XX | +X.XX | +X.XX% |

## Headlines

1. **[Source]** - [Headline]. [One sentence plain-English summary.]
2. **[Source]** - [Headline]. [One sentence plain-English summary.]
3. **[Source]** - [Headline]. [One sentence plain-English summary.]

## Flags

- [Only include this section when something is notable.]

## Sources

- [Source name] - [What it supplied]

*Data pulled [HH:MM timezone]. Verify before trading.*

Add tickers or pull a specific chart level?
```

## Optional Depth Sections

If the user includes `+depth`, add these sections after Headlines and before Flags.

### Sector Performance

Use a compact table for the 11 S&P 500 sector ETFs:

- XLK
- XLV
- XLE
- XLF
- XLI
- XLC
- XLRE
- XLU
- XLB
- XLP
- XLY

Columns: Sector ETF, Price, % Change, Note.

### Earnings This Week

Show notable earnings that could move the broader market or the watchlist.

Columns: Company, Ticker, Report Date, Estimate if available.

### Economic Calendar

Show Fed events, CPI, PPI, jobs data, PMI, Treasury auctions, or other major macro events due today or this week.

Columns: Date, Event, Prior, Estimate.

## Constraints

- Always verify current data before answering.
- Use `--` for any value that cannot be confirmed.
- State the session context clearly when markets are not in regular trading.
- Keep the brief factual and compact.
- Do not use green or red formatting.
- Do not include placeholder text in Flags.
- Do not output a buy, sell, hold, entry, stop, target, or position sizing recommendation.
- Do not describe a headline as market-moving unless it plausibly affects indices, rates, mega-cap tech, energy, crypto, the Fed, inflation, jobs, or broad risk appetite.
- Keep headlines to 3 to 5 items.
- Include a Sources section with the data source names or links used.
- End with exactly: `Add tickers or pull a specific chart level?`

## Flag Rules

Include Flags only for meaningful conditions such as:

- VIX above 25.
- SPY, QQQ, IWM, TLT, or DXY move above roughly 1% intraday.
- BTC moves more than 3% in 24 hours.
- Any watchlist ticker is near or at a 52-week high or low.
- A major Fed, CPI, PPI, jobs, or earnings event is due today or this week.
- Data conflict or stale quote risk could materially affect the brief.

## Validation Checklist

- [ ] Current prices were verified during this run.
- [ ] Market session context is labeled.
- [ ] Default, appended, or override tickers were parsed correctly.
- [ ] Missing values are marked `--` instead of guessed.
- [ ] Headlines are current and limited to 3 to 5.
- [ ] Flags are omitted when nothing notable is found.
- [ ] Sources are listed.
- [ ] Output avoids financial advice and trade instructions.

## Help And Examples

If the user asks how to use the skill, give short examples and ask for the fastest next prompt.

Minimum useful input:

- `mb`

Example prompts:

- `mb`
- `mb + PLTR SOFI`
- `mb only: NVDA TSLA BTC`
- `mb +depth`
- `market brief before open`
