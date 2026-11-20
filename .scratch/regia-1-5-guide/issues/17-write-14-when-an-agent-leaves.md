# Write guide chapter 14, When an Agent leaves

Type: task
Status: open
Assignee:
Blocked by: 05

## Question

Write `docs/guide/14-when-an-agent-leaves.md`, *When an Agent leaves*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 19.
- **Covers:** leaving, `LEFT`, `EMPTIED`, a leaver's Givings taken away, its Picks and bindings dropped, what the Director tidies, `T1901`; a spawn refused with `T1902`.
- **Quotes most:** `royal_banquet.regia`, `honor_duel.regia`.
- **"In 2.0" notes:** joining and `JOINED`; Quota Triggers (spec 18) as a whole, since no other chapter hosts them.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.
