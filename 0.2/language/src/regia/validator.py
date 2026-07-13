"""
Semantic validator for the Regia compiler.

Walks the typed AST produced by the builder and checks for logical
errors that the grammar cannot catch. This is the first pass that
can report user-facing error messages with source locations.

Responsibilities:
    1. Build a symbol table of all declared elements (actions, events,
       facts, playbooks, roles, phases).
    2. Check for duplicate declarations within each namespace.
    3. Check for undeclared references (DO an action that was never
       declared, use a fact in a condition that was never declared, etc.).
    4. Check structural constraints (exactly one INITIAL phase per Plot,
       at most one ON ENTER/EXIT per DURING block, etc.).
    5. Warn about declared-but-never-used elements.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set

from regia.ast_nodes import (
    # Shared
    SourceLoc, SPECIAL_ACTIONS,
    # Imports
    ImportDecl,
    # Base elements
    ActionDecl, EventDecl, FactDecl,
    # Conditions
    FactRef, ConditionNot, ConditionAnd, ConditionOr, ConditionExpr,
    # Playbook
    DoStmt, SignalStmt, PbIfBranch, PbElseBranch, PbWhenBlock, PlaybookDef,
    # Imperative
    AssignStmt, UnassignStmt, WorldDoStmt, RoleDoStmt, InlineTransitionStmt,
    # Plot
    TransitionStmt, OnEnter, OnExit,
    PlotIfBranch, PlotElseBranch, PlotWhenBlock,
    DuringBlock, PhaseDecl, RoleDecl, PlotDef,
    # Root
    Program,
)
from regia.errors import ErrorReporter


# == Symbol table ==============================================================
# Records where each name was declared, so we can report both the
# "first declared here" location and the "duplicate" location.

class _SymbolTable:
    """Tracks declared names and their source locations.

    Maintains separate namespaces for actions, events, facts,
    playbooks, and per-plot scopes for roles and phases.

    Attributes:
        actions:   Declared action names -> source location.
        events:    Declared event names -> source location.
        facts:     Declared fact names -> source location.
        playbooks: Declared playbook names -> source location.
    """

    def __init__(self) -> None:
        """Initialise empty symbol table."""
        self.actions:   Dict[str, SourceLoc] = {}
        self.events:    Dict[str, SourceLoc] = {}
        self.facts:     Dict[str, SourceLoc] = {}
        self.playbooks: Dict[str, SourceLoc] = {}


class _PlotScope:
    """Per-plot scope tracking roles and phases.

    Attributes:
        plot_name: The name of the plot being validated.
        roles:     Declared role names -> source location.
        phases:    Declared phase names -> source location.
    """

    def __init__(self, plot_name: str) -> None:
        """Initialise a scope for the given plot.

        Args:
            plot_name: The plot identifier.
        """
        self.plot_name: str = plot_name
        self.roles:  Dict[str, SourceLoc] = {}
        self.phases: Dict[str, SourceLoc] = {}


# == Validator =================================================================

class Validator:
    """Walks the AST and reports semantic errors and warnings.

    Usage:
        validator = Validator(reporter)
        validator.validate(program)
        # Errors/warnings are now in reporter.messages

    The validator does NOT modify the AST. It only reads it and
    reports issues to the ErrorReporter.
    """

    def __init__(self, reporter: ErrorReporter) -> None:
        """Initialise the validator.

        Args:
            reporter: The shared error reporter to record diagnostics.
        """
        self._reporter: ErrorReporter = reporter
        self._symbols: _SymbolTable = _SymbolTable()

        # Usage trackers: names that were actually referenced
        # somewhere. After validation, any declared name NOT in
        # these sets triggers an "unused" warning.
        self._used_actions:   Set[str] = set()
        self._used_events:    Set[str] = set()
        self._used_facts:     Set[str] = set()
        self._used_playbooks: Set[str] = set()

    # == Public API ============================================================

    def validate(self, program: Program) -> None:
        """Run all semantic checks on the program.

        Args:
            program: The root AST node to validate.
        """
        # Phase 1: collect all declarations into the symbol table
        self._collect_declarations(program)

        # Phase 2: validate each top-level item
        for item in program.items:
            if isinstance(item, PlaybookDef):
                self._validate_playbook(item)
            elif isinstance(item, PlotDef):
                self._validate_plot(item)

        # Phase 3: warn about unused declarations
        self._check_unused()

    # == Phase 1: collect declarations =========================================

    def _collect_declarations(self, program: Program) -> None:
        """Walk top-level items and register all declarations.

        Checks for duplicates within each namespace.

        Args:
            program: The root AST node.
        """
        for item in program.items:
            if isinstance(item, ImportDecl):
                pass  # Import paths are resolved before validation
            elif isinstance(item, ActionDecl):
                self._declare(
                    self._symbols.actions, "action", item.name, item.loc,
                )
            elif isinstance(item, EventDecl):
                self._declare(
                    self._symbols.events, "event", item.name, item.loc,
                )
            elif isinstance(item, FactDecl):
                self._declare(
                    self._symbols.facts, "fact", item.name, item.loc,
                )
            elif isinstance(item, PlaybookDef):
                self._declare(
                    self._symbols.playbooks, "playbook", item.name, item.loc,
                )
            elif isinstance(item, PlotDef):
                # Plots themselves don't need a namespace check for
                # now (single-file, one plot is typical). But we could
                # add duplicate plot detection if needed.
                pass

    def _declare(
        self,
        namespace: Dict[str, SourceLoc],
        kind: str,
        name: str,
        loc: SourceLoc,
    ) -> None:
        """Register a name in a namespace, reporting duplicates.

        Args:
            namespace: The dict to register into (e.g. symbols.actions).
            kind:      Human-readable kind ("action", "event", etc.).
            name:      The identifier being declared.
            loc:       Source location of this declaration.
        """
        if name in namespace:
            prev = namespace[name]
            self._error(
                loc,
                f"Duplicate {kind} declaration: '{name}'"
                f" (previously declared at line {prev.line}).",
            )
            return

        namespace[name] = loc

    # == Phase 2a: validate Playbooks ==========================================

    def _validate_playbook(self, pb: PlaybookDef) -> None:
        """Validate a Playbook definition.

        Checks:
            - WHEN block events are declared.
            - Actions in DO statements are declared.
            - Facts in IF conditions are declared.
            - Signal events are declared.

        Args:
            pb: The PlaybookDef to validate.
        """
        for when in pb.when_blocks:
            self._check_event_ref(when.event, when.loc)

            # Validate prefix statements
            for stmt in when.prefix_stmts:
                self._validate_pb_stmt(stmt)

            # Validate IF branches
            for branch in when.branches:
                self._validate_condition(branch.condition)
                for stmt in branch.stmts:
                    self._validate_pb_stmt(stmt)

            # Validate ELSE branch
            if when.else_branch is not None:
                for stmt in when.else_branch.stmts:
                    self._validate_pb_stmt(stmt)

    def _validate_pb_stmt(self, stmt: object) -> None:
        """Validate a single Playbook statement (DO or SIGNAL).

        Args:
            stmt: A DoStmt or SignalStmt.
        """
        if isinstance(stmt, DoStmt):
            self._check_action_ref(stmt.action, stmt.is_special, stmt.loc)
        elif isinstance(stmt, SignalStmt):
            self._check_event_ref(stmt.event, stmt.loc)

    # == Phase 2b: validate Plots ==============================================

    def _validate_plot(self, plot: PlotDef) -> None:
        """Validate a Plot definition.

        Checks:
            - Exactly one INITIAL phase.
            - No duplicate roles or phases within the plot.
            - DURING blocks reference declared phases.
            - At most one ON ENTER and one ON EXIT per DURING block.
            - DURING PLOT blocks do not contain transitions.
            - All WHEN event references, action references, fact
              references, playbook references, and role references
              are declared.
            - Transition targets reference declared phases.

        Args:
            plot: The PlotDef to validate.
        """
        scope = _PlotScope(plot.name)

        # Register phases and roles within this plot's scope
        for phase in plot.phases:
            self._declare(scope.phases, "phase", phase.name, phase.loc)
        for role in plot.roles:
            self._declare(scope.roles, "role", role.name, role.loc)

        # Check exactly one INITIAL phase
        initial_phases = [p for p in plot.phases if p.is_initial]
        if len(initial_phases) == 0:
            self._error(
                plot.loc,
                f"Plot '{plot.name}' has no INITIAL phase.",
                hint="Mark one phase with INITIAL: PHASE backstage INITIAL.",
            )
        elif len(initial_phases) > 1:
            second = initial_phases[1]
            self._error(
                second.loc,
                f"Plot '{plot.name}' has multiple INITIAL phases "
                f"(first at line {initial_phases[0].loc.line}).",
                hint="Only one phase can be marked INITIAL.",
            )

        # Validate each DURING block
        for block in plot.during_blocks:
            self._validate_during_block(block, scope)

    def _validate_during_block(
        self,
        block: DuringBlock,
        scope: "_PlotScope",
    ) -> None:
        """Validate a single DURING block.

        Args:
            block: The DuringBlock to validate.
            scope: The per-plot scope for role/phase lookups.
        """
        # Check phase reference for phase-specific blocks
        if block.phase_name is not None:
            if block.phase_name not in scope.phases:
                self._error(
                    block.loc,
                    f"DURING references undeclared phase: "
                    f"'{block.phase_name}'.",
                    hint=(
                        f"Add 'PHASE {block.phase_name}.' to "
                        f"plot '{scope.plot_name}'."
                    ),
                )

        # Check for transitions in plot-wide blocks
        if block.phase_name is None and len(block.transitions) > 0:
            self._error(
                block.transitions[0].loc,
                "TRANSITION cannot appear inside DURING PLOT "
                "(transitions need a source phase).",
                hint="Move this TRANSITION to a phase-specific "
                     "DURING block.",
            )

        # Check at most one ON ENTER / ON EXIT
        if len(block.on_enters) > 1:
            self._error(
                block.on_enters[1].loc,
                "Duplicate ON ENTER block "
                f"(first at line {block.on_enters[0].loc.line}).",
                hint="Merge the statements into a single ON ENTER.",
            )
        if len(block.on_exits) > 1:
            self._error(
                block.on_exits[1].loc,
                "Duplicate ON EXIT block "
                f"(first at line {block.on_exits[0].loc.line}).",
                hint="Merge the statements into a single ON EXIT.",
            )

        # Validate transitions
        for tr in block.transitions:
            self._validate_transition(tr, scope)

        # Validate ON ENTER / ON EXIT stmts
        # InlineTransitionStmt is NOT allowed in ON ENTER/EXIT; those
        # hooks execute during an already-in-progress phase change and
        # a second inline transition would be ambiguous.
        for on_enter in block.on_enters:
            for stmt in on_enter.stmts:
                if isinstance(stmt, InlineTransitionStmt):
                    self._error(
                        stmt.loc,
                        "TRANSITION TO cannot appear inside ON ENTER.",
                        hint="Use a declarative TRANSITION TO ... WHEN ... "
                             "instead, or move the transition to a WHEN block.",
                    )
                else:
                    self._validate_imperative_stmt(stmt, scope)
        for on_exit in block.on_exits:
            for stmt in on_exit.stmts:
                if isinstance(stmt, InlineTransitionStmt):
                    self._error(
                        stmt.loc,
                        "TRANSITION TO cannot appear inside ON EXIT.",
                        hint="Use a declarative TRANSITION TO ... WHEN ... "
                             "instead, or move the transition to a WHEN block.",
                    )
                else:
                    self._validate_imperative_stmt(stmt, scope)

        # Validate WHEN blocks
        for when in block.when_blocks:
            self._validate_plot_when_block(when, scope, block.phase_name)

    def _validate_transition(
        self,
        tr: TransitionStmt,
        scope: _PlotScope,
    ) -> None:
        """Validate a TRANSITION statement.

        Args:
            tr:    The transition to validate.
            scope: The per-plot scope.
        """
        # Target phase must be declared
        if tr.target_phase not in scope.phases:
            self._error(
                tr.loc,
                f"TRANSITION targets undeclared phase: "
                f"'{tr.target_phase}'.",
                hint=(
                    f"Add 'PHASE {tr.target_phase}.' to "
                    f"plot '{scope.plot_name}'."
                ),
            )

        # Triggering event must be declared
        self._check_event_ref(tr.event, tr.loc)

        # Optional guard condition
        if tr.guard is not None:
            self._validate_condition(tr.guard)

    def _validate_plot_when_block(
        self,
        when: PlotWhenBlock,
        scope: "_PlotScope",
        phase_name: Optional[str] = None,
    ) -> None:
        """Validate a Plot WHEN block.

        Also enforces that InlineTransitionStmt only appears in
        phase-specific DURING blocks (not DURING PLOT) and that
        it is always the last statement in any body or branch.

        Args:
            when:       The PlotWhenBlock to validate.
            scope:      The per-plot scope.
            phase_name: The phase this WHEN block lives in, or None
                        for DURING PLOT blocks.
        """
        self._check_event_ref(when.event, when.loc)

        # Validate prefix stmts and check position of inline transitions
        self._check_stmt_list_for_inline_transition(
            when.prefix_stmts, phase_name, context="WHEN prefix",
        )
        for stmt in when.prefix_stmts:
            self._validate_imperative_stmt(stmt, scope)

        for branch in when.branches:
            self._validate_condition(branch.condition)
            self._check_stmt_list_for_inline_transition(
                branch.stmts, phase_name, context="IF branch",
            )
            for stmt in branch.stmts:
                self._validate_imperative_stmt(stmt, scope)

        if when.else_branch is not None:
            self._check_stmt_list_for_inline_transition(
                when.else_branch.stmts, phase_name, context="ELSE branch",
            )
            for stmt in when.else_branch.stmts:
                self._validate_imperative_stmt(stmt, scope)

    def _validate_imperative_stmt(
        self,
        stmt: object,
        scope: "_PlotScope",
    ) -> None:
        """Validate a single imperative statement (ASSIGN, WORLD DO, etc).

        Args:
            stmt:  The statement to validate.
            scope: The per-plot scope for role lookups.
        """
        if isinstance(stmt, AssignStmt):
            self._check_playbook_ref(stmt.playbook, stmt.loc)
            self._check_role_ref(stmt.role, stmt.loc, scope)

        elif isinstance(stmt, UnassignStmt):
            self._check_playbook_ref(stmt.playbook, stmt.loc)
            self._check_role_ref(stmt.role, stmt.loc, scope)

        elif isinstance(stmt, WorldDoStmt):
            self._check_action_ref(stmt.action, stmt.is_special, stmt.loc)

        elif isinstance(stmt, RoleDoStmt):
            self._check_role_ref(stmt.role, stmt.loc, scope)
            self._check_action_ref(stmt.action, stmt.is_special, stmt.loc)

        elif isinstance(stmt, InlineTransitionStmt):
            self._check_inline_transition(stmt, scope)

    # == Condition validation ===================================================

    def _validate_condition(self, cond: ConditionExpr) -> None:
        """Recursively validate a condition expression.

        Ensures all fact references in the condition are declared.

        Args:
            cond: The condition expression to validate.
        """
        if isinstance(cond, FactRef):
            self._check_fact_ref(cond.name, cond.loc)

        elif isinstance(cond, ConditionNot):
            self._validate_condition(cond.operand)

        elif isinstance(cond, ConditionAnd):
            for operand in cond.operands:
                self._validate_condition(operand)

        elif isinstance(cond, ConditionOr):
            for operand in cond.operands:
                self._validate_condition(operand)

    # == Reference checkers ====================================================
    # Each checker verifies that a referenced name exists in the
    # symbol table and marks it as used for the unused-warning pass.

    def _check_inline_transition(
        self,
        stmt: InlineTransitionStmt,
        scope: "_PlotScope",
    ) -> None:
        """Validate an inline TRANSITION TO statement.

        Checks that the target phase is declared in the current plot.
        Position checking (must be last in list) is done by
        _check_stmt_list_for_inline_transition before this method is
        called.

        Args:
            stmt:  The InlineTransitionStmt to validate.
            scope: The per-plot scope.
        """
        if stmt.target_phase not in scope.phases:
            self._error(
                stmt.loc,
                f"Inline TRANSITION targets undeclared phase: "
                f"'{stmt.target_phase}'.",
                hint=(
                    f"Add 'PHASE {stmt.target_phase}.' to "
                    f"plot '{scope.plot_name}'."
                ),
            )

    def _check_stmt_list_for_inline_transition(
        self,
        stmts: List,
        phase_name: Optional[str],
        context: str,
    ) -> None:
        """Enforce inline transition placement rules on a statement list.

        Rules enforced:
            1. InlineTransitionStmt may only appear in a phase-specific
               DURING block (not in DURING PLOT).
            2. InlineTransitionStmt must be the last statement in the
               list. Any occurrence before the end is an error.

        Args:
            stmts:      The list of imperative statements to check.
            phase_name: The containing phase (None for DURING PLOT).
            context:    Human-readable context for error messages.
        """
        for i, stmt in enumerate(stmts):
            if not isinstance(stmt, InlineTransitionStmt):
                continue

            # Rule 1: not allowed in DURING PLOT
            if phase_name is None:
                self._error(
                    stmt.loc,
                    f"Inline TRANSITION TO cannot appear inside "
                    f"DURING PLOT ({context}).",
                    hint="Move this transition to a phase-specific "
                         "DURING block.",
                )
                continue

            # Rule 2: must be the last statement
            if i < len(stmts) - 1:
                self._error(
                    stmts[i + 1].loc,
                    f"Unreachable statement after TRANSITION TO "
                    f"in {context}.",
                    hint="TRANSITION TO must be the last statement "
                         "in a body or branch.",
                )

    # =====================================================================

    def _check_action_ref(
        self,
        name: str,
        is_special: bool,
        loc: SourceLoc,
    ) -> None:
        """Check that a referenced action is declared.

        Special actions (TELL, BROADCAST, etc.) are built-in and
        always valid; they don't need a declaration.

        Args:
            name:       The action name.
            is_special: True if this is a special AgentSpeak primitive.
            loc:        Source location of the reference.
        """
        if is_special:
            return  # Built-in, always valid

        if name not in self._symbols.actions:
            self._error(
                loc,
                f"Undeclared action: '{name}'.",
                hint=f"Add 'ACTION {name}.' at the top of the file.",
            )
            return

        self._used_actions.add(name)

    def _check_event_ref(self, name: str, loc: SourceLoc) -> None:
        """Check that a referenced event is declared.

        Args:
            name: The event name.
            loc:  Source location of the reference.
        """
        if name not in self._symbols.events:
            self._error(
                loc,
                f"Undeclared event: '{name}'.",
                hint=f"Add 'EVENT {name}.' at the top of the file.",
            )
            return

        self._used_events.add(name)

    def _check_fact_ref(self, name: str, loc: SourceLoc) -> None:
        """Check that a referenced fact is declared.

        Args:
            name: The fact name.
            loc:  Source location of the reference.
        """
        if name not in self._symbols.facts:
            self._error(
                loc,
                f"Undeclared fact: '{name}'.",
                hint=f"Add 'FACT {name}.' at the top of the file.",
            )
            return

        self._used_facts.add(name)

    def _check_playbook_ref(self, name: str, loc: SourceLoc) -> None:
        """Check that a referenced playbook is declared.

        Args:
            name: The playbook name.
            loc:  Source location of the reference.
        """
        if name not in self._symbols.playbooks:
            self._error(
                loc,
                f"Undeclared playbook: '{name}'.",
                hint=f"Add a 'PLAYBOOK {name}: ...' definition.",
            )
            return

        self._used_playbooks.add(name)

    def _check_role_ref(
        self,
        name: str,
        loc: SourceLoc,
        scope: _PlotScope,
    ) -> None:
        """Check that a referenced role is declared in the current plot.

        Args:
            name:  The role name.
            loc:   Source location of the reference.
            scope: The per-plot scope containing declared roles.
        """
        if name not in scope.roles:
            self._error(
                loc,
                f"Undeclared role: '{name}' in plot "
                f"'{scope.plot_name}'.",
                hint=(
                    f"Add 'ROLE {name}.' to plot "
                    f"'{scope.plot_name}'."
                ),
            )

    # == Phase 3: unused warnings ==============================================

    def _check_unused(self) -> None:
        """Warn about declared elements that were never referenced."""
        self._warn_unused(
            self._symbols.actions, self._used_actions, "action",
        )
        self._warn_unused(
            self._symbols.events, self._used_events, "event",
        )
        self._warn_unused(
            self._symbols.facts, self._used_facts, "fact",
        )
        self._warn_unused(
            self._symbols.playbooks, self._used_playbooks, "playbook",
        )

    def _warn_unused(
        self,
        declared: Dict[str, SourceLoc],
        used: Set[str],
        kind: str,
    ) -> None:
        """Emit a warning for each declared-but-unused name.

        Args:
            declared: The namespace of declared names.
            used:     The set of names that were referenced.
            kind:     Human-readable kind ("action", "event", etc.).
        """
        for name, loc in declared.items():
            if name not in used:
                self._warning(
                    loc,
                    f"Declared {kind} '{name}' is never used.",
                )

    # == Reporter helpers ======================================================

    def _error(
        self,
        loc: SourceLoc,
        message: str,
        hint: str = "",
    ) -> None:
        """Report an error at the given source location.

        Args:
            loc:     Source location of the issue.
            message: Human-readable error description.
            hint:    Optional suggestion for fixing the issue.
        """
        # Column in SourceLoc is 1-based, ErrorReporter expects 0-based
        self._reporter.error(
            line=loc.line,
            column=max(loc.column - 1, 0),
            length=1,
            message=message,
            hint=hint,
            filename=loc.filename,
        )

    def _warning(
        self,
        loc: SourceLoc,
        message: str,
        hint: str = "",
    ) -> None:
        """Report a warning at the given source location.

        Args:
            loc:     Source location of the issue.
            message: Human-readable warning description.
            hint:    Optional suggestion for addressing the issue.
        """
        self._reporter.warning(
            line=loc.line,
            column=max(loc.column - 1, 0),
            length=1,
            message=message,
            hint=hint,
            filename=loc.filename,
        )
