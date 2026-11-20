# Write guide chapter 17, Instancing

Type: task
Status: open
Assignee:
Blocked by: 05

## Question

Write `docs/guide/17-instancing.md`, *Instancing*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 21.
- **Covers:** `.regin` files, Agent kinds, how many start, a kind in several Roles, individual Agents, setup lines, starting Propensities, the Root Plot, the seed, Target settings.
- **Quotes most:** `banquet.regin`.
- **"In 2.0" notes:** spawning.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.
