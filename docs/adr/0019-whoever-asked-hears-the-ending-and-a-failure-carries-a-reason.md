# A Goal's ending is heard by whoever asked, and a Failure carries a Reason

An Agent that asked another for a Goal heard nothing back, and a `FAILED` Plan could not read why its Goal failed. Every answer was a Message written by hand, and in the showcase `WHEN bring FAILED` told the Guest `sold_out` whatever had gone wrong. We now decide two things together (spec 05, 07, 11, 20).

**Whoever asked hears the four endings**, an Agent as a Director already did. The Trigger is the Goal's ending with `BY`, which names the Agent who pursued it: `WHEN bring(?dish) FAILED BY waiter ?s`. `FROM` after a Goal's ending keeps one meaning, who asked for it, and `BY` has the other, who pursued it. A Plot, which used `FROM` for the pursuer, moves to `BY`.

**A Failure made on purpose can carry a Reason**: `FAIL WITH sold_out(?dish)`, read by `WHEN g FAILED WITH sold_out(?dish)`. The Reason is a declared Event, spelled like a Subplot's Outcome. It travels unchanged to every Goal that fails because of it and to whoever asked. A Failure nobody chose (a refused Action, arithmetic, no applicable Plan) has no Reason, and its cause stays in the Trace.

Chapter 07 had kept replies for a later version because `FROM` on `FAILED` could not mean both the asker and the replier. `BY` removes that clash, so the endings could come in now and the rest of cooperation (`REFUSE`, `AGREED`, waiting on an `ASK`) can still be added in the same shape.

## Considered Options

- **Built-in names for the causes** (`FAILED WITH no_plan`, `WITH refused`): a Plan could tell every way of failing apart, but eight words about how the runtime works would enter the language, and a designer mostly wants to tell a Failure they meant from one they didn't. Plain `FAILED` after the `WITH` Plans says exactly that.
- **`BECAUSE ?why`, the reason as a Value**: one Plan could read any reason, but a reason with arguments (`sold_out(?dish)`) is not a Value, and the Transpiler could not check a reason against the recipes that give it.
- **A marker on the Trigger** (`WHEN ASKED bring FAILED FROM ?s`): no new clause, but `FROM` would mean the asker in one Trigger and the pursuer in the next.
- **One Trigger for both**, with nothing to tell a Goal of one's own from one that was asked: an Agent that pursues `bring` and also asks for it could not tell which ended.
- **Waiting on an `ASK`** (`, AND WAIT`): it would let a Body read as a list of steps across Agents, but a Failure and a drop would then spread from one Agent to another, a Role recipient would mean waiting on many, and the asked Agent may leave. Deferred; ADR 0005 stands.

## Consequences

- The showcase's done-Signals, `took_seat` and the hand-written `sold_out` Message are no longer needed. A refusal is `FAIL WITH …` in a `TO g FROM …` Plan.
- A Body still can't wait on an `ASK`. A Plan that goes on only when the asked Goal is over is split into the `ASK` and a `WHEN g ENDED BY …` Plan.
- `WHEN g FAILED` Plans with and without `WITH` share one Trigger, tried in written order, as a Subplot's `ENDED WITH` Blocks are.
- A Goal in a chain can't replace the Reason it passes on, and there is no catch-all `WITH ?why`.
- The Reasons a Goal can fail with are part of the inferred Interface (ADR 0015), and a `FAILED WITH` that names one the Goal never fails with is a warning.
- The Targets must carry the Reason along the failure chain and send the report of an ending from Agent to Agent, as they already do from Agent to Director.
- ADR 0007 is unchanged: every ending is still a notification, also when heard by the asker.
