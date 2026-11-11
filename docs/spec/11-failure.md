# Failure

What happens when a Plan can't carry out a Statement, how a Goal fails, how a designer reacts to it, and the trace every failure leaves behind. Decided in the ticket *Plan failure and fallback* (`.scratch/regia-2/issues/11-plan-failure.md`). It builds on chapters 04–09. The choice to make `WHEN g FAILED` a notification instead of a rescue is recorded in `docs/adr/0007-failed-notifies-it-does-not-rescue.md`.

## When a Plan fails

A Plan **fails** when one of its Statements can't be carried out:

| Cause | Chapter |
|---|---|
| Body arithmetic on something that isn't a Number, or a division by zero | 04 |
| A Weight that isn't a Number | 09 |
| A `WAIT` Duration that isn't a Number | 12 |
| A `TELL` or `ASK` whose Recipient Placeholder isn't an Agent | 07 |
| `CHANGE f TO f2.` when `f` isn't known | 08 |
| A Custom Action that the Target reports as failed | here |
| `PURSUE g.` waiting on a Goal that is dropped or fails | 08, here |
| `FAIL.` | here |

- **Custom Actions** fail only when the Target, or the game behind it, reports that they failed. Regia never checks the world itself. On a Target that never reports failure, every Custom Action succeeds.
- **Nothing else to do with time fails.** 2.0 has no timeouts (chapter 12), and a Plan stopped during a `WAIT` just stops.
- The no-ops of chapter 08 (learning a known Fact, forgetting an unknown one, dropping a Goal that isn't pursued) and an all-zero Random choice (chapter 09) are **not** failures.

### What a failed Plan leaves behind

The Plan **stops at the failing Statement**, and the rest of its Body doesn't run. **Nothing is undone**: Facts already learned or forgotten stay that way, Messages already sent stay sent, Custom Actions already done stay done, and Goals started `WITHOUT WAITING` keep going.

## How failure spreads

- **A failed `TO g` Plan fails `g`.** The Goal stops being pursued without being reached.
- **Every Body waiting on `g`** with `PURSUE g.` then fails as well, and so on up the chain of waiting Plans. If several Bodies joined the same pursuit (chapter 08), all of them fail.
- **`WITHOUT WAITING` stops the spread.** A Body that started `g` without waiting carries on whatever happens to `g`.
- **A failed `WHEN` Plan** has nobody waiting on it, so it just stops.
- **No automatic retry.** When a `TO g` Plan fails, Regia doesn't try another `TO g` Plan, even if a later `GIVEN` would now hold. `g` fails. A second attempt has to be written out (see *Writing a fallback*).

```regia
TO dinner:
    PURSUE find_food.        # find_food fails here …
    DO eat_food.             # … so this never runs, and dinner fails too

TO find_food:
    GIVEN food_nearby(?f):
        DO pick_up(?f).
    # no ELSE: with no food nearby, find_food fails at once
```

## When no Plan applies

- **An Event, or a Fact learned or forgotten**, that no Plan applies to is simply ignored. This is normal and isn't a failure: most Agents ignore most Events.
- **A Goal with no applicable `TO` Plan fails at once.** That covers a Goal with no `TO` Plan at all, and one where every `GIVEN` is false and there is no `ELSE` (chapter 06). This holds however the Goal was given: by `PURSUE`, by `ASK` from another Agent, or by a Director.

## `FAIL`

`FAIL.` is a Basic Action that fails the current Plan on purpose. It takes no argument, and like every Basic Action it is written without `DO`.

```regia
TO buy(?item):
    GIVEN gold(?g), price(?item, ?p):
        IF ?g < ?p:
            FAIL.
        CHANGE gold(?g) TO gold(?g - ?p).
        DO take(?item).
```

- In a `TO g` Plan it fails `g`, which then spreads as above. In a `WHEN` Plan it just stops the Plan.
- It can appear anywhere a Statement can, and usually sits in an `IF` branch or a Random choice Option.
- It is worded like its Trigger kind: `FAIL`/`FAILED`, the same pattern as `LEARN`/`LEARNED` and `DROP`/`DROPPED`.

## Reacting: `WHEN g FAILED`

`FAILED` is a Trigger kind on Goals, shaped like `DROPPED` (chapter 05):

```regia
WHEN find_food FAILED:
    PURSUE beg_for_food, WITHOUT WAITING.

WHEN avenge(?s) FAILED:
    LEARN fears(?s).
```

- It fires when the Goal fails for any reason in this chapter: a failed `TO` Plan, no applicable `TO` Plan, or a waited-on sub-Goal failing.
- **It is a notification, not a rescue.** By the time the `FAILED` Plan runs, every Body that was waiting on the Goal has already failed. Running a `FAILED` Plan doesn't make the Goal reached, and it doesn't let a waiting Body carry on. A Goal is still reached only when its `TO` Plan finishes (chapter 05). See ADR 0007.
- **Every level fires.** When a failure spreads up a chain of waiting Plans, each Goal in the chain fires its own `FAILED`, innermost first. In the example above, `WHEN find_food FAILED` fires, then `WHEN dinner FAILED`.
- **The reason is not part of the Trigger.** There is no `BECAUSE ?why`: a Plan reacts to the fact *that* the Goal failed, and can use the Goal's own Placeholders (`?s` above). The reason is in the trace.
- **`FROM` means the Goal's Sender**, as on `TO g FROM …`: `WHEN find_sword FAILED FROM DIRECTOR:` reacts only to a Goal the Director gave. The same applies to `DROPPED`. A Goal the Agent gave itself has no Sender (chapter 05).
- A Plan for `FAILED` or `DROPPED` is not a Goal recipe. If it fails itself, it just stops and leaves a trace entry. Nothing else fires, so failures can't loop.

### Writing a fallback

Since there is no rescue and no retry, a fallback is written as one of these:

- **another recipe, chosen up front**: several `GIVEN`s under one `TO g`, or an `ELSE`;
- **a fallback Goal started from `FAILED`**, as in `beg_for_food` above;
- **an `IF` before the risky step** that picks another way, or `FAIL.`s cleanly.

## Every Goal that stops fires one Trigger

A Goal that stops being pursued without being reached fires **exactly one** of `DROPPED` or `FAILED`:

- `DROPPED` when it was dropped, including the sub-Goals a `DROP` stops (chapter 08, step 2). They fire innermost first, then the dropped Goal's own `DROPPED`.
- `FAILED` when it failed.

A Goal that is reached fires neither. So a cleanup Plan for a Goal always runs, however the Goal ended.

## The trace

Every failure leaves a **trace entry**, whether or not a `FAILED` Plan handles it. A `FAILED` Plan only reacts, so the trace is the one place that explains *why*. A trace entry must be able to say:

- **what failed**: the Agent, and the Plan by its Trigger and source location;
- **the cause**: the Statement, by source location, and one of the causes in the table above, or "no applicable `TO` Plan";
- **the chain**: each Goal that failed in turn because of it, and each waiting Plan that stopped.

Runtime warnings (negative or all-zero Weights, chapter 09; negative Durations, chapter 12) go in the same trace, marked as warnings, since the Plan carries on.

The language fixes **what** a trace can explain, and chapter 34 fixes its entries, their codes, and how the chain is written (one linked entry per level). Only how it is written belongs to the Target (Jason: chapter 35). The Transpiler's duty is to pass each Target the names and source locations it needs. Future runtime monitoring builds on this trace.

## Transpiler checks

- **Warning:** a Goal that is pursued, asked or declared, but that has no `TO` Plan anywhere in the Program. It would always fail.
- **Warning:** Statements after `FAIL.` in the same Block, which can never run.
- There is no warning for a `TO` Plan with `GIVEN`s and no `ELSE`. Failing when no Context holds is often intended, and a warning there would fire on most recipes.

## Reserved words

`FAIL`, and the kind word `FAILED` (no longer only reserved).

## ASL mapping notes

For *The full ASL mapping* to pick up:

- `FAIL.` maps to `.fail`.
- Jason already fails a sub-goal when no plan is applicable, and fails the plan when arithmetic or an action fails. If an `-!g` event has no plan, it drops the whole intention without generating `-!parent`. So that **every level fires `FAILED`**, the Transpiler generates an `-!g` plan for every declared Goal. That plan runs the designer's `WHEN g FAILED` Plans, if any, writes the trace entry, and then calls `.fail` again, so the failure keeps spreading (notification, not rescue) up to `-!parent`. This behaviour should be checked against Jason's failure-handling semantics when the mapping is written.
- A Body that joined an existing pursuit (chapter 08) waits on a completion event and must be failed explicitly when the joined Goal fails, as for `DROP`.
- `WITHOUT WAITING` (`!!g`) runs on its own intention, so its failure doesn't reach the starter, as required.
- On Targets without a native `if`, a failure inside a generated `regia_if__N` or `regia_either__N` plan must be passed straight through as the Plan's own failure, with no `FAILED` and no trace entry for the generated goal (chapter 06). Trace entries name the designer's Plan and Statement, never generated names.
- Stopped sub-Goals of a `DROP` need generated `DROPPED` events, as for the dropped Goal itself.
- Custom Action failure comes from the environment's action feedback (Jason's `executeAction` result). Whether VEsNA reports it is a Target question.

## Not decided here

- Format, routing and monitoring of the trace: chapter 34 (entries, codes, behaviour cases) and chapter 35 (Jason).
- A failing Director Plan stops with a Trace entry and leaves its Phase and Staging untouched; Director Statements never fail (chapter 20).
- Replies to an asker when an asked Goal fails, and their wording now that `FROM` on `FAILED` means the Goal's Sender: *Agent cooperation* fog.
