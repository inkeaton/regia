#!/usr/bin/env python3
"""
Regia questionnaire -- scoring of the CLOSED (select-all-that-apply) items.

Balanced accuracy + Youden's J, per respondent and per item, with BCa
bootstrap CIs, plus the option-selection heat-map.

Requires: pandas, numpy, scipy, matplotlib, openpyxl
Usage:    python3 score_closed.py
"""
import collections
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.stats import bootstrap

# ---------------------------------------------------------------- config ----
SRC = "data.xlsx"
KEY = "answer_key.csv"      # columns: item, option_id, is_correct, option_text
OUT = "."                   # output directory

# zero-based column index of each closed item in the export
COLS = {"C1": 8, "C2": 11, "C3": 12}

# Options whose text never appears at the start of a response and always
# follows the same predecessor cannot be detected automatically (they have no
# varying context to learn from).  List them here verbatim to force a boundary.
FORCE = {
    "C3": ["It states that the attribute PRIORITY associated with the "
           "assassin becomes 9 when the assassin is spotted."],
}

# ------------------------------------------------------- option recovery ----
def decompose(df, col, item):
    """Split each response into whole options.

    The export joins the selected options with ';' but the option texts
    themselves contain ';', so a naive split invents phantom options.  We infer
    the real boundaries from context: a fragment begins a new option if it ever
    appears first in some response, or if it appears after two different
    predecessors across respondents.
    """
    seqs = []
    for v in df.iloc[:, col].fillna(""):
        s = str(v)
        s = s[:-1] if s.endswith(";") else s
        seqs.append([] if s == "" else s.split(";"))

    preds = collections.defaultdict(set)
    for toks in seqs:
        for i, t in enumerate(toks):
            preds[t].add(None if i == 0 else toks[i - 1])
    starts = {t for t, p in preds.items() if (None in p) or len(p) > 1}
    starts |= set(FORCE.get(item, ()))

    out = []
    for toks in seqs:
        sel, cur = [], []
        for t in toks:
            if t in starts and cur:
                sel.append(";".join(cur).strip())
                cur = []
            cur.append(t)
        if cur:
            sel.append(";".join(cur).strip())
        out.append(set(sel))
    return out


def norm(s):
    """Whitespace-insensitive comparison, so the key file can be re-typed."""
    return " ".join(str(s).split())


# ------------------------------------------------------------- scoring ------
def main():
    df = pd.read_excel(SRC)
    key = pd.read_csv(KEY)
    key["_norm"] = key.option_text.map(norm)

    # --- binary response matrix, driven by the KEY (so options that nobody
    # --- selected still appear, with ticked = 0 for every respondent)
    rows, unmatched = [], []
    for item, col in COLS.items():
        ko = key[key.item == item]
        sel = decompose(df, col, item)
        seen = {norm(x) for s in sel for x in s}
        unmatched += [x for x in seen if x not in set(ko._norm)]
        for r, chosen in enumerate(sel, 1):
            chosen_n = {norm(x) for x in chosen}
            for _, o in ko.iterrows():
                rows.append({"respondent": r, "item": item,
                             "option_id": o.option_id,
                             "is_correct": int(o.is_correct),
                             "ticked": int(o._norm in chosen_n)})
    if unmatched:
        print("WARNING - selected text not found in key (check for typos):")
        for u in set(unmatched):
            print("   ", u[:120])

    M = pd.DataFrame(rows)
    M.to_csv(f"{OUT}/closed_response_matrix.csv", index=False)

    # --- sensitivity / specificity / balanced accuracy / Youden's J
    rec = []
    for (r, item), g in M.groupby(["respondent", "item"]):
        P, N = g[g.is_correct == 1], g[g.is_correct == 0]
        sens = P.ticked.mean()
        spec = 1 - N.ticked.mean()
        rec.append({"respondent": r, "item": item,
                    "n_correct": len(P), "n_distractor": len(N),
                    "hits": int(P.ticked.sum()),
                    "false_alarms": int(N.ticked.sum()),
                    "sensitivity": sens, "specificity": spec,
                    "BA": (sens + spec) / 2, "J": sens + spec - 1})
    S = pd.DataFrame(rec)

    W = S.pivot(index="respondent", columns="item", values="BA")
    W["BA_closed"] = W[list(COLS)].mean(axis=1)
    W["J_closed"] = 2 * W.BA_closed - 1
    W.round(4).to_csv(f"{OUT}/closed_scores_per_respondent.csv")
    S.round(4).to_csv(f"{OUT}/closed_scores_per_item.csv", index=False)

    def ci(x):
        x = np.asarray(x, float)
        if np.ptp(x) == 0:
            return x[0], x[0]
        r = bootstrap((x,), np.mean, confidence_level=.95,
                      n_resamples=10000, method="BCa", random_state=0)
        return r.confidence_interval.low, r.confidence_interval.high

    print(f'\n{"item":5s} {"key/dis":8s} {"sens":>6s} {"spec":>6s} '
          f'{"BA":>6s} {"95% BCa CI":>16s} {"J":>7s}')
    for item in COLS:
        g = S[S.item == item]
        lo, hi = ci(g.BA)
        print(f"{item:5s} {g.n_correct.iloc[0]}/{g.n_distractor.iloc[0]:<6d} "
              f"{g.sensitivity.mean():6.3f} {g.specificity.mean():6.3f} "
              f"{g.BA.mean():6.3f} [{lo:5.3f}, {hi:5.3f}] {g.J.mean():7.3f}")
    lo, hi = ci(W.BA_closed)
    print(f"\nOVERALL  BA = {W.BA_closed.mean():.3f}  95% BCa CI [{lo:.3f}, {hi:.3f}]"
          f"   J = {2 * W.BA_closed.mean() - 1:.3f}")
    print(f"per-respondent BA: min {W.BA_closed.min():.3f}  max {W.BA_closed.max():.3f}  "
          f"SD {W.BA_closed.std():.3f}")

    plot(M, key)
    return M, S, W


# ---------------------------------------------------------------- figure ----
def plot(M, key):
    items = list(COLS)
    widths = [M[M.item == i].option_id.nunique() for i in items]
    fig, axes = plt.subplots(1, len(items), figsize=(13, 6.2),
                             gridspec_kw={"width_ratios": widths})
    corr = key.set_index("option_id").is_correct
    for ax, item in zip(axes, items):
        P = M[M.item == item].pivot(index="respondent", columns="option_id",
                                    values="ticked")
        cols = sorted(P.columns, key=lambda c: (-corr[c], c))
        P = P[cols]
        grid = np.zeros(P.shape)
        for j, c in enumerate(cols):
            grid[:, j] = np.where(P[c] == 1, 1 if corr[c] == 1 else 2,
                                  3 if corr[c] == 1 else 0)
        cmap = matplotlib.colors.ListedColormap(
            ["#f2f2f0", "#2e7d5b", "#c0392b", "#f6d6d0"])
        ax.imshow(grid, cmap=cmap, vmin=0, vmax=3, aspect="auto",
                  interpolation="nearest")
        ax.set_xticks(range(len(cols)))
        ax.set_xticklabels([c.split("_")[1] +
                            ("\n(key)" if corr[c] == 1 else "\n(distr.)")
                            for c in cols], fontsize=8)
        ax.set_yticks(range(0, len(P), 2))
        ax.set_yticklabels(range(1, len(P) + 1, 2), fontsize=8)
        ax.set_title(item, fontsize=11, weight="bold")
        for j in range(len(cols) + 1):
            ax.axvline(j - .5, color="white", lw=1.5)
        for i in range(len(P) + 1):
            ax.axhline(i - .5, color="white", lw=.5)
        if ax is axes[0]:
            ax.set_ylabel("respondent", fontsize=9)
    h = [Rectangle((0, 0), 1, 1, fc=c)
         for c in ["#2e7d5b", "#f6d6d0", "#c0392b", "#f2f2f0"]]
    fig.legend(h, ["hit (key ticked)", "miss (key left)",
                   "false alarm", "correct rejection"],
               loc="lower center", ncol=4, frameon=False, fontsize=9,
               bbox_to_anchor=(.5, -.01))
    fig.suptitle("Closed-item option selection", fontsize=12)
    fig.tight_layout(rect=[0, .05, 1, .97])
    fig.savefig(f"{OUT}/fig_closed_selection.png", dpi=160)


if __name__ == "__main__":
    main()