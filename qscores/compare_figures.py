#!/usr/bin/env python3
"""
Compares a directory of redrawn figures with the paper's.

Both directories must hold the same files. PNGs must have the same pixels
(their compressed bytes may differ), any other file exactly the same text,
except for line endings. Exits with status 1 on any difference.

Usage:  python3 compare_figures.py [FIG_DIR] [REFERENCE_DIR]

    FIG_DIR defaults to figures/ and REFERENCE_DIR to reference/figures/, both
    next to this script.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from matplotlib.image import imread

HERE = Path(__file__).resolve().parent

parser = argparse.ArgumentParser(description="Compare redrawn figures with the paper's.")
parser.add_argument("fig_dir", nargs="?", type=Path, default=HERE / "figures")
parser.add_argument("reference_dir", nargs="?", type=Path, default=HERE / "reference" / "figures")
args = parser.parse_args()


def file_names(folder):
    if not folder.is_dir():
        raise SystemExit(f"{folder}: no such directory")
    return {path.name for path in folder.iterdir() if path.is_file()}


def difference(old, new):
    """Says how two files differ, or returns None if they match."""
    if old.suffix != ".png":
        # read_text normalises line endings.
        same = old.read_text(encoding="utf-8") == new.read_text(encoding="utf-8")
        return None if same else "the text differs"
    a, b = imread(old), imread(new)
    if a.shape != b.shape:
        return f"size {b.shape}, reference {a.shape}"
    pixels = int(np.any(a != b, axis=-1).sum())
    if pixels:
        return f"{pixels} pixels differ, by at most {round(255 * float(np.abs(a - b).max()))}/255"
    return None


reference, redrawn = file_names(args.reference_dir), file_names(args.fig_dir)
if not any(name.endswith(".png") for name in reference):
    raise SystemExit(f"{args.reference_dir}: no reference figures")

failed = False
for name in sorted(reference | redrawn):
    if name not in redrawn:
        print(f"MISSING  {name}")
    elif name not in reference:
        print(f"EXTRA    {name}")
    else:
        found = difference(args.reference_dir / name, args.fig_dir / name)
        if found is None:
            print(f"same     {name}")
            continue
        print(f"DIFFERS  {name}: {found}")
    failed = True

if failed:
    sys.exit("The redrawn figures differ from the reference.")
print(f"All {len(reference)} files match the reference.")
