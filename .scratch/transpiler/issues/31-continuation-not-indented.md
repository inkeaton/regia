# Layout: a continuation line not indented further is R01_05-continuation-not-indented

Type: implementation
Status: open
Assignee:
Blocked by: 30

## Goal

A continuation line not indented further than its logical line's first line is `R01_05-continuation-not-indented`, and starts a new logical line with any open `(` forgotten.

## Spec

Chapter 01, *Continuation lines*: a missing `)` or a stray `,` never swallows the rest of the file, and what the broken line lacks is not reported too. *Review: text to tokens*, *Recovery*. Write the case `01-statements-and-blocks/continuation-not-indented.regia` first; it runs from M3.

## Rust

No new concept.

## Test first

Unit tests: a forgotten `)` followed by an unindented Plan (one `R01_05-continuation-not-indented`, no other Diagnostic, the Plan's tokens as usual); a trailing `,` likewise.

## Done when

The tests pass; the four checks are clean.

## Not here

`R01_03-mixed-tabs-and-spaces`'s silencing of it.
