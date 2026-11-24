"""
jcm_generator.py -- Generate the .jcm and Gradle build for Jason runtime benchmarks.

Given the output files of the Regia compiler, generates a self-contained
JaCaMo Multi-Agent System descriptor (.jcm) and a minimal Kotlin Gradle build.
The build runs on the same JDK 21 toolchain as science_game/minds and is
launched with that project's Gradle wrapper (see runtime_runner.py).
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
        asl_subdir: Directory holding the .asl files, listed as the asl-path.

    Returns:
        The .jcm file content as a string.
    """
    plot_name, director_file = _extract_director(output_files)
    roles = _extract_roles(output_files)

    lines: List[str] = [f"mas {plot_name}_benchmark {{", ""]

    # Role agent declarations
    for role_name, role_file in roles:
        for i in range(n_agents_per_role):
            agent_id = f"{role_name}_{i}"
            lines.append(f"    agent {agent_id}:{role_file} {{}}")
        lines.append("")

    # Director declaration with start_plot goal
    lines.append(f"    agent director:{director_file} {{")

    # Build the start_plot bindings: map(role0, [role0_0, role0_1, ...])
    bindings: List[str] = []
    for role_name, _ in roles:
        agents = ", ".join(f"{role_name}_{i}" for i in range(n_agents_per_role))
        bindings.append(f"map({role_name}, [{agents}])")

    bindings_str = ", ".join(bindings)
    lines.append(f"        goals: start_plot([{bindings_str}])")
    lines.append("    }")
    lines.append("")

    # asl-path must come after the agents (JaCaMo 1.2 parser). It also lets
    # .create_agent find subplot directors by bare name.
    lines.append(f'    asl-path: "{asl_subdir}"')
    lines.append("}")

    return "\n".join(lines) + "\n"


# ==============================================================
# Gradle build generation
# ==============================================================

_SETTINGS_GRADLE: str = """\
plugins {
    // Downloads the JDK 21 toolchain when no matching JDK is installed.
    id("org.gradle.toolchains.foojay-resolver-convention") version "1.0.0"
}

rootProject.name = "regia-benchmark"
"""

_BUILD_GRADLE_TEMPLATE: str = """\
plugins {
    java
}

defaultTasks("run")

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    maven { url = uri("https://raw.githubusercontent.com/jacamo-lang/mvn-repo/master") }
    maven { url = uri("https://repo.gradle.org/gradle/libs-releases") }
    mavenCentral()
}

dependencies {
    implementation("org.jacamo:jacamo:1.2")
}

tasks.register<JavaExec>("run") {
    description = "Jason runtime benchmark"
    group = "Benchmark"
    dependsOn("classes")
    mainClass = "jacamo.infra.JaCaMoLauncher"
    args("@JCM_NAME@")
    classpath = sourceSets.main.get().runtimeClasspath
    javaLauncher = javaToolchains.launcherFor(java.toolchain)
    standardOutput = System.out
    errorOutput = System.err
    jvmArgs("-Xss8m")       // Prevent stack overflow on deep subplot hierarchies
    jvmArgs("-Xms64m")      // Small initial heap so RSS reflects actual usage
    jvmArgs("-Xmx512m")     // Cap max heap so growth is visible in RSS measurements
}

// Downloads everything `run` needs, so that no download is ever measured.
tasks.register("prepare") {
    description = "Resolves the JDK toolchain and the runtime classpath"
    group = "Benchmark"
    val launcher = javaToolchains.launcherFor(java.toolchain)
    val runtime = sourceSets.main.get().runtimeClasspath
    doLast {
        launcher.get()
        runtime.files
    }
}
"""


def generate_build_gradle(jcm_name: str = "benchmark.jcm") -> str:
    """
    Generate a minimal build.gradle.kts for running Jason without Vesna.

    Args:
        jcm_name: Filename of the .jcm file to pass to JaCaMoLauncher.

    Returns:
        The build.gradle.kts content as a string.
    """
    return _BUILD_GRADLE_TEMPLATE.replace("@JCM_NAME@", jcm_name)


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
        <target_dir>/build.gradle.kts
        <target_dir>/settings.gradle.kts

    Args:
        output_files: Compiler output dict (filename -> content).
        target_dir: Root directory to write into (must exist).
        n_agents_per_role: Agent instances per role in the .jcm.
        jcm_name: Filename for the generated .jcm.
    """
    gen_dir = target_dir / "gen"
    gen_dir.mkdir(parents=True, exist_ok=True)

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

    # Write the Gradle build
    gradle_content = generate_build_gradle(jcm_name=jcm_name)
    (target_dir / "build.gradle.kts").write_text(gradle_content, encoding="utf-8")
    (target_dir / "settings.gradle.kts").write_text(_SETTINGS_GRADLE, encoding="utf-8")
