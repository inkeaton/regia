# Layout: INDENT and DEDENT

Type: implementation
Status: open
Assignee:
Blocked by: 28

## Goal

An indent stack adds INDENT and DEDENT, balanced at the end of the file, placed around comments as chapter 22 says.

## Spec

Chapter 23: INDENT and DEDENT follow code lines only; a deeper line is an INDENT whether or not a header came before it. Chapter 01, *Indentation rules*: each tab or space is one column. Chapter 22, *Which Block a comment is in*: a comment is in the deepest open Block no deeper than its column, never shallower than the next code line.

## Rust

Book ch 8.1: a `Vec<usize>` as a stack, `last()` giving an `Option<&usize>`, and `while let` to pop several levels (`while let` is ch 19, met here early).

## Test first

A dump snapshot of chapter 23's example (`WHEN food_served:` … `WHEN idle:`), and one with two dedents at once and the end of the file closing every level.

## Done when

The snapshots match chapter 23's example; INDENT and DEDENT balance in every test; the four checks are clean.

## Not here

Dedent errors and mixed tabs (next tickets).
