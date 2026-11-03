# Requirements

1. Provide a separate read-only n8n security-review candidate alongside, without changing, the workflow builder.
2. Review exported workflow/config evidence for credentials, ingress, least privilege, data retention, untrusted inputs, unsafe code/HTTP and applicable AI tool boundaries. Cite evidence, preconditions and unknowns.
3. Never access a live n8n server, retrieve secrets, execute/import/publish workflows, probe exploits, install integrations, make paid API calls, merge or publish.
4. Verify official documentation and version/edition caveats; do not infer defaults or deployment state from exports.
5. Validate with synthetic positive/negative helper cases and an independent contextual review if available. Keep host/model acceptance separate.
