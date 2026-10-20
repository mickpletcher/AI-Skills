---
name: proxmox-lxc
description: Deploy and configure Proxmox LXC containers for self-hosted services. Always trigger immediately when Mick asks to deploy, set up, or configure a new service on Proxmox, mentions spinning up a container, or needs a systemd service, Cloudflare Tunnel entry, or UniFi static IP assignment. Generate the full stack including the pct create command, container config, apt setup, systemd unit file, and Cloudflare Tunnel config entry from a service name and IP.
version: 1.1.0
---

# Proxmox LXC Deployment

## Intent

Plan and document Proxmox LXC deployments for Mick's homelab with practical container setup, networking, and maintenance steps.

## Use When

- The user explicitly asks for `proxmox-lxc`.
- The request matches the triggers or workflow described below.
- The task benefits from a reusable, structured output instead of a one-off answer.

## Do Not Use When

- Do not use for VM-only designs, Kubernetes, cloud deployments, or destructive production changes without explicit confirmation.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

## Workflow

1. Identify the exact task and available source material.
2. Apply the domain rules and output format in this skill.
3. State assumptions, uncertainty, and missing inputs clearly.
4. Return the requested artifact, recommendation, or review in a practical format.
5. Check the result against the validation checklist before finishing.

## Constraints

- Do not fabricate missing facts, measurements, dates, sources, or user context.
- Keep output aligned with Mick's direct, practical communication style unless the skill says otherwise.
- Preserve safety, legal, medical, financial, and operational boundaries stated in this file.
- Prefer concise, usable output over broad explanation.

## Validation Checklist

- [ ] The output matches the skill's intended task and platform.
- [ ] Required inputs, assumptions, and uncertainty are explicit.
- [ ] Safety, scope, and source limits are respected.
- [ ] The response follows the requested format or the skill's default output format.
- [ ] The result is practical enough to use without another cleanup pass.

Deploy and configure Proxmox LXC containers for self-hosted services on Mick's homelab stack.

## Deployment Inputs

Read the target host's supplied inventory or request the missing values. Do not treat historical homelab details as current configuration.

- Confirm the Proxmox node, an unused cluster-wide CT ID, an available template volume, storage pool and backup target.
- Confirm IP/CIDR, bridge, gateway if required, DNS servers, VLAN and allowed client/origin connections. An unanswered ping alone does not establish that an IP is unused.
- Check host capacity and size memory, cores and disk for the workload and data growth.
- Default to an unprivileged container. Explain any specific device mapping or privilege exception; do not switch to privileged mode merely to bypass a setup failure.
- Separate container privilege from application identity: a generic application service runs as a dedicated non-login account. Use root only for setup or a documented application requirement.
- Select a supported OS template and application runtime from actual inventory and current vendor requirements. Do not invent a template filename, gateway or available storage.
- Keep internal services internal unless external access was requested. Tunnel configuration requires the existing connector location, reachable origin address, approved hostname and access policy. It does not authorize publishing an administrative interface.

If required values are missing, provide a clearly labeled parameterized plan and request those values before execution. Do not claim preflight, deployment, exposure or rollback succeeded without actual evidence. Planning does not authorize changes to Proxmox, UniFi or Cloudflare.

## Service Recipes

Common services deviate from the generic sequence in known ways. Apply these adjustments on top of the full deployment sequence:

| Service | Memory | Disk | Notes |
| --- | --- | --- | --- |
| Pi-hole | 512MB | 8GB | Port 53 TCP/UDP plus web UI; set the container as DNS only after verifying it resolves |
| Home Assistant | 2048MB | 16GB | Assess specific USB device mappings; do not default to privileged mode. Prefer HAOS VM when its features are required. |
| Ollama / local LLM | 4096MB+ | 32GB+ | Models dominate disk; GPU passthrough needs the host driver plus cgroup device entries |
| PostgreSQL / MariaDB | 2048MB | 16GB+ | Put data on a dedicated mount point; schedule dumps, not just snapshots |
| Grafana / monitoring | 1024MB | 8GB | Pair with a metrics store; do not point it at production databases without a read-only user |
| FastAPI / MCP server | 512MB | 8GB | Starting estimate only; verify runtime, entrypoint, data path and access requirements. |

For services not listed, follow the generic sequence and say which recipe assumptions were borrowed.

## Backup And Rollback

Make changes testable before they are permanent:

- snapshot before any in-container upgrade or config change: `pct snapshot {CT_ID} pre-{change}-$(date +%Y%m%d)`
- snapshots are not backups; schedule `vzdump` to storage that is not the same disk as the containers, and verify a restore once rather than assuming
- for stateful services, back up the application data path (database dumps, `/opt/{service}` config) separately from the container image so data can restore into a rebuilt container
- write the rollback step next to the change step in any plan this skill outputs; a change without a rollback line is incomplete

## Full Deployment Sequence

Generate the applicable pieces below after resolving the deployment inputs. These are parameterized examples, not commands that were executed. Substitute validated values; do not pass user-supplied text directly into a shell.

### 1. Container creation

```bash
pct create {CT_ID} '{TEMPLATE_VOLUME}' \
  --hostname {service-name} \
  --memory {MEMORY_MB} \
  --cores {CORES} \
  --rootfs '{STORAGE}:{DISK_GB}' \
  --net0 'name=eth0,bridge={BRIDGE},ip={IP_CIDR},gw={GATEWAY}' \
  --nameserver '{DNS_SERVERS}' \
  --unprivileged 1 \
  --start 0
```

Omit `gw=` when no gateway is required; add the confirmed VLAN tag only when applicable. Verify the resulting config before the separately authorized `pct start {CT_ID}`. Confirm both the ID and target before rollback; do not generate an unconditional `pct destroy` cleanup.

### 2. Container setup

After creation and authorized startup, enter the new container. Package setup runs inside it, not on the Proxmox host.

```bash
pct enter {CT_ID}
apt update
apt install -y ca-certificates python3 python3-venv
```

Use the selected application's documented runtime and package repository. For Node services, verify the supported release and repository setup before installation; do not pipe a downloaded installer directly into a root shell. Plan OS upgrades separately when they could change an existing service.

### 3. Python application and identity

This example applies to a Python service. Confirm the account is new or already belongs to this application; do not reuse another service's identity.

```bash
useradd --system --user-group --home-dir /var/lib/{service-name} --no-create-home --shell /usr/sbin/nologin {service-user}
install -d -o root -g root -m 0755 /opt/{service-name}
python3 -m venv /opt/{service-name}/.venv
/opt/{service-name}/.venv/bin/python -m pip install '{package}'
(umask 077; set -o noclobber; : > /opt/{service-name}/.env)
```

Install reviewed application files under the root-owned application directory and replace the unit's example entrypoint with the verified command. Keep runtime writes in `/var/lib/{service-name}`, not the code or virtual environment. Populate the root-readable environment file locally without logging secrets; the system service manager reads it before dropping privileges. The exclusive environment-file creation refuses an existing path; preserve and review any existing configuration rather than replacing it. Preserve existing config and application data before any update.

### 4. Service unit and verification

```ini
[Unit]
Description={Service Display Name}
After=network.target

[Service]
Type=simple
User={service-user}
Group={service-user}
WorkingDirectory=/opt/{service-name}
EnvironmentFile=/opt/{service-name}/.env
StateDirectory={service-name}
StateDirectoryMode=0750
ExecStart=/opt/{service-name}/.venv/bin/python /opt/{service-name}/server.py http
NoNewPrivileges=yes
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Write the reviewed unit to `/etc/systemd/system/{service-name}.service`. Check its application command, account permissions, writable data path and target systemd version, then validate before starting it.

```bash
systemd-analyze verify /etc/systemd/system/{service-name}.service
systemctl daemon-reload
systemctl enable --now {service-name}
systemctl status --no-pager {service-name}
journalctl -u {service-name} -n 50 --no-pager
```

Verify the actual local health endpoint and service identity, then test only the approved client path. Record a stop/disable and config/data restoration procedure next to the change. Use application-specific units for non-Python services; the generic unit is not proof of compatibility.

### 5. Optional external access

Skip this section for internal-only services. If external access was requested, review the existing tunnel configuration and access policy before proposing an ingress change. The connector must be able to reach the selected origin; confirm bind address and firewall rules for that path. A separate connector may need an allowed LAN origin connection even though no inbound WAN port forwarding is required.

```yaml
ingress:
  - hostname: {APPROVED_HOSTNAME}
    service: http://{ORIGIN_ADDRESS}:{PORT}
  - service: http_status:404
```

Merge the proposed entry into the existing ingress list before its final catch-all; preserve other routes. Back up and validate the configuration, apply only the authorized change, verify the expected authentication and health behavior, and retain the exact prior configuration for rollback. Do not restart a shared connector just because this example includes an ingress entry.

## UniFi Addressing

Use either a verified static address outside the DHCP allocation range or an appropriate DHCP reservation. Match the container's chosen address mode; a reservation does not configure a guest that uses a different static address. Confirm the correct network, MAC and conflict status before any separately authorized controller change.

## Common Service Port Reference

| Service | Default Port |
| --- | --- |
| n8n | 5678 |
| FastMCP or FastAPI | 8000 |
| Home Assistant | 8123 |
| Grafana | 3000 |
| Portainer | 9000 |
| Ollama | 11434 |

## Maintenance Commands

```bash
# List all containers
pct list

# Start, stop, restart
pct start {CT_ID}
pct stop {CT_ID}
pct restart {CT_ID}

# Enter container shell
pct enter {CT_ID}

# Check status
pct status {CT_ID}

# Snapshot before major changes
pct snapshot {CT_ID} pre-update-$(date +%Y%m%d)

# Restore snapshot
pct rollback {CT_ID} pre-update-YYYYMMDD
```

## Quick Deploy Checklist

- CT ID chosen without conflict
- Static IP chosen outside the DHCP conflict range
- `pct create` command completed successfully
- Packages installed inside the container
- App files placed in `/opt/{service-name}/`
- `.env` file created with `chmod 600`
- `systemd` unit file created and enabled
- Service starts cleanly
- Service runs under its confirmed application account with the intended writable data path
- Approved client path and actual health endpoint verified
- External access configured only if requested, with authentication and rollback verified

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- The service you want to host plus any network, storage, or security constraints.

Example prompts:

- `Use proxmox-lxc to plan a new LXC container for an internal automation service.`
- `Help me deploy and harden an LXC on Proxmox for self hosted tooling.`
- `Show me the best example prompt for asking this skill for an LXC setup plan.`


## Host Capabilities

Use only tools, files, conversation history, and connected services actually available and authorized in the current host. If browsing, image/document inspection, code execution, persistent storage, or a related skill is unavailable, state the limitation and request the needed input or provide manual steps. Never claim a lookup, save, execution, publication, or installation occurred without evidence. Preserve the domain safety and confirmation rules above.

## Capability Contract

Read `capabilities.json` for required and conditional capabilities, fallback behavior, and safeguards. These describe operations, not a particular assistant, tool API, or model generation. Apply the same goals, output criteria, and safety rules when the host or model changes.
