PLATFORM_PATHS = {p: f'openai/{p}' if p in ('chatgpt', 'codex') else p
                  for p in ('claude', 'chatgpt', 'codex', 'copilot', 'cursor', 'gemini', 'perplexity')}
