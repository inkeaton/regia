#!/usr/bin/env python3
"""
Draws the Section 8.3 figures from the CSVs written by compute_metrics.py.

    comprehension_by_item.png   every respondent's score on the seven comprehension
                                items, in questionnaire order, split Playbook / Plot
    closed_options.png          share of respondents selecting each closed-question
                                statement; long bars on false statements are misconceptions
    open_units.png              mean rubric score per unit of each open question
    likert_diverging.png        the fifteen quality measures as diverging stacked bars
    calibration.png             self-rated comprehensibility against measured comprehension
    generation_behaviours.png   coverage of each specified behaviour in the generation task

Styling matches plot_scaling.py and plot_interactions.py.

Usage:  python3 make_figures.py [RESULTS_DIR] [FIG_DIR]
"""

import sys
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import pandas as pd

RES = Path(sys.argv[1] if len(sys.argv) > 1 else "results")
FIG = Path(sys.argv[2] if len(sys.argv) > 2 else "figures")
FIG.mkdir(parents=True, exist_ok=True)

C = plt.get_cmap("tab10").colors
DPI = 200

# Okabe-Ito palette: colour-blind safe under all common forms of colour vision
# deficiency, and never pairs red with green. Used wherever a figure encodes a
# correct/incorrect or full/partial/none distinction.
OI_BLUE       = "#0072B2"
OI_SKY_BLUE   = "#56B4E9"
OI_ORANGE     = "#E69F00"
OI_VERMILLION = "#D55E00"
OI_GREY       = "0.80"

# Short labels for the fifteen closed-question statements (T = true, F = false).
OPTION_LABELS = {
    "C1_o1": "Local-level plan within the Playbook",
    "C1_o2": "TEMPER-gated reaction: complain and signal, else toast",
    "C1_o3": "PRIORITY, TEMPER, EFFECTS read as increments",
    "C1_o4": "Static priority; TEMPER gates adoption; EFFECTS a side effect",
    "C1_o5": "A global Plot narrative",
    "C2_o1": "A plan within a RoyalBanquet Playbook",
    "C2_o2": "Phases run in their declared order",
    "C2_o3": "A Plot, describing a global-level narrative",
    "C2_o4": "Exactly two agents exist, named Host and Guest",
    "C2_o5": "Starts in reception; later phases set by TRANSITION",
    "C3_o1": "PLOT is a phase",
    "C3_o2": "The assassin's priority becomes 9",
    "C3_o3": "WORLD is a specific agent",
    "C3_o4": "Host is one specific agent",
    "C3_o5": "In any phase: world locks doors, a Host calls guards, Plot ends",
}


def style(ax, title, xlabel=None, ylabel=None):
    ax.set_title(title, fontsize=13, pad=12)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(True, linestyle="--", linewidth=0.6, color="0.85", zorder=0)
    ax.set_axisbelow(True)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(FIG / name, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  {name}")


print(f"Writing figures to {FIG.resolve()}")

# --- 1. Comprehension by item ------------------------------------------------

summary = pd.read_csv(RES / "items_summary.csv")
closed = pd.read_csv(RES / "closed_items.csv")
open_items = pd.read_csv(RES / "open_items.csv")

rng = np.random.default_rng(7)          # fixed seed: identical jitter on every run
fig, ax = plt.subplots(figsize=(9.5, 5.6))
for x, s in enumerate(summary.itertuples()):
    if s.type == "closed":
        ys = closed.loc[closed["item"] == s.item, "plus_minus"].to_numpy()
        colour, marker = C[0], "o"
    else:
        ys = open_items.loc[open_items["item"] == s.item, "rubric_score"].dropna().to_numpy()
        colour, marker = C[1], "s"
    ax.scatter(x + rng.uniform(-0.18, 0.18, len(ys)), ys, s=26, alpha=0.55,
               color=colour, marker=marker, edgecolor="none", zorder=3)
    ax.plot([x - 0.28, x + 0.28], [np.median(ys)] * 2, color="0.15", linewidth=2.2, zorder=4)

ax.axvline(2.5, color="0.6", linewidth=1)
ax.axhline(0, color="0.6", linewidth=0.8, linestyle=":")
for xpos, label in ((1.0, "Playbook level"), (4.5, "Plot level")):
    ax.text(xpos, 1.14, label, ha="center", fontsize=10, color="0.35")
ax.set_xticks(range(len(summary)))
ax.set_xticklabels([f"{s.question}\n({s.item})" for s in summary.itertuples()])
ax.set_ylim(-1.15, 1.22)
ax.scatter([], [], color=C[0], marker="o", label="Multi-select item: normalised plus/minus (0 = all or none selected)")
ax.scatter([], [], color=C[1], marker="s", label="Explanation item: rubric score (0 = nothing covered)")
ax.plot([], [], color="0.15", linewidth=2.2, label="Median")
ax.legend(fontsize=8.5, loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3, frameon=False)
style(ax, "Comprehension of each item, in questionnaire order", ylabel="Score")
save(fig, "comprehension_by_item.png")

# --- 2. Closed options: selection rates ------------------------------------

opts = pd.read_csv(RES / "closed_options.csv")
fig, ax = plt.subplots(figsize=(9.5, 7.2))
y, ticks, labels = 0, [], []
for item, grp in opts.groupby("item", sort=True):
    for o in grp.itertuples():
        colour = OI_BLUE if o.is_correct else OI_ORANGE
        ax.barh(y, o.selection_rate, color=colour, height=0.72, zorder=3)
        ax.text(o.selection_rate + 0.01, y, f"{100 * o.selection_rate:.0f}%", va="center", fontsize=8.5)
        ticks.append(y)
        labels.append(f"{o.option_id}  {'T' if o.is_correct else 'F'}  {OPTION_LABELS.get(o.option_id, '')}")
        y += 1
    y += 0.8
ax.set_yticks(ticks)
ax.set_yticklabels(labels, fontsize=8.5)
ax.invert_yaxis()
ax.set_xlim(0, 1.1)
ax.legend(handles=[Patch(color=OI_BLUE, label="True statement"),
                   Patch(color=OI_ORANGE, label="False statement")],
          fontsize=8.5, loc="upper center", bbox_to_anchor=(0.4, -0.08), ncol=2, frameon=False)
style(ax, "Closed questions: share of respondents selecting each statement",
      xlabel="Share of respondents selecting the statement")
save(fig, "closed_options.png")

# --- 3. Open rubric units ----------------------------------------------------

units = pd.read_csv(RES / "open_units.csv")
fig, ax = plt.subplots(figsize=(9.5, 8.4))
y, ticks, labels = 0, [], []
for i, (item, grp) in enumerate(units.groupby("item", sort=True)):
    for u in grp.itertuples():
        ax.barh(y, u.mean_proportion, color=C[i], height=0.72, zorder=3)
        ticks.append(y)
        labels.append(f"{u.item} {u.unit}  " + textwrap.shorten(u.unit_desc, 58, placeholder="..."))
        y += 1
    y += 0.8
ax.set_yticks(ticks)
ax.set_yticklabels(labels, fontsize=8)
ax.invert_yaxis()
ax.set_xlim(0, 1.05)
style(ax, "Open questions: mean coverage of each rubric unit",
      xlabel="Mean rubric score, as a proportion of the maximum")
save(fig, "open_units.png")

# --- 4. Likert, diverging stacked bars ---------------------------------------

lik = pd.read_csv(RES / "likert_items.csv")
levels = ["strongly_disagree", "disagree", "neutral", "agree", "strongly_agree"]
colours = ["#b2182b", "#ef8a62", "#bdbdbd", "#67a9cf", "#2166ac"]
names = ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]

fig, ax = plt.subplots(figsize=(10, 6.6))
for i, l in enumerate(lik.itertuples()):
    shares = np.array([getattr(l, f"n_{lv}") for lv in levels], float) / l.n_valid
    left = -(shares[0] + shares[1] + shares[2] / 2)      # centre the neutral share on zero
    for share, colour in zip(shares, colours):
        ax.barh(i, share, left=left, color=colour, height=0.72, zorder=3)
        left += share
    ax.text(1.02, i, f"DK {l.n_dont_know}", va="center", fontsize=8, color="0.4")
ax.set_yticks(range(len(lik)))
ax.set_yticklabels([f"{l.measure}. {l.label}" for l in lik.itertuples()], fontsize=9)
ax.invert_yaxis()
ax.axvline(0, color="0.3", linewidth=0.9)
ax.set_xlim(-1, 1.12)
ax.set_xticks(np.linspace(-1, 1, 5))
ax.set_xticklabels(["100%", "50%", "0", "50%", "100%"])
ax.legend(handles=[Patch(color=c, label=n) for c, n in zip(colours, names)],
          fontsize=8, loc="upper center", bbox_to_anchor=(0.45, -0.09), ncol=5, frameon=False)
style(ax, "Quality measures adapted from AgentDSM-Eval",
      xlabel="Share of valid responses; \"I do not know\" excluded and counted at right")
save(fig, "likert_diverging.png")

# --- 5. Calibration ---------------------------------------------------------

resp = pd.read_csv(RES / "respondents.csv")
pair = resp[["self_rated_comprehensibility", "comprehension"]].dropna()
from scipy.stats import spearmanr
rho = spearmanr(pair.iloc[:, 0], pair.iloc[:, 1]).statistic

fig, ax = plt.subplots(figsize=(7.4, 5.4))
ax.scatter(pair["self_rated_comprehensibility"] + rng.uniform(-0.12, 0.12, len(pair)),
           pair["comprehension"], s=42, color=C[0], alpha=0.75, edgecolor="white", zorder=3)
ax.set_xticks(range(1, 6))
ax.set_xticklabels(["Strongly\ndisagree", "Disagree", "Neutral", "Agree", "Strongly\nagree"])
ax.set_xlim(0.5, 5.5)
ax.text(0.03, 0.05, f"Spearman $\\rho$ = {rho:.2f}, n = {len(pair)}",
        transform=ax.transAxes, fontsize=10)
style(ax, "Perceived against measured comprehension",
      xlabel="\"The effort required to understand Regia is small\"",
      ylabel="Measured comprehension")
save(fig, "calibration.png")

# --- 6. Generation task behaviours ------------------------------------------

beh = pd.read_csv(RES / "generation_behaviours.csv")
cols = [("n2", "Implemented in full", OI_BLUE), ("n1", "Implemented in part", OI_SKY_BLUE),
        ("n0", "Attempted, incorrect", OI_VERMILLION), ("not_attempted", "Not attempted", OI_GREY)]
fig, ax = plt.subplots(figsize=(10, 6.8))
for i, b in enumerate(beh.itertuples()):
    left = 0
    for field, _, colour in cols:
        v = getattr(b, field)
        ax.barh(i, v, left=left, color=colour, height=0.72, zorder=3)
        left += v
ax.set_yticks(range(len(beh)))
ax.set_yticklabels([f"{b.behaviour}  " + textwrap.shorten(b.desc, 60, placeholder="...")
                    for b in beh.itertuples()], fontsize=8.5)
ax.invert_yaxis()
n = int(beh["n"].iloc[0])
ax.set_xlim(0, n)
ax.set_xticks(range(n + 1))
ax.legend(handles=[Patch(color=colour, label=name) for _, name, colour in cols],
          fontsize=8.5, loc="upper center", bbox_to_anchor=(0.4, -0.09), ncol=4, frameon=False)
style(ax, f"Generation task: coverage of each specified behaviour (n = {n}, self-selected)",
      xlabel="Respondents")
save(fig, "generation_behaviours.png")