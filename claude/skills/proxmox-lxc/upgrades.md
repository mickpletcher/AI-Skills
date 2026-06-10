# Upgrade Log: proxmox-lxc

Tracks implemented upgrades to this skill. Future upgrade ideas are in [future-upgrades.md](future-upgrades.md) (local only, not tracked in git).

| Date | Upgrade | Notes |
|------|---------|-------|
| 2026-06-10 | Added pre-deployment checks | CT ID, IP, resources, disk growth, privilege, and network placement are verified before pct create. |
| 2026-06-10 | Added service recipes | Pi-hole, Home Assistant, Ollama, databases, Grafana, and API servers get sizing and known deviations. |
| 2026-06-10 | Added backup and rollback guidance | Snapshots before changes, vzdump as real backup, data-path backups, and rollback lines in every plan. |
