"""
runtime_runner.py -- Jason runtime benchmark runner.

For each (GeneratorConfig, n_agents_per_role) pair:
  1. Generates Regia source via the benchmark generator.
  2. Compiles it to AgentSpeak (.asl) files.
  3. Writes a self-contained Gradle/Jason project to a temp directory.
  4. Launches 'gradle run --no-daemon' and waits for the JVM.
  5. Samples RSS and CPU for a fixed measurement window.
  6. Terminates the process and returns a RuntimeRecord.
"""

import subprocess
import tempfile
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import psutil

from regia.compiler import compile_source

from ..config import GeneratorConfig
from ..generator import generate
from .jcm_generator import write_benchmark_project
from .process_utils import current_username, find_jason_processes, wait_for_jvm


# ==============================================================
# Result data model
# ==============================================================

@dataclass
class RuntimeRecord:
    """
    One row in the runtime benchmark CSV.

    Contains experiment metadata, GeneratorConfig parameters, and
    all measured JVM resource metrics for one benchmark run.

    Args:
        experiment: Name of the experiment suite.
        run_id: Monotonically increasing run index.
        n_agents_per_role: Copies of each role agent spawned.
        n_total_agents: Total agent count including the director.
        measure_duration_s: Requested measurement window in seconds.
        n_samples: Number of RSS/CPU samples collected.
        jvm_found_s: Seconds elapsed before the JVM process appeared.
        rss_peak_mb: Peak RSS (MB) across the measurement window.
        rss_mean_mb: Mean RSS (MB) across the measurement window.
        rss_baseline_mb: First-sample RSS (MB), during JVM class loading.
        rss_settled_mb: Mean RSS of the last 20% of samples (idle state).
        cpu_total_s: Total CPU seconds consumed (user+sys) during window.
        cpu_peak_pct: Peak per-interval CPU% (normalised per core).
        cpu_mean_pct: Mean per-interval CPU% over the window.
        success: Whether compilation succeeded and JVM was found.
        n_roles: From GeneratorConfig.
        n_phases: From GeneratorConfig.
        n_playbooks: From GeneratorConfig.
        n_plans_per_playbook: From GeneratorConfig.
        n_branches_per_plan: From GeneratorConfig.
        n_stmts_per_branch: From GeneratorConfig.
    """

    # ================== Experiment metadata ==================
    experiment: str
    run_id: int

    # ================== Scale parameters ==================
    n_agents_per_role: int
    n_total_agents: int

    # ================== GeneratorConfig fields ==================
    n_roles: int
    n_phases: int
    n_playbooks: int
    n_plans_per_playbook: int
    n_branches_per_plan: int
    n_stmts_per_branch: int

    # ================== Timing ==================
    measure_duration_s: float
    n_samples: int
    jvm_found_s: float

    # ================== RSS metrics ==================
    rss_peak_mb: float
    rss_mean_mb: float
    rss_baseline_mb: float
    rss_settled_mb: float

    # ================== CPU metrics ==================
    cpu_total_s: float
    cpu_peak_pct: float
    cpu_mean_pct: float

    # ================== Status ==================
    success: bool


RUNTIME_CSV_FIELDNAMES: List[str] = list(RuntimeRecord.__dataclass_fields__.keys())


# ==============================================================
# Sampling logic
# ==============================================================

# Module-level state for cpu_times delta computation (reset per run).
_prev_cpu_times: Dict[int, Tuple[float, float]] = {}
_prev_sample_time: float = 0.0


def _reset_cpu_state() -> None:
    """Clear per-run CPU delta state."""
    global _prev_cpu_times, _prev_sample_time
    _prev_cpu_times = {}
    _prev_sample_time = 0.0


def _snapshot(
    cache: Dict[int, psutil.Process],
    now: float,
    num_cpus: int,
) -> Optional[Tuple[float, float, float]]:
    """
    Take a single RSS+CPU snapshot across all cached processes.

    Args:
        cache: Active {pid: Process} dict.
        now: Current time.monotonic() value.
        num_cpus: Logical CPU core count for % normalisation.

    Returns:
        (rss_mb, cpu_delta_s, avg_cpu_pct) or None if cache is empty.
    """
    global _prev_cpu_times, _prev_sample_time

    if not cache:
        return None

    elapsed = now - _prev_sample_time if _prev_sample_time > 0 else 1.0
    total_rss: int = 0
    total_cpu_delta: float = 0.0

    for pid, proc in list(cache.items()):
        try:
            total_rss += proc.memory_info().rss
            ct = proc.cpu_times()
            cur = (ct.user, ct.system)
            if pid in _prev_cpu_times:
                prev = _prev_cpu_times[pid]
                total_cpu_delta += max(0.0, (cur[0] - prev[0]) + (cur[1] - prev[1]))
            _prev_cpu_times[pid] = cur
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            _prev_cpu_times.pop(pid, None)

    _prev_sample_time = now
    rss_mb = total_rss / (1024.0 * 1024.0)
    avg_cpu = (total_cpu_delta / elapsed / num_cpus) * 100.0
    return rss_mb, total_cpu_delta, avg_cpu


def _refresh_cache(username: str, cache: Dict[int, psutil.Process]) -> None:
    """Add new JVM processes to cache and prune dead ones."""
    live = find_jason_processes(username)
    for pid, proc in live.items():
        if pid not in cache:
            cache[pid] = proc
    for pid in [p for p in cache if p not in live]:
        del cache[pid]


# ==============================================================
# Core runner
# ==============================================================

def run_runtime_benchmark(
    experiment: str,
    run_id: int,
    cfg: GeneratorConfig,
    n_agents_per_role: int,
    measure_duration_s: float = 10.0,
    sample_interval_s: float = 0.5,
) -> RuntimeRecord:
    """
    Execute one runtime benchmark run and return its RuntimeRecord.

    Args:
        experiment: Human-readable experiment name.
        run_id: Monotonic run counter for CSV identification.
        cfg: Regia GeneratorConfig controlling code complexity.
        n_agents_per_role: Agent copies per role in the generated .jcm.
        measure_duration_s: How long to sample after the JVM appears.
        sample_interval_s: Time between RSS/CPU samples.

    Returns:
        A fully populated RuntimeRecord (success=False on failure).
    """
    username = current_username()
    num_cpus = psutil.cpu_count(logical=True) or 1
    n_roles = cfg.n_roles
    n_total_agents = n_roles * n_agents_per_role + 1  # +1 for director

    _failure = RuntimeRecord(
        experiment=experiment, run_id=run_id,
        n_agents_per_role=n_agents_per_role, n_total_agents=n_total_agents,
        n_roles=cfg.n_roles, n_phases=cfg.n_phases,
        n_playbooks=cfg.n_playbooks, n_plans_per_playbook=cfg.n_plans_per_playbook,
        n_branches_per_plan=cfg.n_branches_per_plan, n_stmts_per_branch=cfg.n_stmts_per_branch,
        measure_duration_s=measure_duration_s, n_samples=0, jvm_found_s=0.0,
        rss_peak_mb=0.0, rss_mean_mb=0.0, rss_baseline_mb=0.0, rss_settled_mb=0.0,
        cpu_total_s=0.0, cpu_peak_pct=0.0, cpu_mean_pct=0.0, success=False,
    )

    # ============================================================
    # Step 1: Generate and compile Regia source
    # ============================================================
    try:
        source = generate(cfg)
        result = compile_source(source, emit=True)
        if not result.success or not result.outputs:
            print(f"  [runtime] run {run_id}: Compilation failed.")
            return _failure
    except Exception as exc:
        print(f"  [runtime] run {run_id}: Compilation error: {exc}")
        return _failure

    # ============================================================
    # Step 2: Write project to a temp directory and launch Gradle
    # ============================================================
    with tempfile.TemporaryDirectory(prefix="regia_bench_") as tmpdir:
        tmp_path = Path(tmpdir)
        write_benchmark_project(
            result.outputs,
            tmp_path,
            n_agents_per_role=n_agents_per_role,
        )

        launch_start = time.monotonic()
        proc = subprocess.Popen(
            ["gradle", "run", "--no-daemon"],
            cwd=str(tmp_path),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # ============================================================
        # Step 3: Wait for JVM to appear
        # ============================================================
        jvm_procs = wait_for_jvm(username, timeout_s=30.0)
        jvm_found_s = round(time.monotonic() - launch_start, 3)

        if not jvm_procs:
            print(f"  [runtime] run {run_id}: JVM never appeared (timeout).")
            proc.terminate()
            proc.wait(timeout=10)
            return _failure

        # ============================================================
        # Step 4: Sample RSS/CPU for the measurement window
        # ============================================================
        _reset_cpu_state()
        cache: Dict[int, psutil.Process] = dict(jvm_procs)

        # Baseline cpu_times snapshot (before first measurement sample)
        for p in list(cache.values()):
            try:
                ct = p.cpu_times()
                _prev_cpu_times[p.pid] = (ct.user, ct.system)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        _prev_sample_time = time.monotonic()

        samples_rss: List[float] = []
        samples_cpu_delta: List[float] = []
        samples_cpu_pct: List[float] = []

        deadline = time.monotonic() + measure_duration_s
        while time.monotonic() < deadline:
            time.sleep(sample_interval_s)
            _refresh_cache(username, cache)
            snap = _snapshot(cache, time.monotonic(), num_cpus)
            if snap:
                rss_mb, cpu_delta, cpu_pct = snap
                samples_rss.append(rss_mb)
                samples_cpu_delta.append(cpu_delta)
                samples_cpu_pct.append(cpu_pct)

        # ============================================================
        # Step 5: Terminate gracefully
        # ============================================================
        try:
            proc.terminate()
            proc.wait(timeout=10)
        except (subprocess.TimeoutExpired, OSError):
            proc.kill()

        # Kill any lingering JVM daemon processes
        for pid, p in list(cache.items()):
            try:
                p.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    # ============================================================
    # Step 6: Compute derived metrics
    # ============================================================
    n = len(samples_rss)
    if n == 0:
        return _failure

    settled_start = max(0, int(n * 0.8))
    rss_settled = (
        sum(samples_rss[settled_start:]) / len(samples_rss[settled_start:])
        if samples_rss[settled_start:] else samples_rss[-1]
    )

    return RuntimeRecord(
        experiment=experiment, run_id=run_id,
        n_agents_per_role=n_agents_per_role, n_total_agents=n_total_agents,
        n_roles=cfg.n_roles, n_phases=cfg.n_phases,
        n_playbooks=cfg.n_playbooks, n_plans_per_playbook=cfg.n_plans_per_playbook,
        n_branches_per_plan=cfg.n_branches_per_plan, n_stmts_per_branch=cfg.n_stmts_per_branch,
        measure_duration_s=measure_duration_s,
        n_samples=n,
        jvm_found_s=jvm_found_s,
        rss_peak_mb=max(samples_rss),
        rss_mean_mb=sum(samples_rss) / n,
        rss_baseline_mb=samples_rss[0],
        rss_settled_mb=rss_settled,
        cpu_total_s=sum(samples_cpu_delta),
        cpu_peak_pct=max(samples_cpu_pct),
        cpu_mean_pct=sum(samples_cpu_pct) / n,
        success=True,
    )


# ==============================================================
# Batch runner
# ==============================================================

def run_runtime_experiment(
    experiment_name: str,
    configs_and_counts: List[Tuple[GeneratorConfig, int]],
    measure_duration_s: float = 10.0,
    sample_interval_s: float = 0.5,
) -> List[RuntimeRecord]:
    """
    Run a named experiment suite over a list of (config, n_agents) pairs.

    Args:
        experiment_name: Label for the CSV and progress output.
        configs_and_counts: Ordered list of (GeneratorConfig, n_agents_per_role).
        measure_duration_s: Measurement window per run.
        sample_interval_s: Sample frequency.

    Returns:
        List of RuntimeRecord instances, one per run.
    """
    records: List[RuntimeRecord] = []
    for run_id, (cfg, n_agents) in enumerate(configs_and_counts):
        n_total = cfg.n_roles * n_agents + 1
        print(
            f"  [{experiment_name}] run {run_id:3d}  "
            f"roles={cfg.n_roles:<4} agents/role={n_agents:<4} "
            f"total_agents={n_total:<5} ...",
            end="", flush=True,
        )
        record = run_runtime_benchmark(
            experiment=experiment_name,
            run_id=run_id,
            cfg=cfg,
            n_agents_per_role=n_agents,
            measure_duration_s=measure_duration_s,
            sample_interval_s=sample_interval_s,
        )
        status = "OK  " if record.success else "FAIL"
        print(
            f" {status}  "
            f"rss_settled={record.rss_settled_mb:.0f}MB  "
            f"cpu_total={record.cpu_total_s:.2f}s  "
            f"jvm_found={record.jvm_found_s:.1f}s",
            flush=True,
        )
        records.append(record)
    return records
