# Layout: continuation lines

Type: implementation
Status: open
Assignee:
Blocked by: 27

## Goal

A line ending in `,` or with a `(` still open continues onto the next, and the break between them is whitespace.

## Spec

Chapter 01, *Continuation lines*: the joining part only. The indentation rule and `R0105` are a later ticket.

## Rust

Book ch 5.3: `layout`'s state (open `(` count, last code token) as a struct with `&mut self` methods, instead of loose variables.

## Test first

A dump snapshot of chapter 01's `WHEN hates(?h) LEARNED, …` example, and unit tests for `f(a,` / `b)` and a `,` before a comment.

## Done when

The tests pass; the four checks are clean.

## Not here

`R0105`.
