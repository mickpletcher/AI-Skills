---
name: travel-itinerary
description: Plan, format, and export travel itineraries as Obsidian-formatted Markdown files. Always trigger immediately when the user's message starts with "trip" or "itinerary". Also trigger when the user says "plan my trip", "build my itinerary", "travel plan", "export my trip", "format this itinerary", or describes an upcoming trip and asks Claude to organize it. Produces a day-by-day breakdown, logistics summary, packing list, and budget tracker in a single Obsidian-ready .md file.
---

# Travel Itinerary Skill

Build Obsidian-formatted trip files from user supplied details. This skill is a reusable template for organizing travel plans into a clean Markdown itinerary.

## Primary Triggers

**`trip`** or **`itinerary`** — Execute immediately. No clarifying questions before producing the first draft.

Other triggers: "plan my trip", "build my itinerary", "travel plan for...", "export this trip", "format my itinerary"

---

## Step-by-Step Workflow

### Step 1 — Extract Trip Data

Pull everything available from the conversation. Do not ask clarifying questions if enough info exists to produce a useful draft. Extract:

- **Destination(s)** and order of travel
- **Dates** — departure, return, any fixed anchor events
- **Anchor events** — concerts, races, festivals, sporting events with fixed dates (e.g., Tour de France Grand Départ, Running of the Bulls)
- **Accommodation type** — hotel, hostel private room, Airbnb, resort, camping, or user specified preference
- **Departure airport or origin** — if provided
- **Transport** — flights, trains, ferries, buses
- **Budget target** — total or daily
- **Known activities** or goals per destination
- **Trip purpose** — adventure, event-based, exploration, endurance event, etc.

If key data is missing (e.g., no dates at all), produce the best possible draft with placeholders and flag gaps at the bottom.

### Step 2 — Build the Markdown File

**Filename:** `YYYY-MM-DD_[Destination].md` using the departure date.
Example: `2026-07-01_Spain-Morocco.md`

Use this template structure, omitting any section with no data:

```markdown
# [Trip Name]
**Dates:** [Departure] — [Return] ([X] days)
**Destinations:** [City 1 → City 2 → City 3]
**Budget Target:** $X,XXX total / ~$XXX/day
**Departure Point:** [Airport / City / Region]
**Purpose:** [One-line description]

---

## Logistics Overview

| Leg | Mode | Route | Date | Confirmation |
|---|---|---|---|---|
| [Origin] → [City] | Flight | [Route] | [Date] | [Code or TBD] |
| [City] → [City] | Train/Ferry/Bus | [Route] | [Date] | TBD |

---

## Anchor Events

| Event | Location | Dates | Status |
|---|---|---|---|
| [Event Name] | [City] | [Dates] | Confirmed / TBD |

---

## Day-by-Day

### Day 1 — [Date] — [City]
**Accommodation:** [Name or TBD] — [Type] — ~$XX/night
**Travel:** [Arrival details or transit]
**Activities:**
- [Activity 1]
- [Activity 2]
**Meals:** [Notable spots or budget estimate]
**Notes:** [Anything logistical — jet lag buffer, early check-in, etc.]

### Day 2 — [Date] — [City]
...

[Repeat for each day. Group consecutive days in the same city if itinerary is fluid.]

---

## Accommodation Summary

| City | Property | Type | Nights | Est. Cost | Booked? |
|---|---|---|---|---|---|
| [City] | [Name or TBD] | [Type] | X | $XXX | Yes / No |

---

## Budget Tracker

| Category | Estimated | Actual | Notes |
|---|---|---|---|
| Flights | $XXX | — | [Details] |
| Accommodation | $XXX | — | X nights avg $XX/night |
| Ground Transport | $XXX | — | Trains, buses, ferries |
| Food | $XXX | — | ~$XX/day |
| Activities & Entrance Fees | $XXX | — | [Key items] |
| Misc / Buffer | $XXX | — | Visas, SIM, incidentals |
| **TOTAL** | **$X,XXX** | **—** | |

---

## Packing List

Tailor to destination type (urban, trekking, beach, mixed). Always include the travel essentials below, then add trip-specific items.

### Always
- [ ] Passport (valid 6+ months past return)
- [ ] Travel insurance confirmation
- [ ] Downloaded offline maps (Maps.me or Google Maps)
- [ ] Local currency or notify bank
- [ ] International SIM or eSIM (check coverage for each country)
- [ ] Backup card in separate location from wallet
- [ ] Phone charger + universal adapter
- [ ] Portable battery pack
- [ ] AirTag or luggage tracker

### Clothing (carry-on optimized)
- [ ] [X] quick-dry shirts
- [ ] [X] pants/shorts
- [ ] [X] pairs socks/underwear
- [ ] Light layer / packable jacket
- [ ] Comfortable walking shoes
- [ ] [Trip-specific: hiking boots, dress shoes, etc.]

### Health & Safety
- [ ] Prescription medications (extra supply)
- [ ] OTC pain reliever, stomach meds, antihistamine
- [ ] Sunscreen
- [ ] Hand sanitizer
- [ ] [Trip-specific: altitude meds, malaria prophylaxis, etc.]

### Tech
- [ ] Camera or phone kit
- [ ] Extra batteries + charger
- [ ] SD cards
- [ ] Laptop if needed
- [ ] Headphones

### Documents (physical + digital copies)
- [ ] Passport
- [ ] Travel insurance policy + emergency number
- [ ] Accommodation confirmations
- [ ] Flight/transport confirmations
- [ ] Emergency contacts

---

## Key Contacts & Info

| Item | Detail |
|---|---|
| Travel Insurance | [Provider / Policy # / Emergency line] |
| Departure Point | [Airport / City / Region] |
| Emergency Contact | [TBD] |
| Embassy (per country) | [Link or TBD] |

---

## Open Items / To-Do

- [ ] [Book flight or transport from origin to first destination]
- [ ] [Book accommodation in X for nights Y-Z]
- [ ] [Purchase travel insurance]
- [ ] [Apply for visa if required]
- [ ] [Exchange currency or set up travel card]
- [ ] [Other flagged gaps from the data]

---

*Exported [YYYY-MM-DD] | Last updated [YYYY-MM-DD]*
```

### Step 3 — Validate Before Exporting

Before writing the file, check for:

- **Date math** — day count, transit days, anchor event alignment
- **Logic gaps** — overnight transit without accommodation, missing arrival day
- **Budget realism** — flag if estimated total is significantly over or under the stated target
- **Accommodation alignment** — keep lodging recommendations consistent with the user's stated preference
- **Routing assumptions** — note when a connection or transfer is likely required

Flag issues in the Open Items section, not inline in the itinerary.

### Step 4 — Output expectations

Produce the itinerary content directly unless the user explicitly asks for a file to be created in a local repo or folder.

When you finish, confirm:

1. the filename you would use
2. the date range covered
3. any flagged gaps or open items

---

## Rules

- **No fabricated bookings.** If it's not confirmed, mark it TBD.
- **Budget columns stay separate.** Estimated vs. Actual — never merge them. Actual fills in as the itinerary is updated.
- **Packing list is trip-specific.** Add or remove items based on destination, climate, and activities.
- **Anchor events are fixed.** Build the day-by-day around confirmed event dates — never shift them to fit travel convenience.
- **Obsidian tables must render cleanly.** Use pipe-formatted markdown tables throughout. All tables must be Dataview-compatible.
- **No fluff.** This is a logistics document. No preamble, no sign-offs, no "have a great trip!" copy.

---

## Template Guidance

- Use placeholders when essential trip details are missing
- Preserve user supplied naming, destination order, and travel style
- Keep the output neutral and reusable so it works for solo, couple, family, or group travel
