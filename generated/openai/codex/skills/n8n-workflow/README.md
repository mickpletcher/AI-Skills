# n8n-workflow: canonical candidate

Edit [SKILL.md](SKILL.md) and the linked modules here. Version 1.2.0 strengthens the core and adds AI workflow/testing guidance as references, not new standalone skills. This revision is unpromoted; older bounded acceptance does not establish behavior or runtime support for the expansion.

## Review and prerequisites

Start with the core, then load only the references relevant to the task. Try: “Design an RSS briefing with synthetic inputs, no live calls”; “Review this export against a status-only retry policy”; or “Plan two-user Q&A with source citations and approval before sends.” A version and sanitized export improve specificity but are not required for a conceptual plan.

No n8n server, model account, plugin or installation is required for reading the guidance. The optional [export inspector](scripts/inspect_export.py) requires Python 3.10+ standard library; its [usage and limits](references/testing-and-debugging.md#offline-export-inspector) explain that it cannot validate n8n compatibility or secret absence. Local repository checks use existing maintenance dependencies; the illustrative JavaScript test optionally uses Node.js and is not a Code-node runtime test. Do not install anything just to read or generate this candidate.

For later authorized host review, generate candidates with the repository tool and use the intended host's supported skill surface. Generation does not install, promote, publish or connect n8n. No target-host or actual n8n version is certified by these files.

## Provenance

The [original README](https://github.com/mickpletcher/AI-Skills/blob/1deaab97ec585b6451a7ed80bc2a4398a8428ecc/claude/skills/n8n-workflow/README.md) retains the shipped source installation instructions and author context. Shipped packages and history remain unchanged in the Claude tree. `migration.json` preserves source commit/hash/frontmatter, records the explicit entrypoint rewrite and hashes every new supporting resource.

The new material is original repository guidance with dated official documentation links, not copied upstream skill files. Optional official n8n skills are references only; see [reuse and feature gates](references/runtime-and-release.md). The repository MIT license applies where no separate notice says otherwise. Do not infer compatibility, current infrastructure facts or permission from historical context.
