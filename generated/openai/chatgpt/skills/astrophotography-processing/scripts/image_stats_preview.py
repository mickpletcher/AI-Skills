#!/usr/bin/env python3
"""Inspect image files and optionally write small previews to process/."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect TIFF/PNG/JPEG images and optionally create previews."
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=".",
        help="Folder to scan (default: current directory)",
    )
    parser.add_argument(
        "--write-preview",
        action="store_true",
        help="Write resized preview images into process/preview_*.png",
    )
    parser.add_argument(
        "--preview-max-size",
        type=int,
        default=1600,
        help="Maximum width/height for generated previews (default: 1600)",
    )
    return parser.parse_args()


def iter_images(folder: Path) -> Iterable[Path]:
    valid = {".tif", ".tiff", ".png", ".jpg", ".jpeg"}
    for path in sorted(folder.rglob("*")):
        if path.is_file() and path.suffix.lower() in valid:
            yield path


def format_mean(value) -> str:
    if isinstance(value, (int, float)):
        return f"{value:.2f}"
    return "n/a"


def main() -> int:
    args = parse_args()
    folder = Path(args.folder).expanduser().resolve()

    if not folder.exists() or not folder.is_dir():
        print(f"Error: folder not found or not a directory: {folder}")
        return 2

    try:
        from PIL import Image, ImageStat
    except ImportError:
        print(
            "Missing dependency: Pillow is required for image inspection. "
            "Install with: pip install pillow"
        )
        return 1

    files = list(iter_images(folder))
    if not files:
        print(f"No TIFF/PNG/JPEG files found under: {folder}")
        return 0

    process_dir = folder / "process"
    if args.write_preview:
        process_dir.mkdir(parents=True, exist_ok=True)

    for path in files:
        try:
            with Image.open(path) as img:
                mode = img.mode
                width, height = img.size
                extrema = img.getextrema()
                stat = ImageStat.Stat(img)

                if isinstance(extrema, tuple) and len(extrema) > 0 and isinstance(extrema[0], tuple):
                    channels = []
                    for i, ext in enumerate(extrema):
                        mean = stat.mean[i] if i < len(stat.mean) else "n/a"
                        channels.append(
                            f"ch{i}: min={ext[0]}, max={ext[1]}, mean={format_mean(mean)}"
                        )
                    channel_summary = "; ".join(channels)
                else:
                    if isinstance(extrema, tuple):
                        ext_min, ext_max = extrema
                    else:
                        ext_min, ext_max = ("n/a", "n/a")
                    mean = stat.mean[0] if stat.mean else "n/a"
                    channel_summary = (
                        f"min={ext_min}, max={ext_max}, mean={format_mean(mean)}"
                    )

                print(f"{path.name}\tmode={mode}\tsize={width}x{height}\tstats={channel_summary}")

                if args.write_preview:
                    preview = img.copy()
                    preview.thumbnail((args.preview_max_size, args.preview_max_size))
                    target = process_dir / f"preview_{path.stem}.png"
                    preview.save(target)
                    print(f"  preview: {target}")
        except Exception as exc:
            print(f"{path.name}\terror: {exc}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
