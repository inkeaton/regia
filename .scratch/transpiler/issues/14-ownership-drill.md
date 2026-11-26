# Drill: ownership, borrowing and slices

Type: exercise
Status: open
Assignee:
Blocked by: 11

## Goal

Know who owns a piece of text before the lexer starts slicing one.

## Spec

None.

## Rust

Book ch 4: moves, `clone`, references and `&mut`, the rules of references, string slices. Compare with C++ (`std::move`, `const&`, `std::string_view`) and Python (everything shared).

## Test first

Tests given in `docs/.dev/exercises/ch04_ownership/`: a function returning the first word of a line as `&str`, one returning a line's leading whitespace as `&str`, and one program that must be fixed by reading the borrow checker's error.

## Done when

The tests pass, clippy is clean, and each fix to the broken program is explained back.

## Not here

Lifetimes in signatures (ch 10): every function here takes one `&str` and returns a slice of it, so elision covers it.
