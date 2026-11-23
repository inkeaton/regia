"""
runtime_experiments.py -- Experiment suite definitions for Jason runtime benchmarks.

Two experiment types:
  scale_agents -- Fixed BASELINE code complexity, increasing N copies per role.
                  Isolates per-agent JVM cost from code complexity.
  scale_roles  -- Increasing n_roles in GeneratorConfig, 1 agent per role.
                  Measures how director broadcast cost scales with role count.
"""

from dataclasses import replace
from typing import Dict, List, Tuple

from ..config import GeneratorConfig


# ==============================================================
# Baseline configuration
# ==============================================================

# Keep code complexity minimal for the runtime benchmark -- we are
# measuring JVM/agent overhead, not Regia language expressiveness.
RUNTIME_BASELINE: GeneratorConfig = GeneratorConfig(
    n_actions=5,
    n_events=5,
    n_facts=2,
    n_playbooks=1,
    n_plans_per_playbook=1,
    n_branches_per_plan=0,
    n_stmts_per_branch=1,
    n_roles=2,
    n_phases=2,
    n_subplot_breadth=0,
    n_subplot_depth=0,
    seed=42,
    n_reps=1,  # Runtime benchmarks don't loop internally; call run_runtime_experiment multiple times.
)


# ==============================================================
# Experiment definitions
# ==============================================================

# Each entry is a List of (GeneratorConfig, n_agents_per_role) pairs.
RUNTIME_EXPERIMENTS: Dict[str, List[Tuple[GeneratorConfig, int]]] = {

    # ---- scale_agents ----
    # Fixed 2-role BASELINE config. Vary number of agent instances per role.
    # Measures: marginal per-agent memory cost, thread overhead.
    # Expected: linear RSS growth with n_total_agents.
    "scale_agents": [
        (RUNTIME_BASELINE, n)
        for n in [1, 2, 5, 10, 20, 50]
    ],

    # ---- scale_roles ----
    # One agent instance per role. Vary n_roles in GeneratorConfig.
    # Measures: director broadcast cost, plan-base loading per role file.
    # Expected: linear RSS growth; possible CPU spike during !on_enter broadcast.
    "scale_roles": [
        (replace(RUNTIME_BASELINE, n_roles=n), 1)
        for n in [1, 2, 5, 10, 20, 50]
    ],

    # ---- scale_agents_complex ----
    # Same as scale_agents but with higher code complexity (more playbooks/plans).
    # Measures: whether plan-base size affects per-agent memory footprint.
    "scale_agents_complex": [
        (replace(RUNTIME_BASELINE, n_playbooks=5, n_plans_per_playbook=5, n_branches_per_plan=2), n)
        for n in [1, 2, 5, 10, 20]
    ],
}
