# Write guide chapter 05, Placeholders and Expressions

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05

## Question

Write `docs/guide/05-placeholders-and-expressions.md`, *Placeholders and Expressions*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 03, 04.
- **Covers:** filling and using Placeholders, `?_`, what is certainly filled, naming a value, Numbers, Expressions, the Context tests and the Body fills.
- **Quotes most:** `wagering.regia`, `dining.regia`.
- **"In 2.0" notes:** none expected.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-20 (task). [`docs/guide/05-placeholders-and-expressions.md`](../../../docs/guide/05-placeholders-and-expressions.md), about 470 lines, written from the template:

- Sections, simple to full: A blank in a Trigger (with *A Value in a Trigger* and *`ME`*); Blanks in a Context (joining, a Plot's parameters); The blank nobody uses: `?` (what counts as used, with *A blank with a name: `?_who`*); Only what is certainly filled; Numbers; Expressions (operators, order, where an Expression can stand); Random numbers (whole or decimal by how the bounds are written, the guard in `Wagering`); The Context tests, the Body fills (`LET`, `LET` in branches and Options, what lasts is a Fact); When a Number isn't a Number.
- No "In 2.0" notes: nothing in these constructs has a 1.5 stand-in.
- Every showcase snippet checked line by line against its file by script. Throwaways: `DO sneer_at(?foe)` unfilled, the `OR` pair, `?half = ?gold / 2` in a Context, `LET ?stake` in both branches of an `IF`.
- Examples avoid `host` as a Value (`?dish != roast`, `roast + 1`), since `host` is a Role in the showcase.
- Checks borrow `R0704`, `R1007`, `R1008`, `R0604`, `R2604` and `R1517` where the misuse is in this chapter's constructs.
- `Guide: Placeholders and Expressions` added under *03 Parameters and placeholders* (on the line with *Vocabulary and files*) and *04 Numbers and expressions* in the showcase README.
- Grep for retired spellings: only the deliberate `?x = e`. The humanizer pass rewrote four sentences.

Four non-blocking findings: `R0303`/`R1501` both for a Role as a Value; no code for a `LET` Placeholder filled in only some branches (read as `R0305`); chapter 03's "the only cases" spared `R0307` is one case; `R0404` names only a Context.
