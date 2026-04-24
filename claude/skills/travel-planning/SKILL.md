---
name: travel-planning
description: Plan trips, build itineraries, research destinations, estimate budgets, and organize logistics for Mick's travel. Always trigger immediately when the user mentions planning a trip, asks about flights, hotels, itineraries, destinations, or uses phrases like "trip to", "travel to", "planning a visit", "what should I do in", "how do I get to", "how much will this cost", or references any upcoming travel. Also trigger when the user mentions specific destinations, asks about visa requirements, crossing borders, ferry routes, or comparing travel options. This skill encodes Mick's full travel preferences and constraints so outputs are personalized from the first message — never produce generic travel advice.
---

# Travel Planning Skill

Produces personalized, opinionated travel plans for Mick Pletcher. Every output should reflect his specific constraints and preferences — never produce generic tourist recommendations.

---

## Who This Is For

**Mick Pletcher** — Automation Engineer, endurance athlete, and adventure traveler based in Nashville, TN. Visited 33+ countries, targeting 50. Summited Kilimanjaro. Background in competitive cycling and triathlon. Pursues geographic arbitrage and early retirement.

**Travel style: Solo by default.** All itineraries, budgets, and logistics are planned for one person unless Mick explicitly states otherwise. Do not suggest group tours, couples packages, or shared activities framed for multiple people. When Mick mentions a travel companion for a specific trip, note it and adjust accordingly but do not assume it carries over to other trips.

---

## Hard Constraints (Never Violate)

| Constraint | Rule |
|---|---|
| Accommodation | **Private rooms only** — no dorms, no shared baths |
| Home Airport | **BNA (Nashville)** — all flights route through BNA unless Mick specifies otherwise |
| Budget mindset | Value-optimized, not budget-backpacker and not luxury — target the best experience per dollar |
| Activities | Anchor the trip around an **endurance or adventure activity** when one is available (cycling, hiking, running events, climbing, skydiving, etc.) |
| Geographic arbitrage | Flag when a destination offers strong USD value — eating, accommodation, transport costs |

---

## Travel Preferences

**Accommodation style**: Boutique hotels, guesthouses, locally-owned properties. Avoid large chain hotels unless price/location is overwhelming.

**Pace**: Active and structured, not leisurely. Mick covers a lot of ground. Plan for full days.

**Food**: Street food and local spots over tourist restaurants. No dietary restrictions.

**Transport**: Train or ferry over flying when it's feasible and interesting. Renting a car is fine for rural/off-grid destinations.

**Experiences over things**: Prioritize events, physical challenges, cultural immersion over museums and shopping.

**Social media documentation**: Mick documents trips publicly on Facebook and X — good photo/video opportunities matter.

---

## What Claude Should Do When This Skill Triggers

### 1. Identify the trip type

Determine whether this is:
- **Event-anchored** (Tour de France, Running of the Bulls, a race, a summit attempt) — build the itinerary around the event dates, work outward
- **Destination-driven** (exploring a country or region) — anchor around an endurance activity if one fits
- **Logistics query** (flights, visas, border crossings, ferries) — answer precisely and completely

### 2. Build the itinerary structure

For multi-city trips, produce a day-by-day breakdown:
- City/location per day
- Accommodation type and price range (in USD)
- Key activities (endurance anchor highlighted)
- Meals worth noting
- Transport between cities with method, duration, and cost
- Any booking lead time warnings (events, permits, popular routes)

### 3. Budget estimate

Always produce a trip total with a per-day breakdown:
- Flights (BNA routing, round trip)
- Accommodation (nightly rate × nights)
- Food (realistic daily spend for the destination)
- Transport (intercity + local)
- Activities and entrance fees
- Buffer (10%)

Flag when a destination has strong USD purchasing power.

### 4. Logistics flags

Proactively surface:
- Visa requirements for US passport holders
- Booking windows (what needs to be reserved months ahead)
- Peak season/crowd warnings
- Ferry or border crossing logistics
- Phone/SIM recommendations
- Currency situation

---

## Active Trip Context

When Mick mentions a specific upcoming trip, load the relevant reference file if one exists. For trips without a reference file, research inline and apply all hard constraints and preferences.

Current reference files:
- `references/europe-2026.md` — Summer 2026 Spain / Morocco / Portugal trip
- `references/colorado-2026.md` — Summer 2026 Colorado 14ers + Theodore Roosevelt NP

For any new destination not covered by a reference file, proceed using the hard constraints and preferences defined above. Do not treat this skill as limited to documented trips.

---

## Output Format

### For full itinerary requests:
```
TRIP: [Name / Dates]
TOTAL BUDGET ESTIMATE: $X,XXX

DAY-BY-DAY:
Day 1 – [City]: ...
Day 2 – [City]: ...

BUDGET BREAKDOWN:
- Flights (BNA → X → BNA): $
- Accommodation (X nights): $
- Food (avg $/day × days): $
- Transport: $
- Activities: $
- Buffer (10%): $
TOTAL: $

LOGISTICS FLAGS:
- [Visa / booking windows / warnings]
```

### For single-destination or activity queries:
Answer directly and concisely. No need for full itinerary format unless asked.

### For budget comparisons:
Side-by-side table with per-day costs and totals.

---

## Reference Files

- `references/europe-2026.md` — Detailed research notes for the Spain/Morocco/Portugal summer trip
- `references/colorado-2026.md` — Summit profiles, trailhead logistics, permit info

Load the relevant reference file when working on a specific trip. For new destinations not covered, research inline.
