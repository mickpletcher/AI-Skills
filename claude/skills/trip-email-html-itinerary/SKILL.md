---
name: trip-email-html-itinerary
description: >
  Extract trip logistics from pasted travel emails, booking confirmations,
  forwarded messages, reservation notes, or raw itinerary text and generate one
  polished, self-contained offline HTML itinerary file for sharing with family
  or other travelers. Trigger when the user asks to turn trip emails into an
  HTML itinerary, travel handoff page, shareable trip page, family trip summary,
  booking-reference page, or offline travel document.
version: 2.0.0
---

# Trip Email HTML Itinerary

## Intent

Turn a batch of travel-related emails into a complete, shareable HTML trip document. The final file should help the traveler and a spouse, family member, or travel companion quickly understand flights, lodging, rental cars, events, booking references, contact details, open issues, and day-by-day logistics.

Use this skill for email-derived travel organization and offline HTML output. If the user wants a planning Markdown file instead, use the travel-itinerary skill.

## Trigger When

- The user asks to create an HTML itinerary from emails, confirmations, or forwarded trip details.
- The user asks for a shareable trip page, family travel handoff, offline travel document, or complete travel summary from bookings.
- The input includes travel emails for flights, hotels, car rentals, tours, events, restaurants, insurance, visas, or logistics.
- The user wants a single `.html` file that works locally without a server or internet access.

## Do Not Use When

- The user wants live booking, price comparison, destination research, or current visa/legal advice.
- The user only wants a plain text summary or Obsidian Markdown itinerary.
- The user asks to preserve confidential PINs, full payment card numbers, passwords, account login links, or private access codes in the output.

---

## Workflow

### 1. Ingest The Emails

Accept pasted emails, exported email text, copied booking confirmations, screenshots transcribed by the user, or structured trip notes. If the user provides multiple emails, treat the newest or most explicit confirmation as authoritative unless it is clearly a cancellation or change notice.

Extract and normalize:

- trip title, date range, traveler names, route stops, destination cities
- flights: airline, flight number, airports, dates, departure and arrival times, confirmation codes, ticketing notes, baggage notes, terminal notes, cancellation/change status
- lodging: property name, city, dates, address, phone, email, booking number, room type, check-in/out windows, parking, meals, arrival instructions, cancellation status
- ground transport: rental car, train, ferry, bus, shuttle, ride reservation, pickup/drop-off locations and times, reservation numbers
- events and tours: names, dates, times, meeting points, ticket references, warnings, and schedule-sensitive notes
- travel admin: passport, visa, Global Entry/TSA PreCheck, insurance, pending bookings, canceled items, documents to carry
- open questions, gaps, conflicts, or items still needing user action

### 2. Reconcile And Protect The Data

- Prefer confirmed bookings over draft plans.
- Treat cancellation emails as warnings and mark related items canceled unless a later email re-confirms them.
- Preserve confirmation and booking numbers when useful.
- Never include Booking.com PINs, door/keypad/access codes, passwords, full payment card details, CVV codes, bank details, or sensitive login URLs.
- Redact sensitive values as `[redacted]` when the surrounding context is still useful.
- If dates or times conflict, include the most likely value in the main itinerary and add a short conflict note in pending items.
- Do not invent addresses, phone numbers, confirmation codes, or exact times. Use `TBD` or `Pending` when unknown.

### 3. Build A Working Trip Model

Use this internal shape while drafting. It does not have to be shown to the user:

```json
{
  "tripTitle": "",
  "dateRange": "",
  "travelerNames": [],
  "routeStops": [{"code": "", "city": ""}],
  "statusPills": [],
  "keyTripCards": [],
  "contacts": [],
  "flights": [],
  "lodging": [],
  "groundTransport": [],
  "events": [],
  "dayByDay": [],
  "bookingReferences": [],
  "travelAdmin": [],
  "pendingItems": [],
  "canceledItems": []
}
```

### 4. Required HTML Sections

Produce a complete HTML document with these sections in order, omitting only sections with no useful data:

1. **Hero** — trip title, date range, route string (BNA → LIS → BCN → ...), status badge pills, destination character gradient
2. **Destination Timeline** — one card per major stop (equivalent to "island cards" in multi-stop trips)
3. **Action Items** — red/gold alert strips for anything requiring user action before departure
4. **Flights** — confirmed segments in green-badged panels; unbooked/verify segments in red/yellow panels
5. **Destination Sections** — one per city/region with hotel card, transport card, activity card, and alert strips
6. **Day-by-Day Itinerary** — date-keyed rows with country tags and activity lists
7. **Booking References** — full table with What / Details / Reference / Status columns
8. **Booking Checklist** — card grid organized by category (Flights, Hotels, Transport, Tours, Admin, Finance)
9. **Travel Admin** — 2-column card grid for passport/visa, ID rules, baggage, emergency contacts
10. **Footer** — trip name · traveler · dates · route

---

## Design System

This is the canonical visual spec. All HTML output from this skill must use it. It is derived from the Hawaii Trip (Oct 2026) and Europe & Morocco Trip (Jul 2026) itinerary files produced for Mick Pletcher.

### Font Stack

```html
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&family=DM+Mono:ital,wght@0,400;0,500&family=Playfair+Display:ital,wght@0,700;1,700&display=swap" rel="stylesheet">
```

- **Playfair Display 700** — hero title, destination section headers, card names
- **DM Sans 300/400/500** — body text, card subtitles, list items
- **DM Mono 400/500** — all labels, badges, codes, timestamps, section labels, footer

Note: These fonts require an internet connection on first load. The file works offline once fonts are cached. If strict offline is required, fall back to `Georgia, 'Times New Roman', serif` for display and `'Courier New', monospace` for mono.

### CSS Variables

Always declare exactly these variables in `:root`. Swap the destination-palette values per trip; never change the structural variable names.

```css
:root {
  /* ── DESTINATION PALETTE (swap per trip) ── */
  --c1:          #0a4f6e;   /* primary — deep tone of main destination */
  --c1-mid:      #1a8fa0;   /* primary mid — lighter accent */
  --c2:          #e8603c;   /* secondary — alert / contrast destination */
  --c3:          #2d6a4f;   /* tertiary — third destination or activity accent */
  --gold:        #d4a843;   /* universal gold — labels, prices, accents */
  --em-color:    #c8eaf5;   /* italic emphasis in hero h1 */

  /* ── STRUCTURAL (never change) ── */
  --white:        #fdfaf6;
  --dark:         #0c1820;
  --dark2:        #111e28;
  --mid:          #3a5060;
  --green-ok:     #4caf50;
  --green-ok-dim: rgba(76,175,80,0.15);
  --coral:        #e8603c;
  --purple:       #7c5cbf;
  --purple-dim:   rgba(124,92,191,0.12);
}
```

### Destination Palette Reference

Pick the closest match and tune hues to suit:

| Trip character | --c1 (deep) | --c1-mid | --c2 (alert/contrast) | --c3 | --em-color |
|---|---|---|---|---|---|
| Pacific / Hawaii | #0a4f6e | #1a8fa0 | #e8603c | #2d6a4f | #c8eaf5 |
| Mediterranean / Atlantic | #0a3f6e | #1a7a9e | #e8603c | #4a7a38 | #a8d4f0 |
| Morocco / Desert | #6a2a08 | #b04820 | #e8603c | #0a3f6e | #f0a858 |
| Japan / East Asia | #1a2a5e | #2a5a9e | #c8302a | #2d6a4f | #c8d8f5 |
| Scandinavia / Arctic | #0a2a4e | #1a5a8e | #c85030 | #2a4a3a | #a8c8e8 |
| Central America / Tropics | #1a5a2a | #2a9a4a | #e8803c | #0a3f6e | #a8e8b8 |

### Hero Section

```html
<div class="hero">
  <div class="hero-stars"></div>
  <div class="hero-inner">
    <div class="hero-tag">Trip Planning Document &nbsp;·&nbsp; [N] Days · [N] Countries</div>
    <h1>[Destination] &amp; <em>[Secondary]</em><br>[Month Year]</h1>
    <div class="hero-sub">BNA → [CODE] → [CODE] → BNA &nbsp;·&nbsp; [Date range]</div>
    <div class="hero-badges">
      <!-- green dot badge for confirmed flights -->
      <div class="hero-badge"><div class="dot-green"></div> [Airline] <span class="val">[Conf]</span> &nbsp;·&nbsp; Confirmed</div>
      <!-- plain badge for counts -->
      <div class="hero-badge">Hotels <span class="val">[N] of [N]</span> confirmed</div>
      <!-- warn badge for action items -->
      <div class="hero-badge warn-badge"><div class="dot-red"></div> <span class="val">[N] Action Items</span> &nbsp;·&nbsp; required</div>
    </div>
  </div>
  <div class="hero-wave"></div>
</div>
```

Hero gradient: `linear-gradient(155deg, [darkest] 0%, [c1-dark] 28%, [c1-mid-dark] 52%, [c2-dark] 76%, [darkest-c2] 100%)`
Hero `::before` radial overlays: 3 ellipses — primary destination glow at 70% 20%, secondary glow at 15% 85%, gold accent at 50% 60%.

### Destination Timeline Cards

One card per major stop. Status dots: `done` = green (confirmed), `todo` = red (action needed), `sel` = gold (partial/selected).

Card gradient backgrounds follow destination palette:
- Confirmed stop: `linear-gradient(140deg, [c1-dark], [c1-mid])`
- Alert/gap stop: dashed border, warm dark gradient, `border-style: dashed`
- Dim/transit stop: dark muted gradient, `opacity: 0.7`

```html
<div class="dest-card [class]">
  <div class="status-dot [done|todo|sel]"></div>
  <div class="dest-name">[City]</div>
  <div class="dest-country">[Country]</div>
  <div class="dest-dates">[Jul 4–7]</div>
  <div class="dest-nights"><strong>[N]</strong>nights</div>
  <div class="dest-hotel [warn?]">[Hotel name or warning]</div>
</div>
```

### Alert Strip System

Four severity levels. Always use `.icon` + `.txt` structure. Strong tags inside `.txt` inherit the strip color.

```html
<div class="alert-strip red">    <!-- critical: missing booking, canceled hotel, gap -->
<div class="alert-strip gold">   <!-- important: pending payment, verify times, book soon -->
<div class="alert-strip green">  <!-- confirmed: logistics summary, cost estimates -->
<div class="alert-strip purple"> <!-- tip/highlight: dining, activity notes, TDF, events -->
```

### Flights Panel

Group into labeled panels: OUTBOUND — CONFIRMED, MID-TRIP SEGMENTS — VERIFY/BOOK, RETURN — CONFIRMED.

Badges: `.badge-confirmed` (green), `.badge-book` (red), `.badge-verify` (yellow).

```html
<div class="flights-panel">
  <div style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:2px;color:rgba(255,255,255,0.3);margin-bottom:14px">OUTBOUND — CONFIRMED · [Airline] · Conf: [CODE]</div>
  <div class="flight-row">
    <div class="flight-dir">OUTBOUND</div>
    <div class="flight-route">
      <span class="airport">BNA</span><span class="flight-arrow">→</span><span class="airport">HNL</span>
      <span class="flight-via">[Airline + flight] · Economy · Nonstop</span>
    </div>
    <div class="flight-time">[Date]<br>[Time → Time]</div>
    <span class="badge-confirmed">CONFIRMED</span>
  </div>
</div>
```

### Day-by-Day Grid

Country tags color-coded per destination. Anchor items (flights, check-ins, tours) use `.anchor` class for white bold text. Optional activities use `.opt` (dimmed italic). Warnings use `.flag` (coral). Notes use `.note` (gold). Tour/event highlights use `.tour` or `.tdf` (amber/purple).

```html
<div class="day-row">
  <div class="day-label"><strong>Jul 4</strong>SAT</div>
  <div class="day-content [alert-day?]">
    <span class="day-country-tag [portugal|spain|morocco|transit|gap]">[LABEL]</span>
    <ul class="day-activities">
      <li class="anchor">[Flight / check-in / tour time — bold white]</li>
      <li>[Regular activity]</li>
      <li class="flag">⚠ [Warning or action needed]</li>
      <li class="opt">[Optional suggestion]</li>
    </ul>
  </div>
</div>
```

Use `.alert-day` on `.day-content` for days with a lodging gap or critical issue (adds coral border tint).

### Booking References Table

Four columns: What (with sub-label), Details, Reference (DM Mono gold), Status badge.

Status classes: `.status-confirmed` (green), `.status-verify` (yellow), `.status-needed` (coral). Canceled rows use `.canceled-row` class on `<tr>` for reduced opacity and `.ref-canceled` on the name for strikethrough.

### Checklist Grid

3-column grid of `.check-card` elements. Item states:
- `(default)` — open circle, coral — not yet done
- `.done` — filled green circle, strikethrough — complete
- `.sel` — gold diamond — selected/partial
- `.canceled` — ✕ coral — canceled

Suggested card categories: ✈️ Flights, 🏨 Accommodations, 🚗 Transport, 🏕 Tours & Dining, 📋 Admin, 💰 Finance & Gear.

### Complete CSS Block

Paste this verbatim into every generated file. Swap destination palette variables only.

```css
:root {
  --c1: #0a4f6e; --c1-mid: #1a8fa0; --c2: #e8603c; --c3: #2d6a4f;
  --gold: #d4a843; --em-color: #c8eaf5;
  --white: #fdfaf6; --dark: #0c1820; --dark2: #111e28; --mid: #3a5060;
  --green-ok: #4caf50; --green-ok-dim: rgba(76,175,80,0.15);
  --coral: #e8603c; --purple: #7c5cbf; --purple-dim: rgba(124,92,191,0.12);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--dark); color: var(--white); font-family: 'DM Sans', sans-serif; font-weight: 300; min-height: 100vh; overflow-x: hidden; }
.hero { position: relative; background: linear-gradient(155deg, #061218 0%, #08364f 35%, #0e6a82 60%, #1a8a60 85%, #1d6e44 100%); padding: 64px 40px 72px; overflow: hidden; }
.hero::before { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at 75% 20%, rgba(26,143,160,0.35) 0%, transparent 55%), radial-gradient(ellipse at 15% 85%, rgba(212,168,67,0.18) 0%, transparent 50%), radial-gradient(ellipse at 50% 60%, rgba(45,106,79,0.25) 0%, transparent 60%); }
.hero-stars { position: absolute; inset: 0; background-image: radial-gradient(1px 1px at 15% 20%, rgba(255,255,255,0.6) 0%, transparent 100%), radial-gradient(1px 1px at 30% 8%, rgba(255,255,255,0.4) 0%, transparent 100%), radial-gradient(1.5px 1.5px at 65% 15%, rgba(255,255,255,0.7) 0%, transparent 100%), radial-gradient(1px 1px at 80% 30%, rgba(255,255,255,0.3) 0%, transparent 100%), radial-gradient(1px 1px at 45% 5%, rgba(255,255,255,0.5) 0%, transparent 100%); }
.hero-wave { position: absolute; bottom: -2px; left: 0; right: 0; height: 64px; background: var(--dark); clip-path: ellipse(55% 100% at 50% 100%); }
.hero-inner { position: relative; max-width: 960px; margin: 0 auto; }
.hero-tag { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 3.5px; color: var(--gold); text-transform: uppercase; margin-bottom: 18px; opacity: 0.9; }
.hero h1 { font-family: 'Playfair Display', serif; font-size: clamp(42px, 7.5vw, 76px); font-weight: 700; line-height: 1.0; color: var(--white); margin-bottom: 6px; }
.hero h1 em { font-style: italic; color: var(--em-color); }
.hero-sub { font-family: 'DM Mono', monospace; font-size: 12px; color: rgba(255,255,255,0.5); letter-spacing: 1.5px; margin-top: 14px; }
.hero-badges { display: flex; gap: 10px; margin-top: 20px; flex-wrap: wrap; }
.hero-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.14); border-radius: 6px; padding: 7px 14px; font-family: 'DM Mono', monospace; font-size: 10px; color: rgba(255,255,255,0.55); letter-spacing: 1px; }
.hero-badge .val { color: var(--gold); }
.hero-badge.warn-badge { border-color: rgba(232,96,60,0.38); background: rgba(232,96,60,0.1); }
.hero-badge.warn-badge .val { color: var(--coral); }
.hero-badge .dot-green { width: 6px; height: 6px; border-radius: 50%; background: var(--green-ok); box-shadow: 0 0 5px var(--green-ok); flex-shrink: 0; }
.hero-badge .dot-red { width: 6px; height: 6px; border-radius: 50%; background: var(--coral); box-shadow: 0 0 5px var(--coral); flex-shrink: 0; }
.main { max-width: 980px; margin: 0 auto; padding: 44px 24px 80px; }
.section-label { font-family: 'DM Mono', monospace; font-size: 9.5px; letter-spacing: 3px; color: var(--c1-mid); text-transform: uppercase; margin-bottom: 20px; padding-bottom: 8px; border-bottom: 1px solid rgba(26,143,160,0.2); }
.timeline { margin-bottom: 52px; }
.timeline-track { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; }
.dest-card { border-radius: 10px; padding: 16px 14px 14px; position: relative; border: 1px solid transparent; transition: transform 0.2s; }
.dest-card:hover { transform: translateY(-3px); }
.dest-name { font-family: 'Playfair Display', serif; font-size: 15px; font-weight: 700; margin-bottom: 2px; }
.dest-country { font-family: 'DM Mono', monospace; font-size: 8.5px; letter-spacing: 2px; color: rgba(255,255,255,0.45); text-transform: uppercase; margin-bottom: 2px; }
.dest-dates { font-family: 'DM Mono', monospace; font-size: 9.5px; color: rgba(255,255,255,0.6); }
.dest-nights { margin-top: 10px; font-family: 'DM Mono', monospace; font-size: 10px; color: rgba(255,255,255,0.75); }
.dest-nights strong { font-size: 24px; font-weight: 400; display: block; line-height: 1; }
.dest-hotel { margin-top: 8px; font-size: 10px; color: rgba(255,255,255,0.5); font-style: italic; line-height: 1.3; }
.dest-hotel.warn { color: var(--coral); font-style: normal; font-weight: 500; }
.status-dot { width: 7px; height: 7px; border-radius: 50%; position: absolute; top: 12px; right: 12px; }
.status-dot.todo { background: var(--coral); box-shadow: 0 0 6px var(--coral); }
.status-dot.done { background: var(--green-ok); box-shadow: 0 0 6px var(--green-ok); }
.status-dot.sel  { background: var(--gold); box-shadow: 0 0 6px var(--gold); }
.flights-panel { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 12px; padding: 22px 24px; margin-bottom: 14px; }
.flight-row { display: flex; align-items: center; gap: 14px; padding: 11px 0; border-bottom: 1px solid rgba(255,255,255,0.06); }
.flight-row:last-child { border-bottom: none; padding-bottom: 0; }
.flight-dir { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 2px; color: var(--gold); width: 82px; flex-shrink: 0; }
.flight-route { display: flex; align-items: center; gap: 8px; flex: 1; flex-wrap: wrap; }
.airport { font-family: 'DM Mono', monospace; font-size: 17px; font-weight: 500; color: var(--white); }
.flight-arrow { color: rgba(255,255,255,0.22); font-size: 11px; }
.flight-via { font-family: 'DM Mono', monospace; font-size: 9.5px; color: rgba(255,255,255,0.3); }
.flight-time { font-family: 'DM Mono', monospace; font-size: 10.5px; color: rgba(255,255,255,0.45); text-align: right; line-height: 1.5; }
.badge-confirmed { background: rgba(76,175,80,0.12); border: 1px solid rgba(76,175,80,0.28); border-radius: 4px; padding: 2px 8px; font-family: 'DM Mono', monospace; font-size: 8.5px; color: #81c784; letter-spacing: 1px; white-space: nowrap; }
.badge-book   { background: rgba(232,96,60,0.12); border: 1px solid rgba(232,96,60,0.3); border-radius: 4px; padding: 2px 8px; font-family: 'DM Mono', monospace; font-size: 8.5px; color: #f08060; letter-spacing: 1px; white-space: nowrap; }
.badge-verify { background: rgba(224,160,32,0.12); border: 1px solid rgba(224,160,32,0.3); border-radius: 4px; padding: 2px 8px; font-family: 'DM Mono', monospace; font-size: 8.5px; color: #e8c050; letter-spacing: 1px; white-space: nowrap; }
.dest-section { margin-bottom: 52px; }
.dest-header { display: flex; align-items: baseline; gap: 14px; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.07); }
.dest-header-name { font-family: 'Playfair Display', serif; font-size: 28px; font-weight: 700; }
.dest-header-dates { font-family: 'DM Mono', monospace; font-size: 11px; color: rgba(255,255,255,0.35); letter-spacing: 1px; }
.dest-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px; }
.dest-grid.three { grid-template-columns: 1fr 1fr 1fr; }
.info-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; padding: 18px 20px; }
.info-card.full { grid-column: 1 / -1; }
.info-card.warn-card { border-color: rgba(232,96,60,0.3); background: linear-gradient(135deg, rgba(232,96,60,0.07) 0%, rgba(255,255,255,0.02) 100%); }
.info-card.highlight { border-color: rgba(212,168,67,0.3); background: linear-gradient(135deg, rgba(212,168,67,0.07) 0%, rgba(255,255,255,0.02) 100%); }
.info-card.accent { border-color: rgba(124,92,191,0.3); background: linear-gradient(135deg, rgba(124,92,191,0.08) 0%, rgba(255,255,255,0.02) 100%); }
.info-card-label { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 2.5px; text-transform: uppercase; color: rgba(255,255,255,0.3); margin-bottom: 10px; }
.info-card-label.warn { color: #f08060; }
.info-card-label.gold { color: #e8c060; }
.info-card-label.purple { color: #b09ae0; }
.info-card-title { font-size: 15px; font-weight: 500; margin-bottom: 4px; color: var(--white); }
.info-card-sub { font-size: 12px; color: rgba(255,255,255,0.45); line-height: 1.5; margin-bottom: 8px; }
.info-card-note { font-size: 11px; color: rgba(255,255,255,0.3); font-style: italic; line-height: 1.4; }
.info-card-price { display: inline-block; margin-top: 8px; font-family: 'DM Mono', monospace; font-size: 11px; color: var(--gold); background: rgba(212,168,67,0.1); border: 1px solid rgba(212,168,67,0.2); border-radius: 4px; padding: 2px 8px; }
.info-card-ref { display: inline-block; margin-top: 8px; margin-left: 6px; font-family: 'DM Mono', monospace; font-size: 9px; color: rgba(255,255,255,0.25); border: 1px solid rgba(255,255,255,0.1); border-radius: 4px; padding: 2px 8px; }
.info-card-link { display: inline-block; margin-top: 8px; margin-left: 6px; font-family: 'DM Mono', monospace; font-size: 10px; color: var(--c1-mid); text-decoration: none; border-bottom: 1px solid rgba(26,143,160,0.3); }
.alert-strip { display: flex; gap: 12px; align-items: flex-start; padding: 12px 16px; border-radius: 0 8px 8px 0; margin-bottom: 8px; font-size: 12px; line-height: 1.5; }
.alert-strip.red    { background: rgba(232,96,60,0.07); border-left: 3px solid var(--coral); }
.alert-strip.gold   { background: rgba(212,168,67,0.07); border-left: 3px solid var(--gold); }
.alert-strip.green  { background: var(--green-ok-dim); border-left: 3px solid var(--green-ok); }
.alert-strip.purple { background: var(--purple-dim); border-left: 3px solid var(--purple); }
.alert-strip .icon  { font-size: 14px; flex-shrink: 0; margin-top: 1px; }
.alert-strip .txt   { color: rgba(255,255,255,0.65); }
.alert-strip .txt strong { font-weight: 500; }
.alert-strip.red    .txt strong { color: var(--coral); }
.alert-strip.gold   .txt strong { color: var(--gold); }
.alert-strip.green  .txt strong { color: #81c784; }
.alert-strip.purple .txt strong { color: #c0a8f0; }
.days-grid { margin-bottom: 52px; }
.day-row { display: grid; grid-template-columns: 100px 1fr; gap: 12px; margin-bottom: 8px; align-items: start; }
.day-label { font-family: 'DM Mono', monospace; font-size: 9.5px; color: rgba(255,255,255,0.3); letter-spacing: 1px; padding-top: 12px; text-align: right; }
.day-label strong { display: block; font-size: 22px; font-weight: 300; color: rgba(255,255,255,0.55); line-height: 1; margin-bottom: 3px; }
.day-content { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 12px 16px; }
.day-content.alert-day { border-color: rgba(232,96,60,0.25); background: rgba(232,96,60,0.04); }
.day-country-tag { font-family: 'DM Mono', monospace; font-size: 8.5px; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px; padding: 2px 8px; border-radius: 3px; display: inline-block; }
.day-activities { font-size: 12.5px; color: rgba(255,255,255,0.55); line-height: 1.75; }
.day-activities li { list-style: none; padding-left: 14px; position: relative; }
.day-activities li::before { content: '·'; position: absolute; left: 2px; color: rgba(255,255,255,0.2); }
.day-activities .anchor { color: var(--white); font-weight: 500; }
.day-activities .opt    { color: rgba(255,255,255,0.28); font-style: italic; }
.day-activities .flag   { color: var(--coral); }
.day-activities .note   { color: var(--gold); font-size: 11px; }
.day-activities .tour   { color: #f0a858; font-weight: 500; }
.day-activities .event  { color: #c0a8f0; font-weight: 500; }
.refs-table { width: 100%; border-collapse: collapse; font-size: 12.5px; margin-bottom: 48px; }
.refs-table th { font-family: 'DM Mono', monospace; font-size: 8.5px; letter-spacing: 2px; text-transform: uppercase; color: rgba(255,255,255,0.3); padding: 8px 14px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.07); }
.refs-table td { padding: 10px 14px; border-bottom: 1px solid rgba(255,255,255,0.04); color: rgba(255,255,255,0.55); vertical-align: top; line-height: 1.5; }
.refs-table td:first-child { color: var(--white); font-weight: 400; }
.refs-table .ref-code { font-family: 'DM Mono', monospace; font-size: 11px; color: var(--gold); }
.refs-table .ref-canceled { color: var(--coral); text-decoration: line-through; }
.refs-table tr.canceled-row td { opacity: 0.55; }
.status-confirmed { color: #81c784; font-family: 'DM Mono', monospace; font-size: 9px; }
.status-verify    { color: #e8c050; font-family: 'DM Mono', monospace; font-size: 9px; }
.status-needed    { color: var(--coral); font-family: 'DM Mono', monospace; font-size: 9px; }
.checklist-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 52px; }
.check-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; padding: 18px; }
.check-card-title { font-size: 13px; font-weight: 500; margin-bottom: 12px; }
.check-item { display: flex; align-items: flex-start; gap: 8px; font-size: 11.5px; color: rgba(255,255,255,0.5); margin-bottom: 7px; line-height: 1.4; }
.check-item::before { content: '○'; color: var(--coral); flex-shrink: 0; font-size: 10px; margin-top: 1px; }
.check-item.done { color: rgba(255,255,255,0.28); text-decoration: line-through; }
.check-item.done::before { content: '●'; color: var(--green-ok); }
.check-item.sel::before { content: '◆'; color: var(--gold); }
.check-item.sel { color: rgba(255,255,255,0.65); }
.check-item.canceled { color: var(--coral); }
.check-item.canceled::before { content: '✕'; color: var(--coral); }
.admin-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 48px; }
.admin-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; padding: 18px 20px; }
.admin-card-label { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 2.5px; text-transform: uppercase; color: rgba(255,255,255,0.3); margin-bottom: 10px; }
.admin-card-title { font-size: 13px; font-weight: 500; margin-bottom: 6px; color: var(--white); }
.admin-card-body { font-size: 12px; color: rgba(255,255,255,0.45); line-height: 1.7; }
.admin-card-body strong { color: rgba(255,255,255,0.72); font-weight: 500; }
footer { text-align: center; padding: 24px; font-family: 'DM Mono', monospace; font-size: 9px; color: rgba(255,255,255,0.12); letter-spacing: 1.5px; }
@media (max-width: 700px) {
  .timeline-track { grid-template-columns: repeat(3, 1fr); }
  .dest-grid, .dest-grid.three { grid-template-columns: 1fr; }
  .checklist-grid { grid-template-columns: 1fr; }
  .admin-grid { grid-template-columns: 1fr; }
  .day-row { grid-template-columns: 64px 1fr; }
}
@media print {
  .hero { padding: 32px 24px 40px; }
  .hero-stars, .hero-wave { display: none; }
  body { background: #fff; color: #111; }
  .main { padding: 16px; }
}
```

### Country Tag Color Conventions

Define destination-specific tag classes inline per trip. Pattern:

```css
.day-country-tag.[destination] { background: rgba([r],[g],[b],0.5); color: [light-accent]; }
/* Examples: */
.day-country-tag.portugal { background: rgba(10,63,110,0.5);  color: #a8d4f0; }
.day-country-tag.spain    { background: rgba(106,16,16,0.5);  color: #f09090; }
.day-country-tag.morocco  { background: rgba(106,42,8,0.5);   color: #f0a858; }
.day-country-tag.oahu     { background: rgba(10,79,110,0.5);  color: #c8eaf5; }
.day-country-tag.transit  { background: rgba(40,50,60,0.5);   color: rgba(255,255,255,0.4); }
.day-country-tag.gap      { background: rgba(232,60,30,0.18); color: #e8603c; border: 1px solid rgba(232,60,30,0.3); }
```

---

## Constraints

- Do not fabricate addresses, phone numbers, confirmation codes, or times; use `TBD` or `Pending`.
- Never include PINs, access codes, passwords, payment card details, or sensitive login URLs; redact as `[redacted]`.
- Treat visa, entry, and customs notes as verification checklists, not legal advice.
- Google Fonts link requires internet on first load; note this if strict offline is required.

## Validation Checklist

Before finalizing, check the HTML mentally against this list:

- `<!DOCTYPE html>` is present.
- Viewport meta tag is present.
- Google Fonts `<link>` is in `<head>`.
- CSS variables declared in `:root` with destination palette tuned to the trip.
- Hero gradient and radial overlays reflect the destination character.
- Destination timeline cards have correct status dots and card gradients.
- All action items surface in red/gold alert strips near the top.
- Flights grouped into labeled panels with correct badges (confirmed / book / verify).
- Each destination section has at minimum a hotel card + one activity/tip alert strip.
- Day-by-day rows are in chronological order with country tags.
- Alert-day class applied to days with gaps or critical issues.
- Booking references table includes all booking numbers with status column.
- Checklist grid uses done/sel/canceled item states correctly.
- Admin grid has at minimum entry requirements + emergency contacts cards.
- Footer includes trip name · traveler · dates · route.
- Mobile CSS collapses grids to single column.
- Print CSS present.

## Help Response

If the user asks how to use this skill, respond briefly:

```text
Paste the trip emails or booking confirmations into this chat and ask me to create a shareable HTML itinerary. I can work from flights, hotel confirmations, rental cars, event tickets, tour bookings, and notes. I will redact sensitive PINs/payment details and return one complete styled HTML file in the established dark-theme design system.
```

## Fastest Useful Prompt

```text
Turn these trip emails into a shareable HTML itinerary. Include flights, lodging contacts, booking references, event notes, open items, and a day-by-day timeline. Redact anything sensitive.
```
