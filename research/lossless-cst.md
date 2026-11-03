# Lossless syntax trees for Regia 2.0 (research)

**Status:** research only. This note lays out options and evidence. It does not choose one.
**Date:** 2026-11-03
**Ticket:** Regia 2.0 design. The Transpiler exposes a lossless CST to the Visual Editor, possibly in the browser through WASM.

## 1. The question, framed for Regia

Regia is indentation-sensitive: blocks open with `:`, `.` and `;` terminators are optional, and it has `#` line comments, `## ... ##` block comments and `#@` doc comments. The Visual Editor shows Monaco text next to a React Flow graph, and both can be edited. A graph edit has to come back as a text edit that keeps the user's whitespace and comments. Typical graph edits are: insert a step, delete a step, reorder siblings, move a block under another parent (which changes its depth), and edit a condition.

So the CST must do four things:

1. **Losslessness.** `print(parse(src)) == src`, byte for byte, including on invalid input.
2. **Trivia ownership.** Every whitespace or comment run belongs to some node, so moving or deleting a node takes "its" comments with it.
3. **Structured edits.** Insert, replace, delete and move, plus re-indenting a moved block.
4. **Incremental update** after Monaco text edits, with node identities that survive the update so the graph layout stays stable.

It also has to fit a WASM build that runs next to Monaco.

`docs/first reasonings/6 - Transpiler.md` already asks for this: export the CST, translate the CST back to text, and make doc comments part of the grammar instead of a preprocessing side table.

## 2. Overview

| System | Tree model | Where trivia lives | Prints back exactly? | Structured edit API | Incremental reparse | Indentation story | Browser/WASM fit |
|---|---|---|---|---|---|---|---|
| **rowan** (rust-analyzer) | Green (immutable, shared) plus red (cursor with parent and offset) | ≤0.17: trivia are sibling tokens. 0.18-alpha: leading and trailing trivia on each token | Yes | No mutation API since 0.17. rust-analyzer builds `SyntaxEditor` on top | Possible by patching green nodes; rust-analyzer mostly reparses fully | Up to the hand-written lexer and parser. rust-analyzer has an `IndentLevel` helper for edits | Pure Rust, few dependencies. Compiles to wasm32 |
| **Roslyn** | Red/green (the original design) | Leading and trailing trivia on tokens, with fixed ownership rules | Yes ("full fidelity") | `With*`, `ReplaceNode`, `SyntaxEditor`, elastic trivia plus a formatter | `WithChangedText` | Not applicable to C#. The model is general | .NET only. Useful as a design reference |
| **tree-sitter** | Compact C tree of byte ranges. No text stored | `extras`: comments can be nodes, whitespace sits in gaps between nodes | Only by slicing the original buffer | None. You make text edits, then call `tree.edit` and reparse | Yes. This is its core feature. `get_changed_ranges` | External scanner in C (Python scanner keeps an INDENT stack) | `web-tree-sitter` plus a per-grammar `.wasm`. Rust crate can target wasm32 |
| **Lezer** | Compact JS tree of type, range and children. No text stored | Skipped tokens appear in the tree only if named with a capital letter | Only by slicing the input | None | Yes (`TreeFragment.applyChanges`) | `ExternalTokenizer` plus `ContextTracker` (the Python grammar does this) | Native JS, no WASM. Needs a second grammar next to the Rust one |
| **LibCST** | Typed immutable CST (Python dataclasses). Rust native parser | Named whitespace fields on nodes (`leading_lines`, `whitespace_before`, `header`, `footer`, ...) | Yes, checked by round-trip tests | `with_changes`, `deep_replace`, transformers | No | Blocks store indent *relative* to the parent (`IndentedBlock.indent`) | Python-bound (PyO3, optional feature). No documented WASM build |
| **parso** | Mutable Python tree | `prefix` string on every leaf | Yes (`get_code()`) | Direct mutation | "Diff parser": difflib plus node reuse, mutable | INDENT/DEDENT stay out of the tree. Whitespace goes to prefixes | Python only |

## 3. Shared concepts

### 3.1 The lossless invariant

Every system above that claims losslessness rests on the same invariant: **concatenating all token texts (and trivia texts) in order gives back the source**. rust-analyzer says: "Syntax trees are lossless, or full fidelity. All comments and whitespace get preserved", and "even if the input is invalid, the tree produced by the parser represents it exactly" ([rust-analyzer syntax.md][ra-syntax]). Roslyn says trees "can produce the exact text that they were parsed from... by making a new tree out of changes to an existing tree, you have effectively edited the text" ([Roslyn syntax model][roslyn-syntax]).

Error tolerance is part of losslessness. Roslyn inserts zero-width *missing* tokens and stores *skipped* tokens as `SkippedTokensTrivia` ([Roslyn syntax model][roslyn-syntax]). Lezer wraps ignored input in error nodes ([Lezer guide][lezer-guide]). parso "supports error recovery and round-trip parsing" ([parso docs][parso-docs]). This matters for Regia because Monaco shows invalid code most of the time while the user types, and the graph still has to render.

### 3.2 Green/red (immutable, shared) trees

Eric Lippert's description of Roslyn: the green tree "is immutable, persistent, has no parent references", and "every node tracks its width but not its absolute position". The red tree is "an immutable façade that is built around the green tree", built top-down on demand and thrown away on edit. Persistence gives "the ability to reuse most of the existing nodes", so "we rebuild only the portions of the green tree that were affected by the edit" ([Lippert, Red-Green Trees][lippert]).

rowan uses the same idea: only green nodes store data, and `SyntaxNode` "adds parent pointers and identify semantics" ([rust-analyzer syntax.md][ra-syntax]). The rowan cursor module calls itself "a zipper for a purely functional (green) tree" ([rowan cursor.rs][rowan-cursor]).

**Why this matters for a visual editor.** An edit costs O(depth): the path to the root is rebuilt and siblings are shared. Old snapshots stay valid, which gives undo and diffing almost for free. Identical subtrees can be deduplicated.

### 3.3 Four ways to attach trivia

| Model | Used by | Effect on structured edits |
|---|---|---|
| **Trivia as sibling tokens** in the node list | rowan ≤0.17 / rust-analyzer (attached by `TreeSink` heuristics, e.g. a comment above a fn becomes a child of the fn) ([ra-syntax]); tree-sitter `extras` | Simple to build. Moving a node needs a separate rule for which neighbouring whitespace and comments go with it |
| **Leading and trailing trivia on each token** | Roslyn: "a token owns any trivia after it on the same line up to the next token. Any trivia after that line is associated with the following token" ([roslyn-syntax]); Biome's rowan fork ([biome trivia.rs][biome-trivia]); rowan 0.18-alpha ([rowan #219][rowan-219], [rowan token.rs][rowan-token]) | Ownership is fixed by the lexer, so a moved node carries its leading comments automatically. Inserted nodes need trivia synthesized (Roslyn uses elastic trivia) |
| **Named whitespace fields on typed nodes** | LibCST: "assigning it to relevant nodes... much more granular whitespace ownership" ([LibCST why][libcst-why]). Whitespace goes to "the top-most node that can own" it, and between siblings the leftmost usually owns it ([LibCST native README][libcst-native]) | Edits are very ergonomic in typed code. The grammar and node types must be designed with whitespace in mind |
| **Prefix string on each leaf** | parso: `prefix` is "typically a mixture of whitespace and comments" ([parso tree.py][parso-tree]) | Simplest model. It is in effect "leading trivia only" |

The 2026 change in rowan is notable. PR #217 "Remove mutable api" (merged 2026-08-02, released as 0.17.0), then #219 "Make trivia first class member of token" (2026-09-07), shipped as 0.18.0-alpha.1/2. rust-analyzer master already depends on `rowan = "0.18.0-alpha.2"` ([rowan PRs][rowan-prs], [crates.io rowan][crates-rowan], [rust-analyzer Cargo.toml][ra-cargo]). In 0.18, `GreenTokenHead` holds `leading: Box<[GreenToken]>` and `trailing: Box<[GreenToken]>` ([rowan token.rs][rowan-token]). The API gains `trivia_before`, `trivia_after`, `text_without_outer_trivia` and `first_non_trivia_token` ([rowan api.rs][rowan-api]). **Version caveat:** this is an alpha. Its API is still moving.

## 4. The systems

### 4.1 rowan and rust-analyzer's `SyntaxEditor`

- **Data model.** `GreenNode` and `GreenToken` are immutable, untyped, and carry a `SyntaxKind`. Red `SyntaxNode` cursors add parent and offset. A typed AST layer is generated on top ([ra-syntax]). Dependencies are only `rustc-hash`, `hashbrown`, `text-size`, `memoffset` and `countme`, with optional `serde` ([rowan Cargo.toml][rowan-cargo]).
- **Parsing is up to you.** rowan is a tree library, not a parser generator. rust-analyzer's parser emits events into a builder, and the parser never sees whitespace. Trivia are attached in the sink layer ([ra-syntax]). For Regia this means a hand-written lexer and recursive-descent parser, or another parser driving a `GreenNodeBuilder`.
- **Incremental.** "Green trees are cheap to modify, so incremental reparse works by patching a previous tree". The heuristic is to reparse a single `{}` block. rust-analyzer notes that full reparsing is usually fast enough ([ra-syntax]).
- **Editing.** rowan itself now exposes only `replace_with(&self, GreenNode) -> GreenNode`, which returns a new root ([rowan cursor.rs][rowan-cursor]). rust-analyzer's `SyntaxEditor` is "Inspired by Roslyn's SyntaxEditor" ([ra syntax_editor.rs][ra-editor]). It records `insert`, `insert_all`, `insert_with_whitespace`, `replace`, `replace_with_many`, `replace_all`, `delete` and `merge` against an immutable root, using `Position::{before, after, first_child_of, last_child_of}`. `finish()` then validates an `EditPlan` and applies it in one pass ([ra edit_algo.rs][ra-edit-algo]). `SyntaxEdit::find_element` maps old nodes to their counterparts in the new tree, and `SyntaxAnnotation` tags survive the edit. New nodes come from a `SyntaxFactory` with mappings. Indentation is handled by helpers such as `ast::edit::IndentLevel` (imported by the editor module).
- **Forks.** Biome maintains `biome_rowan` with token-attached trivia, a `syntax_factory`, and its own batch mutation ([biome_rowan src][biome-rowan]). cstree is another fork focused on thread safety and interning ([cstree][cstree]).
- **WASM.** rowan is plain Rust with no C. Biome ships its rowan-based toolchain as `@biomejs/wasm-web` (2.6.4 on npm), which shows that rowan-family trees run in the browser. rust-analyzer's old browser demo `rust-analyzer-wasm` is archived (last push 2022).

### 4.2 Roslyn

- Immutable, thread-safe trees with full fidelity, including preprocessor directives. Nodes have `Span` (without trivia) and `FullSpan` (with trivia) ([roslyn-syntax]).
- **Trivia rule** (§3.3). The first token takes the file's initial trivia. Final trivia goes on a zero-width EOF token ([roslyn-syntax]).
- **Edits.** Factory and `With*` methods "create additional snapshots", and trees "reuse underlying nodes, so a new version can be rebuilt fast" ([roslyn-syntax]). `SyntaxFactory.ElasticMarker` is "an elastic trivia ... containing no characters. Elastic marker trivia are included automatically by factory methods when trivia is not specified. Syntax formatting will replace elastic markers with appropriate trivia" ([ElasticMarker][roslyn-elastic]). **This is the main pattern for "insert a new node from the graph without touching the user's formatting elsewhere":** new nodes get placeholder trivia, and only those placeholders are formatted.
- **Incremental.** `SyntaxTree.WithChangedText`: "If the new source text is a minor change ... an incremental parse will occur reusing most of the current syntax tree internal data" ([WithChangedText][roslyn-wct]).
- **WASM.** Not a candidate. This is a design reference only.

### 4.3 tree-sitter

- **Tree model.** A `TSNode` holds only context, an id and a tree pointer. No API returns node text, so you slice the source buffer using `ts_node_start_byte` and `ts_node_end_byte` ([api.h][ts-api]). `extras` are "tokens that may appear anywhere in the language. This is often used for whitespace and comments" ([grammar DSL][ts-dsl]). Comments can therefore be nodes, but whitespace usually exists only as gaps between node ranges.
- **Incremental editing.** First "edit the syntax tree, which adjusts the ranges of its nodes", then call `ts_parser_parse` again with the old tree, which "will create a new tree that internally shares structure with the old tree" ([advanced parsing][ts-adv]). Edits must be described "both in terms of byte offsets and in terms of (row, column) coordinates". `ts_tree_get_changed_ranges` compares the old and new trees ([api.h][ts-api]).
- **Limits for rewriting** (inferred from the API above, not stated by tree-sitter):
  - The tree is a read-only index over a text buffer. There is no node factory and no tree mutation.
  - A structured edit has to be written as a text splice at byte ranges, followed by `tree.edit` and a reparse.
  - Trivia ownership (which comment goes with a moved statement) is not modelled. The consumer must compute it from the gaps.
  - The tree is not a printable value, because printing means slicing the original text.

  This fits "graph edit → text patch → reparse" well. It fits "manipulate a tree, then print" badly.
- **Indentation.** External scanners exist for tokens "impossible or inconvenient to describe with a regular expression", and the docs name Python indent/dedent as the example ([external scanners][ts-ext]). The scanner's `serialize` "must store its entire state", up to `TREE_SITTER_SERIALIZATION_BUFFER_SIZE` bytes. In error recovery, `scan` is called with all tokens valid ([ts-ext]). tree-sitter-python's `scanner.c` keeps an `indents` stack: tabs count 8, blank lines are absorbed, and DEDENT waits until comments at the inner indent have been consumed. It serializes the stack two bytes per level ([tree-sitter-python scanner.c][ts-py-scanner]).
- **WASM.** `web-tree-sitter` (0.27.1 on npm, 2026-10-08) loads per-language `.wasm` files with `Language.load`. `tree-sitter build --wasm` builds a grammar, scanner included, and since 0.26.1 it downloads wasi-sdk automatically ([web binding README][ts-web]). The Rust crate can also target `wasm32-unknown-unknown` using a vendored libc in `src/wasm-stdlib` (0.27) ([docs.rs tree-sitter 0.27 wasm-stdlib][ts-wasm-stdlib]). One grammar (JS DSL to C) can serve both a Rust transpiler and the browser.

### 4.4 Lezer (CodeMirror 6)

- **Tree model.** "Each node only stores a type, a start and end position, and a flat sequence of children". Skipped tokens appear only when capitalized, like `Comment`. Trees are "very compact in memory and cheap to build", and productions you don't name "don't appear in the tree at all" ([Lezer guide][lezer-guide]). There is no text field on `Tree` ([Lezer ref][lezer-ref]). Like tree-sitter, it is an index over the text, not a printable CST, and has no edit API.
- **Incremental.** `TreeFragment.applyChanges` removes or splits fragments around edited ranges so the parser can reuse the rest ([Lezer ref][lezer-ref]).
- **Indentation.** `@lezer/python` uses a `ContextTracker` (`trackIndent`) that pushes a context on `indent` and pops on `dedent`, plus an `ExternalTokenizer` that measures leading whitespace (tab to the next multiple of 8). It emits `dedent` with negative length so the whitespace is not consumed, and ignores blank and comment-only lines. Bracket and string contexts switch the tokenizer off ([lezer python tokens.js][lezer-py]). The context `hash` keeps incremental reuse correct: nodes are reused only under an equal context unless `strict: false` ([Lezer ref][lezer-ref]).
- **WASM.** None needed, since it is JS. The cost is a second grammar (Lezer) maintained next to the Rust transpiler's grammar. Versions: `@lezer/lr` 1.4.12, `@lezer/python` 1.1.19.

### 4.5 LibCST

- **Lossless, typed, immutable.** "LibCST preserves all whitespace and can be reprinted exactly" ([LibCST why][libcst-why]). `with_changes` is "a convenience method for performing mutation-like operations on immutable nodes". `deep_replace` replaces by identity ([LibCST nodes][libcst-nodes]).
- **Parser.** A Rust native parser (`libcst.native`) with three stages: tokenize, a PEG grammar over the tokens (rust-peg) that produces "deflated" nodes holding token references, then **inflation**, which turns tokens into whitespace fields. Inflation mutates the tokens so "each piece of whitespace goes to at most one node". Correctness is checked "with byte-for-byte roundtrip tests" ([LibCST native README][libcst-native]).
- **Indentation (the most relevant detail for Regia).** `IndentedBlock` "begin[s] with an INDENT token and end[s] in a DEDENT token". It owns `header` (the trailing comment and newline after `:`), `indent: Optional[str]` ("None uses the module's default indentation... indentation is allowed to be inconsistent across a file"), and `footer` (comments and lines after the dedent that are indented further than the next statement) ([LibCST statement.py][libcst-stmt]). Codegen calls `state.increase_indent(...)` / `decrease_indent()`. Indentation is therefore **relative**: moving a block to another depth re-indents it without rewriting every line. `Module.default_indent` "is inferred from the contents" ([LibCST nodes][libcst-nodes]).
- **WASM.** The Rust crate's `pyo3` dependency is behind an optional `py` feature ([LibCST Cargo.toml][libcst-cargo]). No WASM build is documented. It is a design reference for Regia, not a dependency.

### 4.6 parso

- **Model.** Every leaf has a `prefix` of whitespace and comments. `get_code(include_prefix=...)` reprints ([parso tree.py][parso-tree]).
- **INDENT/DEDENT** are produced by the tokenizer but kept out of the tree: "We don't want the INDENT/DEDENT in our parser tree... They are virtual leaves... and no prefixes" ([parso parser.py][parso-parser]). Indentation then exists only as text in prefixes, which is absolute, not relative.
- **Incremental.** The diff parser "is trying to be a faster version of the normal parser by trying to reuse the nodes of a previous pass". It computes the changed range "by using difflib". Its author warns: "The biggest issue of this approach is that we reuse nodes in a mutable way" ([parso diff.py][parso-diff]).
- **WASM.** None (Python).

## 5. Indentation-sensitive grammars across approaches

Three questions decide how indentation works in a lossless tree.

**(a) Who produces INDENT/DEDENT?**
- A stateful lexer with an indent stack: parso, LibCST's tokenizer, tree-sitter external scanners, Lezer external tokenizer plus `ContextTracker`.
- In every case, blank lines, comment-only lines and bracketed regions must not change indentation. tree-sitter-python and `@lezer/python` both handle these explicitly ([ts-py-scanner], [lezer-py]).
- Regia's `## ... ##` block comments span lines and need the same exemption. Its optional `.` and `;` terminators decide whether a dedent or a terminator closes a block. The lexer must accept both without emitting a spurious DEDENT.

**(b) Are INDENT/DEDENT in the tree, and how wide are they?**
- parso drops them ([parso-parser]).
- LibCST turns them into the `IndentedBlock.indent` string ([libcst-stmt]).
- In a rowan or Roslyn-style tree, a common choice is zero-width INDENT/DEDENT tokens (or just block nodes), with the real leading whitespace stored as trivia. Losslessness holds because trivia carries all bytes.
- tree-sitter scanners decide token width themselves. Lezer's dedent uses negative length to avoid consuming text ([lezer-py]).

**(c) Absolute or relative indentation in the tree?**
- With absolute whitespace (whitespace trivia text as written, in rowan, Roslyn and parso), moving a block to a new depth requires a re-indent pass over its lines. rust-analyzer uses `IndentLevel` helpers for this.
- With relative indentation (LibCST), each block stores its own step and reprinting computes the absolute columns. Moves are trivial, but the tree is less "raw".
- Incremental reuse must respect the indent stack. tree-sitter serializes scanner state into the tree ([ts-ext]). Lezer hashes the context ([lezer-ref]). A hand-written incremental reparser (rowan style) is safest if it only reuses whole blocks whose starting indent column is unchanged.

## 6. Writing structured edits back to text

### 6.1 Patterns found

1. **Edit the tree, then print the whole tree.** Used by LibCST (`module.code`) and Roslyn (`ToFullString`). Untouched regions come out identical because their trivia is unchanged. To update Monaco, diff old and new text, or better, compute the replaced ranges from the edit, and apply them as `IIdentifiedSingleEditOperation`s.
2. **Edit the tree, emitting text edits only for changed regions.** rust-analyzer's `SyntaxEdit` exposes `changed_elements()` ([ra-editor]). recast "reprints only those parts of the syntax tree that you modify", tracking an `.original` shadow per node and falling back to a pretty-printer only for modified nodes ([recast README][recast]). This keeps user formatting by construction.
3. **Compute text splices from node byte ranges, then reparse.** This is the tree-sitter and Lezer path (§4.3). The edit logic must handle trivia ownership and indentation itself.
4. **Print and reparse to normalize, then match identities.** Enso's frontend AST (TypeScript, synced through Y.js) is fed by Enso's Rust parser compiled to WASM: the `rust-ffi` crate is a `cdylib` with `wasm-bindgen` pinned to `0.2.100` ([enso rust-ffi Cargo.toml][enso-ffi-cargo], [enso ffi.ts][enso-ffi]). Their design discussion argues: "Translating tree edits to text edits is complex", "maintaining the ID map correctly is difficult". It proposes a tree-structured canonical representation where, after any AST edit, "a print-parse process is used to normalize the modified subtree" ([enso #8233][enso-8233]). Their `syncToCode.ts` updates the AST "to match the given source code, while modifying it as little as possible". It finds equivalent nodes with a `syntaxHash` that "is invariant to metadata, including externalId", in "retained-code" and "movement" matching passes ([enso syncToCode.ts][enso-sync]). **This is the closest public analogue of Regia's Monaco and graph setup.**
5. **Projectional editing (no text).** In MPS, "your programs are always represented by an AST", "no parsing is necessary", and "the editor in MPS directly manipulates AST" ([MPS basic notions][mps]). Shown only for contrast. Regia keeps text as a first-class, user-owned view, so pure projection does not apply.
6. **Bidirectional transformations (lenses).** A lens pairs a forward function with a backward function that "takes a modified output plus the original input and returns a modified input" ([Harmony/Boomerang][harmony]; Foster et al., TOPLAS 29(3), 2007; Bohannon et al., POPL 2008). The CST is the "original input" that makes `put` keep formatting. Patterns 1 and 2 are informal lenses from graph to CST to text.
7. **Robust text-graph sync under errors.** van Rest, Wachsmuth, Steel, Süss and Visser, *Robust Real-Time Synchronization between Textual and Graphical Editors*, ICMT 2013. It "recovers from errors during parsing and text-to-model synchronization" and "preserves textual and graphical layout in the presence of erroneous texts and models" ([van Rest et al.][vanrest]).

### 6.2 Cross-cutting needs any option must meet

- **Stable node identity across reparses**, so graph positions and selection survive typing. Options:
  - Span or structural matching (Enso `syntaxHash` plus correspondence passes).
  - Annotations that survive tree edits (rust-analyzer `SyntaxAnnotation`, `find_element`).
  - Green-node pointer equality for unchanged shared subtrees.
- **Synthesizing trivia for new nodes**: Roslyn elastic trivia plus formatter ([roslyn-elastic]), rust-analyzer `insert_with_whitespace` ([ra-editor]), LibCST default fields plus `default_indent`.
- **Monaco integration.** Apply results as model edits so undo and cursors behave. Monaco's `ITextModel.pushEditOperations` is "the preferred way of editing the model. The edit operations will land on the undo stack". `ICodeEditor.executeEdits` behaves the same. `pushUndoStop()` groups one graph action into one undo step ([Monaco editor.api.d.ts][monaco-dts]).
- **Doc comments.** `#@` doc comments are kept as data today. In a token-attached model they could be leading trivia of a specific kind. In a LibCST-style model they could be a typed field. Or they could be real grammar nodes, as the Transpiler notes suggest. This affects whether the graph can show and edit them.

## 7. WASM fit, summarized

| Option | What runs in the browser | One grammar for transpiler and editor? | Evidence |
|---|---|---|---|
| Rust parser plus rowan-style tree (rowan, cstree, own fork) via `wasm-bindgen` | Regia's own Rust crate | Yes | rowan is pure Rust ([rowan-cargo]). Biome ships `@biomejs/wasm-web`. Enso ships a Rust parser to the browser via wasm-bindgen ([enso-ffi-cargo]) |
| tree-sitter grammar | `web-tree-sitter` plus `tree-sitter-regia.wasm` | Yes. Rust crate for the transpiler, wasm for the editor. But the tree-sitter CST is not editable, so the transpiler would still need its own AST lowering | [ts-web], [ts-wasm-stdlib] |
| Lezer grammar | JS | No. A second grammar | [lezer-guide] |
| LibCST or parso | — | — | Python-bound; neither documents a browser build ([libcst-cargo], [parso-docs]) |

Practical WASM points:
- **Boundary cost.** Passing a full tree across JS↔WASM per keystroke is expensive. Designs usually expose cursor or handle APIs, or serialize only what the graph needs (Enso translates the parser `Tree` into a GUI-specific representation, per [enso-8233]).
- **Toolchain pinning.** Enso pins `wasm-bindgen` exactly ([enso-ffi-cargo]). tree-sitter's ABI must match between the CLI-built `.wasm` and `web-tree-sitter`: 0.25+ supports ABI 13–15 ([ts-web]).

## 8. Open questions for the decision (not answered here)

1. **Model.** Should the CST be the edit model (rowan or Roslyn style, patterns 1 and 2), or a read-only index with text splices (tree-sitter or Lezer, pattern 3)?
2. **Trivia.** Sibling tokens, token-attached (rowan 0.18-alpha, Roslyn, Biome), or LibCST-style typed fields? Should rowan 0.18-alpha be adopted while it is still alpha?
3. **Indentation.** Absolute whitespace plus a re-indent helper, or relative indent per block like LibCST?
4. **Optional terminators.** How do `.` and `;` interact with DEDENT in the lexer and in losslessness?
5. **Identity.** Is it owned by the CST (annotations, pointers) or recomputed by matching after each reparse (the Enso style)?
6. **Doc comments.** Is `#@` trivia, a field, or a grammar node?
7. **Incremental reparsing.** Is it needed at all at Regia file sizes? rust-analyzer finds full reparses usually fast enough ([ra-syntax]).

## Sources

[ra-syntax]: https://github.com/rust-lang/rust-analyzer/blob/master/docs/book/src/contributing/syntax.md
[ra-editor]: https://github.com/rust-lang/rust-analyzer/blob/master/crates/syntax/src/syntax_editor.rs
[ra-edit-algo]: https://github.com/rust-lang/rust-analyzer/blob/master/crates/syntax/src/syntax_editor/edit_algo.rs
[ra-cargo]: https://github.com/rust-lang/rust-analyzer/blob/master/Cargo.toml
[rowan-cursor]: https://github.com/rust-analyzer/rowan/blob/master/src/cursor.rs
[rowan-token]: https://github.com/rust-analyzer/rowan/blob/master/src/green/token.rs
[rowan-api]: https://github.com/rust-analyzer/rowan/blob/master/src/api.rs
[rowan-cargo]: https://github.com/rust-analyzer/rowan/blob/master/Cargo.toml
[rowan-219]: https://github.com/rust-analyzer/rowan/pull/219
[rowan-prs]: https://github.com/rust-analyzer/rowan/pulls?q=is%3Apr+is%3Amerged
[crates-rowan]: https://crates.io/crates/rowan/versions
[biome-rowan]: https://github.com/biomejs/biome/tree/main/crates/biome_rowan/src
[biome-trivia]: https://github.com/biomejs/biome/blob/main/crates/biome_rowan/src/syntax/trivia.rs
[cstree]: https://github.com/domenicquirl/cstree
[lippert]: https://ericlippert.com/2012/06/08/red-green-trees/
[roslyn-syntax]: https://learn.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/work-with-syntax
[roslyn-elastic]: https://learn.microsoft.com/en-us/dotnet/api/microsoft.codeanalysis.csharp.syntaxfactory.elasticmarker
[roslyn-wct]: https://learn.microsoft.com/en-us/dotnet/api/microsoft.codeanalysis.syntaxtree.withchangedtext
[ts-adv]: https://tree-sitter.github.io/tree-sitter/using-parsers/3-advanced-parsing.html
[ts-api]: https://github.com/tree-sitter/tree-sitter/blob/master/lib/include/tree_sitter/api.h
[ts-dsl]: https://tree-sitter.github.io/tree-sitter/creating-parsers/2-the-grammar-dsl.html
[ts-ext]: https://tree-sitter.github.io/tree-sitter/creating-parsers/4-external-scanners.html
[ts-py-scanner]: https://github.com/tree-sitter/tree-sitter-python/blob/master/src/scanner.c
[ts-web]: https://github.com/tree-sitter/tree-sitter/blob/master/lib/binding_web/README.md
[ts-wasm-stdlib]: https://docs.rs/crate/tree-sitter/0.27.0/source/src/wasm-stdlib/README.md
[lezer-guide]: https://lezer.codemirror.net/docs/guide/
[lezer-ref]: https://lezer.codemirror.net/docs/ref/
[lezer-py]: https://github.com/lezer-parser/python/blob/main/src/tokens.js
[libcst-why]: https://libcst.readthedocs.io/en/latest/why_libcst.html
[libcst-nodes]: https://libcst.readthedocs.io/en/latest/nodes.html
[libcst-native]: https://github.com/Instagram/LibCST/blob/main/native/libcst/README.md
[libcst-stmt]: https://github.com/Instagram/LibCST/blob/main/libcst/_nodes/statement.py
[libcst-cargo]: https://github.com/Instagram/LibCST/blob/main/native/libcst/Cargo.toml
[parso-docs]: https://parso.readthedocs.io/en/latest/
[parso-tree]: https://github.com/davidhalter/parso/blob/master/parso/tree.py
[parso-parser]: https://github.com/davidhalter/parso/blob/master/parso/python/parser.py
[parso-diff]: https://github.com/davidhalter/parso/blob/master/parso/python/diff.py
[recast]: https://github.com/benjamn/recast/blob/master/README.md
[enso-8233]: https://github.com/enso-org/enso/discussions/8233
[enso-sync]: https://github.com/enso-org/enso/blob/develop/app/ydoc-shared/src/ast/syncToCode.ts
[enso-ffi]: https://github.com/enso-org/enso/blob/develop/app/ydoc-shared/src/ast/ffi.ts
[enso-ffi-cargo]: https://github.com/enso-org/enso/blob/develop/app/rust-ffi/Cargo.toml
[mps]: https://www.jetbrains.com/help/mps/basic-notions.html
[harmony]: https://www.engineering.upenn.edu/~harmony/
[vanrest]: https://eelcovisser.org/blog/2013/03/24/robust-real-time-synchronization-between-textual-and-graphical-editors/
[monaco-dts]: https://unpkg.com/monaco-editor@0.52.2/esm/vs/editor/editor.api.d.ts

- rust-analyzer, *Syntax in rust-analyzer*: [ra-syntax]
- rust-analyzer `SyntaxEditor`: [ra-editor], [ra-edit-algo]; workspace `Cargo.toml` (rowan 0.18.0-alpha.2): [ra-cargo]
- rowan source: [rowan-cursor], [rowan-token], [rowan-api], [rowan-cargo]; PRs #215–#222 (mutable API removed, trivia on tokens): [rowan-prs], [rowan-219]; versions: [crates-rowan]
- Biome `biome_rowan`: [biome-rowan], [biome-trivia]; cstree: [cstree]
- Eric Lippert, *Persistence, façades and Roslyn's red-green trees* (2012): [lippert]
- Microsoft Learn, Roslyn syntax model: [roslyn-syntax]; `ElasticMarker`: [roslyn-elastic]; `WithChangedText`: [roslyn-wct]
- tree-sitter docs and source: [ts-adv], [ts-api], [ts-dsl], [ts-ext], [ts-web], [ts-wasm-stdlib]; tree-sitter-python scanner: [ts-py-scanner]
- Lezer: [lezer-guide], [lezer-ref], `@lezer/python` tokens: [lezer-py]
- LibCST: [libcst-why], [libcst-nodes], [libcst-native], [libcst-stmt], [libcst-cargo]
- parso: [parso-docs], [parso-tree], [parso-parser], [parso-diff]
- recast: [recast]
- Enso: [enso-8233], [enso-sync], [enso-ffi], [enso-ffi-cargo]
- JetBrains MPS: [mps]
- Foster, Greenwald, Moore, Pierce, Schmitt, "Combinators for bidirectional tree transformations", ACM TOPLAS 29(3), 2007; Bohannon, Foster, Pierce, Pilkiewicz, Schmitt, "Boomerang: Resourceful Lenses for String Data", POPL 2008 (both as listed at [harmony])
- van Rest, Wachsmuth, Steel, Süss, Visser, "Robust Real-Time Synchronization between Textual and Graphical Editors", ICMT 2013: [vanrest]
- Monaco `editor.api.d.ts` (0.52.2): [monaco-dts]
- Package versions checked 2026-11-03 on npm, PyPI and crates.io: web-tree-sitter 0.27.1, @lezer/lr 1.4.12, @lezer/python 1.1.19, @biomejs/wasm-web 2.6.4, libcst 1.9.0, parso 0.8.7, rowan 0.18.0-alpha.2 (latest stable 0.17.0), cstree 0.14.0.
