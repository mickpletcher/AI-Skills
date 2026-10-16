# Calibration Reference

Use this file for calibration-specific decisions and frame-matching rules.

## Core Matching Rules

- Darks: Match lights by exposure length, gain/ISO, offset, temperature, binning, and camera readout/mode.
- Flats: Match filter, optical path, focus position, camera angle/orientation, gain/ISO, and binning.
- Dark-flats: Prefer dark-flats when flat exposure duration, dark current, amp glow, rolling/mechanical shutter behavior, or sensor pattern noise matters.
- Bias: Useful in many workflows, but do not blindly mix bias and dark-flats unless the software workflow explicitly expects it.

Use one primary term: dark-flats. Alias: flat darks.

## Do Not Reuse Flats When

- Camera rotation changed.
- Filter changed.
- Focus changed significantly.
- Sensor/window was cleaned.
- Dust moved or optical train spacing changed.

## Reject Questionable Calibration Frames

Reject flats that are:

- Clipped in highlights or crushed in shadows.
- Unevenly illuminated (severe gradient, edge falloff beyond expected vignetting, panel flicker).
- Contaminated by light leaks.
- Taken after a changed optical train.

Reject darks/bias/dark-flats that are:

- Taken at clearly different temperature, gain/ISO, offset, binning, or mode.
- Corrupted, clipped, or showing unstable sensor behavior.

## Practical Decision Flow

1. Verify lights and calibration metadata consistency first.
2. Confirm calibration strategy for software in use (bias-based or dark-flat-based).
3. Calibrate a small subset and inspect residual dust/vignetting/noise patterns.
4. If overcorrection or undercorrection appears, re-check flats and dark-flat/bias compatibility before changing downstream processing.

## Exports and Data Safety

- Preserve original source files.
- Preserve a linear calibrated/integrated master in 32-bit FITS/TIFF or equivalent.
- Use 16-bit TIFF for nonlinear finishing.
- Use JPEG/PNG only for sharing.
