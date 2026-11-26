# Layout: tabs and spaces mixed is R0103

Type: implementation
Status: open
Assignee:
Blocked by: 31

## Goal

The first indented line fixes tabs or spaces for the file; indenting with the other is `R0103`, once per file, after which `R0104` and `R0105` are not reported in that file.

## Spec

Chapter 01, *Indentation rules*: continuation lines count, comment-only lines don't. *Review: text to tokens*, *Recovery*: a line further indented still continues. Write the case `01-statements-and-blocks/tabs-and-spaces-mixed.regia` first; it runs from M3.

## Rust

Book ch 6: an `Option` of a two-variant enum (`Indent::Tabs`, `Indent::Spaces`) for "not decided yet".

## Test first

Unit tests: one `R0103` for two bad lines; a file that would also give `R0104` gives only `R0103`; a tab-indented comment in a space-indented file gives nothing.

## Done when

The tests pass; the four checks are clean.

## Not here

Indentation after a multiline comment (next ticket).
