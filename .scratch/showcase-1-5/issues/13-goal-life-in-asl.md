# A Goal's life in ASL

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05, 10

## Question

Group D of the [inventory](../jason-open-questions.md#d-a-goals-life-in-asl-a-goals-life-in-asl): chapters 05, 08 and 11 leave a Goal's life in Jason to "the Jason chapters", and none has it.

Decide:

- what a Pursuit carries: its Sender, an identity for the Trace;
- how `REACHED`, `DROPPED`, `FAILED` and `ENDED` are raised, specific then plain;
- how a `FAIL WITH` Reason reaches each `-!g` plan of the chain (with the research on `-!g`);
- how the generated `-!g` plan and the designer's `FAILED WITH` and `FAILED` Plans meet;
- a Goal with no applicable `TO` Plan (`T1104`);
- who walks the levels a `DROP` stops, and whether `regia.stop_playbook` shares it;
- `PURSUING` leaving out the current intention.

Closes when the chapters are edited (a new section in a Jason chapter, or a new chapter).

## Comments

- From *A Plan's Statements in ASL*: the Statement translations this ticket decides (`PURSUE`, `DROP`, `FAIL WITH`) go in chapter 39 (`docs/spec/39-jason-plan-bodies.md`), whose *Not decided here* points back here. Chapter 39's `WAIT … UNTIL` example leaves a `FAIL WITH` as `…` for this ticket.

## Resolution

Grilled with the user on 2026-11-18. Recorded in a new chapter 40, *A Goal's life in Jason* (`docs/spec/40-jason-goal-life.md`), a new *Goals* section of chapter 39, and edits to chapters 08, 11, 28, 29, 32 and 35. Jason facts checked in `TransitionSystem.generateGoalDeletion`/`findEventForFailure` and `Intention.findEventForFailure` (3.3.4).

1. **Identity**: every Pursuit carries `regia_pursuit(Id)` on its `+!g` event, where `Id` is the `seq` of its `GOAL … PURSUED` entry, which is written when the request is made. Stamped by `regia.pursue` for an own `PURSUE`, by `RegiaAgent.socAcc` for an incoming `achieve`, and by the `regia_everyone` plan for `ASK EVERYONE`. The Sender stays Jason's `source(S)`. Rejected: an Id taken in the recipe body (misses `T1104`, and `-!g` can't see it).
2. **Ending Plans** compile to plans for `+!regia_reached/dropped/failed/ended(G, Sender, [Reason,] Id)`, with the Items `reached(g)`, `dropped(g)`, `failed(g)` and `ended(g)` (chapter 32). `FAILED WITH` before the plain `FAILED` falls out of chapter 32's step 3 (Pos 0 against Pos 1). One `regia_noop` plan per kind covers an ending with no Plan (step 0 widened), and a `-!regia_<kind>` catcher makes a failing ending Plan just stop.
3. **`REACHED`**: each recipe ends with `regia.reached`, which writes the entry and runs `REACHED` then `ENDED` on a new intention, so the waiting Body carries on at once.
4. **`FAILED`**: one generated `-!g` per Goal, in `asl/goals.asl`, with the context `true` and **no Givings guard** (this reverses chapter 29). It writes the entries, runs `FAILED` then `ENDED` in the failing intention (so innermost first, each level complete), then `regia.pass_failure` either fails the goal below, or writes a waiting `WHEN` Plan's entry and ends quietly, or (at the bottom) succeeds. No applicable recipe is the same plan, reached through `error(no_applicable)`.
5. **Reasons**: `FAIL WITH r` is `.fail(regia_fail, regia_reason(r))`. Jason puts the `.fail` arguments on the next `-!` event, and each `-!g` passes them on with `regia_because(Seq)`. Refinement made while writing: the catcher writes `T1103` rather than the Statement, so that each Failure has exactly one cause entry. A Statement that writes its own cause (`CHANGE`'s `T0801`) fails with `regia_because`.
6. **`DROP`**: `regia.drop(G)` is a Java walker shared with `regia.stop_playbook`. It removes every intention holding `+!g` whole, calls off waiting `DO`s, writes the `DROPPED` entries (`because` the dropped one), and starts one new intention per removed one, which runs `DROPPED` then `ENDED` for each level, innermost first.
7. **`PURSUING`** is `regia.pursuing(G, Except)`, which scans `+!g` frames. `Except` is the trigger's own `Id` in a `TO g` Plan and `none` elsewhere, which avoids the stale `current` of `.intention` in a Context.
8. **A `WHEN` Plan failing with no Goal under it**: `regia.RegiaAgent` catches it on the Java side and writes the cause entry. Which Jason hook it uses is left to the implementation.
9. **Placement**: the Statements are in chapter 39 and the mechanism in chapter 40. Chapters 08 and 11 keep only Target-neutral notes.
