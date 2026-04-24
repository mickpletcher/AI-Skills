---
name: pihole-blocklist
description: Evaluate, categorize, and document new Pi-hole blocklist sources for the curated blocklist repository. Always trigger immediately when the user asks about adding, evaluating, or researching a new Pi-hole blocklist source, or uses phrases like "should I add this list", "evaluate this blocklist", "add to pihole", "new blocklist", "is this a good list", or pastes a raw blocklist URL. Also trigger when the user wants to review existing sources, update the repo README, check for list overlap, or document a new category. Pre-loaded with the full category taxonomy and evaluation criteria so every new addition is consistent with the existing curation standard.
---

# Pi-hole Blocklist Skill

Evaluate new blocklist sources, assign them to the correct category, check for quality and overlap, and produce ready-to-commit documentation for the curated blocklist repository at `github.com/mickpletcher/PiHole`.

---

## Repository Context

**Repo**: `github.com/mickpletcher/PiHole`  
**Current sources**: 57 curated blocklist URLs  
**Maintenance cadence**: Regular scheduled updates  
**Format**: Mixed (hosts file format and plain domain lists)  
**Pi-hole instance**: CT 101 at 192.168.0.101 (local reference only — do not publish this)

---

## Category Taxonomy

Every blocklist source belongs to exactly one primary category. Use this taxonomy consistently.

| Category | What It Covers |
|---|---|
| **Advertising** | Ad servers, ad networks, pop-up ad domains |
| **Tracking** | Telemetry, fingerprinting, analytics, CNAME cloaking |
| **Malicious** | Malware, ransomware, phishing, scam domains |
| **Suspicious** | Spam, referrer spam, high-risk domains |
| **Fake DNS / DynDNS** | Fake DNS providers, dynamic DNS abusers |
| **Piracy** | Anti-piracy DNS blocklists |
| **Fake News** | Known fake news domains |
| **Stalkerware** | Stalkerware and spyware indicator domains |
| **Device Trackers** | Platform-native trackers (Amazon, Apple, TikTok, Samsung, LG, Windows/Office) |
| **Smart TV / IoT** | Broad smart TV and IoT telemetry across all brands |
| **URL Shorteners** | URL shortener services used to obscure malicious links |
| **Encrypted DNS / VPN Bypass** | Domains used to circumvent DNS filtering |
| **OISD** | Comprehensive all-in-one lists covering ads, tracking, and malware |
| **Whitelist** | Approved domains excluded from blocking |

---

## Evaluation Criteria

When asked to evaluate a new source, assess all of the following:

### 1. Source Quality
- Is the list actively maintained? Check last commit date or update timestamp.
- Does it have a clear maintainer (GitHub repo, named project, organization)?
- Is there a stated methodology for what gets added and removed?
- Does it have community trust signals (stars, forks, citations in other blocklist projects)?

### 2. Category Fit
- Which category from the taxonomy does it best fit?
- Does it duplicate coverage already provided by an existing source in that category?
- Does it add meaningfully new domains not covered by existing sources?

### 3. Format Compatibility
- Is the URL a direct raw link to the list (not an HTML page)?
- Is it in a Pi-hole-compatible format: hosts file (`0.0.0.0 domain.com`) or plain domain list (one per line)?
- Is it stable — does the URL change between updates, or is it a permanent raw URL?

### 4. Risk Assessment
- Could any domains on the list cause false positives for common services?
- Is the list known to be aggressive (high false positive rate) or conservative?
- Has the list been flagged in the Pi-hole community for issues?

### 5. Recommendation
- **Add**: Meets quality bar, fills a gap, compatible format, stable URL
- **Add with caution**: Useful but aggressive — note false positive risk in documentation
- **Skip**: Redundant, unmaintained, incompatible format, or unclear provenance
- **Whitelist candidate**: Source contains domains that should be whitelisted rather than blocked

---

## What Claude Should Produce

### For a new source evaluation:

```
SOURCE: [Name]
URL: [raw URL]
CATEGORY: [from taxonomy]
MAINTAINER: [GitHub user / org / project name]
LAST UPDATED: [date or "active" if recent commits]
DOMAIN COUNT: [approximate if known]
FORMAT: [hosts / plain domain list / mixed]
OVERLAP RISK: [low / medium / high — with which existing category]
FALSE POSITIVE RISK: [low / medium / high — brief reason]
RECOMMENDATION: [Add / Add with caution / Skip / Whitelist candidate]
NOTES: [Any caveats, known issues, or context]
```

### For a README table entry (when adding a new source):

```markdown
| [Source Name] | [URL] |
```

Formatted to match the existing table style in the repo README.

### For a batch evaluation (multiple URLs at once):

Produce one evaluation block per source, then a summary table at the end showing recommended adds vs. skips.

---

## How to Add a New Source to Pi-hole

1. Log into the Pi-hole admin panel
2. Navigate to **Group Management → Adlists**
3. Paste the raw URL into the **Address** field
4. Add a comment matching the source name from the repo
5. Click **Add**
6. Go to **Tools → Update Gravity** and click **Update**

---

## Reference Files

- `pihole-blocklist-sources.md` — local index of the current curated sources organized by category
