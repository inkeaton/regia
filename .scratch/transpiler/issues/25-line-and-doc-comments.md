# Scan: line comments, doc comments and R02_02-doc-comment-mid-line

Type: implementation
Status: open
Assignee:
Blocked by: 24

## Goal

`# …` and `#@key …` are comment tokens up to the end of the line, and a doc comment that doesn't start its line is `R02_02-doc-comment-mid-line`.

## Spec

Chapter 02, *Plain comments* and *Doc comments*; `R02_02-doc-comment-mid-line`. A line starting with `##` is a plain comment. Write the case `02-comments/doc-comment-after-code.regia` first; it runs from M3.

## Rust

Book ch 8.2: `starts_with`, `find` and slicing on a `&str`.

## Test first

Unit tests: `DO x # note`, `#@doc text`, `## heading`, `DO x #@doc late` (`R02_02-doc-comment-mid-line`), and a STOP before `#`.

## Done when

The tests pass; the four checks are clean.

## Not here

Multiline comments (next ticket); which Block a comment is in (layout and the tree builder).
