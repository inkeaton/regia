# Scan: numbers and R0401

Type: implementation
Status: open
Assignee:
Blocked by: 20

## Goal

`3`, `0.5` and `10` are NUMBER tokens; a number in a form Regia doesn't have is a NUMBER with `R0401`.

## Spec

Chapter 04, `R0401`: `.5`, an exponent, digit separators, another base. Chapter 23: malformed text keeps the kind it was meant to have (`0xFF` is a number). Write the case `04-numbers-and-expressions/number-in-a-form-regia-lacks.regia` first (format: chapter 27); it runs from M3.

## Rust

No new concept: practice of ch 6 (`match`, `Option`), and of keeping a function short by splitting it.

## Test first

Unit tests: `0.5` (one NUMBER), `1.` (NUMBER, STOP), `0xFF`, `1e3`, `1_000` (one NUMBER and one `R0401` each), `.5` (`R0401`).

## Done when

The tests and the case's lines agree; the four checks are clean.

## Not here

Negative numbers (`-` stays a token of its own).
