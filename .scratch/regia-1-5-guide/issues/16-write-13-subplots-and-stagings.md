# Write guide chapter 13, Subplots and Stagings

Type: task
Status: open
Assignee:
Blocked by: 05

## Question

Write `docs/guide/13-subplots-and-stagings.md`, *Subplots and Stagings*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 17.
- **Covers:** `START SUBPLOT`, casting, several Stagings of one Plot, a Subplot outliving its Phase, `FINISHED WITH`, `ENDED` as the catch-all, `DROP SUBPLOT`, no cycles.
- **Quotes most:** `honor_duel.regia`, `poisoning.regia`, `royal_banquet.regia`.
- **"In 2.0" notes:** a joiner reaching a Staging.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.
