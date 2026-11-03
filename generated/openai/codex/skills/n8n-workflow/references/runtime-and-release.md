# Runtime inventory and release boundaries

Checked against official documentation on 2026-11-03. These are feature-specific documentation observations, not a supported-version matrix for an uninspected instance. Recheck the target's version and edition before using a feature; do not upgrade just to fit an example.

## Minimum evidence

Record only fields relevant to the task: instance version/hosting/plan, available node types and versions, timezone, execution mode/queue configuration, credential aliases and owners, workflow ID/revision/production state and destination allowlist. Operations work also needs installation method, database/storage locations, encryption-key backup method, service manager and rollback evidence. Historical CT 104/IP/SQLite/npm/systemd descriptions are unverified source history, not commands to run.

If evidence is unavailable, produce a blueprint with `target_version: unknown`, `import_test: not_run` and `runtime_test: not_run`. A skill or MCP plugin cannot supply a server, credentials or permissions.

## Consequential boundaries

| Stage | Check before proceeding |
| --- | --- |
| Design/review/local artifact | Requested scope, sanitized inputs, target assumptions; do not silently edit a reviewed export. |
| Import or instance edit | Authorized target/workflow, backup/export, node availability, credential placeholders and unchanged production state. Editing production settings can be consequential. |
| Manual/partial/test execution | Every reachable node/sub-workflow, data destinations, approved effects/costs, mock/sink substitutions and stop limits. Unpublished does not mean harmless. |
| Publish/activate/settings | Explicit production scope, trigger registration, recipient/service bindings, schedule/timezone, rollback and post-change verification. |
| Credentials/access/exposure/ops | Separate required approval for secrets, persistent access, tunnel/network changes, installation, restart, upgrade or restore. |

Reuse existing authorization when it covers the exact action and effects; don't require duplicate approval. A denied, cancelled or uncertain action is not a successful operation. Check uncertain outcomes before retrying.

## Export hygiene and handoff

An export should come from a known target or verified schema; record version and node `typeVersion` evidence. Retain user intent and unrelated settings. Scrub credential names/IDs when private, literal headers/tokens, webhook URLs, pinned data, personal examples and execution data. Do not export decrypted credentials. Credential references are not credential values, but may still disclose names. Inspect code and expression strings manually; a scanner cannot prove the absence of secrets. [Export/import](https://docs.n8n.io/build/manage-workflows/export-and-import.md)

Provide an inactive/unpublished candidate when supported, not an automatic production update. Verify actual imported state and credential mapping without execution. A boolean `active: false` in a file alone does not prove the destination workflow is inactive or unpublished. An authorized runtime test should use a separately identified isolated workflow/instance and sink destinations. Keep prior export/version and restoration steps; verify restore behavior in an authorized environment, not by assumption.

## Feature gates to verify

| Feature | Documented boundary and fallback |
| --- | --- |
| Save/publish/settings | Current docs separate draft and published versions; settings-only updates can republish automatically. Publishing can leave only some triggers running. Inspect target behavior and trigger state, not just a success click. [Save and publish](https://docs.n8n.io/build/understand-workflows/save-and-publish-workflows.md) |
| Instance MCP | Build/edit documented from 2.13.0; newer per-client settings layout from 2.33.0. Inspect live tool schemas and user/workflow access, with no blanket exposure. Offline plans remain the fallback. [MCP](https://docs.n8n.io/connect/connect-to-n8n-mcp-server.md) |
| Native Python | Docs place native Python runners at 1.111.0, stable in 2; Pyodide removed in 2.0. Cloud/self-hosted imports differ. Use verified target language/helpers, or provide pseudocode. [Code](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code) |
| Task runners | Official guidance calls for external mode on production/sensitive instances, matched n8n/runner image versions and worker coverage. Do not infer operational safety from a passing local snippet. [Task runners](https://docs.n8n.io/deploy/host-n8n/configure-n8n/set-up-task-runners.md) |
| Environments | Classic source-control environments require Business/Enterprise; newer Environments are Enterprise Preview. Sanitized exports in ordinary Git are the baseline, without claiming native environment support. [Environments](https://docs.n8n.io/administer/use-source-control-and-environments.md) |
| AI/memory/evaluation | Node availability, first-item sub-node behavior, memory/queue limits, vector isolation and metric-evaluation entitlements need separate checks. Use mocked fixtures before paid calls. [AI module](ai-workflows.md) |
| Redaction | Do not rely on paid viewer-redaction features or UI masking to sanitize exports, underlying storage, logs or outbound calls. [Testing module](testing-and-debugging.md) |

No supplied fixture is an import-ready n8n export. The fixture pack and offline helper have no claimed n8n version support; runtime compatibility remains not tested. For later exports record an explicit per-example matrix: n8n version, node versions, hosting/plan, imported result, mock runtime result, real-integration result and evidence date.

## Reuse official material

The [official n8n skills collection](https://github.com/n8n-io/skills) is optional reference material, not an installed dependency. Its README's 2.2.0 MCP baseline is not a promise that all tools/features work on that version. This module pack links to official documentation and does not vendor upstream skill source. If later copying/adapting upstream files, pin the reviewed commit and preserve applicable Apache-2.0 license/attribution notices; the enclosing repository's MIT license does not replace them. Installing hooks, connecting MCP or granting workflow access requires its own authorization.

## Operations handoff

Keep n8n-specific version/credential/export considerations here and route host/container/tunnel changes to the infrastructure workflow. Inventory the actual database, binary storage and encryption-key needs before planning backups. Keep the key separately protected; never request it in chat. Do not substitute a copied database for a verified consistent backup/restore plan. Editor/admin exposure is separate from webhook exposure. No restart, upgrade, publication or recovery drill is implied by authoring this skill.
