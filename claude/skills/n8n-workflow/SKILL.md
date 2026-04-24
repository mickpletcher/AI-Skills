---
name: n8n-workflow
description: Design, build, or troubleshoot n8n automation workflows. Always trigger immediately when Mick mentions n8n, workflow nodes, automating a pipeline, or connecting services via n8n. Covers node selection, webhook patterns, Claude API integration, credential setup, Cloudflare Tunnel exposure, and Proxmox LXC deployment. Mick runs n8n on Proxmox CT 104 at 192.168.0.81:5678 with Cloudflare Tunnel for HTTPS.
---

# n8n Workflow Builder

Design, build, or troubleshoot n8n automation workflows for Mick's self-hosted Proxmox environment.

## Mick's n8n Stack

- **Instance:** Proxmox LXC CT 104, static IP `192.168.0.81`, port `5678`
- **External access:** Cloudflare Tunnel to an HTTPS subdomain
- **Primary use cases:** morning briefing pipeline, trading alerts, RSS processing, Claude API orchestration, webhook receivers
- **Claude API integration:** HTTP Request node to `https://api.anthropic.com/v1/messages`

## Workflow Design Principles

1. **One trigger, one purpose:** Keep workflows focused. Chain them with webhooks when needed.
2. **Error handling on every external call:** Add an Error Trigger or use `Continue on Fail` with a downstream notification step.
3. **Credentials in the n8n credential store:** Never hardcode API keys in nodes. Use named credentials.
4. **Use a Set node to normalize data:** Clean up fields before passing data to downstream steps.
5. **Test with static data first:** Pin node output during development and unpin for production.

## Common Node Patterns

### HTTP Request to Claude API

```json
{
  "method": "POST",
  "url": "https://api.anthropic.com/v1/messages",
  "headers": {
    "x-api-key": "={{ $credentials.anthropicApi.apiKey }}",
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
  },
  "body": {
    "model": "use-your-current-claude-model",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": "={{ $json.prompt }}"
      }
    ]
  }
}
```

Extract the response with:

```text
{{ $json.content[0].text }}
```

### Webhook Trigger

- Node: `Webhook`
- Method: `POST`
- Path: `/your-endpoint-name`
- Authentication: Header auth with downstream `IF` validation of `X-Webhook-Secret`
- External URL via Cloudflare: `https://n8n.yourdomain.com/webhook/your-endpoint-name`

### Schedule Trigger

- Node: `Schedule Trigger`
- Common patterns:
  - Daily 6am: `0 6 * * *`
  - Every 15 minutes: `*/15 * * * *`
  - Weekdays only at 7am: `0 7 * * 1-5`

### RSS Feed Processing

```text
Schedule Trigger
  -> HTTP Request (GET RSS feed URL)
  -> XML node (parse feed)
  -> SplitInBatches (process items)
  -> IF (filter by date or keyword)
  -> Set (normalize fields: title, link, pubDate, summary)
  -> Merge or Aggregate
  -> HTTP Request (Claude API for summarization)
```

### Error Notification Pattern

```text
[Any node with Continue on Fail enabled]
  -> IF (check {{ $json.error }} exists)
    -> True branch: HTTP Request to Slack, Teams, or Discord webhook
       Body: "Workflow failed: {{ $workflow.name }} | Error: {{ $json.error.message }}"
```

## Morning Briefing Pipeline Pattern

```text
Schedule Trigger (6am weekdays)
  |- HTTP Request -> CoinGecko API (BTC, ETH prices)
  |- HTTP Request -> RSS feeds (tech news)
  `- HTTP Request -> Reddit API (r/algotrading, r/homelab)

Merge (all three branches)
  -> Set (combine into single prompt string)
  -> HTTP Request -> Claude API
     Prompt: "Summarize this morning's briefing: {combined_data}"
  -> Send Email, Slack, or Discord
```

## Cloudflare Tunnel Config

Append an ingress entry to the existing `cloudflared` config when external webhook access is needed:

```yaml
ingress:
  - hostname: n8n.yourdomain.com
    service: http://192.168.0.81:5678
  - service: http_status:404
```

Restart the tunnel after config changes:

```bash
systemctl restart cloudflared
```

## Proxmox LXC Maintenance

```bash
# Check n8n service status
pct exec 104 -- systemctl status n8n

# View logs
pct exec 104 -- journalctl -u n8n -f

# Restart n8n
pct exec 104 -- systemctl restart n8n

# Update n8n
pct exec 104 -- npm update -g n8n
```

## Credential Setup Reference

| Service | Credential Type | Key Fields |
| --- | --- | --- |
| Anthropic Claude | Header auth | `x-api-key` |
| CoinGecko | None for the free tier | None |
| Alpaca | Header auth | `APCA-API-KEY-ID`, `APCA-API-SECRET-KEY` |
| Reddit | OAuth2 | `client_id`, `client_secret` |
| SMTP or email | SMTP | `host`, `port`, `user`, `pass` |

## Quality Checklist

- Trigger node defined: schedule, webhook, or manual
- Credentials stored in the n8n credential store
- Error handling present on external HTTP calls
- Set node used to normalize data between major steps
- Claude API node extracts `content[0].text`
- Webhook endpoints use secret header validation
- Cloudflare Tunnel config updated when external access is needed
