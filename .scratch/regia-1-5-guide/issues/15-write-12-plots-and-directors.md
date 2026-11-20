# Write guide chapter 12, Plots and Directors

Type: task
Status: open
Assignee:
Blocked by: 05

## Question

Write `docs/guide/12-plots-and-directors.md`, *Plots and Directors*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 20, 16.
- **Covers:** a Plot, its Roles, a Role's Block as its setup, Phases, `ENTER`, `WHEN ENTERED`, `DURING PLOT`, what a Director perceives, Director Actions, failure in a Director, the Root Plot.
- **Quotes most:** `royal_banquet.regia`.
- **"In 2.0" notes:** `FROM GAME`, Quota Triggers in a Director.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.
