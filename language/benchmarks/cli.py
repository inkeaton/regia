"""
Command-line interface for the Regia scalability benchmark suite.

Usage:
    python -m benchmarks run EXPERIMENT
    python -m benchmarks run --all
    python -m benchmarks list

Output layout:
    <output_dir>/
        <experiment_name>/
            <experiment_name>.csv        <- performance data
            sources/
                <experiment>_<hash>.regia  <- generated source files
"""

import sys
from pathlib import Path

import click

from .experiments import BASELINE, EXPERIMENTS
from .runner import run_experiment, save_csv


# ======================================================
# CLI Group
# ======================================================

@click.group()
def main() -> None:
    """Regia transpiler scalability benchmark suite."""


# ======================================================
# run command
# ======================================================

@main.command("run")
@click.argument("experiment", required=False, default=None)
@click.option(
    "--all", "run_all",
    is_flag=True,
    help="Run all experiment suites sequentially.",
)
@click.option(
    "--output", "-o",
    default="results",
    show_default=True,
    type=click.Path(file_okay=False, dir_okay=True, writable=True),
    help="Root directory for CSV results and source files.",
)
@click.option(
    "--reps", "-r",
    default=None,
    type=int,
    help="Override the number of timed repetitions per config (default: per-experiment value).",
)
def run_cmd(
    experiment: str | None,
    run_all: bool,
    output: str,
    reps: int | None,
) -> None:
    """
    Run one or all benchmark experiment suites.

    EXPERIMENT must be a name from `benchmarks list`.
    Use --all to run every suite in sequence.
    """
    output_dir = Path(output)

    if run_all:
        suites = list(EXPERIMENTS.keys())
    elif experiment:
        if experiment not in EXPERIMENTS:
            click.echo(
                f"Error: unknown experiment '{experiment}'.\n"
                f"Run 'python -m benchmarks list' to see available names.",
                err=True,
            )
            sys.exit(1)
        suites = [experiment]
    else:
        click.echo(
            "Error: provide an experiment name or use --all.",
            err=True,
        )
        sys.exit(1)

    for suite_name in suites:
        sep = "=" * 60
        click.echo(f"\n{sep}")
        click.echo(f"  Suite: {suite_name}")
        click.echo(sep)

        configs = EXPERIMENTS[suite_name]

        # Apply --reps override if requested.
        if reps is not None:
            from dataclasses import replace
            configs = [replace(cfg, n_reps=reps) for cfg in configs]

        sources_dir = output_dir / suite_name / "sources"
        records = run_experiment(suite_name, configs, sources_dir)

        csv_path = output_dir / suite_name / f"{suite_name}.csv"
        save_csv(records, csv_path)

        click.echo(f"\n  {len(records)} records -> {csv_path}")

    click.echo("\nDone.")


# ======================================================
# list command
# ======================================================

@main.command("list")
def list_cmd() -> None:
    """List all available experiment suite names with a brief description."""
    click.echo("\nAvailable experiment suites:\n")
    header = f"  {'Suite name':<35} {'Configs':>7}  {'Reps':>4}  Varied parameter"
    click.echo(header)
    click.echo("  " + "-" * 70)

    # Infer the varied parameter by comparing each config against BASELINE.
    from dataclasses import fields
    baseline_dict = {f.name: getattr(BASELINE, f.name) for f in fields(BASELINE)}

    for name, configs in EXPERIMENTS.items():
        n_configs = len(configs)
        n_reps = configs[0].n_reps if configs else 0
        varied = "?"
        if configs:
            first_dict = {f.name: getattr(configs[0], f.name) for f in fields(configs[0])}
            diffs = [k for k, v in first_dict.items() if baseline_dict.get(k) != v
                     and k not in ("n_reps",)]
            varied = ", ".join(diffs) if diffs else "(combined)"
        click.echo(
            f"  {name:<35} {n_configs:>7}  {n_reps:>4}  {varied}"
        )

    click.echo()


# ======================================================
# validate command
# ======================================================

@main.command("validate")
@click.argument("experiment", required=False, default=None)
@click.option("--all", "validate_all", is_flag=True, help="Validate all suites.")
def validate_cmd(experiment: str | None, validate_all: bool) -> None:
    """
    Dry-run: generate source and compile each config without timing.

    Useful to confirm that all generated Regia code is valid before
    committing to a full benchmark run.
    """
    from .generator import generate
    from regia.compiler import compile_source

    if validate_all:
        suites = list(EXPERIMENTS.keys())
    elif experiment:
        if experiment not in EXPERIMENTS:
            click.echo(f"Error: unknown experiment '{experiment}'.", err=True)
            sys.exit(1)
        suites = [experiment]
    else:
        click.echo("Error: provide an experiment name or use --all.", err=True)
        sys.exit(1)

    total = 0
    failures = 0

    for suite_name in suites:
        configs = EXPERIMENTS[suite_name]
        click.echo(f"\nValidating {suite_name} ({len(configs)} configs)...")

        for i, cfg in enumerate(configs):
            source = generate(cfg)
            result = compile_source(source, emit=False)
            total += 1
            icon = "OK" if result.success else "FAIL"
            err_str = f"  {result.error_count} error(s)" if not result.success else ""
            click.echo(f"  config {i:>3}: {icon}{err_str}")
            if not result.success:
                failures += 1
                for msg in result.messages:
                    click.echo(f"    [{msg.severity.name}] {msg.message}", err=True)

    click.echo(f"\nTotal: {total} configs, {failures} failure(s).")
    if failures:
        sys.exit(1)


# ======================================================
# plot command
# ======================================================

@main.command("plot")
@click.argument("experiment", required=False, default=None)
@click.option("--all", "plot_all", is_flag=True, help="Plot all suites.")
@click.option(
    "--output", "-o",
    default="results",
    show_default=True,
    type=click.Path(file_okay=False, dir_okay=True),
    help="Root directory where CSV results are stored.",
)
def plot_cmd(experiment: str | None, plot_all: bool, output: str) -> None:
    """
    Generate plots from previously generated CSV results.
    
    Requires pandas and matplotlib: `pip install -e .[benchmarks]`
    """
    from .visualize import plot_experiment
    
    output_dir = Path(output)
    
    if plot_all:
        suites = list(EXPERIMENTS.keys())
    elif experiment:
        if experiment not in EXPERIMENTS:
            click.echo(f"Error: unknown experiment '{experiment}'.", err=True)
            sys.exit(1)
        suites = [experiment]
    else:
        click.echo("Error: provide an experiment name or use --all.", err=True)
        sys.exit(1)
        
    for suite_name in suites:
        csv_path = output_dir / suite_name / f"{suite_name}.csv"
        try:
            plot_experiment(csv_path)
        except ImportError as e:
            click.echo(f"\nError: {e}", err=True)
            sys.exit(1)


# ======================================================
# profile command
# ======================================================

@main.command("profile")
@click.argument("filepath", type=click.Path(exists=True, dir_okay=False))
def profile_cmd(filepath: str) -> None:
    """Benchmark the compilation of a specific external .regia file."""
    import time
    import tempfile
    
    from regia.compiler import compile_file
    from .metrics import measure_time_and_ram, count_loc, count_output_loc
    from .runner import warmup
    
    path = Path(filepath)
    click.echo(f"\nProfiling file: {path.name} ({path.stat().st_size} bytes)")
    
    # Read input for loc count
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    input_loc = count_loc(source)
    
    # Warm up Lark
    warmup()
    
    def _compile() -> object:
        return compile_file(str(path))
        
    result, wall_time, peak_mb = measure_time_and_ram(_compile)
    
    if not result.success:
        click.echo(f"  Result: FAIL ({result.error_count} errors)", err=True)
        for msg in result.messages:
            click.echo(f"    [{msg.severity.name}] {msg.message}", err=True)
        sys.exit(1)
        
    output_files = len(result.outputs)
    output_loc_total, _ = count_output_loc(result.outputs)
    loc_ratio = output_loc_total / max(input_loc, 1)
    
    # Measure IO time
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        t_start = time.perf_counter()
        for fname, fcontent in result.outputs.items():
            (tmp_path / fname).write_text(fcontent, encoding="utf-8")
        io_time_s = time.perf_counter() - t_start
        
    total_time = wall_time + io_time_s
    
    sep = "-" * 50
    click.echo(sep)
    click.echo(f"  CPU Time:  {wall_time:.4f}s")
    click.echo(f"  I/O Time:  {io_time_s:.4f}s")
    click.echo(f"  Total:     {total_time:.4f}s")
    click.echo(f"  Peak RAM:  {peak_mb:.2f} MB")
    click.echo(f"  In LoC:    {input_loc}")
    click.echo(f"  Out LoC:   {output_loc_total} (Ratio: {loc_ratio:.2f}x)")
    click.echo(f"  Files:     {output_files}")
    click.echo(sep)
    click.echo("Done.\n")

