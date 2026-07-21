# Completed Changes: trip-email-html-itinerary

| Date | Change | Notes |
| --- | --- | --- |
| 2026-07-21 | Added today's details and travel-time checks | Added a generation-stamped current/next travel-day panel plus door-to-door travel estimates, buffers, feasibility checks, and action-item escalation for tight transitions. |
| 2026-07-21 | Added sanitized reference template | Added `assets/itinerary-template.html` as the required starting point for generated itineraries, preserving the established format without retaining personal trip data. |
| 2026-07-21 | Enlarged major section titles | Increased Destination Sequence, Action Items, Flights, and all other `.section-label` headings to 18px on desktop and 19–20px on phone layouts without changing the established format. |
| 2026-07-21 | Added destination restaurant and activity research | Added current-source research, selection rules, practical metadata, itinerary-fit checks, and clear separation between recommendations and confirmed bookings while preserving the established Europe & Morocco HTML format. |
| 2026-07-14 | Apple Notes first readability update | Updated the source skill to treat Apple Notes on iPhone as the primary viewing path, increased section and metadata label readability for mobile, added Apple Notes static HTML constraints in validation, and rebuilt the packaged `.skill` file. |
| 2026-06-29 | Replaced skill with v2.0.0 design-system version | Updated the source skill and Claude package to use the canonical dark-theme itinerary sections, CSS variables, validation checklist, and destination palette guidance. |
| 2026-06-10 | Added companion emergency contact sheet | A plain-text printable sheet with lodging, flights, transport, and key contacts can accompany the HTML file. |
| 2026-06-08 | Created skill | Added the initial Claude skill for turning travel emails and booking confirmations into shareable offline HTML itineraries. |
