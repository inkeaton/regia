"""
Named experiment suite definitions for the Regia scalability benchmark.

Each suite varies exactly ONE GeneratorConfig field across a range of values
while holding all others at the BASELINE.  This isolates the contribution of
each structural dimension to compilation cost.

Usage in the CLI:
    python -m benchmarks run scale_roles
    python -m benchmarks run --all
"""

import itertools
from dataclasses import replace
from typing import Dict, List

from .config import GeneratorConfig


# ======================================================
# Baseline Configuration
# ======================================================

BASELINE: GeneratorConfig = GeneratorConfig(
    n_actions=10,
    n_events=10,
    n_facts=5,
    n_playbooks=2,
    n_plans_per_playbook=2,
    n_branches_per_plan=1,
    n_stmts_per_branch=2,
    n_roles=2,
    n_phases=2,
    n_subplot_breadth=0,
    n_subplot_depth=0,
    seed=42,
    n_reps=5,
)


# ======================================================
# Sweep Helper
# ======================================================

def _sweep(
    param: str,
    values: List[int],
    base: GeneratorConfig = BASELINE,
) -> List[GeneratorConfig]:
    """
    Build a parameter sweep by varying one field through given values.

    Args:
        param: Name of the GeneratorConfig field to vary.
        values: Ordered list of values to apply to that field.
        base: Base configuration; all other fields are held constant.

    Returns:
        List of GeneratorConfig instances, one per value.
    """
    return [replace(base, **{param: v}) for v in values]


def _sweep_2d(
    param1: str, values1: List[int],
    param2: str, values2: List[int],
    base: GeneratorConfig = BASELINE,
) -> List[GeneratorConfig]:
    """
    Helper to generate a Cartesian product of two parameters.
    """
    return [
        replace(base, **{param1: v1, param2: v2})
        for v1, v2 in itertools.product(values1, values2)
    ]


# ======================================================
# Experiment Suites
# ======================================================

EXPERIMENTS: Dict[str, List[GeneratorConfig]] = {

    # ================== Structural Experiments ==================

    # How does the number of Roles affect the director and role files?
    # Expected: linear growth in director .asl (on_enter/on_exit bodies)
    # and one new role .asl file per role.
    "scale_roles": _sweep(
        "n_roles", [1, 2, 5, 10, 50, 100, 250, 500, 1000]
    ),

    # How does the number of Phases affect the director file?
    # Expected: linear growth; each phase adds DURING / ON ENTER / ON EXIT plans.
    "scale_phases": _sweep(
        "n_phases", [1, 2, 5, 10, 25, 50, 100, 200]
    ),

    # How does the number of Playbooks affect role file includes and
    # transitive closure computation?
    # Expected: roughly linear (each playbook adds one .asl file and one include).
    "scale_playbooks": _sweep(
        "n_playbooks", [0, 1, 2, 5, 10, 50, 100, 250]
    ),

    # How does the number of WHEN blocks per Playbook affect the playbook .asl size?
    # Expected: linear in playbook file size; branching adds multiple plans per WHEN.
    "scale_plans": _sweep(
        "n_plans_per_playbook", [1, 2, 5, 10, 25, 50, 100, 200]
    ),

    # How do IF branches affect plan expansion?  Each branch compiles to a separate
    # plan with a different context guard, so this multiplies output plan count.
    "scale_branches": _sweep(
        "n_branches_per_plan", [0, 1, 2, 5, 10, 25, 50]
    ),

    # How does the number of DO statements per branch affect plan body size?
    # Expected: linear growth within each plan body; no structural explosion.
    "scale_stmts": _sweep(
        "n_stmts_per_branch", [1, 2, 5, 10, 25, 50, 100, 500]
    ),

    # ================== Subplot Experiments ==================

    # How does the number of parallel subplots (breadth) scale?
    # Uses depth=1 so that breadth=0 produces no subplots at all.
    # Expected: linear growth in number of output files; possible super-linear
    # growth in transitive closure computation.
    "scale_subplot_breadth": _sweep(
        "n_subplot_breadth",
        [0, 1, 2, 5, 10, 20, 50],
        base=replace(BASELINE, n_subplot_depth=1),
    ),

    # How does subplot nesting depth scale?
    # Uses breadth=2 so that depth=0 produces no subplots at all.
    # Expected: exponential growth in output files (breadth^depth plots),
    # with possible non-linear DFS computation cost.
    "scale_subplot_depth": _sweep(
        "n_subplot_depth",
        [0, 1, 2, 3, 4, 5, 6],
        base=replace(BASELINE, n_subplot_breadth=2),
    ),

    # ================== Vocabulary Experiments ==================

    # How does the number of ACTION declarations affect compilation?
    # Expected: linear growth in validator pass (registration); validator
    # also checks unused symbols, so cost includes checking all declarations.
    "scale_actions": _sweep(
        "n_actions", [1, 5, 10, 50, 100, 500, 1000, 2500]
    ),

    # How does EVENT count affect compilation?
    "scale_events": _sweep(
        "n_events", [1, 5, 10, 50, 100, 500, 1000, 2500]
    ),

    # How does FACT count affect compilation?
    # Facts of 0 is special: disables IF branching even if n_branches_per_plan>0.
    "scale_facts": _sweep(
        "n_facts", [0, 1, 5, 10, 50, 100, 500, 1000]
    ),

    # Combined vocabulary scaling: grow all three simultaneously.
    # Allows measuring aggregate vocabulary overhead vs. individual element cost.
    "scale_vocabulary_combined": [
        replace(BASELINE, n_actions=n, n_events=n, n_facts=max(n // 2, 1))
        for n in [5, 10, 50, 100, 500, 1000, 2000]
    ],

    # ================== Multi-Dimensional Interactions ==================

    # Multiplicative expansion in director.asl: (Roles * Playbooks) assignments per phase.
    # $O(R \times P)$ statements generated in the ON ENTER / ON EXIT blocks.
    "interaction_roles_playbooks": [
        replace(BASELINE, n_roles=n, n_playbooks=n)
        for n in [1, 2, 5, 10, 20, 50, 100]
    ],

    # Multiplicative expansion in director.asl: (Phases * Roles) assignments.
    # Each phase adds ON ENTER / ON EXIT blocks which iterate over all roles.
    "interaction_phases_roles": [
        replace(BASELINE, n_phases=n, n_roles=n)
        for n in [1, 2, 5, 10, 20, 50, 100]
    ],

    # Internal playbook complexity: Playbooks * Plans * Branches.
    # Total AgentSpeak plans generated = $P_b \times P_l \times B$.
    "interaction_playbook_complexity": [
        replace(BASELINE, n_playbooks=n, n_plans_per_playbook=n, n_branches_per_plan=n)
        for n in [1, 2, 5, 10, 15, 20]
    ],

    # Exponential subplot growth * linear phase growth inside each subplot.
    # Output grows by $O(\text{Phases} \times \text{Breadth}^{\text{Depth}})$.
    "interaction_subplots_phases": [
        replace(BASELINE, n_subplot_depth=d, n_phases=p, n_subplot_breadth=2)
        for d, p in [(1, 2), (2, 5), (3, 10), (4, 20), (5, 50)]
    ],

    # ================== Game Design Interactions ==================

    # "Growing Cast" - As the number of roles grows, the vocabulary needed grows.
    "interaction_growing_cast": [
        replace(BASELINE, n_roles=n, n_actions=n, n_events=n, n_facts=max(n // 2, 1))
        for n in [5, 10, 50, 100, 250, 500, 1000]
    ],

    # "Full Game" - Scaling structural dimensions together. 
    # This triggers the quadratic assignment logic + linear playbook logic at the same time.
    "interaction_full_game": [
        replace(BASELINE, n_roles=n, n_phases=n, n_playbooks=n, n_plans_per_playbook=n)
        for n in [1, 2, 5, 10, 20, 50, 100]
    ],

    # "Subplot Scope" - Nested subplots usually come with their own sets of new roles.
    "interaction_subplot_scope": [
        replace(BASELINE, n_subplot_depth=d, n_roles=r, n_subplot_breadth=2)
        for d, r in [(1, 10), (2, 20), (3, 50), (4, 100), (5, 200)]
    ],

    # "Dense AI" - Focused on pure behavioral depth. Many playbooks, huge action sequences.
    "interaction_dense_ai": _sweep_2d(
        "n_playbooks", [2, 5, 10, 25, 50],
        "n_stmts_per_branch", [2, 5, 10, 25, 50],
    ),

    # ================== 2D Grid Sweeps ==================

    # 2D Grid: Phases vs Roles. Tests the $O(P \times R)$ assignment explosion in full Cartesian space.
    "grid_phases_roles": _sweep_2d(
        "n_phases", [2, 10, 25, 50],
        "n_roles", [2, 10, 25, 50],
    ),

    # 2D Grid: Playbook Logic. Playbooks vs Plans per playbook.
    "grid_playbook_logic": _sweep_2d(
        "n_playbooks", [2, 5, 10, 25, 50],
        "n_plans_per_playbook", [2, 5, 10, 25, 50],
    ),
    
    # ================== Import Resolution ==================
    "scale_import_nodes": [
        replace(BASELINE, n_import_nodes=n, n_import_edges=2)
        for n in [10, 50, 100, 250, 500, 1000]
    ],
    "scale_import_edges": [
        replace(BASELINE, n_import_nodes=100, n_import_edges=n)
        for n in [1, 2, 5, 10, 25, 50]
    ],
    "grid_imports": _sweep_2d(
        "n_import_nodes", [10, 50, 100, 250],
        "n_import_edges", [1, 5, 10, 25],
    ),
}
