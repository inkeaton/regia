# Scan: Placeholders, punctuation and operators

Type: implementation
Status: open
Assignee:
Blocked by: 18

## Goal

`?h`, `?_h` and `?` are one token each; `:`, `;`, `,`, `(`, `)` and every operator have kinds.

## Spec

Chapter 01, *Names, Strings and characters*; chapter 03 (Placeholders, no space after `?`); chapter 04 (operators: `+ - * /`, `= != < > <= >=`; `%` of a share, chapter 15). Chapter 23: a `-` is always its own token. `.` is the next ticket.

## Rust

Book ch 6.2 patterns: `|` and ranges such as `b'a'..=b'z'` in a `match` (ranges are ch 19, met here early).

## Test first

A dump snapshot of `?h-10 <= ?_x, (?)` and unit tests for `? x` (a lone `?` then a name) and `!` alone (`R01_12-stray-character`).

## Done when

The tests pass; the four checks are clean.

## Not here

Joining `-` to a number: the parser's.
