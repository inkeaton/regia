# Layout: a continuation line not indented further is R0105

Type: implementation
Status: open
Assignee:
Blocked by: 30

## Goal

A continuation line not indented further than its logical line's first line is `R0105`, and starts a new logical line with any open `(` forgotten.

## Spec

Chapter 01, *Continuation lines*: a missing `)` or a stray `,` never swallows the rest of the file, and what the broken line lacks is not reported too. *Review: text to tokens*, *Recovery*. Write the case `01-statements-and-blocks/continuation-not-indented.regia` first; it runs from M3.

## Rust

No new concept.

## Test first

Unit tests: a forgotten `)` followed by an unindented Plan (one `R0105`, no other Diagnostic, the Plan's tokens as usual); a trailing `,` likewise.

## Done when

The tests pass; the four checks are clean.

## Not here

`R0103`'s silencing of it.
