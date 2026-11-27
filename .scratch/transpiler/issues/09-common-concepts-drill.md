# Drill: variables, functions, control flow

Type: exercise
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 08

## Goal

Be at ease with Rust that has no ownership questions in it yet.

## Spec

None.

## Rust

Book ch 2–3: shadowing, integer types, expressions and statements, `loop`/`while`/`for`. Compare with Python and C++.

## Test first

Tests given in `docs/.dev/exercises/ch03_common_concepts/`: three functions, one counting the leading columns of a line.

## Done when

The tests pass and clippy is clean.

## Not here

Ownership (`String` against `&str`): M1.

## Resolution

Done on 2026-11-27. `docs/.dev/exercises/ch03_common_concepts/` holds `leading_columns`, `line_and_column` (1-based line and character column of a byte offset, as chapter 23's CLI shows them) and `dedents` (open blocks a line closes, a preview of ticket 29). 20 tests in `tests/drill.rs`, named after the function they test so `cargo test <fn>` selects them; all pass, clippy clean. Met along the way: `offset` counts bytes while `chars()` gives characters (`len_utf8`, `char_indices`), and `&&` guarding an index against `usize` underflow.
