# Write guide chapter 01, The logic of Regia

Type: task
Status: open
Assignee:
Blocked by: 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28

## Question

Write `docs/guide/01-the-logic-of-regia.md`, *The logic of Regia*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`). Written after the other chapters so it picks the snippets they made familiar.

- **Spec:** 05, 15, 16, 20, 21 (a section each).
- **Covers:** one small Program read end to end: a Playbook, a Plot with Roles and Phases, a Giving, an Instancing, one run; each section ends pointing at the chapter that covers it in full.
- **Quotes most:** `courtesy.regia`, `royal_banquet.regia`, `banquet.regin`.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.
