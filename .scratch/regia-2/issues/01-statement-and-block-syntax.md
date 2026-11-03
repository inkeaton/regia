# Statement and block syntax

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo

## Question

How are statements ended and blocks opened and closed in 2.0? Primer ch.1 proposes mandatory indentation, with `.` (explicit statement end) and `;` (explicit block end) as an alternative for writing on one line, and `,` for writing several things at once. Decide: are indentation and explicit terminators both allowed, and can they be mixed? Should `.` and `;` swap roles? Are special cases like IF/ELSE allowed without `;`? Can a `,`-separated list span lines without indentation? Does the `PLOT` header take a `:` like every other block?

## Answer

Spec chapter: `docs/spec/01-statements-and-blocks.md`. Glossary entries added: Block, Block header, Inline block.

- **Two styles, freely mixed:** indentation (one line is one Statement, `:` plus indented body) and explicit (`.` ends a Statement, `;` closes a Block). The primer's roles for `.` and `;` are kept, not swapped.
- **Every Block header ends with `:`**, `PLOT` included.
- **A Block's style depends on where its body starts:** next line, indented, means an indentation Block. Same line means an Inline block, which ends at `;` or at the end of the line and never spans lines. IF/ELSE needs no special case.
- **A Block header ending a line inside an Inline block is an error.**
- **`.` ends a Statement only before a space, the end of the line, or `;`.** Anywhere else it belongs to a dotted name or a number.
- **Redundant `.` or `;` at the end of a line** is allowed silently.
- **Indentation follows Python's rules:** consistent tabs or spaces per file, no dedent to a level never opened, blank and comment lines ignored.
- **Continuation:** a trailing `,` or an open `(` continues the logical line, and continuation lines are indented further. Long Label lines are left to Label syntax.
- **Empty Blocks** are allowed, with a warning. No placeholder keyword.
