# Failure

What happens when a Plan can't carry out a Statement, how a Goal fails, how a designer reacts to it, and the trace every failure leaves behind. Decided in the ticket *Plan failure and fallback* (`.scratch/regia-2/issues/11-plan-failure.md`). It builds on chapters 04–09. The choice to make `WHEN g FAILED` a notification instead of a rescue is recorded in `docs/adr/0007-failed-notifies-it-does-not-rescue.md`. That a dropped Goal no longer fails the Body waiting on it, and the check on a retry, were decided in the ticket *A Goal's life: reached, dropped, repeated* (`.scratch/regia-revision/issues/02-goal-lifecycle.md`), with ADR 0018. Reasons (`FAIL WITH`, `FAILED WITH`) were decided in the ticket *Failure a Plan can read, and answers to an `ASK`* (`.scratch/regia-revision/issues/03-failure-and-replies.md`), with ADR 0019.

## When a Plan fails

A Plan **fails** when one of its Statements can't be carried out:

| Cause | Chapter |
|---|---|
| Body arithmetic on something that isn't a Number, or a division by zero | 04 |
| A Weight that isn't a Number | 09 |
| A `WAIT` Duration that isn't a Number | 12 |
| A `TELL` or `ASK` whose Recipient Placeholder isn't an Agent | 07 |
| `UPDATE f TO f2` when `f` isn't known | 08 |
| A Custom Action that the game refuses, or reports as failed while the `DO` waits | 08, here |
| `PURSUE g` waiting on a Goal that fails | 08, here |
| `FAIL` and `FAIL WITH r` | here |

- **Custom Actions** fail only when the Target, or the game behind it, reports that they failed. Regia never checks the world itself. On a Target that never reports failure, every Custom Action succeeds. A `DO … , WITHOUT WAITING` fails only if the game refuses the Action; a later failure is only traced (chapter 08).
- **Nothing else to do with time fails.** 2.0 has no timeout clauses (chapter 12): the limit of a `WAIT … UNTIL` running out lets the Body carry on, an `AFTER` is a Trigger, and a Plan stopped during a `WAIT` just stops.
- The no-ops of chapter 08 (learning a known Fact, forgetting an unknown one, dropping a Goal that isn't pursued) and an all-zero Random choice (chapter 09) are **not** failures.
- **Calling off is not a failure.** A Plan stopped while it waits in `DO` calls its Action off (chapter 08), and nothing fails because of it.
- **A drop is not a failure.** A Body waiting on a Goal that is dropped stops, and its own Goal is dropped with it (chapter 08, ADR 0018).

### What a failed Plan leaves behind

The Plan **stops at the failing Statement**, and the rest of its Body doesn't run. **Nothing is undone**: Facts already learned or forgotten stay that way, Messages already sent stay sent, Custom Actions already done stay done, and Goals started `WITHOUT WAITING` keep going.

## How failure spreads

- **A failed `TO g` Plan fails `g`.** The Goal stops being pursued without being reached.
- **The Body waiting on `g`** with `PURSUE g` then fails as well, and so on up the chain of waiting Plans. A Pursuit has at most one Body waiting on it (chapter 05).
- **A Reason travels with it**, unchanged, to every Goal in the chain (see *Reasons*).
- **`WITHOUT WAITING` stops the spread.** A Body that started `g` without waiting carries on whatever happens to `g`.
- **A failed `WHEN` Plan** has nobody waiting on it, so it just stops.
- **No automatic retry.** When a `TO g` Plan fails, Regia doesn't try another `TO g` Plan, even if a later `GIVEN` would now hold. `g` fails. A second attempt has to be written out (see *Writing a fallback*).

```regia
TO dinner:
    PURSUE find_food         # find_food fails here …
    DO eat_food              # … so this never runs, and dinner fails too

TO find_food:
    GIVEN food_nearby(?f):
        DO pick_up(?f)
    # no ELSE: with no food nearby, find_food fails at once
```

## When no Plan applies

- **A Cue, or a Fact learned or forgotten**, that no Plan applies to is simply ignored. This is normal and isn't a failure: most Agents ignore most Cues.
- **A Goal with no applicable `TO` Plan fails at once.** That covers a Goal with no `TO` Plan at all, and one where every recipe the Agent holds lets it fall through: every `GIVEN` is false and there is no `ELSE` (chapters 06 and 13). A recipe whose `GIVEN`s all fail doesn't fail the Goal by itself; a recipe for the same Goal in another Playbook the Agent holds, ranked after it, still gets its turn. This holds however the Goal was given: by `PURSUE`, by `ASK` from another Agent, or by a Director.

## `FAIL`

`FAIL` is a Basic Action that fails the current Plan on purpose. Like every Basic Action it is written without `DO`. It may give a Reason: `FAIL WITH sold_out(?dish)` (next section).

```regia
TO buy(?item):
    GIVEN gold(?g) AND price(?item, ?p):
        IF ?g < ?p:
            FAIL
        UPDATE gold(?g) TO gold(?g - ?p)
        DO take(?item)
```

- In a `TO g` Plan it fails `g`, which then spreads as above. In a `WHEN` Plan it just stops the Plan.
- It can appear anywhere a Statement can, and usually sits in an `IF` branch or a Random choice Option.
- It is worded like its Trigger kind: `FAIL`/`FAILED`, the same pattern as `LEARN`/`LEARNED` and `DROP`/`DROPPED`.

## Reasons

A **Reason** is a Cue that a Plan gives when it fails on purpose. It says why, in the designer's words, to the Plans that react.

```regia
CUE sold_out(dish)

TO fetch(?dish):
    GIVEN in_kitchen(?dish):
        DO pick_up(?dish)
    ELSE:
        FAIL WITH sold_out(?dish)

TO bring(?dish), FROM patron ?guest:
    PURSUE fetch(?dish)                      # fails WITH sold_out(?dish) when fetch does
    DO walk_to(?guest)

WHEN bring(?dish) FAILED WITH sold_out(?dish):
    DO cross_off(?dish)

WHEN bring(?dish) FAILED:                    # every other Failure of bring
    DO shrug
```

- **`FAIL WITH <event>`** takes exactly one Cue declared in the Vocabulary, with its arguments filled, as `END PLOT WITH` does (chapter 17). The Cue is not sent to anyone and triggers no `WHEN sold_out` Plan: it only rides on the Failure.
- **Only `FAIL WITH` gives a Reason.** A Failure from any other cause in the table above (a refused Action, arithmetic, no applicable `TO` Plan, a plain `FAIL`) has none. Those causes are in the Trace and are not words of the language.
- **The Reason travels unchanged** up the chain of waiting Plans: every Goal that fails because of it fails with the same Reason, and so does the report to whoever asked (chapters 05, 07, 20). A Goal in the chain can't replace or drop it in 2.0.
- **`WHEN g FAILED WITH <event>:`** matches a Failure with that Reason, filling Placeholders as any Trigger does (chapter 03). `WITH` comes straight after `FAILED`, before `FROM` or `BY` (chapter 05).
- **One Trigger, first match wins.** The `WHEN g FAILED` Plans of one Playbook, with and without `WITH`, share a Trigger and are tried in written order; the first that matches runs, as for the `FINISHED` Plans of a Subplot's ending, whose plain `FINISHED` works the same way (chapter 17). A plain `FAILED` matches every Failure, with a Reason or without. Written above a `WITH` Plan it shadows it, with a warning (`R11_06-shadowed-failed-with`).
- **No catch-all for Reasons.** There is no `WITH ?why`: a Reason is a Cue, not a Value (chapter 03). Plain `FAILED` is the catch-all.
- `WITH` goes only on `FAILED`. On `REACHED`, `DROPPED` and `ENDED` it is an error; a Plan that cleans up under `ENDED` and needs the Reason records it from its `FAILED WITH` Plan, which runs first.
- **In a `WHEN` Plan**, `FAIL WITH` is allowed. Nobody hears a `WHEN` Plan fail, so the Reason only reaches the Trace.
- A Quota and `WITH` on one Trigger is an error in 2.0 (chapter 18).
- A local Cue of a Playbook can be a Reason (chapter 10).
- The Transpiler works out which Reasons each Goal can fail with, and warns on a `FAILED WITH` that names one the Goal never fails with (chapter 38).
- **A refusal is a Failure with a Reason.** An asked Agent that won't do it writes `FAIL WITH …` in its `TO g, FROM …` Plan (chapter 07).

## Reacting: `WHEN g FAILED`

`FAILED` is a Trigger kind on Goals, shaped like `DROPPED` (chapter 05):

```regia
WHEN find_food FAILED:
    PURSUE beg_for_food, WITHOUT WAITING

WHEN avenge(?s) FAILED:
    LEARN fears(?s)
```

- It fires when the Goal fails for any reason in this chapter: a failed `TO` Plan, no applicable `TO` Plan, or a waited-on sub-Goal failing.
- **It is a notification, not a rescue.** By the time the `FAILED` Plan runs, every Body that was waiting on the Goal has already failed. Running a `FAILED` Plan doesn't make the Goal reached, and it doesn't let a waiting Body carry on. A Goal is still reached only when its `TO` Plan finishes (chapter 05). See ADR 0007.
- **Every level fires.** When a failure spreads up a chain of waiting Plans, each Goal in the chain fires its own `FAILED`, innermost first. In the example above, `WHEN find_food FAILED` fires, then `WHEN dinner FAILED`.
- **A Plan can read the Reason, not the cause.** `WHEN g FAILED WITH r` matches a Reason the designer gave (*Reasons*, above). Which Statement failed and how (the causes in the table at the top) is in the Trace only.
- **`FROM` means where the Goal's request came from**, as on `TO g, FROM …`: `WHEN find_sword FAILED, FROM DIRECTOR:` reacts only to a Goal the Director gave. The same applies to `REACHED`, `DROPPED` and `ENDED`. A Goal the Agent gave itself has no Sender and is `FROM ME` (chapter 05).
- A Plan for `FAILED`, or for any other ending, is not a Goal recipe. If it fails itself, it just stops and leaves a trace entry. Nothing else fires, so failures can't loop.
- **Whoever asked for the Goal hears `FAILED`**, with its Reason: an Agent or a Director, with `BY` (chapters 05, 20).
- **A failed `WHEN` Plan can't be reacted to.** It has no name to hang a Trigger on. A step that must be recoverable goes in a Goal of its own, pursued from the `WHEN` Plan.

### Writing a fallback

Since there is no rescue and no retry, a fallback is written as one of these:

- **another recipe, chosen up front**: several `GIVEN`s under one `TO g`, or an `ELSE`;
- **a fallback Goal started from `FAILED`**, as in `beg_for_food` above;
- **an `IF` before the risky step** that picks another way, or `FAIL`s cleanly.

### Trying again

A `FAILED` Plan may pursue the Goal that has just failed. That Pursuit is over, so the `PURSUE` starts a new one:

```regia
WHEN have_dinner FAILED:
    IF tries(?n) AND ?n < 3:
        UPDATE tries(?n) TO tries(?n + 1)
        PURSUE have_dinner, WITHOUT WAITING
```

Without the `IF`, a Goal that fails every time is pursued again for as long as the Program runs. A `WHEN g FAILED` Plan that pursues `g` with the Trigger's own arguments, with no `GIVEN` or `IF` around the `PURSUE`, gets a warning (`R11_03-endless-failure-retry`). There is no limit at runtime.

## Every Pursuit that ends fires its Triggers

A Pursuit fires **exactly one** of `REACHED`, `DROPPED` and `FAILED`, and then `ENDED` (chapter 05, *How a Pursuit ends*):

- `DROPPED` when it was dropped, including the Pursuits a `DROP` stops below it and above it (chapter 08).
- `FAILED` when it failed.
- `REACHED` when its recipe finished.

Cleanup that must run however the Goal ended is written once, under `WHEN g ENDED`.

## The trace

Every failure leaves a **trace entry**, whether or not a `FAILED` Plan handles it. A `FAILED` Plan only reacts, so the trace is the one place that explains *why*. A trace entry must be able to say:

- **what failed**: the Agent, and the Plan by its Trigger and source location;
- **the cause**: the Statement, by source location, and one of the causes in the table above, or "no applicable `TO` Plan"; and the Reason, when `FAIL WITH` gave one;
- **the chain**: each Goal that failed in turn because of it, and each waiting Plan that stopped.

Runtime warnings (negative or all-zero Weights, chapter 09; negative Durations, chapter 12) go in the same trace, marked as warnings, since the Plan carries on.

The language fixes **what** a trace can explain, and chapter 34 fixes its entries, their codes, and how the chain is written (one linked entry per level). Only how it is written belongs to the Target (Jason: chapter 35). The Transpiler's duty is to pass each Target the names and source locations it needs. Future runtime monitoring builds on this trace.

## Transpiler checks

**Errors**

- `R11_04-misused-fail-with` `FAIL WITH` something other than one declared Cue, or with unfilled arguments.
- `R11_05-with-on-wrong-trigger` `WITH` on `REACHED`, `DROPPED` or `ENDED` after a Goal's name.

**Warnings**

- `R11_01-goal-without-plan` A Goal that is pursued, asked or declared, but has no `TO` Plan anywhere in the Program. It would always fail.
- `R11_02-statement-after-fail` Statements after `FAIL` in the same Block, which can never run.
- `R11_03-endless-failure-retry` A `WHEN g FAILED` Plan that pursues `g` with the Trigger's own arguments and no `GIVEN` or `IF` around the `PURSUE`: it retries without end.
- `R11_06-shadowed-failed-with` A plain `WHEN g FAILED` Plan written above a `WHEN g FAILED WITH …` Plan it also matches, which can then never run.

There is no warning for a `TO` Plan with `GIVEN`s and no `ELSE`. Failing when no Context holds is often intended, and a warning there would fire on most recipes.

## Trace entries

**Failures**

- `T11_01-failed-custom-action` A Custom Action that the game refuses, or reports as failed while the `DO` waits.
- `T11_02-pursued-goal-failed` `PURSUE g` waiting on a Goal that fails.
- `T11_03-explicit-fail` `FAIL`, with its Reason when `FAIL WITH` gave one.
- `T11_04-goal-found-no-plan` A Goal with no applicable `TO` Plan.

The other causes in the table above have their codes in their own chapters: `T04_01-operand-not-number`, `T04_02-division-by-zero`, `T07_01-recipient-not-agent`, `T08_01-update-of-unknown-fact`, `T09_01-weight-not-number`, `T12_01-duration-not-number`.

## Reserved words

Every keyword is listed in chapter 01, *Reserved words* (`01-statements-and-blocks.md`).

## ASL mapping notes

The Jason mapping is chapter 40 (`40-jason-goal-life.md`); the Statements are in chapter 39. What any AgentSpeak Target must respect:

- `FAIL WITH r` must carry `r` to the failure handling of every Goal in the chain (and, after 1.5, to the report sent to whoever asked). Jason: `.fail(regia_fail, regia_reason(r))`, passed on by each generated `-!g`.
- So that **every level fires `FAILED`** and the failure isn't rescued, the Transpiler generates a failure plan for every Goal. It runs the designer's `FAILED` and `ENDED` Plans, writes the trace entry, and then fails again up to the next level. In Jason that plan has the context `true` and no Givings guard, since a `-!g` plan whose context is false drops the whole intention (chapter 40).
- `WITHOUT WAITING` (`!!g`) runs on its own intention, so its failure doesn't reach the starter, as required.
- On Targets without a native `if`, a failure inside a generated `regia_if__N` or `regia_randomly__N` plan must be passed straight through as the Plan's own failure, with no `FAILED` and no trace entry for the generated goal (chapter 06). Trace entries name the designer's Plan and Statement, never generated names.
- Every Pursuit a `DROP` stops, below and above the dropped one, needs generated `DROPPED` and `ENDED` events, as for the dropped Goal itself. A reached Goal needs generated `REACHED` and `ENDED` events, and a failed one `ENDED` after its `FAILED` Plans.
- Custom Action failure comes from the game's `refused` or `failed` reply to `regia.act` (chapter 37).

## Regia 1.5

In 1.5 (ADR 0025), except what reaches the asker: nobody hears `FAILED` for a Goal it asked, and a Reason travels only up the Agent's own chain of waiting Plans. `FAIL WITH`, `FAILED WITH`, `R11_04-misused-fail-with`, `R11_05-with-on-wrong-trigger`, `R11_06-shadowed-failed-with` and the Trace entries are in.

For the ASL mapping, `FAIL WITH r` carries `r` to the generated `-!g` plans of the chain, and to no report (chapter 40).

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- Format, routing and monitoring of the trace: chapter 34 (entries, codes, behaviour cases) and chapter 35 (Jason).
- A failing Director Plan stops with a Trace entry and leaves its Phase and Staging untouched; Director Statements never fail (chapter 20).
- Reacting to how a `DO a, WITHOUT WAITING` ended, built-in names for the causes, and a Goal that replaces the Reason it passes on: after 2.0.
