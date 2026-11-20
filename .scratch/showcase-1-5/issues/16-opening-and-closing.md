# A Playbook's opening and closing in ASL

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 13, 15

## Question

Group G of the [inventory](../jason-open-questions.md#g-a-playbook-given-and-taken-away-a-playbooks-opening-and-closing-in-asl): chapter 29's *Taking a Playbook away* predates ADR 0021, and says so.

Decide:

- what posts `ASSIGNED` on the first Giving;
- how a closing Playbook passes its own guard for its `DROPPED`, `ENDED` and `UNASSIGNED` Plans only, and when closing ends;
- how closing Plans still `SIGNAL` and `TELL` through the Givings as they were;
- the new step 1 of chapter 29, and the events `regia.stop_playbook` raises.

Closes when chapter 29 is rewritten, its banner removed.

## Comments

- From *A Goal's life in ASL*: `regia.stop_playbook` now shares `regia.drop`'s walker (chapter 40, *`DROPPED`: the walker*), which treats every level it stops as dropped. Chapter 29's step 1 still says that a waiting Plan of another, still-given Playbook **fails**. That contradicts chapter 08 and ADR 0018 (a drop spreads as a drop). Fix it in the rewrite. The generated `-!g` plans are no longer guarded.
- From [*Exclusions, one Agent and a Phase in the Giving record*](15-giving-record.md): four more plans can take a Playbook's last Giving away (`regia_take`, `regia_set_aside`, `regia_take_phase`, `regia_end_staging`), and one can give it back (`regia_restore`), so `UNASSIGNED`/`ASSIGNED` fire from each of them. A re-entered Phase takes its Givings, then gives them again.

## Resolution

Grilled with the user on 2026-11-18. Recorded in chapter 29 (*The guard*, *Messages between Director and Agent*, *Reading the record*, a new *Opening: `ASSIGNED`*, *Taking a Playbook away* rewritten with *The take step*, *Stopping P's Plans* and *The closing*, the state table and the Trace entries; banner removed). Carried into chapter 40 (the ending goals' `Closing` argument, the walker's notes, the order table), chapter 15 (an ended Staging's whole-Role bindings), chapters 31, 32, 33 and 39 (readers through `regia_holds`, the leaver step, `regia_end_staging`), chapter 34 (`T2902` retired) and the glossary's *Giving*.

1. **`ASSIGNED`.** `regia_give` and `regia_restore` test whether P was held before adding. If P was neither held nor closing, they post `!!regia_assigned(P)`, which runs on a new intention after the atomic plan. If P was closing, the closing runs `ASSIGNED` as its last step. P's `ASSIGNED` plans carry the Givings guard and the Item `assigned`. `agent.asl` has a `regia_noop` plan and a `-!` catcher for `regia_assigned` and `regia_unassigned`.
2. **The take step.** Each of `regia_take`, `regia_set_aside`, `regia_take_phase` and `regia_end_staging` is one take step. `Ps` is every Playbook that lost its last Giving in it. Their removed `regia_given` records are moved into a snapshot, `regia_closing(C, P, D, T, Rank, B, U)`; set-aside records are not snapshotted. `C` is the `seq` of the step's first `TAKE` entry. Then come `regia.stop_playbook(C, Ps)`, clearing the Quota counts, and `!!regia_close(C, Ps, Steps)`.
3. **One closing intention per take step.** Its steps are the endings handed back by the walker (intentions in creation order, innermost first in each), then `regia_unassigned(P)` per P in name order, then clearing the snapshot, then `regia_assigned(P)` for any P given back. The closing is that intention, and it ends when the intention ends.
4. **The guard.** The ending goals take a fifth argument, `Closing` (`none` outside a take). P's `DROPPED`/`ENDED` plans are guarded by `regia_given(p, …) | regia_closing(Closing, p, …)`, so they pass for this take's drops and for no other ending of P while it closes. `UNASSIGNED` plans have no Givings guard.
5. **Speaking through the Givings as they were.** A new rule, `regia_holds`, is the union of `regia_given` and `regia_closing`, and every reader uses it: `regia_plays`, `SIGNAL`, `FROM DIRECTOR` and `selectOption`'s Rank. Only the guard reads `regia_given`. A leaver is dropped from the `fixed` lists of the snapshot too.
6. **An ended Staging.** Its cast copy is gone, so a live binding through it reaches nobody, while `fixed` bindings still reach their Agents. A `SIGNAL` to its Director is caught by `regia.send` with an `info` entry, not `T3303`. Chapter 15's bullet gains the clause.
7. **The walker** (`regia.stop_playbook`, sharing `regia.drop`'s) takes whole intentions, and a drop spreads as a drop. This fixes the old step 1, which said that a waiting Plan of a still-given Playbook fails. It skips the steps of a closing of P. Elsewhere, a `DROP` or take that finds a frame in a closing intention cuts only above its `regia_close` frame, and the closing goes on. A closing intention is never removed.
8. **Trace.** A stopped Pursuit writes `GOAL … DROPPED` with `because:` the `TAKE` entry, and a stopped `WHEN` Plan writes `plan … stopped` at `info`. `T2902` is retired and its number is not reused.
