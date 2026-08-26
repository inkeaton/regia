"""
Configuration dataclass for the Regia benchmark generator.

Every field is stored verbatim in the output CSV so that any row
can be reproduced by passing the same config to generator.generate().
"""

from dataclasses import dataclass


@dataclass
class GeneratorConfig:
    """
    Full specification for one benchmark code generation run.

    All fields together uniquely determine the generated source and
    are written into the output CSV for reproducibility.

    Args:
        n_actions: Number of ACTION vocabulary declarations.
        n_events: Number of EVENT vocabulary declarations.
        n_facts: Number of FACT vocabulary declarations.
        n_playbooks: Number of PLAYBOOK definitions (0 = no playbooks).
        n_plans_per_playbook: Number of WHEN blocks per Playbook (min 1).
        n_branches_per_plan: IF branches inside each WHEN body (0 = unconditional).
        n_stmts_per_branch: DO statements per branch / unconditional body (min 1).
        n_roles: ROLE declarations in the root Plot (min 1).
        n_phases: Regular PHASE declarations in the root Plot (min 1).
        n_subplot_breadth: Child Plots spawned at each nesting level
            (0 = no subplots; both breadth and depth must be > 0 for subplots).
        n_subplot_depth: Depth of the subplot hierarchy
            (0 = no subplots).
        seed: Random seed; unused currently but reserved for future
            stochastic generators and stored for reproducibility.
        n_reps: Number of timed compilation repetitions per configuration.
    """

    # ================== VOCABULARY ==================
    n_actions: int = 10
    n_events: int = 10
    n_facts: int = 5

    # ================== PLAYBOOKS ==================
    n_playbooks: int = 2
    n_plans_per_playbook: int = 2
    n_branches_per_plan: int = 1
    n_stmts_per_branch: int = 2

    # ================== PLOT STRUCTURE ==================
    n_roles: int = 2
    n_phases: int = 2

    # ================== SUBPLOTS ==================
    n_subplot_breadth: int = 0
    n_subplot_depth: int = 0

    # ================== RUNNER ==================
    seed: int = 42
    n_reps: int = 5
