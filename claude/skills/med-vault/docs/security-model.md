# MedVault Security Model

## Design Principles

1. **Local by default.** No medication data leaves the user's device unless explicitly requested.
2. **Minimum data collection.** Only extract and store fields that have clear functional value.
3. **Audit everything.** All data mutations are logged with timestamps.
4. **Reversible over destructive.** Stopping a medication preserves history. Deletion is confirmed and logged.
5. **Transparent operations.** Every API call is disclosed. Offline mode is clearly labeled.

---

## Storage Architecture

### Local File Layout

```
MedVault/
├── medications.json          # Medication records (structured, versioned)
├── interactions.json         # Interaction analysis cache
├── schedule.json             # Current dosing schedule
├── audit.log                 # Append-only action log
├── images/                   # Uploaded label image files
│   └── [uuid].[ext]          # Renamed on import to avoid PII in filename
└── exports/                  # Generated export files
    └── [timestamp]-[type].[ext]
```

### Recommended Storage Paths

| OS | Path |
|---|---|
| Windows | `%USERPROFILE%\MedVault\` |
| macOS | `~/MedVault/` |
| Linux | `~/.medvault/` |

Users may specify a custom path. If the path is on an encrypted volume (e.g., BitLocker on Windows, FileVault on macOS), this provides filesystem-level encryption at rest.

---

## Data Encryption

### Current Implementation (v1.0.0)

MedVault stores data in plaintext JSON at the local path. Security at rest depends on:

- OS-level filesystem encryption (BitLocker, FileVault, LUKS)
- File permissions set to user-only access
- Physical device security

This is acceptable for the initial skill-based implementation. Encryption at the application layer is a Tier 1 planned upgrade.

### Planned: Application-Level Encryption (v1.1.0)

- AES-256-GCM encryption for `medications.json`
- Key derived from a user-set passphrase using PBKDF2 (100,000 iterations, SHA-256)
- Salt stored separately from encrypted data
- Key never stored on disk — derived fresh on each session open
- Image files encrypted individually with per-file AES keys

### Planned: Biometric Authentication (v1.2.0)

- Windows Hello integration for key derivation on Windows
- Touch ID / Face ID integration on macOS and iOS via .NET MAUI frontend
- Biometric unlock replaces passphrase prompt for daily use
- Passphrase remains as a backup unlock method

---

## Audit Log

The audit log (`audit.log`) is append-only. No entry is ever modified or deleted.

### Log Entry Format

```
[ISO8601 timestamp] [ACTION] [medication_id] [field] [old_value] → [new_value] [source]
```

### Logged Actions

| Action | Trigger |
|---|---|
| `CREATE` | `mv add` or `mv scan` save |
| `EDIT` | `mv edit` save |
| `STOP` | `mv stop` |
| `DELETE` | `mv delete` confirmation |
| `EXPORT` | `mv export` completion |
| `INTERACTION_CHECK` | Interaction engine run (logs count of findings and severity summary) |
| `OCR_IMPORT` | Image processed and saved |

### Example Log Entries

```
2026-05-15T10:32:14Z CREATE med-a1b2c3 — Metformin 500mg [source: manual]
2026-05-15T10:33:02Z INTERACTION_CHECK — 4 medications, 2 interactions found (0 Critical, 1 Major, 1 Moderate)
2026-05-15T11:15:44Z CREATE med-d4e5f6 — Lisinopril 10mg [source: ocr, image: images/d4e5f6.jpg]
2026-05-15T14:00:00Z EDIT med-a1b2c3 — frequency: "once daily" → "twice daily"
2026-05-15T16:22:11Z EXPORT — format: emergency-card, file: exports/2026-05-15-emergency-card.md
```

---

## Privacy Rules

### What MedVault Never Extracts or Stores

- Patient date of birth
- Patient address
- Insurance ID or group number
- Prescriber DEA number
- Social Security number or national ID
- Payment information

### Patient Name Handling

Prescription labels typically include the patient name. MedVault:

1. Detects the patient name field during OCR
2. Does not include it in the confirmation table by default
3. Displays a note: "Patient name detected. Not saving unless you request it."
4. Saves the name only if the user explicitly types `save patient name` or confirms when asked

### Image Storage

- Images are renamed to a UUID on import (removes any PII from the filename)
- Original filename is not stored
- Image content is not analyzed beyond the OCR pass
- Images can be deleted independently of the medication record via `mv delete-image [id]`

---

## Network and API Policy

### Conditions for Network Requests

MedVault makes network requests only for:

1. RxNorm name normalization (anonymous medication name lookup — no user data transmitted)
2. OpenFDA label data (anonymous NDC or drug name lookup — no user data transmitted)
3. DailyMed prescribing information (anonymous drug name lookup — no user data transmitted)

### What Is Never Transmitted

- Medication records
- Image files
- Patient names
- Audit logs
- Dosing schedules
- User identity

### Offline Mode

When no network access is detected, MedVault:

1. Skips API queries
2. Uses Claude's pharmacological knowledge for all analysis
3. Labels every interaction result as `[Offline — Claude knowledge base only]`
4. Recommends pharmacist verification for all results

---

## Export Security

Export files contain structured health data. MedVault:

1. Saves exports to the `MedVault/exports/` directory only
2. Prompts the user before any export: "This file will contain your full medication list. Keep it secure."
3. Does not transmit export files to any service
4. Includes a generated timestamp and format tag in each export filename
5. Logs all exports in the audit log

---

## Data Deletion

### mv stop

Marks the medication inactive. Record and history are preserved. No data is deleted.

### mv delete

Requires confirmation prompt before execution. After deletion:

- Medication record is removed from `medications.json`
- Audit log retains a record of the deletion action
- Image file reference is removed from the record (image file itself must be deleted manually or via `mv delete-image`)

### Full Data Wipe

To completely remove all MedVault data, the user deletes the MedVault directory. The skill does not maintain any data outside of this directory.

---

## Future Security Enhancements

| Feature | Target Version |
|---|---|
| AES-256-GCM application-level encryption | v1.1.0 |
| PBKDF2 key derivation from passphrase | v1.1.0 |
| Biometric authentication (Windows Hello, Touch ID) | v1.2.0 |
| Per-session key derivation (no key at rest) | v1.2.0 |
| Encrypted image storage | v1.2.0 |
| Secure export with password-protected ZIP | v1.3.0 |
| Tamper detection for audit log | v1.3.0 |
| Secure backup to user-controlled encrypted cloud storage | v2.0.0 |
