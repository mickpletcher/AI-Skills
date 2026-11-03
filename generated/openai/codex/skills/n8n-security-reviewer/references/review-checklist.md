# Security review checklist

Apply only to supplied evidence. Missing settings are unknown until matching-version defaults and effective deployment configuration are established. Keep potential risk separate from actual exposure.

## Credentials and privilege

- Distinguish credential references (names/IDs) from inline secret material. Inspect headers imported from cURL, URL userinfo/query tokens, request bodies, expressions, Code nodes, notes, pinned/sample data, and notification templates. Report values redacted. References do not prove the credential exists, is encrypted at rest, or has narrow scopes.
- Ask for non-secret credential scope/role metadata and workflow/project sharing details when needed. Check least-privilege service identities, separate test/production credentials, resource scoping, and who may edit or execute workflows using them. A name such as “read-only” is not permission evidence.
- Treat encryption-key backup/access and credential rotation as configuration/evidence questions. Never request the key or rotate anything. If secret material may have been shared, recommend owner-led containment and rotation according to incident context, without declaring the secret active.
- External secret stores, project roles, and custom RBAC have version/edition gates. Do not require an unavailable paid feature as the only fix. Ordinary n8n credentials and reduced sharing may be appropriate alternatives.

## Webhooks, network exposure, and authorization

- Inspect explicit node authentication, credentials references, intended callers, request signatures/replay protection, and all routes to privileged effects. Editor login is not webhook authentication. HTTPS or a Cloudflare Tunnel does not itself authenticate callers. An unguessable path or CORS is not authorization.
- Separate no built-in authentication from internet exposure. Reverse proxy, gateway/service-token auth, IP controls, or in-workflow signature verification may protect a route, but require evidence of actual coverage and ordering. An IF label or `onlyRunIf` expression alone is insufficient. Verify fail-closed behavior, false/error outputs, raw-body handling where signatures require it, and replay/time-window checks where relevant.
- A test webhook and production webhook are different surfaces. An export's active flag, absent flag, or saved editor state does not establish the published runtime state. Disabled/disconnected nodes still merit dormant-risk notes, not claims that they currently run.
- Inspect response bodies/headers and Respond to Webhook branches for unfiltered input, secrets, internal errors, or excessive record disclosure. Ask about rate/payload/concurrency limits only where abuse could matter; do not invent their effective values.

## Untrusted data and high-impact operations

- Follow external webhook, form, email, RSS, uploaded-file, API, and AI-output inputs into Code, shell, file paths, SQL, URL targets, template/HTML responses, and external messaging. Validate schemas/types/lengths; normalize and explicitly allow values appropriate to the sink.
- Distinguish parameterized SQL values from dynamic SQL identifiers or concatenated queries. Do not call any expression in a query a confirmed SQL injection without establishing the data source and sink semantics.
- Inspect Code and Execute Command content as text. Presence alone is a review point. Look for code-as-data, dynamic evaluation, shell interpolation, filesystem/environment access, broad imports, and all relevant guards. Never execute a payload to demonstrate risk.
- External task runners improve isolation, but actual container user, mounts, capabilities, import allowlists, network access, and insecure-mode overrides need deployment evidence. Do not claim that default sandboxing makes arbitrary user code safe.
- For AI workflows, treat retrieved content, prompts from callers, model output, and tool arguments as untrusted. Inspect tool scope, allowed destinations, data minimization, cross-user memory/vector access, and authorization gates before external effects. Prompt instructions are not an access-control boundary. Approval nodes must cover every consequential branch and bind the exact pending action.
- Retries and error paths can duplicate harmful side effects or bypass checks. Respect any supplied retry/attempt policy and distinguish uncertain outcome from confirmed failure. This review recommends changes only.

## HTTP and egress

- Check plain HTTP, ignored TLS validation, URL userinfo/tokens, dynamic hosts/schemes/ports, pagination next-URLs, redirects, proxy settings, and data sent with credentials. A dynamic URL is a conditional SSRF or exfiltration risk, not proof of exploitability.
- Establish whether untrusted input controls the destination and whether validation, DNS resolution, redirects, and network egress restrictions constrain it. Internal endpoints may be intentional; require the threat model before calling them vulnerable.
- Native SSRF protection is version-specific and defense in depth. Host allowlists may bypass IP blocking. Absence from a workflow export says nothing about effective instance/network controls.
- Unknown/community/custom nodes need separate implementation and dependency provenance review. Do not assume an unknown node is malicious or that a built-in node is safe.

## Execution data, logs, and evidence retention

- Inspect workflow save-on-error/success/manual/progress settings, pinned/static data, error-notification bodies, response payloads, and supplied log samples. A `console.log` or saved execution is not proof that secrets are recorded; identify the actual data path.
- Review effective retention/pruning, viewer access, external log sinks, binary storage/backups, and sensitive-data minimization using supplied metadata. Saving disabled at one layer does not prove deletion from logs, exports, backups, or previous executions.
- Execution redaction restricts visibility; it is not secure erasure, data minimization, or a substitute for access control. Plan and version constraints apply, and privileged reveal behavior must be considered.
- Never recommend destroying incident evidence reflexively. Separate authorized future retention changes from existing legal, operational, and incident-preservation needs.

## Deployment/version boundary

Check exact version evidence, release/advisory source freshness, Cloud versus self-hosted responsibilities, TLS termination/proxy trust, authentication/access control, node exclusions, runners, network restrictions, file/env access, and backup protections only when relevant evidence exists. An export alone cannot certify the host or its patch status. Do not browse private URLs from supplied artifacts. Public release/advisory checks must be matched to actual version, component, and configuration; a CVE identifier alone is not a finding.
