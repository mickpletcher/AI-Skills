# APP, DSS, and Finishing Tools Reference

Use this file for Astro Pixel Processor (APP), DeepSkyStacker (DSS), and finishing workflows in Photoshop, Lightroom, GIMP, or Affinity.

## Astro Pixel Processor (APP)

- Load by session/filter consistently.
- Calibrate, analyze stars, register, normalize, integrate.
- Use light pollution removal carefully on a saved intermediate or duplicate.
- For mosaics and multi-session data, keep panel/session normalization consistent.

## DeepSkyStacker (DSS)

- Load light/dark/flat/bias frames correctly.
- Register checked pictures and verify debayer settings for RAW/OSC.
- Save 16-bit or 32-bit TIFF with embedded adjustments disabled when possible.
- Complete advanced nonlinear finishing in a dedicated editor.

## Photoshop, Lightroom, GIMP, Affinity

- Use these mainly for nonlinear finishing or Milky Way landscape blending.
- Start from high-bit TIFF data where possible.
- Use masks for selective control of sky/background/subject.
- Avoid heavy clarity, texture, sharpening, or saturation on noisy backgrounds.
- Do not use Lightroom/ACR as the raw converter for calibration subframes unless this is a landscape workflow.

## Export Guidance

- Preserve linear master data in 32-bit FITS/TIFF or equivalent when available.
- Use 16-bit TIFF for nonlinear finishing and round-tripping.
- Use JPEG/PNG only for web/social sharing.
