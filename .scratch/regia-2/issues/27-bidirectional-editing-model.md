# Bidirectional editing model

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 01, 02, 26

## Question

How do edits on the Visual Editor's graph become edits to the Regia source? Building on the lossless-CST research (24), decide:
- Is the CST the model that edits are made on, or a read-only index used to patch text and reparse?
- Comment model: who owns a plain comment (leading/trailing trivia on tokens vs separate siblings). Doc comment attachment at the language level is settled in [Comment syntax](02-comment-syntax.md): directly above the declaration, no blank line.
- Indentation: absolute or relative to each block, and how optional `.`/`;` interact with DEDENT.
- Node identity across reparses: kept stable, or matched by structural hash as in Enso.
- How inserted nodes get formatted (elastic placeholders plus a formatter?).
- Is incremental parsing needed at all at Regia file sizes?

## Comments

- From Statement and block syntax: indentation and explicit `.`/`;` styles mix freely, and redundant terminators are allowed. Decide whether write-back preserves the user's style or normalises it.
- From [Implementation language for the Transpiler](26-implementation-language.md): Rust, with a hand-written lexer that keeps whitespace and comments as tokens, and a recursive-descent parser that marks where nodes start and finish (ADR 0010). Still open: rowan (0.17, no mutable API; 0.18-alpha with trivia on tokens and rust-analyzer's `SyntaxEditor`) or our own tree, and which form trivia takes. That ties into the comment-ownership question above. lelwel's tree is a reference.

## Answer

Spec: `docs/spec/22-bidirectional-editing.md`. ADR 0011.

- **Model:** the text is the only source of truth, and the syntax tree is a read-only index (option (a)). A graph action calls a domain edit operation in the Rust core (add a Phase, move a construct, ...). The core returns text edits per file, and the Visual Editor applies them with `pushEditOperations` + `pushUndoStop`, so one graph action is one undo step. Then every changed file is reparsed in full. The Visual Editor reads spans only for highlighting and selection, and never builds edits from them.
- **The tree as edit model** (option (b), Roslyn/`SyntaxEditor` style) was preferred but postponed for cost. Switching later only replaces the code inside the core that computes text edits. The operation API, the per-file text edits, the ownership rules and the before/operation/after tests all stay.
- **Comments (Extent):** comment lines directly above a construct (no blank line) and a same-line trailing comment belong to it. Comment lines at the end of a Block body, before the dedent, belong to that Block. Anything set apart by a blank line belongs to nothing and stays put. Ownership is structural: the tree builder puts owned comments inside the node, and doc comments become the declaration's first children.
- **Style:** text an edit doesn't touch is kept byte for byte, redundant `.`/`;` included. New constructs use indentation style, one Statement per line, no redundant terminators. Adding to an Inline block first expands the smallest enclosing Inline block. No normalising. A formatter is a separate concern.
- **Indentation:** absolute, as written. Each file has an indent unit (its first indented line, or 4 spaces). A moved extent shifts line by line, continuation lines and `#[ ]#` contents included.
- **Tree:** lossless; zero-width INDENT/DEDENT, leading whitespace as a token; `.`/`;` are tokens inside the node they end. rowan 0.17, wrapped in the core's own `syntax` module. Revisit 0.18 when it is stable.
- **Identity:** nothing stored. A structural key (`Plot/Phase/WHEN e#n`) is recomputed on every parse.
- **Incremental parsing:** not needed. Full reparse, debounced, with a performance budget checked in development (for example 5,000 lines in under 16 ms in WASM).
- **Broken source:** the graph draws from the latest tree. Constructs whose extent holds an error can't be edited from the graph. Edits are computed against the current text, reparsing first if the text is stale.
- **Left open:** which edit operations exist, and where a new declaration lands (for example an Event a new transition needs). Moved to the "What the graph shows" fog.
