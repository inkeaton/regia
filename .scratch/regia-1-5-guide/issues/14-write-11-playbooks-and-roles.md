# Write guide chapter 11, Playbooks and Roles

Type: task
Status: open
Assignee:
Blocked by: 05

## Question

Write `docs/guide/11-playbooks-and-roles.md`, *Playbooks and Roles*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 15.
- **Covers:** a Playbook, its Roles, Mappings, `CAST`, counts and fractions (`%`), `EXCEPT`, `PLAYS`, Givings, several Givings of one Playbook, taking a Playbook away.
- **Quotes most:** `noble_socializing.regia`, `royal_banquet.regia`.
- **"In 2.0" notes:** the parts of 15 that 1.5 leaves out (Quota, joining).

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.
