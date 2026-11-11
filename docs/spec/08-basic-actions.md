# Basic Actions

The Actions built into Regia: changing the Agent's own Facts and Goals, sending, printing and waiting. Decided in the ticket *Basic Action set* (`.scratch/regia-2/issues/07-basic-action-set.md`). It builds on chapters 03–07 and replaces the list of basic actions in primer ch.4. Making `PURSUE` wait by default is recorded in `docs/adr/0005-pursue-waits-ask-does-not.md`.

## The set

| Statement | Does | Fires |
|---|---|---|
| `LEARN f.` | adds the Fact `f` | `WHEN f LEARNED` |
| `FORGET f.` | removes the Fact `f` | `WHEN f FORGOTTEN` |
| `CHANGE f TO f2.` | replaces `f` with `f2` (same Fact name) | `FORGOTTEN`, then `LEARNED` |
| `PURSUE g.` | gives the Agent the Goal `g` and waits until it is reached | `TO g` |
| `PURSUE g, WITHOUT WAITING.` | gives the Agent the Goal `g` and carries on | `TO g` |
| `DROP g.` | stops pursuing `g` | `WHEN g DROPPED` |
| `TELL <recipient> <fact or event>.` | sends a Fact or Event (chapter 07) | at the receiver |
| `ASK <recipient> TO <goal>.` | asks for a Goal (chapter 07) | at the receiver |
| `SIGNAL <event>.` | sends an Event to the Directors (chapter 07) | at the Directors |
| `PRINT(e1, e2, …).` | prints Expressions, for debugging | nothing |
| `WAIT <Duration>.` | pauses the Body | nothing |
| `FAIL.` | fails the current Plan (chapter 11) | `WHEN g FAILED`, in a `TO g` Plan |

- Basic Actions are written **without `DO`**. Only Custom Actions take `DO` (`DO eat_food.`).
- Each Fact and Goal Action is worded like the Trigger kind it fires: `LEARN`/`LEARNED`, `FORGET`/`FORGOTTEN`, `DROP`/`DROPPED`, and `PURSUE` matches the Context test `PURSUING`.
- Arguments follow chapter 03: Values, or Placeholders that are **certainly filled**. Expressions are allowed in any argument (chapter 04): `LEARN health(?h - 10).` A blank (an unfilled Placeholder) is an error in every Basic Action. "Forget every `hates`" is written `FOR EACH hates(?x): FORGET hates(?x).` (chapter 26), and the error message suggests it.
- The kind of a name must suit the Action: `LEARN` or `FORGET` with an Event or a Goal, or `PURSUE` or `DROP` with a Fact or an Event, is an error that suggests the right Action.
- There is no empty Statement. A branch that does nothing is left out (`ELSE` is optional, chapter 06).

## Facts

```regia
WHEN insulted(?s):
    LEARN hates(?s).

WHEN apology(?s):
    FORGET hates(?s).
```

- **Learning a known Fact does nothing**, and `LEARNED` doesn't fire. **Forgetting an unknown Fact does nothing**, and `FORGOTTEN` doesn't fire. Neither one fails the Plan.
- `LEARNED` and `FORGOTTEN` fire whatever caused the change, including these Actions (chapter 05). A Fact the Agent learned itself has no Sender.

### Changing a Fact

`CHANGE f TO f2.` is shorthand for `FORGET f.` followed by `LEARN f2.`:

```regia
WHEN hit(?dmg):
    GIVEN health(?h):
        CHANGE health(?h) TO health(?h - ?dmg).
```

- Both sides name the **same Fact**, and they may differ only in their arguments. `CHANGE health(?h) TO score(3)` is an error.
- **The old Fact must be known.** If it isn't, the Plan fails, because a change from something that isn't there is a mistake rather than a no-op. (A plain `FORGET` of an unknown Fact does nothing.) What failing does is in chapter 11 (`11-failure.md`).
- It fires exactly what the pair would: `FORGOTTEN` for the old Fact, then `LEARNED` for the new one. If both sides are equal, nothing changes and nothing fires.

## Goals

### Pursuing

```regia
TO dinner:
    PURSUE find_food.                    # waits until find_food is reached
    DO eat_food.

WHEN dawn:
    PURSUE patrol, WITHOUT WAITING.      # starts patrol and carries on
    PRINT("Patrol started").
```

- **`PURSUE g.` waits.** The Body stops at the Statement until a Plan for `g` finishes, then continues, the same way each Statement finishes before the next one.
- **`, WITHOUT WAITING`** is a trailing clause in the `,` shape reserved for message Statements (chapter 07). The Body goes on at once, and `g` is pursued alongside it.
- `ASK` never waits, as chapter 07 says. Doing something yourself is sequential, but sending isn't.
- **Pursuing a Goal already being pursued** (same arguments) starts nothing new (chapter 05). A waiting `PURSUE` waits for that existing pursuit to be reached, and continues when it is.
- If no `TO` Plan applies, or the recipe fails, `g` fails (chapter 11). A waiting Body fails with it; a Body that used `WITHOUT WAITING` isn't affected.

### Dropping

```regia
WHEN apology(?s):
    DROP avenge(?s).

WHEN avenge(?s) DROPPED:
    PRINT("Let it go.").
```

`DROP g.` does, in this order:

1. stops the running `TO` Plan for `g`, at once, even if that Plan is the one running `DROP` (the rest of its Body doesn't run);
2. stops every Goal that Plan was **waiting** on, and every Goal those were waiting on, in turn;
3. fires `WHEN g DROPPED`.

- Goals started `WITHOUT WAITING` are not stopped: they were deliberately set loose.
- A Body that was **waiting** on `g` with `PURSUE g.` fails, since `g` will never be reached. What failing does is in chapter 11 (`11-failure.md`).
- **Dropping a Goal that isn't being pursued does nothing**, and `DROPPED` doesn't fire.
- Goals stopped in step 2 **fire their own `DROPPED`**, innermost first, before `g`'s. A stopped Plan leaves behind whatever it already did; nothing is undone (chapter 11).

## Sending

`TELL`, `ASK … TO` and `SIGNAL` keep the names and meaning of chapter 07. `BROADCAST` is gone; the recipient `EVERYONE` replaces it.

## `PRINT`

```regia
PRINT("Ouch! Lost", ?dmg, "health").    # Ouch! Lost 12 health
```

- Takes **any number of Expressions**, in parentheses, separated by `,`. They are printed in order, joined by single spaces. There is no `+` on strings (chapter 04).
- The parentheses stay so that a `,` list is never confused with a trailing clause.
- Output goes wherever the Target logs. It is for debugging and doesn't affect the Agent.

## `WAIT`

`WAIT 3 SECONDS.` pauses the Body for a Duration (`SECONDS` or `MINUTES`, always written). It pauses only its own Body, and fails only when the Duration isn't a Number. The clock belongs to the Target. All of this is in chapter 12 (`12-time.md`).

## Reserved words

`LEARN`, `FORGET`, `CHANGE`, `PURSUE`, `DROP`, `PRINT`, `WAIT`, `FAIL` (chapter 11), and the clause `WITHOUT WAITING`; plus chapter 07's `TELL`, `ASK`, `SIGNAL`, `EVERYONE`. `BELIEVE` and `ACHIEVE` are no longer keywords.

## ASL mapping notes

For *The full ASL mapping* to pick up:

- `LEARN f` maps to `+f` and `FORGET f` to `-f` (removing every source, chapter 07), each guarded so that no event is generated when nothing changes, so `LEARNED`/`FORGOTTEN` Plans don't run. `CHANGE f TO f2` maps to a test that `f` is known, then `-f; +f2` (not `-+`, which matches any arguments); when `f` equals `f2`, nothing.
- `PURSUE g` maps to `!g`, and `PURSUE g, WITHOUT WAITING` to `!!g`. A duplicate pursuit must join the existing intention rather than start a second one: the waiting form checks `.desire(g)` and waits for it to finish (for example with `.wait` on a generated completion event) instead of calling `!g` again.
- `DROP g` maps to `.drop_desire(g)` (or `.drop_intention`), which also removes sub-goals pushed with `!` on the same intention and leaves `!!` ones alone, as required. `WHEN g DROPPED` has no native Jason event, so the generated drop code raises it explicitly, and does nothing if `g` isn't desired.
- A waiting Body whose Goal is dropped fails: in Jason the waiting sub-goal is on the same intention, so the drop removes it; a Plan that joined an existing pursuit (above) must be failed explicitly.
- `PRINT(a, b)` maps to `.print(a, " ", b)`.

## Not decided here

- Picking an Action at random: a Random choice, `EITHER:` … `OR:` (chapter 09). There are no Groups.
- A Director can use all of these except `PURSUE`, `DROP` and `SIGNAL`, and gives Goals with `ASK` (chapter 20).
- Changing or dropping everything that matches a blank: `FOR EACH`, chapter 26 (`26-match-selection.md`).
