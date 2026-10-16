#!/usr/bin/env python3
"""
Expands the questionnaire's evaluation sheets when new responses arrive.

Each evaluation file is a long table keyed by respondent:

    coding_sheet_A.csv   one row per respondent x open item x rubric unit
                         (26 rows: 7 + 6 + 6 + 7 units for O1 to O4)
    gen_behaviour.csv    one row per respondent x specified behaviour
                         (15 rows, only for respondents who attempted the task)
    gen_syntax.csv       one row per respondent who attempted the task
    answer_key.csv       one row per closed-question option; its n_selected
                         column counts selections over the whole sample and so
                         goes stale whenever a response is added

This script finds the respondents present in data.xlsx but missing from each
file, appends the rows they need with the codes left blank, and recomputes
n_selected. It never modifies a row that already exists, so it is safe to run
repeatedly, and rows already coded are untouched.

The rubric itself is read from the existing rows rather than hard-coded: the
unit identifiers and their descriptions come from the units already recorded
for each item, and the behaviour descriptions from those already recorded in
gen_behaviour.csv. Editing the rubric therefore means editing the sheets, and
the next expansion follows.

What the script fills in, and what it leaves to the rater:

    filled    respondent, item, unit, rater, unit_desc, desc, in_scope,
              the response text being coded, and nonblank_lines
    blank     code, misconceptions, flag, syntax_conformance, notes, E1 to E5

Usage:
    python3 expand_data.py [DATA_DIR]            report what is missing
    python3 expand_data.py [DATA_DIR] --write    append the rows (makes .bak)
    python3 expand_data.py [DATA_DIR] --write --sort
                                                 also sort each file by key

Then fill the blank cells and rerun compute_metrics.py, which reports any
units still uncoded under "Data gaps".
"""

import argparse
import re
import shutil
from pathlib import Path

import pandas as pd

from form_data import load_form_rows, show_column_mapping

# Column indices in data.xlsx. These must match compute_metrics.py; if the form
# changes, change both.
COL_ID = 0
OPEN_ITEM_COLUMNS = {"O1": 9, "O2": 10, "O3": 13, "O4": 14}
COL_GENERATION = 15

RATER_DEFAULT = "A"

parser = argparse.ArgumentParser(description="Expand the evaluation sheets for new respondents.")
parser.add_argument("data_dir", nargs="?", default=".")
parser.add_argument("--write", action="store_true", help="append the rows; without it, only report")
parser.add_argument("--sort", action="store_true", help="sort each file by its key after appending")
args = parser.parse_args()
DATA = Path(args.data_dir)


def norm(text):
    return re.sub(r"\s+", " ", str(text)).strip()


# --- responses -------------------------------------------------------------

header, rows = load_form_rows(DATA / "data.xlsx")
show_column_mapping(header, {"id": COL_ID, "generation": COL_GENERATION,
                             **{f"open {k}": v for k, v in OPEN_ITEM_COLUMNS.items()}})
responses = {}
for row in rows:
    rid = int(row[COL_ID])
    responses[rid] = {
        "open": {item: (row[col] or "") for item, col in OPEN_ITEM_COLUMNS.items()},
        "generation": str(row[COL_GENERATION] or "").strip(),
    }
all_ids = sorted(responses)
generation_ids = [r for r in all_ids if responses[r]["generation"]]
print(f"{len(all_ids)} respondents, {len(generation_ids)} attempted the optional generation task")

pending = {}        # filename -> DataFrame of rows to append


def report_missing(name, present, expected, label):
    missing = [r for r in expected if r not in present]
    extra = [r for r in present if r not in all_ids]
    if extra:
        print(f"  {name}: WARNING, {len(extra)} respondent(s) not in data.xlsx: {extra}")
    print(f"  {name}: {len(present)} respondent(s) recorded, {len(missing)} to add"
          + (f" ({label}: {missing})" if missing else ""))
    return missing


# --- coding_sheet_A.csv ----------------------------------------------------

coding = pd.read_csv(DATA / "coding_sheet_A.csv")
missing = report_missing("coding_sheet_A.csv", set(coding["respondent"]), all_ids, "ids")
if missing:
    # The rubric template: the units of each item, in the order they were first
    # recorded, with their descriptions.
    template = (coding.drop_duplicates(subset=["item", "unit"])
                      .loc[:, ["item", "unit", "unit_desc"]])
    rater = coding["rater"].dropna().iloc[-1] if coding["rater"].notna().any() else RATER_DEFAULT
    new_rows = []
    for rid in missing:
        for t in template.itertuples():
            new_rows.append({"rater": rater, "respondent": rid, "item": t.item, "unit": t.unit,
                             "code": pd.NA, "unit_desc": t.unit_desc, "misconceptions": pd.NA,
                             "flag": pd.NA, "response": responses[rid]["open"].get(t.item, "")})
    pending["coding_sheet_A.csv"] = (pd.DataFrame(new_rows)[coding.columns], coding,
                                     ["respondent", "item", "unit"])
    blank = len(new_rows)
    print(f"    -> {blank} rubric rows ({blank // len(template)} respondents x {len(template)} units)")

# --- gen_behaviour.csv -----------------------------------------------------

beh = pd.read_csv(DATA / "gen_behaviour.csv", dtype={"code": str})
missing = report_missing("gen_behaviour.csv", set(beh["respondent"]), generation_ids, "ids")
if missing:
    template = beh.drop_duplicates(subset=["behaviour"]).loc[:, ["behaviour", "in_scope", "desc"]]
    new_rows = [{"respondent": rid, "behaviour": t.behaviour, "code": pd.NA,
                 "in_scope": t.in_scope, "desc": t.desc, "flag": pd.NA}
                for rid in missing for t in template.itertuples()]
    pending["gen_behaviour.csv"] = (pd.DataFrame(new_rows)[beh.columns], beh,
                                    ["respondent", "behaviour"])
    print(f"    -> {len(new_rows)} behaviour rows")

# --- gen_syntax.csv --------------------------------------------------------

syn = pd.read_csv(DATA / "gen_syntax.csv")
error_columns = [c for c in syn.columns if re.fullmatch(r"E\d+", c)]
missing = report_missing("gen_syntax.csv", set(syn["respondent"]), generation_ids, "ids")
if missing:
    new_rows = []
    for rid in missing:
        # Length is measurable from the submission; everything else is judged.
        lines = [ln for ln in responses[rid]["generation"].splitlines() if ln.strip()]
        row = {c: pd.NA for c in syn.columns}
        row["respondent"] = rid
        row["nonblank_lines"] = len(lines)
        new_rows.append(row)
    pending["gen_syntax.csv"] = (pd.DataFrame(new_rows)[syn.columns], syn, ["respondent"])
    print(f"    -> {len(new_rows)} syntax rows, with nonblank_lines counted from the submission")

# --- answer_key.csv: n_selected is derived, so recompute it ----------------

key = pd.read_csv(DATA / "answer_key.csv")
key["text_norm"] = key["option_text"].map(norm)
closed_columns = {"C1": 8, "C2": 11, "C3": 12}      # must match compute_metrics.py
counts = []
for option in key.itertuples():
    col = closed_columns[option.item]
    counts.append(sum(1 for row in rows if option.text_norm in norm(row[col] or "")))
key = key.drop(columns="text_norm")
changed = (key["n_selected"] != counts).sum()
print(f"  answer_key.csv: {changed} option(s) whose n_selected changed")
key_updated = key.assign(n_selected=counts)

# --- apply -----------------------------------------------------------------

if not args.write:
    print("\nNothing written. Rerun with --write to append these rows.")
    raise SystemExit

for name, (new, old, sort_keys) in pending.items():
    shutil.copy(DATA / name, DATA / f"{name}.bak")
    combined = pd.concat([old, new], ignore_index=True)
    if args.sort:
        combined = combined.sort_values(sort_keys, kind="stable", ignore_index=True)
    combined.to_csv(DATA / name, index=False)
    print(f"wrote {name} (+{len(new)} rows, backup in {name}.bak)")

if changed:
    shutil.copy(DATA / "answer_key.csv", DATA / "answer_key.csv.bak")
    key_updated.to_csv(DATA / "answer_key.csv", index=False)
    print(f"wrote answer_key.csv (n_selected recomputed, backup in answer_key.csv.bak)")

if pending:
    print("\nNext: fill the blank cells in the appended rows, then rerun\n"
          "  python3 compute_metrics.py <data_dir> results\n"
          "  python3 make_figures.py results figures\n"
          "compute_metrics.py lists any units still uncoded under \"Data gaps\".")