# MedVault Upgrade Roadmap

## Current: v1.0.0 (2026-05-15)

Initial skill release. Covers the core medication tracking workflow: manual entry, OCR label scanning, interaction analysis, schedule generation, and local data export. All analysis runs inside Claude Code with no external dependencies required.

---

## v1.1.0 — Application-Level Encryption

**Target:** Near-term

**Changes:**
- AES-256-GCM encryption for `medications.json` and `interactions.json`
- PBKDF2 key derivation from user passphrase (100,000 iterations, SHA-256)
- Salt stored in a separate `medvault.salt` file
- Encrypted image files (per-file AES keys)
- Password-protected ZIP export option
- Tamper detection for audit log via SHA-256 hash chain

**Why:** The initial version relies on OS-level filesystem encryption. This upgrade adds an independent layer that protects data even if filesystem encryption is bypassed or not configured.

---

## v1.2.0 — Biometric Authentication

**Target:** After encryption layer is stable

**Changes:**
- Windows Hello integration for vault unlock
- macOS Touch ID / Face ID integration (requires .NET MAUI groundwork)
- Passphrase remains as backup unlock
- Per-session key derivation from biometric confirmation

**Why:** Passphrase prompts create friction for daily use. Biometric unlock makes the security model practical without weakening it.

---

## v1.3.0 — DrugBank API Integration

**Target:** After API key licensing is obtained

**Changes:**
- DrugBank provider implementing the `MedVaultApiProvider` interface
- Comprehensive drug-drug interaction database (significantly broader than public APIs)
- Pharmacokinetic profile data for scheduling optimization
- Drug target and mechanism of action data for interaction explanations
- Confidence levels recalibrated with DrugBank as highest-authority source

**Why:** Public APIs (RxNorm, OpenFDA, DailyMed) cover FDA-labeled interactions well but miss many clinically relevant interactions not explicitly in prescribing information. DrugBank fills this gap.

---

## v1.4.0 — Refill Prediction and Adherence Scoring

**Target:** After core data is stable with enough history

**Changes:**
- Supply quantity tracking per medication (pills remaining, days supply)
- Refill prediction: calculate projected run-out date, alert N days before
- Adherence scoring: user confirms each dose; streak tracking and missed-dose logging
- Adherence report: weekly summary showing adherence rate per medication
- Missed dose guidance: per-medication instructions for what to do if a dose is skipped (based on prescribing label)

**Why:** Tracking when medications were taken closes the loop from scheduling to actual adherence. Refill prediction prevents running out unexpectedly.

---

## v1.5.0 — Side Effect and Effectiveness Journal

**Target:** After adherence scoring is in place

**Changes:**
- Symptom log: user records symptoms with timestamp and severity rating
- Correlation engine: associates reported symptoms with medications based on timing
- Effectiveness rating: user rates perceived effectiveness of each medication periodically
- Journal export: structured log of symptoms and ratings for physician visits
- Side effect flags: when a known side effect of a medication appears in the symptom log, surface it

**Why:** Gives users a structured way to track how they feel on a regimen, which is valuable data for doctor visits and medication adjustments.

---

## v2.0.0 — .NET MAUI Mobile Frontend

**Target:** Medium-term, after skill layer is mature

**Changes:**
- Cross-platform mobile app (iOS and Android) built with .NET MAUI
- Offline-first architecture: full functionality without network
- Sync with Claude skill vault via local JSON file (no cloud sync by default)
- Native camera integration for label scanning
- Push notification reminders for scheduled doses
- Biometric unlock on mobile (Face ID, fingerprint)
- Apple Health write: log dose adherence events to Apple Health
- HealthKit read: import existing medication data from Apple Health pharmacy records

**Why:** The Claude Code skill is powerful but requires a desktop. A mobile app makes MedVault usable at the point of care — at a pharmacy, a doctor's office, or when taking medications on the road.

---

## v2.1.0 — Family Medication Profiles

**Target:** After mobile frontend is stable

**Changes:**
- Multiple named profiles within one vault
- Profile switching with optional authentication per profile
- Shared interaction analysis across profiles (detect interactions between a patient's medications and a caregiver's medications, for example)
- Family emergency card combining key medications from all active profiles
- Role-based access: owner profile can view all; member profiles can view their own

**Why:** Many users manage medications for family members — children, elderly parents, spouses. A single vault per person does not fit how households actually work.

---

## v2.2.0 — Voice Input

**Target:** After mobile frontend is stable

**Changes:**
- Hands-free medication entry via speech-to-text
- Voice command support: "Add Metformin 500mg twice daily"
- Transcription review step before saving (same confirmation workflow as OCR)
- Wake word support on mobile for reminder acknowledgment: "I took it"

**Why:** Voice input is the lowest-friction entry method. Critical for accessibility and for situations where hands are occupied.

---

## v2.3.0 — Travel Medication Mode

**Target:** Medium-term

**Changes:**
- Country-specific drug import restriction database
- For each active medication: flag if controlled in the destination country and provide guidance
- TSA/customs documentation generator: structured letter listing medications, dosages, and prescribing doctor
- Time zone adjustment calculator for medications with narrow therapeutic windows
- Travel supply calculator: days supply needed, account for delays, recommend buffer
- Insulin travel guidance: temperature storage requirements, airline policies

**Why:** International travel with medications is complicated. Import restrictions, time zone shifts, and temperature-sensitive storage are real problems that generic travel apps do not handle well.

---

## v3.0.0 — Wearable Integration

**Target:** Long-term

**Changes:**
- Apple Watch complication showing next scheduled dose
- Garmin Connect IQ widget for dose reminders
- Adherence acknowledgment from wrist: tap to confirm dose taken
- Integration with heart rate variability data (HRV) to correlate medication timing with recovery metrics (relevant for athletes)

**Why:** Wearable reminders eliminate the need to check the phone. For athletes tracking HRV and recovery, correlating medication timing with training response data adds real value.

---

## Long-Term Exploration

These features are not scheduled but are worth designing for:

- **Telehealth export:** Structured medication list formatted for major telehealth platform intake forms
- **Pharmacy API integration:** Automated refill requests via national pharmacy APIs (Walgreens, CVS, RxSense)
- **AI-powered interaction research:** Claude-powered deep dive on new drug additions using the latest research, not just FDA-labeled interactions
- **Medication cost tracking:** Compare pharmacy prices for each medication, flag generic alternatives
- **Prescription handwriting OCR:** Support for handwritten prescription pads (harder OCR problem than printed labels)
- **Faxed document parsing:** PDF support for faxed prescriptions from specialist offices
