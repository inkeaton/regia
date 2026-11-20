# When a Giving starts and ends, and what a joiner gets

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

What can react to a Playbook being given or taken, can a Giving or a Subplot be tied to a Phase, and how do a setup, a standing `ASSIGN` and a one-off Message treat an Agent that arrives late?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- N2 A Giving has no start and no end that anything can react to
- D7 A Giving is standing and a Message is sent once
- B3 The Role setups run before the first Phase starts counting

Decide:

- Triggers for a Playbook given and taken away, and what happens to its Goals and Local Facts when it goes.
- A Giving or a Subplot that lasts as long as a Phase.
- Whether a Director can call off a Goal it asked for.
- One rule for what a joiner receives, and whether a setup can depend on the Phase.
- The order of Role setups and the entry of the initial Phase.
- What happens to the `DROPPED` and `ENDED` Plans of a Goal dropped by an `UNASSIGN` when they sit in the Playbook taken away (from [*A Goal's life: reached, dropped, repeated*](02-goal-lifecycle.md)).

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

## Resolution

Resolved on 2026-11-16, with the user.

- **N2, fixed.** A Playbook reacts to being given and taken with `WHEN ASSIGNED:` and `WHEN UNASSIGNED:`, which fire on its first Giving arriving and its last one going, whatever took it (an `UNASSIGN`, a Phase left, a Staging ending). A Playbook taken away now **closes**: its Plans stop, the `DROPPED` and `ENDED` Plans of the Goals dropped still run, then `UNASSIGNED`, and nothing else of the Playbook starts. This answers the question handed on by [*A Goal's life: reached, dropped, repeated*](02-goal-lifecycle.md). Local Facts stay unless a closing Plan forgets them. A Giving or a Subplot lasts a Phase with a trailing `, UNTIL EXITED` on `ASSIGN` and `START SUBPLOT`, or by being in the Phase's Role setup (D7). **Deferred**: a Director calling off a Goal it asked, with replies and refusals (F3). Until then the Goal's recipe goes in a Playbook given for the Phase.
- **D7, fixed for the setup, kept for the rest.** A `DURING <phase>` Block may hold `ROLE … STARTS WITH:` Blocks. A Phase's setup runs for every Agent of the Role at entry and for whoever joins during the Phase, and its Givings are taken away at exit. So a latecomer in `feast` is asked to dine, and one in `farewell` isn't sent to its seat. **Kept**: a whole-Role `ASSIGN` in a Plan is standing and a Message is a one-off, because a Giving is a state and a Message is something that happened. `UNASSIGN` reaches a Phase setup's Giving as it reaches the Plot's.
- **B3, fixed.** A Phase is current and counting before anything is sent on its behalf. At Staging start: `DURING PLOT` and the initial Phase become active, the Plot's setups run, then the initial Phase's, then `DURING PLOT`'s `ENTERED`, then the Phase's. A `TRANSITION` stops the old Phase's Plans, runs `EXITED`, takes away what was given for the Phase, changes the Phase, runs the new setups, then `ENTERED`. A joiner gets the Plot's setup, the current Phase's setup, the standing Givings, then `JOINED`.

Settled while writing, not asked: a closing Plan's `TELL` and `SIGNAL` go through the Givings as they were just before the taking, and a Director whose Staging has ended hears nothing.

Changed:

- Spec: chapters 05, 10, 15, 16, 17, 18, 19 and 20, and a note at the head of *Taking a Playbook away* in chapter 29. New codes: `R1508`, `R1509`, `R1606`, `R1607`.
- ADRs: 0021 *A Playbook taken away still runs its closing Plans*; 0022 *A Phase may carry Role setups, and a Giving stays standing*.
- Glossary: *Role setup*, *Giving* and *Trigger kind* reworded.

Handed on:

- The words `ASSIGNED`, `UNASSIGNED` and `UNTIL` are open to [*Words and syntax*](20-words-and-syntax.md).
- `UNASSIGN P FROM ?who` still takes every Giving of `P` the Agent holds from this Staging, a setup's included (F2): [*Telling Stagings and Givings apart*](08-stagings-and-casts.md).
- The Jason chapters 29, 30 and 31 don't yet describe the closing state of a Playbook, the generated `ASSIGNED` and `UNASSIGNED` events, Givings marked with a Phase, Phase setups inside a transition, or counts started before the setups.
- The guide's *Playbooks and Roles*, *Quotas and Cast Changes*, *Subplots and Stagings* and the showcase still have the paired `UNASSIGN`s, the `JOINED` Plan that repeats an `ASK`, and `take_seat` in the Plot's setup.

1.5, from [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md):

- N2 in. D7 in, except what a joiner gets: there is no joining in 1.5. B3 in for the order of setups and `ENTERED`; the counting part goes with Quota Triggers, later.
