# Scan: Strings and R01_13-malformed-string

Type: implementation
Status: open
Assignee:
Blocked by: 23

## Goal

`"…"` is one STRING token, and a non-ASCII character outside a String or comment is one ERROR token.

## Spec

Chapter 01, *Names, Strings and characters*: one line, escapes `\"` and `\\` only, any Unicode inside. `R01_13-malformed-string`: not closed on its line, or another escape. Chapter 23: an unclosed String is a String up to the end of its line. Write the case `01-statements-and-blocks/unclosed-string.regia` first; it runs from M3.

## Rust

Book ch 8.2: a `&str` is UTF-8, so a range must fall on a character boundary; `char_indices` to step over a whole character.

## Test first

Unit tests: `"hi \"you\""` (one STRING), `"café"`, `"open` then a line break (STRING to the end of the line, `R01_13-malformed-string`), `"a\n"` (`R01_13-malformed-string`), `é` alone (one ERROR, `R01_12-stray-character`).

## Done when

The tests pass; every token's text is a valid slice; the four checks are clean.

## Not here

What a String means (the Model's).
