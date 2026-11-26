# Layout: indentation after a multiline comment

Type: implementation
Status: open
Assignee:
Blocked by: 32

## Goal

Code after a multiline comment that started its line has the indentation of the line the comment opened on.

## Spec

Chapter 01, *Indentation rules*, last item; chapter 02 (the lines a multiline comment spans don't count for indentation).

## Rust

No new concept.

## Test first

Dump snapshots: `#[ … ]# DO x` across three lines inside a Block, and a multiline comment between two Plans.

## Done when

The tests pass; the four checks are clean.

## Not here

Which Block the comment belongs to (the tree builder's).
