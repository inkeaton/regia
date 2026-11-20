# Entering and leaving a Phase in ASL

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05, 10, 15

## Question

Group I of the [inventory](../jason-open-questions.md#i-entering-and-leaving-a-phase-entering-and-leaving-a-phase-in-asl): chapter 30's `TRANSITION` doesn't run a Phase's setups, take its Givings away, end its `UNTIL EXITED` Subplots, or start its `AFTER` plans.

Decide:

- the transition's steps with a Phase's setups and Givings;
- where an `UNTIL EXITED` Subplot is ended and its `dropped` posted;
- `AFTER` in a Phase and in `DURING PLOT`;
- `IN`;
- an `EXITED` Plan with a `DO` that waits on the game, inside the atomic transition (with the research on atomic intentions).

Closes when chapter 30 is edited.

## Comments

- From [*Exclusions, one Agent and a Phase in the Giving record*](15-giving-record.md): `regia_give` now carries `Until` (`staging` or `phase(Ph)`), and a `CAST` Giving has target `role(cast)`. `TRANSITION` step 3 sends `regia_take_phase(Old)` to the cast and removes the `phase(Old)` standing records, after `EXITED` (chapter 30).
- From [*A Playbook's opening and closing in ASL*](16-opening-and-closing.md): `regia_take_phase` is one take step. The Playbooks that lose their last Giving in it share one closing intention: their drops' `DROPPED`/`ENDED`, then `UNASSIGNED`. A Playbook given again by the new or re-entered Phase's setup runs its other Plans at once, but `ASSIGNED` only as the closing's last step (chapter 29, *Opening* and *The closing*).
- From [*What a Staging runs when it starts*](17-staging-start.md): a Phase's setups are `!regia_run_setups(phase(x))` (chapter 30, *Setups*), fixed Infrastructure. Place it in `TRANSITION` after `regia_phase(x)` is set and before `ENTERED` is posted. Setup Givings write no `regia_standing`; `regia_take_phase` takes them by `Until`.

## Resolution

Decided with the user on 2026-11-18. Chapter 30 is edited (*`IN`*, *`AFTER`*, *`TRANSITION`*, *A `DO` in `EXITED`*, and `regia_begin` step 7), with notes in chapters 12, 20, 31, 33 and 37.

1. **The transition's steps.** `!regia_transition(x)` is atomic and runs seven steps that match chapter 20's six. (1) `regia.stop_phase(Old)`; (2) `!regia_exited(phase(Old))` to completion; (3) `regia_take_phase(Old)`, removing the `phase(Old)` standing records, and ending the `UNTIL EXITED` children; (4) replace `regia_phase`, then write the `phase` entry; (5) `!regia_run_setups(phase(x))`; (6) post `ENTERED`, then the Phase's `AFTER`s; (7) `regia.end_body`. Quota clearing is later than 1.5 and goes at step 4 when it comes.
2. **`UNTIL EXITED` Subplots.** `regia_child` gains a third argument, `Until` (`staging` or `phase(feast)`), as `regia_give` did. At step 3, each `regia_child(C, P, phase(Old))` is removed and sent `achieve regia_end`, and `!!regia_subplot_dropped(P)` is posted without waiting, as for `END SUBPLOT`. It is queued before `ENTERED`, so the `DROPPED` Plan starts first, under the new Phase.
3. **`AFTER`.** Each `AFTER` is its own Goal, `regia_after(Scope, N)`, numbered in source order, and listed in `regia_afters(Scope, [1, …])`. The plan works out the Duration once, calls `regia.wait(D)`, and then tests the Context through `regia_after_body`; catch-alls cover the rest. A Phase's `AFTER`s are posted right after its `ENTERED`. `regia_begin` posts `entered(plot)`, `entered(phase(I))`, then the Plot's `AFTER`s, then the Phase's. `DURING PLOT`'s count from the start and stop only with the Staging. Counts that end together run in posting order.
4. **Queued entry events.** `regia.stop_phase(Old)` also drops the queued `regia_entered(phase(Old))` and `regia_after(phase(Old), _)` events, so a re-entry never starts a count twice. Queued Trigger events are kept for the new Phase.
5. **`IN p`** is `regia_phase(p)`, and `NOT IN p` is `not regia_phase(p)`.
6. **A waiting `DO` in `EXITED`** is allowed, and the transition waits for the game. The Director runs nothing else meanwhile: messages are read, their events queue, and the new Phase hears them. The Root's `regia.act` resumes from Java. A Subplot Director's `regia.act` wakes on `regia_act_result` through a circumstance listener, never through an ASL plan (chapter 37). `WAIT` in `EXITED` is still `R2003`.
