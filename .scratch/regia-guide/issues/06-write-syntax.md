# Write: Syntax

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Task

Write `docs/guide/2 - Syntax.md`.

Covers: Statements, Blocks and Block headers, Inline blocks, Comments and Doc comments, files and Imports.

Sources: 01, 02, 10.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-12: [`docs/guide/2 - Syntax.md`](../../../docs/guide/2%20-%20Syntax.md), about 2,600 words counting snippets, tables and the diagram. Twice the sample's length, because it covers seven constructs where the sample covers four. Not yet read by the user.

- **Sections**: Statements and Blocks; Inline blocks; What a `.` ends; Long lines; Comments; Doc comments; Files and Imports; How this combines with… (Instancing, the Visual Editor, the Transpiler); Since 1.0.
- **Snippets**: cuts of `courtesy.regia`, `noble_socializing.regia`, `banquet.regin`, `duelling.regia`, `royal_banquet.regia`, `vocabulary.regia`, `poisoning.regia` and `test.regin`. Throwaway variants for the one-line style (`;`, two Statements on a line), the Inline block error and a nested `#[ … ]#`.
- **Showcase changed**: the Doc comment of `RoyalBanquet` in `plots/royal_banquet.regia` is now a `#@version: 2.0` line and a two-line `#@desc[ … ]#`. No chapter written so far quotes those lines.
- **Diagram**: a flowchart of which showcase file imports which.
- **Checked against**: spec chapters 01, 02 and 10 in full; 21 (`.regin` files, Instancing comments, a header with no Body), 22 (which Comments belong to a construct, text never normalised), 09 (Options are ordinary Blocks), 23 (each file parsed alone), 25 (where Doc comments are shown). Not covered here and left to *Vocabulary*: External names, Local Vocabulary, the one namespace and the name rules of chapter 10.
- **Review notes**, seven `#revise`:
  - The `.` at the end of a line is optional. The showcase and the spec's examples write it on Statements and Imports and not on Vocabulary lines, and the Visual Editor writes none.
  - The showcase never uses `;` nor two Statements on a line, so the whole one-line style went unused in 700 lines.
  - `.` ends a Statement, marks a decimal and joins dotted names, told apart by the next character.
  - A blank line decides what a Doc comment describes and whether it is read at all.
  - The showcase puts plain Comments above its Plans where Doc comments were possible; one character separates the two.
  - The spec doesn't say what a Doc comment above a Multi-definition describes.
  - Importing what a file uses is a habit nothing checks; an Import doesn't say which names it brings.
- **Showcase README**: two entries added to *Gaps in the showcase* (no `#[ … ]#` and no Doc comment on a Plan, Role or Phase; no `#%` comment) and two to *Spec wording* (chapter 21's "ends with `.`" against chapter 01; Doc comments in `.regin` files).
- **Glossary**: Statement is defined as "a single step of a Plan's Body", but spec chapters 01, 10 and 21 also call an `IMPORT` line and a `COUNT 1.` line Statements. The chapter says "one Statement or one declaration" per line. Added to the map's *Not yet specified*.
- **For the consistency pass**: sections are referred to in prose ("the last section"), never in italics, which are kept for chapter titles. The chapter cites *Precedence and Labels*, *Randomness*, *Vocabulary*, *Instancing*, *The Visual Editor*, *The Transpiler*.
- Five `#changes` lines, from spec chapters 01, 02, 10 and 21 and primer chapters 1 to 3.
