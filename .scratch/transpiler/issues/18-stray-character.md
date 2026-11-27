# A stray character is R01_12-stray-character

Type: implementation
Status: open
Assignee:
Blocked by: 17

## Goal

`scan` returns its Diagnostics in a list beside the tokens, and the first one is `R01_12-stray-character`.

## Spec

Chapter 01, `R01_12-stray-character`; chapter 23, *What the lexer hands to the parser*: a stray character is an ERROR token, which the parser steps over silently, so the mistake is reported once. Chapter 23, *Diagnostics*: `enum Code` (*Review: Diagnostics and where checks live*). The case `01-statements-and-blocks/bad-character-reported-once.regia` exists; it runs from M3.

## Rust

Book ch 6.1 again: `enum Code` holding only `R01_12-stray-character` for now, and a `Diagnostic` struct. Returning two lists from one function: a struct (`Lexed { tokens, diagnostics }`) rather than a tuple, and why.

## Test first

A unit test: `DO $glare` gives one `R01_12-stray-character` at the `$`, and the `$` is an ERROR token.

## Done when

The test passes; the dump shows the ERROR token; the four checks are clean.

## Not here

Non-ASCII stray characters (they need ch 8, in *Scan: Strings and R01_13-malformed-string*); rendering Diagnostics.
