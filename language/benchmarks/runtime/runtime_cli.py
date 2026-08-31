"""
runtime_cli.py -- CLI entry point for Jason runtime benchmarks.

Usage:
    python -m benchmarks.runtime run scale_agents
    python -m benchmarks.runtime run scale_roles
    python -m benchmarks.runtime run --all
    python -m benchmarks.runtime run scale_agents --duration 15 --interval 0.25
    python -m benchmarks.runtime run scale_agents --out results/my_run.csv
"""

import argparse
import csv
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import List

from .runtime_experiments import RUNTIME_EXPERIMENTS
from .runtime_runner import RuntimeRecord, RUNTIME_CSV_FIELDNAMES, run_runtime_experiment


# ==============================================================
# CSV I/O
# ==============================================================

def save_csv(records: List[RuntimeRecord], csv_path: Path) -> None:
    """
    Write runtime benchmark records to a CSV file.

    Args:
        records: The records to write.
        csv_path: Destination file path.
    """
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=RUNTIME_CSV_FIELDNAMES)
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))


# ==============================================================
# Main
# ==============================================================

def main() -> None:
    """Parse CLI arguments and run the requested runtime experiment(s)."""
    parser = argparse.ArgumentParser(
        prog="python -m benchmarks.runtime",
        description="Jason runtime scalability benchmarks.",
    )
    parser.add_argument(
        "command", choices=["run", "list"],
        help="'run' executes experiments; 'list' shows available experiment names.",
    )
    parser.add_argument(
        "experiment", nargs="?", default=None,
        help="Experiment name to run, or omit when using --all.",
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Run all registered runtime experiments sequentially.",
    )
    parser.add_argument(
        "--duration", type=float, default=10.0,
        help="Measurement window in seconds per run (default: 10).",
    )
    parser.add_argument(
        "--interval", type=float, default=0.5,
        help="Sampling interval in seconds (default: 0.5).",
    )
    parser.add_argument(
        "--out", type=Path, default=None,
        help="Output CSV path. Defaults to runtime_<experiment>_<timestamp>.csv",
    )

    args = parser.parse_args()

    if args.command == "list":
        print("Available runtime experiments:")
        for name in RUNTIME_EXPERIMENTS:
            configs = RUNTIME_EXPERIMENTS[name]
            print(f"  {name:<30} ({len(configs)} runs)")
        return

    # Determine which experiments to run
    if args.all:
        to_run = list(RUNTIME_EXPERIMENTS.keys())
    elif args.experiment:
        if args.experiment not in RUNTIME_EXPERIMENTS:
            print(f"ERROR: Unknown experiment '{args.experiment}'.", file=sys.stderr)
            print(f"Available: {', '.join(RUNTIME_EXPERIMENTS)}", file=sys.stderr)
            sys.exit(1)
        to_run = [args.experiment]
    else:
        parser.print_help()
        sys.exit(1)

    all_records: List[RuntimeRecord] = []

    for exp_name in to_run:
        configs_and_counts = RUNTIME_EXPERIMENTS[exp_name]
        print(f"\n{'='*60}")
        print(f"  Running experiment: {exp_name}")
        print(f"  Runs: {len(configs_and_counts)}  |  "
              f"Duration/run: {args.duration}s  |  "
              f"Interval: {args.interval}s")
        print(f"{'='*60}")

        records = run_runtime_experiment(
            experiment_name=exp_name,
            configs_and_counts=configs_and_counts,
            measure_duration_s=args.duration,
            sample_interval_s=args.interval,
        )
        all_records.extend(records)

    # Determine output path
    if args.out:
        csv_path = args.out
    else:
        exp_label = "_".join(to_run) if len(to_run) <= 2 else "all"
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = Path(f"runtime_{exp_label}_{ts}.csv")

    save_csv(all_records, csv_path)

    successful = sum(1 for r in all_records if r.success)
    print(f"\n{'='*60}")
    print(f"  Done. {successful}/{len(all_records)} runs succeeded.")
    print(f"  Results saved to: {csv_path.resolve()}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
