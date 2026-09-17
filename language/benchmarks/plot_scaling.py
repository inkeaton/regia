#!/usr/bin/env python3
"""
Generates the two single-dimension scaling figures for Section 7.2.2.

    compile_time_vs_input_loc.png   -- the eight sweeps fall together
    compile_time_vs_output_loc.png  -- the eight sweeps separate

Both are produced here so that the adjacent figures share styling, since the
contrast between them is the point being made.

Usage:  python3 plot_scaling.py [DATA_DIR] [OUT_DIR]
"""

import csv
import statistics
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DATA_DIR = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT_DIR = Path(sys.argv[2] if len(sys.argv) > 2 else ".")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# (csv filename, column holding the swept parameter, legend label)
SWEEPS = [
    ("scale_roles.csv",           "n_roles",              "Roles"),
    ("scale_phases.csv",          "n_phases",             "Phases"),
    ("scale_playbooks.csv",       "n_playbooks",          "Playbooks"),
    ("scale_plans.csv",           "n_plans_per_playbook", "Plans per Playbook"),
    ("scale_branches.csv",        "n_branches_per_plan",  "Branches per Plan"),
    ("scale_stmts.csv",           "n_stmts_per_branch",   "Statements per Branch"),
    ("scale_subplot_breadth.csv", "n_subplot_breadth",    "Subplot Breadth"),
    ("scale_subplot_depth.csv",   "n_subplot_depth",      "Subplot Depth"),
]

MARKERS = ["o", "s", "D", "^", "v", "P", "X", "*"]
COLORS = plt.get_cmap("tab10").colors


def load(filename, param):
    """Return (input_loc, output_loc, mean_compile_ms) per configuration point."""
    groups = {}
    with open(DATA_DIR / filename, newline="") as fh:
        for row in csv.DictReader(fh):
            groups.setdefault(int(row[param]), []).append(row)
    points = []
    for key in sorted(groups):
        runs = groups[key]
        points.append((
            int(runs[0]["input_loc"]),
            int(runs[0]["output_loc_total"]),
            statistics.mean(float(r["compile_time_s"]) for r in runs) * 1000.0,
        ))
    return points


def fit_loglog(xs, ys):
    """Least-squares fit of log(y) against log(x); returns (exponent, r_squared)."""
    lx, ly = np.log(np.asarray(xs, float)), np.log(np.asarray(ys, float))
    slope, intercept = np.polyfit(lx, ly, 1)
    resid = ly - (intercept + slope * lx)
    r2 = 1.0 - resid.var() / ly.var()
    return slope, intercept, r2


def render(index, xlabel, title, filename, show_fit):
    fig, ax = plt.subplots(figsize=(8.4, 5.6), dpi=200)

    pooled_x, pooled_y = [], []
    for i, (filename_csv, param, label) in enumerate(SWEEPS):
        points = load(filename_csv, param)
        xs = [p[index] for p in points]
        ys = [p[2] for p in points]
        pooled_x.extend(xs)
        pooled_y.extend(ys)
        ax.plot(xs, ys,
                marker=MARKERS[i], markersize=6, linewidth=1.6,
                color=COLORS[i], label=label, zorder=3)

    slope, intercept, r2 = fit_loglog(pooled_x, pooled_y)

    if show_fit:
        grid = np.linspace(np.log(min(pooled_x)), np.log(max(pooled_x)), 100)
        ax.plot(np.exp(grid), np.exp(intercept + slope * grid),
                linestyle="--", linewidth=1.5, color="0.35", zorder=2,
                label=f"Pooled fit (exponent {slope:.2f}, $R^2$ = {r2:.2f})")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel("Compilation time (milliseconds, log scale)", fontsize=11)
    ax.set_title(title, fontsize=13, pad=12)
    ax.grid(True, which="major", linestyle="--", linewidth=0.6, color="0.85", zorder=0)
    ax.grid(True, which="minor", linestyle=":", linewidth=0.4, color="0.92", zorder=0)
    ax.set_axisbelow(True)
    ax.legend(fontsize=8.5, loc="upper left", framealpha=0.95)
    fig.tight_layout()
    fig.savefig(OUT_DIR / filename, bbox_inches="tight")
    plt.close(fig)

    print(f"{filename}: exponent {slope:.3f}, R^2 {r2:.4f}")


render(index=0,
       xlabel="Regia source (input lines of code, log scale)",
       title="Compilation cost against source size, for each construct scaled alone",
       filename="compile_time_vs_input_loc.png",
       show_fit=True)

render(index=1,
       xlabel="Generated AgentSpeak (output lines of code, log scale)",
       title="The same measurements against generated output size",
       filename="compile_time_vs_output_loc.png",
       show_fit=True)
