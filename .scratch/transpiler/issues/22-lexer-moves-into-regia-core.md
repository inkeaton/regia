# The lexer moves into regia-core

Type: implementation
Status: open
Assignee:
Blocked by: 21

## Goal

`transpiler/crates/regia-core` exists as a library, the lexer is its `syntax` module and `enum Code` its `diagnostics` module, and `regia-cli` depends on it.

## Spec

Chapter 23, *Crates*: `regia-core` has no file I/O and no global state. Its public surface is what the parser will need: `scan`, `Token`, the kinds, `Diagnostic`, `Code`.

## Rust

Book ch 7: packages and crates, modules in their own files, `pub` on structs and enums, `use` paths, a path dependency between workspace members.

## Test first

The unit tests and the snapshot move with the code and stay green; a doc test (a preview of ch 14) shows `scan` from outside the crate.

## Done when

Nothing of the lexer is left in `regia-cli`; the crate opts into the workspace lints; the four checks are clean; the crate and module doc comments follow `comments-rust.md`.

## Not here

The `wasm32-unknown-unknown` check: added by the ticket that adds rowan.
