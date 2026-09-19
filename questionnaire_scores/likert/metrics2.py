#!/usr/bin/env python3
"""
Regia questionnaire -- LIKERT block (15 perceived-quality items).

Non-parametric treatment throughout:
  * "I do not know" is treated as MISSING, never as Neutral, and its rate is
    reported as a separate indicator.
  * median / IQR, net agreement (%agree - %disagree) with a percentile
    bootstrap CI, top-2-box, and a Holm-corrected Wilcoxon signed-rank test
    against the neutral midpoint.
  * diverging stacked bar chart, items ordered by net agreement.

Requires: pandas, numpy, scipy, matplotlib, openpyxl
Usage:    python3 score_likert.py
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.stats import wilcoxon, norm as znorm

SRC = "data.xlsx"
OUT = "."
FIRST, LAST = 16, 31          # Likert columns are df.columns[16:31]
DK = "I do not know"
SCALE = {"Strongly Disagree": 1, "Disagree": 2, "Neutral": 3,
         "Agree": 4, "Strongly Agree": 5}
LEVELS = list(SCALE)
DK_EXCLUDE = 0.50             # drop a respondent from aggregates above this DK rate

LABEL = {                     # (short label, AgentDSM-Eval characteristic, measure no.)
    1:  ("completeness",              "Functional Suitability", 1),
    2:  ("appropriateness",           "Functional Suitability", 2),
    3:  ("comprehensibility",         "Usability",              3),
    4:  ("learnability",              "Usability",              4),
    5:  ("efficiency (steps)",        "Usability",              5),
    6:  ("likeability",               "Usability",              6),
    7:  ("error protection",          "Reliability",           10),
    8:  ("correctness",               "Reliability",           11),
    9:  ("design-to-program",         "Expressiveness",        12),
    10: ("uniqueness",                "Expressiveness",        13),
    11: ("orthogonality",             "Expressiveness",        14),
    12: ("necessity",                 "Expressiveness",        15),
    13: ("conflict-freedom",          "Expressiveness",        16),
    14: ("methodology fit",           "Compatibility",         18),
    15: ("MAS structural power",      "MAS Development",       23),
}


def load():
    df = pd.read_excel(SRC)
    cols = list(df.columns[FIRST:LAST])
    L = df[cols].copy()
    L.columns = [f"L{i:02d}" for i in range(1, len(cols) + 1)]
    L.index = range(1, len(L) + 1)
    L.index.name = "respondent"
    texts = {f"L{i:02d}": t for i, t in enumerate(cols, 1)}
    return L, texts


def net_ci(codes, n_boot=10000, seed=0):
    """Percentile bootstrap CI for net agreement, resampling RESPONDENTS."""
    x = np.asarray(codes, float)
    if len(x) == 0:
        return np.nan, np.nan
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(n_boot, len(x)))
    b = x[idx]
    net = ((b >= 4).mean(1) - (b <= 2).mean(1)) * 100
    return np.percentile(net, 2.5), np.percentile(net, 97.5)


def analyse(L, tag=""):
    rows = []
    for j, item in enumerate(L.columns, 1):
        s = L[item]
        counts = {lv: int((s == lv).sum()) for lv in LEVELS}
        dk = int((s == DK).sum())
        codes = s[s.isin(LEVELS)].map(SCALE).astype(float).values
        n = len(codes)
        net = ((codes >= 4).mean() - (codes <= 2).mean()) * 100 if n else np.nan
        lo, hi = net_ci(codes)
        # Wilcoxon signed-rank vs the neutral midpoint (3)
        d = codes - 3
        if np.any(d != 0):
            st, p = wilcoxon(d, zero_method="wilcox", alternative="two-sided")
            z = abs(znorm.ppf(p / 2))
            r = z / np.sqrt(n)
        else:
            p, r = 1.0, 0.0
        rows.append({"item": item, "label": LABEL[j][0],
                     "construct": LABEL[j][1], **counts,
                     "DK": dk, "n_valid": n,
                     "median": float(np.median(codes)) if n else np.nan,
                     "q1": float(np.percentile(codes, 25)) if n else np.nan,
                     "q3": float(np.percentile(codes, 75)) if n else np.nan,
                     "top2box": (codes >= 4).mean() * 100 if n else np.nan,
                     "net_agreement": net, "net_lo": lo, "net_hi": hi,
                     "p_wilcoxon": p, "effect_r": r})
    T = pd.DataFrame(rows)
    # Holm correction across the 15 items
    o = T.p_wilcoxon.values.argsort()
    m, adj, run = len(T), np.empty(len(T)), 0.0
    for k, i in enumerate(o):
        run = max(run, (m - k) * T.p_wilcoxon.values[i])
        adj[i] = min(run, 1.0)
    T["p_holm"] = adj
    T = T.sort_values("net_agreement", ascending=False).reset_index(drop=True)
    T.to_csv(f"{OUT}/likert_item_stats{tag}.csv", index=False)
    return T


def diverging_plot(T, fname="fig_likert_diverging.png"):
    T = T.sort_values("net_agreement")
    colors = ["#a01d28", "#d98a86", "#e8e6e1", "#7fb79a", "#2e7d5b"]
    fig, ax = plt.subplots(figsize=(11.5, 7.2))
    for i, (_, r) in enumerate(T.iterrows()):
        n = r.n_valid
        pct = [r[lv] / n * 100 for lv in LEVELS]
        left = -(pct[0] + pct[1] + pct[2] / 2)   # centre the bar on Neutral
        for k, lv in enumerate(LEVELS):
            ax.barh(i, pct[k], left=left, color=colors[k],
                    edgecolor="white", lw=.8, height=.72)
            left += pct[k]
        ax.text(left + 3, i, f"{r.net_agreement:+.0f}", va="center",
                fontsize=8.5, color="#333")
        if r.DK:
            ax.text(118, i, f"DK {int(r.DK)}", va="center", fontsize=8,
                    color="#888")
    ax.axvline(0, color="#444", lw=1)
    ax.set_yticks(np.arange(len(T)))
    ax.set_yticklabels([f'{r.label}  ({r["item"]})' for _, r in T.iterrows()],
                       fontsize=9)
    ax.set_xlim(-80, 132)
    ax.set_xticks([-75, -50, -25, 0, 25, 50, 75, 100])
    ax.set_xticklabels(["75%", "50%", "25%", "0", "25%", "50%", "75%", "100%"],
                       fontsize=8)
    ax.set_xlabel("percentage of valid (non-DK) responses", fontsize=9)
    ax.set_title("Perceived quality of Regia — 15 items, ordered by net agreement\n"
                 "(bars centred on Neutral; net agreement %A − %D at right)",
                 fontsize=11)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    h = [Rectangle((0, 0), 1, 1, fc=c) for c in colors]
    ax.legend(h, LEVELS, loc="lower center", bbox_to_anchor=(.5, -.16),
              ncol=5, frameon=False, fontsize=8.5)
    fig.tight_layout()
    fig.savefig(f"{OUT}/{fname}", dpi=160, bbox_inches="tight")


def main():
    L, texts = load()
    dk_rate = (L == DK).mean(axis=1)
    dropped = dk_rate[dk_rate > DK_EXCLUDE].index.tolist()
    print(f"DK rate > {DK_EXCLUDE:.0%} -> respondents excluded from the "
          f"sensitivity analysis: {dropped}")

    T = analyse(L)
    show = ["item", "label", "n_valid", "DK", "median", "q1", "q3", "top2box",
            "net_agreement", "net_lo", "net_hi", "p_holm", "effect_r"]
    print("\n=== all respondents (available-case) ===")
    print(T[show].round(2).to_string(index=False))

    if dropped:
        T2 = analyse(L.drop(index=dropped), tag="_sensitivity")
        merged = T[["item", "net_agreement"]].merge(
            T2[["item", "net_agreement"]], on="item", suffixes=("_all", "_excl"))
        merged["delta"] = merged.net_agreement_excl - merged.net_agreement_all
        print(f"\n=== sensitivity: net agreement shift excluding {dropped} ===")
        print(merged.round(2).to_string(index=False))

    # per-respondent scores for the later correlation analysis
    codes = L.where(L.isin(LEVELS)).replace(SCALE).astype(float)
    per = pd.DataFrame({
        "perceived_overall": codes.mean(axis=1),
        "perceived_comprehension": codes[["L03", "L04"]].mean(axis=1),
        "n_answered": codes.notna().sum(axis=1),
        "dk_count": (L == DK).sum(axis=1)})
    per.round(4).to_csv(f"{OUT}/likert_per_respondent.csv")
    print("\nper-respondent perceived_overall: "
          f"mean {per.perceived_overall.mean():.2f}, "
          f"range {per.perceived_overall.min():.2f}-{per.perceived_overall.max():.2f}")

    diverging_plot(T)
    pd.Series(texts).to_csv(f"{OUT}/likert_codebook.csv", header=["item_text"])
    print("\nwrote likert_item_stats.csv, likert_per_respondent.csv, "
          "likert_codebook.csv, fig_likert_diverging.png")


if __name__ == "__main__":
    main()