---
name: proxmox-lxc
description: Deploy and configure Proxmox LXC containers for self-hosted services. Always trigger immediately when Mick asks to deploy, set up, or configure a new service on Proxmox, mentions spinning up a container, or needs a systemd service, Cloudflare Tunnel entry, or UniFi static IP assignment. Generate the full stack including the pct create command, container config, apt setup, systemd unit file, and Cloudflare Tunnel config entry from a service name and IP.
---

# Proxmox LXC Deployment

Deploy and configure Proxmox LXC containers for self-hosted services on Mick's homelab stack.

## Infrastructure Reference

| Item | Value |
| --- | --- |
| Proxmox host | Local network |
| UniFi controller | Static IP assignment via MAC |
| Cloudflare Tunnel | HTTPS exposure with no port forwarding |
| Existing containers | `CT 104` = `n8n` at `192.168.0.81` |
| Template | Ubuntu 22.04 standard |
| Next available CT ID | Ask Mick or check with `pvesh get /nodes/{node}/lxc` |

## Full Deployment Sequence

When asked to deploy a new service, generate all five of these pieces.

### 1. `pct create` command

```bash
pct create {CT_ID} local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst \
  --hostname {service-name} \
  --memory 512 \
  --cores 1 \
  --rootfs local-lvm:8 \
  --net0 name=eth0,bridge=vmbr0,ip={IP}/24,gw=192.168.0.1 \
  --nameserver 1.1.1.1 \
  --unprivileged 1 \
  --start 1
```

Adjust memory based on workload:

- Light: MCP server or small API, `512MB`
- Medium: Python app or n8n-like workload, `1024MB`
- Heavy: database or ML workload, `2048MB+`

### 2. Initial container setup

```bash
# Enter container
pct enter {CT_ID}

# Update and install basics
apt update && apt upgrade -y
apt install -y curl wget git python3 python3-pip

# For Python services
pip install {packages} --break-system-packages

# For Node services
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs
```

### 3. Application install and config

```bash
# Create app directory
mkdir -p /opt/{service-name}
cd /opt/{service-name}

# Install app
pip install {package} --break-system-packages

# Create .env file for secrets
cat > /opt/{service-name}/.env << EOF
API_KEY=your_key_here
API_BASE_URL=https://api.example.com
PORT=8000
EOF

chmod 600 /opt/{service-name}/.env
```

### 4. `systemd` service unit

```ini
# /etc/systemd/system/{service-name}.service

[Unit]
Description={Service Display Name}
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/{service-name}
EnvironmentFile=/opt/{service-name}/.env
ExecStart=/usr/bin/python3 /opt/{service-name}/server.py http
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable --now {service-name}
systemctl status {service-name}
journalctl -u {service-name} -f
```

### 5. Cloudflare Tunnel config entry

```yaml
ingress:
  - hostname: {service-name}.yourdomain.com
    service: http://{IP}:{PORT}
  - service: http_status:404
```

```bash
systemctl restart cloudflared
curl https://{service-name}.yourdomain.com/health
```

## UniFi Static IP Assignment

1. Open UniFi controller and go to `Clients`
2. Find the container by hostname or MAC
3. Open settings and assign the fixed IP
4. Apply and reprovision if needed

You can also set the IP at creation time with `--net0 ... ip={IP}/24`.

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
- Cloudflare Tunnel config updated and restarted
- External URL responds correctly
