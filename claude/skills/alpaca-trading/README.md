# alpaca-trading

A Claude skill for working safely in the `Trading` repository and its Alpaca-related workflows.

## What It Does

Guides Claude to work within the current mixed Python and PowerShell `Trading` repo structure. It preserves existing repo patterns, defaults to paper-trading-safe guidance, keeps live-trading safeguards explicit, and treats AI analysis as advisory rather than as a direct execution trigger.

## Trigger Phrases

| Phrase | Action |
|--------|--------|
| `alpaca script for...` | Create or update a script in the existing Trading repo structure |
| `backtesting script` | Work in the `Backtesting/` area |
| `paper trading...` | Prefer the paper-trading-safe path |
| `live trading...` | Require explicit live-trading guardrails |
| `trade journal...` | Work in the `Journal/` area or its related logging flows |
| `alpaca module` | Use the reusable PowerShell modules under `src/` |

## Repo Structure: Trading

```text
Trading/
|-- Alpaca/
|-- Backtesting/
|-- Journal/
|-- Scheduler/
|-- src/
|-- Tests/
|-- rsi_macd_bot/
`-- btc-signal-executor/
```

## Safety Rules Always Enforced

- Paper trading is the default guidance unless the user explicitly requests live trading
- API keys come from environment variables or existing repo config flows, never hardcoded
- Live trading must remain opt-in and guarded by an explicit confirmation step
- AI output is advisory only and must not directly place orders
- Existing trading logic should be preserved unless the user explicitly asks for a larger rewrite

## Live Trading Guard

Every script touching real money should keep an explicit confirmation gate:

```powershell
if ($LiveTrading) {
    $Confirm = Read-Host "Type CONFIRM to proceed with live trading"
    if ($Confirm -ne "CONFIRM") { exit 0 }
}
```

## AI Coaching Pattern

Claude can provide analysis such as `BULLISH`, `BEARISH`, or `NEUTRAL`, but deterministic code must still apply risk checks and decide whether any order is placed.

## Script Conventions

Follow the existing repo conventions for PowerShell and Python rather than inventing a new architecture. Reuse nearby patterns for logging, config, tests, and docs.

## Files

```text
Alpaca Trading/
|-- README.md
|-- skill.md
`-- alpaca-trading.skill
```

## Installation

Run the repo packer against this folder to rebuild `alpaca-trading.skill`, then install it with your normal Claude skill workflow.
