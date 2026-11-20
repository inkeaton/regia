# Write guide chapter 15, Interfaces

Type: task
Status: open
Assignee:
Blocked by: 05

## Question

Write `docs/guide/15-interfaces.md`, *Interfaces*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 38.
- **Covers:** nothing is declared; the Interface of a Playbook and of a Plot; who sends a Cue; the checks of one side against the other.
- **Quotes most:** across `playbooks/` and `plots/`.
- **"In 2.0" notes:** the asked-Goal rows, `R3805`, `R3806`.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.
