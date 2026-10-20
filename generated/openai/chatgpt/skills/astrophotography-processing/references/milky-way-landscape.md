# Milky Way Landscape Reference

Use this file for night-sky landscape workflows combining tracked sky and static foreground.

## Recommended Flow

1. Separate sky and foreground acquisition/processing when possible.
2. Stack tracked sky frames for noise control and detail.
3. Process foreground separately for realistic dynamic range and color.
4. Correct lens profile, vignetting, chromatic aberration, and gradient/light pollution.
5. Blend sky and foreground with realistic horizon transitions.

## Guardrails

- Keep sky brightness and horizon glow physically plausible.
- Avoid over-saturated Milky Way cores and neon foreground color shifts.
- Avoid aggressive local contrast that amplifies blotchy noise.

## Export Guidance

- Keep a high-bit editable master (16-bit TIFF minimum).
- Preserve an analysis/stack output separately when scientific detail matters.
- Use JPEG/PNG only for sharing.
