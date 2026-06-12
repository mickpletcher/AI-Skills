# Comets, Mosaics, and OSC Dual-Narrowband Reference

Use this file for special-case workflows that need separate registration/compositing logic.

## Comets

1. Calibrate lights normally.
2. Register once on stars and once on the comet nucleus when possible.
3. Create separate star-aligned and comet-aligned integrations.
4. Use masking/compositing to avoid smeared stars or smeared comet structure.
5. Preserve a scientifically honest version if position, coma/tail structure, or photometry matters.

## Mosaics

1. Calibrate and integrate each panel consistently.
2. Handle severe panel gradients before final merge, but avoid overfitting backgrounds.
3. Register/plate-solve panels with consistent geometry.
4. Match background level, scale, color, and noise across panels.
5. Blend seams conservatively and inspect stars in overlap regions for distortion/doubling.

## OSC Dual-Narrowband

1. Calibrate and debayer correctly.
2. Extract/map channels intentionally, commonly toward HOO-like output.
3. Do not treat dual-band OSC data like ordinary broadband RGB.
4. Use RGB stars when available; otherwise balance narrowband stars carefully.
5. Watch for magenta stars, teal backgrounds, and over-suppressed green/yellow.
