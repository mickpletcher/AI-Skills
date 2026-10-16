# Troubleshooting Reference

Use this file when diagnosing artifacts or failed processing stages.

## Common Artifacts and Likely Causes

- Strong gradients: moonlight, light pollution, poor flats, dew/cloud changes, extraction sample placement.
- Dust motes remain: flat mismatch (focus/orientation), clipped flats, dust moved after flats.
- Walking noise: insufficient dithering, weak rejection, calibration mismatch.
- Banding: sensor pattern noise, weak dithering, aggressive stretch, calibration gaps.
- Green cast: debayer mismatch, incomplete color calibration, filter/channel imbalance.
- Purple/magenta stars: saturation imbalance, chromatic aberration, narrowband star mapping issues.
- Halos around stars: filter halos, aggressive deconvolution/sharpening, over-strong star separation/recombine.
- Bloated stars: focus/seeing/guiding limits, over-stretch, chromatic aberration.
- Black clipping: over-aggressive black point/histogram clipping.
- Ringing/sharpen artifacts: deconvolution/wavelet too strong, weak masks.
- Flat overcorrection or undercorrection: flat exposure mismatch, incompatible dark-flats/bias usage, changed optical train.
- Registration double stars: poor reference selection, differential distortion, wind/tracking outliers, mixed focal scale.
- Satellite rejection failure: too few frames, weak rejection thresholds, trail persistence in aligned stack.
- Color blotching: aggressive nonlinear stretch/denoise, poor channel SNR balance, compression artifacts.
- Chromatic aberration: optics/filter mismatch, focus shift by channel, extreme edge stretch.
- Backfocus/tilt issues: elongated stars varying by field position, sensor tilt, spacing errors.
- Ringing from star reduction: over-aggressive morphological/star shrink operations and hard masks.

## Recovery Pattern

1. Identify stage where artifact first appears.
2. Verify whether issue exists in linear master or only after nonlinear edits.
3. Re-run the smallest earlier stage needed to test the suspected cause.
4. Keep old and new results side-by-side for objective comparison.
