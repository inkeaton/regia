#!/usr/bin/env python3
"""
Compares the regenerated CSVs with the paper's (reference/results).

Every reference CSV must exist in RESULTS_DIR with exactly the same text, and
RESULTS_DIR may hold no other CSV. Only line endings may differ. Exits with
status 1 on any difference.

Usage:  python3 compare_reference.py [RESULTS_DIR] [REFERENCE_DIR]

    RESULTS_DIR defaults to results/ and REFERENCE_DIR to reference/results/,
    both next to this script.
"""

import argparse
import difflib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

parser = argparse.ArgumentParser(description="Compare regenerated CSVs with the paper's.")
parser.add_argument("results_dir", nargs="?", type=Path, default=HERE / "results")
parser.add_argument("reference_dir", nargs="?", type=Path, default=HERE / "reference" / "results")
args = parser.parse_args()


def csv_names(folder):
    if not folder.is_dir():
        raise SystemExit(f"{folder}: no such directory")
    return {path.name for path in folder.glob("*.csv")}


reference, results = csv_names(args.reference_dir), csv_names(args.results_dir)
if not reference:
    raise SystemExit(f"{args.reference_dir}: no reference CSVs")

failed = False
for name in sorted(reference | results):
    if name not in results:
        print(f"MISSING  {name}")
    elif name not in reference:
        print(f"EXTRA    {name}")
    else:
        # read_text normalises line endings; everything else must match exactly.
        old = (args.reference_dir / name).read_text(encoding="utf-8")
        new = (args.results_dir / name).read_text(encoding="utf-8")
        if old == new:
            print(f"same     {name}")
            continue
        print(f"DIFFERS  {name}")
        diff = difflib.unified_diff(old.splitlines(), new.splitlines(),
                                    f"reference/{name}", f"regenerated/{name}", "", "", 0, "")
        print("\n".join(f"    {line}" for line in diff))
    failed = True

if failed:
    sys.exit("The regenerated CSVs differ from the reference.")
print(f"All {len(reference)} CSVs match the reference.")
