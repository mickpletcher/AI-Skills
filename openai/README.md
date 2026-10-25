# OpenAI

OpenAI skills are organized by target:

| Target | Repository directory | Entry point | Status |
| --- | --- | --- | --- |
| ChatGPT | `openai/chatgpt/skills/` | `instructions.md` | Existing shipped source; see the [Food Analyzer README](chatgpt/skills/food-analyzer/README.md). |
| Codex | `openai/codex/skills/` | `SKILL.md` | Existing example scaffold only; excluded from shipped catalog and release bundles. |

The target IDs remain `chatgpt` and `codex`. Each keeps its own capability requirements, instruction format and suitability rules.

Review candidates live under `generated/openai/chatgpt/skills/` and `generated/openai/codex/skills/`. Named model builds use the same grouping below their profile directory. These generated bundles are not installed or promoted. See the [canonical migration guide](https://github.com/mickpletcher/AI-Skills/blob/main/master-skills/README.md) and [platform installation guidance](../docs/installation.md#chatgpt).
