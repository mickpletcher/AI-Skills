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
