---
name: trip-email-html-itinerary
description: >
  Extract trip logistics from pasted travel emails, booking confirmations,
  forwarded messages, reservation notes, or raw itinerary text, research useful
  restaurant and activity suggestions for each destination, and generate one
  polished, self-contained offline HTML itinerary file for sharing with family
  or other travelers. Trigger when the user asks to turn trip emails into an
  HTML itinerary, travel handoff page, shareable trip page, family trip summary,
  booking-reference page, destination recommendation page, or offline travel
  document.
version: 2.10.0
---

# Trip Email HTML Itinerary

## Intent

Turn a batch of travel-related emails into a complete, shareable HTML trip document. The final file should help the traveler and a spouse, family member, or travel companion quickly understand flights, lodging, rental cars, events, booking references, contact details, open issues, day-by-day logistics, and worthwhile places to eat and things to do at each destination.

Primary viewing target is Apple Notes on iPhone while traveling. Assume the user will drop the `.html` file into Apple Notes for quick access. Favor clarity and larger section labels over dense desktop styling when there is a tradeoff.

Use this skill for email-derived travel organization and offline HTML output. If the user wants a planning Markdown file instead, use the travel-itinerary skill.

## Trigger When

- The user asks to create an HTML itinerary from emails, confirmations, or forwarded trip details.
- The user asks for a shareable trip page, family travel handoff, offline travel document, or complete travel summary from bookings.
- The user asks for an itinerary they can save into Apple Notes for quick mobile retrieval.
- The user says they will drop the HTML file into Apple Notes for quick travel access.
- The input includes travel emails for flights, hotels, car rentals, tours, events, restaurants, insurance, visas, or logistics.
- The user wants restaurant or activity ideas added to an email-derived itinerary.
- The user asks for a fake, sample, synthetic, portfolio, or public demonstration itinerary that can be shared as social-media images.
- The user wants a single `.html` file that works locally without a server or internet access.

## Do Not Use When

- The user wants live booking, price comparison, broad destination comparison, or current visa/legal advice.
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
- offline locations: full street addresses for lodging, restaurants, attractions, transport pickup/drop-off points, and tour meeting points when verified
- stated food interests, dietary needs, activity preferences, mobility limits, budget clues, and must-do experiences
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

### 3. Research Each Destination

Research current restaurant and activity options for every overnight destination. Skip airport-only connections unless the schedule allows a realistic layover outing.

- Browse current sources. Prefer official attraction, restaurant, tourism-board, and venue pages. Use reputable local guides or current map/listing results only to fill gaps.
- Check that each suggestion appears open and operating for the trip period. Verify hours, seasonal closures, reservation rules, ticket requirements, and location when they affect the plan.
- Choose four restaurant suggestions per destination when credible options exist: **Quick Meal**, **Local Specialty**, **Nice Dinner**, and **Near Hotel**. Do not force separate cards when one place legitimately fills two categories; label both uses and add another distinct option only when useful.
- Choose four activity suggestions per destination when credible options exist: **Main Attraction**, **Outdoor Activity**, **Cultural Activity**, and **Bad-Weather Backup**.
- Match suggestions to the traveler's stated interests, dietary needs, budget, mobility, available time, hotel area, and existing bookings. If preferences are unknown, provide a useful mix instead of asking first.
- Favor local specialties and independent local places. Include one convenient option near the lodging or planned route when possible.
- State restaurant category, cuisine, neighborhood, price level, why it fits, and reservation urgency.
- State activity category, expected duration, area, booking need, weather suitability, and the best itinerary window.
- Account for travel time and opening hours. Do not place suggestions into a day when they conflict with a confirmed booking or create unrealistic backtracking.
- Keep researched suggestions visually and verbally distinct from confirmed reservations. Label them `SUGGESTED`, never `CONFIRMED`.
- Include a direct source link for each suggestion when internet use is allowed. Add a short `Verify hours and availability` note because operating details can change.
- If current research is unavailable or the user prohibits browsing, include only options supported by the supplied material and label them `UNVERIFIED SUGGESTION`. Do not rely on memory for current business status.
- Do not invent ratings, prices, addresses, hours, availability, or claims such as "best" or "local favorite."

### Offline Address Support

Include a readable plain-text location for every place the traveler may need to reach. Do not make the traveler depend on a map link.

- Prefer the full verified street address from the booking confirmation or the venue's official current page.
- Include venue/property name, street address, locality, postal code when available, and country when cross-border ambiguity is possible.
- For airports and stations, include terminal, concourse, platform, entrance, or pickup zone when confirmed and operationally useful.
- For tours and events, distinguish the venue address from the actual meeting or pickup point.
- For restaurants and activities, place the address directly in the recommendation card beneath the summary.
- For the current or next travel day, repeat critical lodging, meeting-point, pickup, and departure addresses in Today's Critical Details.
- Add both Apple Maps and Google Maps links after every verified plain-text address when internet links are allowed.
- Build Apple Maps links as `https://maps.apple.com/?q=[URL-encoded full address]`.
- Build Google Maps links as `https://www.google.com/maps/search/?api=1&query=[URL-encoded full address]`.
- URL-encode the complete verified address. Do not use URL shorteners, tracking redirects, API keys, or guessed coordinates.
- Keep official-site links as separate optional conveniences. Map and official links supplement the plain-text address and may require internet access.
- If a precise address cannot be verified, write `Address pending — verify before travel` and add it to Action Items when the location is schedule-critical.
- Never guess an address from a venue name, neighborhood, postal code, or search snippet.

Assign one evidence-based urgency label to every restaurant and activity suggestion:

- `BOOK NOW` — limited capacity, fixed entry, known sellout risk, or a schedule-critical option that requires advance booking
- `BOOK SOON` — advance booking is advisable but the option is not yet schedule-critical
- `WALK-IN LIKELY` — current sources support walk-in use or no advance ticket is normally required
- `VERIFY BEFORE VISITING` — hours, access, seasonal operation, or booking expectations remain uncertain

Do not infer availability from the label. Explain the reason briefly and link the source used.

Use existing badge classes so urgency remains consistent with the established format:

- `BOOK NOW` → `.badge-book`
- `BOOK SOON` → `.badge-verify`
- `WALK-IN LIKELY` → `.badge-confirmed`
- `VERIFY BEFORE VISITING` → `.badge-verify`

### 4. Build A Working Trip Model

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
  "restaurantSuggestions": [],
  "activitySuggestions": [],
  "todayCriticalDetails": {},
  "travelTimeBlocks": [],
  "dailyPacing": [],
  "offlineAddresses": [],
  "emergencyReplacement": {},
  "emergencyContactsSheet": {},
  "dayByDay": [],
  "bookingReferences": [],
  "travelAdmin": [],
  "pendingItems": [],
  "canceledItems": []
}
```

### 5. Start From The Reference Template

Read `assets/itinerary-template.html` before generating the itinerary. Use it as the required visual and structural starting point.

- Copy the template into the requested output `.html` file and replace its `{{PLACEHOLDER}}` values with reconciled trip data.
- Preserve the template's section order, class names, dark-theme styling, spacing, responsive behavior, and 18–20px major section labels.
- Duplicate destination cards, destination sections, flight rows, day rows, booking rows, checklist cards, and admin cards as needed.
- Remove unused example blocks and optional sections instead of leaving empty cards.
- Keep the template CSS unless destination palette values or destination-specific tag/card classes need adjustment.
- Apply the research, redaction, reconciliation, and validation rules in this file when filling the template.
- Never copy traveler data from another itinerary into the output. The bundled template is intentionally sanitized and is the only reusable layout source.

### Public Demo Mode

When the user requests an example that can be shown publicly, generate the social-media carousel with `scripts/New-PublicDemoItinerary.ps1` or follow the same deterministic rules. A ready-made validated example is bundled at `examples/public-demo-social/`.

```powershell
./scripts/New-PublicDemoItinerary.ps1 `
  -OutputDirectory ./public-demo-social `
  -BrowserChannel msedge
```

- Produce ten numbered 1080 x 1350 JPEG files in deterministic carousel order: cover, trip overview, flights, hotels and transport, restaurants, activities, day plan, bookings, travel admin, and emergency replacement.
- Treat the generated HTML as a temporary render source. Delete it after a successful export unless `-KeepHtml` is explicitly requested for debugging.
- Require Microsoft Edge and `npx` with Playwright available on the generation computer. The exported JPG files are standalone and need no browser or internet connection.
- Display `PUBLIC DEMO · FICTIONAL DATA · NOT VALID FOR TRAVEL OR BOOKING` in a fixed bottom watermark on every JPG.

- Use synthetic travelers, destinations, countries, airlines, hotels, venues, addresses, routes, schedules, prices, and booking references.
- Make fictional names unmistakable with labels such as `(Fictional)`, `Example`, `Sample`, or `Demo`.
- Display `PUBLIC DEMO · FICTIONAL DATA · NOT VALID FOR TRAVEL OR BOOKING` prominently at the top, in the footer, and in the fixed JPG watermark.
- Include `PUBLIC DEMO` in the HTML `<title>`.
- Do not derive demo data from user emails, an existing itinerary, memory, downloaded files, or prior generated output.
- Do not include real names, contact details, confirmation codes, loyalty numbers, policy numbers, document numbers, payment details, identity images, private addresses, or personal travel dates.
- Use `example.com` for non-official demonstration links. Official government recovery links and Apple/Google map link formats may remain to demonstrate functionality.
- Do not generate an emergency contacts sheet for a public demo.
- Never present the output as proof of travel, proof of accommodation, an onward-travel document, a visa document, or a valid booking.

### 6. Required HTML Sections

Produce a complete HTML document with these sections in order, omitting only sections with no useful data:

1. **Hero** — trip title, date range, route string (BNA → LIS → BCN → ...), status badge pills, destination character gradient
2. **Quick Navigation** — static anchor links directly below the hero for Flights, Hotels, Day Plan, Restaurants, Activities, Bookings, and Admin
3. **Destination Timeline** — one card per major stop (equivalent to "island cards" in multi-stop trips)
4. **Action Items** — red/gold alert strips for anything requiring user action before departure
5. **Today's Critical Details** — a generation-time snapshot of the current travel day's schedule, lodging/transport, essential references, and immediate warnings. Use **Next Travel Day** when the current date is outside the trip window
6. **Flights** — confirmed segments in green-badged panels; unbooked/verify segments in red/yellow panels
7. **Destination Sections** — one per city/region using the established hotel, dining, transport, tour/activity card, and alert-strip layout. Add restaurant and activity suggestions inside the existing destination grid. Each suggestion includes fit/reason, area, practical timing, reservation or ticket guidance, source link, and a `SUGGESTED` label
8. **Day-by-Day Itinerary** — date-keyed rows with country tags, activity lists, travel-time lines, and schedule warnings
9. **Booking References** — full table with What / Details / Reference / Status columns
10. **Booking Checklist** — card grid organized by category (Flights, Hotels, Transport, Tours, Admin, Finance)
11. **Travel Admin** — 2-column card grid for passport/visa, ID rules, baggage, emergency contacts
12. **Emergency Replacement** — lost passport, driver's license, Global Entry card, and payment-card response steps with masked identifiers and official links
13. **Footer** — trip name · traveler · dates · route

### Quick Navigation

Use plain HTML fragment links only. Do not add JavaScript, menus, dropdowns, or sticky behavior.

- Place the quick-navigation strip immediately below the hero and above the main content.
- Use these standard targets: `#flights`, `#destinations`, `#day-plan`, `#restaurants`, `#activities`, `#bookings`, and `#admin`.
- Assign each `id` exactly once. Place `#restaurants` on the first restaurant recommendation group and `#activities` on the first activity recommendation group.
- Remove a navigation link when its target section is omitted.
- Keep labels short enough to wrap cleanly on iPhone: Flights, Hotels, Day Plan, Restaurants, Activities, Bookings, Admin.
- Preserve readable content order so the itinerary remains fully usable when an Apple Notes viewer does not honor fragment navigation.

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

Add a travel-time line between scheduled locations when movement is required:

```html
<li class="note">Travel: [origin] → [destination] · ~[duration] by [mode] + [buffer] buffer</li>
```

- Estimate door-to-door travel time, not only vehicle time. Include walking to transit, parking, security, baggage, and likely transfer time when applicable.
- Prefer current official transit, airport, rail, ferry, venue, or map-routing sources. Treat map times as estimates and note when traffic or service conditions can change them.
- Use the confirmed end time and location of one item and the start time and location of the next to check feasibility.
- Require enough time for travel plus a practical buffer. Use larger buffers for airports, border crossings, rental-car pickup/drop-off, unfamiliar stations, and fixed-entry events.
- Add a `.flag` warning and repeat the issue in Action Items when the available gap is shorter than travel time plus buffer, or when key locations/times are unknown.
- Do not invent precise travel time. Use `Estimate unavailable — verify route` when reliable routing information cannot be obtained.
- Avoid adding travel-time lines between activities in the same compact venue or area unless the transition affects the schedule.

Evaluate the full daily load after adding confirmed items, travel, meals, and optional suggestions. Add one pacing label to each day:

- `LIGHT` — arrival, departure, recovery, or one primary commitment with ample free time
- `BALANCED` — one or two primary commitments with realistic meals, travel, and rest
- `FULL` — several commitments are feasible but leave limited flexibility; identify what to drop first
- `OVERLOADED` — the plan does not fit safely or practically; move or remove items and add a `.flag` warning

Render the pacing label with `.badge-confirmed` for LIGHT or BALANCED, `.badge-verify` for FULL, and `.badge-book` for OVERLOADED.

Apply these pacing rules:

- Count door-to-door travel, check-in, security, queues, meals, hydration, and recovery time as part of the day.
- Limit arrival days to one nonessential anchor after hotel check-in. Avoid nonessential anchors after long-haul arrivals unless the user explicitly requests them.
- Keep departure-day activities close to the lodging or departure point and preserve the required airport or station buffer.
- Avoid stacking multiple strenuous activities or multiple fixed-entry attractions without a realistic break.
- Preserve regular meal windows. Add a meal or snack note when a long transit or activity block would otherwise skip one.
- Treat restaurant and activity suggestions as optional until selected. Do not fill every open hour merely because suggestions exist.
- For `FULL` days, mark the lowest-priority optional item as the first item to drop.
- For `OVERLOADED` days, revise the plan when possible. If confirmed bookings prevent revision, surface the conflict in Action Items.

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

### Restaurant And Activity Suggestion Cards

Preserve the established Europe & Morocco itinerary format. Do not redesign the document, introduce a standalone recommendations section, change the section order, create a new card system, or replace existing class names and visual styling.

Add suggestions within each destination's existing `.dest-grid` alongside its hotel, dining, transport, and booked-tour cards. Use the same `.info-card`, `.info-card-label`, `.info-card-title`, `.info-card-sub`, `.info-card-note`, and `.info-card-ref` structure already used by the itinerary. Use existing accent variants only when they already exist in the document. Keep recommendations visually subordinate to confirmed bookings.

Render restaurant cards in this order: Quick Meal, Local Specialty, Nice Dinner, Near Hotel. Render activity cards in this order: Main Attraction, Outdoor Activity, Cultural Activity, Bad-Weather Backup. Omit a category only when no credible current option exists and state that gap in a short destination note.

```html
<div class="info-card">
  <div class="info-card-label">🍽 Dining — Suggested · $$</div>
  <div class="info-card-title">[Name]</div>
  <div class="info-card-sub">[Cuisine or activity type] · [Neighborhood] · [Best itinerary window]</div>
  <div class="info-card-note">[Why it fits] · [Reservation, ticket, duration, or hours note] · Verify hours and availability</div>
  <span class="badge-verify">[BOOK NOW | BOOK SOON | WALK-IN LIKELY | VERIFY BEFORE VISITING]</span>
  <a class="info-card-ref" href="[direct source URL]">Official details</a>
</div>
```

Use the same pattern for activities with an appropriate existing label such as `🏛 Activity — Suggested`, `🚶 Activity — Suggested`, or `🏕 Tour — Suggested`. Add a short `.opt` item to the relevant day-by-day row only when the suggestion fits that day's route. Do not turn optional suggestions into fixed itinerary anchors.

Do not place researched suggestions in the Booking References table or mark their checklist items done unless the input confirms a reservation.

### Canonical HTML Template

Use `assets/itinerary-template.html` as the sole source of truth for complete HTML, CSS, component markup, responsive rules, and print rules. Do not reconstruct or replace its stylesheet from memory.

Change only destination palette values and destination-specific card or country-tag classes when the trip requires them. Keep structural class names and rules unchanged.

### Emergency Replacement And Contact Sheet

Generate a separate plain-text emergency sheet from `assets/emergency-contacts-template.txt` alongside every HTML itinerary unless the user declines it. Name it `[trip-name]-emergency-contacts.txt`.

- Include the trip route, dates, traveler names, primary emergency contact, insurance, airlines, lodging, transport, tour contacts, embassy/consulate contacts, and local emergency numbers.
- Include lost passport, driver's license, Global Entry, and payment-card response instructions.
- Use current official replacement links. Prefer the U.S. State Department, U.S. embassy or consulate, issuing DMV, Trusted Traveler Programs, and card issuer.
- Mask passport, driver's-license, PASSID, insurance-policy, and payment-card identifiers. For cards, include issuer and last four digits only.
- Never include ID images, full payment-card numbers, CVV/CVC, PINs, passwords, access codes, or banking credentials.
- Refer to ID copies only by secure storage location, such as `Locked Apple Note: Travel ID Backup`. Do not embed them in the HTML or contact sheet.
- Keep the sheet plain text, printable, and usable without internet. Links supplement the written phone numbers and instructions.

### Accessibility

- Keep body text at 16px or larger and supporting card/table text at 12px or larger.
- Maintain strong contrast for body, dimmed notes, links, status badges, and warnings. Do not communicate status by color alone.
- Keep interactive links and navigation controls at least 44px high on touch layouts.
- Use visible `:focus-visible` outlines, semantic landmarks, a skip link, and meaningful link labels.
- Support `prefers-reduced-motion` and remove decorative motion when requested.
- Keep tables horizontally scrollable and grids single-column on narrow screens.

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
- Do not substitute a clickable link for a plain-text address. Critical locations must remain readable offline.
- Do not fabricate or imply current restaurant or attraction details. Research them live, link to the source, and distinguish suggestions from bookings.
- Never include PINs, access codes, passwords, payment card details, or sensitive login URLs; redact as `[redacted]`.
- Never embed passport, driver's-license, Global Entry, or payment-card images in the itinerary or emergency contacts sheet.
- Never use Public Demo Mode to create deceptive booking evidence or documents intended to pass as real travel reservations.
- Treat visa, entry, and customs notes as verification checklists, not legal advice.
- Keep the output self-contained and Apple Notes friendly: avoid JavaScript dependencies, external script tags, iframes, and interaction patterns that require a browser runtime beyond static HTML/CSS.
- Google Fonts link requires internet on first load; note this if strict offline is required.

## Validation Checklist

Before finalizing, run the bundled validator and then review the output visually:

```powershell
./scripts/Test-ItineraryHtml.ps1 -Path ./trip.html -EmergencyContactsPath ./trip-emergency-contacts.txt -FailOnWarnings
```

- `<!DOCTYPE html>` is present.
- Output was built from `assets/itinerary-template.html` and retains its established structure and classes.
- No unresolved `{{PLACEHOLDER}}` tokens remain.
- Viewport meta tag is present.
- Google Fonts `<link>` is in `<head>`.
- HTML remains usable when opened from Apple Notes on iPhone with no JavaScript required.
- CSS variables declared in `:root` with destination palette tuned to the trip.
- Hero gradient and radial overlays reflect the destination character.
- Quick-navigation links appear below the hero, use no JavaScript, and each `href="#..."` has exactly one matching element `id`.
- Existing itinerary format, section order, CSS classes, spacing, and dark-theme visual system remain intact when adding suggestions.
- Major `.section-label` headings such as Destination Sequence, Action Items, Flights, Day-by-Day Itinerary, Booking References, Booking Checklist, and Travel Admin render at 18px minimum on desktop and increase to 19–20px on phone layouts.
- Destination timeline cards have correct status dots and card gradients.
- All action items surface in red/gold alert strips near the top.
- Today's Critical Details appears after Action Items, is stamped with its generation date/time, and switches to Next Travel Day outside the active trip window.
- Today's Critical Details shows the day's fixed schedule, lodging/transport, essential references, and urgent warnings without exposing sensitive values.
- Today's Critical Details repeats the verified plain-text addresses needed for the current or next travel day.
- Flights grouped into labeled panels with correct badges (confirmed / book / verify).
- Each destination section retains the established hotel, dining, transport, activity, and alert-strip composition where those components apply.
- Each overnight destination covers Quick Meal, Local Specialty, Nice Dinner, and Near Hotel restaurant categories when credible options exist.
- Each overnight destination covers Main Attraction, Outdoor Activity, Cultural Activity, and Bad-Weather Backup categories when credible options exist.
- Restaurant suggestions include category, cuisine, area, price level, fit, and reservation urgency.
- Activity suggestions include category, type, area, duration or timing, weather suitability, fit, and ticket urgency.
- Every suggestion has exactly one supported urgency label: BOOK NOW, BOOK SOON, WALK-IN LIKELY, or VERIFY BEFORE VISITING.
- Every lodging, restaurant, attraction, transport pickup/drop-off, and tour meeting point has a verified plain-text address or an explicit `Address pending — verify before travel` warning.
- Every verified address has Apple Maps and Google Maps links when internet links are allowed; both use the URL-encoded verified address and no API key or URL shortener.
- Official-site and map links supplement addresses but never replace them.
- All researched options are labeled `SUGGESTED`, have direct source links when browsing is allowed, and remain separate from confirmed bookings.
- Suggested items fit the day-by-day geography and do not conflict with confirmed logistics.
- Day rows include estimated travel time, travel mode, and a practical buffer when movement between scheduled locations affects feasibility.
- Tight or unverifiable transitions appear as `.flag` items and are repeated in Action Items.
- Every day is labeled LIGHT, BALANCED, FULL, or OVERLOADED after travel, meals, buffers, and recovery time are counted.
- FULL days identify the first optional item to drop; OVERLOADED days are revised or escalated to Action Items.
- Day-by-day rows are in chronological order with country tags.
- Alert-day class applied to days with gaps or critical issues.
- Booking references table includes all booking numbers with status column.
- Checklist grid uses done/sel/canceled item states correctly.
- Admin grid has at minimum entry requirements + emergency contacts cards.
- Emergency Replacement covers passport, driver's license, Global Entry, and payment cards using masked details and official recovery links.
- Separate emergency contacts sheet was generated from `assets/emergency-contacts-template.txt`, contains no unresolved placeholders, and remains usable offline.
- Body and supporting text meet the template's larger readable sizes, interactive targets are at least 44px, keyboard focus is visible, and reduced-motion CSS is present.
- Footer includes trip name · traveler · dates · route.
- Mobile CSS collapses grids to single column.
- Print CSS present.
- Public demos pass `Test-ItineraryHtml.ps1 -PublicDemo -FailOnWarnings` before rendering, contain no personal or real booking data, and leave no HTML file unless `-KeepHtml` was requested.
- Public demos produce exactly ten ordered JPG files. Each is a valid 1080 x 1350 JPEG, has a distinct section label where applicable, and keeps the fictional-data warning visible at the bottom.

## Help Response

If the user asks how to use this skill, respond briefly:

```text
Paste the trip emails or booking confirmations into this chat and ask me to create a shareable HTML itinerary. I can work from flights, hotel confirmations, rental cars, event tickets, tour bookings, and notes. I will research restaurant and activity suggestions, redact sensitive details, and return a styled HTML itinerary plus a separate offline emergency contacts sheet.
```

## Fastest Useful Prompt

```text
Turn these trip emails into a shareable HTML itinerary. Include flights, lodging contacts, booking references, event notes, open items, a day-by-day timeline, and researched restaurant and activity suggestions for each destination. Redact anything sensitive.
```
