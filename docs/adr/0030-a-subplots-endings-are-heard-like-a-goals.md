# A Subplot's endings are heard like a Goal's, including one its parent caused

Chapter 17 had one Trigger for a Subplot's ending: `WHEN P ENDED`, with `WITH e` Blocks and a plain catch-all tried in written order, first match wins. A Subplot ended from above (`END SUBPLOT`, `UNTIL EXITED`) reported nothing, because "the parent did it on purpose". As a result, "ended with no Outcome" couldn't be written on its own, and the tidying for a duel (giving `Dining` back) was written twice: once in the `ENDED` Plan and once beside every `END SUBPLOT`. With `UNTIL EXITED` it had no good place at all.

We now follow the Goal endings (chapter 05, ADR 0017). A specific Trigger fires first and then plain `ENDED`:

- `ENDED WITH e` when the Subplot ended itself with that Outcome;
- `ENDED WITHOUT OUTCOME` when it ended itself with a bare `END PLOT`;
- `DROPPED` when this Staging ended it, by `END SUBPLOT` or by `UNTIL EXITED`.

The parent hears an ending it caused once per Staging, with that Staging's arguments, after the Body that caused it. An ending from `UNTIL EXITED` is heard by the new Phase, or else by `DURING PLOT`. A Subplot that ends because its parent is ending still reports nothing.

On the child's side, `WHEN EXITED BY PARENT` fires before plain `EXITED` when the Staging is being ended from above. This follows the same "specific first, then plain" order.

## Considered Options

- **Keep "first match wins"**, adding `WITHOUT OUTCOME` and `DROPPED` as narrower Blocks. Every ending would then still run exactly one Plan, so tidying shared by all endings would be written in each Block. That is the duplication this decision removes.
- **Keep endings from above silent**: the parent knows what it did. That only holds for one Staging ended by name. `END SUBPLOT HonorDuel(?)` ends duels the parent can't list without keeping its own Facts, and an `UNTIL EXITED` ending happens in a Phase whose Plans are already stopped.
- **Report endings from above as plain `ENDED` with no Outcome**, with no word of its own. A parent could then not tell "abandoned" from "stopped by the guards".

## Consequences

- `R17_07-shadowed-ended-with` (a plain `ENDED` shadowing a `WITH` Block) is retired. The `ENDED WITH` Blocks still compete among themselves, in written order.
- `DROPPED` after a Plot's name is a Subplot ending, and after a Goal's name a Goal's (ADR 0006).
- A `DROPPED` with no Plan writes no Trace entry. An ending the Subplot chose itself with no Plan still writes `T38_02-ending-found-no-plan`.
- A Statement written right after `END SUBPLOT` runs before the `DROPPED` and `ENDED` Plans.
- `DROPPED` in a Plot that never ends that Subplot from above is an error (`R17_12-subplot-never-dropped`). A `DROPPED` or `ENDED` Plan written only in the Phase whose `UNTIL EXITED` ends the Subplot is a warning (`R17_13-unheard-until-exited-ending`).
- Waiting for a Subplot in the Plan that started it stays out of 2.0, with Directors that have Goals.
