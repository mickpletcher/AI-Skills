---
name: trip-email-html-itinerary
description: >
  Extract trip logistics from pasted travel emails, booking confirmations,
  forwarded messages, reservation notes, or raw itinerary text and generate one
  polished, self-contained offline HTML itinerary file for sharing with family
  or other travelers. Trigger when the user asks to turn trip emails into an
  HTML itinerary, travel handoff page, shareable trip page, family trip summary,
  booking-reference page, or offline travel document.
version: 1.0.0
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
- Treat cancellation emails as warnings and mark related items canceled unless another later email re-confirms them.
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

Produce a complete HTML document with these sections, omitting only sections with no useful data:

1. Hero / masthead with trip title, date range, route summary, status pills, and a CSS-only visual panel.
2. Key trip cards for major travel legs, major events, lodging milestones, return travel, and open concerns.
3. Route overview with airport or city code bubbles connected by responsive lines.
4. Contact quick reference near the top, with one compact lodging/contact card per stay and clickable `tel:` / `mailto:` links.
5. Day-by-day itinerary with chronological timeline entries for flights, check-ins, rental pickup/drop-off, driving legs, tours, events, and open items.
6. Where I'm Staying with detailed lodging cards.
7. Booking reference with flights, hotels, rental cars, events, and other reservation numbers.
8. Event notes for schedule-sensitive activities and warnings.
9. Travel admin with passport/visa notes, trusted traveler notes, insurance, pending bookings, and canceled items.

## HTML Output Rules

- Return only the full HTML document in one fenced `html` code block unless the user explicitly asks for explanation or files.
- Start with `<!doctype html>`.
- Include `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- Use inline CSS inside `<style>`.
- Do not use JavaScript.
- Do not use remote images, local images, web fonts, icon libraries, external CSS, external scripts, or CDN links.
- Do not include `http://`, `https://`, or `file://` references unless the user explicitly asks to preserve a non-sensitive URL.
- Do not include local machine paths such as `/Users/...`, `C:\...`, or `~/...`.
- Use only native system fonts:
  `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif`.
- Use semantic HTML where practical: `header`, `main`, `section`, `article`, `footer`, `address`, `time`.
- Use clickable `tel:` links for phone numbers and `mailto:` links for emails.
- Use calm, practical styling. This is an operational trip document, not a marketing landing page.
- Keep cards compact and readable.
- Make long addresses, emails, booking references, and notes wrap cleanly with CSS.
- Include print-friendly CSS with `@media print`.
- Ensure mobile layout has no horizontal overflow.

## Design Guidance

Use a restrained visual system that feels like a travel operations brief:

- light neutral background, white cards, dark readable text
- one or two accent colors for route markers and status pills
- compact card grids that collapse to one column on small screens
- timeline rows with clear time, title, description, and tags
- pending/canceled states visually distinct but not alarming
- CSS-only route panel using gradients, borders, dots, and simple shapes

Avoid:

- oversized hero marketing layout
- decorative stock image placeholders
- external icons or emoji
- dense tables that overflow on phones
- tiny low-contrast text

## Required Validation

Before finalizing, check the HTML mentally against this list:

- `<!doctype html>` is present.
- The viewport meta tag is present.
- No remote dependencies are referenced.
- No sensitive access codes, PINs, passwords, CVV/card details, or login URLs remain.
- Contact Quick Reference appears near the top.
- Confirmed lodging has address and telephone number when available.
- Unknown lodging/contact details are marked pending.
- Day-by-day events are chronological.
- Canceled items are not mixed into active itinerary steps without a clear canceled label.
- Long emails, addresses, and confirmation codes wrap.
- Mobile CSS prevents horizontal overflow.
- Print CSS hides decorative elements and keeps essential sections readable.

## Help Response

If the user asks how to use this skill, respond briefly:

```text
Paste the trip emails or booking confirmations into this chat and ask me to create a shareable HTML itinerary. I can work from flights, hotel confirmations, rental cars, event tickets, tour bookings, and notes. I will redact sensitive PINs/payment details and return one complete offline HTML file.
```

## Fastest Useful Prompt

```text
Turn these trip emails into a shareable offline HTML itinerary for my family. Include flights, lodging contacts, booking references, event notes, open items, and a day-by-day timeline. Redact anything sensitive.
```
