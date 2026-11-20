# Numbers and Expressions

How Regia writes numbers, compares them, calculates with them and rolls random ones, and how a Plan's Body fills a Placeholder with a computed value. Decided in the ticket *Numbers and arithmetic* (`.scratch/regia-2/issues/04-numbers-and-arithmetic.md`). It builds on *Parameters and Placeholders* (`03-parameters-and-placeholders.md`). The choice to fill Placeholders with computed values only in the Body is recorded in `docs/adr/0002-values-are-named-in-the-body.md`; its spelling, `LET ?x BE …`, and `!=` in `docs/adr/0042-let-fills-a-placeholder-and-equals-only-compares.md`.

In the examples, the Context is written as the `IF` directly under the Trigger, as in chapter 03. Chapter 06 (`06-context-and-control-flow.md`) replaces this with `GIVEN`. Changing a Fact in one step is `UPDATE … TO` (chapter 08); the examples spell it out with `FORGET` and `LEARN`.

## Numbers

There is **one kind of Number**. Whole numbers and decimals are the same kind, so `5 = 5.0` is true.

| Written | Meaning |
|---|---|
| `80` | eighty |
| `-3` | minus three |
| `0.5` | one half |

- A decimal always has a digit before the `.`: write `0.5`, never `.5`. A `.` followed by a digit belongs to the number, so it never ends a Statement (chapter 01).
- A `-` directly before a digit, where a Value starts, is part of the number: `sympathy(-0.5)`.
- There are no exponents (`1e3`), digit separators (`1_000`) or other bases (`0xFF`).
- How precise decimals are is up to each Target. The language only promises that decimals exist.

## Expressions

An **Expression** is something that works out to a Value: a Value, a filled Placeholder, `RANDOM(…)`, `COUNT(…)` (the number of matches of a condition, chapter 26), or any of these combined with operators.

### Arithmetic

| Operator | Meaning |
|---|---|
| `+` | add |
| `-` | subtract (or negate: `-?x`) |
| `*` | multiply |
| `/` | divide; the result is always a decimal when it doesn't come out whole (`7 / 2` is `3.5`) |
| `( … )` | group |

`*` and `/` bind tighter than `+` and `-`, as in school math. There is no remainder or whole-number division, and `%` is never a remainder: it writes the share of a count, `50% OF Guest` (chapter 15, ADR 0045). A remainder, if Regia ever needs one, will be a word. Arithmetic works only on Numbers; there is no `+` for joining strings (`PRINT` joins its arguments with spaces, chapter 08).

Spaces around operators are optional: `?h-10` and `?h - 10` are the same, since names never contain `-`.

### Comparisons

| Operator | Meaning | Works on |
|---|---|---|
| `=` | equal | any Values |
| `!=` | not equal | any Values |
| `<` `>` | less, greater | Numbers |
| `<=` `>=` | less or equal, greater or equal | Numbers |

`=` has one meaning, wherever it is written: **equal**. It never fills a Placeholder. `?who != host` is the same test as `NOT ?who = host`; the spec and the tools write `!=`.

### Order of operations

From tightest to loosest:

1. arithmetic (`*` `/`, then `+` `-`)
2. comparisons
3. `NOT`, `AND`, `OR` (`NOT` before `AND` before `OR`, and mixing `AND` with `OR` needs parentheses: chapter 06)

So `NOT ?h + 1 = 5` means `NOT ((?h + 1) = 5)`.

Comparisons don't chain. `0 < ?h < 20` is an error, and the Transpiler suggests `0 < ?h AND ?h < 20`.

### Random numbers

`RANDOM(a, b)` gives a random Number from `a` to `b`, **both included**. Whether the roll is whole or decimal is decided by **how the bounds are written**, never by the values they work out to (`docs/adr/0034-a-rolls-kind-is-written.md`):

- when either bound is a **decimal number written out**, such as `3.0` or `-0.5`, the roll is a decimal: `RANDOM(1, 3.0)`, `RANDOM(0.0, ?max)`;
- otherwise the roll is **whole**: `RANDOM(1, 6)` is a die roll, and so are `RANDOM(1, ?gold / 2)` and `RANDOM(?low, ?high)`, whatever the Placeholders and Expressions hold.

A whole roll gives one of the whole numbers from `a` to `b`. With 13 coins, `RANDOM(1, ?gold / 2)` is a roll from 1 to 6.5, so it gives 1 to 6. This is the only place a Number is rounded by a roll.

- **Bounds in either order** mean the same range: `RANDOM(6, 1)` is `RANDOM(1, 6)`.
- **A whole roll with no whole number between its bounds** (`RANDOM(1, ?gold / 2)` with 1 coin, a range from 1 to 0.5) has nothing to give. In a Body it **fails the Plan** (`T0403`), like a division by zero. In a Context the comparison that holds it is false. A guard avoids it: `IF ?gold >= 2:`.
- A starting Propensity value in Instancing is always a decimal roll, whatever its bounds look like (chapter 21).

Every `RANDOM(…)` is a fresh roll. To use the same roll twice, fill a Placeholder with it in the Body (`LET`, below). Which rolls a seed covers is in chapter 34.

## Where Expressions can appear

| Place | Expressions? |
|---|---|
| Body argument slots: `LEARN health(?h - 10)` | yes |
| After `BE` in a `LET` Statement: `LET ?dmg BE RANDOM(1, 6)` | yes |
| Either side of a comparison in a Context: `?a + ?b > 10` | yes |
| Trigger slots: `WHEN damaged(?n + 1)` | **no**: a Trigger matches what arrived, with Values and Placeholders only |
| Declarations: `FACT health(80)` | **no**: declarations hold parameter names |

To compare a Fact's number, match the Fact and then compare the Placeholder:

```regia
WHEN danger_seen:
    IF health(?h) AND ?h < 20:
        DO flee
```

## The Context tests, the Body fills

In a **Context**, a comparison only ever compares. Both sides must be filled already, and it never fills a Placeholder. `IF health(?h) AND ?new = ?h - 1:` is an error, because `?new` is not filled. `LET` is a Body Statement and can't be written in a condition.

`RANDOM(…)` can be used inside a Context comparison, for Plans that apply only some of the time. It is never stored there:

```regia
WHEN food_served:
    IF is_hungry AND RANDOM(1, 100) <= 30:    # 30% of the time
        DO grab_food
```

In a **Body**, a **`LET` Statement**, `LET ?name BE Expression`, fills the Placeholder `?name` with what the Expression works out to.

```regia
WHEN hit:
    IF health(?h):
        LET ?dmg BE RANDOM(1, 6)
        FORGET health(?h)
        LEARN health(?h - ?dmg)
        PRINT("Ouch! Lost", ?dmg)       # the same roll
```

A Placeholder filled by `LET` follows the same rules as any other (chapter 03): filled once, never reassigned, gone when the Plan run ends.

- **Already filled is an error.** `LET` on a Placeholder that the Trigger, the Context or an earlier Statement already filled is an error, not a comparison or a reassignment. `LET ?h BE ?h - 1` is an error; write `LET ?new BE ?h - 1`.
- **`LET` goes only in a Body**, as a Statement of its own, one-line Options included (`OPTION: LET ?stake BE ?gold / 2`, chapter 09). It is an error in a Context or an `IF` condition.
- **The spelling without `LET`**, `?x = e` as a Statement, is retired: it is an error, with the hint `LET ?x BE e`.
- **Order matters.** A Placeholder filled by `LET` can be used only by the Statements after it.
- **Branches.** A Placeholder filled inside a Body `IF` branch can be used after the `IF` only if every branch fills it, just as with `OR` in a Context. The same holds for the Options of a Random choice (chapter 09): a Placeholder filled in every Option outlives the choice.

```regia
WHEN gift_received(?giver):
    IF trust(?giver, ?t):
        IF ?t > 5:
            LET ?gain BE 2
        ELSE:
            LET ?gain BE 1
        FORGET trust(?giver, ?t)
        LEARN trust(?giver, ?t + ?gain)    # every branch filled ?gain
```

A value that has to last beyond one Plan run is stored as a Fact and read back by matching:

```regia
WHEN banquet_starts:
    LET ?luck BE RANDOM(1, 10)
    LEARN luck(?luck)

WHEN dice_game_offered:
    IF luck(?l) AND ?l > 7:
        DO accept_game
```

An Expression that's used only once doesn't need a `LET`: `LEARN score(?m + ?t)`.

## When a Number isn't a Number

Parameters are untyped (chapter 03), so a slot can hold a name where a Number was expected.

- The **Transpiler** reports every misuse it can see in the source, such as `host + 1` or `"hi" < 3`.
- At runtime, in a **Context**, a comparison that needs Numbers and doesn't get them is **false**: that match doesn't satisfy the Context. So is one holding a whole roll with nothing to give (above).
- At runtime, in a **Body**, arithmetic on something that isn't a Number, or a division by zero, makes the **Plan fail**. What failure does is in chapter 11 (`11-failure.md`).


## Transpiler checks

**Errors**

- `R0401` A number written in a form Regia doesn't have: `.5`, an exponent, digit separators, another base.
- `R0402` An Expression in a Trigger slot.
- `R0403` A chained comparison, such as `0 < ?h < 20` or `?a = ?b != ?c` (hint: `0 < ?h AND ?h < 20`).
- `R0404` A comparison in a Context with a side that isn't filled yet (a comparison never fills).
- `R0405` `LET` on a Placeholder that is already filled (`LET ?h BE ?h - 1`; hint: `LET ?new BE ?h - 1`).
- `R0406` Arithmetic, or `<` `>` `<=` `>=`, on something the source shows isn't a Number (`host + 1`, `"hi" < 3`).
- `R0407` The retired spelling `?x = e` as a Body Statement (hint: `LET ?x BE e`).
- `R0408` `LET` in a Context or an `IF` condition.

## Trace entries

**Failures**

- `T0401` Body arithmetic on something that isn't a Number.
- `T0402` A division by zero.
- `T0403` A whole roll with no whole number between its bounds.

## Reserved words

Every keyword is listed in chapter 01, *Reserved words* (`01-statements-and-blocks.md`).

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025).

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- Changing a numeric Fact in one step (`UPDATE … TO`), and joining values for `PRINT`: decided in chapter 08 (`08-basic-actions.md`).
- A shorthand comparison on a Fact (`health < 20`), a math library (`abs`, `round`, …), and filling Placeholders with computed values in the Context: not yet specified.
