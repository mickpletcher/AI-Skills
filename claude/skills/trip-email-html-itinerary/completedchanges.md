# Completed Changes: trip-email-html-itinerary

| Date | Change | Notes |
| --- | --- | --- |
| 2026-07-21 | Added safe public demo generation | Added a deterministic fictional-itinerary generator, a ready-made validated public example, prominent non-validity labels, and validator enforcement that prevents personal data or deceptive booking use. |
| 2026-07-21 | Added accessibility, validation, and emergency outputs | Increased readability and contrast, added accessible interaction rules, bundled a deterministic PowerShell validator, added emergency replacement guidance, and shipped a real offline emergency contacts template. |
| 2026-07-21 | Added offline addresses and connected map links | Added verified plain-text addresses for lodging, recommendations, attractions, transport points, and tour meeting locations, plus Apple Maps and Google Maps links for connected use and explicit pending warnings when an address cannot be confirmed. |
| 2026-07-21 | Added quick navigation | Added static Apple Notes friendly anchor links below the hero for Flights, Hotels, Day Plan, Restaurants, Activities, Bookings, and Admin. |
| 2026-07-21 | Added categorized suggestions, urgency, and pacing | Added four restaurant categories, four activity categories, evidence-based reservation urgency labels, and daily Light/Balanced/Full/Overloaded pacing checks. |
| 2026-07-21 | Added today's details and travel-time checks | Added a generation-stamped current/next travel-day panel plus door-to-door travel estimates, buffers, feasibility checks, and action-item escalation for tight transitions. |
| 2026-07-21 | Added sanitized reference template | Added `assets/itinerary-template.html` as the required starting point for generated itineraries, preserving the established format without retaining personal trip data. |
| 2026-07-21 | Enlarged major section titles | Increased Destination Sequence, Action Items, Flights, and all other `.section-label` headings to 18px on desktop and 19–20px on phone layouts without changing the established format. |
| 2026-07-21 | Added destination restaurant and activity research | Added current-source research, selection rules, practical metadata, itinerary-fit checks, and clear separation between recommendations and confirmed bookings while preserving the established Europe & Morocco HTML format. |
| 2026-07-14 | Apple Notes first readability update | Updated the source skill to treat Apple Notes on iPhone as the primary viewing path, increased section and metadata label readability for mobile, added Apple Notes static HTML constraints in validation, and rebuilt the packaged `.skill` file. |
| 2026-06-29 | Replaced skill with v2.0.0 design-system version | Updated the source skill and Claude package to use the canonical dark-theme itinerary sections, CSS variables, validation checklist, and destination palette guidance. |
| 2026-06-10 | Added companion emergency contact sheet | A plain-text printable sheet with lodging, flights, transport, and key contacts can accompany the HTML file. |
| 2026-06-08 | Created skill | Added the initial Claude skill for turning travel emails and booking confirmations into shareable offline HTML itineraries. |
