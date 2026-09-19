#!/usr/bin/env python3
"""
Regia questionnaire -- OPEN comprehension items: rubric tooling.

  python3 score_open.py init            -> writes blank coding sheets
  python3 score_open.py score           -> scores filled sheets + reliability

Codes: 2 = explicit and correct, 1 = present but vague/under-specified,
       0 = absent or contradicted, blank = not yet coded.

Requires: pandas, numpy, matplotlib, openpyxl
"""
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SRC = "data.xlsx"
OUT = "."
OPEN_COLS = {"O1": 9, "O2": 10, "O3": 13, "O4": 14}
MAXCODE = 2
RELIABILITY_SAMPLE = [2, 4, 6, 8, 11, 13, 15, 17, 20]   # respondents double-coded

RUBRIC = {
 "O1": [("U1", "triggered by the digestion_check event"),
        ("U2", "applies to agents assigned NobleSocializing (role/playbook scope, not one guest)"),
        ("U3", "body guarded by the is_hungry fact"),
        ("U4", "eat_food executes when the guard holds"),
        ("U5", "FORGET retracts the is_hungry belief"),
        ("U6", "PRINT emits the message"),
        ("U7", "nothing happens when the guard is false (no else branch)")],

 "O2": [("U1", "triggered by the food_served event"),
        ("U2", "PRINT executes unconditionally, before the test"),
        ("U3", "condition includes (is_hungry OR is_drunk)"),
        ("U4", "AND NOT hates(host) - both conjuncts, correct precedence"),
        ("U5", "eat_food on true"),
        ("U6", "complain on the else branch")],

 "O3": [("U1", "the block scopes behaviour to one phase of a plot"),
        ("U2", "ON ENTER fires once, at phase entry"),
        ("U3", "WORLD DO is an environment/director-level action, not an agent's"),
        ("U4", "ASSIGN targets the Guest ROLE, hence all its occupants"),
        ("U5", "WHEN food_served causes TRANSITION TO feast"),
        ("U6", "the trigger is live throughout the phase, not only at entry")],
        
 "O4": [("U1", "ON ENTER -> serve_wine at world level"),
        ("U2", "trigger is a SIGNAL raised BY an agent playing Guest (bottom-up)"),
        ("U3", "stop_music executes"),
        ("U4", "START SUBPLOT HonorDuel"),
        ("U5", "MAPPING Guest TO Challenger is a role mapping into the subplot"),
        ("U6", "TRANSITION TO duel_interruption"),
        ("U7", "ON EXIT fires on leaving the phase, so UNASSIGN happens then")],
}

MISCONCEPTIONS = {
 "M1": "role treated as a single agent instance",
 "M2": "WORLD read as a named agent",
 "M3": "signal direction reversed (plot->agent)",
 "M4": "MAPPING read as permanent role change, not subplot mapping",
 "M5": "boolean precedence error",
 "M6": "ON ENTER/EXIT read as an agent entering/leaving",
 "M7": "action conflated with event",
 "M8": "invented semantics not present in the fragment",
}


def responses():
    df = pd.read_excel(SRC)
    out = {}
    for item, col in OPEN_COLS.items():
        out[item] = [" ".join(str(v).replace("\xa0", " ").split())
                     for v in df.iloc[:, col].fillna("")]
    return out


def init():
    """Blank coding sheets, one row per respondent x unit."""
    resp = responses()
    for rater in ("A", "B"):
        rows = []
        for item, units in RUBRIC.items():
            for r in range(1, len(resp[item]) + 1):
                if rater == "B" and r not in RELIABILITY_SAMPLE:
                    continue
                for uid, desc in units:
                    rows.append({"rater": rater, "respondent": r, "item": item,
                                 "unit": uid, "code": "", "unit_desc": desc,
                                 "misconceptions": "", "flag": "",
                                 "response": resp[item][r - 1] if uid == units[0][0] else ""})
        pd.DataFrame(rows).to_csv(f"{OUT}/coding_sheet_{rater}.csv", index=False)
        print(f"wrote coding_sheet_{rater}.csv  ({len(rows)} judgements)")
    pd.DataFrame([{"code": k, "meaning": v} for k, v in MISCONCEPTIONS.items()]
                 ).to_csv(f"{OUT}/misconception_codes.csv", index=False)
    print("rater B sheet covers respondents", RELIABILITY_SAMPLE)


def krippendorff_ordinal(units_by_item):
    """Ordinal Krippendorff's alpha. units_by_item: list of lists of codes
    (one inner list per coded unit, containing that unit's codes from each rater)."""
    vals = sorted({v for u in units_by_item for v in u})
    idx = {v: i for i, v in enumerate(vals)}
    n_tot = sum(len(u) for u in units_by_item if len(u) > 1)
    if n_tot == 0:
        return np.nan
    # observed coincidence matrix
    O = np.zeros((len(vals), len(vals)))
    for u in units_by_item:
        m = len(u)
        if m < 2:
            continue
        for a in range(m):
            for b in range(m):
                if a != b:
                    O[idx[u[a]], idx[u[b]]] += 1.0 / (m - 1)
    n = O.sum(1)

    def delta(c, k):
        if c == k:           
            return 0.0
        lo, hi = min(c, k), max(c, k)
        s = n[lo]/2 + n[hi]/2 + n[lo+1:hi].sum()
        return s**2

    D = np.array([[delta(c, k) for k in range(len(vals))] for c in range(len(vals))])
    Do = (O * D).sum() / n_tot
    De = sum(n[c] * n[k] * D[c, k] for c in range(len(vals))
             for k in range(len(vals)) if c != k) / (n_tot * (n_tot - 1))
    return 1 - Do / De if De else np.nan


def score():
    A = pd.read_csv(f"{OUT}/coding_sheet_A.csv")
    A = A[A.code.notna()].copy()
    A["code"] = A.code.astype(float)

    # ---- reliability against rater B, if present
    try:
        B = pd.read_csv(f"{OUT}/coding_sheet_B.csv")
        B = B[B.code.notna()].copy()
        B["code"] = B.code.astype(float)
        m = A.merge(B, on=["respondent", "item", "unit"], suffixes=("_A", "_B"))
        if len(m):
            pairs = [[a, b] for a, b in zip(m.code_A, m.code_B)]
            alpha = krippendorff_ordinal(pairs)
            agree = (m.code_A == m.code_B).mean()
            print(f"reliability on {len(m)} double-coded judgements: "
                  f"ordinal alpha = {alpha:.3f}, raw agreement = {agree:.1%}")
            dis = m[m.code_A != m.code_B]
            if len(dis):
                print("\ndisagreements by unit:")
                print(dis.groupby(["item", "unit"]).size()
                      .sort_values(ascending=False).head(10).to_string())
    except FileNotFoundError:
        print("no coding_sheet_B.csv -- skipping reliability")

    # ---- per respondent x fragment
    per = (A.groupby(["respondent", "item"])
             .agg(pts=("code", "sum"), n=("code", "size")).reset_index())
    per["score"] = per.pts / (MAXCODE * per.n)
    W = per.pivot(index="respondent", columns="item", values="score")
    W["BA_open"] = W.mean(axis=1)
    W.round(4).to_csv(f"{OUT}/open_scores_per_respondent.csv")

    print("\nper-fragment mean coverage:")
    for item in RUBRIC:
        if item in W:
            print(f"  {item}: {W[item].mean():.3f}")
    print(f"\nBA_open mean {W.BA_open.mean():.3f}  "
          f"range {W.BA_open.min():.3f}-{W.BA_open.max():.3f}  SD {W.BA_open.std():.3f}")

    # ---- unit difficulty
    U = (A.groupby(["item", "unit"]).code.mean() / MAXCODE).reset_index(name="difficulty")
    U.round(3).to_csv(f"{OUT}/open_unit_difficulty.csv", index=False)
    print("\nhardest units:")
    print(U.sort_values("difficulty").head(8).to_string(index=False))

    # ---- misconception frequency
    mis = []
    for v in A.misconceptions.dropna():
        mis += [t.strip() for t in str(v).split(";") if t.strip()]
    if mis:
        mc = pd.Series(mis).value_counts()
        mc.index = [f"{c} - {MISCONCEPTIONS.get(c, '?')}" for c in mc.index]
        print("\nmisconceptions:")
        print(mc.to_string())

    heatmap(A)


def heatmap(A, fname="fig_open_units.png"):
    items = list(RUBRIC)
    widths = [len(RUBRIC[i]) for i in items]
    fig, axes = plt.subplots(1, len(items), figsize=(14, 6.4),
                             gridspec_kw={"width_ratios": widths})
    cmap = matplotlib.colors.ListedColormap(["#c0392b", "#e8d5a8", "#2e7d5b"])
    for ax, item in zip(axes, items):
        P = (A[A.item == item].pivot(index="respondent", columns="unit", values="code")
             .reindex(columns=[u for u, _ in RUBRIC[item]]))
        ax.imshow(P.values, cmap=cmap, vmin=0, vmax=2, aspect="auto",
                  interpolation="nearest")
        ax.set_xticks(range(P.shape[1]))
        ax.set_xticklabels(P.columns, fontsize=8)
        ax.set_yticks(range(0, P.shape[0], 2))
        ax.set_yticklabels(P.index[::2], fontsize=8)
        ax.set_title(item, fontsize=11, weight="bold")
        for j in range(P.shape[1] + 1):
            ax.axvline(j - .5, color="white", lw=1.2)
        for i in range(P.shape[0] + 1):
            ax.axhline(i - .5, color="white", lw=.5)
        if ax is axes[0]:
            ax.set_ylabel("respondent", fontsize=9)
    h = [matplotlib.patches.Rectangle((0, 0), 1, 1, fc=c)
         for c in ["#2e7d5b", "#e8d5a8", "#c0392b"]]
    fig.legend(h, ["2 explicit", "1 vague", "0 absent/wrong"], loc="lower center",
               ncol=3, frameon=False, fontsize=9, bbox_to_anchor=(.5, -.01))
    fig.suptitle("Open-item semantic unit coverage", fontsize=12)
    fig.tight_layout(rect=[0, .05, 1, .97])
    fig.savefig(f"{OUT}/{fname}", dpi=160)


# def migrate():
#     """Rebuild coding sheets against the current RUBRIC, keeping existing codes."""
#     resp = responses()
#     for rater in ("A", "B"):
#         path = f"{OUT}/coding_sheet_{rater}.csv"
#         try:
#             old = pd.read_csv(path, dtype={"misconceptions": object, "flag": object})
#         except FileNotFoundError:
#             print(f"{path} missing - run init first"); continue
#         old = old.set_index(["respondent", "item", "unit"])

#         rows, kept, added = [], 0, 0
#         for item, units in RUBRIC.items():
#             for r in range(1, len(resp[item]) + 1):
#                 if rater == "B" and r not in RELIABILITY_SAMPLE:
#                     continue
#                 for uid, desc in units:
#                     prev = old.loc[(r, item, uid)] if (r, item, uid) in old.index else None
#                     if prev is not None:
#                         kept += 1
#                     else:
#                         added += 1
#                     rows.append({
#                         "rater": rater, "respondent": r, "item": item, "unit": uid,
#                         "code": "" if prev is None else prev.code,
#                         "unit_desc": desc,                      # always refreshed
#                         "misconceptions": "" if prev is None else prev.misconceptions,
#                         "flag": "" if prev is None else prev.flag,
#                         "response": resp[item][r - 1]})

#         new_keys = {(r["respondent"], r["item"], r["unit"]) for r in rows}
#         dropped = [k for k in old.index if k in old.index and k not in new_keys]
#         coded_dropped = sum(1 for k in dropped if pd.notna(old.loc[k].code)
#                             and str(old.loc[k].code).strip() != "")

#         sheet = pd.DataFrame(rows)
#         if BY_UNIT:
#             sheet = sheet.sort_values(["item", "unit", "respondent"])
#         sheet.to_csv(path.replace(".csv", "_migrated.csv"), index=False)
#         print(f"{rater}: kept {kept}, added {added} blank, dropped {len(dropped)} "
#               f"({coded_dropped} of them already coded)")
#     print("wrote *_migrated.csv - check them, then rename over the originals")

# and register it:
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "init"
    #{"init": init, "score": score, "migrate": migrate}[cmd]()
    {"init": init, "score": score}[cmd]()

if __name__ == "__main__":
    {"init": init, "score": score}[sys.argv[1] if len(sys.argv) > 1 else "init"]()