# proxmox-lxc

A Claude skill for deploying and configuring Proxmox LXC containers on Mick's self-hosted homelab stack.

## Source of Truth

Use [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/proxmox-lxc/SKILL.md) as the canonical source for this skill. The packaged [proxmox-lxc.skill](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/proxmox-lxc/proxmox-lxc.skill) file is the Claude-ready export built from it.

## What It Does

Generates a full Proxmox LXC deployment stack for a new service from a single request. Given a service name and IP address, it can produce:

1. the `pct create` command
2. initial container setup commands
3. application install and config steps
4. a `systemd` service unit
5. a Cloudflare Tunnel ingress entry

## Trigger Phrases

| Phrase | Action |
| --- | --- |
| `deploy [service] on Proxmox` | Full five-step deployment stack |
| `spin up a container for...` | New LXC with all configs |
| `add [service] to Cloudflare Tunnel` | Tunnel config entry only |
| `systemd service for...` | Unit file only |
| `set up static IP for...` | UniFi assignment steps |

## Infrastructure Notes

- Base template: Ubuntu 22.04 standard
- Gateway: `192.168.0.1`
- DNS: `1.1.1.1`
- Known container: `CT 104` is `n8n` at `192.168.0.81`
- Networking: UniFi static IP assignment or `--net0` at creation
- Exposure: Cloudflare Tunnel, no direct port forwarding

## File Structure

```text
proxmox-lxc/
|-- README.md
|-- SKILL.md
|-- upgrades.md
`-- proxmox-lxc.skill
```

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `proxmox-lxc.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
