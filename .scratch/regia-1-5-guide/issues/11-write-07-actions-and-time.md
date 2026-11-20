# Write guide chapter 07, Actions and time

Type: task
Status: open
Assignee:
Blocked by: 05

## Question

Write `docs/guide/07-actions-and-time.md`, *Actions and time*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 08, 12.
- **Covers:** Basic Actions on Facts and Goals, `PRINT`, Custom Actions, `WAIT`, `WAIT … UNTIL`, `AFTER` (Phases themselves are *Plots and Directors*), the Target's clock and pausing.
- **Quotes most:** `serving.regia`, `keeping_watch.regia`, `royal_banquet.regia`.
- **"In 2.0" notes:** none expected.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.
