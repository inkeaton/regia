# Random choice

How a Plan's Body picks one of several written Options at random, optionally weighted. Decided in the ticket *Groups* (`.scratch/regia-2/issues/09-groups.md`). It builds on chapters 01, 03, 04 and 06, and replaces the `GROUP` idea in primer ch.3.

## No Groups

Regia 2.0 has **no Groups**. The primer's `FACT GROUP a, b, c` was meant for picking among options and for testing "any of these" in a Context, and other constructs already do each of those jobs better:

| Need | Written as |
|---|---|
| Do one of several things at random | a Random choice (below) |
| "Any of a family" in a Context | a parameterised Fact: `FACT feeling(kind)`, `GIVEN feeling(?f):` |
| The same choice in several Plans | a Goal whose recipe makes the choice: `TO idle: EITHER: …`, then `PURSUE idle.` |
| Declaring several items in one line | Multi-definition: `FACT a, b, c` |

`GROUP` is not a keyword and is not reserved.

## `EITHER` / `OR`

```regia
WHEN bored:
    EITHER: DO wave.
    OR: DO yawn.
    OR:
        PRINT("So tired…").
        LEARN sleepy.
```

- A **Random choice** is a Body Statement made of an `EITHER:` Block followed by one or more `OR:` Blocks at the same indentation. When the Body reaches it, **exactly one Option runs**, picked at random, and then the Body carries on after the last `OR`.
- Each **Option** is an ordinary Block (chapter 01): indented under its header, or written as an Inline block on the header's line.
- An Option may hold **any Statements**, mixing kinds freely: Custom and Basic Actions, `IF`s, and another Random choice.
- **An `EITHER` with no `OR` is an error**, since it isn't a choice. "Only sometimes" is written with `IF RANDOM(1, 100) <= 30:` (chapter 04).
- An `OR:` header that doesn't follow an `EITHER` or `OR` Option is an error. The Context operator `OR` (chapter 06) is never a Block header, so the two can't be confused.
- **Options have no conditions of their own.** To make an Option depend on a Fact, write an `IF` inside it. The Option keeps its share of the roll and does nothing when the `IF` doesn't hold. Alternatively, give it a weight that works out to 0 (below).
- Random choice can be used wherever a Statement can, including a Director's Body.

## Weights

```regia
WHEN bored:
    EITHER, WEIGHT 3: DO wave.
    OR: DO yawn.                            # weight 1
    OR, WEIGHT ?anger: DO curse.
```

- A weight is the trailing clause `, WEIGHT <Expression>` on an `EITHER` or `OR` header, before the `:`. It is the same `,` shape as `PURSUE g, WITHOUT WAITING` (chapter 08).
- **Weights are relative.** An Option without a weight has weight 1. The chance of an Option is its weight divided by the sum of all the weights. In the example above, with `?anger` at 2, the chances are 3/6, 1/6 and 2/6. There are no percentages, so adding an Option never breaks the others.
- A weight is any **Expression** (chapter 04): a Number, a filled Placeholder, arithmetic, even `RANDOM(…)`. Its Placeholders must be **certainly filled** before the Random choice (chapter 03).
- **All the weights are worked out together, once**, when the Body reaches `EITHER`, before the roll. Nothing an Option does can change the roll.
- A **weight of 0** means that Option is never picked.
- A **negative weight counts as 0**, and the Agent writes a **runtime warning** to the log, because a negative weight is usually a sign mistake.
- A **weight that isn't a Number fails the Plan**, like any Body arithmetic (chapter 04). What failing does is in chapter 11 (`11-failure.md`).
- **If every weight is 0** (or negative), no Option runs. The Agent writes a runtime warning to the log, and the Body carries on. Like the no-op Basic Actions (chapter 08), this doesn't fail the Plan.
- Runtime warnings go wherever the Target logs, the same place as `PRINT` output. A Target with no log skips them.

## Placeholders in an Option

The rules for `IF` branches apply (chapter 06):

- A Placeholder filled inside an Option, by naming (`?dmg = RANDOM(1, 6).`) or by an `IF` condition inside it, can be used **only inside that Option**, not in the other Options and not after the Random choice, because it isn't certainly filled there.
- **Sibling Options may reuse a name**, since only one of them runs.
- Reusing that name anywhere else in the Plan is an error, as for `IF`.
- Placeholders filled before the Random choice can be used in every Option and in every weight.

```regia
WHEN attacked(?foe):
    EITHER: ?dmg = RANDOM(1, 6). DO hit(?foe, ?dmg).
    OR, WEIGHT 2: ?dmg = RANDOM(2, 4). DO kick(?foe, ?dmg).    # sibling, may reuse ?dmg
    OR: DO flee.
```

## Reserved words

`EITHER`, `WEIGHT`. `OR` is already reserved as a Context operator (chapter 06).

## ASL mapping notes

For *The full ASL mapping* to pick up:

- **Native `if` (Jason).** Work out each weight into a fresh variable, clamp negatives to 0 with a warning, then roll once with `math.random(T)` (a real number from 0 up to, but not including, `T`) and pick with an `if`/`elif` chain on running sums:

  ```
  +bored : true <-
      W1 = 3; W2 = 1; W3 = Anger;
      if (W3 < 0) { .print("[regia] warning: negative weight in bored, counted as 0") };
      W3c = math.max(0, W3);
      T = W1 + W2 + W3c;
      if (T > 0) {
          R = math.random(T);
          if (R < W1) { wave }
          elif (R < W1 + W2) { yawn }
          else { curse }
      } else {
          .print("[regia] warning: every weight is 0 in bored, nothing chosen")
      }.
  ```

  Constant weights are folded by the Transpiler (no clamp or warning code when they are fixed and non-negative). When all weights are constant and equal, `.random` over a single index is enough. A non-Number weight makes the Jason arithmetic fail, which fails the Plan as required. Warnings should carry the Plan's source location once the logging scheme is decided (*The full ASL mapping* fog).
- Generated variable names (`W1`, `T`, `R`, …) use a prefix designers can't produce, like the other generated names in chapter 06.
- **Targets without a native `if`**: lowered like an `IF` chain (chapter 06). The Body computes the weights and the roll, then posts `!regia_either__N(R, W1, W2, …, captured Placeholders)`. There is one plan per Option, with contexts on running sums (`R < W1`, `R >= W1 & R < W1 + W2`, …), plus a generated plan for the all-zero case that logs the warning and succeeds.
- Jason keeps variables bound inside a branch bound afterwards. The scoping rules above mean a later Statement never sees them, so no renaming is needed (as for `IF`).

## Not decided here

- Picking one of a condition's matches at random (`, AT RANDOM`), or running for every match (`FOR EACH`): chapter 26 (`26-match-selection.md`). `EITHER` chooses among written Options only. Weighted Picks are post-2.0.
- Named weight levels (`OFTEN`, `RARELY`) as sugar: not in 2.0.
- The format and routing of runtime warnings: *The full ASL mapping* (logging).
