# IdeaForge Output Template

Standard output structure for Stage 5. Include all sections that have meaningful content. Omit sections that do not apply — do not generate placeholder filler.

For mode-specific output rules, see the Modes table in `SKILL.md`.

---

## Section Definitions

### 1. Idea Summary
One paragraph, plain language. No jargon. Should be understandable by someone with no technical background. Describes what the idea is, what problem it solves, and who it is for.

### 2. Core Problem
The specific pain point being solved. One to three sentences. Be concrete — name the friction, cost, risk, or gap. Avoid abstract statements like "improves efficiency".

### 3. Proposed Solution
What this idea does and how it does it at a high level. Include the core mechanism. Two to five sentences.

### 4. IdeaForge Score
The scoring table from Stage 4. Format:

```
| Metric                   | Score | Weight |
|--------------------------|-------|--------|
| Technical Feasibility    | X/10  | 20%    |
| Commercial Potential     | X/10  | 25%    |
| Automation Potential     | X/10  | 15%    |
| Implementation Simplicity| X/10  | 15%    |
| Market Openness          | X/10  | 10%    |
| Patent Potential         | X/10  | 10%    |
| Speed to MVP             | X/10  | 5%     |

IdeaForge Score: XX/100
Verdict: [band label]

Strongest signal: [metric name] — [one sentence why]
Weakest signal: [metric name] — [one sentence why]
Missing inputs: [list any signals that could not be scored accurately]
```

### 5. Technical Analysis
- Primary technology stack recommendation
- Key dependencies (APIs, libraries, models, hardware)
- Hardest technical problem to solve and the most likely approach
- What breaks first under load or scale

### 6. AI Opportunities
Specific, named AI integration points. Not "use AI to improve X." Name the model type, the task it performs, and where it sits in the system.

Examples of acceptable specificity:
- "Claude handles idea classification and expansion via a structured prompt with tool use"
- "Local embedding model (e.g. nomic-embed-text via Ollama) indexes all stored ideas for semantic similarity search"
- "GPT-4o Vision reads screenshot inputs when OCR extraction is needed"

### 7. Automation Opportunities
- What triggers the system (event, schedule, webhook, user action)
- What runs automatically after the trigger
- What requires human review or decision
- Suggested n8n workflow structure if applicable
- Suggested Home Assistant automation if applicable

### 8. Suggested Architecture
High-level component view. Use a table or annotated text layout — not a Mermaid diagram unless explicitly requested.

Example format:

```
Capture layer:   [input sources]
Processing:      [Claude skill / API / local model]
Storage:         [file system / SQLite / vector DB]
Interface:       [CLI / Claude chat / web UI / mobile]
Automation:      [n8n / scheduled task / webhook]
```

### 9. Potential APIs and Integrations
Name specific services, not generic categories. For each, state the integration angle.

Example format:

```
- GitHub API: auto-create repo and scaffold from the generated blueprint
- Alpaca Markets API: relevant if the idea involves trading or financial data
- Home Assistant REST API: trigger or respond to smart home events
- Obsidian local vault: write output to a dated note in the ideas folder
- n8n webhook: receive idea input from any capture source
```

### 10. Privacy and Security Concerns
Name specific risks. For each risk, note the mitigation.

If no meaningful risk exists, state that plainly: "No significant privacy or security surface identified."

Do not generate generic security advice that applies to all software.

### 11. Monetization Opportunities
Ordered from fastest path to revenue to most ambitious long-term play.

For each path, include:
- Model type (subscription, one-time, usage-based, etc.)
- Target buyer
- Rough price range or pricing unit
- Time to first revenue (realistic estimate)

### 12. Patent Potential
One of four verdicts followed by a brief explanation:

- **Strong patent potential**: [describe the specific novel claim]
- **Narrow patent potential**: [describe the angle and prior art concern]
- **No clear patent angle**: [why]
- **Defer to a patent attorney**: [what makes this worth a professional search]

### 13. MVP Roadmap
Phased build plan. Phase 1 must be completable by one person in under 30 days or it is not an MVP — break it down further.

Format:

```
Phase 1 — [Name] (target: [timeframe], solo completable)
- [Task 1]
- [Task 2]
- [Task 3]
Milestone: [what works at the end of Phase 1]

Phase 2 — [Name] (target: [timeframe])
- [Task 1]
- [Task 2]
Milestone: [what works at the end of Phase 2]

Phase 3 — [Name] (target: [timeframe])
...
```

### 14. GitHub Repository Suggestions
For each suggested repo:
- Repo name (kebab-case)
- One-line description
- Suggested top-level folder structure (annotated tree)
- Suggested initial labels or milestones if relevant

### 15. Similar Existing Products
Name specific products, projects, or companies — not categories. For each:
- Name and URL if known
- How it is similar
- Key differentiator for the proposed idea

If nothing directly comparable exists, say so. Do not invent competitors.

### 16. Future Expansion Ideas
Three to five directions the idea could grow if the MVP succeeds. Each in one to two sentences.

### 17. Risk Assessment
Top three risks. For each:
- Risk description
- Likelihood (low / medium / high)
- Mitigation approach

### 18. Long-Term Strategic Value
What this becomes if it works at scale. One paragraph. Be honest about ceiling — not everything becomes a platform. Some ideas are excellent utilities with a low ceiling, and that is fine.
