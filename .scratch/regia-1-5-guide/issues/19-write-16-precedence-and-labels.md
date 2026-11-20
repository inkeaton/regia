# Write guide chapter 16, Precedence and Labels

Type: task
Status: open
Assignee:
Blocked by: 05

## Question

Write `docs/guide/16-precedence-and-labels.md`, *Precedence and Labels*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 13, 14.
- **Covers:** one Plan per Trigger, falling through, order inside a Playbook, `PRECEDENCE`, a Plot and its Subplots, a Director's own Plans, Labels, Propensities, Suits, `SHIFT`, reading the order.
- **Quotes most:** `scheming.regia`, `duelling.regia`, `royal_banquet.regia`.
- **"In 2.0" notes:** none expected.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.
