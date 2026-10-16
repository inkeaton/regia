#!/usr/bin/env python3
"""
Loading the questionnaire export.

Both compute_metrics.py and expand_data.py read data.xlsx through this module,
so that they always see the same rows.

Reading the file defensively matters. An export written by a tool other than
openpyxl often carries a missing or wrong dimension record, and openpyxl's
read-only mode trusts that record: iter_rows then yields nothing at all and the
scripts report an empty questionnaire instead of failing. The workbook is
therefore opened normally, the dimensions are recomputed, and the sheet holding
the responses is found by its header rather than assumed to be the active one.
"""

import openpyxl

ID_HEADER = "id"          # the first column of a Microsoft Forms export


def load_form_rows(path, verbose=True):
    """Return (header, rows) from the response sheet of the export.

    rows excludes the header and any row without an id, which is what trailing
    blank rows in an export look like.
    """
    workbook = openpyxl.load_workbook(path, read_only=False, data_only=True)

    candidates = []
    for sheet in workbook.worksheets:
        try:
            sheet.reset_dimensions()          # ignore the stored dimension record
        except AttributeError:
            pass
        rows = [r for r in sheet.iter_rows(values_only=True) if any(c is not None for c in r)]
        if not rows:
            continue
        header = rows[0]
        first = str(header[0]).strip().lower() if header and header[0] is not None else ""
        candidates.append((sheet.title, header, rows[1:], first == ID_HEADER, len(header)))

    if not candidates:
        raise SystemExit(f"{path}: no sheet contains any data. Check that the export is complete.")

    # Prefer a sheet whose first column is the id; otherwise the widest one.
    candidates.sort(key=lambda c: (c[3], c[4]), reverse=True)
    title, header, rows, looks_right, width = candidates[0]

    rows = [r for r in rows if r and r[0] is not None and str(r[0]).strip() != ""]

    if verbose:
        print(f"{path}: sheet '{title}', {len(rows)} responses, {width} columns")
        if not looks_right:
            print(f"  WARNING: the first column is '{header[0]}', not '{ID_HEADER}'. "
                  "Check that the column indices in the scripts still match this export.")
        if len(candidates) > 1:
            others = ", ".join(f"'{c[0]}'" for c in candidates[1:])
            print(f"  note: other non-empty sheets were ignored ({others})")
    if not rows:
        raise SystemExit(f"{path}: sheet '{title}' has a header but no responses.")
    return header, rows


def show_column_mapping(header, mapping):
    """Print which question each configured column index points at.

    The scripts address columns by position, so a question added to or removed
    from the form shifts them silently. Printing the header of each configured
    column makes such a shift visible on the next run.
    """
    print("  column mapping:")
    for name, index in mapping.items():
        if index >= len(header):
            print(f"    {name:<12} column {index}: MISSING, the export has {len(header)} columns")
            continue
        label = " ".join(str(header[index] or "").split())
        print(f"    {name:<12} column {index}: {label[:70]}{'...' if len(label) > 70 else ''}")