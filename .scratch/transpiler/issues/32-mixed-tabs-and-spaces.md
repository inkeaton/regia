# Layout: tabs and spaces mixed is R01_03-mixed-tabs-and-spaces

Type: implementation
Status: open
Assignee:
Blocked by: 31

## Goal

The first indented line fixes tabs or spaces for the file; indenting with the other is `R01_03-mixed-tabs-and-spaces`, once per file, after which `R01_04-dedent-to-unopened-level` and `R01_05-continuation-not-indented` are not reported in that file.

## Spec

Chapter 01, *Indentation rules*: continuation lines count, comment-only lines don't. *Review: text to tokens*, *Recovery*: a line further indented still continues. Write the case `01-statements-and-blocks/tabs-and-spaces-mixed.regia` first; it runs from M3.

## Rust

Book ch 6: an `Option` of a two-variant enum (`Indent::Tabs`, `Indent::Spaces`) for "not decided yet".

## Test first

Unit tests: one `R01_03-mixed-tabs-and-spaces` for two bad lines; a file that would also give `R01_04-dedent-to-unopened-level` gives only `R01_03-mixed-tabs-and-spaces`; a tab-indented comment in a space-indented file gives nothing.

## Done when

The tests pass; the four checks are clean.

## Not here

Indentation after a multiline comment (next ticket).
