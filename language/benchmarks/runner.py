"""
Benchmark runner and result record types for the Regia benchmark suite.

Responsibilities:
- BenchmarkRecord: one CSV row (all config fields + all measured metrics).
- warmup()        : prime the Lark LALR table before timing starts.
- run_experiment(): drive a list of GeneratorConfigs, collect records.
- save_csv()      : write records to a CSV file.
"""

import csv
import hashlib
import json
import logging
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List

from regia.compiler import compile_source, compile_file

from .config import GeneratorConfig
from .generator import generate
from .import_generator import generate_import_graph
from .metrics import count_loc, count_output_loc, measure_time_and_ram, get_system_info


# ======================================================
# Result Data Model
# ======================================================

@dataclass
class BenchmarkRecord:
    """
    One row in the output CSV: a single timed compilation run.

    Contains every GeneratorConfig field (for reproducibility) plus
    all measured metrics.  Fields are written to CSV in declaration order.

    Args:
        experiment: Name of the experiment suite (e.g. 'scale_roles').
        run_id: Monotonically increasing integer across all runs.
        n_actions: From GeneratorConfig.
        n_events: From GeneratorConfig.
        n_facts: From GeneratorConfig.
        n_playbooks: From GeneratorConfig.
        n_plans_per_playbook: From GeneratorConfig.
        n_branches_per_plan: From GeneratorConfig.
        n_stmts_per_branch: From GeneratorConfig.
        n_roles: From GeneratorConfig.
        n_phases: From GeneratorConfig.
        n_subplot_breadth: From GeneratorConfig.
        n_subplot_depth: From GeneratorConfig.
        seed: From GeneratorConfig.
        input_loc: Lines of Regia source code.
        input_bytes: Byte size of the Regia source (UTF-8).
        output_files: Number of .asl files emitted.
        output_loc_total: Sum of lines across all emitted files.
        output_loc_per_file: JSON string mapping filename to line count.
        loc_ratio: output_loc_total / input_loc.
        compile_time_s: Wall-clock compile time in seconds.
        peak_ram_mb: tracemalloc peak heap during compilation (MB).
        success: Whether compilation produced zero errors.
        warning_count: Number of compiler warnings.
        error_count: Number of compiler errors.
    """

    # ================== Experiment metadata ==================
    experiment: str
    run_id: int
    
    # ================== System info ==================
    sys_os: str
    sys_cpu: str
    sys_cores: int
    sys_ram_gb: float
    sys_python: str

    # ================== Generator config ==================
    n_actions: int
    n_events: int
    n_facts: int
    n_playbooks: int
    n_plans_per_playbook: int
    n_branches_per_plan: int
    n_stmts_per_branch: int
    n_roles: int
    n_phases: int
    n_subplot_breadth: int
    n_subplot_depth: int
    seed: int

    # ================== Input metrics ==================
    input_loc: int
    input_bytes: int

    # ================== Output metrics ==================
    output_files: int
    output_loc_total: int
    output_loc_per_file: str    # JSON: {filename: loc}
    loc_ratio: float

    # ================== Performance metrics ==================
    compile_time_s: float
    io_time_s: float
    peak_ram_mb: float

    # ================== Compilation result ==================
    success: bool
    warning_count: int
    error_count: int


CSV_FIELDNAMES: List[str] = list(BenchmarkRecord.__dataclass_fields__.keys())


# ======================================================
# Warm-up
# ======================================================

_warmed_up: bool = False


def warmup() -> None:
    """
    Compile a trivial program once to warm up the Lark LALR table.

    The Lark parser builds its LALR tables on first use and caches them.
    Without a warm-up, the first timed run would include this one-time
    overhead, skewing its result.  Subsequent calls are no-ops.
    """
    global _warmed_up
    if _warmed_up:
        return
    compile_source("ACTION warmup_act.", emit=True)
    _warmed_up = True


# ======================================================
# Experiment Runner
# ======================================================

def run_experiment(
    experiment_name: str,
    configs: List[GeneratorConfig],
    output_dir: Path,
) -> List[BenchmarkRecord]:
    """
    Run a named experiment suite over all given configs.

    For each config:
    1. Generates the Regia source once (outside the timed loop).
    2. Saves the source to output_dir for reproducibility.
    3. Runs the compiler n_reps times, collecting one BenchmarkRecord per rep.

    Args:
        experiment_name: Human-readable experiment name (used in CSV + filenames).
        configs: Ordered list of GeneratorConfig instances defining the sweep.
        output_dir: Directory where generated .regia source files are saved.

    Returns:
        List of BenchmarkRecord instances, one per (config, rep) pair.
    """
    warmup()
    output_dir.mkdir(parents=True, exist_ok=True)

    records: List[BenchmarkRecord] = []
    global_run_id: int = 0

    for cfg in configs:
        source: str = generate(cfg)
        _save_source(source, cfg, experiment_name, output_dir)

        for rep in range(cfg.n_reps):
            record = _run_single(experiment_name, global_run_id, cfg, source)
            records.append(record)
            global_run_id += 1
            _print_progress(experiment_name, cfg, rep + 1, cfg.n_reps, record)

    return records


def save_csv(records: List[BenchmarkRecord], csv_path: Path) -> None:
    """
    Write benchmark records to a CSV file.

    Creates parent directories if they do not exist.

    Args:
        records: The records to write (one row each).
        csv_path: Destination file path.
    """
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))


# ======================================================
# Private Helpers
# ======================================================

def _run_single(
    experiment_name: str,
    run_id: int,
    cfg: GeneratorConfig,
    source: str,
) -> BenchmarkRecord:
    """
    Execute one timed compilation and return the populated BenchmarkRecord.

    Args:
        experiment_name: Experiment suite name.
        run_id: Monotonically increasing run identifier.
        cfg: The configuration for this run.
        source: Pre-generated Regia source string.

    Returns:
        A fully populated BenchmarkRecord.
    """
    if cfg.n_import_nodes > 0:
        import_files = generate_import_graph(cfg)
        input_loc = sum(len(content.splitlines()) for content in import_files.values())
        input_bytes = sum(len(content.encode("utf-8")) for content in import_files.values())
        
        def _compile() -> object:
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_path = Path(tmpdir)
                for fname, fcontent in import_files.items():
                    (tmp_path / fname).write_text(fcontent, encoding="utf-8")
                    
                entry_file = tmp_path / "file_0.regia"
                return compile_file(str(entry_file))
                
        compile_result, wall_time, peak_mb = measure_time_and_ram(_compile)
    else:
        input_loc = count_loc(source)
        input_bytes = len(source.encode("utf-8"))
    
        def _compile() -> object:
            return compile_source(source, emit=True)
    
        compile_result, wall_time, peak_mb = measure_time_and_ram(_compile)

    output_files: int = 0
    output_loc_total: int = 0
    output_loc_per_file: str = "{}"
    loc_ratio: float = 0.0
    io_time_s: float = 0.0

    if compile_result.success and compile_result.outputs:
        output_files = len(compile_result.outputs)
        output_loc_total, per_file_dict = count_output_loc(compile_result.outputs)
        output_loc_per_file = json.dumps(per_file_dict)
        loc_ratio = output_loc_total / max(input_loc, 1)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            t_start = time.perf_counter()
            for fname, fcontent in compile_result.outputs.items():
                (tmp_path / fname).write_text(fcontent, encoding="utf-8")
            io_time_s = time.perf_counter() - t_start

    sys_info = get_system_info()

    return BenchmarkRecord(
        experiment=experiment_name,
        run_id=run_id,
        sys_os=sys_info["sys_os"],
        sys_cpu=sys_info["sys_cpu"],
        sys_cores=sys_info["sys_cores"],
        sys_ram_gb=sys_info["sys_ram_gb"],
        sys_python=sys_info["sys_python"],
        n_actions=cfg.n_actions,
        n_events=cfg.n_events,
        n_facts=cfg.n_facts,
        n_playbooks=cfg.n_playbooks,
        n_plans_per_playbook=cfg.n_plans_per_playbook,
        n_branches_per_plan=cfg.n_branches_per_plan,
        n_stmts_per_branch=cfg.n_stmts_per_branch,
        n_roles=cfg.n_roles,
        n_phases=cfg.n_phases,
        n_subplot_breadth=cfg.n_subplot_breadth,
        n_subplot_depth=cfg.n_subplot_depth,
        seed=cfg.seed,
        input_loc=input_loc,
        input_bytes=input_bytes,
        output_files=output_files,
        output_loc_total=output_loc_total,
        output_loc_per_file=output_loc_per_file,
        loc_ratio=loc_ratio,
        compile_time_s=wall_time,
        io_time_s=io_time_s,
        peak_ram_mb=peak_mb,
        success=compile_result.success,
        warning_count=compile_result.warning_count,
        error_count=compile_result.error_count,
    )


def _save_source(
    source: str,
    cfg: GeneratorConfig,
    experiment: str,
    output_dir: Path,
) -> None:
    """
    Save the generated Regia source to disk for offline inspection.

    The filename encodes the experiment name and a SHA-256 hash of the
    canonical config string, guaranteeing uniqueness without collisions
    even if multiple experiments share the same parameter values.

    Args:
        source: Regia source string to save.
        cfg: The config that produced this source.
        experiment: The experiment suite name.
        output_dir: Destination directory.
    """
    canonical = (
        f"{experiment}_{cfg.n_actions}_{cfg.n_events}_{cfg.n_facts}"
        f"_{cfg.n_playbooks}_{cfg.n_plans_per_playbook}"
        f"_{cfg.n_branches_per_plan}_{cfg.n_stmts_per_branch}"
        f"_{cfg.n_roles}_{cfg.n_phases}"
        f"_{cfg.n_subplot_breadth}_{cfg.n_subplot_depth}"
        f"_{cfg.seed}"
    )
    hash_hex = hashlib.sha256(canonical.encode()).hexdigest()[:12]
    filename = f"{experiment}_{hash_hex}.regia"
    (output_dir / filename).write_text(source, encoding="utf-8")


def _print_progress(
    experiment: str,
    cfg: GeneratorConfig,
    rep: int,
    n_reps: int,
    record: BenchmarkRecord,
) -> None:
    """
    Print a compact one-line progress update to stdout.

    Args:
        experiment: Experiment suite name.
        cfg: The configuration being run.
        rep: Current repetition number (1-based).
        n_reps: Total repetitions for this config.
        record: The just-completed BenchmarkRecord.
    """
    status = "OK  " if record.success else "FAIL"
    print(
        f"  [{experiment}] rep {rep}/{n_reps}  "
        f"roles={cfg.n_roles:<4} pbs={cfg.n_playbooks:<3} "
        f"phases={cfg.n_phases:<3} "
        f"sub={cfg.n_subplot_breadth}x{cfg.n_subplot_depth}  "
        f"-> {status}  "
        f"t={record.compile_time_s:.4f}s (io={record.io_time_s:.4f}s)  "
        f"ram={record.peak_ram_mb:.2f}MB  "
        f"loc={record.input_loc}->{record.output_loc_total} ({record.loc_ratio:.1f}x)",
        file=sys.stdout,
        flush=True,
    )
