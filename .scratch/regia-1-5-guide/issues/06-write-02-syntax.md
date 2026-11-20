# Write guide chapter 02, Syntax

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05

## Question

Write `docs/guide/02-syntax.md`, *Syntax*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 01, 02.
- **Covers:** Statements and Blocks, indentation as the default, the `.`/`;` one-line layout, continuation lines, empty Blocks (`PASS`), comments and doc comments, reserved words, and retired spellings as a pointer to chapter 01's table (not a copy).
- **Quotes most:** any file; `vocabulary.regia` for doc comments.
- **"In 2.0" notes:** `R0109` on a word of 2.0.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-20 (task). [`docs/guide/02-syntax.md`](../../../docs/guide/02-syntax.md), about 470 lines, written from the template:

- Sections, simple to full: Statements and Blocks, Inline blocks, `.`, `;`, continuation lines, clauses and the comma (with condition-word order and parsing without declarations, since a Transpiler builder needs them and `R0111` lives there), empty Blocks and `PASS`, comments, Doc comments, `#@allow`, keywords, retired spellings (a pointer to spec 01's table, not a copy), words of Regia 2.0 (`R0109`, with the "In 2.0" note).
- Showcase snippets checked line by line against the files. The one-line layouts, the error cases, `#@allow: R1305` and the `EITHER` example are throwaway variations of showcase lines.
- Checks borrow `R1412`, `R2125` and `R0706` where the misuse is in this chapter's constructs.
- `Guide: Syntax` added under *01 Statements and blocks* and *02 Comments* in the showcase README.
- Grep for retired spellings: only the deliberate `EITHER` example. The humanizer pass rewrote three contrast sentences.

One finding: whether an unclosed `#@key[` is `R0201` (chapter 02 doesn't say).
