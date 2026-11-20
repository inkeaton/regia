# What a Director knows about itself, and how a Subplot's ending is heard

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

Which conditions can a Director write about its own Phase, Stagings and Roles, and how does an ending reach the parent?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- N7 A Director can't ask about its own state
- D11 How a Subplot's ending reaches its parent

Decide:

- Conditions on the current Phase, on where a transition comes from and goes to, on running Stagings, on the number of Agents of a Role. A condition on running Stagings can now match a Plot's arguments (`HonorDuel(?q)`, ADR 0028), which guards against a second duel between the same two Guests ([*Telling Stagings and Givings apart*](08-stagings-and-casts.md)). `COUNT(? PLAYS Guest)` already exists (chapter 15).
- An ending from above (`END SUBPLOT`, `UNTIL EXITED`) reports nothing, so a parent that took a Playbook from the duellists gives it back in the Plan that ends the duel (chapter 15, *Giving it back*). Whether that stays so is part of D11.
- "Ended with no Outcome", an ending from above, and starting a Subplot and waiting for it.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

## Resolution

Resolved on 2026-11-17, with the user.

- **N7, fixed except where a transition goes, which is kept.**
  - Current Phase: the condition `IN <phase>`, for a `DURING PLOT` Plan that must not re-enter a Phase. Re-entering on purpose stays allowed. A Phase is not a Value, so there is no `IN ?p`.
  - Where a transition goes or comes from: **kept**. The user was concerned that `EXITED TO`/`ENTERED FROM` would muddy the Visual Editor's narrative flow. In the Phase map an edge is the Plan that runs `TRANSITION`, so what belongs to the edge is written in that Plan, before the `TRANSITION`.
  - Running Stagings: `<Plot>(args) RUNNING`, for the Stagings this Staging started. It works with `NOT`, `COUNT`, Picks and `FOR EACH`. A Staging stops counting before its ending is heard. Matches are distinct (chapter 26), so `COUNT` counts distinct arguments and a Plot without parameters counts 1 or 0.
  - A Subplot telling an ending by its parent from its own: `WHEN EXITED BY PARENT`, which fires before plain `EXITED`.
  - Counting a Role's Agents: already fixed by [*What can be said about a Role*](06-roles.md) (`COUNT(? PLAYS Guest)`).
- **D11, fixed except waiting, which is deferred.**
  - A Subplot's endings are heard like a Goal's: the specific Trigger (`ENDED WITH e`, `ENDED WITHOUT OUTCOME`, `DROPPED`), then plain `ENDED`. "First match wins" between plain and `WITH` is gone. `ENDED WITH` Blocks still compete among themselves.
  - An ending from above is heard: `END SUBPLOT` and `UNTIL EXITED` fire `DROPPED` and then `ENDED`, once per Staging with its arguments, after the Body. `UNTIL EXITED` endings are heard by the new Phase, else by `DURING PLOT`. A Subplot ended because its parent is ending still reports nothing. The tidying is written once, in the `ENDED` Plan.
  - Which Staging ended: by its arguments ([*Telling Stagings and Givings apart*](08-stagings-and-casts.md), ADR 0028). An ending the parent never hears: `R1708` ([*What passes between a Playbook and a Plot*](01-playbook-plot-interface.md)).
  - Starting a Subplot and waiting for it in the same Plan: deferred past 2.0, with *Richer Directors*.

Settled while writing, after the user agreed the resolution:

- A `DROPPED` with no Plan writes no Trace entry. The parent caused it.
- `EXITED BY PARENT` follows the same order as the endings, specific first and then plain `EXITED`. The question had proposed first-match-wins, before the endings were settled the other way.
- The Phase map draws a `DURING PLOT` Plan with a positive `IN p` as a dashed edge from `p`. `NOT IN p` appears only in the label.

Changed:

- Spec:
  - Chapter 17: *Running Stagings*, *The parent's Triggers*, `END SUBPLOT`, `UNTIL EXITED`, the checks, *Not in 2.0*.
  - Chapter 20: *What a Director knows about its own Staging*, `EXITED BY PARENT`, the Trigger table, *What a `TRANSITION` does*.
  - Chapter 25: the `DURING PLOT` and *Entry and exit* layers.
  - Chapters 05, 11, 15, 26 and 38: cross-references, `R0506`, `T3802` and the catch-all.
  - New codes: `R1712`, `R1714`, `R2014` (errors); `R1713`, `R2015` (warnings). `R1707` retired.
  - Reserved words: `OUTCOME`, `RUNNING`, `IN`.
- ADR: 0030 *A Subplot's endings are heard like a Goal's, including one its parent caused*.
- Glossary: *Subplot* and *Phase*.

Handed on:

- The Jason chapters (30, 31): the `dropped(Plot)` report and its silent catch-all, the record of running Stagings for `RUNNING`, `IN` against the current-Phase belief, `BY PARENT` carried on the end message, and the endings run specific-then-plain.
- Chapters 15 and 17 disagree on `HonorDuel`'s parameters: `(?offended, ?offender)` in chapter 15, `(quarrel)` in chapter 17. Both are examples, but the guide should pick one when it is brought up to date.
- `IN`, `RUNNING`, `OUTCOME` and the second job of `BY` are open to [*Words that do several jobs*](20-words-and-syntax.md).

1.5, from [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md):

- N7 in: `IN`, `RUNNING`, `EXITED BY PARENT`, the kept rule on transitions. D11 in: the endings and `DROPPED`. Waiting is later than 2.0. Nothing here needs a later part of 2.0.
