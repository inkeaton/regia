"""
Parametric Regia source code generator.

Given a GeneratorConfig, produces a complete, syntactically and
semantically valid Regia program as a string.  The generation is
fully deterministic (no randomness used; the seed field is reserved
for future stochastic variants).

Validity guarantees:
- Every ACTION / EVENT / FACT referenced in a plan is declared.
- Every PLAYBOOK referenced in ASSIGN / UNASSIGN is declared.
- Every ROLE used in a DURING block belongs to the enclosing PLOT.
- Every PHASE referenced in TRANSITION TO belongs to the enclosing PLOT.
- Every subplot referenced in START SUBPLOT / WHEN SUBPLOT ENDS
  is a declared PLOT with a compatible role.
- TRANSITION TO is never in DURING PLOT or ON ENTER / ON EXIT.
- END PLOT is always the last statement in its block.
"""

from typing import List, Optional, Tuple

from .config import GeneratorConfig


# ======================================================
# Public API
# ======================================================

def generate(config: GeneratorConfig) -> str:
    """
    Generate a complete, valid Regia source string from the given config.

    Args:
        config: Generation parameters controlling all aspects of the output.

    Returns:
        A string of valid Regia source code ready for compile_source().
    """
    return _RegiaGenerator(config).generate()


# ======================================================
# Internal Generator
# ======================================================

class _RegiaGenerator:
    """
    Stateful generator — create a fresh instance for each call to generate().

    Args:
        config: The generation configuration.
    """

    def __init__(self, config: GeneratorConfig) -> None:
        self._cfg = config
        self._subplot_counter: int = 0

        # Build vocabulary pools (guarantee at least 1 action and 1 event).
        n_act = max(config.n_actions, 1)
        n_evt = max(config.n_events, 1)
        n_fct = max(config.n_facts, 0)
        n_pb = max(config.n_playbooks, 0)

        self._actions: List[str] = [f"act_{i}" for i in range(n_act)]
        self._events: List[str] = [f"evt_{i}" for i in range(n_evt)]
        self._facts: List[str] = [f"fct_{i}" for i in range(n_fct)]
        self._pb_names: List[str] = [f"Playbook{i}" for i in range(n_pb)]

    # ================== Top-level entry point ==================

    def generate(self) -> str:
        """
        Build the full Regia source document.

        Returns:
            The complete Regia source as a single string.
        """
        self._subplot_counter = 0  # Reset for idempotency.
        parts: List[str] = []

        parts += self._header()
        parts += self._gen_vocabulary()

        if self._pb_names:
            parts.append("")
            parts += self._section("Playbooks")
            for i, name in enumerate(self._pb_names):
                parts += self._gen_playbook(name, i)
                parts.append("")

        has_subplots = (
            self._cfg.n_subplot_breadth > 0 and self._cfg.n_subplot_depth > 0
        )

        subplot_starts: List[str] = []
        subplot_whens: List[str] = []
        subplot_defs: List[str] = []

        if has_subplots:
            subplot_starts, subplot_whens, subplot_defs = (
                self._gen_subplot_children(parent_role="Role0", level=1)
            )

        parts += self._section("Main Plot")
        parts += self._gen_main_plot(subplot_starts, subplot_whens)

        if subplot_defs:
            parts.append("")
            parts += self._section("Subplot Definitions")
            parts += subplot_defs

        return "\n".join(parts)

    # ================== Vocabulary section ==================

    def _gen_vocabulary(self) -> List[str]:
        """
        Generate all ACTION, EVENT, and FACT declarations.

        Returns:
            Lines containing all vocabulary declarations.
        """
        lines: List[str] = []
        lines.append("# == Actions ==")
        for a in self._actions:
            lines.append(f"ACTION {a}.")
        lines.append("")
        lines.append("# == Events ==")
        for e in self._events:
            lines.append(f"EVENT {e}.")
        if self._facts:
            lines.append("")
            lines.append("# == Facts ==")
            for f in self._facts:
                lines.append(f"FACT {f}.")
        return lines

    # ================== Playbook section ==================

    def _gen_playbook(self, name: str, pb_idx: int) -> List[str]:
        """
        Generate one PLAYBOOK definition.

        Args:
            name: The playbook name (e.g. 'Playbook0').
            pb_idx: Index of this playbook; used for stable event cycling.

        Returns:
            Lines for the complete PLAYBOOK block.
        """
        lines: List[str] = [f"PLAYBOOK {name}:"]
        n_plans = max(self._cfg.n_plans_per_playbook, 1)
        for plan_i in range(n_plans):
            global_idx = pb_idx * n_plans + plan_i
            event = self._evt(global_idx)
            lines += self._gen_pb_when(event, global_idx)
        return lines

    def _gen_pb_when(self, event: str, global_plan_idx: int) -> List[str]:
        """
        Generate one WHEN block inside a Playbook.

        Args:
            event: The triggering event name.
            global_plan_idx: Global plan index for stable action/fact cycling.

        Returns:
            Lines for the WHEN block (indented 1 level = 4 spaces).
        """
        lines: List[str] = [f"    WHEN {event}:"]
        n_branches = self._cfg.n_branches_per_plan
        n_stmts = max(self._cfg.n_stmts_per_branch, 1)

        if n_branches <= 0 or not self._facts:
            # Unconditional body.
            for s in range(n_stmts):
                lines.append(
                    f"        DO {self._act(global_plan_idx * n_stmts + s)}."
                )
        else:
            # IF / ELSE branches.
            for b in range(n_branches):
                fact = self._fct(global_plan_idx * n_branches + b)
                lines.append(f"        IF {fact}:")
                for s in range(n_stmts):
                    a = self._act(
                        (global_plan_idx * n_branches + b) * n_stmts + s
                    )
                    lines.append(f"            DO {a}.")
            lines.append("        ELSE:")
            lines.append(f"            DO {self._act(global_plan_idx)}.")

        return lines

    # ================== Main Plot section ==================

    def _gen_main_plot(
        self,
        subplot_starts: List[str],
        subplot_whens: List[str],
    ) -> List[str]:
        """
        Generate the root PLOT MainPlot definition.

        The root plot has n_phases regular phases.  If subplots are
        present, an additional 'subplot_phase' is appended after the
        last regular phase; the last regular phase then transitions
        into it rather than ending the plot directly.

        Args:
            subplot_starts: Unindented START SUBPLOT lines for the
                subplot phase ON ENTER block.
            subplot_whens: Pre-indented (8-/12-space) WHEN SUBPLOT …
                ENDS lines for the subplot_phase DURING block.

        Returns:
            Lines for the complete PLOT MainPlot block.
        """
        cfg = self._cfg
        lines: List[str] = ["PLOT MainPlot."]
        lines.append("")

        n_phases = max(cfg.n_phases, 1)
        n_roles = max(cfg.n_roles, 1)
        has_subplots = bool(subplot_starts)

        role_names = [f"Role{i}" for i in range(n_roles)]

        # Build phase list: regular phases + optional subplot_phase.
        phase_names: List[str] = [f"phase_{i}" for i in range(n_phases)]
        if has_subplots:
            phase_names.append("subplot_phase")

        # Phase declarations.
        for i, ph in enumerate(phase_names):
            marker = " INITIAL" if i == 0 else ""
            lines.append(f"    PHASE {ph}{marker}.")
        lines.append("")

        # Role declarations.
        for r in role_names:
            lines.append(f"    ROLE {r}.")
        lines.append("")

        # DURING PLOT: Plot-wide emergency handler.
        # evt_0 is reserved for this handler across all generated plots.
        lines.append("    DURING PLOT:")
        lines.append(f"        WHEN {self._evt(0)}:")
        lines.append("            END PLOT.")
        lines.append("")

        # Regular phase DURING blocks.
        regular_phases = [p for p in phase_names if p != "subplot_phase"]
        for ph_i, phase in enumerate(regular_phases):
            next_phase: Optional[str] = (
                phase_names[ph_i + 1] if ph_i + 1 < len(phase_names) else None
            )

            lines.append(f"    DURING {phase}:")

            if self._pb_names:
                # ON ENTER: assign playbooks and fire a world action.
                lines.append("        ON ENTER:")
                for ri, role in enumerate(role_names):
                    pb = self._pb(ri)
                    lines.append(f"            ASSIGN {pb} TO {role}.")
                    lines.append(f"            WORLD DO {self._act(ri)}.")
                lines.append("")
                # ON EXIT: unassign playbooks.
                lines.append("        ON EXIT:")
                for ri, role in enumerate(role_names):
                    pb = self._pb(ri)
                    lines.append(f"            UNASSIGN {pb} FROM {role}.")
                lines.append("")

            # Phase transition event.
            # Offset by 1 so we never collide with the evt_0 emergency event.
            evt = self._evt(ph_i + 1)
            lines.append(f"        WHEN {evt}:")
            if next_phase is not None:
                lines.append(f"            TRANSITION TO {next_phase}.")
            else:
                lines.append("            END PLOT.")
            lines.append("")

        # Subplot phase DURING block.
        if has_subplots:
            lines.append("    DURING subplot_phase:")
            lines.append("        ON ENTER:")
            for stmt in subplot_starts:
                lines.append(f"            {stmt}")
            lines.append("")
            for wl in subplot_whens:
                lines.append(wl)
            lines.append("")

        return lines

    # ================== Subplot generation ==================

    def _gen_subplot_children(
        self, parent_role: str, level: int
    ) -> Tuple[List[str], List[str], List[str]]:
        """
        Recursively generate child subplot data for embedding in a parent
        DURING block.

        Each generated subplot has exactly one role named 'subrole'.
        Using the same role name across all subplots is safe because
        role namespaces are per-PLOT in Regia's validator.

        The convention for indentation in the returned lists:
        - start_stmts: no leading whitespace; callers wrap with 12-space
          prefix to place them inside an ON ENTER block.
        - when_blocks: pre-indented at 8 spaces (WHEN headers) and
          12 spaces (body statements) — ready to embed in a DURING block.

        Args:
            parent_role: The role name in the parent plot to map from.
            level: Current nesting depth (starts at 1 for direct children
                of the root plot; generation stops at n_subplot_depth).

        Returns:
            A 3-tuple of:
                start_stmts  – START SUBPLOT lines for ON ENTER.
                when_blocks  – WHEN SUBPLOT … ENDS lines for the DURING block.
                plot_defs    – Flat list of all generated PLOT definition lines.
        """
        cfg = self._cfg
        if level > cfg.n_subplot_depth or cfg.n_subplot_breadth <= 0:
            return [], [], []

        child_role = "subrole"

        # Allocate globally unique subplot names at this level.
        subplot_names: List[str] = []
        for _ in range(cfg.n_subplot_breadth):
            idx = self._subplot_counter
            self._subplot_counter += 1
            subplot_names.append(f"Subplot_L{level}_{idx}")

        start_stmts: List[str] = [
            f"START SUBPLOT {sp} MAPPING {parent_role} TO {child_role}."
            for sp in subplot_names
        ]

        when_blocks: List[str] = []
        all_plot_defs: List[str] = []

        for i, sp_name in enumerate(subplot_names):
            is_last = i == len(subplot_names) - 1

            # Recursively generate this subplot's own children.
            child_starts, child_whens, child_defs = self._gen_subplot_children(
                parent_role=child_role, level=level + 1
            )

            # Generate this subplot's PLOT definition.
            sp_lines = self._gen_subplot_plot(
                name=sp_name,
                role=child_role,
                child_starts=child_starts,
                child_whens=child_whens,
            )
            all_plot_defs += sp_lines
            all_plot_defs.append("")
            all_plot_defs += child_defs

            # WHEN SUBPLOT … ENDS block for the parent.
            # Pre-indented at 8 spaces (header) and 12 spaces (body).
            when_blocks.append(f"        WHEN SUBPLOT {sp_name} ENDS:")
            when_blocks.append(f"            WORLD DO {self._act(i)}.")
            if is_last:
                # The last subplot ending terminates the parent phase.
                when_blocks.append("            END PLOT.")

        return start_stmts, when_blocks, all_plot_defs

    def _gen_subplot_plot(
        self,
        name: str,
        role: str,
        child_starts: List[str],
        child_whens: List[str],
    ) -> List[str]:
        """
        Generate a standalone subplot PLOT definition.

        Structure:
        - If leaf (no children): 1 phase 'main' INITIAL; WHEN evt → END PLOT.
        - If non-leaf (has children): 2 phases ('main' INITIAL, 'subplot_phase');
          DURING main: WHEN evt → TRANSITION TO subplot_phase.
          DURING subplot_phase: ON ENTER spawns children; WHEN SUBPLOT … ENDS.

        Args:
            name: Unique plot name (e.g. 'Subplot_L1_0').
            role: Single role in this subplot (always 'subrole').
            child_starts: START SUBPLOT lines for the subplot phase ON ENTER.
            child_whens: WHEN SUBPLOT … ENDS lines for the subplot phase.

        Returns:
            Lines for the complete subplot PLOT block.
        """
        has_children = bool(child_starts)
        lines: List[str] = [f"PLOT {name}."]
        lines.append("")

        # Phases.
        lines.append("    PHASE main INITIAL.")
        if has_children:
            lines.append("    PHASE subplot_phase.")
        lines.append("")

        # Roles.
        lines.append(f"    ROLE {role}.")
        lines.append("")

        # DURING PLOT: emergency handler (uses evt_0).
        lines.append("    DURING PLOT:")
        lines.append(f"        WHEN {self._evt(0)}:")
        lines.append("            END PLOT.")
        lines.append("")

        # Main phase.
        lines.append("    DURING main:")
        next_ph: Optional[str] = "subplot_phase" if has_children else None
        lines.append(f"        WHEN {self._evt(1)}:")
        if next_ph is not None:
            lines.append(f"            TRANSITION TO {next_ph}.")
        else:
            lines.append("            END PLOT.")
        lines.append("")

        # Subplot phase (non-leaf only).
        if has_children:
            lines.append("    DURING subplot_phase:")
            lines.append("        ON ENTER:")
            for stmt in child_starts:
                lines.append(f"            {stmt}")
            lines.append("")
            for wl in child_whens:
                lines.append(wl)
            lines.append("")

        return lines

    # ================== Cycling accessors ==================

    def _act(self, idx: int) -> str:
        """Return an action name, cycling through the pool.

        Args:
            idx: Any non-negative integer index.

        Returns:
            An action name from the declared pool.
        """
        return self._actions[idx % len(self._actions)]

    def _evt(self, idx: int) -> str:
        """Return an event name, cycling through the pool.

        Args:
            idx: Any non-negative integer index.

        Returns:
            An event name from the declared pool.
        """
        return self._events[idx % len(self._events)]

    def _fct(self, idx: int) -> str:
        """Return a fact name, cycling through the pool.

        Args:
            idx: Any non-negative integer index.

        Returns:
            A fact name from the declared pool.
        """
        return self._facts[idx % len(self._facts)]

    def _pb(self, idx: int) -> Optional[str]:
        """Return a playbook name, cycling through the pool.

        Args:
            idx: Any non-negative integer index.

        Returns:
            A playbook name, or None if no playbooks are declared.
        """
        if not self._pb_names:
            return None
        return self._pb_names[idx % len(self._pb_names)]

    # ================== Formatting helpers ==================

    def _header(self) -> List[str]:
        """
        Generate a comment block header embedding the config for traceability.

        Returns:
            Header comment lines.
        """
        cfg = self._cfg
        return [
            "# =======================================================",
            "# Generated by Regia Benchmark Generator",
            f"# n_actions={cfg.n_actions}  n_events={cfg.n_events}  n_facts={cfg.n_facts}",
            f"# n_playbooks={cfg.n_playbooks}  n_plans={cfg.n_plans_per_playbook}",
            f"# n_branches={cfg.n_branches_per_plan}  n_stmts={cfg.n_stmts_per_branch}",
            f"# n_roles={cfg.n_roles}  n_phases={cfg.n_phases}",
            f"# n_subplot_breadth={cfg.n_subplot_breadth}  n_subplot_depth={cfg.n_subplot_depth}",
            f"# seed={cfg.seed}",
            "# =======================================================",
            "",
        ]

    def _section(self, title: str) -> List[str]:
        """
        Generate a section separator comment.

        Args:
            title: Section title text.

        Returns:
            Section header comment lines.
        """
        bar = "=" * 55
        return [
            f"# {bar}",
            f"# {title}",
            f"# {bar}",
            "",
        ]
