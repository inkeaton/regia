"""
Generates the two combined benchmark figures for the Transpiler Benchmarks
results subsection:

  Figure 1 (fig_compile_time_vs_output_loc.png):
      Compilation time vs. generated AgentSpeak output (log-log), every
      swept dimension overlaid on one axis. A straight line on log-log
      axes demonstrates linear growth in compilation cost regardless of
      which construct is being scaled.

  Figure 2 (fig_expansion_ratio.png):
      Expansion ratio (output LoC / input LoC) vs. the fraction of each
      dimension's own tested range, every swept dimension overlaid on one
      axis. This groups the eight dimensions into three visible families:
      multiplying constructs (ratio climbs), additive constructs (ratio
      flattens near a constant), and sub-unity constructs (ratio falls
      below 1).

Input: the eight scale_*.csv files produced by the benchmark tool, expected
in the same directory as this script (or pass a directory as argv[1]).
Output: two PNGs written to the given output directory (argv[2], default
"./figures").
"""

import csv
import glob
import os
import statistics
import sys
from collections import defaultdict

import matplotlib.pyplot as plt

# Maps each CSV file (by suffix) to the column it sweeps and a short,
# human-readable label used in legends and captions.
DIMENSIONS = {
    "scale_roles.csv": ("n_roles", "Roles"),
    "scale_phases.csv": ("n_phases", "Phases"),
    "scale_playbooks.csv": ("n_playbooks", "Playbooks"),
    "scale_plans.csv": ("n_plans_per_playbook", "Plans per Playbook"),
    "scale_branches.csv": ("n_branches_per_plan", "Branches per Plan"),
    "scale_stmts.csv": ("n_stmts_per_branch", "Statements per Branch"),
    "scale_subplot_breadth.csv": ("n_subplot_breadth", "Subplot Breadth"),
    "scale_subplot_depth.csv": ("n_subplot_depth", "Subplot Depth"),
}

# Consistent colour/marker per dimension across both figures.
STYLES = {
    "Roles": dict(color="#1f77b4", marker="o"),
    "Phases": dict(color="#ff7f0e", marker="s"),
    "Playbooks": dict(color="#2ca02c", marker="^"),
    "Plans per Playbook": dict(color="#d62728", marker="D"),
    "Branches per Plan": dict(color="#9467bd", marker="v"),
    "Statements per Branch": dict(color="#8c564b", marker="P"),
    "Subplot Breadth": dict(color="#e377c2", marker="X"),
    "Subplot Depth": dict(color="#17becf", marker="*"),
}


def load_grouped(path, sweep_col):
    """Group rows by the swept parameter's value, returning per-value means."""
    groups = defaultdict(list)
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            groups[int(row[sweep_col])].append(row)

    results = []
    for k in sorted(groups):
        rows = groups[k]
        input_loc = int(rows[0]["input_loc"])
        output_loc = int(rows[0]["output_loc_total"])
        loc_ratio = output_loc / input_loc
        compile_time = statistics.mean(float(r["compile_time_s"]) for r in rows)
        results.append(
            dict(
                sweep_value=k,
                input_loc=input_loc,
                output_loc=output_loc,
                loc_ratio=loc_ratio,
                compile_time_s=compile_time,
            )
        )
    return results


def load_all(data_dir):
    data = {}
    for fname, (sweep_col, label) in DIMENSIONS.items():
        path = os.path.join(data_dir, fname)
        if not os.path.exists(path):
            print(f"warning: {path} not found, skipping {label}", file=sys.stderr)
            continue
        data[label] = load_grouped(path, sweep_col)
    return data


def plot_compile_time_vs_output_loc(data, out_path):
    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    for label, rows in data.items():
        style = STYLES[label]
        xs = [r["output_loc"] for r in rows]
        ys = [r["compile_time_s"] * 1000 for r in rows]  # ms for readability
        ax.plot(
            xs,
            ys,
            label=label,
            linewidth=1.6,
            markersize=6,
            **style,
        )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Generated AgentSpeak (output lines of code, log scale)")
    ax.set_ylabel("Compilation time (milliseconds, log scale)")
    ax.set_title("Compilation time versus generated output size, by scaled dimension")
    ax.grid(True, which="both", linestyle="--", alpha=0.4)
    ax.legend(loc="upper left", fontsize=8, framealpha=0.9)

    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def plot_expansion_ratio(data, out_path):
    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    for label, rows in data.items():
        style = STYLES[label]
        max_sweep = max(r["sweep_value"] for r in rows) or 1
        xs = [r["sweep_value"] / max_sweep for r in rows]
        ys = [r["loc_ratio"] for r in rows]
        ax.plot(
            xs,
            ys,
            label=label,
            linewidth=1.6,
            markersize=6,
            **style,
        )

    ax.axhline(1.0, color="black", linewidth=0.8, linestyle=":")
    ax.set_xlabel("Dimension value, as a fraction of its own maximum tested value")
    ax.set_ylabel("Expansion ratio (output LoC / input LoC)")
    ax.set_title("Code expansion ratio versus scaled dimension, normalised range")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="upper left", fontsize=8, framealpha=0.9)

    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def main():
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "./figures"
    os.makedirs(out_dir, exist_ok=True)

    data = load_all(data_dir)
    if not data:
        print("error: no benchmark CSVs found", file=sys.stderr)
        sys.exit(1)

    plot_compile_time_vs_output_loc(
        data, os.path.join(out_dir, "fig_compile_time_vs_output_loc.png")
    )
    plot_expansion_ratio(data, os.path.join(out_dir, "fig_expansion_ratio.png"))

    print(f"Wrote figures to {out_dir}/")


if __name__ == "__main__":
    main()
