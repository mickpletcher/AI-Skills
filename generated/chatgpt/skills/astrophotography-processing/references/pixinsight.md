# PixInsight Reference

Use this file when the user is processing in PixInsight.

## Typical Linear-First Order

1. Calibration/registration/integration via WeightedBatchPreprocessing or manual workflow.
2. Quality control with Blink and/or SubframeSelector.
3. DynamicCrop.
4. Gradient removal with DBE/ABE while still linear.
5. Color calibration with SPCC/PCC as appropriate.
6. Linear denoise with masks (NoiseXTerminator, MLT, or TGV).
7. Optional deconvolution or BlurXTerminator when sampling/SNR/masks support it.
8. Stretch with HistogramTransformation, MaskedStretch, or GHS.
9. Nonlinear refinement with Curves and local contrast controls.
10. Optional star separation/recombination with StarXTerminator or StarNet-style tools when it improves control.

## Guardrails

- Do not use SCNR as a substitute for proper color calibration.
- Use SCNR sparingly and only for residual cast cleanup after proper calibration.
- Avoid fixed numeric recipes; provide starting ranges and adjust by visual/statistical cues.
- Check for halos, ringing, and plastic textures after star or sharpening operations.

## Suggested Checks Per Stage

- After calibration/integration: background smoothness, dust correction, rejection map quality.
- After gradient/color calibration: neutral background trend and plausible star colors.
- After denoise/sharpen: no waxy nebulosity, no ringing around stars.
- After stretch: no clipped black point, preserved star cores.

## Export Guidance

- Keep linear master in 32-bit FITS/TIFF or equivalent.
- Use 16-bit TIFF for nonlinear handoff/finishing.
- Use JPEG/PNG only for web sharing.
