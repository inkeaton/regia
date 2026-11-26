# Scan: names and every reserved word

Type: implementation
Status: open
Assignee:
Blocked by: 15

## Goal

A name is a NAME token, and each reserved word is a kind of its own.

## Spec

Chapter 01, *Names, Strings and characters* and *Reserved words*: the 2.0, later and retired words get kinds too (chapter 23: context never decides whether a word is a keyword). Keywords are matched exactly: `when` is a name. `BELIEVE` and the other dropped 1.0 words are names.

## Rust

Book ch 6.1–6.2: an enum with many variants, `match` on a `&str` to pick the kind, exhaustiveness. A small drill first: an enum and a `match` with no lexer in it.

## Test first

Unit tests: `WHEN`, `when`, `EVENT`, `TOLD`, `BELIEVE` and `food_served` get the kinds above.

## Done when

The tests pass; every word of *Reserved words* has a kind, checked by counting against the list; the four checks are clean.

## Not here

Dotted names (a later ticket); `R0110`, which isn't the lexer's.
