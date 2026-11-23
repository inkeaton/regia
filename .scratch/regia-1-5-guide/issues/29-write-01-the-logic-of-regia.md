# Write guide chapter 01, The logic of Regia

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
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

## Resolution

`docs/guide/01-the-logic-of-regia.md` written (2026-11-23).

- Shape: one section per spec chapter, in reading order: *A Playbook* (`Courtesy` whole, spec 05), *A Plot and its Roles* (the `CAST:` and Role setups, binding by name, spec 16 and 15), *A Playbook given for a while* (`reception`'s `ASSIGN NobleSocializing` and its `WHEN idle` Plan, spec 15), *The Director and its Phases* (the `PHASE` lines, `DURING arrival` and `reception`, `Hosting`'s `open_feast`, spec 20), *Who is in the hall* (`banquet.regin`'s top, with a table of the whole hall, spec 21), *One run* (a sequence diagram from the start to `ENTER feast`, and the start order), then *How this combines with…* pointing at Failure, Precedence, Subplots, leaving, Interfaces and the Transpiler/Jason.
- Each section names the guide chapters that cover it in full, just above its *Checks*. *Checks* borrow codes from those chapters (a few each); *One run* lists `T1601` and `T2002`.
- One "In 2.0" note: the hand count in `arrival` (asked-Goal endings, Quota Triggers).
- The run stops at `feast`; the feast, the Subplots and `farewell` are left to *Plots and Directors* and *Subplots and Stagings*.
- `Guide:` lines added under the README's headings for 05, 15, 16, 20 and 21.
- Every snippet checked verbatim against the showcase by script; re-read against chapters 05, 15, 16, 20 and 21; no retired spellings except those the *Checks* name; humanizer pass done.
- One non-blocking finding: chapter 20's start order leaves out the `CAST:` setup and the Root Plot's kind lines.
