# Upgrade Log: trip-email-html-itinerary

Tracks implemented upgrades to this skill. Future upgrade ideas are in [future-upgrades.md](future-upgrades.md).

| Date | Upgrade | Notes |
| --- | --- | --- |
| 2026-07-21 | Added current-day briefing and transition feasibility | Added the current or next travel day's critical details near the top and travel-time plus buffer checks between scheduled locations. |
| 2026-07-21 | Added reusable sanitized HTML template | Added the established itinerary structure as a bundled placeholder-driven asset and made it the required generation starting point. |
| 2026-07-21 | Increased major section-title readability | Raised `.section-label` typography to 18px desktop, 19px tablet/phone, and 20px narrow-phone sizing while retaining the existing dark-theme treatment. |
| 2026-07-21 | Added restaurant and activity suggestions per destination | Requires current research for overnight stops, at least three credible options in each category when available, practical timing and booking guidance, source links, explicit suggested status, and reuse of the established destination-grid format. |
| 2026-06-29 | Replaced source with v2.0.0 canonical itinerary design system | Added required dark-theme HTML sections, destination palette rules, complete CSS block, component patterns, and expanded validation checklist. |
| 2026-06-10 | Added companion emergency contact sheet | A plain-text printable sheet with lodging, flights, transport, and key contacts can accompany the HTML file. |
| 2026-06-08 | Initial skill creation | Added workflow for extracting travel emails into a complete self-contained offline HTML itinerary with redaction and validation rules. |
