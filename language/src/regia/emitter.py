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

from typing import Dict, List, Set, Tuple

from regia.ast_nodes import (
    # Constants
    SPECIAL_ACTIONS,
    # Base elements
    ActionDecl, EventDecl, FactDecl, Arg,
    # Conditions
    ConditionExpr, ConditionNot, ConditionAnd, ConditionOr, FactRef,
    # Playbook
    DoStmt, SignalStmt, PbWhenBlock, PbIfBranch, PbElseBranch, PlaybookDef,
    # Temper (VEsNA)
    TemperSpec,
    # Imperative
    AssignStmt, UnassignStmt, WorldDoStmt, RoleDoStmt,
    InlineTransitionStmt, StartSubplotStmt, PlotEndStmt, RoleMapping,
    # Plot
    OnEnter, OnExit,
    PlotWhenBlock, PlotWhenSubplotEndsBlock, PlotWhenRoleSignalsBlock, PlotIfBranch, PlotElseBranch,
    DuringBlock, PhaseDecl, RoleDecl, PlotDef,
    # Root
    Program, DocAnnotation,
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

        # Action aliases: alias -> original_name
        self._action_aliases: Dict[str, str] = {}

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

        # Graph of role mappings: List of (SourcePlot, SourceRole, TargetPlot, TargetRole)
        self._role_mappings: List[Tuple[str, str, str, str]] = []

        # Computed transitive closures:
        # plot_name -> role_name -> set of (Plot, Role) tuples
        self._role_closures: Dict[str, Dict[str, Set[Tuple[str, str]]]] = {}

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
            elif getattr(item, "alias", None):
                self._action_aliases[item.alias] = item.name

        # Phase 2: pre-scan Plots to discover Role-Playbook assignments
        # and Role DO directives
        for item in program.items:
            if isinstance(item, PlotDef):
                self._prescan_plot(item)

        # Phase 2.5: Compute Role Transitive Closures
        self._compute_role_transitive_closures()

        # Phase 3: emit Playbook files (one per unique playbook)
        for pb_name in sorted(self._playbook_defs.keys()):
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
        phase_name: str | None,
    ) -> None:
        """Scan imperative statements for ASSIGN and Role DO.

        Args:
            stmts:      List of imperative statements.
            plot_name:  Name of the containing Plot.
            phase_name: Name of the containing phase (None for PLOT-wide).
        """
        for stmt in stmts:
            match stmt:
                case AssignStmt():
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
                case RoleDoStmt():
                    if stmt.role not in self._role_directives:
                        self._role_directives[stmt.role] = []
                    self._role_directives[stmt.role].append(
                        _RoleDirective(plot_name, phase_name, stmt)
                    )
                case StartSubplotStmt():
                    for mapping in stmt.mappings:
                        self._role_mappings.append(
                            (plot_name, mapping.source_role, stmt.plot_name, mapping.target_role)
                        )

    def _prescan_when(
        self,
        when: PlotWhenBlock | PlotWhenSubplotEndsBlock | PlotWhenRoleSignalsBlock,
        plot_name: str,
        phase_name: str | None,
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

    def _compute_role_transitive_closures(self) -> None:
        """Compute the transitive closure of role mappings."""
        # 1. Build adjacency list
        # node (Plot, Role) -> list of (Plot, Role)
        adj: Dict[Tuple[str, str], List[Tuple[str, str]]] = {}
        for src_plot, src_role, tgt_plot, tgt_role in self._role_mappings:
            u = (src_plot, src_role)
            v = (tgt_plot, tgt_role)
            if u not in adj:
                adj[u] = []
            adj[u].append(v)

        # 2. Compute closure for every known plot-role pair
        for plot_name, roles_dict in self._plot_role_playbooks.items():
            if plot_name not in self._role_closures:
                self._role_closures[plot_name] = {}
            
            for role_name in roles_dict.keys():
                closure = set()
                stack = [(plot_name, role_name)]
                while stack:
                    curr = stack.pop()
                    if curr not in closure:
                        closure.add(curr)
                        for nxt in adj.get(curr, []):
                            stack.append(nxt)
                
                self._role_closures[plot_name][role_name] = closure

    # == Emit Director =========================================================

    def _emit_director(self, plot: PlotDef) -> None:
        """Emit a Director .asl file for a Plot.

        The Director agent manages:
            - Phase state (current_phase belief)
            - ON ENTER / ON EXIT lifecycle hooks
            - WORLD DO actions
            - ASSIGN / UNASSIGN via .send
            - WHEN blocks (director-centric reactive plans)

        Args:
            plot: The PlotDef to emit a Director for.
        """
        lines: List[str] = []
        plot_lower = plot.name.lower()
        self._current_plot_name = plot.name

        # Header comment
        lines.append(
            "// ============================================\n"
            f"// Director agent for Plot: {plot.name}\n"
            "// ============================================\n"
            "// Generated by the Regia v0.2 compiler\n"
        )
        doc_str = self._format_docs(plot.docs)
        if doc_str:
            lines[0] += doc_str + "\n"

        # Initial beliefs: starting phase
        initial_phase = next(
            p.name for p in plot.phases if p.is_initial
        )
        lines.append(
            "// ============================================\n"
            "// == Initial Beliefs ==\n"
            "// ============================================\n"
            f"plot_name({plot.name.lower()}).\n"
            f"current_phase({initial_phase}).\n"
        )

        # Boot plan: fires on agent creation, runs ON ENTER
        # for the initial phase, and registers the plot identity.
        lines.append(
            "// ============================================\n"
            "// == Boot Plan ==\n"
            "// ============================================\n"
            "// Runs when the Director agent is created.\n"
            "// Registers plot identity and executes ON ENTER for the initial phase.\n"
            f"@boot__{plot.name}[atomic]\n"
            "+!boot <-\n"
            "    .my_name(Me);\n"
            "    +plot_id(Me);\n"
            f"    .print(\"[{plot.name}] Booting up director agent \", Me, \" in phase '{initial_phase}'...\");\n"
            f"    !on_enter({initial_phase}).\n"
        )

        # WHEN blocks (director-centric plans)
        self._emit_director_when_blocks(plot, lines)

        # Phase Transition Infrastructure
        self._emit_phase_infrastructure(plot, lines)

        # Role-Agent registry and communication helpers
        self._emit_role_registry(plot, lines)

        filename = f"director_{plot_lower}.asl"
        self._outputs[filename] = "\n".join(lines) + "\n"

    def _emit_phase_infrastructure(self, plot: PlotDef, lines: List[str]) -> None:
        """Emit infrastructural plans for atomic phase transitions."""
        lines.append(
            "// ============================================\n"
            "// == Phase Transition Infrastructure ==\n"
            "// ============================================\n"
            "@switch_phase_atomic[atomic]\n"
            "+!switch_phase(Target) : current_phase(Current) <-\n"
            f"    .print(\"[{plot.name}] Transitioning from phase '\", Current, \"' to '\", Target, \"'...\");\n"
            "    !on_exit(Current);\n"
            "    -current_phase(Current);\n"
            "    +current_phase(Target);\n"
            "    !on_enter(Target).\n"
        )
        
        for phase in plot.phases:
            # ON EXIT
            exit_stmts = self._get_on_exit_stmts(plot, phase.name)
            if exit_stmts:
                lines.append(f"+!on_exit({phase.name}) <-")
                body = self._emit_imperative_body(exit_stmts, indent=4)
                lines.append(body)
            # ON ENTER
            enter_stmts = self._get_on_enter_stmts(plot, phase.name)
            if enter_stmts:
                lines.append(f"+!on_enter({phase.name}) <-")
                body = self._emit_imperative_body(enter_stmts, indent=4)
                lines.append(body)

        lines.append("+!on_exit(_) <- true.")
        lines.append("+!on_enter(_) <- true.")
        lines.append("")

        lines.append(
            "// ============================================\n"
            "// == Plot Lifecycle Infrastructure ==\n"
            "// ============================================\n"
            "// If the parent terminates, it signals children with !parent_ended\n"
            "+!parent_ended[source(Parent)] : parent_plot(Parent) <-\n"
            f"    .print(\"[{plot.name}] Parent plot \", Parent, \" ended. Terminating this subplot...\");\n"
            "    -parent_plot(Parent);\n"
            "    !end_plot.\n\n"
            "@end_plot_atomic[atomic]\n"
            "+!end_plot : current_phase(Current) <-\n"
            "    .my_name(Me);\n"
            f"    .print(\"[{plot.name}] Ending plot. Running exit hooks and broadcasting termination...\");\n"
            "    !on_exit(Current);\n"
            "    .findall(C, child_plot(C, _, _), Children);\n"
            "    for ( .member(Child, Children) ) { .send(Child, achieve, parent_ended) };\n"
            "    .findall(A, role_agent(_, A), Roles);\n"
            "    for ( .member(RoleAgent, Roles) ) { .send(RoleAgent, achieve, plot_ended(Me)) };\n"
            "    !notify_parent;\n"
            "    .kill_agent(Me).\n\n"
            "+!notify_parent : parent_plot(Parent) <-\n"
            "    .my_name(Me);\n"
            f"    .send(Parent, achieve, child_ended({plot.name.lower()}, Me)).\n"
            "+!notify_parent <- true.\n\n"
            "@start_subplot_atomic[atomic]\n"
            "+!start_subplot(SubplotStr, SubplotAtom, MappingsData) <-\n"
            "    !build_bindings(MappingsData, Bindings);\n"
            "    // uses current time to generate new distinct sub-plot agent id\n"
            "    .time(HH, MM, SS, MS);\n"
            "    .my_name(Me);\n"
            "    .concat(SubplotStr, \"_\", Me, \"_\", MS, ChildId);\n"
            "    .concat(\"director_\", SubplotStr, \".asl\", SourceFile);\n"
            f"    .print(\"[{plot.name}] Spawning subplot '\", SubplotStr, \"' as agent \", ChildId, \" with bindings \", Bindings);\n"
            "    .create_agent(ChildId, SourceFile);\n"
            "    .send(ChildId, achieve, start_plot(Bindings));\n"
            "    .send(ChildId, tell, parent_plot(Me));\n"
            "    +child_plot(ChildId, SubplotAtom, MappingsData).\n\n"
            "// Recursive helper to build role agent bindings from mappings\n"
            "+!build_bindings([], []).\n"
            "+!build_bindings([map(Target, Source) | RestMappings], [map(Target, Agents) | RestBindings]) <-\n"
            "    .findall(A, role_agent(Source, A), Agents);\n"
            "    !build_bindings(RestMappings, RestBindings).\n"
        )

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
                if isinstance(when, PlotWhenRoleSignalsBlock):
                    self._emit_when_role_signals(
                        when, phase_ctx, block.phase_name, plot, lines,
                    )
                else:
                    self._emit_when_as_director(
                        when, phase_ctx, block.phase_name, plot, lines,
                    )

        if has_when:
            lines.append("")

    def _emit_when_as_director(
        self,
        when: PlotWhenBlock | PlotWhenSubplotEndsBlock,
        phase_context: str | None,
        source_phase: str | None,
        plot: PlotDef,
        lines: List[str],
    ) -> None:
        """Emit a single Plot WHEN block as Director AgentSpeak plans.

        Handles the three body forms:
            1. Pure unconditional: single plan with all stmts
            2. Pure conditional: one plan per IF branch + ELSE
            3. Mixed: prefix stmts prepended to every branch plan

        Inline TRANSITION TO statements are expanded in-place into the
        ON EXIT sequence, phase belief update, and ON ENTER sequence.

        Args:
            when:          The PlotWhenBlock or PlotWhenSubplotEndsBlock to emit.
            phase_context: Optional phase guard (e.g. "current_phase(backstage)").
            source_phase:  The source phase name (None for DURING PLOT).
            plot:          The PlotDef (needed for ON EXIT/ENTER expansion).
            lines:         The output line buffer.
        """
        priority = when.priority if when.priority is not None else 0
        plot_name = plot.name
        
        if isinstance(when, PlotWhenSubplotEndsBlock):
            event_name = f"!child_ended({when.subplot_name.lower()}, _)"
            event_label = f"subplot_{when.subplot_name.lower()}_ended"
        else:
            event_name = f"!{when.event}" if when.event in ["parent_ended", "child_ended"] else when.event
            event_label = when.event

        def _expand_stmts(stmts: list) -> List[str]:
            """Expand a stmt list."""
            result: List[str] = []
            for s in stmts:
                result.append(self._emit_imperative_stmt(s))
            return result

        # Case 1: no branches (unconditional)
        if not when.branches:
            context_parts: List[str] = []
            if phase_context:
                context_parts.append(phase_context)

            body_stmts = _expand_stmts(when.prefix_stmts)

            label = f"dir__{plot_name}__{event_label}__0"
            self._write_plan(
                lines, label, event_name, context_parts, body_stmts, priority,
            )
            return

        # Case 2 & 3: branches (with optional prefix)
        prefix_stmts = _expand_stmts(when.prefix_stmts)

        for idx, branch in enumerate(when.branches):
            context_parts = []
            if phase_context:
                context_parts.append(phase_context)
            context_parts.append(
                self._emit_condition(branch.condition)
            )

            body_stmts = prefix_stmts + _expand_stmts(branch.stmts)

            label = f"dir__{plot_name}__{event_label}__{idx}"
            self._write_plan(
                lines, label, event_name, context_parts, body_stmts, priority,
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

            body_stmts = prefix_stmts + _expand_stmts(when.else_branch.stmts)

            label = f"dir__{plot_name}__{event_label}__{len(when.branches)}"
            self._write_plan(
                lines, label, event_name, context_parts, body_stmts, priority,
            )

    def _emit_when_role_signals(
        self,
        when: PlotWhenRoleSignalsBlock,
        phase_context: str | None,
        source_phase: str | None,
        plot: PlotDef,
        lines: List[str],
    ) -> None:
        """Emit a WHEN ROLE X SIGNALS y block as a source-filtered Director plan.

        The trigger becomes: +event[source(Sender)]
        An extra guard is injected: role_agent(role_lower, Sender)

        Args:
            when:          The PlotWhenRoleSignalsBlock to emit.
            phase_context: Optional phase guard string.
            source_phase:  The source phase name (None for DURING PLOT).
            plot:          The PlotDef (needed for transition expansion).
            lines:         The output line buffer.
        """
        priority   = when.priority if when.priority is not None else 0
        plot_name  = plot.name
        role_lower = when.role_name.lower()
        event_name = when.event

        # The trigger must carry the source annotation to unify Sender
        trigger = f"{event_name}[source(Sender)]"

        # Build event label for plan annotation (unique, readable)
        event_label = f"{role_lower}_signals_{event_name}"

        def _expand_stmts(stmts: list) -> List[str]:
            result: List[str] = []
            for s in stmts:
                result.append(self._emit_imperative_stmt(s))
            return result

        def _build_context(extra_condition: str | None = None) -> List[str]:
            parts: List[str] = []
            if phase_context:
                parts.append(phase_context)
            # Role guard: Sender must be a known agent playing the role
            parts.append(f"role_agent({role_lower}, Sender)")
            if extra_condition:
                parts.append(extra_condition)
            return parts

        # No branches: single unconditional plan
        if not when.branches:
            body_stmts = _expand_stmts(when.prefix_stmts)
            label = f"dir__{plot_name}__{event_label}__0"
            self._write_plan(lines, label, trigger, _build_context(), body_stmts, priority)
            return

        # With branches
        prefix_stmts = _expand_stmts(when.prefix_stmts)
        for idx, branch in enumerate(when.branches):
            condition_str = self._emit_condition(branch.condition)
            body_stmts = prefix_stmts + _expand_stmts(branch.stmts)
            label = f"dir__{plot_name}__{event_label}__{idx}"
            self._write_plan(lines, label, trigger, _build_context(condition_str), body_stmts, priority)

        # ELSE branch
        if when.else_branch is not None:
            negated = [f"not ({self._emit_condition(b.condition)})" for b in when.branches]
            else_ctx = _build_context()
            else_ctx.extend(negated)
            body_stmts = prefix_stmts + _expand_stmts(when.else_branch.stmts)
            label = f"dir__{plot_name}__{event_label}__{len(when.branches)}"
            self._write_plan(lines, label, trigger, else_ctx, body_stmts, priority)

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
        lines.append(
            "// ============================================\n"
            "// == Role-Agent Registry ==\n"
            "// ============================================\n"
            "// Populated at plot startup via !start_plot.\n"
            f"@dir__{plot.name}__start_plot__0\n"
            "+!start_plot(Bindings) <-\n"
            "    for ( .member(map(Role, Agents), Bindings) ) {\n"
            "        for ( .member(Agent, Agents) ) {\n"
            "            +role_agent(Role, Agent);\n"
            "        }\n"
            "    };\n"
            "    !boot.\n\n"
            f"@dir__{plot.name}__send_to_role__0\n"
            "+!send_to_role(Role, Performative, Content) <-\n"
            "    .findall(A, role_agent(Role, A), Agents);\n"
            "    .send(Agents, Performative, Content).\n\n"
            "// Handle agent death (broadcast by the environment) to avoid stalling\n"
            f"@dir__{plot.name}__agent_died__0[atomic]\n"
            "+agent_died(DeadAgent) : role_agent(Role, DeadAgent) <-\n"
            f"    .print(\"[{plot.name}] Agent \", DeadAgent, \" playing role '\", Role, \"' has died! Cleaning registry...\");\n"
            "    -role_agent(Role, DeadAgent).\n"
        )

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

        lines.append(
            "// ============================================\n"
            f"// == Playbook: {pb_name} ==\n"
            "// ============================================\n"
            "// Generated by the Regia v0.2 compiler\n"
            f"// Plans are gated by playbook_active({pb_name.lower()}, _).\n"
            "// Included by role templates that use this playbook.\n"
        )
        doc_str = self._format_docs(pb_def.docs)
        if doc_str:
            lines[0] += doc_str + "\n"

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

        lines.append(
            "// ============================================\n"
            f"// == Role: {role_name} in Plot: {plot_name} ==\n"
            "// ============================================\n"
            "// Generated by the Regia v0.2 compiler\n"
        )

        # Include directives for each assignable Playbook in the transitive closure
        reachable_roles = self._role_closures.get(plot_name, {}).get(role_name, {(plot_name, role_name)})
        
        all_playbooks = set()
        for p_name, r_name in reachable_roles:
            all_playbooks.update(
                self._plot_role_playbooks.get(p_name, {}).get(r_name, set())
            )
        playbooks = sorted(all_playbooks)
        if playbooks:
            lines.append(
                "// ============================================\n"
                "// == Included Playbooks ==\n"
                "// ============================================"
            )
            for pb in playbooks:
                pb_lower_name = pb.lower()
                lines.append(
                    f'{{ include("playbook_{pb_lower_name}.asl") }}'
                )
            lines.append("")

        # Playbook activation handlers: when the Director tells
        # this agent to add/remove a playbook, toggle the belief.
        lines.append(
            "// ============================================\n"
            "// == Playbook Management ==\n"
            "// ============================================\n"
            "// When the Director assigns a playbook, add the\n"
            "// playbook_active belief to enable its gated plans.\n"
            "+!add_playbook(Name)[source(Sender)] <-\n"
            f"    .print(\"[{role_name}] Added playbook \", Name, \" from \", Sender);\n"
            "    +playbook_active(Name, Sender).\n\n"
            "+!remove_playbook(Name)[source(Sender)] <-\n"
            f"    .print(\"[{role_name}] Removed playbook \", Name, \" from \", Sender);\n"
            "    -playbook_active(Name, Sender).\n\n"
            "// Cleanup ghost playbooks when the Plot terminates\n"
            "+!plot_ended(PlotId)[source(PlotId)] <-\n"
            "    -playbook_active(_, PlotId).\n\n"
            "// Signal all active directors for a given playbook\n"
            "+!signal_directors(PbName, Payload) <-\n"
            f"    .print(\"[{role_name}] Signaling directors of \", PbName, \" with \", Payload);\n"
            "    .findall(D, playbook_active(PbName, D), Directors);\n"
            "    for ( .member(DirectorId, Directors) ) { .send(DirectorId, untell, Payload); .send(DirectorId, tell, Payload) }.\n"
        )

        # Generate handler plans for Role DO directives across the transitive closure
        handler_plans = set()
        for p_name, r_name in reachable_roles:
            for d in self._role_directives.get(r_name, []):
                if d.plot_name != p_name:
                    continue
                stmt = d.stmt
                args = self._emit_args(stmt.args)
                action_lower = stmt.action.lower()
                goal = f"{action_lower}({args})" if args else action_lower

                if stmt.is_special:
                    do = DoStmt(action=stmt.action, is_special=True, args=stmt.args)
                    body = self._emit_do_stmt(do)
                else:
                    action_name = self._action_aliases.get(stmt.action, stmt.action)
                    body = f"{action_name}({args})" if args else action_name

                import re # move upwards
                safe_goal = re.sub(r'[^a-zA-Z0-9]', '_', goal)
                handler_plans.add(
                    f"@role__{p_name.lower()}__{r_name.lower()}__{safe_goal}\n"
                    f"+!{goal} <- {body}."
                )

        if handler_plans:
            lines.append(
                "// ============================================\n"
                "// == Director Commands ==\n"
                "// ============================================"
            )
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
        gate = f"playbook_active({pb.name.lower()}, _)"

        for when in pb.when_blocks:
            priority = when.priority if when.priority is not None else 0

            # Case 1: no branches (unconditional)
            if not when.branches:
                body_stmts = [
                    self._emit_pb_stmt(s, pb.name.lower()) for s in when.prefix_stmts
                ]
                label = f"pb__{pb.name}__{when.event}__0"
                self._write_plan(
                    lines, label, when.event, [gate], body_stmts, priority,
                    temper=when.temper,
                )
                continue

            # Case 2 & 3: branches (with optional prefix)
            prefix_stmts = [
                self._emit_pb_stmt(s, pb.name.lower()) for s in when.prefix_stmts
            ]

            for idx, branch in enumerate(when.branches):
                context_parts = [gate]
                context_parts.append(
                    self._emit_condition(branch.condition)
                )

                body_stmts = prefix_stmts + [
                    self._emit_pb_stmt(s, pb.name.lower()) for s in branch.stmts
                ]

                label = f"pb__{pb.name}__{when.event}__{idx}"
                self._write_plan(
                    lines, label, when.event, context_parts, body_stmts,
                    priority, temper=when.temper,
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
                    self._emit_pb_stmt(s, pb.name.lower())
                    for s in when.else_branch.stmts
                ]

                label = f"pb__{pb.name}__{when.event}__{len(when.branches)}"
                self._write_plan(
                    lines, label, when.event, context_parts, body_stmts,
                    priority, temper=when.temper,
                )

    # == Statement emission ====================================================

    def _emit_pb_stmt(self, stmt: object, pb_name: str) -> str:
        """Emit a single Playbook statement as AgentSpeak.

        Args:
            stmt: A DoStmt or SignalStmt.
            pb_name: The lowercase name of the playbook.

        Returns:
            AgentSpeak string for this statement.
        """
        match stmt:
            case DoStmt():
                return self._emit_do_stmt(stmt)
            case SignalStmt():
                return self._emit_signal_stmt(stmt, pb_name)
            case _:
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
        action_name = self._action_aliases.get(stmt.action, stmt.action)
        if not stmt.is_special:
            args = self._emit_args(stmt.args)
            if args:
                return f"{action_name}({args})"
            return action_name

        # Special actions
        def _fmt(index: int, default: str) -> str:
            if index < len(stmt.args):
                a = stmt.args[index]
                return f'"{a.value}"' if a.is_string else str(a.value)
            return default

        match stmt.action:
            case "TELL":
                target = _fmt(0, "unknown")
                msg = _fmt(1, "msg")
                return f".send({target}, tell, {msg})"
            case "BROADCAST":
                msg = _fmt(0, "msg")
                return f".broadcast(tell, {msg})"
            case "ACHIEVE":
                goal = _fmt(0, "goal")
                return f"!{goal}"
            case "BELIEVE":
                fact = _fmt(0, "fact")
                return f"+{fact}"
            case "FORGET":
                fact = _fmt(0, "fact")
                return f"-{fact}"
            case "PRINT":
                args_str = self._emit_args(stmt.args)
                return f".print({args_str})"
            case "WAIT":
                args_str = self._emit_args(stmt.args)
                return f".wait({args_str})"
            case _:
                return f"/* unknown special: {stmt.action} */"

    def _emit_signal_stmt(self, stmt: SignalStmt, pb_name: str) -> str:
        """Emit a SIGNAL statement as AgentSpeak.

        SIGNAL delegates to the Role's !signal_directors infrastructural plan.

        Args:
            stmt: The SignalStmt to emit.
            pb_name: The playbook name to search for active instances.

        Returns:
            AgentSpeak string.
        """
        args = self._emit_args(stmt.args)
        payload = f"{stmt.event}({args})" if args else stmt.event
        return f"!signal_directors({pb_name}, {payload})"

    def _emit_imperative_stmt(self, stmt: object) -> str:
        """Emit an imperative statement (Director context).

        For InlineTransitionStmt, use _emit_inline_transition_stmts
        instead (it returns a List[str] due to the multi-step expansion).
        This method returns a fallback comment if called directly on one.

        Args:
            stmt: An AssignStmt, UnassignStmt, WorldDoStmt, RoleDoStmt,
                  or InlineTransitionStmt.

        Returns:
            AgentSpeak string.
        """
        match stmt:
            case AssignStmt():
                # Director sends add_playbook goal to all agents
                # bound to this role
                role_lower = stmt.role.lower()
                return (
                    f"!send_to_role({role_lower}, achieve, "
                    f"add_playbook({stmt.playbook.lower()}))"
                )
            case UnassignStmt():
                role_lower = stmt.role.lower()
                return (
                    f"!send_to_role({role_lower}, achieve, "
                    f"remove_playbook({stmt.playbook.lower()}))"
                )
            case WorldDoStmt():
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
            case RoleDoStmt():
                role_lower = stmt.role.lower()
                args = self._emit_args(stmt.args)
                action_lower = stmt.action.lower()
                goal = f"{action_lower}({args})" if args else action_lower
                return f"!send_to_role({role_lower}, achieve, {goal})"
            case InlineTransitionStmt():
                return f"!switch_phase({stmt.target_phase})"
            case StartSubplotStmt():
                return self._emit_start_subplot_stmts(stmt)
            case PlotEndStmt():
                return "!end_plot"
            case _:
                return f"/* unknown imperative */"



    def _emit_start_subplot_stmts(
        self,
        stmt: StartSubplotStmt,
    ) -> str:
        """Expand a START SUBPLOT statement into a direct infrastructural call."""
        child_lower = stmt.plot_name.lower()

        if stmt.mappings:
            map_pairs = ", ".join(
                f"map({m.target_role.lower()}, {m.source_role.lower()})"
                for m in stmt.mappings
            )
            mappings_str = f"[{map_pairs}]"
        else:
            mappings_str = "[]"

        return f'!start_subplot("{child_lower}", {stmt.plot_name.lower()}, {mappings_str})'



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

    def _emit_condition(self, cond: ConditionExpr, _parent_is_and: bool = False) -> str:
        """Emit a condition expression as AgentSpeak context.

        Parenthesizes ConditionOr nodes when they appear as children of a
        ConditionAnd, because Jason (like Prolog) gives & higher precedence
        than |.  Without this, `(A OR B) AND C` would be emitted as
        `A | B & C`, which Jason reads as `A | (B & C)` — wrong semantics.

        Args:
            cond:           The condition expression to emit.
            _parent_is_and: True when this call is being made from inside a
                            ConditionAnd serialisation (internal use only).

        Returns:
            AgentSpeak context string, correctly parenthesized.
        """
        match cond:
            case FactRef():
                args = self._emit_args(cond.args)
                if args:
                    return f"{cond.name}({args})"
                return cond.name
            case ConditionNot():
                # _parent_is_and=False: NOT already wraps in parens so the
                # inner expression precedence cannot cause ambiguity here.
                inner = self._emit_condition(cond.operand)
                return f"not ({inner})"
            case ConditionAnd():
                # Children that are OR must be parenthesized (OR < AND in precedence).
                parts = [self._emit_condition(op, _parent_is_and=True) for op in cond.operands]
                result = " & ".join(parts)
                return result
            case ConditionOr():
                parts = [self._emit_condition(op) for op in cond.operands]
                result = " | ".join(parts)
                # If our parent is an AND (or higher-precedence context),
                # wrap ourselves in parens so the grouping is preserved.
                if _parent_is_and:
                    return f"({result})"
                return result
            case _:
                return "true"


    # == Helpers ===============================================================

    def _format_docs(self, docs: List[DocAnnotation]) -> str:
        """Format a list of DocAnnotations as // comment lines.

        Args:
            docs: A list of DocAnnotation nodes.

        Returns:
            A string containing the formatted comments, or an empty string.
        """
        if not docs:
            return ""
        
        lines = ["//"]
        for doc in docs:
            doc_lines = doc.value.splitlines()
            for i, sub_line in enumerate(doc_lines):
                if i == 0:
                    lines.append(f"// {doc.key}: {sub_line}")
                else:
                    lines.append(f"//   {sub_line}")
        return "\n".join(lines) + "\n"

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
        temper: TemperSpec | None = None,
    ) -> None:
        """Write a complete AgentSpeak plan to the output.

        Format:
            @label[priority(N), temper([...]), effects([...])]
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
            temper:        Optional temper/effects annotation (VEsNA).
        """
        # Build annotation list
        annotations: List[str] = []
        if priority != 0:
            annotations.append(f"priority({priority})")
        if temper is not None:
            dims = ", ".join(
                f"{e.name}({e.value})" for e in temper.dimensions
            )
            annotations.append(f"temper([{dims}])")
            if temper.effects:
                effs = ", ".join(
                    f"{e.name}({e.value})" for e in temper.effects
                )
                annotations.append(f"effects([{effs}])")

        if annotations:
            lines.append(f"@{label}[{', '.join(annotations)}]")
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
        phase_name: str | None,
        stmt: RoleDoStmt,
    ) -> None:
        """Initialise a role directive.

        Args:
            plot_name:  The source Plot name.
            phase_name: The phase.
            stmt:       The RoleDoStmt.
        """
        self.plot_name: str = plot_name
        self.phase_name: str | None = phase_name
        self.stmt: RoleDoStmt = stmt
