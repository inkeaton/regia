# Write guide chapter 11, Playbooks and Roles

Type: task
Status: closed
Assignee: Edoardo Vassallo
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

## Resolution

Done on 2026-11-20 (task). [`docs/guide/11-playbooks-and-roles.md`](../../../docs/guide/11-playbooks-and-roles.md), about 560 lines, written from the template:

- An opening table of the chapter's words (`ROLE`, `MAPPING … AS`, counts, `EXCEPT`, `PLAYS`, `REMOVE`, `ASSIGNED`/`REMOVED`).
- Sections, simple to full: A Playbook (`Keeping_watch` whole); Roles of a Playbook (`Serving`, the three places a Role stands); Mappings (the `feast` setups, `peer`, `HonorDuel`'s crosswise `opponent`, `Courtesy`'s `host` by name, a mermaid of every Mapping, *A binding is live*); Givings (target table, standing in 1.5, *For as long as a Phase lasts: `UNTIL EXITED`* on the `Poisoning` start); The whole Cast; Counts and fractions (with *A counted recipient*); `EXCEPT`; `PLAYS`; Several Givings of one Playbook (the Watchmen); `ASSIGNED` and `REMOVED`; Taking a Playbook away (the `REMOVE` forms, *Giving it back*, *What stops* with interaction 7).
- Givings come before `CAST`, counts, `EXCEPT` and `PLAYS`, not after them as in the ticket's list: the `CAST:` setup and the counted `Poisoner` read as Givings, so the Giving has to be explained first.
- Two "In 2.0" notes: joining (a standing Giving reaching later joiners; 1.5's cast only shrinks), and Quotas (a count after `FROM`/`BY`; 1.5's hand count with `COUNT(? PLAYS Guest)`).
- Throwaways: `EXCEPT` on a Giving and a recipient (`ASSIGN Wagering TO Guest EXCEPT Guard`, `TELL Guest EXCEPT ?culprit duel_on`), and *Giving it back* as a banquet variation (the offender loses `Dining` for the duel and gets it back in `WHEN HonorDuel(?offender) ENDED`, with nothing to lift once `feast` is over).
- Every showcase snippet checked against its file by script (19 snippets). Codes appear in *Checks* only (checked by script); they borrow `R0109`, `R0303`, `R1007`, `R1601`, `R1603`, `R1714`, `R2005`, `R2014`, `T3801`.
- `Guide: Playbooks and Roles` added under *15 Roles and mappings* in the showcase README.
- Grep for retired spellings: only in *Checks* lines naming them. The humanizer pass changed nothing.

Four non-blocking findings: chapter 15's `EXCEPT` list example says `TO` for `AS`; no code for a `ROLE` line after a Trigger Block; `R2005`'s `ENDED` is ambiguous in a Playbook; a non-Number count in a Director (`T1501` "fails the Plan" against "Director Statements never fail").
