# Write: Playbooks and Roles

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Task

Write `docs/guide/10 - Playbooks and Roles.md`.

Covers: Playbooks as sets of Plans, Roles inside a Playbook, Mappings, Givings and how they add up, Local Vocabulary in a Playbook.

Sources: 15, 10.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-12: [`docs/guide/10 - Playbooks and Roles.md`](../../../docs/guide/10%20-%20Playbooks%20and%20Roles.md), about 3,800 words counting snippets, tables and the diagram, over eight sections (a Playbook, Roles of a Playbook, Mappings, what a Mapping binds, Givings, several Givings of one Playbook, taking a Playbook away, Local Vocabulary in a Playbook). As long as *Goals and Failure*: it carries Mappings and Givings, which the four chapters after it only point back to. Not yet read by the user.

- **Showcase**: the Program is unchanged. The README got one more line under *Gaps in the showcase* and three under *Spec wording*.
- **Counted and Placeholder Mappings** are explained on a throwaway line (`ASSIGN Dining TO Guest, MAPPING 1 OF Servant TO waiter.`), since the showcase only uses them on `START SUBPLOT`. The draw itself is left to *Randomness*.
- **Diagram**: one flowchart of every Mapping onto a Playbook Role that `RoyalBanquet` writes.
- **Checked against** spec chapters 05, 07, 10, 13, 15, 16, 19, 20 and 29, and the glossary entries for Role, Mapping, Giving and Playbook.

`#revise` notes in the chapter (eleven; three repeat a README or earlier-chapter note in the place where it belongs):

1. A Role gives up an Agent only when a Message arrives from it: `Duelling` can't write `lunge(opponent)`, and the Challenger never holds its opponent in a Placeholder.
2. A Playbook can't ask whether an Agent plays one of its Roles, nor which Roles its own Agent plays (the Host's Plans in `Courtesy`; repeats the README).
3. `Host`/`host`: no Mapping in the showcase binds by name, and one that did would leave no sign in the Plot that the Playbook has a Role (extends the README note).
4. `TO` has six jobs, three of them within two lines of `feast`'s entry Plan, with the Role on either side of it.
5. `1 OF` on a Mapping is one draw shared by every receiver; a draw per receiver can't be written.
6. A Phase can't give a Playbook for as long as it lasts: three `UNASSIGN`s in `farewell` mirror three `ASSIGN`s in other Blocks.
7. A Plan can't tell its Givings apart: no Signal to one Director, no `opponent` of one duel, no Fact per Giving (repeats the README's two-duels note, and adds the shared `stamina`).
8. Whether a Signal has a listener depends on the sender's Givings: a duel winner given `Keeping_watch` by `RoyalBanquet` alone seizes the Poisoner and `Poisoning` never hears of it.
9. Nothing fires when a Playbook is given or taken away (repeats the README), and a Playbook's own `DROPPED` Plans don't run on the way out.
10. `UNASSIGN … FROM ?who` removes every Giving the Agent holds from this Staging, the Role setup's included, and `FROM <Role>` doesn't reach a Giving made to `?who`; the showcase never ends the guard of honour.
11. A Playbook's interface is declared only in its `ROLE` lines; the Goals it expects and the Messages it sends are found by reading its Plans (same note as *The Logic of Regia*).
