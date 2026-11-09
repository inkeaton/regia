# Research: grammar-driven parsing in Rust

Type: research
Status: resolved

## Question

Which Rust tools let Regia's parser be generated or mostly derived from a grammar file, the way 1.0 used Lark, while still meeting the 2.0 parser requirements? Requirements: a lossless syntax tree (every token, whitespace and comment kept; the source prints back exactly, including invalid input), several errors reported per run with recovery, an indentation-sensitive grammar (INDENT/DEDENT from an indent stack) mixed with optional `.`/`;` terminators, a `.` that ends a Statement only before a space or end of line, nestable `#[ … ]#` comments, compiling to `wasm32-unknown-unknown`, and low effort when the grammar changes. Candidates include lelwel, tree-sitter (with Rust bindings and its external scanner; also typed wrappers such as type-sitter or rust-sitter), lalrpop plus logos, pest, chumsky, and the rust-analyzer approach (ungrammar/codegen for syntax kinds and typed AST over a hand-written parser). For each: maturity and maintenance in 2026, how lossless trees and error recovery are done, how indentation is handled, wasm support, and how much is still hand-written. Input for [Implementation language for the Transpiler](26-implementation-language.md).

## Comments

Research ran on throwaway branch `research/grammar-driven-parsing-rust` (file `research/grammar-driven-parsing-rust.md`). Never merged.

## Answer

Full findings are on branch `research/grammar-driven-parsing-rust`, file `research/grammar-driven-parsing-rust.md`. The note lays out the options without deciding. Nothing was compiled, because no Rust toolchain was available.

- **The lexer is hand-written whatever we pick.** No tool generates Regia's indent stack, line continuation, nestable `#[ ]#` or doc-comment placement. That is about 200–400 lines of Rust; the tools only change where it lives.
- **`;` closing nested Inline blocks** is a dangling-else ambiguity. lelwel resolves it with a `?t` predicate; LR generators report a conflict.
- **lelwel** (0.10.4, 2026-04, still active) fits best. It generates resilient LL(1) recursive-descent parsers from a `.llw` grammar, with a lossless tree of its own (not rowan), automatic multi-error recovery and a grammar language server. Its repo has a Python example with an INDENT/DEDENT lexer, and its playground runs as wasm. Risks: one maintainer, pre-1.0, 3 dependents. The generated code can be vendored.
- **tree-sitter** (0.27.2) is the most mature and the only incremental parser. But all the lexing goes in a C scanner, it produces no error messages, and the tree stores whitespace only as byte ranges. Typed wrappers are weak: type-sitter is alpha and rust-sitter is stale.
- **lalrpop + logos** and **grmtools**: active, but the lossless tree is all hand-written action code. lalrpop recovery is manual; grmtools has the best automatic LR recovery.
- **pest** stops at the first error. **chumsky** has no grammar file (combinators in Rust code).
- **The rust-analyzer approach** (ungrammar codegen for kinds and the typed AST, with a hand-written parser) is the proven end state and a fallback, but the parser itself isn't generated. `ungrammar` is archived.
- **parol** (5.0.4) is worth a short trial; whether its tree is lossless and how its recovery works is unverified.
- **Suggested check:** parse the spec chapter 1 and 2 examples, print them back byte for byte, get two errors from one file, and build for `wasm32-unknown-unknown`.
