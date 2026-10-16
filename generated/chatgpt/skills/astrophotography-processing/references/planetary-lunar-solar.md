# Planetary, Lunar, and Solar Reference

Use this file for lucky imaging, video stacking, and sharpening workflows.

## Typical Workflow

1. Start from SER/AVI/MOV or burst image sequences.
2. Pre-sort and stabilize (for example with PIPP when needed).
3. Stack best frames in AutoStakkert or equivalent.
4. Sharpen with wavelets/deconvolution in controlled passes.
5. Color-balance and contrast-tune conservatively.

## Planetary Notes

- Keep separate passes for detail and color if needed.
- For Jupiter/Saturn/Mars, optional WinJUPOS de-rotation can improve detail retention over longer captures.
- Avoid over-sharpening halos and edge ringing around limbs.

## Lunar Notes

- Manage local contrast carefully to avoid brittle, over-processed texture.
- In mosaics, match tone/noise before seam blending.

## Solar Safety

- Do not provide capture advice that implies viewing or imaging the Sun without a proper front-mounted solar filter or a purpose-built solar telescope.
- Processing guidance is acceptable, but correct unsafe acquisition assumptions briefly.

## Export Guidance

- Keep a high-bit master (preferably 16-bit TIFF or higher where supported).
- Use JPEG/PNG only for sharing copies.
