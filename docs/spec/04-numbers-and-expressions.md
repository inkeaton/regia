# Numbers and Expressions

How Regia writes numbers, compares them, calculates with them and rolls random ones, and how a Plan's Body names a computed value. Decided in the ticket *Numbers and arithmetic* (`.scratch/regia-2/issues/04-numbers-and-arithmetic.md`). It builds on *Parameters and Placeholders* (`03-parameters-and-placeholders.md`). The choice to name values only in the Body is recorded in `docs/adr/0002-values-are-named-in-the-body.md`.

In the examples, the Context is written as the `IF` directly under the Trigger, as in chapter 03. Chapter 06 (`06-context-and-control-flow.md`) replaces this with `GIVEN`. Changing a Fact in one step is `CHANGE … TO` (chapter 08); the examples spell it out with `FORGET` and `LEARN`.

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

`*` and `/` bind tighter than `+` and `-`, as in school math. There is no remainder or whole-number division. Arithmetic works only on Numbers; there is no `+` for joining strings (`PRINT` joins its arguments with spaces, chapter 08).

Spaces around operators are optional: `?h-10` and `?h - 10` are the same, since names never contain `-`.

### Comparisons

| Operator | Meaning | Works on |
|---|---|---|
| `=` | equal | any Values |
| `<` `>` | less, greater | Numbers |
| `<=` `>=` | less or equal, greater or equal | Numbers |

There is no "not equal" operator. Write `NOT ?who = host`.

### Order of operations

From tightest to loosest:

1. arithmetic (`*` `/`, then `+` `-`)
2. comparisons
3. `NOT`, `AND`, `OR` (`NOT` before `AND` before `OR`, and mixing `AND` with `OR` needs parentheses: chapter 06)

So `NOT ?h + 1 = 5` means `NOT ((?h + 1) = 5)`.

Comparisons don't chain. `0 < ?h < 20` is an error, and the Transpiler suggests `0 < ?h AND ?h < 20`.

### Random numbers

`RANDOM(a, b)` gives a random Number from `a` to `b`, **both included**:

- when both bounds are whole, a whole number: `RANDOM(1, 6)` is a die roll;
- when either bound is a decimal, a decimal: `RANDOM(0, 1.0)`.

Every `RANDOM(…)` is a fresh roll. To use the same roll twice, name it in the Body (see below).

## Where Expressions can appear

| Place | Expressions? |
|---|---|
| Body argument slots: `LEARN health(?h - 10)` | yes |
| Either side of a comparison in a Context: `?a + ?b > 10` | yes |
| Trigger slots: `WHEN damaged(?n + 1)` | **no**: a Trigger matches what arrived, with Values and Placeholders only |
| Declarations: `FACT health(80)` | **no**: declarations hold parameter names |

To compare a Fact's number, match the Fact and then compare the Placeholder:

```regia
WHEN danger_seen:
    IF health(?h) AND ?h < 20:
        DO flee.
```

## The Context tests, the Body names

In a **Context**, `=` only ever compares. Both sides must be filled already, and it never fills a Placeholder. `IF health(?h) AND ?new = ?h - 1:` is an error, because `?new` is not filled.

`RANDOM(…)` can be used inside a Context comparison, for Plans that apply only some of the time. It is never stored there:

```regia
WHEN food_served:
    IF is_hungry AND RANDOM(1, 100) <= 30:    # 30% of the time
        DO grab_food.
```

In a **Body**, a Statement of the form `?name = Expression.` **names** a value: it fills the Placeholder `?name` with what the Expression works out to.

```regia
WHEN hit:
    IF health(?h):
        ?dmg = RANDOM(1, 6).
        FORGET health(?h).
        LEARN health(?h - ?dmg).
        PRINT("Ouch! Lost", ?dmg).      # the same roll
```

Naming follows the same rules as any other Placeholder (chapter 03): filled once, never reassigned, gone when the Plan run ends.

- **Already filled is an error.** Naming a Placeholder that the Trigger, the Context or an earlier Statement already filled is an error, not a comparison or a reassignment. `?h = ?h - 1.` is an error; write `?new = ?h - 1.`
- **Order matters.** A named Placeholder can be used only by the Statements after the naming Statement.
- **Branches.** A Placeholder named inside a Body `IF` branch can be used after the `IF` only if every branch names it, just as with `OR` in a Context.

```regia
WHEN gift_received(?giver):
    IF trust(?giver, ?t):
        IF ?t > 5:
            ?gain = 2.
        ELSE:
            ?gain = 1.
        FORGET trust(?giver, ?t).
        LEARN trust(?giver, ?t + ?gain).   # every branch named ?gain
```

A value that has to last beyond one Plan run is stored as a Fact and read back by matching:

```regia
WHEN banquet_starts:
    ?luck = RANDOM(1, 10).
    LEARN luck(?luck).

WHEN dice_game_offered:
    IF luck(?l) AND ?l > 7:
        DO accept_game.
```

An Expression that's used only once doesn't need a name: `LEARN score(?m + ?t).`

## When a Number isn't a Number

Parameters are untyped (chapter 03), so a slot can hold a name where a Number was expected.

- The **Transpiler** reports every misuse it can see in the source, such as `host + 1` or `"hi" < 3`.
- At runtime, in a **Context**, a comparison that needs Numbers and doesn't get them is **false**: that match doesn't satisfy the Context.
- At runtime, in a **Body**, arithmetic on something that isn't a Number, or a division by zero, makes the **Plan fail**. What failure does is in chapter 11 (`11-failure.md`).


## Transpiler checks

**Errors**

- `R0401` A number written in a form Regia doesn't have: `.5`, an exponent, digit separators, another base.
- `R0402` An Expression in a Trigger slot.
- `R0403` A chained comparison, such as `0 < ?h < 20` (hint: `0 < ?h AND ?h < 20`).
- `R0404` A comparison in a Context with a side that isn't filled yet (`=` never fills).
- `R0405` Naming a Placeholder that is already filled (`?h = ?h - 1.`).
- `R0406` Arithmetic, or `<` `>` `<=` `>=`, on something the source shows isn't a Number (`host + 1`, `"hi" < 3`).

## Trace entries

**Failures**

- `T0401` Body arithmetic on something that isn't a Number.
- `T0402` A division by zero.

## Not decided here

- Changing a numeric Fact in one step (`CHANGE … TO`), and joining values for `PRINT`: decided in chapter 08 (`08-basic-actions.md`).
- A shorthand comparison on a Fact (`health < 20`), a math library (`abs`, `round`, …), and naming values in the Context: not yet specified.
