# Regia — Compiler Architecture & Mapping

> **Scope**: This document maps the core constructs defined in the [Regia Language Design Document](regia_design_document.md) to their actual implementation inside the Regia compiler. It serves as a bridge for developers who need to understand how the theoretical language design maps to the grammar, AST, and compiler pipeline.

---

## 1. Compiler Pipeline Overview

The Regia compiler (`language/src/regia/`) translates `.regia` source files into `.asl` AgentSpeak files in five distinct passes:

1. **Preprocessor** (`preprocessor.py`): Scans raw source text to extract doc-comments and resolve imports, substituting them with blank lines to preserve line numbers before passing the cleaned text to the parser.
2. **Parser** (`regia.lark`): Defines the formal grammar and parses text into a raw parse tree using Lark.
3. **AST Builder** (`ast_builder.py`): Transforms the raw parse tree into strongly-typed Python objects defined in `ast_nodes.py`.
4. **Validator** (`validator.py`): Performs semantic checks (name resolution, type constraints, structural rules) and reports user-facing errors.
5. **Emitter** (`emitter.py`): Translates the validated AST into valid AgentSpeak (`.asl`) code.

---

## 2. Concept Implementation Mapping

This section details exactly which data structures and functions are responsible for handling each major language element.

### 2.1 Actions
* **Grammar** (`regia.lark`): `action_decl`
* **AST Node** (`ast_nodes.py`): `ActionDecl`
* **Builder** (`ast_builder.py`): `action_decl()`
* **Validator** (`validator.py`): `_check_action_ref()` ensures that any action referenced in a `DO` statement has been declared.
* **Emitter** (`emitter.py`): Emitted through `_emit_pb_stmt()` and `_emit_imperative_stmt()`. Special actions (`TELL`, `BROADCAST`, etc.) have hardcoded translations here.

### 2.2 Events
* **Grammar** (`regia.lark`): `event_decl`
* **AST Node** (`ast_nodes.py`): `EventDecl`
* **Builder** (`ast_builder.py`): `event_decl()`
* **Validator** (`validator.py`): `_check_event_ref()` ensures that events used in `WHEN` triggers and `SIGNAL` statements have been declared.
* **Emitter** (`emitter.py`): Processed as the trigger condition (e.g. `+event`) when writing AgentSpeak plans via `_write_plan()`.

### 2.3 Facts
* **Grammar** (`regia.lark`): `fact_decl`
* **AST Node** (`ast_nodes.py`): `FactDecl` (declaration), `FactRef` (usage)
* **Builder** (`ast_builder.py`): `fact_decl()`
* **Validator** (`validator.py`): `_check_fact_ref()` and `_validate_condition()` ensure facts used in `IF` and `TRANSITION` guards are valid.
* **Emitter** (`emitter.py`): Compiled into context clauses (e.g. `: fact(X)`) within `_emit_condition()`.

### 2.4 Playbooks
* **Grammar** (`regia.lark`): `playbook_def`, `pb_when_block`
* **AST Node** (`ast_nodes.py`): `PlaybookDef`, `PbWhenBlock`
* **Builder** (`ast_builder.py`): `playbook_def()`, `pb_when_block()`
* **Validator** (`validator.py`): `_validate_playbook()` ensures that playbook internal logic is sound and delegates to `_validate_pb_when_block()`.
* **Emitter** (`emitter.py`): `_emit_playbook()` handles the creation of a dedicated `.asl` file for each playbook, resolving `WHEN` blocks into `.asl` plans.

### 2.5 Plots & Phases
* **Grammar** (`regia.lark`): `plot_def`, `phase_decl`, `during_block`
* **AST Node** (`ast_nodes.py`): `PlotDef`, `PhaseDecl`, `DuringBlock`
* **Builder** (`ast_builder.py`): `plot_def()`, `_sort_during_content()` organizes the internal statements (`ON ENTER`, `ON EXIT`, transitions).
* **Validator** (`validator.py`): `_validate_plot()` performs plot-wide scoping checks (like missing roles, exactly one initial phase), and `_validate_during_block()` checks phase-specific limits (e.g., maximum one `ON ENTER` block).
* **Emitter** (`emitter.py`): Uses `_emit_director()` to generate the `director_<plot_name>.asl` file, and `_emit_role()` to generate the `role_<plot_name>_<role>.asl` files.

### 2.6 Transitions (Inline)
* **Grammar** (`regia.lark`): Handled as `transition_stmt` inside `imperative_stmt` (within `WHEN` blocks).
* **AST Node** (`ast_nodes.py`): `InlineTransitionStmt`
* **Builder** (`ast_builder.py`): Constructed naturally via statement parsing inside `WHEN` branches.
* **Validator** (`validator.py`): `_check_inline_transition()` validates target phases and ensures the transition is always the final statement in its block/branch. It also explicitly forbids them inside `DURING PLOT` scopes.
* **Emitter** (`emitter.py`): Evaluated in `_emit_imperative_stmt()`, translating into a sequence of beliefs: triggering the old phase's `ON EXIT`, updating `current_phase`, and triggering the new phase's `ON ENTER`.

### 2.7 Reactive Plans (WHEN blocks)
* **Grammar** (`regia.lark`): `pb_when_block`, `plot_when_block`
* **AST Node** (`ast_nodes.py`): `PbWhenBlock`, `PlotWhenBlock`
* **Builder** (`ast_builder.py`): `pb_when_block()`, `plot_when_block()` separate the statement bodies into conditional branches (`IF`/`ELSE`) and unconditional prefixes.
* **Validator** (`validator.py`): Validates event references and branch contexts within `_validate_pb_when_block()` and `_validate_plot_when_block()`.
* **Emitter** (`emitter.py`): Emitted dynamically via `_write_plan()`, combining triggers (`+event`), context clauses (`: condition`), and bodies (`<- actions`) into discrete `.asl` plans.

### 2.8 Preprocessing Constructs (Imports & Doc Comments)
* **Grammar**: Not parsed by Lark. Handled purely by regex before syntax parsing.
* **Data Structures** (`preprocessor.py`): `DocAnnotation`, `SourceAnnotations`
* **Processor** (`preprocessor.py`): `preprocess()`, `resolve_imports()`
* **Validator** (`validator.py`): (Imports) Validated globally by merging ASTs from multiple files into a single project scope.
* **Emitter**: Doc comments are discarded at emission time, while imports dictate which source files are compiled.

### 2.9 Emotional Modeling (TEMPER & EFFECTS)
* **Grammar** (`regia.lark`): `temper`, `effects`
* **AST Node** (`ast_nodes.py`): `TemperSpec`, `TemperEntry`
* **Builder** (`ast_builder.py`): `temper()`
* **Emitter** (`emitter.py`): Processed directly into AgentSpeak plan annotations (`temper([...])`, `effects([...])`) inside the `_write_plan()` helper function.
