"""Stable ecosystem IDs mapped to vendor-grouped repository paths."""
PLATFORM_PATHS = {p: f'openai/{p}' if p in ('chatgpt', 'codex')
                  else f'microsoft/{p}' if p == 'copilot' else p
                  for p in ('claude', 'chatgpt', 'codex', 'copilot', 'cursor', 'gemini', 'perplexity')}
