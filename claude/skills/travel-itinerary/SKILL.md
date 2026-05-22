---
name: travel-itinerary
description: Plan, format, and export travel itineraries as Obsidian-formatted Markdown files. Always trigger immediately when the user's message starts with "trip" or "itinerary". Also trigger when the user says "plan my trip", "build my itinerary", "travel plan", "export my trip", "format this itinerary", or describes an upcoming trip and asks Claude to organize it. Produces a day-by-day breakdown, logistics summary, packing list, and budget tracker in a single Obsidian-ready .md file.
version: 1.1.0
---

# Travel Itinerary Skill

## Intent

Build practical travel itineraries with route notes, lodging context, pacing, budget visibility, and export-ready structure.

## Do Not Use When

- Do not use for broad destination comparison, live booking, visa/legal advice, or unsafe assumptions about current availability.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

## Validation Checklist

- [ ] The output matches the skill's intended task and platform.
- [ ] Required inputs, assumptions, and uncertainty are explicit.
- [ ] Safety, scope, and source limits are respected.
- [ ] The response follows the requested format or the skill's default output format.
- [ ] The result is practical enough to use without another cleanup pass.

Build Obsidian-formatted trip files from user supplied details. This skill is a reusable template for organizing travel plans into a clean Markdown itinerary.

## Primary Triggers

**`trip`** or **`itinerary`** — Execute immediately. No clarifying questions before producing the first draft.

Other triggers: "plan my trip", "build my itinerary", "travel plan for...", "export this trip", "format my itinerary"

Infer the best trip template before drafting:

- `city trip`
- `road trip`
- `active travel`
- `mixed work and leisure`

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
- **Trip template fit** — city trip, road trip, active travel, or mixed work and leisure

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
**Template:** [City Trip / Road Trip / Active Travel / Mixed Work + Leisure]

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
**Route Notes:** [Station to hotel, airport transfer, parking note, walk time, or local transit note]
**Activities:**
- [Activity 1]
- [Activity 2]
**Meals:** [Notable spots or budget estimate]
**Budget Snapshot:** Lodging $X | Food $X | Transit $X | Activities $X
**Notes:** [Anything logistical — jet lag buffer, early check-in, etc.]
**Contingency:** [Weather fallback, delay backup, lower-energy option, or TBD]

### Day 2 — [Date] — [City]
...

[Repeat for each day. Group consecutive days in the same city if itinerary is fluid.]

---

## Accommodation Summary

| City | Property | Type | Nights | Est. Cost | Booked? |
|---|---|---|---|---|---|
| [City] | [Name or TBD] | [Type] | X | $XXX | Yes / No |

---

## Reservation Summary

| Item | Status | Date | Confirmation | Notes |
|---|---|---|---|---|
| [Flight / Train / Hotel / Event] | Booked / TBD | [Date] | [Code or TBD] | [Key note] |

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

### Daily Budget View

| Day | Lodging | Food | Transit | Activities | Total |
|---|---|---|---|---|---|
| Day 1 | $X | $X | $X | $X | $X |
| Day 2 | $X | $X | $X | $X | $X |

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

## Packing Summary

- Essential documents ready: [Yes / No / TBD]
- Trip specific gear: [short rollup]
- Weather dependent items: [short rollup]
- Work items if needed: [short rollup]

---

## Key Contacts & Info

| Item | Detail |
|---|---|
| Travel Insurance | [Provider / Policy # / Emergency line] |
| Departure Point | [Airport / City / Region] |
| Emergency Contact | [TBD] |
| Embassy (per country) | [Link or TBD] |

---

## Map And Route Notes

- [Arrival route note]
- [Transfer note between stops]
- [Parking, station, or ferry detail]
- [Walking or local transit shortcut]

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

### Template Guidance

Adjust emphasis by template:

- `city trip`: denser day plans, neighborhood flow, museum or restaurant timing, transit realism
- `road trip`: driving blocks, parking, fuel or charging notes, check-in timing, scenic or backup stop logic
- `active travel`: training or event anchors, recovery windows, gear, nutrition, and weather contingency emphasis
- `mixed work and leisure`: protected work blocks, quieter lodging needs, Wi-Fi or workspace notes, lighter sightseeing pacing on work days

### Step 3 — Validate Before Exporting

Before writing the file, check for:

- **Date math** — day count, transit days, anchor event alignment
- **Logic gaps** — overnight transit without accommodation, missing arrival day
- **Budget realism** — flag if estimated total is significantly over or under the stated target
- **Accommodation alignment** — keep lodging recommendations consistent with the user's stated preference
- **Routing assumptions** — note when a connection or transfer is likely required
- **Daily structure realism** — do not overload a day beyond likely transit, meal, and pacing limits
- **Meal spacing** — note when long activity or transit blocks should have a real meal or snack plan
- **Contingency coverage** — add backup notes for weather, delays, or a failed booking dependency when relevant

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
- **Packing and reservation rollups should stay concise.** They are quick-reference sections, not duplicates of the full itinerary.
- **Anchor events are fixed.** Build the day-by-day around confirmed event dates — never shift them to fit travel convenience.
- **Obsidian tables must render cleanly.** Use pipe-formatted markdown tables throughout. All tables must be Dataview-compatible.
- **No fluff.** This is a logistics document. No preamble, no sign-offs, no "have a great trip!" copy.

---

## Template Guidance

- Use placeholders when essential trip details are missing
- Preserve user supplied naming, destination order, and travel style
- Keep the output neutral and reusable so it works for solo, couple, family, or group travel

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- Trip dates, destinations, and the rough plan you want turned into an itinerary.

Example prompts:

- `Use travel-itinerary to turn this rough trip plan into a day by day itinerary.`
- `Build me a realistic itinerary for Spain and Portugal with train transfers and daily pacing.`
- `Show me an example prompt for asking this skill to format and tighten an itinerary.`

