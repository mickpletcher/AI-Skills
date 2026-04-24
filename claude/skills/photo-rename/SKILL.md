---
name: photo-rename
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

### 3. Generate the new filename

Rules:

- use `snake_case`
- prefer specific names over generic ones
- include a place type like `waterfall`, `trail`, `overlook`, or `beach` when it helps
- keep names under 50 characters when practical
- preserve the original file extension
- avoid special characters except underscores

Fallback priority when confidence is low:

1. If GPS exists but the landmark is unclear, use a reverse-geocoded place name such as `stewart_county_tennessee`
2. If there is no GPS data and the image cannot be identified, use `unidentified_photo_01`, `unidentified_photo_02`, and so on

If two photos would receive the same name, append `_01`, `_02`, and so on.

### 4. Output a rename report

Produce a clear rename report rather than assuming the files can be renamed in place.

Example format:

```text
PHOTO RENAME REPORT
===================

[PASS] IMG_4821.jpg  ->  phantom_ranch_grand_canyon.jpg
   Confidence: High | GPS: 36.1069, -112.0605 | Method: GPS + vision + web search

[PASS] IMG_4822.jpg  ->  colorado_river_bright_angel_trail.jpg
   Confidence: High | GPS: 36.0975, -112.1129 | Method: GPS + web search

[WARN] IMG_4823.jpg  ->  stewart_county_tennessee.jpg
   Confidence: Low | GPS: 36.3012, -87.8456 | Method: GPS reverse geocode only
   Note: Could not identify a specific landmark

[FAIL] IMG_4824.jpg  ->  unidentified_photo_01.jpg
   Confidence: None | No GPS data | Could not identify from image alone

===================
4 photos processed | 2 high confidence | 1 fallback to GPS | 1 unidentified
```

## Notes

- Process all uploaded photos before producing the final report
- For well-known landmarks, use the common English name most people would recognize
- For remote or natural areas, be as specific as the available data allows
- If web results conflict, prefer the answer most consistent with the image and the location data
- The final deliverable is the rename report unless the user explicitly asks for a script or file operation
