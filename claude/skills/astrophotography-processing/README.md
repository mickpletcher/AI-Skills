# Astrophotography Processing Skill

Claude skill for planning, troubleshooting, and guiding astrophotography image processing workflows.

## Use Cases

- Calibrate, register, stack, and stretch deep-sky image sets
- Process DSLR, mirrorless, OSC, mono LRGB, SHO, HOO, planetary, lunar, solar, and Milky Way data
- Troubleshoot gradients, star issues, calibration failures, noise, halos, color casts, and clipping
- Create tool-specific processing plans for PixInsight, Siril, Astro Pixel Processor, DeepSkyStacker, Photoshop, Lightroom, GIMP, Affinity, and Python
- Build non-destructive file organization and processing logs

## Core Behavior

The skill asks for acquisition context when needed, protects original files, prioritizes linear-stage technical correction before nonlinear finishing, and adapts recommendations to the user's software and data stage.

## Example Prompts

- "Help me process my Orion Nebula FITS stack in PixInsight."
- "I have 80 lights, 30 darks, flats, and bias from a DSLR. Build a Siril workflow."
- "Why do my stacked images still have dust donuts?"
- "Make a Python script to inspect FITS exposure times and filters."
- "Review this stretched image and tell me what to fix next."

## Files

- `SKILL.md`: Main Claude skill instructions.
- `upgrades.md`: Near-term enhancement ideas.
- `future-upgrades.md`: Longer-term possibilities.
- `completedchanges.md`: Change history.
