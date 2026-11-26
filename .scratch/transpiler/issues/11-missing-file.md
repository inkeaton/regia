# A missing file is an error

Type: implementation
Status: open
Assignee:
Blocked by: 10

## Goal

No argument, or a file that cannot be read, gives a message on standard error and exit status 1.

## Spec

Chapter 23, *The command line* (exit status).

## Rust

Book ch 6.1–6.2, ahead of its place: `match`, here on a `Result`. New concept: `match` as an expression.

## Test first

Two integration tests, one per failure, checking the exit status and that standard output is empty.

## Done when

Both tests pass; no `expect` or `unwrap` on this path.

## Not here

`?` and error types (M2); Diagnostics.
