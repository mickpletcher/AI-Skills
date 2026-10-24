# Siril Reference

Use this file when the user is processing in Siril.

## Typical Siril Flow

1. Convert and organize sequences.
2. Run OSC or mono preprocessing scripts only when frame assumptions match acquisition.
3. Register and stack with appropriate rejection.
4. Perform photometric color calibration when available.
5. Apply background extraction on linear data.
6. Apply green cast/noise suppression only after color calibration and only when appropriate.
7. Stretch with asinh/histogram methods.
8. Export for further finishing if needed.

## Guardrails

- For unusual calibration needs, prefer manual Siril steps over one-click scripts.
- Do not force green suppression before validating color calibration.
- Avoid aggressive denoise/sharpen before assessing gradient and color balance.

## Suggested Checks

- Confirm sequence registration quality and star FWHM consistency.
- Inspect stack rejection behavior for satellite trails and clouds.
- Validate color balance before nonlinear enhancement.

## Export Guidance

- Keep linear/integration masters in 32-bit FITS/TIFF or equivalent when possible.
- Use 16-bit TIFF for nonlinear finishing.
- Use JPEG/PNG only for sharing.
