# Review: text to tokens

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

What exactly does the lexer hand to the parser?

Work by hand: `IF is_hungry: DO eat_food; ELSE: DO complain`, then a Block ending in comments (chapter 22, Extent rules 3 and 4).

Decide:

- Where INDENT and DEDENT are placed around comments and blank lines. Extent rule 3 needs a Block's last comments before its DEDENT, yet chapter 22 gives ownership to the tree builder and chapter 23 gives the indent stack to the lexer.
- Who joins continuation lines (a final `,`, an open `(`), and who tells `.` the terminator from `.` in a name or a number.
- Who turns `:`, `.`, `;` of the explicit style into structure: lexer or parser.
- Which Diagnostics the lexer reports itself (mixed tabs, `R0104`), and the token kinds. Are keywords, 2.0 and retired ones included, kinds of their own?

Chapters 01, 02, 22, 23.

## Resolution

Agreed with Edoardo on 2026-11-25. The answer is in chapter 23, *What the lexer hands to the parser*.

- **Shape.** Lex is `scan` (text to raw tokens) then `layout` (lines, INDENT, DEDENT). NEWLINE is a token; `layout` joins continuation lines.
- **Comments.** Columns decide: a comment is in the deepest open Block no deeper than its own column, never shallower than the next code line. *Extent* rules 1 and 3 changed to fit (chapter 22, *Which Block a comment is in*). Under a header with no body, columns are compared (by the tree builder, corrected in *Review: tokens to tree to accessors*).
- **`:`, `.`, `;`.** Plain tokens; the parser makes structure of them, so `R0101` and `R0108` are the parser's. `scan` tells STOP from a dotted name by the next character, and a dotted name is one token.
- **Kinds.** Every reserved word has one, 2.0, later and retired words included. A Placeholder is one token; `-` is always its own.
- **Recovery.** A line that breaks a continuation is `R0105` and starts a new logical line, with the open `(` forgotten and no missing `)` reported. After `R0104` the line belongs to the outer Block. `R0103` is once per file, continuation lines included, and silences `R0104` and `R0105` in it; a line further indented still continues.
- **Diagnostics.** The lexer returns a list beside the tokens, and malformed text keeps the kind it was meant to have. New codes: `R0112` to `R0115`. Names and Strings are defined in chapter 01.
- **Teach-back.** The user worked a second example: continuation, a forgotten `)`, two dedents around comments.
- **Implementation note for *Cut M1 into tickets*:** `layout` reads past comments to the next code line before it can place a NEWLINE, INDENT or DEDENT.
- **Not done:** no Conformance cases for `R0112` to `R0115` yet; they come test-first with the tickets that implement them.
- No ADR: the reasons sit in the chapters, and none of this is hard to reverse.
