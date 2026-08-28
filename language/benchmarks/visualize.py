"""
Visualization module for the Regia scalability benchmark suite.

Reads the output CSVs and generates plots for Compile Time, Peak RAM, and LoC Expansion Ratio
using matplotlib.
"""

import logging
from pathlib import Path

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
except ImportError:
    pd = None
    plt = None

from .experiments import EXPERIMENTS, BASELINE

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def _get_swept_parameter(df: pd.DataFrame, experiment: str) -> str:
    """
    Infer which GeneratorConfig field was varied in this experiment suite
    by checking which columns have more than one unique value in the CSV.
    """
    cols_to_check = [
        "n_actions", "n_events", "n_facts", "n_playbooks", "n_plans_per_playbook",
        "n_branches_per_plan", "n_stmts_per_branch", "n_roles", "n_phases",
        "n_subplot_breadth", "n_subplot_depth"
    ]
    
    # Filter to only the columns that actually exist in the dataframe
    valid_cols = [c for c in cols_to_check if c in df.columns]
    
    # Find columns that vary (have more than 1 unique value)
    varying_cols = [c for c in valid_cols if df[c].nunique() > 1]
    
    if len(varying_cols) == 1:
        return varying_cols[0]
    elif len(varying_cols) > 1:
        # In combined sweeps, usually they are named explicitly, or we return the first one as the primary axis.
        # But for the string representation we can show them all.
        return f"Combined ({', '.join(varying_cols)})"
    else:
        return "None"


def plot_experiment(csv_path: Path) -> None:
    """
    Reads a benchmark CSV file and generates a 3-panel PNG plot in the same directory.
    
    Args:
        csv_path: Path to the benchmark CSV file (e.g. results/scale_roles/scale_roles.csv).
    """
    if pd is None or plt is None:
        raise ImportError(
            "Visualization dependencies are missing. "
            "Please install them via: pip install -e .[benchmarks]"
        )

    if not csv_path.exists():
        logger.error(f"Error: CSV file not found at {csv_path}")
        return

    logger.info(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)

    if df.empty:
        logger.warning(f"Warning: {csv_path} is empty. Skipping plot.")
        return

    experiment_name = df["experiment"].iloc[0]
    
    # Extract the varying columns
    cols_to_check = [
        "n_actions", "n_events", "n_facts", "n_playbooks", "n_plans_per_playbook",
        "n_branches_per_plan", "n_stmts_per_branch", "n_roles", "n_phases",
        "n_subplot_breadth", "n_subplot_depth"
    ]
    varying_cols = [c for c in cols_to_check if c in df.columns and df[c].nunique() > 1]
    
    x_col = varying_cols[0] if varying_cols else "run_id"
    
    # Check if it's a 2D grid
    is_grid = False
    if len(varying_cols) == 2:
        c1, c2 = varying_cols
        n1, n2 = df[c1].nunique(), df[c2].nunique()
        combo_count = len(df.drop_duplicates(varying_cols))
        if combo_count >= n1 * n2 and n1 > 1 and n2 > 1:
            is_grid = True
            y_col = c2
            x_col = c1

    if is_grid:
        logger.info(f"Detected 2D Grid Sweep: {x_col} x {y_col}. Generating heatmaps...")
        _plot_heatmap(df, experiment_name, x_col, y_col, csv_path)
    else:
        x_label = f"{x_col} (coupled with: {', '.join(varying_cols[1:])})" if len(varying_cols) > 1 else x_col
        _plot_line(df, experiment_name, x_col, x_label, csv_path)


def _plot_line(df, experiment_name, x_col, x_label, csv_path):
    # Group by the swept parameter and compute mean and std
    grouped = df.groupby(x_col).agg(
        time_mean=("compile_time_s", "mean"),
        time_std=("compile_time_s", "std"),
        io_mean=("io_time_s", "mean"),
        io_std=("io_time_s", "std"),
        ram_mean=("peak_ram_mb", "mean"),
        ram_std=("peak_ram_mb", "std"),
        loc_mean=("loc_ratio", "mean"),
        loc_std=("loc_ratio", "std"),
        files_mean=("output_files", "mean")
    ).reset_index()

    # Create a 2x2 subplot layout
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f"Scalability Benchmark: {experiment_name}", fontsize=14, fontweight="bold")

    # Plot 1: Compile Time vs I/O Time (Stacked Area)
    ax1.plot(grouped[x_col], grouped["time_mean"], "-o", color="#1f77b4", label="CPU Time")
    ax1.plot(grouped[x_col], grouped["time_mean"] + grouped["io_mean"], "-^", color="#d62728", label="Total Time (CPU + I/O)")
    ax1.fill_between(grouped[x_col], 0, grouped["time_mean"], color="#1f77b4", alpha=0.3)
    ax1.fill_between(grouped[x_col], grouped["time_mean"], grouped["time_mean"] + grouped["io_mean"], color="#d62728", alpha=0.3)
    ax1.legend(loc="upper left")
    
    ax1.set_title("Compilation & I/O Time")
    ax1.set_xlabel(x_label)
    ax1.set_ylabel("Time (seconds)")
    ax1.grid(True, linestyle="--", alpha=0.7)
    
    if (grouped["time_mean"] + grouped["io_mean"]).max() / max((grouped["time_mean"] + grouped["io_mean"]).min(), 1e-6) > 50:
        ax1.set_yscale("log")
        ax1.set_xscale("log")
        ax1.yaxis.set_major_formatter(ticker.ScalarFormatter())
        ax1.xaxis.set_major_formatter(ticker.ScalarFormatter())

    # Plot 2: Peak RAM
    ax2.errorbar(
        grouped[x_col], grouped["ram_mean"], yerr=grouped["ram_std"],
        fmt="-s", capsize=5, capthick=1.5, color="#ff7f0e"
    )
    ax2.set_title("Peak RAM Usage")
    ax2.set_xlabel(x_label)
    ax2.set_ylabel("Memory (MB)")
    ax2.grid(True, linestyle="--", alpha=0.7)
    
    if grouped["ram_mean"].max() / max(grouped["ram_mean"].min(), 1e-6) > 50:
        ax2.set_yscale("log")
        ax2.set_xscale("log")
        ax2.yaxis.set_major_formatter(ticker.ScalarFormatter())
        ax2.xaxis.set_major_formatter(ticker.ScalarFormatter())

    # Plot 3: LoC Expansion Ratio
    ax3.errorbar(
        grouped[x_col], grouped["loc_mean"], yerr=grouped["loc_std"],
        fmt="-^", capsize=5, capthick=1.5, color="#2ca02c"
    )
    ax3.set_title("Code Expansion (Output / Input LoC)")
    ax3.set_xlabel(x_label)
    ax3.set_ylabel("LoC Ratio")
    ax3.grid(True, linestyle="--", alpha=0.7)
    
    if grouped["loc_mean"].max() / max(grouped["loc_mean"].min(), 1e-6) > 50:
        ax3.set_xscale("log")
        ax3.xaxis.set_major_formatter(ticker.ScalarFormatter())

    # Plot 4: Generated File Count
    ax4.plot(grouped[x_col], grouped["files_mean"], "-D", color="#9467bd")
    ax4.set_title("Generated File Count")
    ax4.set_xlabel(x_label)
    ax4.set_ylabel("Output Files")
    ax4.grid(True, linestyle="--", alpha=0.7)
    
    if grouped["files_mean"].max() / max(grouped["files_mean"].min(), 1e-6) > 50:
        ax4.set_yscale("log")
        ax4.set_xscale("log")
        ax4.yaxis.set_major_formatter(ticker.ScalarFormatter())
        ax4.xaxis.set_major_formatter(ticker.ScalarFormatter())

    plt.tight_layout()
    out_png = csv_path.with_name(f"{experiment_name}_plots.png")
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    logger.info(f"Saved visualization to: {out_png}")
    plt.close(fig)


def _plot_heatmap(df, experiment_name, x_col, y_col, csv_path):
    import numpy as np
    
    # Group by the two swept parameters and compute mean
    grouped = df.groupby([y_col, x_col]).agg(
        time_mean=("compile_time_s", "mean"),
        ram_mean=("peak_ram_mb", "mean"),
        loc_mean=("loc_ratio", "mean"),
        files_mean=("output_files", "mean")
    ).reset_index()

    # Pivot to get 2D matrices
    time_matrix = grouped.pivot(index=y_col, columns=x_col, values="time_mean")
    ram_matrix = grouped.pivot(index=y_col, columns=x_col, values="ram_mean")
    loc_matrix = grouped.pivot(index=y_col, columns=x_col, values="loc_mean")
    files_matrix = grouped.pivot(index=y_col, columns=x_col, values="files_mean")

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle(f"Scalability Benchmark (2D Sweep): {experiment_name}", fontsize=14, fontweight="bold")

    def draw_heatmap(ax, matrix, title, cmap):
        c = ax.pcolormesh(matrix.columns, matrix.index, matrix.values, shading='nearest', cmap=cmap)
        fig.colorbar(c, ax=ax)
        ax.set_title(title)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        # Set ticks explicitly since these are discrete points
        ax.set_xticks(matrix.columns)
        ax.set_yticks(matrix.index)
        
        # Determine if we should use log scale for axes visually
        if max(matrix.columns) / max(min(matrix.columns), 1e-6) > 50:
            ax.set_xscale('log')
            ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
        if max(matrix.index) / max(min(matrix.index), 1e-6) > 50:
            ax.set_yscale('log')
            ax.yaxis.set_major_formatter(ticker.ScalarFormatter())

    draw_heatmap(ax1, time_matrix, "Compilation Time (s)", "Blues")
    draw_heatmap(ax2, ram_matrix, "Peak RAM (MB)", "Oranges")
    draw_heatmap(ax3, loc_matrix, "Code Expansion Ratio", "Greens")
    draw_heatmap(ax4, files_matrix, "Generated File Count", "Purples")

    plt.tight_layout()
    out_png = csv_path.with_name(f"{experiment_name}_plots.png")
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    logger.info(f"Saved visualization to: {out_png}")
    plt.close(fig)
