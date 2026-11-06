# Context and control flow

How a Plan's Context is written, how several Plans share one Trigger, and how `IF`/`ELSE` work inside a Body. Decided in the ticket *Context vs control flow* (`.scratch/regia-2/issues/06-context-vs-control-flow.md`). It builds on chapters 01, 03, 04 and 05, and replaces the context and `IF` parts of primer ch.4. The choice to split the Context from `IF` is recorded in `docs/adr/0004-given-is-the-context-if-is-control-flow.md`.

## Two different questions

A Plan asks two kinds of question, at two different times:

- **The Context**, written after `GIVEN`, is checked **once, when the Plan is chosen**, before any of its Body runs. If it doesn't hold, the Plan is not chosen at all.
- **An `IF`** is a Statement in the Body. It is checked **when the Body reaches it**, after every Statement before it has run, and only picks which Statements run next. The Plan has already been chosen.

```regia
WHEN food_served:
    GIVEN is_hungry:
        DO PRINT("A guest notices food arriving.").
        LEARN served.
        IF NOT hates(host):          # checked now, after the PRINT and the LEARN
            DO eat_food.
        ELSE:
            DO complain.
```

In 1.0 an `IF` directly under a `WHEN` was the Context. In 2.0 that is `GIVEN`, and `IF` always means control flow.

## Conditions

A Context and an `IF` condition are written the same way and can test the same things: Facts, `PURSUING g` (chapter 05), comparisons (chapter 04), with Values and Placeholders (chapter 03).

| Operator | Meaning | Binds |
|---|---|---|
| comparisons `< > <= >= =` | chapter 04 | tightest |
| `NOT x` | `x` doesn't hold | |
| `x AND y` | both hold | |
| `x OR y` | at least one holds | loosest |
| `( … )` | grouping | |

- `NOT` applies to the single item after it: `NOT a AND b` means `(NOT a) AND b`. Write `NOT (a AND b)` to negate both.
- **Mixing `AND` and `OR` at one level without parentheses is an error.** `a OR b AND c` is rejected with a hint suggesting `a OR (b AND c)` or `(a OR b) AND c`. A chain of only `AND`s or only `OR`s needs no parentheses.
- Testing an Event is an error (chapter 05).

## Plans under one Trigger

The Context is a Block header nested under the Trigger. One Trigger can head several Plans:

```regia
WHEN fan_greets:
    GIVEN happy:
        DO greet_back.
    GIVEN angry:
        DO curse.
    ELSE:
        DO ignore.
```

Each `GIVEN` Block, and the `ELSE` Block, is **one Plan**. The rules:

- **First match wins, top to bottom.** Of the `GIVEN` Blocks under one Trigger, only the **first in the text whose Context holds** runs. If none holds, the `ELSE` runs. This holds however the Plans end up ordered at runtime, and whatever other Playbooks react to the same Trigger. How Plans from different Trigger Blocks compete is decided in *Priority model*.
- **`ELSE` is optional** and must come last. Without it, if no Context holds, none of these Plans applies (what that means is decided in *Plan failure and fallback*). An `ELSE` with no `GIVEN` before it is an error.
- **A Trigger Block holds either a Body or `GIVEN`/`ELSE` Blocks, never both.** A `WHEN` whose Statements come straight after it is a single Plan with no Context. Statements before, between or after `GIVEN` Blocks are an error, and the message explains that the Context is checked before any Statement runs. 1.0's "prefix" Statements, which were copied into every branch, are gone: write the Statement in each Plan, or use one Plan with an `IF`.
- **What the Plans share.** Everything in the Trigger: the item, its kind word, the Placeholders it fills, `FROM`, and the Labels on the Trigger's header. Each Plan fills its own Context Placeholders, so sibling `GIVEN` Blocks may reuse a name. Whether a single `GIVEN` can carry its own Labels is decided in *Label syntax*.
- **Doc comments** (chapter 02). A doc comment above the Trigger documents every Plan under it. A doc comment above a `GIVEN` or `ELSE` documents only that Plan.
- **A `GIVEN` that can never run** gets a **warning**: one an earlier `GIVEN` always catches first, such as `GIVEN a AND b:` after `GIVEN a:`. The Transpiler checks this as far as it can (fully for plain Facts, best effort with Placeholders and comparisons). The fix is usually to move the narrower case up.
- The same rules apply to `TO` Triggers (Goal recipes), and to Plans in Playbooks and in Plots.

A one-Plan Trigger with a Context fits on one line with nested Inline blocks (chapter 01):

```regia
WHEN fan_greets: GIVEN happy: DO greet_back.
```

## `IF` in a Body

```regia
IF cond:
    …
ELSE IF cond:
    …
ELSE:
    …
```

- Any number of `ELSE IF`s, an optional final `ELSE`, nesting to any depth. If no branch is taken and there is no `ELSE`, the Body carries on after the `IF`.
- The condition is matched against the Agent's Facts and Goals **at that moment**. With several matches, one is used and the language doesn't say which (chapter 03).

### Placeholders in an `IF`

An `IF` condition **fills** Placeholders by matching, like a Context, with the same "only what's certainly filled" rules for `NOT` and `OR` (chapter 03).

- A Placeholder filled in an `IF` condition can be used **only inside that branch**. Not in the `ELSE IF`/`ELSE` branches, and not after the `IF`.
- **Sibling branches of one chain may reuse the name**, since only one of them runs: `IF hates(?x): … ELSE IF fears(?x): …`.
- **Reusing it anywhere else in the Plan is an error**, for example in a later, separate `IF`, or as a Placeholder filled in the Trigger or Context. The message suggests a different name. This keeps "filled once per Plan run" true.
- A Placeholder that was already filled (by the Trigger, the Context, or a named value earlier in the Body) is simply tested in an `IF` condition, as anywhere else.

```regia
WHEN insult_heard FROM ?speaker:
    IF hates(?speaker):              # tests the Sender, already filled
        DO curse(?speaker).
    ELSE IF friend_of(?speaker, ?f):
        DO complain_to(?f).          # ?f exists only in this branch
```

## Loops

There are no `WHILE` or `FOR` loops in 2.0. Repetition comes from a Plan pursuing its Goal again, or from reacting to Fact changes. Running a Body for every match of a condition belongs to *Match selection*, which is not yet specified. Loops are deferred, not ruled out.

## ASL mapping notes

For *The full ASL mapping* to pick up:

- `AND`/`OR`/`NOT` map to `&`/`|`/`not`, which have the same precedence.
- A body `IF` chain maps to Jason's `if (…) { … } elif (…) { … } else { … }`. Jason keeps variables bound in an `if` condition bound for the rest of the plan. The Placeholder rules above mean this never changes what a later condition tests, so no renaming is needed.
- Each `GIVEN` Block becomes its own ASL plan with the shared trigger. To keep "first match wins" independent of plan order (Playbooks loaded at runtime, a reordering priority model), the plan's context is its own Context **AND the negation of every earlier sibling's Context**: `ctx3 & not ctx1 & not ctx2`. The `ELSE` plan's context is the negation of all of them.
- In the negated copies, every Placeholder **not filled by the Trigger** gets a **fresh variable name**. Without this, `GIVEN hates(?x)` then `GIVEN fears(?x)` would emit `fears(X) & not hates(X)` ("someone I fear but don't hate") instead of "I hate nobody, and fear someone". Placeholders filled by the Trigger stay shared on purpose.
- **Targets without a native `if`** (the in-house AgentSpeak interpreters): each `IF` chain is lowered to an internal subgoal with one plan per branch. The Body posts `!regia_if_N(…)`, which waits until the branch finishes, and then carries on. The branch plans use the same encoding as `GIVEN`: each context negates the earlier siblings', with fresh names for Placeholders the subgoal doesn't receive. When no `ELSE` is written, an empty one is always generated, so "no branch taken" never fails the Plan. Every Placeholder filled before the `IF` and used in the condition or branch is passed as an argument; Placeholders filled in a branch's condition live only in that branch's plan, which is exactly the scoping rule above. Nesting is a subgoal posted from a branch plan.

  ```
  +insult_heard[source(Speaker)] : true <-
      frown; !regia_if_1(Speaker); leave.
  +!regia_if_1(Speaker) : hates(Speaker) <- curse(Speaker).
  +!regia_if_1(Speaker) : friend_of(Speaker, F) & not hates(Speaker) <- complain_to(F).
  +!regia_if_1(Speaker) : not hates(Speaker) & not friend_of(Speaker, F_1) <- true.
  ```

  This needs: generated goal names under a prefix designers can't declare, loaded and unloaded with their Playbook; a branch's failure propagating as the Plan's own failure, never visible to designers; the duplicate-Goal rule and `PURSUING` (chapter 05) applying to declared Goals only; and no Labels on generated plans, so mood-based selection never picks among branches. It costs one extra reasoning cycle per `IF`.
- If an interpreter can't suspend a plan on a subgoal, the fallback is to split the Plan at each `IF`, with each branch plan ending by posting a continuation goal that holds the rest of the Body. More machinery for the same behaviour; used only if needed.
- **Choosing the encoding.** Which of the two encodings is emitted (native `if/elif/else`, or subgoal plans) is selected per build with an Instancing comment, for example `#% ASL_VERSION = JASON` or `#% ASL_VERSION = GENERIC`. Its exact name, values, default and where it may appear are decided in *Instancing comments*. The language semantics are the same either way.
- The emitted contexts grow quadratically with the number of `GIVEN` Blocks, and earlier Contexts are re-tested. That's acceptable for chains of designer size.

## Not decided here

- Labels on a single `GIVEN`: *Label syntax*.
- What happens when no Plan applies, including a Trigger Block with no matching `GIVEN` and no `ELSE`: *Plan failure and fallback*.
- How Plans from different Trigger Blocks or Playbooks compete for the same Trigger: *Priority model*.
- Choosing among matches explicitly, and running for every match: *Match selection*, not yet specified.
- Loops: deferred.
- Random choice among written Options (`EITHER`/`OR`): chapter 09.
