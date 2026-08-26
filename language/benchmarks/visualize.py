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
    swept_param_str = _get_swept_parameter(df, experiment_name)
    
    # Extract the primary x-axis column. If it's Combined, just grab the first varying column.
    cols_to_check = [
        "n_actions", "n_events", "n_facts", "n_playbooks", "n_plans_per_playbook",
        "n_branches_per_plan", "n_stmts_per_branch", "n_roles", "n_phases",
        "n_subplot_breadth", "n_subplot_depth"
    ]
    varying_cols = [c for c in cols_to_check if c in df.columns and df[c].nunique() > 1]
    
    x_col = varying_cols[0] if varying_cols else "run_id"
    
    if len(varying_cols) > 1:
        logger.info(f"Swept parameter is '{swept_param_str}'. Using '{x_col}' for X-axis.")

    # Group by the swept parameter and compute mean and std
    grouped = df.groupby(x_col).agg(
        time_mean=("compile_time_s", "mean"),
        time_std=("compile_time_s", "std"),
        ram_mean=("peak_ram_mb", "mean"),
        ram_std=("peak_ram_mb", "std"),
        loc_mean=("loc_ratio", "mean"),
        loc_std=("loc_ratio", "std")
    ).reset_index()

    # Create a 1x3 subplot layout
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f"Scalability Benchmark: {experiment_name}", fontsize=14, fontweight="bold")

    # Plot 1: Compile Time
    ax1.errorbar(
        grouped[x_col], grouped["time_mean"], yerr=grouped["time_std"],
        fmt="-o", capsize=5, capthick=1.5, color="#1f77b4"
    )
    ax1.set_title("Compilation Time")
    ax1.set_xlabel(x_col)
    ax1.set_ylabel("Time (seconds)")
    ax1.grid(True, linestyle="--", alpha=0.7)
    
    # Optional: Log scale if data spans multiple orders of magnitude
    if grouped["time_mean"].max() / max(grouped["time_mean"].min(), 1e-6) > 50:
        ax1.set_yscale("log")
        ax1.set_xscale("log")
        # Format axes nicely for log scale
        ax1.yaxis.set_major_formatter(ticker.ScalarFormatter())
        ax1.xaxis.set_major_formatter(ticker.ScalarFormatter())

    # Plot 2: Peak RAM
    ax2.errorbar(
        grouped[x_col], grouped["ram_mean"], yerr=grouped["ram_std"],
        fmt="-s", capsize=5, capthick=1.5, color="#ff7f0e"
    )
    ax2.set_title("Peak RAM Usage")
    ax2.set_xlabel(x_col)
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
    ax3.set_xlabel(x_col)
    ax3.set_ylabel("LoC Ratio")
    ax3.grid(True, linestyle="--", alpha=0.7)
    
    if grouped["loc_mean"].max() / max(grouped["loc_mean"].min(), 1e-6) > 50:
        ax3.set_xscale("log")
        ax3.xaxis.set_major_formatter(ticker.ScalarFormatter())

    # Finalize layout and save
    plt.tight_layout()
    
    out_png = csv_path.with_name(f"{experiment_name}_plots.png")
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    logger.info(f"Saved visualization to: {out_png}")
    
    # Close the figure to release memory
    plt.close(fig)
