# Candidate helper and deployment follow-up, 2026-10-19

Mick authorized all four items from the focused follow-up review: prevent Obsidian note overwrites, contain saves within the chosen vault, correct stale migration documentation and review/correct the Proxmox deployment workflow. Changes apply only to canonical candidates and their allowed generated review copies. PR #11 remains draft; no installation, merging, promotion or live infrastructure action is authorized by this work.

## Obsidian helper

The original helper at baseline `dab7098c2710d8e29033543ee6ca86912bbc5619` was independently exercised with disposable files. Saving the same title replaced an existing note with exit 0. Passing `--folder ../outside` created a note outside the chosen vault with exit 0. No personal vault was used.

The corrected helper rejects absolute, drive-qualified, UNC and parent-traversal folders before writes, resolves the destination and refuses paths outside the selected vault, including an outward symlink or Windows junction. The vault must be an existing directory. Exclusive file creation refuses an existing filename without a check-then-overwrite window. Sanitized-title collisions and existing linked files are preserved. The skill tells the caller to choose a distinct title; updating an existing note is a separate requested edit.

Seven executable regression methods cover nested Unicode output/body preservation, repeated and sanitized-title collisions, invalid destination forms, missing/file vault paths, outward directory links, existing hardlinked files and concurrent creation with exactly one winner. Tests use disposable directories only. This is a local CLI helper correction, not native Obsidian, Apple Notes or fresh model certification. Destination resolution assumes the selected filesystem is not concurrently replaced by another writer; it is not an adversarial filesystem transaction.

Original shipped resource hashes remain in `migration.json`; `supporting_file_overrides` records the corrected helper hash and reason. Original helper SHA-256: `b1a4e1203f6dbed1794bb0e1d18c3af13d2bdae95d3205b264979203775dba03`; corrected candidate: `aeff847c020aac344b1fd96c4780fad559751d85428f912fbf730e2a44830bbd`. Instruction changes are exact recorded transformations. Generated Claude/ChatGPT copies must match the master; IdeaForge remains excluded from Cursor/Codex.

## Proxmox deployment review

The original candidate combined preflight guidance with concrete historical network/template defaults, a root application service, global Python package installation and unconditional tunnel steps. Those examples could contradict a request for an internal service or an unfamiliar host.

The revised candidate requires confirmed node/CT ID, template/storage, network and capacity inputs. Unknown inputs produce a parameterized plan, with execution waiting for the needed evidence and authorization. It keeps unprivileged containers separate from application identity, creates a dedicated non-login application account, uses a Python virtual environment and root-owned code, and defines a writable service state directory. Environment-file creation refuses existing paths. The service unit uses the dedicated identity and a verified application entrypoint; its example is not declared runnable for every application.

External access is conditional. The candidate preserves existing tunnel routes and requires the connector/origin path, approved hostname, access policy, validation and rollback. It distinguishes WAN port forwarding from an allowed LAN origin connection. It removes the downloaded-installer-to-root-shell recipe and the blanket privileged Home Assistant suggestion. Static guest addressing and DHCP reservations are distinguished. No Proxmox, systemd, UniFi or Cloudflare command was run against a live system.

All five Bash code blocks passed `bash -n` after synthetic parameter substitution. Seven static unit checks confirmed account/group, code/environment/state paths, virtual-environment command and privilege setting consistency. The example's exclusive environment-file creation succeeded once, refused a second attempt and preserved the existing synthetic bytes. Only the disposable file-creation fragment was executed; no deployment commands ran. Bash parsing and static unit checks do not replace `systemd-analyze verify` or application tests on the actual target.

The parameter choices were checked against the [official Proxmox administration guide](https://pve.proxmox.com/pve-docs/pve-admin-guide.pdf), [systemd execution settings](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html) and [Python virtual environment documentation](https://docs.python.org/3/library/venv.html). These sources support the mechanisms; they do not establish compatibility with an uninspected deployment. Source instructions and original frontmatter remain hash-pinned, with exact candidate transformations recorded.

## Documentation and deferred work

The canonical README and generic audit now distinguish historical confounded captures from corrected isolated runs, bounded accepted foundation/second-batch results, pending third-batch/native photo acceptance and unchanged build/promotion metadata. They explain explicit supporting-resource overrides instead of claiming all current candidate resources equal the originals.

Mick chose to defer the itinerary native phone check. Its unresolved booking-table/renderer result remains recorded and unchecked; deferral is not acceptance or a visual pass. Broader host/model/routing coverage and live deployment certification remain separate work.

## Validation

Clean Git-byte snapshot validation passed all 86 Python regressions, including seven Obsidian methods and source/transformation/resource provenance checks. Generator drift, repository and PowerShell quality (46 shipped skills, zero issues), exact-case folders (35 Claude skills, zero issues) and 24 offline cases with 99 negative checks passed. Only 24 generated files changed, all belonging to these two candidates or the resource manifest. Shipped source, packages, catalog, checksums, ecosystem decisions and model profiles are unchanged. Hosted checks are recorded against their exact delivered head in the PR description. Validation does not promote a skill or accept pending behavioral results.

The generic skill-creator validator accepts IdeaForge. It rejects Proxmox's pre-existing top-level `version` field, which this repository's schema explicitly supports. That metadata is preserved and the generic validator result is not reported as a pass. Native Codex frontmatter compatibility remains a pre-promotion adaptation issue; no installation or schema widening occurred here.
