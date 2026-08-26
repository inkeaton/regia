"""
Performance measurement utilities for the Regia benchmark suite.

Provides:
- count_loc()           : Lines of code in a source string.
- count_output_loc()    : Lines across all compiler output files.
- measure_time_and_ram(): Wall-clock time + tracemalloc peak heap.
"""

import platform
import os
import subprocess
import time
import tracemalloc
from functools import lru_cache
from typing import Callable, Dict, Tuple, TypeVar, Any

T = TypeVar("T")

# ======================================================
# System Information
# ======================================================

@lru_cache(maxsize=1)
def get_system_info() -> Dict[str, Any]:
    """
    Retrieve OS-independent system details (OS, CPU, Cores, RAM, Python version).
    Uses standard library only.
    """
    info = {
        "sys_os": f"{platform.system()} {platform.release()}",
        "sys_cpu": platform.machine(),
        "sys_cores": os.cpu_count() or 0,
        "sys_ram_gb": 0.0,
        "sys_python": platform.python_version()
    }
    
    try:
        sys_name = platform.system().lower()
        if sys_name == "linux":
            if hasattr(os, 'sysconf') and 'SC_PHYS_PAGES' in os.sysconf_names and 'SC_PAGE_SIZE' in os.sysconf_names:
                total_bytes = os.sysconf('SC_PHYS_PAGES') * os.sysconf('SC_PAGE_SIZE')
                info["sys_ram_gb"] = round(total_bytes / (1024**3), 2)
        elif sys_name == "darwin":
            proc = subprocess.run(['sysctl', '-n', 'hw.memsize'], capture_output=True, text=True)
            if proc.returncode == 0:
                info["sys_ram_gb"] = round(int(proc.stdout.strip()) / (1024**3), 2)
        elif sys_name == "windows":
            proc = subprocess.run(['wmic', 'computersystem', 'get', 'TotalPhysicalMemory'], capture_output=True, text=True)
            if proc.returncode == 0:
                lines = proc.stdout.strip().split('\n')
                if len(lines) > 1:
                    info["sys_ram_gb"] = round(int(lines[1].strip()) / (1024**3), 2)
    except Exception:
        pass
        
    return info


# ======================================================
# LoC Counters
# ======================================================

def count_loc(source: str) -> int:
    """
    Count the total number of lines in a source string.

    Blank lines and comment lines are included so the result matches
    what most editors and wc -l report.

    Args:
        source: The source string to count.

    Returns:
        Number of lines (0 for an empty string).
    """
    if not source:
        return 0
    return source.count("\n") + 1


def count_output_loc(outputs: Dict[str, str]) -> Tuple[int, Dict[str, int]]:
    """
    Count lines of code across all compiler output files.

    Args:
        outputs: Mapping of filename to file content returned by compile_source().

    Returns:
        A tuple of (total_loc, per_file_loc) where per_file_loc maps
        each filename to its individual line count.
    """
    per_file: Dict[str, int] = {
        filename: count_loc(content) for filename, content in outputs.items()
    }
    total = sum(per_file.values())
    return total, per_file


# ======================================================
# Time and RAM Measurement
# ======================================================

def measure_time_and_ram(fn: Callable[[], T]) -> Tuple[T, float, float]:
    """
    Execute a callable and measure its wall-clock time and peak heap allocation.

    Uses tracemalloc to capture the peak memory allocated *during* the call.
    This isolates the compiler's own heap pressure from total process RSS,
    making results comparable across different system states.

    Args:
        fn: A zero-argument callable to execute and measure.

    Returns:
        A tuple of (result, wall_time_seconds, peak_ram_mb).
    """
    tracemalloc.start()
    t_start = time.perf_counter()

    result = fn()

    t_end = time.perf_counter()
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    wall_time: float = t_end - t_start
    peak_mb: float = peak_bytes / (1024.0 * 1024.0)

    return result, wall_time, peak_mb
