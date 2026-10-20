#!/usr/bin/env python3
"""Read FITS headers in a folder and print a compact metadata audit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit FITS/FIT headers without modifying files."
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=".",
        help="Folder to scan (default: current directory)",
    )
    return parser.parse_args()


def iter_fits_files(folder: Path) -> Iterable[Path]:
    exts = {".fit", ".fits", ".fts", ".fit.gz", ".fits.gz", ".fts.gz"}
    for path in sorted(folder.rglob("*")):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        name = path.name.lower()
        if suffix in {".fit", ".fits", ".fts"} or any(name.endswith(ext) for ext in exts):
            yield path


def get_first_header(hdul):
    if len(hdul) > 0 and hasattr(hdul[0], "header"):
        return hdul[0].header
    return None


def get_first_data_shape(hdul) -> str:
    for hdu in hdul:
        data = getattr(hdu, "data", None)
        if data is not None and hasattr(data, "shape"):
            return "x".join(str(v) for v in data.shape)
    return "n/a"


def field(header, *keys, default="n/a"):
    for key in keys:
        if key in header:
            return header.get(key)
    return default


def main() -> int:
    args = parse_args()
    folder = Path(args.folder).expanduser().resolve()

    if not folder.exists() or not folder.is_dir():
        print(f"Error: folder not found or not a directory: {folder}")
        return 2

    try:
        from astropy.io import fits
    except ImportError:
        print(
            "Missing dependency: astropy is required for FITS audits. "
            "Install with: pip install astropy"
        )
        return 1

    files = list(iter_fits_files(folder))
    if not files:
        print(f"No FITS/FIT files found under: {folder}")
        return 0

    print("filename\tdimensions\tEXPTIME\tFILTER\tGAIN\tOFFSET\tTEMP\tBINNING\tDATE-OBS\tOBJECT\tBAYERPAT")
    for path in files:
        try:
            with fits.open(path) as hdul:
                header = get_first_header(hdul)
                shape = get_first_data_shape(hdul)
                if header is None:
                    print(f"{path.name}\t{shape}\tn/a\tn/a\tn/a\tn/a\tn/a\tn/a\tn/a\tn/a\tn/a")
                    continue

                exptime = field(header, "EXPTIME", "EXPOSURE")
                filt = field(header, "FILTER", "FILTNAM", "INSFLNAM")
                gain = field(header, "GAIN", "EGAIN")
                offset = field(header, "OFFSET", "BLACKLVL")
                temp = field(header, "CCD-TEMP", "CCD_TEMP", "SENSOR_TEMP", "TEMP", "SET-TEMP")
                binning = field(header, "XBINNING", "BINNING", "CCDBINX")
                date_obs = field(header, "DATE-OBS", "DATE_OBS")
                obj = field(header, "OBJECT", "OBJNAME")
                bayer = field(header, "BAYERPAT", "BAYERPATN", "COLORTYP")

                print(
                    f"{path.name}\t{shape}\t{exptime}\t{filt}\t{gain}\t{offset}\t{temp}\t{binning}\t{date_obs}\t{obj}\t{bayer}"
                )
        except Exception as exc:
            print(f"{path.name}\terror: {exc}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
