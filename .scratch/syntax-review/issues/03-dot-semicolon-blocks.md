# `.`, `;` and the Block styles

Type: grilling
Status: closed
Assignee: claude (with Edoardo)
Blocked by: 01

## Question

`.` has three meanings: it ends a Statement, it is the decimal point, and it joins the parts of an External name. The character after it tells which, so `DO a.DO b` is an error (`R0102`). `;` closes Inline and Flat blocks. There are three Block styles (indented, Inline, Flat), and `PASS` exists partly because of Flat blocks.

Decide, applying the principles' rule on what can be dropped and weighing *Regia is generated too*:

- whether `.` stops ending Statements, or something else takes over the job (a new line only, or another mark), and whether External names keep their dots;
- whether Flat blocks, `;`, and several Statements on one line stay, and which explicit form generated code gets if they don't;
- whether `PASS` and the "an empty Option needs no `PASS`" exception stay;
- whether a `.` at the end of a line stays allowed and silent (habits from 1.0, the showcase's dots), or gets a warning.

Done when chapters 01 and 02 and the examples that use these forms are edited, and the rule for generated code is written down.

## Resolution

Grilled with the user on 2026-11-19. Applies ADR 0041's rule on dropping syntax; no new ADR.

1. **`.` keeps ending a Statement**, optional, for code written without indentation. It stays the decimal point, and External names keep their dots (`engine.security.summon_guards`); the "next character" rule and `R0102` are unchanged. Several Statements on one line stay.
2. **The two styles, reframed.** On one line, `:` followed by a body stands for an indent, `.` for a new line, `;` for a dedent, and the explicit style is nothing more: it never spans lines.
3. **Flat blocks are removed.** A header ending its line with no indented body is an empty Block (`R0106`). `;` closes only Inline blocks; a stray `;` is `R0108`, whose hint says Flat blocks are gone. `R0107` is retired and its number not reused.
4. **The rule for generated code** (chapter 01, *Two styles*): indentation is the default for hand-written and generated code, and the Visual Editor and formatters write it (one Statement per line, no trailing `.`). The explicit marks are for code that must fit on one line, and for writers who prefer not to indent, as a style choice: each Block then goes on one line.
5. **A trailing `.`, or a `;` closing an Inline block at the end of a line**, stays allowed and silent; tools never write it. Dropping the trailing dots from spec examples went to *Spec examples after the review*.
6. **`PASS` stays**, as the Statement that does nothing and marks a Block empty on purpose. **The exception for empty Options is dropped**: an Option with no body warns like any empty Block, and "otherwise nothing" is `OR, WEIGHT 7: PASS`.

Edited: chapter 01 (*Two styles*, *Where a Block's body starts*, the Flat-block section replaced by *No Block without indentation across lines*, *Redundant terminators*, *Indentation rules*, *Empty Blocks*, checks), chapter 09 (empty Options), chapter 39 (the `true` branch), `GLOSSARY.md` (**Block**; **Flat block** removed). Chapter 02 needed no change.
