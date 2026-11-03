# Research: lossless syntax trees and round-tripping

Type: research
Status: resolved

## Question

What are the established ways to build a lossless concrete syntax tree that keeps whitespace and comments and can be printed back to identical source, while supporting incremental edits from a visual editor? Look at rust-analyzer's rowan, Roslyn red-green trees, tree-sitter, Lezer, and how editors apply structured edits back to text (bidirectional or projectional editing). Also cover indentation-sensitive grammars. This is input for Regia's bidirectional Visual Editor (primer ch.6, ch.7).

## Comments

Research running on throwaway branch `research/lossless-cst` (file `research/lossless-cst.md`). Never merged.

## Answer

Full findings are on branch `research/lossless-cst`, file `research/lossless-cst.md`.

- **The one rule:** every lossless design guarantees that concatenating all tokens, whitespace and comments in order gives back the exact source, even for invalid code (rust-analyzer, Roslyn, LibCST, parso).
- **Where whitespace and comments go:** as separate sibling tokens (rowan ≤0.17, tree-sitter), as leading/trailing parts of each token (Roslyn, Biome, rowan 0.18-alpha), as named fields on typed nodes (LibCST), or as a prefix string on each leaf (parso).
- **rowan:** the mutable API was removed in 0.17.0 (Aug 2026). 0.18.0-alpha moved comments and whitespace onto tokens, and rust-analyzer's Roslyn-style `SyntaxEditor` is now the way to edit. Still alpha.
- **Inserting nodes:** Roslyn's "elastic trivia" are empty placeholders that a formatter fills later. This is the standard way to insert a node without disturbing formatting elsewhere.
- **tree-sitter and Lezer:** excellent incremental parsing, but their trees only store byte ranges and have no edit API. Graph edits mean patching text and reparsing, with comment ownership and re-indenting left to us. Lezer would need a second grammar.
- **Indentation:** INDENT/DEDENT always come from a lexer with an indent stack that skips blank lines, comment-only lines and brackets. LibCST stores indentation relative to each block, so moving a block re-indents it for free.
- **Closest real case:** Enso, a Rust parser in WASM behind a TypeScript tree. After an edit it prints and reparses, then re-matches node identities by structural hash. recast shows the "reprint only what changed" approach.
- **WASM:** a Rust parser with a rowan-style tree (Biome) or tree-sitter (`web-tree-sitter`) both let one grammar serve the Transpiler and the editor.
- **Monaco:** `pushEditOperations` plus `pushUndoStop` makes one graph action a single undo step.
- **Open questions** (now [Bidirectional editing model](27-bidirectional-editing-model.md)): CST as edit model vs read-only index, comment model, absolute vs relative indentation, optional `.`/`;` vs DEDENT, node identity, where `#@` doc comments live, whether incremental parsing is needed at all.
