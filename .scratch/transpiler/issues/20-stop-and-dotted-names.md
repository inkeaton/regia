# Scan: STOP and dotted names

Type: implementation
Status: open
Assignee:
Blocked by: 19

## Goal

`scan` tells a `.` ending a Statement (STOP) from a dotted name by the character after it, and a dotted name is one token.

## Spec

Chapter 01, *When `.` ends a Statement*: STOP when followed by whitespace, a line break, the end of the file, `;` or `#`. Chapter 23: a dotted name is one token. `complain.SIGNAL` is one dotted name here; its `R01_02-keyword-in-dotted-name` is the parser's.

## Rust

Book ch 6.1 and 6.3: `Option` from `get(i + 1)` to look ahead without going out of bounds, `if let`, and why there is no null.

## Test first

Unit tests: `DO complain.` (NAME, STOP), `DO complain. SIGNAL x`, `engine.security.summon_guards` (one token), `DO complain.SIGNAL x` (one dotted name), `x.;` and `x.#c`.

## Done when

The tests pass; the four checks are clean.

## Not here

Numbers with a `.` (next ticket).
