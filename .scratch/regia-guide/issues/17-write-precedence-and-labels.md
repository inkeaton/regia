# Write: Precedence and Labels

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Task

Write `docs/guide/14 - Precedence and Labels.md`.

Covers: Which Plan runs when several could: order within a Trigger, Precedence declared by the Plot, ties, Suits alternatives and the Selection function, Shifts Labels.

Sources: 13, 14; ADR 0008.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-12: [`docs/guide/14 - Precedence and Labels.md`](../../../docs/guide/14%20-%20Precedence%20and%20Labels.md), about 5,250 words counting snippets, tables and the diagram, over eleven sections (one Plan for each Trigger, falling through, inside a Playbook, the `PRECEDENCE` Block, a Plot and its Subplots, a Director's own Plans, Labels on a header, Suits alternatives, Shifts, tied Playbooks, reading the order). The longest chapter so far: it carries two spec chapters, and every other chapter points to it for "which Plan runs". Propensity declarations are left to *Vocabulary*, their values to *Instancing*, and the latecomer in `farewell` to *Plots and Directors*. Not yet read by the user.

- The showcase Program is unchanged. `TIES`, two overlapping Trigger Blocks in one Playbook, and a relation between `DURING PLOT` and a Phase are shown with throwaway snippets and listed under *Gaps in the showcase*. `TIES` was not added on purpose: it only works with `SUITS` on both Playbooks' Plans, which would have changed snippets that six chapters quote.
- Sixteen `#revise`, one of them repeating the README's cycle note. From reading the systems together: the knight's order on `scandal` is spread over two `PRECEDENCE` Blocks, a default and two missing `ELSE`s, and only the conflict report shows it whole; an `ELSE` added to one Playbook silently ends another's Plan; a tie is declared by the Plot and only works through Labels inside both Playbooks, and with one side unlabelled VEsNA-Pro makes it an `OVER`; a Mood moves between Playbooks that never name each other, yet can't be tested or traced. On Precedence alone: one Plan per Trigger rules out "watch and snigger"; two of `RoyalBanquet`'s three relations say what name order would decide anyway, so a rename is what changes behaviour; `PARENT OVER SELF ON scandal` is written blind; `SELF` means the Plot's own Playbooks in one line and the whole subtree in another; a relation can't name a single Trigger Block; a tie can't cross a Plot. On Labels alone: the three ways to take an insult name three different sets of Propensities, so the source doesn't say what a knight does; there is no neutral alternative; when a Shift applies is the Target's, and on VEsNA-Pro a lone Plan never shifts; a Shift can't sit on an `IF` branch; the three alternatives write the same `PLAN` line in a Trace.
- Five entries added to the README's *Spec wording*: how `ON` is written for cast Triggers, `ENDED` and `ENTERED`; two wordings of the Phase-over-`DURING PLOT` warning, under one of which the showcase warns; under which Role the conflict report lists a competition between Playbooks of two Roles; whether a failed or stopped Plan has shifted; and the two meanings of `SELF`, which follow only from chapter 32.
- Glossary: Trigger Block, the unit that competes in chapter 13 and a word the guide's chapters use freely, has no entry. Nor does the conflict report. The Precedence entry lists "rank" under *Avoid*, while chapters 13 and 32 and the Selection function's own entry ("equally ranked Plans") use it throughout; the chapter writes "order" and "place".
- Every example was re-read against spec chapters 13 and 14, with 05, 06, 17, 18, 20, 21, 32 and 34 for the parts they own, and ADR 0008. `humanizer` was run as the last pass.
