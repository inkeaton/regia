"""
jcm_generator.py -- Generate .jcm and build.gradle for Jason runtime benchmarks.

Given the output files of the Regia compiler, generates a self-contained
JaCaMo Multi-Agent System descriptor (.jcm) and a minimal build.gradle.
No Vesna/WebSocket infrastructure is required -- agents run in Jason's
standard centralised runtime.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple


# ==============================================================
# Role name extraction
# ==============================================================

def _extract_roles(output_files: Dict[str, str]) -> List[Tuple[str, str]]:
    """
    Derive (role_name, asl_filename) pairs from the compiler output dict.

    Role files are named 'role_<plotname>_<rolename>.asl'. The role_name
    is the last segment after the plot name prefix.

    Args:
        output_files: Mapping of filename -> content from compile_source().

    Returns:
        Sorted list of (role_name, filename) pairs.
    """
    pattern = re.compile(r"^role_[^_]+_(.+)\.asl$")
    roles: List[Tuple[str, str]] = []
    for fname in sorted(output_files.keys()):
        m = pattern.match(fname)
        if m:
            roles.append((m.group(1), fname))
    return roles


def _extract_director(output_files: Dict[str, str]) -> Tuple[str, str]:
    """
    Find the director .asl filename and extract the plot name from it.

    Args:
        output_files: Compiler output dict.

    Returns:
        (plot_name, director_filename) tuple.

    Raises:
        ValueError: If no director file is found.
    """
    pattern = re.compile(r"^director_(.+)\.asl$")
    for fname in output_files:
        m = pattern.match(fname)
        if m:
            return m.group(1), fname
    raise ValueError("No director_*.asl file found in compiler output.")


# ==============================================================
# JCM generation
# ==============================================================

def generate_jcm(
    output_files: Dict[str, str],
    n_agents_per_role: int = 1,
    asl_subdir: str = "gen",
) -> str:
    """
    Generate a JaCaMo .jcm descriptor string for the compiled agents.

    Each role gets n_agents_per_role agent instances (role0_0, role0_1, ...).
    The director receives a start_plot goal wiring all instances to their roles.
    No ports are declared (no VesnaAgent body needed).

    Args:
        output_files: Compiler output dict (filename -> asl content).
        n_agents_per_role: How many agent instances to spawn per role.
        asl_subdir: Subdirectory prefix for .asl paths in the .jcm.

    Returns:
        The .jcm file content as a string.
    """
    plot_name, director_file = _extract_director(output_files)
    roles = _extract_roles(output_files)

    lines: List[str] = [f"mas {plot_name}_benchmark {{", ""]

    # Role agent declarations
    for role_name, role_file in roles:
        asl_path = f"{asl_subdir}/{role_file}" if asl_subdir else role_file
        for i in range(n_agents_per_role):
            agent_id = f"{role_name}_{i}"
            lines.append(f"    agent {agent_id}:{asl_path} {{}}")
        lines.append("")

    # Director declaration with start_plot goal
    director_path = f"{asl_subdir}/{director_file}" if asl_subdir else director_file
    lines.append(f"    agent director:{director_path} {{")

    # Build the start_plot bindings: map(role0, [role0_0, role0_1, ...])
    bindings: List[str] = []
    for role_name, _ in roles:
        agents = ", ".join(f"{role_name}_{i}" for i in range(n_agents_per_role))
        bindings.append(f"map({role_name}, [{agents}])")

    bindings_str = ", ".join(bindings)
    lines.append(f"        goals: start_plot([{bindings_str}])")
    lines.append("    }")
    lines.append("}")

    return "\n".join(lines) + "\n"


# ==============================================================
# build.gradle generation
# ==============================================================

_BUILD_GRADLE_TEMPLATE = """\
defaultTasks 'run'
apply plugin: 'java'

repositories {{
    maven {{ url "https://raw.githubusercontent.com/jacamo-lang/mvn-repo/master" }}
    mavenCentral()
}}

dependencies {{
    implementation('org.jacamo:jacamo:1.2')
}}

task run(type: JavaExec, dependsOn: 'classes') {{
    description 'Jason runtime benchmark'
    group 'Benchmark'
    mainClass = 'jacamo.infra.JaCaMoLauncher'
    args '{jcm_name}'
    classpath sourceSets.main.runtimeClasspath
    standardOutput = System.out
    errorOutput    = System.err
    jvmArgs '-Xss8m'       // Prevent stack overflow on deep subplot hierarchies
    jvmArgs '-Xms64m'      // Small initial heap so RSS reflects actual usage
    jvmArgs '-Xmx512m'     // Cap max heap so growth is visible in RSS measurements
}}

sourceSets {{
    main {{
        java {{ srcDir 'src/' }}
    }}
}}
"""


def generate_build_gradle(jcm_name: str = "benchmark.jcm") -> str:
    """
    Generate a minimal build.gradle for running Jason without Vesna.

    Args:
        jcm_name: Filename of the .jcm file to pass to JaCaMoLauncher.

    Returns:
        The build.gradle content as a string.
    """
    return _BUILD_GRADLE_TEMPLATE.format(jcm_name=jcm_name)


# ==============================================================
# Convenience: write everything to a directory
# ==============================================================

def write_benchmark_project(
    output_files: Dict[str, str],
    target_dir: Path,
    n_agents_per_role: int = 1,
    jcm_name: str = "benchmark.jcm",
) -> None:
    """
    Write all files for a self-contained Gradle/Jason benchmark project.

    Creates:
        <target_dir>/gen/<all .asl files>
        <target_dir>/benchmark.jcm
        <target_dir>/build.gradle
        <target_dir>/src/  (empty, required by Gradle java plugin)

    Args:
        output_files: Compiler output dict (filename -> content).
        target_dir: Root directory to write into (must exist).
        n_agents_per_role: Agent instances per role in the .jcm.
        jcm_name: Filename for the generated .jcm.
    """
    gen_dir = target_dir / "gen"
    gen_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "src").mkdir(exist_ok=True)

    # Write all .asl files into gen/
    for fname, content in output_files.items():
        (gen_dir / fname).write_text(content, encoding="utf-8")

    # Write .jcm
    jcm_content = generate_jcm(
        output_files,
        n_agents_per_role=n_agents_per_role,
        asl_subdir="gen",
    )
    (target_dir / jcm_name).write_text(jcm_content, encoding="utf-8")

    # Write build.gradle
    gradle_content = generate_build_gradle(jcm_name=jcm_name)
    (target_dir / "build.gradle").write_text(gradle_content, encoding="utf-8")
