"""
AST node definitions for the Regia v0.2 compiler.

The parse tree (lark.Tree) is transformed into these dataclasses
by the ast_builder module. All subsequent passes (validation, emission)
work exclusively on these nodes, never on the raw parse tree.

Each node carries a SourceLoc (line, column) for error reporting.

The node hierarchy mirrors the three-layer language architecture:

    Program
    ├── ImportDecl                           (import declarations)
    ├── ActionDecl / EventDecl / FactDecl   (base elements)
    ├── PlaybookDef                          (reactive behaviour sets)
    │   └── PbWhenBlock
    │       ├── DoStmt / SignalStmt
    │       ├── PbIfBranch
    │       └── PbElseBranch
    └── PlotDef                              (narrative scenarios)
        ├── PhaseDecl / RoleDecl
        └── DuringBlock
            ├── OnEnter / OnExit
            └── PlotWhenBlock
                ├── AssignStmt / UnassignStmt
                ├── WorldDoStmt / RoleDoStmt
                ├── InlineTransitionStmt
                ├── PlotIfBranch
                └── PlotElseBranch

Doc annotations (#@ comments) are attached to top-level nodes
after AST building by the compiler's post-pass.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Union


# == Constants =================================================================
# Set of action names that map to special AgentSpeak primitives.
# These are reserved words in the grammar and cannot be used as
# regular action identifiers.

SPECIAL_ACTIONS: frozenset[str] = frozenset([
    "TELL", "BROADCAST", "ACHIEVE", "BELIEVE", "FORGET", "PRINT"
])



# == Source Location ===========================================================

@dataclass(frozen=True)
class SourceLoc:
    """Source position attached to every AST node for error reporting.

    Attributes:
        line:     1-based line number in the source file.
        column:   1-based column number in the source file.
        filename: Name of the source file (empty for single-file).
    """

    line:     int = 0
    column:   int = 0
    filename: str = ""


# Helper for creating a default SourceLoc in dataclass fields.
_NO_LOC = SourceLoc(0, 0)


# == Doc annotations ===========================================================
# Produced by the preprocessor from #@ comment lines and attached
# to AST nodes by the compiler's post-pass. These are NOT part of
# the grammar; they are extracted before parsing.

@dataclass
class DocAnnotation:
    """A single #@ doc-comment annotation.

    Attached to top-level AST nodes (ActionDecl, PlaybookDef, PlotDef,
    etc.) after AST building by the compiler's annotation post-pass.

    Attributes:
        key:   The annotation key (free-form identifier).
        value: The annotation value (freeform text).
        line:  The 1-based source line of the annotation.
    """

    key:   str
    value: str
    line:  int = 0


# == Import declarations =======================================================
# ImportDecl nodes are produced by the AST builder from IMPORT
# statements in the grammar. They appear as the first items
# in Program.items (in source order).

@dataclass
class ImportDecl:
    """An import declaration: IMPORT \"path/to/file.regia\".

    The compiler resolves these before validation. After resolution,
    the imported definitions are merged into the Program and these
    nodes are kept for informational/tooling purposes.

    Attributes:
        path: The raw import path string (as written in source).
        loc:  Source location of the IMPORT keyword.
    """

    path: str
    loc:  SourceLoc = _NO_LOC


# == Enums =====================================================================

class EventOrigin(Enum):
    """Origin of an event declaration.

    Attributes:
        SELF:        Event generated internally by the agent.
        ENVIRONMENT: Event perceived from the game world (default).
    """

    SELF        = "SELF"
    ENVIRONMENT = "ENVIRONMENT"


# == Shared Primitives =========================================================

@dataclass(frozen=True)
class Arg:
    """An argument in an action call or fact reference.

    The value is either a string (for identifier arguments like
    'sword', 'player') or an int (for numeric arguments like 7).
    The type of `value` encodes whether it came from an ID or
    NUMBER token in the source.

    Attributes:
        value:     The argument value (string identifier, string literal, or integer).
        is_string: True if the value was parsed from a STRING literal.
        loc:       Source location.
    """

    value:     Union[str, int]
    is_string: bool = False
    loc:       SourceLoc = _NO_LOC


# == Base Element Declarations =================================================
# ACTION, EVENT, FACT: the shared vocabulary that Playbooks and
# Plots reference. Declared at the top of a Regia source file.

@dataclass
class ActionDecl:
    """An action declaration: ACTION greet_back. or ACTION give(item, target).

    Attributes:
        name:   The action identifier.
        params: Parameter slot names (empty list if no parameters).
        loc:    Source location of the declaration.
        docs:   Doc annotations attached to this declaration.
    """

    name:   str
    params: List[str]           = field(default_factory=list)
    loc:    SourceLoc           = _NO_LOC
    docs:   List[DocAnnotation] = field(default_factory=list)


@dataclass
class EventDecl:
    """An event declaration: EVENT fan_greets. or EVENT check SELF.

    Attributes:
        name:   The event identifier.
        origin: Optional origin qualifier (SELF or ENVIRONMENT).
                None means the default (ENVIRONMENT).
        loc:    Source location of the declaration.
        docs:   Doc annotations attached to this declaration.
    """

    name:   str
    origin: Optional[EventOrigin] = None
    loc:    SourceLoc              = _NO_LOC
    docs:   List[DocAnnotation]   = field(default_factory=list)


@dataclass
class FactDecl:
    """A fact declaration: FACT happy. or FACT has_item(item).

    Attributes:
        name:   The fact identifier.
        params: Parameter slot names (empty list if no parameters).
        loc:    Source location of the declaration.
        docs:   Doc annotations attached to this declaration.
    """

    name:   str
    params: List[str]           = field(default_factory=list)
    loc:    SourceLoc           = _NO_LOC
    docs:   List[DocAnnotation] = field(default_factory=list)


# == Conditions ================================================================
# Boolean expressions over facts, used in IF guards and TRANSITION
# guards. Precedence: NOT > AND > OR. Parentheses override.
#
# The builder collapses single-child wrappers, so a simple check
# like "IF happy:" becomes just a FactRef, not a nested
# ConditionOr > ConditionAnd > FactRef chain.

@dataclass
class FactRef:
    """A reference to a fact, optionally with arguments.

    Examples: happy, has_item(sword), at_location(room, 3)

    Attributes:
        name: The fact identifier.
        args: Arguments (empty list if bare fact).
        loc:  Source location of the fact name.
    """

    name: str
    args: List[Arg]   = field(default_factory=list)
    loc:  SourceLoc   = _NO_LOC


@dataclass
class ConditionNot:
    """Negation of a condition: NOT happy, NOT (x AND y).

    Attributes:
        operand: The negated condition expression.
        loc:     Source location of the NOT keyword.
    """

    operand: ConditionExpr
    loc:     SourceLoc = _NO_LOC


@dataclass
class ConditionAnd:
    """Conjunction of condition expressions: happy AND healthy.

    Only created when there are 2+ operands; a single operand
    is collapsed to its inner expression by the AST builder.

    Attributes:
        operands: The conjuncts (always len >= 2).
        loc:      Source location of the first operand.
    """

    operands: List[ConditionExpr]
    loc:      SourceLoc = _NO_LOC


@dataclass
class ConditionOr:
    """Disjunction of condition expressions: happy OR neutral.

    Only created when there are 2+ operands; a single operand
    is collapsed to its inner expression by the AST builder.

    Attributes:
        operands: The disjuncts (always len >= 2).
        loc:      Source location of the first operand.
    """

    operands: List[ConditionExpr]
    loc:      SourceLoc = _NO_LOC


# Union type for any condition expression.
# Used in IF guards, TRANSITION guards, and recursively inside
# ConditionNot, ConditionAnd, ConditionOr.
ConditionExpr = Union[ConditionOr, ConditionAnd, ConditionNot, FactRef]


# == Playbook Statements =======================================================
# Statements used inside PLAYBOOK WHEN blocks. These are
# self-directed: the agent executes them on itself.

@dataclass
class DoStmt:
    """Self-directed action: DO greet_back. or DO TELL(player, msg).

    Attributes:
        action:     The action name (e.g. 'greet_back', 'TELL').
        is_special: True if the action is a special AgentSpeak
                    primitive (TELL, BROADCAST, ACHIEVE, BELIEVE,
                    FORGET).
        args:       Arguments to the action.
        loc:        Source location of the DO keyword.
    """

    action:     str
    is_special: bool           = False
    args:       List[Arg]      = field(default_factory=list)
    loc:        SourceLoc      = _NO_LOC


@dataclass
class SignalStmt:
    """Signal the Director: SIGNAL emergency. or SIGNAL alert(loc).

    A signal is a message from an agent (inside a Playbook) to
    the Director that manages the Plot. It allows Playbooks to
    communicate events upward without knowing the Plot structure.

    Attributes:
        event: The signal event name.
        args:  Arguments to the signal.
        loc:   Source location of the SIGNAL keyword.
    """

    event: str
    args:  List[Arg]      = field(default_factory=list)
    loc:   SourceLoc      = _NO_LOC


# Type alias for statements valid inside a PLAYBOOK WHEN block.
PbStmt = Union[DoStmt, SignalStmt]


# == Playbook Branching ========================================================

@dataclass
class PbIfBranch:
    """A conditional branch in a Playbook WHEN block: IF happy: DO greet.

    Attributes:
        condition: The boolean guard expression.
        stmts:     Statements to execute if the condition is true.
        loc:       Source location of the IF keyword.
    """

    condition: ConditionExpr
    stmts:     List[PbStmt]
    loc:       SourceLoc = _NO_LOC


@dataclass
class PbElseBranch:
    """The fallback branch in a Playbook WHEN block: ELSE: DO ignore.

    Attributes:
        stmts: Statements to execute if no IF branch matched.
        loc:   Source location of the ELSE keyword.
    """

    stmts: List[PbStmt]
    loc:   SourceLoc = _NO_LOC


# == Temper (VEsNA) ============================================================

@dataclass
class TemperEntry:
    """A single temper or effect dimension: e.g. sympathy(0.8).

    Attributes:
        name:  The dimension identifier (e.g. sympathy, fear).
        value: The numeric value (float).
    """

    name:  str
    value: float


@dataclass
class TemperSpec:
    """Full TEMPER annotation with optional EFFECTS.

    Attributes:
        dimensions: The temper dimensions list.
        effects:    The effects dimensions list (may be empty).
    """

    dimensions: List[TemperEntry]
    effects:    List[TemperEntry] = field(default_factory=list)


# == Playbook ==================================================================

@dataclass
class PbWhenBlock:
    """A reactive plan inside a Playbook: WHEN event PRIORITY n: body.

    The body is split into three parts by the AST builder:
      1. prefix_stmts: unconditional actions executed before branches
      2. branches:     IF condition: ... blocks
      3. else_branch:  ELSE: ... fallback (optional)

    In the emitter, prefix_stmts are prepended to every branch's
    plan body.

    Attributes:
        event:        The triggering event name.
        priority:     Numeric priority (None means default = 0).
        temper:       Optional temper/effects annotation (VEsNA).
        prefix_stmts: Unconditional statements before any IF.
        branches:     Conditional IF branches.
        else_branch:  Optional ELSE fallback.
        loc:          Source location of the WHEN keyword.
    """

    event:        str
    priority:     Optional[int]              = None
    temper:       Optional[TemperSpec]        = None
    prefix_stmts: List[PbStmt]               = field(default_factory=list)
    branches:     List[PbIfBranch]            = field(default_factory=list)
    else_branch:  Optional[PbElseBranch]      = None
    loc:          SourceLoc                   = _NO_LOC


@dataclass
class PlaybookDef:
    """A Playbook definition: PLAYBOOK SingerInBackstage: ...

    A Playbook is a reusable, context-free bundle of reactive
    plans. It contains only self-directed actions (DO) and
    signals to the Director (SIGNAL).

    Attributes:
        name:        The Playbook identifier.
        when_blocks: The reactive plans inside this Playbook.
        loc:         Source location of the PLAYBOOK keyword.
        docs:        Doc annotations attached to this Playbook.
    """

    name:        str
    when_blocks: List[PbWhenBlock]   = field(default_factory=list)
    loc:         SourceLoc           = _NO_LOC
    docs:        List[DocAnnotation] = field(default_factory=list)


# == Imperative Statements =====================================================
# Statements used inside Plot WHEN blocks, ON ENTER, and ON EXIT.
# These are director-level commands.

@dataclass
class InlineTransitionStmt:
    """An inline phase transition inside a WHEN body: TRANSITION TO phase.

    Must always be the final statement in its containing body or branch.
    Forbidden in DURING PLOT blocks (there is no single current phase to leave).
    Forbidden in ON ENTER / ON EXIT hooks.

    Attributes:
        target_phase: The destination phase name.
        loc:          Source location of the TRANSITION keyword.
    """

    target_phase: str
    loc:          SourceLoc = _NO_LOC


@dataclass
class AssignStmt:
    """Playbook assignment: ASSIGN SingerInBackstage TO Singer.

    Tells the Director to inject a Playbook into a Role's agents.
    At the AgentSpeak level, this toggles a playbook_active(...)
    belief on the bound agents (static gating).

    Attributes:
        playbook: The Playbook identifier to assign.
        role:     The Role to assign it to.
        loc:      Source location of the ASSIGN keyword.
    """

    playbook: str
    role:     str
    loc:      SourceLoc = _NO_LOC


@dataclass
class UnassignStmt:
    """Playbook removal: UNASSIGN SingerInBackstage FROM Singer.

    Tells the Director to remove a Playbook from a Role's agents.

    Attributes:
        playbook: The Playbook identifier to remove.
        role:     The Role to remove it from.
        loc:      Source location of the UNASSIGN keyword.
    """

    playbook: str
    role:     str
    loc:      SourceLoc = _NO_LOC


@dataclass
class WorldDoStmt:
    """Director-executed action: WORLD DO trigger_alarm.

    An action executed by the Director itself (no agent owner).
    Maps to an internal action or environment command in AgentSpeak.

    Attributes:
        action:     The action name.
        is_special: True for special primitives (TELL, BROADCAST, etc).
        args:       Arguments to the action.
        loc:        Source location of the WORLD keyword.
    """

    action:     str
    is_special: bool           = False
    args:       List[Arg]      = field(default_factory=list)
    loc:        SourceLoc      = _NO_LOC


@dataclass
class RoleDoStmt:
    """Role-directed action: Singer DO acknowledge.

    The Director sends a one-off command to a Role's bound agents.
    Maps to .send(agent, achieve, action) in AgentSpeak.

    Attributes:
        role:       The Role whose agents should execute the action.
        action:     The action name.
        is_special: True for special primitives (TELL, BROADCAST, etc).
        args:       Arguments to the action.
        loc:        Source location of the Role identifier.
    """

    role:       str
    action:     str
    is_special: bool           = False
    args:       List[Arg]      = field(default_factory=list)
    loc:        SourceLoc      = _NO_LOC


@dataclass
class RoleMapping:
    """A single role binding in a START SUBPLOT mapping clause.

    Maps a role from the parent Plot to a role in the child Plot.

    Attributes:
        source_role: The role name in the parent (spawning) Plot.
        target_role: The role name in the child (spawned) Plot.
        loc:         Source location of the source role token.
    """

    source_role: str
    target_role: str
    loc:         SourceLoc = _NO_LOC


@dataclass
class StartSubplotStmt:
    """Start a child Plot: START SUBPLOT DungeonCrawl MAPPING Hero TO Adventurer.

    Spawns a new Director agent for the named Plot and passes it role
    bindings derived from the parent's current role-agent registry.

    The MAPPING clause is optional for roleless Plots; the compiler emits
    a warning if omitted when the target Plot declares roles.

    Attributes:
        plot_name: The Plot type to instantiate.
        mappings:  Role binding list (may be empty for roleless Plots).
        loc:       Source location of the START keyword.
    """

    plot_name: str
    mappings:  List[RoleMapping]
    loc:       SourceLoc = _NO_LOC


@dataclass
class PlotEndStmt:
    """Terminate the current Plot: END PLOT.

    Notifies all child plots (parent_ended event) and the parent plot
    (child_ended event), then kills the Director agent.

    Must be the last statement in its WHEN block or branch.
    Forbidden inside ON ENTER / ON EXIT hooks.

    Attributes:
        loc: Source location of the END keyword.
    """

    loc: SourceLoc = _NO_LOC


# Type alias for statements valid inside Plot WHEN blocks,
# ON ENTER, and ON EXIT.
# InlineTransitionStmt and PlotEndStmt must be the last statement
# in their block; StartSubplotStmt is unrestricted.
# PlotEndStmt is forbidden in ON ENTER / ON EXIT (validator enforces this).
ImperativeStmt = Union[
    AssignStmt, UnassignStmt, WorldDoStmt, RoleDoStmt,
    InlineTransitionStmt, StartSubplotStmt, PlotEndStmt
]


# == Plot Branching ============================================================

@dataclass
class PlotIfBranch:
    """A conditional branch in a Plot WHEN block.

    Attributes:
        condition: The boolean guard expression.
        stmts:     Imperative statements to execute.
        loc:       Source location of the IF keyword.
    """

    condition: ConditionExpr
    stmts:     List[ImperativeStmt]
    loc:       SourceLoc = _NO_LOC


@dataclass
class PlotElseBranch:
    """The fallback branch in a Plot WHEN block.

    Attributes:
        stmts: Imperative statements to execute.
        loc:   Source location of the ELSE keyword.
    """

    stmts: List[ImperativeStmt]
    loc:   SourceLoc = _NO_LOC


# == Plot Content ==============================================================


@dataclass
class OnEnter:
    """Phase entry hook: ON ENTER: imperative_stmts.

    Executed when the Director transitions INTO this phase,
    after the previous phase's ON EXIT has run.

    Attributes:
        stmts: Imperative statements to execute on entry.
        loc:   Source location of the ON keyword.
    """

    stmts: List[ImperativeStmt]
    loc:   SourceLoc = _NO_LOC


@dataclass
class OnExit:
    """Phase exit hook: ON EXIT: imperative_stmts.

    Executed when the Director transitions OUT of this phase,
    before the new phase's ON ENTER runs.

    Attributes:
        stmts: Imperative statements to execute on exit.
        loc:   Source location of the ON keyword.
    """

    stmts: List[ImperativeStmt]
    loc:   SourceLoc = _NO_LOC


@dataclass
class PlotWhenBlock:
    """A director-centric reactive plan inside a Plot.

    Same structure as PbWhenBlock but uses imperative statements
    (WORLD DO, Role DO, ASSIGN, UNASSIGN) instead of self-directed
    DO/SIGNAL.

    Attributes:
        event:        The triggering event name.
        priority:     Numeric priority (None means default = 0).
        prefix_stmts: Unconditional statements before any IF.
        branches:     Conditional IF branches.
        else_branch:  Optional ELSE fallback.
        loc:          Source location of the WHEN keyword.
    """

    event:        str
    priority:     Optional[int]                = None
    prefix_stmts: List[ImperativeStmt]         = field(default_factory=list)
    branches:     List[PlotIfBranch]            = field(default_factory=list)
    else_branch:  Optional[PlotElseBranch]      = None
    loc:          SourceLoc                     = _NO_LOC


# == During Blocks =============================================================

@dataclass
class DuringBlock:
    """A DURING block inside a Plot.

    DURING backstage:  (phase-specific, phase_name = 'backstage')
    DURING PLOT:       (plot-wide,      phase_name = None)

    Contains lifecycle hooks (ON ENTER/EXIT) and director-centric WHEN blocks.
    Phase transitions are expressed as inline TRANSITION TO statements inside
    WHEN block bodies, not as separate top-level items here.

    Note: the validator enforces that at most one ON ENTER and
    one ON EXIT exist per DURING block. The AST stores them as
    lists to let the builder remain mechanical and defer
    validation to the semantic pass.

    Attributes:
        phase_name:  Phase name (None for DURING PLOT = all phases).
        on_enters:   ON ENTER hooks (validator checks len <= 1).
        on_exits:    ON EXIT hooks (validator checks len <= 1).
        when_blocks: Director-centric reactive plans.
        loc:         Source location of the DURING keyword.
    """

    phase_name:  Optional[str]
    on_enters:   List[OnEnter]           = field(default_factory=list)
    on_exits:    List[OnExit]            = field(default_factory=list)
    when_blocks: List[PlotWhenBlock]     = field(default_factory=list)
    loc:         SourceLoc               = _NO_LOC


# == Plot ======================================================================

@dataclass
class PhaseDecl:
    """A phase declaration: PHASE backstage INITIAL. or PHASE performing.

    Attributes:
        name:       The phase identifier.
        is_initial: True if this is the starting phase.
        loc:        Source location of the PHASE keyword.
    """

    name:       str
    is_initial: bool      = False
    loc:        SourceLoc = _NO_LOC


@dataclass
class RoleDecl:
    """A role declaration: ROLE Singer.

    A Role is a template that gets bound to specific agent
    instances at runtime. The same Role can appear in multiple
    Plots.

    Attributes:
        name: The role identifier.
        loc:  Source location of the ROLE keyword.
    """

    name: str
    loc:  SourceLoc = _NO_LOC


@dataclass
class PlotDef:
    """A Plot definition: PLOT Concert. phases roles during_blocks.

    A Plot is a narrative scenario written from the Director's
    perspective. Each active Plot spawns its own Director agent
    at runtime.

    Attributes:
        name:          The Plot identifier.
        phases:        Phase declarations (at least one must be INITIAL).
        roles:         Role declarations.
        during_blocks: DURING phase/PLOT blocks with behaviour.
        loc:           Source location of the PLOT keyword.
        docs:          Doc annotations attached to this Plot.
    """

    name:          str
    phases:        List[PhaseDecl]     = field(default_factory=list)
    roles:         List[RoleDecl]      = field(default_factory=list)
    during_blocks: List[DuringBlock]   = field(default_factory=list)
    loc:           SourceLoc           = _NO_LOC
    docs:          List[DocAnnotation] = field(default_factory=list)


# == Root ======================================================================

# Type alias for any top-level item in a program.
TopLevelItem = Union[ImportDecl, ActionDecl, EventDecl, FactDecl, PlaybookDef, PlotDef]


@dataclass
class Program:
    """Root AST node representing a complete Regia source file.

    After the compiler's annotation post-pass, doc_comments contains
    the file-level #@ annotations (those that precede any top-level
    item). Annotations attached to specific items are stored on the
    items themselves via their own `docs` lists.

    Attributes:
        items:        All top-level declarations and definitions,
                      in source order. ImportDecl nodes appear first.
        doc_comments: File-level #@ annotations (preprocessor output).
    """

    items:        List[TopLevelItem]  = field(default_factory=list)
    doc_comments: List[DocAnnotation] = field(default_factory=list)
