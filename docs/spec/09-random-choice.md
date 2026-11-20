# Random choice

How a Plan's Body picks one of several written Options at random, optionally weighted. Decided in the ticket *Groups* (`.scratch/regia-2/issues/09-groups.md`). It builds on chapters 01, 03, 04 and 06, and replaces the `GROUP` idea in primer ch.3.

## No Groups

Regia 2.0 has **no Groups**. The primer's `FACT GROUP a, b, c` was meant for picking among options and for testing "any of these" in a Context, and other constructs already do each of those jobs better:

| Need | Written as |
|---|---|
| Do one of several things at random | a Random choice (below) |
| "Any of a family" in a Context | a parameterised Fact: `FACT feeling(kind)`, `GIVEN feeling(?f):` |
| The same choice in several Plans | a Goal whose recipe makes the choice: `TO idle: RANDOMLY: …`, then `PURSUE idle` |
| Declaring several items in one line | Multi-definition: `FACT a, b, c` |

`GROUP` is not a keyword and is not reserved.

## `RANDOMLY` / `OPTION`

```regia
WHEN bored:
    RANDOMLY:
        OPTION: DO wave
        OPTION: DO yawn
        OPTION:
            PRINT("So tired…")
            LEARN sleepy
```

- A **Random choice** is a Body Statement: a `RANDOMLY:` Block whose children are `OPTION:` Blocks. When the Body reaches it, **exactly one Option runs**, picked at random, and then the Body carries on after the `RANDOMLY` Block.
- Each **Option** is an ordinary Block (chapter 01): indented under its header, or written as an Inline block on the header's line. On one line the whole choice is `RANDOMLY: OPTION: DO wave; OPTION: DO yawn` (`;` closes an Option, chapter 01).
- **Only `OPTION` Blocks stand directly under `RANDOMLY:`.** Any other Statement there is an error (`R0902`), and so is an `OPTION:` anywhere else.
- An Option may hold **any Statements**, mixing kinds freely: Custom and Basic Actions, `IF`s, and another Random choice.
- **A `RANDOMLY` with no Option is an error** (`R0901`): there is nothing to run. **One with a single Option is a warning** (`R0905`): it isn't a choice, the Option always runs, but a generator building Options from a list may well produce one.
- **An Option that does nothing holds `PASS`** (chapter 01). This is how "only sometimes" is written, in the same shares as any other Weight. An Option with no body at all is an empty Block like any other, and gets the `R0106` warning:

  ```regia
  WHEN dessert_served:
      RANDOMLY:
          OPTION, WEIGHT 3: DO complain     # three times in ten
          OPTION, WEIGHT 7: PASS            # otherwise nothing
  ```

  `IF RANDOM(1, 100) <= 30:` (chapter 04) says the same thing and is still valid.
- **Why a container.** Until the syntax review the choice was a run of sibling headers, `EITHER:` then `OR:`. That gave `OR` a second job, a Block header beside the Context operator, and needed a rule gluing the siblings into one Statement. The headers `EITHER:` and `OR:` are retired spellings, errors with a hint (`R0906`). Decided in the ticket *`AND`, `OR` and `EITHER`* (`.scratch/syntax-review/issues/06-and-or.md`).
- **Options have no conditions of their own.** To make an Option depend on a Fact, write an `IF` inside it. The Option keeps its share of the roll and does nothing when the `IF` doesn't hold. Alternatively, give it a weight that works out to 0 (below).
- Random choice can be used wherever a Statement can, including a Director's Body.

## Weights

```regia
WHEN bored:
    RANDOMLY:
        OPTION, WEIGHT 3: DO wave
        OPTION: DO yawn                         # weight 1
        OPTION, WEIGHT ?anger: DO curse
```

- A weight is the trailing clause `, WEIGHT <Expression>` on an `OPTION` header, before the `:`. It is the same `,` shape as `PURSUE g, WITHOUT WAITING` (chapter 08).
- **Weights are relative.** An Option without a weight has weight 1. The chance of an Option is its weight divided by the sum of all the weights. In the example above, with `?anger` at 2, the chances are 3/6, 1/6 and 2/6. There are no percentages, so adding an Option never breaks the others: `WEIGHT 30%` is an error (`R1517`, chapter 15).
- A weight is any **Expression** (chapter 04): a Number, a filled Placeholder, arithmetic, even `RANDOM(…)`. Its Placeholders must be **certainly filled** before the Random choice (chapter 03).
- **All the weights are worked out together, once**, when the Body reaches `RANDOMLY`, before the roll. Nothing an Option does can change the roll.
- A **weight of 0** means that Option is never picked.
- A **negative weight counts as 0**. A computed weight such as `?anger - 2` that drops below 0 means "never", and the writer has no `max` to keep it at 0, so nothing warns. The Trace records it (`T0902`).
- **If every weight is 0** (or negative), no Option runs and the Body carries on: "none of these, this time" can be meant. Like the no-op Basic Actions (chapter 08), this doesn't fail the Plan. The Trace records it (`T0903`).
- A **weight that isn't a Number fails the Plan**, like any Body arithmetic (chapter 04). What failing does is in chapter 11 (`11-failure.md`).
- The same rules hold for a weighted Pick (chapter 26). `WEIGHT` has one meaning in both: how likely this one is, against the sum of the others, among Options or among Matches.

## Placeholders in an Option

The rules for `IF` branches apply (chapters 04 and 06), with Options in the place of branches:

- A Placeholder filled inside an Option, by `LET` (`LET ?dmg BE RANDOM(1, 6)`) or by an `IF` condition inside it, can be used inside that Option.
- **A Placeholder filled in every Option outlives the Random choice**, as one filled in every branch of an `IF`/`ELSE` outlives the `IF`: it is certainly filled after it. An Option holding only `PASS` fills nothing, so a Random choice with one fills nothing that outlives it.
- A Placeholder filled in some Options but not all can't be used after the Random choice, or anywhere else in the Plan but a sibling Option.
- **Sibling Options may fill the same Placeholder**, since only one of them runs.
- Placeholders filled before the Random choice can be used in every Option and in every weight.

```regia
WHEN attacked(?foe):
    RANDOMLY:
        OPTION: LET ?dmg BE RANDOM(1, 6). DO hit(?foe, ?dmg)
        OPTION, WEIGHT 2: LET ?dmg BE RANDOM(2, 4). DO kick(?foe, ?dmg)     # sibling, may fill ?dmg too
        OPTION: DO flee
                                       # ?dmg can't be used here: the last Option doesn't fill it

WHEN wager_offered(?gold):
    RANDOMLY:
        OPTION: LET ?stake BE ?gold / 2
        OPTION: LET ?stake BE 1
    DO bet(?stake)                     # every Option filled ?stake
```

## Reserved words

Every keyword is listed in chapter 01, *Reserved words* (`01-statements-and-blocks.md`).

## Transpiler checks

**Errors**

- `R0901` A `RANDOMLY` with no `OPTION` Block.
- `R0902` An `OPTION:` Block that isn't directly under a `RANDOMLY:`, or a Statement other than an `OPTION` Block directly under a `RANDOMLY:` (hint: wrap it in an `OPTION:`, or move it out).
- `R0903` A weight whose Placeholders aren't certainly filled before the Random choice.
- `R0904` A Placeholder filled inside some Options but not all, used after the Random choice, or anywhere else in the Plan but a sibling Option.
- `R0906` The retired headers `EITHER:` and `OR:` (hint: write `RANDOMLY:` with one `OPTION:` Block per Option).

**Warnings**

- `R0905` A `RANDOMLY` with a single `OPTION`: it always runs.

## Trace entries

**Failures**

- `T0901` A weight that isn't a Number.

**Entries**

- `T0902` A negative weight, counted as 0.
- `T0903` Every weight is 0 (or negative): no Option runs.

Neither is a warning: both can be meant.

## ASL mapping notes

The Jason translation is chapter 39 (`39-jason-plan-bodies.md`): an `if`/`elif` chain on running sums, rolled once from `regia.random`, with generated variables named as chapter 39 says. What any AgentSpeak Target must keep: one roll from the seeded source (chapter 35), constant weights folded, a negative weight clamped with `T0902`, and an all-zero total logged with `T0903`.

- **Targets without a native `if`** (not Jason): lowered like an `IF` chain (chapter 06). The Body computes the weights and the roll, then posts `!regia_randomly__N(R, W1, W2, …, captured Placeholders)`. There is one plan per Option, with contexts on running sums (`R < W1`, `R >= W1 & R < W1 + W2`, …), plus a generated plan for the all-zero case that logs the warning and succeeds.
- A name made in only some Options is never seen by a later Statement, so no renaming is needed (as for `IF`). On Targets without a native `if`, a name made in every Option is passed back from the generated Option plans like one made in every branch of an `IF` chain (chapter 06).

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025).

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- Picking one of a condition's matches at random (`, RANDOMLY`), weighted (`, WEIGHT …`), or running for every match (`FOR EACH`): chapter 26 (`26-match-selection.md`). `RANDOMLY` chooses among written Options only.
- Named weight levels (`OFTEN`, `RARELY`) as sugar: not in 2.0.
