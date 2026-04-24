---
name: pihole-csv-analyzer
description: Analyze CSV exports from Pi-hole such as query logs, top domains, top clients, or adlist exports and produce actionable recommendations. Trigger immediately when the user uploads or mentions a Pi-hole CSV file, types "pihole" or "ph analyze", or asks to analyze DNS query data, blocklist hits, or Pi-hole exports. Produce an in-chat analysis plus candidate blocklist and allowlist outputs for review.
---

# Pi-hole CSV Analyzer

Analyze Pi-hole CSV exports and turn them into practical, reviewable cleanup actions.

## Supported Inputs

This skill should handle:

- query log exports
- top domains exports
- top clients exports
- blocklist or adlist exports

If the format is ambiguous, inspect the header row and the first few rows before proceeding.

## Export Type Detection

Use the CSV header to identify the likely export type.

| Export Type | Typical Columns | Typical Source |
| --- | --- | --- |
| Query Log | `time`, `type`, `domain`, `client`, `status`, `reply_type`, `reply_time`, `dnssec` | Pi-hole web UI query log export |
| Top Domains | `domain`, `count` or `hits` | Dashboard top permitted or blocked domains |
| Top Clients | `client`, `count` or `hits` | Dashboard top clients |
| Blocklist or Adlist | `address`, `enabled`, `comment`, `group`, `date_added` | Adlist or domain export |

Pi-hole v6 exports can vary slightly. Normalize column names before applying logic.

## Query Status Mapping

When analyzing query-log exports, use Pi-hole's documented query-database status meanings.

Common blocked status values:

- `1` blocked by gravity
- `4` blocked by regex denylist
- `5` blocked by exact denylist
- `6` blocked by upstream known blocking IP
- `7` blocked by upstream null response
- `8` blocked by upstream `NXDOMAIN` with `RA` bit unset
- `9` blocked by gravity during deep CNAME inspection
- `10` blocked by regex during deep CNAME inspection
- `11` blocked by exact denylist during deep CNAME inspection
- `15` blocked while the database is busy
- `16` blocked special domains
- `18` blocked by upstream `EDE 15`

Common allowed status values:

- `2` allowed and forwarded
- `3` allowed and replied from cache
- `12` allowed retried query
- `13` allowed retried but ignored query
- `14` allowed already forwarded
- `17` allowed and replied from stale cache

Treat unknown or new status values carefully and flag them instead of guessing.

## Analysis Workflow

### 1. Normalize the data

- normalize column names to lowercase
- strip extra whitespace
- detect whether status values are numeric or text

### 2. Compute the high-value summary

For query-log exports, compute:

- total query volume
- blocked versus allowed volume
- top allowed domains
- top blocked domains
- top clients by volume
- unusually noisy clients
- suspicious allowed domains that may deserve review

For top domains or top clients exports, normalize the columns and rank by count.

For blocklist or adlist exports, summarize enabled versus disabled state and obvious cleanup opportunities.

### 3. Generate review candidates

#### Blocklist candidates

Flag allowed domains that look suspicious based on signals such as:

- telemetry or tracking patterns
- free-TLD abuse indicators such as `.tk`, `.cf`, `.gq`, `.ml`
- IP-style subdomain patterns
- long random-looking subdomains
- repeated high-volume domains tied to a single client with no obvious user-facing purpose

Avoid recommending major infrastructure or obviously essential domains without a strong reason. Be conservative.

#### Allowlist candidates

Flag blocked domains that may be legitimate when they:

- are tied to sign-in, updates, streaming, or other common core functionality
- appear frequently among blocked queries
- clearly belong to major legitimate platforms

### 4. Output

Always provide an in-chat summary with:

- overview metrics
- top allowed and blocked domains
- top clients
- noisy-client callouts
- suspicious allowed domains
- possible allowlist candidates
- practical next-step recommendations

Also produce reviewable candidate outputs named:

- `blocklist_candidates.txt`
- `allowlist_candidates.txt`

If the environment supports file output, create those files. Otherwise, present their contents inline in clearly separated sections.

## Reference Logic

Use Pi-hole's documented status values as the source of truth. For example, a basic numeric mapping can start like this:

```python
BLOCKED_STATUSES = {1, 4, 5, 6, 7, 8, 9, 10, 11, 15, 16, 18}
ALLOWED_STATUSES = {2, 3, 12, 13, 14, 17}
```

When string-style status values appear instead of integers, use cautious text matching and keep uncertainty visible.

## Edge Cases

- Empty or malformed CSV files: explain what is wrong and what is expected
- No blocked queries: say so directly
- No suspicious domains: say so directly
- IPv6 clients: display as-is
- Large files: summarize and sample pattern analysis if needed
- Unknown status values: flag them as unknown instead of forcing a blocked or allowed label

## Style

- Lead with the most actionable findings
- Keep the output concise and practical
- Do not invent recommendations
- Be explicit when confidence is low
- Treat generated blocklist and allowlist entries as review queues, not final policy
