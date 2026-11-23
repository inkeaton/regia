"""
process_utils.py -- Shared JVM process discovery utilities.

Used by both science_game/monitor.py and the runtime benchmark runner
to locate Gradle/Jason JVM processes by scanning the process list rather
than walking child-process trees (which misses the Gradle daemon).
"""

import os
import time
from typing import Dict, List

import psutil


# ==============================================================
# JVM identification markers
# ==============================================================

# A java process is considered a Jason/Gradle process if ANY of these
# strings appear in its full command line.
JVM_MARKERS: List[str] = [
    "science_game",
    "benchmark",
    "jason",
    "GradleDaemon",
    "org.gradle",
    "jacamo",
    "JaCaMo",
]


# ==============================================================
# Username helper
# ==============================================================

def current_username() -> str:
    """
    Return the OS username of the current process.

    Returns:
        Username string, or empty string if detection fails.
    """
    try:
        return psutil.Process().username()
    except Exception:
        return os.environ.get("USER", "")


# ==============================================================
# Process discovery
# ==============================================================

def find_jason_processes(username: str) -> Dict[int, psutil.Process]:
    """
    Scan all running processes for Java processes owned by 'username'
    whose command line contains at least one JVM_MARKER.

    Args:
        username: OS username to filter by.

    Returns:
        Dict mapping pid -> psutil.Process for all matching processes.
    """
    found: Dict[int, psutil.Process] = {}
    for proc in psutil.process_iter(["pid", "name", "cmdline", "username"]):
        try:
            info = proc.info
            if info["username"] != username:
                continue
            if info["name"] not in ("java", "java.exe"):
                continue
            cmdline = " ".join(info["cmdline"] or [])
            if any(marker in cmdline for marker in JVM_MARKERS):
                found[proc.pid] = proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return found


def wait_for_jvm(username: str, timeout_s: float = 20.0) -> Dict[int, psutil.Process]:
    """
    Block until at least one matching Jason JVM process appears, or timeout.

    Args:
        username: OS username to filter by.
        timeout_s: Maximum seconds to wait before giving up.

    Returns:
        Dict of found processes (empty if timed out).
    """
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        found = find_jason_processes(username)
        if found:
            return found
        time.sleep(0.5)
    return {}
