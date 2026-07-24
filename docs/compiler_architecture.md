# Regia Compiler Architecture

> **Scope**: This document explains the internal architecture of the Regia compiler. It traces the data flow from raw `.regia` source code to compiled AgentSpeak (`.asl`) files, detailing the goals, key patterns, and core data structures of each compilation phase.

---

## 1. Compiler Pipeline Overview

The Regia compiler (located in `language/src/regia/`) operates as a classic multi-pass transpiler. It converts domain-specific Regia narratives into executable, multi-agent AgentSpeak logic.

The transpilation pipeline consists of five strict, sequential phases:

1. **Preprocessor:** Cleans the source, resolves imports, and extracts metadata.
2. **Parser:** Converts raw text into an untyped syntax tree.
3. **AST Builder:** Transforms the parse tree into strongly-typed Python objects.
4. **Validator:** Enforces semantic rules, scopes, and name resolution.
5. **Emitter:** Generates the final AgentSpeak `.asl` files.

---

## 2. CLI Entrypoint (`cli.py`)

The compiler is invoked via the command-line interface defined in `cli.py`.

* **Goal**: Handle user input, manage file I/O, orchestrate the pipeline, and report errors.
* **Key Operations**:
  * Exposes commands like `compile <file.regia> -o <out_dir>`.
  * Instantiates the `ErrorReporter` to collect warnings and errors across all phases.
  * Triggers the `compile_file()` sequence, passing data cleanly from one phase to the next.
  * Formats and prints any intercepted compilation errors to the terminal, halting the process if validation fails.

---

## 3. Phase 1: Preprocessing & Import Resolution (`preprocessor.py`)

Before the formal grammar even sees the text, the Preprocessor cleans it up and resolves multi-file dependencies.

* **Goal**: Extract documentation, strip comments to prevent parser clutter, and resolve `IMPORT` statements into a single cohesive AST.
* **Key Patterns**:
  * **Regex Scrubbing**: Single-line and block comments are identified and replaced with whitespace (to preserve accurate line numbers for error reporting later).
  * **Recursive Compilation**: When an `IMPORT "path/to/file.regia".` is encountered, the compiler recursively runs the Preprocessor, Parser, and AST Builder on the imported file. The resulting AST nodes are merged into the main file's AST before validation.
* **Data Structures**:
  * `DocAnnotation`: Stores the text and source location of documentation comments.
  * `SourceAnnotations`: A container mapping line numbers to their extracted `DocAnnotation`s.

---

## 4. Phase 2: Lexing & Parsing (`grammars/regia.lark`)

Regia relies on the [Lark](https://github.com/lark-parser/lark) parsing toolkit to define its formal grammar and build the initial syntax tree.

* **Goal**: Convert the preprocessed string into an untyped, hierarchical tree based on syntactic rules.
* **Key Patterns**:
  * **LALR(1) Parsing**: The grammar uses the efficient LALR algorithm.
  * **Tree Shaping**: The grammar file (`regia.lark`) makes heavy use of Lark's tree-shaping operators (like `?` to inline rules and aliases) to keep the generated tree as flat and clean as possible.
* **Data Structures**:
  * Lark's native `Tree` (representing grammar rules) and `Token` (representing raw string matches like IDs or literals).

---

## 5. Phase 3: AST Construction (`ast_builder.py` & `ast_nodes.py`)

Raw parse trees are difficult to work with safely. This phase converts the untyped Lark Tree into our own strictly-typed Abstract Syntax Tree (AST).

* **Goal**: Transform strings and raw tokens into semantic, domain-specific Python objects.
* **Key Patterns**:
  * **Bottom-Up Traversal**: `ast_builder.py` implements a Lark `Transformer`. It walks the parse tree from the leaves to the root. As each rule is encountered, its corresponding method (e.g., `def action_decl(...)`) is called, receiving its previously-transformed children as arguments.
* **Data Structures (`ast_nodes.py`)**:
  * Python `@dataclass` objects represent the structure of Regia.
  * *Base Elements*: `ActionDecl`, `EventDecl`, `FactDecl`.
  * *Narrative Scopes*: `PlaybookDef`, `PlotDef`, `PhaseDecl`.
  * *Control Flow*: `PbWhenBlock`, `PlotWhenBlock`, `IfBranch`.
  * *Statements*: `DoStmt`, `SignalStmt`, `InlineTransitionStmt`.

---

## 6. Phase 4: Semantic Validation (`validator.py`)

A syntactically correct Regia file can still contain semantic errors (e.g., referencing an action that doesn't exist, or transitioning to a non-existent phase).

* **Goal**: Enforce language rules, validate references, and emit warnings for unused code.
* **Key Patterns**:
  * **Two-Pass Visitor**:
    * **Pass 1 (Collection)**: The validator scans all top-level items (`ActionDecl`, `PlaybookDef`, etc.) and registers them in a central symbol table. Duplicate declarations are caught here.
    * **Pass 2 (Validation)**: The validator walks deeply into `WHEN` blocks and `DURING` blocks. It checks that every `DO` action exists in the symbol table, ensures transitions point to valid phases, and verifies structural constraints (like `ON ENTER` uniqueness).
* **Data Structures**:
  * `Validator`: The main visitor class.
  * `_SymbolTable` & `DeclInfo`: Maps identifiers to their arity and source locations.
  * **Usage Sets**: Tracks which elements were actually referenced (`_used_actions`, `_used_events`, etc.). Anything not in these sets by the end of Pass 2 triggers an "unused declaration" warning.

---

## 7. Phase 5: AgentSpeak Emission (`emitter.py`)

The final phase takes the validated, completely sound AST and translates it into Jason-compatible AgentSpeak code.

* **Goal**: Generate multi-agent `.asl` files that accurately reproduce the Regia logic.
* **Key Patterns**:
  * **Multi-Pass Generation**:
    1. **Pre-scan**: The emitter scans all Plots to discover exactly which Playbooks are assigned to which Roles, and computes transitive closures (to handle nested plot mappings).
    2. **Emit Playbooks**: Creates a separate `.asl` file for each Playbook. `WHEN` blocks are mapped to AgentSpeak plans triggered by `+event`. These plans are gated dynamically using the `playbook_active(Name)` context guard.
    3. **Emit Directors**: Creates a central coordinator `.asl` file for each Plot. It handles the finite-state machine logic (phase transitions, `ON ENTER`/`ON EXIT` logic, and `START SUBPLOT` delegations).
    4. **Emit Roles**: Creates an `.asl` file for each specific Role in a Plot. This file includes the necessary Playbooks and sets up listeners for Director commands. Listeners for playbook assignments use `achieve` goals (`+!add_playbook`) and signal broadcasts use `untell/tell` sequences to prevent Jason's belief base from dropping duplicate events.
* **Data Structures**:
  * `Emitter`: Maintains the state of file generation.
  * `_outputs`: A dictionary mapping output filenames (e.g., `director_test.asl`) to their generated string content. These strings are finally written to disk by the CLI.
