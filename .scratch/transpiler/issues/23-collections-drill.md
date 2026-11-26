# Drill: vectors, Strings and hash maps

Type: exercise
Status: open
Assignee:
Blocked by: 22

## Goal

Be at ease with `Vec`, `String` and UTF-8, and `HashMap`, before Strings and comments are scanned.

## Spec

None.

## Rust

Book ch 8: a `Vec` as a stack, iterating by reference and by value, why `s[0]` doesn't compile, `chars` and `char_indices`, `is_char_boundary`, the entry API. Performance note: `Vec::with_capacity` (perf-book, *Heap Allocations*).

## Test first

Tests given in `docs/.dev/exercises/ch08_collections/`: balancing brackets with a `Vec` stack, cutting a `&str` at a character boundary, counting words with a `HashMap`.

## Done when

The tests pass and clippy is clean.

## Not here

Iterator adaptors (ch 13, M5).
