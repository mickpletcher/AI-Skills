---
name: photo-rename
version: 1.1.0
description: Rename photos using image analysis, GPS metadata, and web research to generate descriptive real-world filenames such as "grand_canyon_phantom_ranch.jpg" or "eiffel_tower_paris.jpg". Trigger immediately when the user's message starts with "rp", or when they upload photos and ask to rename, identify, or label them by location or content. Supports batch processing.
---

# Photo Rename Skill

Rename photos to descriptive real-world names using a combination of image analysis, EXIF metadata, reverse geocoding, and web research.

## Trigger

Use this skill when the user's message starts with `rp`, or when they upload photos and ask to rename, identify, or label them.

## Workflow

### 1. Extract EXIF metadata

Extract GPS coordinates and date-taken metadata from each image when available.

Useful EXIF tags include:

- `GPS GPSLatitude`
- `GPS GPSLatitudeRef`
- `GPS GPSLongitude`
- `GPS GPSLongitudeRef`
- `EXIF DateTimeOriginal`

If metadata extraction tooling is needed, use a lightweight EXIF reader and convert GPS rational values to decimal degrees.

Treat metadata as supporting evidence, not automatic truth. If GPS values are missing, obviously wrong, or inconsistent with the image, lower confidence and fall back to image and context based naming.

### 2. Identify what each photo shows

Use a combination of:

**A. Image analysis**

Look for:

- recognizable landmarks
- natural features
- structures
- visible signs or text
- any other identifying context

**B. GPS reverse geocoding**

If GPS coordinates exist, use them to get place context through a reverse-geocoding service.

**C. Web research for specificity**

Combine what the image shows with the GPS location to identify the most specific likely landmark, trail, attraction, or place name.

### 3. Batch review before naming

When multiple images are provided, review them as a set before finalizing names:

- group visually or contextually similar images
- look for shared date, place, event, or subject patterns
- keep naming consistent across the batch instead of naming each file in isolation
- use sequence suffixes only after the shared naming pattern is stable

If the user provides only one image, skip the grouping logic.

### 4. Generate the new filename

Rules:

- use `snake_case`
- prefer specific names over generic ones
- order parts consistently as `date_location_event_subject` when enough evidence exists
- omit any segment that cannot be supported instead of inventing it
- prefer the strongest identifying segment order available, such as `location_subject` or `date_location_subject`
- include a place type like `waterfall`, `trail`, `overlook`, or `beach` when it helps
- keep names under 50 characters when practical
- preserve the original file extension
- avoid special characters except underscores

Ordering guidance:

1. **Date** if capture date is reliable and useful to distinguish the set
2. **Location** at the most specific supportable level
3. **Event** when a shared trip, hike, ride, build session, or landmark stop is clear
4. **Subject** as the final differentiator

Examples:

- `2026_05_road_to_hana_black_sand_beach.jpg`
- `paris_eiffel_tower_night_view.jpg`
- `stewart_county_container_home_weld_frame.jpg`

Fallback priority when confidence is low:

1. If GPS exists but the landmark is unclear, use the best supported place name such as `stewart_county_tennessee`
2. If GPS is missing or likely wrong, fall back to date plus visible subject if possible
3. If there is no reliable location data and the image cannot be identified, use `unidentified_photo_01`, `unidentified_photo_02`, and so on

Collision handling:

- if two photos would receive the same name, append `_01`, `_02`, and so on
- treat this as collision-safe rename behavior, not a failure
- keep suffix numbering stable inside a batch so follow-up cleanup is not needed

Confidence handling:

- **High**: subject and place are clear from multiple signals
- **Medium**: most likely name is strong but one part is inferred
- **Low**: only partial subject or place identification is possible
- **None**: no defensible descriptive name is available

### 5. Output a rename report

Produce a clear rename report rather than assuming the files can be renamed in place.

Example format:

```text
PHOTO RENAME REPORT
===================

[PASS] IMG_4821.jpg  ->  phantom_ranch_grand_canyon.jpg
   Confidence: High | GPS: 36.1069, -112.0605 | Method: GPS + vision + web search
   Reason: Landmark and location agree clearly

[PASS] IMG_4822.jpg  ->  colorado_river_bright_angel_trail.jpg
   Confidence: High | GPS: 36.0975, -112.1129 | Method: GPS + web search
   Reason: GPS and trail context support the same destination

[WARN] IMG_4823.jpg  ->  stewart_county_tennessee.jpg
   Confidence: Low | GPS: 36.3012, -87.8456 | Method: GPS reverse geocode only
   Note: Could not identify a specific landmark

[FAIL] IMG_4824.jpg  ->  unidentified_photo_01.jpg
   Confidence: None | No GPS data | Could not identify from image alone

===================
4 photos processed | 2 high confidence | 1 fallback to GPS | 1 unidentified
```

For batch requests, also include:

- the old name
- the new name
- the confidence level
- the short reason for the chosen name
- any batch grouping note when similar files were named together

## Notes

- Process all uploaded photos before producing the final report
- For well-known landmarks, use the common English name most people would recognize
- For remote or natural areas, be as specific as the available data allows
- If web results conflict, prefer the answer most consistent with the image and the location data
- If GPS looks obviously wrong, say so and do not anchor the filename to it
- When the subject is only partly identifiable, choose the most defensible generic subject instead of overclaiming specificity
- The final deliverable is the rename report unless the user explicitly asks for a script or file operation
