# Name

`alpaca-trading`

## Intent

Support safe, practical work in the `Trading` repository for Alpaca-connected scripts, backtesting, journaling, scheduling, and reusable PowerShell modules. The skill should help with implementation, debugging, reviews, and documentation while preserving the repo's current mixed Python and PowerShell structure.

## Use When

- The user is working in the `Trading` repo.
- The request mentions Alpaca scripts, paper trading, backtesting, journaling, scheduling, or related modules.
- The task involves repo docs, tests, or workflow changes around existing trading capabilities.

## Do Not Use When

- The user wants general investing or financial advice.
- The request is for autonomous live trading with no human confirmation or code-level safeguards.
- The task belongs to a different repo or a different broker/integration entirely.

## Inputs

- The relevant repo path or file path
- The user goal or requested behavior change
- Nearby README, script, module, or test context
- Whether the request is paper-trading-only or touches live-trading risk

## Outputs

- Repo-aligned code, docs, review feedback, or troubleshooting guidance
- Safe recommendations that default to paper trading
- Clear notes when live-trading safeguards are required

## Workflow

1. Identify the affected area of the `Trading` repo and inspect the existing implementation.
2. Preserve the established mixed Python and PowerShell layout instead of inventing a new one.
3. Reuse current repo patterns for logging, config, tests, and docs.
4. For non-trivial work, follow the repo workflow of requirements, spec, plan, tasks, implementation, audit, and regression test.
5. Prefer paper-trading-safe examples and require explicit opt-in for live-trading paths.
6. Keep AI analysis advisory and separate from final execution logic.
7. Update tests and docs when behavior changes.

## Constraints

- Preserve existing business logic unless the user asks for a larger rewrite.
- Do not hardcode secrets.
- Do not describe the repo with outdated folder names or obsolete architecture.
- Do not let AI output directly place orders without deterministic checks and explicit safeguards.
- Do not give financial advice.

## Platform Notes

### Claude

Claude packaging may require front matter metadata and a packaged `.skill` export, but the behavior should stay aligned with this portable source.

### ChatGPT

A ChatGPT wrapper may use system-prompt or instruction packaging, but it should keep the same repo shape, safety rules, and workflow.

### GitHub Copilot

A Copilot variant should align with the repo's existing `.github/copilot-instructions.md` and prompt workflow rather than redefining the repository structure.

## Examples

### Example 1

Input:

```text
Add a safer paper-trading helper to the Alpaca folder and keep it aligned with the existing repo.
```

Expected behavior:

- Reads current `Alpaca/` scripts before changing anything
- Keeps paper trading as the default path
- Updates nearby docs or tests if the helper changes repo behavior

### Example 2

Input:

```text
Review this Trading repo change and tell me if it breaks the journal or live-trading safeguards.
```

Expected behavior:

- Reviews the affected repo area against current journal and safety patterns
- Flags risky live-trading changes or stale architectural assumptions

## Test Cases

- The skill correctly describes the current `Trading` repo structure.
- The skill defaults examples and guidance to paper trading.
- The skill calls for explicit confirmation guards when live trading is requested.

## Maintenance Notes

- Owner: Mick
- Review trigger: repo structure, workflow, or live-trading safety changes in `Trading`
- Related docs: `Trading/README.md`, `Trading/specs/001-core-trading-foundation/`, `Trading/.github/copilot-instructions.md`
