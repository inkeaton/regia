# Scan: multiline comments and R0201

Type: implementation
Status: open
Assignee:
Blocked by: 25

## Goal

`#[ … ]#` and `#@key[ … ]#` are one comment token each, nesting, and an unclosed one is `R0201` at its opener.

## Spec

Chapter 02: multiline comments nest, every opener (`#[`, `#@key[`) counts a level, and code after `]#` carries on. Chapter 23: an unclosed comment is a comment up to the end of the file. Write the case `02-comments/unclosed-multiline-comment.regia` first; it runs from M3.

## Rust

Book ch 8.1: a `Vec` of opener positions as a stack, so `R0201` can point at the opener left open.

## Test first

Unit tests and a dump snapshot: a comment across lines, `#[ a #[ b ]# c ]# DO x`, an unclosed nested one (`R0201` at the outer opener).

## Done when

The tests pass; the four checks are clean.

## Not here

Indentation after a multiline comment (a layout ticket).
