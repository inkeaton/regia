// src/types/ast.ts

// ==============================================================================
// BASE TYPES
// ==============================================================================

/**
 * The generic base for all AST nodes.
 * The `type` field is injected by the Python `ASTEncoder` and matches the
 * Python dataclass class name (e.g. "PhaseDecl", "PlotDef").
 */
export type ASTNode = {
    type: string;
};

/**
 * Source location attached to every AST node, for error reporting and
 * future click-to-navigate functionality.
 */
export type SourceLoc = {
    line:     number;
    column:   number;
    filename: string;
};

// ==============================================================================
// PREPROCESSOR TYPES
// ==============================================================================

/**
 * A doc comment attached to a node: `#@key: value`
 */
export type DocAnnotation = {
    type:  "DocAnnotation";
    key:   string;
    value: string;
    loc:   SourceLoc;
};

/**
 * An import statement: `IMPORT "path".`
 */
export type ImportDecl = ASTNode & {
    type: "ImportDecl";
    path: string;
    loc:  SourceLoc;
};

// ==============================================================================
// BASE ELEMENT DECLARATIONS
// Declared at the top of a Regia source file with ACTION, EVENT, FACT.
// ==============================================================================

/**
 * An action declaration: `ACTION greet_back.` or `ACTION give_item(item, target).`
 */
export type ActionDecl = ASTNode & {
    type:   "ActionDecl";
    name:   string;
    params: string[];
    docs?:  DocAnnotation[];
    loc:    SourceLoc;
};

/**
 * An event declaration: `EVENT fan_greets.` or `EVENT check SELF.`
 */
export type EventDecl = ASTNode & {
    type:   "EventDecl";
    name:   string;
    origin: "SELF" | "ENVIRONMENT" | null;
    docs?:  DocAnnotation[];
    loc:    SourceLoc;
};

/**
 * A fact declaration: `FACT happy.` or `FACT has_item(item).`
 */
export type FactDecl = ASTNode & {
    type:   "FactDecl";
    name:   string;
    params: string[];
    docs?:  DocAnnotation[];
    loc:    SourceLoc;
};

// ==============================================================================
// ARGUMENT TYPE
// ==============================================================================

/**
 * An argument in an action call or fact reference.
 * `value` is a string (identifier or string literal) or a number.
 */
export type Arg = {
    value:     string | number;
    is_string: boolean;
    loc:       SourceLoc;
};

// ==============================================================================
// CONDITION TYPES
// Boolean expressions over FACTs, used in IF guards and TRANSITION guards.
// Precedence: NOT > AND > OR. Parentheses override.
// ==============================================================================

/**
 * A reference to a fact: `happy`, `has_item(sword)`.
 */
export type FactRef = {
    type: "FactRef";
    name: string;
    args: Arg[];
    loc:  SourceLoc;
};

/**
 * Negation of a condition: `NOT happy`.
 */
export type ConditionNot = {
    type:    "ConditionNot";
    operand: ConditionExpr;
    loc:     SourceLoc;
};

/**
 * Conjunction: `happy AND has_item(sword)`.
 */
export type ConditionAnd = {
    type:     "ConditionAnd";
    operands: ConditionExpr[];
    loc:      SourceLoc;
};

/**
 * Disjunction: `happy OR neutral`.
 */
export type ConditionOr = {
    type:     "ConditionOr";
    operands: ConditionExpr[];
    loc:      SourceLoc;
};

/**
 * Union type for any condition expression.
 * Used in IF guards, TRANSITION guards, and recursively inside
 * ConditionNot, ConditionAnd, and ConditionOr.
 */
export type ConditionExpr = ConditionOr | ConditionAnd | ConditionNot | FactRef;

// ==============================================================================
// PLAYBOOK STATEMENTS
// Statements valid inside a PLAYBOOK WHEN block.
// ==============================================================================

/**
 * Self-directed action: `DO greet_back.` or `DO TELL(player, msg).`
 */
export type DoStmt = ASTNode & {
    type:       "DoStmt";
    action:     string;
    is_special: boolean;
    args:       Arg[];
    loc:        SourceLoc;
};

/**
 * Signal to the Director: `SIGNAL emergency.`
 */
export type SignalStmt = ASTNode & {
    type:  "SignalStmt";
    event: string;
    args:  Arg[];
    loc:   SourceLoc;
};

/** Union type for statements valid inside a Playbook WHEN block. */
export type PbStmt = DoStmt | SignalStmt;

// ==============================================================================
// TEMPER AND EFFECTS
// ==============================================================================

/**
 * A single temper or effect dimension: e.g. sympathy(0.8).
 */
export type TemperEntry = ASTNode & {
    type:  "TemperEntry";
    name:  string;
    value: number;
    loc:   SourceLoc;
};

/**
 * Full TEMPER annotation with optional EFFECTS.
 */
export type TemperSpec = ASTNode & {
    type:       "TemperSpec";
    dimensions: TemperEntry[];
    effects:    TemperEntry[];
    loc:        SourceLoc;
};

// ==============================================================================
// PLAYBOOK BRANCHING
// ==============================================================================

/**
 * Conditional branch in a Playbook WHEN block: `IF happy: DO greet.`
 */
export type PbIfBranch = ASTNode & {
    type:      "PbIfBranch";
    condition: ConditionExpr;
    stmts:     PbStmt[];
    loc:       SourceLoc;
};

/**
 * Fallback branch: `ELSE: DO ignore.`
 */
export type PbElseBranch = ASTNode & {
    type:  "PbElseBranch";
    stmts: PbStmt[];
    loc:   SourceLoc;
};

// ==============================================================================
// PLAYBOOK DEFINITION
// ==============================================================================

/**
 * A reactive plan triggered by a single event inside a Playbook.
 * `WHEN fan_greets PRIORITY 3: ...`
 */
export type PbWhenBlock = ASTNode & {
    type:         "PbWhenBlock";
    event:        string;
    priority:     number | null;
    temper:       TemperSpec | null;
    prefix_stmts: PbStmt[];
    branches:     PbIfBranch[];
    else_branch:  PbElseBranch | null;
    loc:          SourceLoc;
};

/**
 * A complete Playbook definition: `PLAYBOOK SingerInBackstage: ...`
 */
export type PlaybookDef = ASTNode & {
    type:        "PlaybookDef";
    name:        string;
    when_blocks: PbWhenBlock[];
    docs?:       DocAnnotation[];
    loc:         SourceLoc;
};

// ==============================================================================
// IMPERATIVE STATEMENTS
// Statements valid inside Plot WHEN blocks, ON ENTER, and ON EXIT.
// ==============================================================================

/**
 * Assign a Playbook to a Role: `ASSIGN SingerInBackstage TO Singer.`
 */
export type AssignStmt = ASTNode & {
    type:     "AssignStmt";
    playbook: string;
    role:     string;
    loc:      SourceLoc;
};

/**
 * Remove a Playbook from a Role: `UNASSIGN SingerInBackstage FROM Singer.`
 */
export type UnassignStmt = ASTNode & {
    type:     "UnassignStmt";
    playbook: string;
    role:     string;
    loc:      SourceLoc;
};

/**
 * Director-executed action: `WORLD DO trigger_alarm.`
 */
export type WorldDoStmt = ASTNode & {
    type:       "WorldDoStmt";
    action:     string;
    is_special: boolean;
    args:       Arg[];
    loc:        SourceLoc;
};

/**
 * Role-directed action: `Singer DO acknowledge.`
 */
export type RoleDoStmt = ASTNode & {
    type:       "RoleDoStmt";
    role:       string;
    action:     string;
    is_special: boolean;
    args:       Arg[];
    loc:        SourceLoc;
};

/**
 * Inline phase transition: `TRANSITION TO target.`
 */
export type InlineTransitionStmt = ASTNode & {
    type:         "InlineTransitionStmt";
    target_phase: string;
    loc:          SourceLoc;
};

/**
 * Maps a role from a parent plot to a child subplot.
 */
export type RoleMapping = {
    type:        "RoleMapping";
    source_role: string;
    target_role: string;
    loc:         SourceLoc;
};

/**
 * Spawns a new subplot: `START SUBPLOT PlotName MAPPING ...`
 */
export type StartSubplotStmt = ASTNode & {
    type:      "StartSubplotStmt";
    plot_name: string;
    mappings:  RoleMapping[];
    loc:       SourceLoc;
};

/**
 * Terminates the current plot: `END PLOT.`
 */
export type PlotEndStmt = ASTNode & {
    type: "PlotEndStmt";
    loc:  SourceLoc;
};

/** Union type for statements valid inside Plot WHEN blocks, ON ENTER, and ON EXIT. */
export type ImperativeStmt = AssignStmt | UnassignStmt | WorldDoStmt | RoleDoStmt | InlineTransitionStmt | StartSubplotStmt | PlotEndStmt;

// ==============================================================================
// PLOT BRANCHING
// ==============================================================================

/**
 * Conditional branch in a Plot WHEN block.
 */
export type PlotIfBranch = ASTNode & {
    type:      "PlotIfBranch";
    condition: ConditionExpr;
    stmts:     ImperativeStmt[];
    loc:       SourceLoc;
};

/**
 * Fallback branch in a Plot WHEN block.
 */
export type PlotElseBranch = ASTNode & {
    type:  "PlotElseBranch";
    stmts: ImperativeStmt[];
    loc:   SourceLoc;
};

// ==============================================================================
// PLOT CONTENT
// ==============================================================================

/**
 * A phase transition: `TRANSITION TO performing WHEN time_to_start.`
 * Optionally guarded: `TRANSITION TO done WHEN end IF all_complete.`
 */


/**
 * Phase entry hook: `ON ENTER: ...`
 * Executed when the Director transitions INTO this phase.
 */
export type OnEnter = ASTNode & {
    type:  "OnEnter";
    stmts: ImperativeStmt[];
    loc:   SourceLoc;
};

/**
 * Phase exit hook: `ON EXIT: ...`
 * Executed when the Director transitions OUT of this phase.
 */
export type OnExit = ASTNode & {
    type:  "OnExit";
    stmts: ImperativeStmt[];
    loc:   SourceLoc;
};

/**
 * A director-centric reactive plan inside a Plot.
 * `WHEN emergency PRIORITY 9: WORLD DO trigger_alarm.`
 */
export type PlotWhenBlock = ASTNode & {
    type:         "PlotWhenBlock";
    event:        string;
    priority:     number | null;
    temper:       TemperSpec | null;
    prefix_stmts: ImperativeStmt[];
    branches:     PlotIfBranch[];
    else_branch:  PlotElseBranch | null;
    loc:          SourceLoc;
};

/**
 * A DURING block inside a Plot.
 * `DURING backstage: ...` (phase-specific, phase_name = "backstage")
 * `DURING PLOT: ...`      (plot-wide,      phase_name = null)
 */
export type DuringBlock = ASTNode & {
    type:          "DuringBlock";
    phase_name:    string | null;
    on_enters:     OnEnter[];
    on_exits:      OnExit[];
    when_blocks:   PlotWhenBlock[];
    loc:           SourceLoc;
};

// ==============================================================================
// PLOT DECLARATION
// ==============================================================================

/**
 * A phase declaration: `PHASE backstage INITIAL.` or `PHASE performing.`
 */
export type PhaseDecl = ASTNode & {
    type:       "PhaseDecl";
    name:       string;
    is_initial: boolean;
    loc:        SourceLoc;
};

/**
 * A role declaration: `ROLE Singer.`
 */
export type RoleDecl = ASTNode & {
    type: "RoleDecl";
    name: string;
    loc:  SourceLoc;
};

/**
 * A complete Plot definition: `PLOT Concert. ...`
 */
export type PlotDef = ASTNode & {
    type:          "PlotDef";
    name:          string;
    phases:        PhaseDecl[];
    roles:         RoleDecl[];
    during_blocks: DuringBlock[];
    docs?:         DocAnnotation[];
    loc:           SourceLoc;
};

// ==============================================================================
// ROOT PROGRAM
// ==============================================================================

/**
 * Discriminated union of all valid top-level items in a Regia program.
 */
export type TopLevelItem =
    | ActionDecl
    | EventDecl
    | FactDecl
    | PlaybookDef
    | PlotDef
    | ImportDecl;

/**
 * The root AST node representing a complete Regia source file.
 * This is what the `/parse` endpoint returns.
 */
export type Program = ASTNode & {
    type:         "Program";
    doc_comments?: DocAnnotation[];
    items:        TopLevelItem[];
};