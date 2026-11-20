# Write guide chapter 24, Jason: Directors and Stagings

Type: task
Status: open
Assignee:
Blocked by: 05

## Question

Write `docs/guide/24-jason-directors-and-stagings.md`, *Jason: Directors and Stagings*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 30, 31, 33.
- **Covers:** the Director's agent class, hearing the game, Phases (`!regia_enter`), the standing-Giving record, signals and messages from a Director, one Director agent per Staging, starting and ending a Staging, the parent's ending Plans, the starting cast, leaving, sends to agents that are gone.
- **Quotes most:** `royal_banquet.regia`, `honor_duel.regia`.
- **"In 2.0" notes:** joining, Quota counts.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.
