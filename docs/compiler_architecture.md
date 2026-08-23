# Regia Compiler Architecture

> **Scope**: This document explains the internal architecture of the Regia compiler. It traces the data flow from raw `.regia` source code to compiled AgentSpeak (`.asl`) files, detailing the goals, key patterns, data structures, and concrete implementation decisions of each compilation phase.

---

## 1. Compiler Pipeline Overview

The Regia compiler (located in `language/src/regia/`) operates as a classic multi-pass transpiler. It converts domain-specific Regia narratives into executable, multi-agent AgentSpeak logic.

The transpilation pipeline consists of six strict, sequential phases:

```
  Raw .regia source
        │
        ▼
  ┌─────────────┐
  │  Phase 0    │  Preprocessor  (preprocessor.py)
  │  Preprocess │  Extracts doc comments, strips IMPORT lines,
  │             │  resolves the import dependency graph.
  └──────┬──────┘
         │  SourceAnnotations (clean_source, doc_comments, import_paths)
         ▼
  ┌─────────────┐
  │  Phase 1    │  Parser  (parser.py + grammars/regia.lark)
  │  Parse      │  Lark LALR(1) grammar produces a concrete syntax tree.
  │             │
  └──────┬──────┘
         │  lark.Tree (untyped parse tree)
         ▼
  ┌─────────────┐
  │  Phase 2    │  AST Builder  (ast_builder.py)
  │  Build AST  │  Lark Transformer converts the parse tree into
  │             │  strongly-typed Python dataclass AST nodes.
  └──────┬──────┘
         │  Program (root AST node)
         ▼
  ┌─────────────┐
  │  Phase 3    │  Annotation  (compiler.py internal pass)
  │  Annotate   │  Attaches #@ doc comments to their AST nodes
  │             │  by source-line proximity.
  └──────┬──────┘
         │  Program (with docs attached)
         ▼
  ┌─────────────┐
  │  Phase 4    │  Validator  (validator.py)
  │  Validate   │  Semantic checks: name resolution, arity, structural
  │             │  constraints. Emits errors and unused warnings.
  └──────┬──────┘
         │  Validated Program (or failure)
         ▼
  ┌─────────────┐
  │  Phase 5    │  Emitter  (emitter.py)
  │  Emit       │  Multi-pass generation of .asl files.
  │             │  One playbook file + one director file + one role file
  │             │  per Plot-Role pair.
  └──────┬──────┘
         │  Dict[str, str] (filename -> AgentSpeak source)
         ▼
  Written to disk by CLI, or returned as JSON by the server.
```

Each phase runs only if the previous produced zero errors. This fail-fast design prevents misleading cascading errors downstream.

---

## 2. CLI Entrypoint (`cli.py`)

The compiler is invoked via the command-line interface defined in `cli.py`, built on [Click](https://click.palletsprojects.com/).

### Commands

| Command | Description |
|---|---|
| `regia compile <file.regia> -o <dir>` | Full pipeline: parse → validate → emit → write files |
| `regia check <file.regia>` | Parse and validate only, no file output |
| `regia parse <file.regia>` | Parse and pretty-print the AST (development aid) |

All commands accept `--quiet` (suppress warnings) and `--verbose` (extra stage output) flags, stored in a `CliState` dataclass on the Click context.

### Output Formatting

Diagnostics are rendered by `_print_diagnostics()`, which sorts all messages by `(filename, line)` and prints a coloured, structured block per message:

```
============================================================
 ERROR  my_file.regia:12, col 4
 Undeclared action: 'do_thing'.
 Hint: Add 'ACTION do_thing.' at the top of the file.

    DO do_thing.
    ^^^^^^^^^^^
============================================================
```

The caret (`^^^`) is computed from the message's `column` and `length` fields. The CLI exits with code `1` on any error via `sys.exit(1)` inside `_print_summary()`.

---

## 3. Pipeline Orchestrator (`compiler.py`)

`compiler.py` contains no grammar or emission logic — it is pure pipeline wiring. It exposes three public functions and owns the `CompileResult` type.

### `CompileResult`

The unified return type for all pipeline entry points:

```python
@dataclass
class CompileResult:
    success:       bool              # True if no errors
    outputs:       Dict[str, str]   # filename -> AgentSpeak source
    error_count:   int
    warning_count: int
    messages:      List[CompilerMessage]
    ast:           Optional[Program] # Attached for the editor server
```

### Entry Points

**`compile_source(source, filename, emit)`** — Compiles a raw string. This is used by `server.py` (the editor backend). Because there is no filesystem context, `IMPORT` statements inside the string are parsed but *not resolved*. Runs all six phases in sequence.

**`compile_file(filepath, emit)`** — Compiles a single `.regia` file with full `IMPORT` resolution. It first calls `resolve_imports()` (Preprocessor) to discover the full dependency graph. If the file has no imports, it delegates directly to `compile_source()` for efficiency. Otherwise it delegates to `compile_files()`.

**`compile_files(filepaths, emit)`** — Compiles multiple files. Each file goes through Phases 0–3 independently (to collect all errors from every file). The resulting `Program` objects are then **merged** into a single root `Program` before Phases 4–5 (Validation and Emission). This merge is a simple `list.extend()` on `Program.items` and `Program.doc_comments`.

### Doc Comment Attachment (Phase 3)

After AST building, `_attach_doc_comments()` performs a proximity match between `DocAnnotation` objects (from the Preprocessor) and the top-level AST nodes they precede. The algorithm:

1. Builds a sorted list of `(line_number, ast_node)` pairs for all annotatable node types: `ActionDecl`, `EventDecl`, `FactDecl`, `PlaybookDef`, `PlotDef`.
2. Iterates through annotations in order. For each annotation, finds the first AST node whose source line is *after* the annotation's line.
3. Appends the annotation to that node's `.docs` list.
4. Annotations with no subsequent node are stored on the root `Program.doc_comments` as file-level annotations.

---

## 4. Phase 0: Preprocessing (`preprocessor.py`)

The Preprocessor runs before Lark parsing. It scans the source text line by line and handles two constructs that the grammar does not need to see.

### 4.1 Doc-Comment Extraction

Doc comments use the `#@key: value` syntax. The preprocessor matches each line against two patterns:

- **`_DOC_RE`**: `#@key: value` — starts a new annotation.
- **`_DOC_CONT_RE`**: `#- continuation text` — appends to the most recent annotation's value on a new line.

Matched lines are replaced with empty strings (preserving line numbers) and accumulated as `DocAnnotation` objects. A `last_doc_idx` pointer tracks the most recent annotation for continuations. Any non-blank, non-doc line resets the pointer, preventing accidental continuations.

### 4.2 IMPORT Statement Stripping

`IMPORT "path/to/file.regia".` lines are matched by `_IMPORT_RE` and replaced with empty strings. The raw path string is extracted into `SourceAnnotations.import_paths`.

### 4.3 Import Graph Resolution

`resolve_imports(entry_file, reporter_cb)` performs a **Breadth-First Search** over the import graph starting from the entry file:

1. Reads and preprocesses each file to extract its own `import_paths`.
2. Resolves relative paths against the importing file's directory.
3. Detects **circular imports** using a `imported_from` dictionary that maps each visited path to the file that imported it.
4. Detects **missing files** with a `.exists()` check.
5. Returns an ordered `List[Path]` of unique absolute file paths (each file appears at most once, regardless of how many files import it).

### 4.4 Output Structure

`preprocess()` returns a `SourceAnnotations` dataclass:

```python
@dataclass
class SourceAnnotations:
    clean_source: str              # Source with #@ and IMPORT lines blanked
    doc_comments: List[DocAnnotation]
    import_paths: List[str]        # Raw (unresolved) import path strings
```

The `clean_source` is the only thing the Lark parser ever sees.

---

## 5. Phase 1: Lexing & Parsing (`parser.py` + `grammars/regia.lark`)

### 5.1 The Parser Module

`parser.py` is intentionally minimal. It loads the Lark grammar from `grammars/regia.lark` once at **import time**, compiling it into an LALR table (fast, no external tools). It exposes a single `parse(source: str) -> Tree` function.

The Lark parser is configured with `propagate_positions=True`, which attaches `line` and `column` attributes to every `Tree` node. This is the source of all position information used in later error messages.

Syntax errors are re-raised as Lark's `UnexpectedToken` or `UnexpectedCharacters` exceptions. The caller (`compiler.py`) catches these and routes them through `syntax_errors.py`.

### 5.2 Syntax Error Humanisation (`syntax_errors.py`)

Raw Lark exceptions contain technical terminal names that are not user-friendly. `report_syntax_error()` translates them:

- **`UnexpectedToken`**: Extracts the offending token text, its position, and the set of expected terminals. The expected set is mapped through `_FRIENDLY` (a dict of terminal name → plain-English description) and formatted into a comma-separated list.
- **`UnexpectedCharacters`**: Simpler — just records the position with a generic "unrecognised character" message.

Both error types are added to the `ErrorReporter` via its `error()` method.

### 5.3 Grammar Design (`regia.lark`)

The grammar is LALR(1) and uses several Lark features to keep the parse tree clean:

- **`?` rule inlining**: Rules like `?element_decl`, `?pb_stmt`, `?during_content`, and `?imperative_stmt` are prefixed with `?`. When such a rule matches exactly one alternative, Lark removes the wrapper node and promotes the child directly. This means `program.items` will contain `action_decl`, `playbook_def`, etc. directly, not wrapped in `element_decl` nodes.
- **`->` aliases**: Rules with multiple alternatives (e.g., `phase_decl`) use `-> alias_name` to give each alternative a distinct name. The AST Builder can then have a separate method for `initial_phase_decl` vs. `phase_decl`, avoiding the need to inspect child content.
- **Anonymous terminals**: Keywords like `"WHEN"`, `"DO"`, `"ASSIGN"` are written as string literals in the grammar. Lark treats these as anonymous terminals and **automatically filters them** from the tree, leaving only the semantically meaningful tokens.
- **Named terminals**: A small set of tokens that carry semantic value — `ID`, `NUMBER`, `FLOAT`, `STRING`, `SELF`, `ENVIRONMENT`, `TELL`, `BROADCAST`, `ACHIEVE`, `BELIEVE`, `FORGET`, `PRINT`, `WAIT` — are defined as named terminals. These are kept in the tree as `Token` objects and receive higher lexer priority than `ID`, making them effectively reserved words.
- **`ID` terminal**: Supports optional leading dots (`.print`) and dot-namespaced names (`vesna.transition_to`), defined as the regex `/\.?[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)*/`.

### 5.4 Condition Precedence

Boolean conditions are expressed in three nested grammar rules that encode precedence directly:

```lark
condition:      condition_and ("OR"  condition_and)*   // lowest precedence
condition_and:  condition_atom ("AND" condition_atom)* // medium
?condition_atom: "NOT" condition_atom -> condition_not  // highest (recursive)
               | fact_ref
               | "(" condition ")" -> condition_group
```

This structure ensures `NOT` binds tighter than `AND`, which binds tighter than `OR`, without needing an explicit precedence declaration.

---

## 6. Phase 2: AST Construction (`ast_builder.py` & `ast_nodes.py`)

### 6.1 The Transformer Pattern

`ASTBuilder` is a Lark `Transformer`. It walks the parse tree **bottom-up**: for each grammar rule node it encounters, it calls the method with the matching name (or alias). By the time a method is called, all its children have already been transformed into AST nodes or plain Python values.

Key method decorators:
- **`@v_args(meta=True)`**: Passes a `meta` object (containing `.line` and `.column`) as the first argument. Used for methods that produce AST nodes with source locations.
- **`@v_args(inline=True)`**: Unpacks children as positional arguments instead of a list. Used for simple, fixed-arity rules.

A `_filename: str` stored on the builder is embedded into every `SourceLoc` it creates, enabling multi-file error reporting.

### 6.2 Intermediate Types

Two helper types exist **only inside the builder** and never appear in the final AST:

- **`_ActionInfo(name, is_special)`**: Produced by the `action_name` rule. Bundles the action name and whether it is a reserved special primitive (`TELL`, `ACHIEVE`, etc.). Consumed by `do_stmt`, `world_do_stmt`, and `role_do_stmt`.
- **`Tuple[prefix_stmts, branches, else_branch]`**: Produced by `pb_when_body` and `plot_when_body`. Classifies the flat, `?`-inlined list of children into the three logical parts of a `WHEN` block body before `pb_when_block` / `plot_when_block` constructs the final node.

### 6.3 AST Node Hierarchy (`ast_nodes.py`)

All downstream passes work exclusively on these typed `@dataclass` nodes, never on the raw Lark tree:

```
Program
├── ImportDecl                            (IMPORT statements)
├── ActionDecl / EventDecl / FactDecl    (shared vocabulary declarations)
├── PlaybookDef                           (reusable behaviour bundles)
│   └── PbWhenBlock
│       ├── prefix_stmts: List[DoStmt | SignalStmt]
│       ├── branches:     List[PbIfBranch]
│       │   └── condition: ConditionExpr
│       └── else_branch:  PbElseBranch (optional)
└── PlotDef                               (narrative scenarios)
    ├── phases:        List[PhaseDecl]
    ├── roles:         List[RoleDecl]
    └── during_blocks: List[DuringBlock]
        ├── on_enters:   List[OnEnter]
        ├── on_exits:    List[OnExit]
        └── when_blocks: List[PlotWhenBlock | PlotWhenSubplotEndsBlock]
            ├── prefix_stmts: List[ImperativeStmt]
            ├── branches:     List[PlotIfBranch]
            └── else_branch:  PlotElseBranch (optional)
```

#### Source Locations

Every AST node carries a `SourceLoc(line, column, filename)`. `line` and `column` are 1-based, matching the Lark convention. The `filename` field enables per-file error messages in multi-file compilation. A frozen sentinel `_NO_LOC = SourceLoc(0, 0)` is used as the default for nodes where position is irrelevant.

#### Condition Expression Types

Condition expressions form a small recursive union type:

```python
ConditionExpr = Union[ConditionOr, ConditionAnd, ConditionNot, FactRef]
```

The builder applies **single-child collapsing** to keep conditions flat: if a `condition` rule (OR) has only one `condition_and` child, it returns the child directly instead of wrapping it in a `ConditionOr`. The same logic applies to `condition_and`. This means a simple `IF happy:` becomes a bare `FactRef`, not a deeply nested `ConditionOr > ConditionAnd > FactRef` chain.

#### Special Constants

`SPECIAL_ACTIONS: frozenset[str]` holds the names of reserved action keywords (`TELL`, `BROADCAST`, `ACHIEVE`, `BELIEVE`, `FORGET`, `PRINT`, `WAIT`). This constant is imported by both the builder (to set `is_special` flags) and the validator (to skip declaration checks for built-ins).

---

## 7. Phase 4: Semantic Validation (`validator.py`)

The validator walks the typed AST and enforces semantic rules that the grammar cannot express. It does **not** modify the AST — it only reads and reports.

### 7.1 Global Symbol Table (`_SymbolTable`)

Holds four flat namespaces mapping identifier strings to `DeclInfo(loc, arity)`:

| Namespace | Contents |
|---|---|
| `actions` | All `ActionDecl` names (and aliases) |
| `events` | All `EventDecl` names |
| `facts` | All `FactDecl` names |
| `playbooks` | All `PlaybookDef` names |

### 7.2 Per-Plot Scope (`_PlotScope`)

Each `PlotDef` gets its own `_PlotScope(plot_name, roles, phases)`. Roles and phases live only within their Plot; they cannot be referenced from other Plots and do not pollute the global namespace.

### 7.3 Validation Passes

`validate(program)` runs three sequential sub-passes:

**Pass 0 — Plot Role Registry Pre-scan**: Iterates all `PlotDef` items and builds `_plot_roles: Dict[str, Set[str]]` (plot name → set of role names). This is needed to validate `START SUBPLOT` targets and `MAPPING` clauses *before* the items are individually validated in Pass 2.

**Pass 1 — Declaration Collection (`_collect_declarations`)**: Registers every top-level declaration into the global symbol table, catching duplicates. For `ActionDecl` nodes with an `alias`, both the canonical name and the alias are registered under the same arity. A separate `_action_aliases` dict is maintained for use during emission.

**Pass 2 — Deep Validation**: Traverses into `PlaybookDef` and `PlotDef` nodes, checking every reference:

- *Playbook validation*: WHEN event references, DO action references, SIGNAL event references, and IF condition fact references.
- *Plot validation*: Exactly one `INITIAL` phase, no duplicate phases/roles within the plot scope, DURING block phase references, ON ENTER/ON EXIT structural constraints (at most one each per DURING block), and all WHEN block references.

**Pass 3 — Unused Warnings (`_check_unused`)**: Compares the declared namespaces against four usage-tracking sets (`_used_actions`, `_used_events`, `_used_facts`, `_used_playbooks`). Any declared name not in its usage set triggers a WARNING diagnostic.

### 7.4 Terminal Statement Rules

`_check_terminal_stmts()` enforces positional constraints on `InlineTransitionStmt` and `PlotEndStmt`:

1. `InlineTransitionStmt` is forbidden inside `DURING PLOT` blocks (where there is no single current phase to leave).
2. Both terminal types must be the **last statement** in their containing list. Any statement that follows one is reported as "unreachable".
3. Both are also forbidden inside `ON ENTER` and `ON EXIT` hooks (checked separately in `_validate_during_block`).

### 7.5 Implicit Events

Two event names — `parent_ended` and `child_ended` — are declared in the `_IMPLICIT_EVENTS` frozenset. They are part of the Plot lifecycle infrastructure and are always valid references in `WHEN` blocks without needing an explicit `EVENT` declaration.

---

## 8. Phase 5: AgentSpeak Emission (`emitter.py`)

The emitter takes the validated AST and generates the AgentSpeak (`.asl`) files. It never writes to disk; it returns a `Dict[str, str]` mapping filenames to source strings. The caller (CLI or `compiler.py`) handles writing.

### 8.1 Output File Structure

For a program with *P* Plots, *B* Playbooks, and roles *R₁...Rₙ* in each plot, the emitter produces:

| Filename | One per | Contents |
|---|---|---|
| `playbook_<name>.asl` | Playbook | Static-gated WHEN plans |
| `director_<plot>.asl` | Plot | Phase FSM, WORLD DO plans, lifecycle infrastructure |
| `role_<plot>_<role>.asl` | Plot × Role | Playbook includes, activation handlers, Role DO handlers |

### 8.2 Emission Passes

`emit(program)` executes five internal phases:

**Phase 1 — Index Playbooks**: Builds `_playbook_defs: Dict[str, PlaybookDef]` and collects action aliases from `ActionDecl.alias` fields.

**Phase 2 — Pre-scan Plots**: For each Plot, `_prescan_plot()` walks all `DuringBlock`, `OnEnter`, `OnExit`, and `WHEN` block bodies. It populates:
- `_role_playbooks`: global map of role name → set of all Playbooks ever assigned to it across all Plots.
- `_plot_role_playbooks`: per-Plot map of role name → Playbooks assigned in that specific Plot.
- `_role_directives`: per-role list of `_RoleDirective` (one-off `Role DO` commands, with their source plot and phase).
- `_role_mappings`: flat list of `(source_plot, source_role, target_plot, target_role)` tuples from `START SUBPLOT ... MAPPING` clauses.

**Phase 2.5 — Transitive Closure Computation**: `_compute_role_transitive_closures()` builds a directed graph from `_role_mappings` and performs a Depth-First Search from each `(plot_name, role_name)` pair. The resulting `_role_closures` captures all `(Plot, Role)` pairs reachable from any starting role via MAPPING chains. This is used during role file emission to include *all* Playbooks that might ever be assigned to an agent across nested subplot hierarchies — ensuring static gating works for deep plot nesting without dynamic plan injection.

**Phase 3 — Emit Playbook Files**: For each Playbook, `_emit_playbook_file()` generates a standalone `.asl` containing static-gated plans for each `PbWhenBlock`. The gate condition is `playbook_active(playbook_name, _)`, which must be true for any plan to fire. Any `#@` doc annotations on the Playbook are emitted as `//` comments below the file banner.

**Phase 4 — Emit Director Files**: `_emit_director()` generates the Director agent `.asl` for each Plot. Any `#@` doc annotations on the Plot are emitted as `//` comments below the file banner. This is the most complex output file, containing:
- **Initial beliefs**: `plot_name(...)` and `current_phase(initial_phase)`.
- **Boot plan**: `+!boot` — fires on agent creation, logs the startup, registers the plot identity, and triggers `!on_enter` for the initial phase.
- **Director WHEN plans**: Generated by `_emit_when_as_director()` from all `DuringBlock.when_blocks`.
- **Phase transition infrastructure**: An atomic `+!switch_phase(Target)` plan that executes the ON EXIT of the current phase, updates the `current_phase` belief, and executes the ON ENTER of the new phase. Per-phase `+!on_exit(phase)` and `+!on_enter(phase)` plans are emitted from the AST's `OnExit` and `OnEnter` nodes. Catch-all `+!on_exit(_) <- true.` and `+!on_enter(_) <- true.` plans handle phases with no hooks.
- **Plot lifecycle infrastructure**: `+!parent_ended`, `+!end_plot`, `+!notify_parent`, and `+!start_subplot` plans for the parent-child Director hierarchy.
- **Role-agent registry**: `+!start_plot(Bindings)` to populate `role_agent/2` beliefs, `+!send_to_role/3` as a communication helper, and `+agent_died(DeadAgent)` to prune dead agents from the registry.

**Phase 5 — Emit Role Files**: `_emit_plot_role(plot_name, role_name)` generates a per-Plot-Role `.asl` file. It uses the transitive closure to determine the full set of Playbooks this role might ever need (including those from subplots), then emits:
- `{ include("playbook_<name>.asl") }` directives for each Playbook in the closure.
- `+!add_playbook` and `+!remove_playbook` handlers for the Director's ASSIGN/UNASSIGN commands.
- `+!plot_ended(PlotId)` to clean up ghost `playbook_active` beliefs when a plot terminates.
- `+!signal_directors(PbName, Payload)` — the infrastructural plan used by `SIGNAL`. It uses `.findall` to discover all active Director IDs for a playbook, then sends `untell` followed by `tell` to force the Director to process duplicate signals as fresh events.
- One `+!goal <- action.` plan for each unique `Role DO` directive in the transitive closure.

### 8.3 Plan Generation

All AgentSpeak plans are written through `_write_plan()`, which formats the complete plan structure:

```agentspeak
@plan_label[priority(N), temper([...]), effects([...])]
+event_name : context1 & context2 <-
    stmt1;
    stmt2.
```

Context conditions from multiple sources (phase guard, IF condition) are joined with ` & `. Plan bodies use `;` separators with a final `.`. The `ELSE` branch is implemented as a separate plan whose context is the negation of all preceding `IF` conditions: `not (cond1) & not (cond2)`.

### 8.4 Statement Emission

| Regia statement | Emitter method | AgentSpeak output |
|---|---|---|
| `DO action(args)` | `_emit_do_stmt` | `action(args)` |
| `DO TELL(t, m)` | `_emit_do_stmt` (special) | `.send(t, tell, m)` |
| `DO BROADCAST(m)` | `_emit_do_stmt` (special) | `.broadcast(tell, m)` |
| `DO ACHIEVE(g)` | `_emit_do_stmt` (special) | `!g` |
| `DO BELIEVE(f)` | `_emit_do_stmt` (special) | `+f` |
| `DO FORGET(f)` | `_emit_do_stmt` (special) | `-f` |
| `DO PRINT(t)` | `_emit_do_stmt` (special) | `.print(t)` |
| `DO WAIT(ms)` | `_emit_do_stmt` (special) | `.wait(ms)` |
| `SIGNAL e` | `_emit_signal_stmt` | `!signal_directors(pb_name, e)` |
| `WORLD DO action` | `_emit_imperative_stmt` | `action` |
| `Role DO action` | `_emit_imperative_stmt` | `!send_to_role(role, achieve, action)` |
| `ASSIGN Pb TO Role` | `_emit_imperative_stmt` | `!send_to_role(role, achieve, add_playbook(pb))` |
| `UNASSIGN Pb FROM Role` | `_emit_imperative_stmt` | `!send_to_role(role, achieve, remove_playbook(pb))` |
| `TRANSITION TO phase` | `_emit_imperative_stmt` | `!switch_phase(phase)` |
| `START SUBPLOT P MAPPING ...` | `_emit_start_subplot_stmts` | `!start_subplot("p", p, [map(...)])` |
| `END PLOT` | `_emit_imperative_stmt` | `!end_plot` |

Action aliases declared with `AS` are resolved during emission: `_emit_do_stmt` looks up the alias in `_action_aliases` and emits the canonical action name.

---

## 9. Error Reporting Infrastructure (`errors.py`)

All compiler phases share a single `ErrorReporter` instance. It acts as a central accumulator for `CompilerMessage` objects throughout the entire pipeline run.

### `CompilerMessage`

A frozen snapshot of a single diagnostic:

```python
@dataclass
class CompilerMessage:
    severity:    Severity   # ERROR or WARNING
    line:        int        # 1-based line number
    column:      int        # 0-based column offset
    length:      int        # Token length (for caret width)
    message:     str        # Human-readable description
    hint:        str        # Optional fix suggestion
    source_line: str        # Raw source line for caret display
    filename:    str        # Source file name
```

### Source Registry

`register_source(filename, source)` stores a split-by-line copy of each source file. When a message is added, `_get_source_line(filename, line)` retrieves the relevant line for caret display. This allows any phase to produce context-rich diagnostics from any file in a multi-file compilation without coupling to the file system.

### Column Convention

- The Lark parser reports columns as **1-based**.
- `syntax_errors.py` subtracts 1 when calling `reporter.error()` to convert to 0-based.
- `validator.py` uses `max(loc.column - 1, 0)` for the same reason.
- `ErrorReporter` stores and displays columns in **0-based** form.

---

## 10. Web Server Integration (`server.py`)

The FastAPI server (`server.py`) exposes the compiler to the React editor frontend via a single `POST /parse` endpoint. It uses `compile_source()` (which stops after Phase 4 Validation and attaches the AST) and returns the AST as JSON for visual rendering in the editor's canvas.

### `ASTEncoder`

Because the AST consists of Python `@dataclass` objects, a custom `json.JSONEncoder` is required. `ASTEncoder.default()` uses `obj.__dict__.copy()` (a *shallow* dict) and injects a `"type"` field with the class name. This forces the standard `json.dumps` machinery to call `default()` recursively for each nested dataclass, rather than trying to serialize the entire tree in one pass. This `"type"` field is what the React frontend uses to identify which node it is rendering.

On compilation failure, the server raises an `HTTPException(status_code=400)` with the diagnostic list as the detail body. Severity enum values are serialised to their `.name` string (`"ERROR"` / `"WARNING"`) before returning, since raw `Enum` objects are not JSON-serialisable.

---

## 11. Module Summary

| File | Role | Key exports |
|---|---|---|
| `cli.py` | User-facing CLI | `main()` (Click group) |
| `compiler.py` | Pipeline orchestrator | `compile_source`, `compile_file`, `compile_files`, `CompileResult` |
| `preprocessor.py` | Phase 0 | `preprocess()`, `resolve_imports()`, `SourceAnnotations`, `DocAnnotation` |
| `parser.py` | Phase 1 (interface) | `parse()` |
| `grammars/regia.lark` | Phase 1 (grammar) | LALR(1) grammar definition |
| `syntax_errors.py` | Phase 1 (error humaniser) | `report_syntax_error()` |
| `ast_nodes.py` | Phase 2 (data model) | All AST node `@dataclass` types, `ConditionExpr`, `SPECIAL_ACTIONS` |
| `ast_builder.py` | Phase 2 (construction) | `ASTBuilder` (Lark Transformer) |
| `validator.py` | Phase 4 | `Validator`, `_SymbolTable`, `_PlotScope`, `DeclInfo` |
| `emitter.py` | Phase 5 | `Emitter`, `_RoleDirective` |
| `errors.py` | Cross-cutting concern | `ErrorReporter`, `CompilerMessage`, `Severity` |
