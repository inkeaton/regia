# Layout: NEWLINE ends a logical line

Type: implementation
Status: open
Assignee:
Blocked by: 26

## Goal

`layout` takes `scan`'s tokens and adds NEWLINE; `lex` is `scan` then `layout`.

## Spec

Chapter 23, *What the lexer hands to the parser*: NEWLINE ends a logical line; breaks on blank and comment-only lines are whitespace; at the end of a file without a final break, NEWLINE is zero-width. Implementation note from *Review: text to tokens*: `layout` reads past comments to the next code line before it places a token.

## Rust

Book ch 8.1 and ch 4 together: `layout` takes the `Vec` by value and returns a new one; iterating by value against by reference, and what the move costs (nothing is copied).

## Test first

Dump snapshots: two code lines with a blank and a comment-only line between them; a file without a final break.

## Done when

The tests pass; print-back still holds; the four checks are clean.

## Not here

Continuation lines; INDENT and DEDENT.
