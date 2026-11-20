# Subplot arguments and endings in ASL

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 18

## Question

Group J of the [inventory](../jason-open-questions.md#j-subplots-after-adr-0030-subplot-arguments-and-endings-in-asl): chapter 31 predates ADR 0030 and Plot arguments.

Decide:

- how a Subplot gets and reads its arguments, and the parent's record of running Stagings for `RUNNING`;
- `END SUBPLOT` with an argument pattern;
- the parent's `DROPPED`, `ENDED WITH`, `ENDED WITHOUT OUTCOME` and `ENDED` Plans, specific then plain, and which ending writes `T3802`;
- `EXITED BY PARENT`;
- a Subplot's `DO` while its parent is ending: as written, the Root ignores it and waits for the child forever.

Closes when chapter 31 is edited.

## Comments

- From [*Entering and leaving a Phase in ASL*](18-phase-change.md): `regia_child` is now `regia_child(C, Plot, Until)`, with `Until` `staging` or `phase(Ph)`. An `UNTIL EXITED` child is ended at `TRANSITION` step 3, which posts `!!regia_subplot_dropped(Plot)` without waiting (chapter 30). Chapter 31's `END SUBPLOT` doesn't post it yet: decide that here, along with the Plans `regia_subplot_dropped` runs.

## Resolution

Decided with the user on 2026-11-19. Chapter 31 is edited (*Starting a Subplot*, a new *Plot arguments*, *The walk*, *A child ended by its parent*, `regia_ended`, *`END SUBPLOT`*, a new *`RUNNING`*, *An ending Director hears nothing*, and *The parent's ending Plans* in place of *`WHEN <Plot> ENDED`*), with notes in chapters 17, 20, 30, 32, 33 and 37.

1. **Plot arguments.** The start message is `regia_start(Cast, Prefix, Args)`, with `Args` the arguments in parameter order (`[]` without parameters). The child keeps them as `regia_args(List)` before `!regia_begin`. Each generated plan whose Block names a parameter reads `regia_args([…])` at the head of its context, after the Phase guard, so a Trigger naming a parameter tests it. The Root has no `regia_args`.
2. **The parent's record and `RUNNING`.** `regia_child(C, Plot, Args, Until)`, where `Plot` stays bare for percept forwarding. `P(?x) RUNNING` is `regia_child(_, p, [X], _)`, and `COUNT` goes through `.setof` on `Args`, so it counts distinct argument lists. The record is removed, as before, before the ending is posted.
3. **`END SUBPLOT` with a pattern.** For each `regia_child` whose `Args` unify with the pattern: remove the record, send `regia_end`, and post `!!regia_subplot_endings(p, Args, dropped)`, once per Staging. `TRANSITION` step 3 does the same for `UNTIL EXITED` children. A child's late `regia_ended` is ignored, so it is heard once, as `DROPPED`.
4. **The parent's ending Plans.** These are four generated goals, `regia_subplot_with/without/dropped/ended(p, Args, …, Heard)`, each with a catch-all and a `-!` catcher that writes `T2002`. One dispatcher intention, `regia_subplot_endings(p, Args, How)` (`How`: `with(O)`, `without`, `dropped`), runs the specific goal and then `regia_subplot_ended`, each to completion. Each is picked when posted (current Phase, else `DURING PLOT`, chapter 32's rank). `ENDED WITH` Blocks share the Item `subplot_with(p)` at their written `Pos`, which gives first match in written order, as for `FAILED WITH`. The old context exclusion is dropped.
5. **`TRANSITION` or `END PLOT` in a specific Plan.** `regia.end_body` now drops only the frames of the Plan that ran it (chapter 30, step 7). The dispatcher carries on, and the plain `ENDED` runs under the new Phase.
6. **`T3802`.** `Heard` is an out-argument: generated plans bind `heard`, catch-alls bind `unheard`. The dispatcher writes `T3802` when both are `unheard` and `How \== dropped`.
7. **`EXITED BY PARENT`.** `regia_end` carries no flag: receiving it is what "by parent" means. The walk is `!regia_end_plot(O, By)`. With `By = parent`, `regia_exited_by_parent(Scope)` (a generated goal with a catch-all) runs before each `regia_exited(Scope)`: the Phase's, then `DURING PLOT`'s, all inside the atomic step.
8. **A Subplot's `DO` while its parent ends.** The Root's relay plans for `regia_act` and `regia_act_cancel` have no Phase guard and accept any sender. The Root is never killed and tells the game `regia_story_ended` only after every child acks, so `DO ring_bell`/`DO discard_cup` in `EXITED BY PARENT` are answered and the walk finishes. Percept forwarding is still guarded.
