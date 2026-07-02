"""
AgentSpeak emitter for the Regia compiler.

Transforms the validated AST into AgentSpeak (.asl) source strings.
This is the final stage of the compiler pipeline.

Output files:
    - One `role_<name>.asl` per unique Role across all Plots.
      Contains static-gated Playbook plans and one-off Role DO
      handlers from Plots.
    - One `director_<plotname>.asl` per Plot.
      Contains phase management, transitions, lifecycle hooks,
      WORLD DO plans, ASSIGN/UNASSIGN logic, and SIGNAL handlers.

The emitter does NOT write files to disk. It returns a Dict[str, str]
mapping output file names to their AgentSpeak source code. The
compiler pipeline or CLI is responsible for writing them.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple

from regia.ast_nodes import (
    # Constants
    SPECIAL_ACTIONS,
    # Base elements
    ActionDecl, EventDecl, FactDecl, Arg,
    # Conditions
    ConditionExpr, ConditionNot, ConditionAnd, ConditionOr, FactRef,
    # Playbook
    DoStmt, SignalStmt, PbWhenBlock, PbIfBranch, PbElseBranch, PlaybookDef,
    # Imperative
    AssignStmt, UnassignStmt, WorldDoStmt, RoleDoStmt,
    # Plot
    TransitionStmt, OnEnter, OnExit,
    PlotWhenBlock, PlotIfBranch, PlotElseBranch,
    DuringBlock, PhaseDecl, RoleDecl, PlotDef,
    # Root
    Program,
)
from regia.errors import ErrorReporter


# == Emitter ===================================================================

class Emitter:
    """Transforms a validated AST into AgentSpeak source files.

    Usage:
        emitter = Emitter()
        outputs = emitter.emit(program)
        # outputs is Dict[str, str] mapping filenames to .asl content
    """

    def __init__(self) -> None:
        """Initialise the emitter with empty output state."""
        # Accumulated AgentSpeak output, keyed by filename
        self._outputs: Dict[str, str] = {}

        # Tracks which Playbooks are assigned to which Roles
        # across all Plots. Populated during a pre-scan.
        # role_name -> set of playbook_names (global)
        self._role_playbooks: Dict[str, Set[str]] = {}

        # Per-plot tracking of which Playbooks are assigned
        # to which Roles. Used for include directives in
        # per-plot role files.
        # plot_name -> role_name -> set of playbook_names
        self._plot_role_playbooks: Dict[str, Dict[str, Set[str]]] = {}

        # Tracks which Plots use which Roles, so we can
        # emit one-off Role DO handlers per plot context.
        # role_name -> list of (plot_name, when_block, phase_name)
        self._role_directives: Dict[str, List[_RoleDirective]] = {}

        # Lookup for PlaybookDef by name
        self._playbook_defs: Dict[str, PlaybookDef] = {}

    # == Public API ============================================================

    def emit(self, program: Program) -> Dict[str, str]:
        """Emit AgentSpeak files from the validated AST.

        Args:
            program: The root AST node (must have passed validation).

        Returns:
            Dict mapping output filenames to AgentSpeak source strings.
        """
        # Phase 1: index all Playbook definitions
        for item in program.items:
            if isinstance(item, PlaybookDef):
                self._playbook_defs[item.name] = item

        # Phase 2: pre-scan Plots to discover Role-Playbook assignments
        # and Role DO directives
        for item in program.items:
            if isinstance(item, PlotDef):
                self._prescan_plot(item)

        # Phase 3: emit Playbook files (one per unique playbook)
        all_playbooks: Set[str] = set()
        for role_pbs in self._role_playbooks.values():
            all_playbooks.update(role_pbs)
        for pb_name in sorted(all_playbooks):
            self._emit_playbook_file(pb_name)

        # Phase 4: emit Director files (one per Plot)
        for item in program.items:
            if isinstance(item, PlotDef):
                self._emit_director(item)

        # Phase 5: emit Role files (one per Plot-Role pair)
        for item in program.items:
            if isinstance(item, PlotDef):
                for role in item.roles:
                    self._emit_plot_role(item.name, role.name)

        return self._outputs

    # == Pre-scan ==============================================================
    # Walk Plots to discover which Playbooks get ASSIGNed to which
    # Roles, and which Roles receive one-off DO directives.

    def _prescan_plot(self, plot: PlotDef) -> None:
        """Pre-scan a Plot to discover Role-Playbook bindings.

        Args:
            plot: The PlotDef to scan.
        """
        plot_name = plot.name
        self._plot_role_playbooks[plot_name] = {}

        for role in plot.roles:
            if role.name not in self._role_playbooks:
                self._role_playbooks[role.name] = set()
            self._plot_role_playbooks[plot_name][role.name] = set()
            if role.name not in self._role_directives:
                self._role_directives[role.name] = []

        for block in plot.during_blocks:
            phase_name = block.phase_name  # None for DURING PLOT

            # Scan ON ENTER / ON EXIT for ASSIGN statements
            for on_enter in block.on_enters:
                self._prescan_stmts(on_enter.stmts, plot_name, phase_name)
            for on_exit in block.on_exits:
                self._prescan_stmts(on_exit.stmts, plot_name, phase_name)

            # Scan WHEN blocks for ASSIGN and Role DO
            for when in block.when_blocks:
                self._prescan_when(when, plot_name, phase_name)

    def _prescan_stmts(
        self,
        stmts: list,
        plot_name: str,
        phase_name: Optional[str],
    ) -> None:
        """Scan imperative statements for ASSIGN and Role DO.

        Args:
            stmts:      List of imperative statements.
            plot_name:  Name of the containing Plot.
            phase_name: Name of the containing phase (None for PLOT-wide).
        """
        for stmt in stmts:
            if isinstance(stmt, AssignStmt):
                # Global tracking
                self._role_playbooks.setdefault(stmt.role, set())
                self._role_playbooks[stmt.role].add(stmt.playbook)
                # Per-plot tracking
                if plot_name in self._plot_role_playbooks:
                    self._plot_role_playbooks[plot_name].setdefault(
                        stmt.role, set(),
                    )
                    self._plot_role_playbooks[plot_name][stmt.role].add(
                        stmt.playbook,
                    )
            elif isinstance(stmt, RoleDoStmt):
                if stmt.role not in self._role_directives:
                    self._role_directives[stmt.role] = []
                self._role_directives[stmt.role].append(
                    _RoleDirective(plot_name, phase_name, stmt)
                )

    def _prescan_when(
        self,
        when: PlotWhenBlock,
        plot_name: str,
        phase_name: Optional[str],
    ) -> None:
        """Scan a Plot WHEN block for ASSIGN and Role DO statements.

        Args:
            when:       The PlotWhenBlock to scan.
            plot_name:  Name of the containing Plot.
            phase_name: Name of the containing phase.
        """
        self._prescan_stmts(when.prefix_stmts, plot_name, phase_name)
        for branch in when.branches:
            self._prescan_stmts(branch.stmts, plot_name, phase_name)
        if when.else_branch is not None:
            self._prescan_stmts(
                when.else_branch.stmts, plot_name, phase_name,
            )

    # == Emit Director =========================================================

    def _emit_director(self, plot: PlotDef) -> None:
        """Emit a Director .asl file for a Plot.

        The Director agent manages:
            - Phase state (current_phase belief)
            - Phase transitions
            - ON ENTER / ON EXIT lifecycle hooks
            - WORLD DO actions
            - ASSIGN / UNASSIGN via .send
            - WHEN blocks (director-centric reactive plans)

        Args:
            plot: The PlotDef to emit a Director for.
        """
        lines: List[str] = []
        plot_lower = plot.name.lower()

        # Header comment
        lines.append(
            f"// Director agent for Plot: {plot.name}"
        )
        lines.append(
            f"// Generated by the Regia v0.2 compiler"
        )
        lines.append("")

        # Initial beliefs: starting phase
        initial_phase = next(
            p.name for p in plot.phases if p.is_initial
        )
        lines.append(f"// == Initial Beliefs ==")
        lines.append(f"current_phase({initial_phase}).")
        lines.append("")

        # Boot plan: fires on agent creation, runs ON ENTER
        # for the initial phase
        lines.append(f"// == Boot Plan ==")
        lines.append(f"// Runs when the Director agent is created.")
        lines.append(f"// Executes the ON ENTER hook for the initial phase.")
        lines.append(f"@boot__{plot.name}[atomic]")
        lines.append(f"+!boot <- ")
        boot_stmts = self._get_on_enter_stmts(plot, initial_phase)
        if boot_stmts:
            lines.append(
                self._emit_imperative_body(boot_stmts, indent=4)
            )
        else:
            lines.append("    true.")
        lines.append("")

        # Phase transition plans
        self._emit_transitions(plot, lines)

        # WHEN blocks (director-centric plans)
        self._emit_director_when_blocks(plot, lines)

        # Role-Agent registry and communication helpers
        self._emit_role_registry(plot, lines)

        filename = f"director_{plot_lower}.asl"
        self._outputs[filename] = "\n".join(lines) + "\n"

    def _get_on_enter_stmts(
        self,
        plot: PlotDef,
        phase_name: str,
    ) -> list:
        """Get the ON ENTER statements for a given phase.

        Args:
            plot:       The Plot definition.
            phase_name: The phase to look up.

        Returns:
            List of imperative statements, or empty list.
        """
        for block in plot.during_blocks:
            if block.phase_name == phase_name and block.on_enters:
                return block.on_enters[0].stmts
        return []

    def _get_on_exit_stmts(
        self,
        plot: PlotDef,
        phase_name: str,
    ) -> list:
        """Get the ON EXIT statements for a given phase.

        Args:
            plot:       The Plot definition.
            phase_name: The phase to look up.

        Returns:
            List of imperative statements, or empty list.
        """
        for block in plot.during_blocks:
            if block.phase_name == phase_name and block.on_exits:
                return block.on_exits[0].stmts
        return []

    def _emit_transitions(
        self,
        plot: PlotDef,
        lines: List[str],
    ) -> None:
        """Emit phase transition plans for all DURING blocks.

        A transition plan:
            1. Checks current_phase matches the source phase
            2. Optionally checks the guard condition
            3. Runs ON EXIT of the source phase
            4. Updates current_phase belief
            5. Runs ON ENTER of the target phase

        Args:
            plot:  The Plot definition.
            lines: The output line buffer to append to.
        """
        has_transitions = False
        for block in plot.during_blocks:
            if block.phase_name is None:
                continue  # DURING PLOT has no transitions

            for tr in block.transitions:
                if not has_transitions:
                    lines.append(f"// == Phase Transitions ==")
                    has_transitions = True

                source_phase = block.phase_name
                target_phase = tr.target_phase

                lines.append(
                    f"// TRANSITION: {source_phase} -> "
                    f"{target_phase} on {tr.event}"
                )

                # Build the context (guard conditions)
                context_parts: List[str] = [
                    f"current_phase({source_phase})",
                ]
                if tr.guard is not None:
                    context_parts.append(
                        self._emit_condition(tr.guard)
                    )

                context = " & ".join(context_parts)

                # Build the plan body
                body_stmts: List[str] = []

                # ON EXIT of source phase
                exit_stmts = self._get_on_exit_stmts(plot, source_phase)
                for stmt in exit_stmts:
                    body_stmts.append(
                        self._emit_imperative_stmt(stmt)
                    )

                # Update phase belief
                body_stmts.append(
                    f"-current_phase({source_phase})"
                )
                body_stmts.append(
                    f"+current_phase({target_phase})"
                )

                # ON ENTER of target phase
                enter_stmts = self._get_on_enter_stmts(plot, target_phase)
                for stmt in enter_stmts:
                    body_stmts.append(
                        self._emit_imperative_stmt(stmt)
                    )

                body = ";\n    ".join(body_stmts)
                lines.append(f"@tr__{plot.name}__{source_phase}_to_{target_phase}__{tr.event}[atomic]")
                lines.append(f"+{tr.event} : {context} <-")
                lines.append(f"    {body}.")
                lines.append("")

        if has_transitions:
            lines.append("")

    def _emit_director_when_blocks(
        self,
        plot: PlotDef,
        lines: List[str],
    ) -> None:
        """Emit director-centric WHEN plans from all DURING blocks.

        Args:
            plot:  The Plot definition.
            lines: The output line buffer.
        """
        has_when = False
        for block in plot.during_blocks:
            for when in block.when_blocks:
                if not has_when:
                    lines.append(f"// == Director WHEN Plans ==")
                    has_when = True

                phase_ctx = (
                    f"current_phase({block.phase_name})"
                    if block.phase_name is not None
                    else None
                )
                self._emit_when_as_director(
                    when, phase_ctx, plot.name, lines,
                )

        if has_when:
            lines.append("")

    def _emit_when_as_director(
        self,
        when: PlotWhenBlock,
        phase_context: Optional[str],
        plot_name: str,
        lines: List[str],
    ) -> None:
        """Emit a single Plot WHEN block as Director AgentSpeak plans.

        Handles the three body forms:
            1. Pure unconditional: single plan with all stmts
            2. Pure conditional: one plan per IF branch + ELSE
            3. Mixed: prefix stmts prepended to every branch plan

        Args:
            when:          The PlotWhenBlock to emit.
            phase_context: Optional phase guard (e.g. "current_phase(backstage)").
            plot_name:     The Plot name for labeling.
            lines:         The output line buffer.
        """
        priority = when.priority if when.priority is not None else 0

        # Case 1: no branches (unconditional)
        if not when.branches:
            context_parts: List[str] = []
            if phase_context:
                context_parts.append(phase_context)

            body_stmts = [
                self._emit_imperative_stmt(s)
                for s in when.prefix_stmts
            ]

            label = f"dir__{plot_name}__{when.event}__0"
            self._write_plan(
                lines, label, when.event, context_parts, body_stmts, priority,
            )
            return

        # Case 2 & 3: branches (with optional prefix)
        prefix_stmts = [
            self._emit_imperative_stmt(s)
            for s in when.prefix_stmts
        ]

        for idx, branch in enumerate(when.branches):
            context_parts = []
            if phase_context:
                context_parts.append(phase_context)
            context_parts.append(
                self._emit_condition(branch.condition)
            )

            body_stmts = prefix_stmts + [
                self._emit_imperative_stmt(s)
                for s in branch.stmts
            ]

            label = f"dir__{plot_name}__{when.event}__{idx}"
            self._write_plan(
                lines, label, when.event, context_parts, body_stmts, priority,
            )

        # ELSE branch: negation of all IF conditions
        if when.else_branch is not None:
            context_parts = []
            if phase_context:
                context_parts.append(phase_context)

            negated = [
                f"not ({self._emit_condition(b.condition)})"
                for b in when.branches
            ]
            context_parts.extend(negated)

            body_stmts = prefix_stmts + [
                self._emit_imperative_stmt(s)
                for s in when.else_branch.stmts
            ]

            label = f"dir__{plot_name}__{when.event}__{len(when.branches)}"
            self._write_plan(
                lines, label, when.event, context_parts, body_stmts, priority,
            )

    def _emit_role_registry(
        self,
        plot: PlotDef,
        lines: List[str],
    ) -> None:
        """Emit role-agent registry management and communication helpers.

        Args:
            plot:  The Plot definition.
            lines: The output line buffer.
        """
        lines.append("// == Role-Agent Registry ==")
        lines.append("// Populated at plot startup via !start_plot.")
        lines.append(f"@dir__{plot.name}__start_plot__0")
        lines.append("+!start_plot(Bindings) <-")
        lines.append("    for ( .member(role_agent(Role, Agent), Bindings) ) {")
        lines.append("        +role_agent(Role, Agent);")
        lines.append("    }.")
        lines.append("")
        lines.append(f"@dir__{plot.name}__send_to_role__0")
        lines.append("+!send_to_role(Role, Performative, Content) <-")
        lines.append("    .findall(A, role_agent(Role, A), Agents);")
        lines.append("    .send(Agents, Performative, Content).")
        lines.append("")

    # == Emit Playbook File =====================================================

    def _emit_playbook_file(self, pb_name: str) -> None:
        """Emit a standalone Playbook .asl file.

        Contains only the static-gated WHEN plans for one Playbook.
        This file is included by role templates via { include(...) }.

        Args:
            pb_name: The Playbook identifier.
        """
        pb_def = self._playbook_defs.get(pb_name)
        if pb_def is None:
            return

        lines: List[str] = []
        pb_lower = pb_name.lower()

        lines.append(f"// Playbook: {pb_name}")
        lines.append(f"// Generated by the Regia v0.2 compiler")
        lines.append(f"//")
        lines.append(
            f"// Plans are gated by playbook_active({pb_name})."
        )
        lines.append(
            f"// Included by role templates that use this playbook."
        )
        lines.append("")

        self._emit_playbook_plans(pb_def, lines)

        filename = f"playbook_{pb_lower}.asl"
        self._outputs[filename] = "\n".join(lines) + "\n"

    # == Emit Role =============================================================

    def _emit_plot_role(
        self,
        plot_name: str,
        role_name: str,
    ) -> None:
        """Emit a per-Plot Role .asl file.

        Contains:
            1. Include directives for each assignable Playbook
            2. Playbook activation/deactivation handlers

        Args:
            plot_name: The Plot this role belongs to.
            role_name: The Role identifier.
        """
        lines: List[str] = []
        plot_lower = plot_name.lower()
        role_lower = role_name.lower()

        lines.append(f"// Role: {role_name} in Plot: {plot_name}")
        lines.append(f"// Generated by the Regia v0.2 compiler")
        lines.append("")

        # Include directives for each assignable Playbook
        playbooks = sorted(
            self._plot_role_playbooks
            .get(plot_name, {})
            .get(role_name, set())
        )
        if playbooks:
            lines.append(f"// == Included Playbooks ==")
            for pb in playbooks:
                pb_lower_name = pb.lower()
                lines.append(
                    f'{{ include("playbook_{pb_lower_name}.asl") }}'
                )
            lines.append("")

        # Playbook activation handlers: when the Director tells
        # this agent to add/remove a playbook, toggle the belief.
        lines.append(f"// == Playbook Management ==")
        lines.append(
            f"// When the Director assigns a playbook, add the"
        )
        lines.append(
            f"// playbook_active belief to enable its gated plans."
        )
        lines.append(f"+add_playbook(Name) <-")
        lines.append(f"    +playbook_active(Name).")
        lines.append(f"")
        lines.append(f"+remove_playbook(Name) <-")
        lines.append(f"    -playbook_active(Name).")
        lines.append("")

        # Generate handler plans for Role DO directives
        handler_plans = set()
        for d in self._role_directives.get(role_name, []):
            if d.plot_name != plot_name:
                continue
            stmt = d.stmt
            args = self._emit_args(stmt.args)
            action_lower = stmt.action.lower()
            goal = f"{action_lower}({args})" if args else action_lower

            if stmt.is_special:
                do = DoStmt(action=stmt.action, is_special=True, args=stmt.args)
                body = self._emit_do_stmt(do)
            else:
                body = goal

            handler_plans.add(
                f"@role__{plot_name}__{role_name}__{action_lower}\n"
                f"+!{goal} <-\n    {body}."
            )

        if handler_plans:
            lines.append("// == Director Commands ==")
            for plan in sorted(handler_plans):
                lines.append(plan)
                lines.append("")

        filename = f"role_{plot_lower}_{role_lower}.asl"
        self._outputs[filename] = "\n".join(lines) + "\n"

    def _emit_playbook_plans(
        self,
        pb: PlaybookDef,
        lines: List[str],
    ) -> None:
        """Emit all WHEN blocks from a Playbook as static-gated plans.

        Each plan includes `playbook_active(PlaybookName)` in its
        context so it only fires when the Playbook is currently
        assigned to the agent.

        Args:
            pb:    The PlaybookDef to emit.
            lines: The output line buffer.
        """
        gate = f"playbook_active({pb.name})"

        for when in pb.when_blocks:
            priority = when.priority if when.priority is not None else 0

            # Case 1: no branches (unconditional)
            if not when.branches:
                body_stmts = [
                    self._emit_pb_stmt(s) for s in when.prefix_stmts
                ]
                label = f"pb__{pb.name}__{when.event}__0"
                self._write_plan(
                    lines, label, when.event, [gate], body_stmts, priority,
                )
                continue

            # Case 2 & 3: branches (with optional prefix)
            prefix_stmts = [
                self._emit_pb_stmt(s) for s in when.prefix_stmts
            ]

            for idx, branch in enumerate(when.branches):
                context_parts = [gate]
                context_parts.append(
                    self._emit_condition(branch.condition)
                )

                body_stmts = prefix_stmts + [
                    self._emit_pb_stmt(s) for s in branch.stmts
                ]

                label = f"pb__{pb.name}__{when.event}__{idx}"
                self._write_plan(
                    lines, label, when.event, context_parts, body_stmts,
                    priority,
                )

            # ELSE branch
            if when.else_branch is not None:
                context_parts = [gate]
                negated = [
                    f"not ({self._emit_condition(b.condition)})"
                    for b in when.branches
                ]
                context_parts.extend(negated)

                body_stmts = prefix_stmts + [
                    self._emit_pb_stmt(s)
                    for s in when.else_branch.stmts
                ]

                label = f"pb__{pb.name}__{when.event}__{len(when.branches)}"
                self._write_plan(
                    lines, label, when.event, context_parts, body_stmts,
                    priority,
                )

    # == Statement emission ====================================================

    def _emit_pb_stmt(self, stmt: object) -> str:
        """Emit a single Playbook statement as AgentSpeak.

        Args:
            stmt: A DoStmt or SignalStmt.

        Returns:
            AgentSpeak string for this statement.
        """
        if isinstance(stmt, DoStmt):
            return self._emit_do_stmt(stmt)
        elif isinstance(stmt, SignalStmt):
            return self._emit_signal_stmt(stmt)
        return f"/* unknown pb stmt */"

    def _emit_do_stmt(self, stmt: DoStmt) -> str:
        """Emit a DO statement as AgentSpeak.

        Special actions map to AgentSpeak primitives:
            TELL(target, msg) -> .send(target, tell, msg)
            BROADCAST(msg)    -> .broadcast(tell, msg)
            ACHIEVE(goal)     -> !goal
            BELIEVE(fact)     -> +fact
            FORGET(fact)      -> -fact

        Regular actions map to: action or action(args)

        Args:
            stmt: The DoStmt to emit.

        Returns:
            AgentSpeak string.
        """
        if not stmt.is_special:
            args = self._emit_args(stmt.args)
            if args:
                return f"{stmt.action}({args})"
            return stmt.action

        # Special actions
        def _fmt(index: int, default: str) -> str:
            if index < len(stmt.args):
                a = stmt.args[index]
                return f'"{a.value}"' if a.is_string else str(a.value)
            return default

        if stmt.action == "TELL":
            target = _fmt(0, "unknown")
            msg = _fmt(1, "msg")
            return f".send({target}, tell, {msg})"

        elif stmt.action == "BROADCAST":
            msg = _fmt(0, "msg")
            return f".broadcast(tell, {msg})"

        elif stmt.action == "ACHIEVE":
            goal = _fmt(0, "goal")
            return f"!{goal}"

        elif stmt.action == "BELIEVE":
            fact = _fmt(0, "fact")
            return f"+{fact}"

        elif stmt.action == "FORGET":
            fact = _fmt(0, "fact")
            return f"-{fact}"

        elif stmt.action == "PRINT":
            args_str = self._emit_args(stmt.args)
            return f".print({args_str})"

        return f"/* unknown special: {stmt.action} */"

    def _emit_signal_stmt(self, stmt: SignalStmt) -> str:
        """Emit a SIGNAL statement as AgentSpeak.

        SIGNAL becomes a .send to the Director agent.

        Args:
            stmt: The SignalStmt to emit.

        Returns:
            AgentSpeak string.
        """
        args = self._emit_args(stmt.args)
        if args:
            return f".send(director, tell, {stmt.event}({args}))"
        return f".send(director, tell, {stmt.event})"

    def _emit_imperative_stmt(self, stmt: object) -> str:
        """Emit an imperative statement (Director context).

        Args:
            stmt: An AssignStmt, UnassignStmt, WorldDoStmt, or RoleDoStmt.

        Returns:
            AgentSpeak string.
        """
        if isinstance(stmt, AssignStmt):
            # Director sends add_playbook belief to all agents
            # bound to this role
            role_lower = stmt.role.lower()
            return (
                f"!send_to_role({role_lower}, tell, "
                f"add_playbook({stmt.playbook}))"
            )

        elif isinstance(stmt, UnassignStmt):
            role_lower = stmt.role.lower()
            return (
                f"!send_to_role({role_lower}, tell, "
                f"remove_playbook({stmt.playbook}))"
            )

        elif isinstance(stmt, WorldDoStmt):
            if stmt.is_special:
                # Reuse the DO special action logic
                do = DoStmt(
                    action=stmt.action,
                    is_special=True,
                    args=stmt.args,
                )
                return self._emit_do_stmt(do)

            args = self._emit_args(stmt.args)
            if args:
                return f"{stmt.action}({args})"
            return stmt.action

        elif isinstance(stmt, RoleDoStmt):
            role_lower = stmt.role.lower()
            args = self._emit_args(stmt.args)
            action_lower = stmt.action.lower()
            goal = f"{action_lower}({args})" if args else action_lower
            return f"!send_to_role({role_lower}, achieve, {goal})"

        return f"/* unknown imperative */"

    def _emit_imperative_body(
        self,
        stmts: list,
        indent: int = 4,
    ) -> str:
        """Emit a sequence of imperative statements as a plan body.

        Args:
            stmts:  List of imperative statements.
            indent: Number of spaces for indentation.

        Returns:
            Formatted body string with semicolons and final period.
        """
        parts = [self._emit_imperative_stmt(s) for s in stmts]
        sep = ";\n" + " " * indent
        return " " * indent + sep.join(parts) + "."

    # == Condition emission ====================================================

    def _emit_condition(self, cond: ConditionExpr) -> str:
        """Emit a condition expression as AgentSpeak context.

        Args:
            cond: The condition expression to emit.

        Returns:
            AgentSpeak context string.
        """
        if isinstance(cond, FactRef):
            args = self._emit_args(cond.args)
            if args:
                return f"{cond.name}({args})"
            return cond.name

        elif isinstance(cond, ConditionNot):
            inner = self._emit_condition(cond.operand)
            return f"not ({inner})"

        elif isinstance(cond, ConditionAnd):
            parts = [self._emit_condition(op) for op in cond.operands]
            return " & ".join(parts)

        elif isinstance(cond, ConditionOr):
            parts = [self._emit_condition(op) for op in cond.operands]
            return " | ".join(parts)

        return "true"

    # == Helpers ===============================================================

    def _emit_args(self, args: List[Arg]) -> str:
        """Emit a list of arguments as a comma-separated string.

        Args:
            args: List of Arg nodes.

        Returns:
            Comma-separated argument string, or empty string.
        """
        if not args:
            return ""
        parts = []
        for a in args:
            if a.is_string:
                parts.append(f'"{a.value}"')
            else:
                parts.append(str(a.value))
        return ", ".join(parts)

    def _write_plan(
        self,
        lines: List[str],
        label: str,
        event: str,
        context_parts: List[str],
        body_stmts: List[str],
        priority: int = 0,
    ) -> None:
        """Write a complete AgentSpeak plan to the output.

        Format:
            @label[priority(N)]
            +event : context1 & context2 <-
                stmt1;
                stmt2.

        Args:
            lines:         The output line buffer.
            label:         The plan label string.
            event:         The triggering event name.
            context_parts: List of context conditions (ANDed together).
            body_stmts:    List of body statement strings.
            priority:      Numeric priority (included as annotation).
        """
        # Priority annotation
        if priority != 0:
            lines.append(f"@{label}[priority({priority})]")
        else:
            lines.append(f"@{label}")

        # Trigger + context
        context = " & ".join(context_parts) if context_parts else "true"
        lines.append(f"+{event} : {context} <-")

        # Body
        if body_stmts:
            body = ";\n    ".join(body_stmts)
            lines.append(f"    {body}.")
        else:
            lines.append(f"    true.")

        lines.append("")


# == Internal types ============================================================

class _RoleDirective:
    """Tracks a one-off Role DO directive from a Plot.

    Attributes:
        plot_name:  The source Plot name.
        phase_name: The phase (None for PLOT-wide).
        stmt:       The RoleDoStmt directive.
    """

    def __init__(
        self,
        plot_name: str,
        phase_name: Optional[str],
        stmt: RoleDoStmt,
    ) -> None:
        """Initialise a role directive.

        Args:
            plot_name:  The source Plot name.
            phase_name: The phase.
            stmt:       The RoleDoStmt.
        """
        self.plot_name: str = plot_name
        self.phase_name: Optional[str] = phase_name
        self.stmt: RoleDoStmt = stmt
