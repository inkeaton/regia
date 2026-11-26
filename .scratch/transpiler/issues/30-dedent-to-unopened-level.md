# Layout: a dedent to an unopened level is R0104

Type: implementation
Status: open
Assignee:
Blocked by: 29

## Goal

A line dedented to a level that was never opened is `R0104`, and belongs to the Block outside.

## Spec

Chapter 01, *Indentation rules*, `R0104`. The case `01-statements-and-blocks/dedent-to-unopened-level.regia` exists; it runs from M3.

## Rust

No new concept: adding a `Code` and testing a recovery.

## Test first

A unit test on the case's text: one `R0104` on the right line, and the tokens after it as if the line were at the outer level.

## Done when

The test passes; the four checks are clean.

## Not here

`R0103`'s silencing of it.
