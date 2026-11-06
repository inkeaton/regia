# Plan failure and fallback

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 05

## Question

What happens when things go wrong (Q4b)? An Action fails, a Goal can't be reached, or no Plan applies to an Event. Does Regia expose failure handling (like ASL `-!` plans), and how would a designer write a fallback? What is the default behaviour when nothing handles a failure?

## Answer

Spec chapter: `docs/spec/11-failure.md`. ADR 0007 (`FAILED` notifies, it does not rescue). Glossary: *Failure* and *Trace* added; *Trigger*, *Trigger kind* and *Basic Action* updated.

- **Causes:** the runtime cases from chapters 04, 07, 08 and 09, plus a **Custom Action the Target reports as failed** (Regia never checks the world; with no reports, Actions succeed) and the new Basic Action **`FAIL.`** (no argument). The no-ops and an all-zero Random choice are not failures.
- **A failed Plan stops at the Statement**, and nothing is undone.
- **It spreads:** a failed `TO g` Plan fails `g`, and every Body waiting on `g` fails, up the chain; `WITHOUT WAITING` stops the spread. A failed `WHEN` Plan just stops. There is **no automatic retry** of another `TO g` Plan.
- **No Plan applies:** an Event or Fact change is ignored (normal). A Goal **fails at once**, however it was given.
- **`WHEN g FAILED:`** is a real Trigger kind and a **notification, not a rescue**: waiters have already failed (ADR 0007). Every level of a chain fires, innermost first. It has no reason clause. `FROM` on `FAILED`/`DROPPED` means the Goal's Sender. A failing `FAILED`/`DROPPED` Plan just stops.
- **Every Goal that stops unreached fires exactly one of `DROPPED`/`FAILED`.** `DROP`'s stopped sub-Goals fire their own `DROPPED`, innermost first.
- **Trace:** every failure (handled or not) and every runtime warning leaves a trace entry that can say what failed, why (Statement and source location), and what failed in turn. The language fixes what a trace explains; the Target decides format, routing and monitoring.
- **Transpiler warnings:** a Goal with no `TO` Plan in the Program; Statements after `FAIL.`. No warning for `GIVEN`s without `ELSE`.
- **Handed off:** trace format and runtime monitoring to *The full ASL mapping* fog; a failing Director Plan to *Director capabilities*; timeouts to *Time and timers*; the clash between `FROM` on local `FAILED` and the reserved reply `FAILED FROM ?who` to the cooperation fog.

## Comments

- From *Numbers and arithmetic* (04): Body arithmetic on a non-Number, or division by zero, makes the Plan fail at runtime. This ticket decides what that failure does. See `docs/spec/04-numbers-and-expressions.md`.
- From *Goals and Trigger kinds* (05): a "Goal fails" Trigger kind is reserved (e.g. `WHEN g FAILED:`); decide whether it exists. Also what happens when a Goal is pursued and no `TO` Plan applies. A Goal is reached when its `TO` Plan finishes. See `docs/spec/05-goals-and-triggers.md`.
- From *Context vs control flow* (06): a Trigger with `GIVEN` Blocks and no `ELSE`, where no Context holds, is a "no Plan applies" case. See `docs/spec/06-context-and-control-flow.md`.
- From *Context vs control flow* (06): on Targets without a native `if`, an `IF` becomes an internal subgoal (`regia_if_N`). A failure inside a branch must behave exactly like a failure of the Plan itself, and designers must never see or handle the internal goal.
- From *Messaging between Agents* (08): a `TELL`/`ASK` whose recipient Placeholder holds something that isn't an Agent fails the Plan; an asked Goal with no applicable `TO` Plan is a "no Plan applies" case, and in a future cooperation system it would reply `REFUSED` or `FAILED` to the asker. `FAILED` is reserved as a Goal kind word for those replies too, so keep the two meanings compatible. See `docs/spec/07-messaging.md`.
- From *Basic Action set* (07): new ways a Plan fails: `CHANGE f TO f2` when `f` isn't known, and a Body waiting on `PURSUE g.` when `g` is dropped (or its recipe fails). Also decide whether Goals stopped by a `DROP` (sub-Goals the dropped Plan was waiting on) fire their own `DROPPED`, what a stopped Plan leaves behind, and whether there is a Basic Action that fails a Plan on purpose. See `docs/spec/08-basic-actions.md`.
- From *Groups* (09): a Random choice weight that isn't a Number fails the Plan; a negative or all-zero weight does **not** fail, it logs a runtime warning and carries on. If this ticket introduces a general notion of runtime warnings vs failures, check it against these. See `docs/spec/09-random-choice.md`.
