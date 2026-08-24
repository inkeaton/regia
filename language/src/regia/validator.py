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

from typing import Dict, List, Set

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
    AssignStmt, UnassignStmt, WorldDoStmt, RoleDoStmt,
    InlineTransitionStmt, StartSubplotStmt, PlotEndStmt, RoleMapping,
    # Plot
    OnEnter, OnExit,
    PlotIfBranch, PlotElseBranch, PlotWhenBlock, PlotWhenSubplotEndsBlock,
    PlotWhenRoleSignalsBlock,

    DuringBlock, PhaseDecl, RoleDecl, PlotDef,
    # Root
    Program,
)
from regia.errors import ErrorReporter


# == Implicit built-in events ==================================================
# These events are implicitly available to all Plots as part of the hierarchy
# protocol. They do not need to be declared with EVENT.

_IMPLICIT_EVENTS: frozenset[str] = frozenset([
    "parent_ended",
    "child_ended",
])


from dataclasses import dataclass

# == Symbol table ==============================================================
# Records where each name was declared and its arity, so we can report
# duplicate locations and verify arguments during usage.

@dataclass
class DeclInfo:
    """Information about a declared symbol.

    Attributes:
        loc:   Source location of the declaration.
        arity: Number of arguments the symbol accepts (for actions/facts).
    """
    loc: SourceLoc
    arity: int = 0


class _SymbolTable:
    """Tracks declared names, their source locations, and arities.

    Maintains separate namespaces for actions, events, facts,
    playbooks, and per-plot scopes for roles and phases.

    Attributes:
        actions:   Declared action names -> DeclInfo.
        events:    Declared event names -> DeclInfo.
        facts:     Declared fact names -> DeclInfo.
        playbooks: Declared playbook names -> DeclInfo.
    """

    def __init__(self) -> None:
        """Initialise empty symbol table."""
        self.actions:   Dict[str, DeclInfo] = {}
        self.events:    Dict[str, DeclInfo] = {}
        self.facts:     Dict[str, DeclInfo] = {}
        self.playbooks: Dict[str, DeclInfo] = {}


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
        self._action_aliases: Dict[str, str] = {}

        # Registry of all declared Plot names and their role sets.
        # Used to validate START SUBPLOT targets and MAPPING roles.
        # plot_name -> set of role names
        self._plot_roles: Dict[str, Set[str]] = {}

    # == Public API ============================================================

    def validate(self, program: Program) -> None:
        """Run all semantic checks on the program.

        Args:
            program: The root AST node to validate.
        """
        # Phase 0: build plot role registry (needed for SUBPLOT validation)
        for item in program.items:
            if isinstance(item, PlotDef):
                self._plot_roles[item.name] = {
                    r.name for r in item.roles
                }

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
            match item:
                case ImportDecl():
                    pass  # Import paths are resolved before validation
                case ActionDecl():
                    self._declare(
                        self._symbols.actions, "action", item.name, item.loc, len(item.params)
                    )
                    if item.alias:
                        self._declare(
                            self._symbols.actions, "action alias", item.alias, item.loc, len(item.params)
                        )
                        self._action_aliases[item.alias] = item.name
                        self._action_aliases[item.name] = item.alias
                case EventDecl():
                    self._declare(
                        self._symbols.events, "event", item.name, item.loc, 0
                    )
                case FactDecl():
                    self._declare(
                        self._symbols.facts, "fact", item.name, item.loc, len(item.params)
                    )
                case PlaybookDef():
                    self._declare(
                        self._symbols.playbooks, "playbook", item.name, item.loc, 0
                    )
                case PlotDef():
                    # Plots themselves don't need a namespace check for
                    # now. But we could add duplicate plot detection if needed.
                    pass

    def _declare(
        self,
        namespace: Dict[str, DeclInfo],
        kind: str,
        name: str,
        loc: SourceLoc,
        arity: int = 0,
    ) -> None:
        """Register a name in a namespace, reporting duplicates.

        Args:
            namespace: The dict to register into (e.g. symbols.actions).
            kind:      Human-readable kind ("action", "event", etc.).
            name:      The identifier being declared.
            loc:       Source location of this declaration.
            arity:     Number of arguments the symbol accepts.
        """
        if name in namespace:
            prev = namespace[name]
            self._error(
                loc,
                f"Duplicate {kind} declaration: '{name}'"
                f" (previously declared at line {prev.loc.line}).",
            )
            return

        namespace[name] = DeclInfo(loc, arity)

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
        match stmt:
            case DoStmt():
                self._check_action_ref(stmt.action, stmt.args, stmt.is_special, stmt.loc)
            case SignalStmt():
                self._check_event_ref(stmt.event, stmt.loc)

    # == Phase 2b: validate Plots ==============================================

    def _validate_plot(self, plot: PlotDef) -> None:
        """Validate a Plot definition.

        Checks:
            - Exactly one INITIAL phase.
            - No duplicate roles or phases within the plot.
            - DURING blocks reference declared phases.
            - At most one ON ENTER and one ON EXIT per DURING block.
            - All WHEN event references, action references, fact
              references, playbook references, and role references
              are declared.

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

        if len(block.on_enters) > 1:
            self._error(block.on_enters[1].loc, "Duplicate ON ENTER block.")
        if len(block.on_exits) > 1:
            self._error(block.on_exits[1].loc, "Duplicate ON EXIT block.")

        # Validate ON ENTER / ON EXIT stmts
        # InlineTransitionStmt and PlotEndStmt are NOT allowed in ON
        # ENTER/EXIT; those hooks execute during an already-in-progress
        # phase change and such statements would be ambiguous.
        for on_enter in block.on_enters:
            for stmt in on_enter.stmts:
                match stmt:
                    case InlineTransitionStmt():
                        self._error(
                            stmt.loc,
                            "TRANSITION TO cannot appear inside ON ENTER.",
                            hint="Move the transition to a WHEN block.",
                        )
                    case PlotEndStmt():
                        self._error(
                            stmt.loc,
                            "END PLOT cannot appear inside ON ENTER.",
                            hint="Move END PLOT to a WHEN block.",
                        )
                    case _:
                        self._validate_imperative_stmt(stmt, scope)
        for on_exit in block.on_exits:
            for stmt in on_exit.stmts:
                match stmt:
                    case InlineTransitionStmt():
                        self._error(
                            stmt.loc,
                            "TRANSITION TO cannot appear inside ON EXIT.",
                            hint="Move the transition to a WHEN block.",
                        )
                    case PlotEndStmt():
                        self._error(
                            stmt.loc,
                            "END PLOT cannot appear inside ON EXIT.",
                            hint="Move END PLOT to a WHEN block.",
                        )
                    case _:
                        self._validate_imperative_stmt(stmt, scope)

        # Validate WHEN blocks
        for when in block.when_blocks:
            self._validate_plot_when_block(when, scope, block.phase_name)

    def _validate_plot_when_block(
        self,
        when: PlotWhenBlock | PlotWhenSubplotEndsBlock | PlotWhenRoleSignalsBlock,
        scope: "_PlotScope",
        phase_name: str | None = None,
    ) -> None:
        """Validate a Plot WHEN block or WHEN SUBPLOT ENDS block.

        Also enforces that InlineTransitionStmt only appears in
        phase-specific DURING blocks (not DURING PLOT) and that
        it is always the last statement in any body or branch.

        Args:
            when:       The block to validate.
            scope:      The per-plot scope.
            phase_name: The phase this WHEN block lives in, or None
                        for DURING PLOT blocks.
        """
        match when:
            case PlotWhenBlock():
                self._check_event_ref(when.event, when.loc)
            case PlotWhenRoleSignalsBlock():
                self._check_event_ref(when.event, when.loc)
                if when.role_name not in scope.roles:
                    self._error(
                        when.loc,
                        f"WHEN ROLE ... SIGNALS ... references undeclared role: "
                        f"'{when.role_name}'.",
                        hint=f"Add a 'ROLE {when.role_name}.' declaration to plot '{scope.plot_name}'.",
                    )
            case _:
                if when.subplot_name not in self._plot_roles:
                    self._error(
                        when.loc,
                        f"WHEN SUBPLOT ENDS references undeclared plot: "
                        f"'{when.subplot_name}'.",
                        hint=f"Add a 'PLOT {when.subplot_name}. ...' definition.",
                    )

        # Validate prefix stmts and check position rules
        self._check_terminal_stmts(
            when.prefix_stmts, phase_name, context="WHEN prefix",
        )
        for stmt in when.prefix_stmts:
            self._validate_imperative_stmt(stmt, scope)

        for branch in when.branches:
            self._validate_condition(branch.condition)
            self._check_terminal_stmts(
                branch.stmts, phase_name, context="IF branch",
            )
            for stmt in branch.stmts:
                self._validate_imperative_stmt(stmt, scope)

        if when.else_branch is not None:
            self._check_terminal_stmts(
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
        match stmt:
            case AssignStmt():
                self._check_playbook_ref(stmt.playbook, stmt.loc)
                self._check_role_ref(stmt.role, stmt.loc, scope)
            case UnassignStmt():
                self._check_playbook_ref(stmt.playbook, stmt.loc)
                self._check_role_ref(stmt.role, stmt.loc, scope)
            case WorldDoStmt():
                self._check_action_ref(stmt.action, stmt.args, stmt.is_special, stmt.loc)
            case RoleDoStmt():
                self._check_role_ref(stmt.role, stmt.loc, scope)
                self._check_action_ref(stmt.action, stmt.args, stmt.is_special, stmt.loc)
            case InlineTransitionStmt():
                self._check_inline_transition(stmt, scope)
            case StartSubplotStmt():
                self._check_start_subplot(stmt, scope)
            case PlotEndStmt():
                pass  # No references to validate; placement is checked by _check_terminal_stmts

    # == Condition validation ===================================================

    def _validate_condition(self, cond: ConditionExpr) -> None:
        """Recursively validate a condition expression.

        Ensures all fact references in the condition are declared.

        Args:
            cond: The condition expression to validate.
        """
        match cond:
            case FactRef():
                self._check_fact_ref(cond.name, cond.args, cond.loc)
            case ConditionNot():
                self._validate_condition(cond.operand)
            case ConditionAnd() | ConditionOr():
                for op in cond.operands:
                    self._validate_condition(op)

    # == Reference checkers ====================================================
    # Each checker verifies that a referenced name exists in the
    # symbol table and marks it as used for the unused-warning pass.

    def _check_start_subplot(
        self,
        stmt: StartSubplotStmt,
        scope: _PlotScope,
    ) -> None:
        """Validate a START SUBPLOT statement.

        Rules:
            1. The target Plot must be declared in the program.
            2. Each source role in MAPPING must exist in the current plot.
            3. Each target role in MAPPING must exist in the spawned plot.
            4. Warn if no MAPPING is given but the spawned plot has roles.

        Args:
            stmt:  The StartSubplotStmt to validate.
            scope: The per-plot scope of the spawning Plot.
        """
        # Rule 1: target plot must exist
        if stmt.plot_name not in self._plot_roles:
            self._error(
                stmt.loc,
                f"START SUBPLOT references undeclared plot: "
                f"'{stmt.plot_name}'.",
                hint=f"Add a 'PLOT {stmt.plot_name}. ...' definition.",
            )
            return

        child_roles = self._plot_roles[stmt.plot_name]

        # Rule 4: warn if no mapping provided but child has roles
        if not stmt.mappings and child_roles:
            self._warning(
                stmt.loc,
                f"START SUBPLOT '{stmt.plot_name}' has no MAPPING clause, "
                f"but that plot declares {len(child_roles)} role(s).",
                hint="Add 'MAPPING SourceRole TO TargetRole, ...' to bind "
                     "agents from this plot to the child plot's roles.",
            )

        # Rules 2 & 3: validate each role mapping
        for mapping in stmt.mappings:
            # Source role must exist in the current (parent) plot
            if mapping.source_role not in scope.roles:
                self._error(
                    mapping.loc,
                    f"MAPPING source role '{mapping.source_role}' is not "
                    f"declared in plot '{scope.plot_name}'.",
                    hint=f"Add 'ROLE {mapping.source_role}.' to plot "
                         f"'{scope.plot_name}', or fix the role name.",
                )

            # Target role must exist in the spawned (child) plot
            if mapping.target_role not in child_roles:
                self._error(
                    mapping.loc,
                    f"MAPPING target role '{mapping.target_role}' is not "
                    f"declared in plot '{stmt.plot_name}'.",
                    hint=f"Add 'ROLE {mapping.target_role}.' to plot "
                         f"'{stmt.plot_name}', or fix the role name.",
                )

    def _check_inline_transition(
        self,
        stmt: InlineTransitionStmt,
        scope: "_PlotScope",
    ) -> None:
        """Validate an inline TRANSITION TO statement.

        Checks that the target phase is declared in the current plot.
        _check_terminal_stmts before this method is
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

    def _check_terminal_stmts(
        self,
        stmts: List,
        phase_name: str | None,
        context: str,
    ) -> None:
        """Enforce placement rules for terminal statements in a body list.

        Terminal statements are those that must appear last:
            - InlineTransitionStmt
            - PlotEndStmt

        Rules:
            1. InlineTransitionStmt may only appear in phase-specific
               DURING blocks (not in DURING PLOT).
            2. Both terminal statement types must be the last statement
               in the list. Any statement following one is an error.

        Args:
            stmts:      The list of imperative statements to check.
            phase_name: The containing phase (None for DURING PLOT).
            context:    Human-readable context for error messages.
        """
        for i, stmt in enumerate(stmts):
            is_terminal = isinstance(
                stmt, (InlineTransitionStmt, PlotEndStmt)
            )
            if not is_terminal:
                continue

            # InlineTransitionStmt: not allowed in DURING PLOT
            if isinstance(stmt, InlineTransitionStmt) and phase_name is None:
                self._error(
                    stmt.loc,
                    f"Inline TRANSITION TO cannot appear inside "
                    f"DURING PLOT ({context}).",
                    hint="Move this transition to a phase-specific "
                         "DURING block.",
                )
                continue

            # Both terminals: must be the last statement
            if i < len(stmts) - 1:
                self._error(
                    stmts[i + 1].loc,
                    f"Unreachable statement after "
                    f"{'TRANSITION TO' if isinstance(stmt, InlineTransitionStmt) else 'END PLOT'} "
                    f"in {context}.",
                    hint="This statement type must be the last in a body "
                         "or branch.",
                )
    # ==========================================================================

    def _check_action_ref(
        self,
        name: str,
        args: List,
        is_special: bool,
        loc: SourceLoc,
    ) -> None:
        """Check that a referenced action is declared.

        Special actions (TELL, BROADCAST, etc.) are built-in and
        always valid; they don't need a declaration.

        Args:
            name:       The action name.
            args:       The arguments provided to the action.
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

        decl = self._symbols.actions[name]
        if decl.arity != len(args):
            self._error(
                loc,
                f"Action '{name}' expects {decl.arity} argument(s), but {len(args)} were provided."
            )

        self._used_actions.add(name)
        if name in self._action_aliases:
            self._used_actions.add(self._action_aliases[name])

    def _check_event_ref(self, name: str, loc: SourceLoc) -> None:
        """Check that a referenced event is declared (or is a built-in).

        Implicit hierarchy events (parent_ended, child_ended) are
        always valid and do not need an EVENT declaration.

        Args:
            name: The event name.
            loc:  Source location of the reference.
        """
        # Implicit hierarchy events: always accepted, never need EVENT decl.
        if name in _IMPLICIT_EVENTS:
            return

        if name not in self._symbols.events:
            self._error(
                loc,
                f"Undeclared event: '{name}'.",
                hint=f"Add 'EVENT {name}.' at the top of the file.",
            )
            return

        self._used_events.add(name)

    def _check_fact_ref(self, name: str, args: List, loc: SourceLoc) -> None:
        """Check that a referenced fact is declared.

        Args:
            name: The fact name.
            args: The arguments provided to the fact.
            loc:  Source location of the reference.
        """
        if name not in self._symbols.facts:
            self._error(
                loc,
                f"Undeclared fact: '{name}'.",
                hint=f"Add 'FACT {name}.' at the top of the file.",
            )
            return

        decl = self._symbols.facts[name]
        if decl.arity != len(args):
            self._error(
                loc,
                f"Fact '{name}' expects {decl.arity} argument(s), but {len(args)} were provided."
            )

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
        declared: Dict[str, DeclInfo],
        used: Set[str],
        kind: str,
    ) -> None:
        """Emit a warning for each declared-but-unused name.

        Args:
            declared: The namespace of declared names (mapped to DeclInfo).
            used:     The set of names that were referenced.
            kind:     Human-readable kind ("action", "event", etc.).
        """
        for name, decl in declared.items():
            if name not in used:
                self._warning(
                    decl.loc,
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
