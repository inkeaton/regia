"""
Scaling fits and figures for Section 7.2 of the thesis.

Reads the CSVs written by `python -m benchmarks run` (one directory per suite,
<results>/<suite>/<suite>.csv, several timed runs per configuration), averages
the runs of each configuration, and fits two models of compilation time T
against size S, both by ordinary least squares:

  Power law:   log10 T = c + k log10 S, i.e. T = C * S^k.
      k is the scaling exponent (k = 1: linear growth). R^2 is computed on
      the log scale and measures how closely the points follow a power law.
      The 95% interval for k comes from its standard error (t, n - 2 df).
      This fit tests the claim that cost grows near-linearly. A fixed
      overhead flattens the smallest configurations and biases k slightly
      downwards, so k < 1 should be read as "no faster than linear".

  Straight line:   T = a + b S.
      b is the marginal cost (ms per thousand lines), a a fixed overhead.
      Its R^2 is not a test of linearity: over several orders of magnitude
      it is dominated by the largest configurations.

Both models are fitted against Regia source size (input_loc) and against
generated AgentSpeak size (output_loc_total), so the two can be compared.

Analyses, matching Section 7.2:
  - the eight single-dimension sweeps, pooled and one by one (SWEEPS);
  - the realistic-project scenario (SCENARIOS);
  - the construct-mix comparison (MIX): cost per thousand source lines of the
    two compositions, compared at matched source size by interpolating each
    curve on a log-spaced grid over the size range both cover.

Usage:
    python benchmark_fits.py RESULTS_DIR [--out OUT_DIR] [--format pdf|png|both] [--dpi N] [--include-io]

Outputs, in OUT_DIR (default RESULTS_DIR/fits):
    fits.csv, fits.md             every fit, and a readable summary
    per_kloc.csv                  cost per thousand lines at the top of each sweep
    mix_comparison.csv            the two mix curves at matched source size
    sweeps_vs_input.{pdf,png}     pooled sweeps, log axes, with the power-law fit
    realistic_project.{pdf,png}   the scenario, with its fit and a linear reference
    construct_mix.{pdf,png}       cost per thousand lines of the two mixes
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, LogLocator


# ======================================================
# Experiments analysed, by suite name in experiments.py
# ======================================================

SWEEPS = {
    "scale_roles": "Roles",
    "scale_phases": "Phases",
    "scale_playbooks": "Playbooks",
    "scale_plans": "Plans per Playbook",
    "scale_branches": "Branches per Plan",
    "scale_stmts": "Statements per Branch",
    "scale_subplot_breadth": "Subplot Breadth",
    "scale_subplot_depth": "Subplot Depth",
}
SCENARIO = ("interaction_full_game_case_study", "Realistic project")
MIX = {
    "interaction_shape_narrative_heavy": "Narrative-heavy",
    "interaction_shape_reactive_heavy": "Reactive-heavy",
}

BASELINE = dict(n_actions=10, n_events=10, n_facts=5, n_playbooks=2, n_plans_per_playbook=2,
                n_branches_per_plan=1, n_stmts_per_branch=2, n_roles=2, n_phases=2,
                n_subplot_breadth=0, n_subplot_depth=0)
MIX_SIZES = [300, 1000, 4000]   # source sizes at which Table 7.x compares the two mixes

PARAM_COLS = [
    "n_actions", "n_events", "n_facts", "n_playbooks", "n_plans_per_playbook",
    "n_branches_per_plan", "n_stmts_per_branch", "n_roles", "n_phases",
    "n_subplot_breadth", "n_subplot_depth",
]


# ======================================================
# Loading
# ======================================================

def load_suite(results: Path, suite: str, include_io: bool) -> pd.DataFrame | None:
    """Load one suite's CSV and average its runs, one row per configuration."""
    path = results / suite / f"{suite}.csv"
    if not path.exists():
        print(f"warning: {path} not found, skipping", file=sys.stderr)
        return None
    df = pd.read_csv(path)
    failed = (~df["success"].astype(bool)).sum()
    if failed:
        print(f"warning: {suite}: {failed} failed compilations excluded", file=sys.stderr)
        df = df[df["success"].astype(bool)]
    df["time_ms"] = df["compile_time_s"] * 1000.0
    if include_io:
        df["time_ms"] += df["io_time_s"] * 1000.0
    g = df.groupby(PARAM_COLS, as_index=False).agg(
        time_ms=("time_ms", "mean"),
        time_sd=("time_ms", "std"),
        input_loc=("input_loc", "first"),
        output_loc=("output_loc_total", "first"),
        output_files=("output_files", "first"),
        peak_ram_mb=("peak_ram_mb", "mean"),
        runs=("time_ms", "size"),
    )
    g["suite"] = suite
    return g.sort_values("input_loc").reset_index(drop=True)


# ======================================================
# Fits
# ======================================================

def fit_power(size, time) -> dict:
    res = stats.linregress(np.log10(size), np.log10(time))
    n = len(size)
    t = stats.t.ppf(0.975, n - 2) if n > 2 else np.nan
    return {"k": res.slope, "k_low": res.slope - t * res.stderr, "k_high": res.slope + t * res.stderr,
            "r2": res.rvalue ** 2, "C_ms": 10 ** res.intercept, "points": n}


def fit_linear(size, time) -> dict:
    res = stats.linregress(size, time)
    pred = res.intercept + res.slope * size
    return {"ms_per_kloc": res.slope * 1000.0, "overhead_ms": res.intercept, "r2": res.rvalue ** 2,
            "max_rel_residual": float(np.max(np.abs(time - pred) / time)), "points": len(size)}


def fits_for(label: str, data: pd.DataFrame) -> list[dict]:
    rows = []
    for size_col in ["input_loc", "output_loc"]:
        s, t = data[size_col].to_numpy(float), data["time_ms"].to_numpy(float)
        if len(s) >= 3:
            rows.append({"analysis": label, "size": size_col, "model": "power", **fit_power(s, t)})
            rows.append({"analysis": label, "size": size_col, "model": "linear", **fit_linear(s, t)})
    return rows


def compare_mix(curves: dict[str, pd.DataFrame], n_grid: int = 50) -> pd.DataFrame:
    """Cost per thousand source lines of each curve, on a common log-spaced size grid."""
    lo = max(c["input_loc"].min() for c in curves.values())
    hi = min(c["input_loc"].max() for c in curves.values())
    if lo >= hi:
        return pd.DataFrame()
    grid = np.logspace(np.log10(lo), np.log10(hi), n_grid)
    out = pd.DataFrame({"input_loc": grid})
    for label, c in curves.items():
        per_kloc = c["time_ms"] / c["input_loc"] * 1000.0
        out[label] = np.interp(np.log10(grid), np.log10(c["input_loc"]), per_kloc)
    a, b = list(curves)
    out["gap_pct"] = (out[a] - out[b]).abs() / out[[a, b]].min(axis=1) * 100.0
    return out


# ======================================================
# Figures
# ======================================================

FORMATS = ["pdf"]   # set from --format in main()
DPI = 300


def _save(fig, path: Path) -> None:
    """Save a figure in every requested format."""
    fig.tight_layout()
    for fmt in FORMATS:
        fig.savefig(path.with_suffix(f".{fmt}"), dpi=DPI)
    plt.close(fig)


PLAIN = FuncFormatter(lambda v, _: f"{v:,.0f}" if v >= 1 else f"{v:g}")


def _plain_ticks(axis) -> None:
    """Show log-scale ticks as plain numbers (1,000 rather than 10^3)."""
    axis.set_major_locator(LogLocator(base=10, subs=(1.0, 2.0, 5.0)))
    axis.set_major_formatter(PLAIN)
    axis.set_minor_formatter(FuncFormatter(lambda v, _: ""))


def _log_axes(ax, xlabel, ylabel):
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(f"{xlabel}, log scale"); ax.set_ylabel(f"{ylabel}, log scale")
    _plain_ticks(ax.xaxis); _plain_ticks(ax.yaxis)
    ax.grid(True, which="both", alpha=0.3); ax.legend(fontsize=8)


def plot_sweeps(sweeps: dict[str, pd.DataFrame], fit: dict, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    for label, g in sweeps.items():
        ax.plot(g["input_loc"], g["time_ms"], "o-", ms=4, lw=1, label=label)
    allx = pd.concat(sweeps.values())["input_loc"]
    xs = np.logspace(np.log10(allx.min()), np.log10(allx.max()), 100)
    ax.plot(xs, fit["C_ms"] * xs ** fit["k"], "k--", lw=1.5,
            label=f"pooled fit, k = {fit['k']:.2f}, R$^2$ = {fit['r2']:.2f}")
    _log_axes(ax, "Regia source size (lines)", "Compilation time (ms)")
    _save(fig, path)


def plot_scenario(g: pd.DataFrame, fit: dict, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(g["input_loc"], g["time_ms"], "o-", label="measured")
    xs = np.logspace(np.log10(g["input_loc"].min()), np.log10(g["input_loc"].max()), 100)
    x0, t0 = g["input_loc"].iloc[0], g["time_ms"].iloc[0]
    ax.plot(xs, t0 * xs / x0, ":", color="grey", label="linear rate of the 1$\\times$ point")
    ax.plot(xs, fit["C_ms"] * xs ** fit["k"], "k--", label=f"fit, k = {fit['k']:.3f}")
    _log_axes(ax, "Regia source size (lines)", "Compilation time (ms)")
    _save(fig, path)


def plot_mix(curves: dict[str, pd.DataFrame], path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    for label, c in curves.items():
        ax.plot(c["input_loc"], c["time_ms"] / c["input_loc"] * 1000.0, "o-", label=label)
    ax.set_xscale("log")
    ax.set_xlabel("Regia source size (lines), log scale"); ax.set_ylabel("Compilation time per 1,000 lines (ms)")
    _plain_ticks(ax.xaxis)
    ax.grid(True, which="both", alpha=0.3); ax.legend(fontsize=8)
    _save(fig, path)


# ======================================================
# Main
# ======================================================

def main() -> None:
    ap = argparse.ArgumentParser(description="Scaling fits and figures for the Regia benchmarks.")
    ap.add_argument("results_dir", type=Path)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--format", choices=["pdf", "png", "both"], default="pdf",
                    help="figure format: pdf (vector, for LaTeX), png, or both (default: pdf)")
    ap.add_argument("--dpi", type=int, default=300, help="resolution of PNG figures (default: 300)")
    ap.add_argument("--include-io", action="store_true",
                    help="fit compilation plus write time instead of compilation time alone")
    args = ap.parse_args()
    global FORMATS, DPI
    FORMATS = ["pdf", "png"] if args.format == "both" else [args.format]
    DPI = args.dpi
    res, out = args.results_dir, args.out or args.results_dir / "fits"
    out.mkdir(parents=True, exist_ok=True)

    sweeps = {lab: d for s, lab in SWEEPS.items() if (d := load_suite(res, s, args.include_io)) is not None}
    scenario = load_suite(res, SCENARIO[0], args.include_io)
    mix = {lab: d for s, lab in MIX.items() if (d := load_suite(res, s, args.include_io)) is not None}

    rows, md = [], ["# Benchmark fits", "",
                    f"Time: {'compilation + write' if args.include_io else 'compilation only'}; "
                    "each point is the mean of the runs of one configuration.", ""]
    if sweeps:
        pooled = pd.concat(sweeps.values(), ignore_index=True)
        rows += fits_for("Pooled sweeps", pooled)
        for lab, d in sweeps.items():
            rows += fits_for(lab, d)
    if scenario is not None:
        rows += fits_for(SCENARIO[1], scenario)
    for lab, d in mix.items():
        rows += fits_for(lab, d)
    fits = pd.DataFrame(rows)
    fits.to_csv(out / "fits.csv", index=False)

    md += ["## Fits", "", "| Analysis | Size | Model | Result | R² | Points |", "|---|---|---|---|---|---|"]
    for _, r in fits.iterrows():
        result = (f"k = {r['k']:.3f} [{r['k_low']:.3f}, {r['k_high']:.3f}]" if r["model"] == "power"
                  else f"{r['ms_per_kloc']:.1f} ms/kLOC, overhead {r['overhead_ms']:.1f} ms")
        md.append(f"| {r['analysis']} | {r['size']} | {r['model']} | {result} | {r['r2']:.3f} | {int(r['points'])} |")

    if sweeps:
        top = pd.DataFrame([{"dimension": lab, "input_loc": d["input_loc"].iloc[-1],
                             "output_loc": d["output_loc"].iloc[-1], "time_ms": d["time_ms"].iloc[-1],
                             "ms_per_kloc_input": d["time_ms"].iloc[-1] / d["input_loc"].iloc[-1] * 1000,
                             "ms_per_kloc_output": d["time_ms"].iloc[-1] / d["output_loc"].iloc[-1] * 1000}
                            for lab, d in sweeps.items()])
        top.to_csv(out / "per_kloc.csv", index=False)
        md += ["", "## Cost per thousand lines at the top of each sweep", "",
               "| Dimension | Source lines | ms per kLOC (source) | ms per kLOC (output) |", "|---|---|---|---|"]
        md += [f"| {r['dimension']} | {r['input_loc']:.0f} | {r['ms_per_kloc_input']:.1f} | {r['ms_per_kloc_output']:.1f} |"
               for _, r in top.iterrows()]
        pf = fits[(fits["analysis"] == "Pooled sweeps") & (fits["size"] == "input_loc") & (fits["model"] == "power")].iloc[0]
        plot_sweeps(sweeps, pf, out / "sweeps_vs_input.pdf")

    if sweeps:
        md += ["", "## Sweep endpoints", "",
               "| Dimension | Range | Source lines | Output lines | Time (ms) |", "|---|---|---|---|---|"]
        for s_name, lab in SWEEPS.items():
            if lab not in sweeps:
                continue
            d = sweeps[lab]
            col = next(c for c in PARAM_COLS if d[c].nunique() > 1)
            lo, hi = d.sort_values(col).iloc[0], d.sort_values(col).iloc[-1]
            md.append(f"| {lab} | {lo[col]} -> {hi[col]} | {lo['input_loc']:.0f} -> {hi['input_loc']:.0f} | "
                      f"{lo['output_loc']:.0f} -> {hi['output_loc']:.0f} | {lo['time_ms']:.1f} -> {hi['time_ms']:.1f} |")
        allpts = pd.concat(sweeps.values(), ignore_index=True)
        base = allpts[np.logical_and.reduce([allpts[c] == v for c, v in BASELINE.items()])]
        if len(base):
            md += ["", "## Default configuration (mean over the sweeps containing it)", "",
                   f"- Source lines: {base['input_loc'].iloc[0]:.0f}; output lines: {base['output_loc'].iloc[0]:.0f}; "
                   f"files: {base['output_files'].iloc[0]:.0f}; ratio: {base['output_loc'].iloc[0] / base['input_loc'].iloc[0]:.2f}",
                   f"- Time: {base['time_ms'].mean():.2f} ms (range {base['time_ms'].min():.2f} to {base['time_ms'].max():.2f} "
                   f"across {len(base)} sweeps); peak RAM: {base['peak_ram_mb'].mean():.2f} MB"]

    if scenario is not None:
        s = scenario
        md += ["", f"## {SCENARIO[1]}", "",
               "| Source lines | Output lines | Files | Time (ms) | ms per kLOC | Peak RAM (MB) |", "|---|---|---|---|---|---|"]
        md += [f"| {r['input_loc']:.0f} | {r['output_loc']:.0f} | {r['output_files']:.0f} | {r['time_ms']:.1f} | "
               f"{r['time_ms'] / r['input_loc'] * 1000:.1f} | {r['peak_ram_mb']:.1f} |" for _, r in s.iterrows()]
        sf = fits[(fits["analysis"] == SCENARIO[1]) & (fits["size"] == "input_loc") & (fits["model"] == "power")].iloc[0]
        plot_scenario(s, sf, out / "realistic_project.pdf")

    if len(mix) == 2:
        cmp = compare_mix(mix)
        cmp.to_csv(out / "mix_comparison.csv", index=False)
        md += ["", "## Construct mix at matched source size", ""]
        if cmp.empty:
            md.append("The two curves do not overlap in source size.")
        else:
            a, b = list(mix)
            md += [f"- Overlap: {cmp['input_loc'].iloc[0]:.0f} to {cmp['input_loc'].iloc[-1]:.0f} source lines",
                   f"- Gap between the curves: {cmp['gap_pct'].min():.1f}% to {cmp['gap_pct'].max():.1f}%",
                   f"- Same order throughout: {bool(((cmp[a] > cmp[b]).all()) or ((cmp[a] < cmp[b]).all()))}",
                   f"- Rise in cost per kLOC across the overlap: {a} x{cmp[a].iloc[-1] / cmp[a].iloc[0]:.2f}, "
                   f"{b} x{cmp[b].iloc[-1] / cmp[b].iloc[0]:.2f}"]
            md += ["", "| Source lines | " + " | ".join(f"{lab} (ms/kLOC)" for lab in mix) + " |",
                   "|---|" + "---|" * len(mix)]
            for size in MIX_SIZES:
                vals = [np.interp(np.log10(size), np.log10(c["input_loc"]), c["time_ms"] / c["input_loc"] * 1000)
                        for c in mix.values()]
                md.append(f"| {size} | " + " | ".join(f"{v:.1f}" for v in vals) + " |")
            cross = np.where(np.diff(np.sign(cmp[a] - cmp[b])) != 0)[0]
            if len(cross):
                md.append("")
                md.append("- Curves cross near: " + ", ".join(f"{cmp['input_loc'].iloc[i]:.0f}" for i in cross) + " source lines")
        plot_mix(mix, out / "construct_mix.pdf")

    (out / "fits.md").write_text("\n".join(md) + "\n")
    print("\n".join(md)); print(f"\nOutputs written to {out}")


if __name__ == "__main__":
    main()