# Scan: whitespace and line breaks

Type: implementation
Status: open
Assignee:
Blocked by: 14

## Goal

`scan(text: &str) -> Vec<Token>` exists in `regia-cli` and knows three kinds: whitespace, a line break, and ERROR for everything else.

## Spec

Chapter 23, *What the lexer hands to the parser* (`scan` knows nothing about lines). Chapter 01, *Names, Strings and characters*: a line ends with `\n` or `\r\n` (one token), and a byte order mark at the start is ignored but kept, so print-back holds.

## Rust

Book ch 5: a struct (`Token { kind, range }`), `#[derive(Debug, PartialEq)]`, a method `text(&self, source: &str) -> &str`. The kind is a fieldless enum, used here and taught properly in the next ticket (ch 6). The lexer lives in `regia-cli` for now, until *The lexer moves into `regia-core`*.

## Test first

Unit tests (a preview of ch 11): `"a \r\n"` gives ERROR, whitespace, one line break, with their ranges; and the texts of all tokens joined give back the input.

## Done when

The tests pass; the four checks are clean; `Token`'s doc comment follows `comments-rust.md`.

## Not here

Diagnostics (`R01_12-stray-character` comes later); names; NEWLINE, which is `layout`'s.
