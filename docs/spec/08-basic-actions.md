# Basic Actions

The Actions built into Regia: changing the Agent's own Facts and Goals, sending, printing and waiting. Decided in the ticket *Basic Action set* (`.scratch/regia-2/issues/07-basic-action-set.md`). It builds on chapters 03–07 and replaces the list of basic actions in primer ch.4. Making `PURSUE` wait by default is recorded in `docs/adr/0005-pursue-waits-ask-does-not.md`. Pursuing twice, repeating and what a drop does to a waiting Body were revised in the ticket *A Goal's life: reached, dropped, repeated* (`.scratch/regia-revision/issues/02-goal-lifecycle.md`), with ADRs 0017 and 0018. Calling off a waiting Custom Action when its Plan stops was added in the ticket *Time and Actions in the game* (`.scratch/regia-revision/issues/19-time-and-actions.md`), with ADR 0038.

## The set

| Statement | Does | Fires |
|---|---|---|
| `LEARN f` | adds the Fact `f` | `WHEN f LEARNED` |
| `FORGET f` | removes the Fact `f` | `WHEN f FORGOTTEN` |
| `UPDATE f TO f2` | replaces `f` with `f2` (same Fact name) | `FORGOTTEN`, then `LEARNED` |
| `PURSUE g` | starts a Pursuit of `g` and waits until it is reached | `TO g` |
| `PURSUE g, WITHOUT WAITING` | starts a Pursuit of `g` and carries on | `TO g` |
| `DROP g` | stops every Pursuit of `g` | `WHEN g DROPPED`, then `WHEN g ENDED` |
| `TELL <recipient> <fact or event>.` | sends a Fact or Cue (chapter 07) | at the receiver |
| `ASK <recipient> TO <goal>.` | asks for a Goal (chapter 07) | at the receiver |
| `SIGNAL <event>.` | sends a Cue to the Directors (chapter 07) | at the Directors |
| `PRINT(e1, e2, …)` | prints Expressions, for debugging | nothing |
| `WAIT <Duration>.` | pauses the Body | nothing |
| `WAIT [<Duration>,] UNTIL <condition>.` | pauses the Body until the condition holds, or the Duration runs out (chapter 12) | nothing |
| `FAIL` | fails the current Plan (chapter 11) | `WHEN g FAILED`, in a `TO g` Plan |
| `SHIFT m BY n` | changes the Agent's Mood `m` by `n` (chapter 14) | nothing |
| `PASS` | nothing: it fills a Block meant to be empty (chapter 01) | nothing |

- Basic Actions are written **without `DO`**. Only Custom Actions take `DO` (`DO eat_food`), below.
- Each Fact and Goal Action is worded like the Trigger kind it fires: `LEARN`/`LEARNED`, `FORGET`/`FORGOTTEN`, `DROP`/`DROPPED`, and `PURSUE` matches the Context test `PURSUING`. A Director's `DROP SUBPLOT P` fires `DROPPED` the same way (chapter 17).
- Arguments follow chapter 03: Values, or Placeholders that are **certainly filled**. Expressions are allowed in any argument (chapter 04): `LEARN health(?h - 10)`. A blank (an unfilled Placeholder) is an error in every Basic Action. "Forget every `hates`" is written `FOR EACH hates(?x): FORGET hates(?x)` (chapter 26), and the error message suggests it.
- The kind of a name must suit the Action: `LEARN` or `FORGET` with a Cue or a Goal, or `PURSUE` or `DROP` with a Fact or a Cue, is an error that suggests the right Action.
- A branch that does nothing is left out (`ELSE` is optional, chapter 06). Where a Block must be written and do nothing, its body is `PASS` (chapter 01).

## Facts

```regia
WHEN insulted(?s):
    LEARN hates(?s)

WHEN apology(?s):
    FORGET hates(?s)
```

- **Learning a known Fact does nothing**, and `LEARNED` doesn't fire. **Forgetting an unknown Fact does nothing**, and `FORGOTTEN` doesn't fire. Neither one fails the Plan.
- `LEARNED` and `FORGOTTEN` fire whatever caused the change, including these Actions (chapter 05). A Fact the Agent learned itself has no Sender.
- **A game Fact** (`GAME FACT`, chapter 10) is the game's to keep. `LEARN`, `FORGET` or `UPDATE` on one works, but the game may undo it at its next report, so the Transpiler warns (`R0807`). To remember what the game said, a Plan records a Fact of its own.

### Updating a Fact

`UPDATE f TO f2` is shorthand for `FORGET f` followed by `LEARN f2`:

```regia
WHEN hit(?dmg):
    GIVEN health(?h):
        UPDATE health(?h) TO health(?h - ?dmg)
```

- Both sides name the **same Fact**, and they may differ only in their arguments. `UPDATE health(?h) TO score(3)` is an error.
- **The old Fact must be known.** If it isn't, the Plan fails, because a change from something that isn't there is a mistake rather than a no-op. (A plain `FORGET` of an unknown Fact does nothing.) What failing does is in chapter 11 (`11-failure.md`).
- It fires exactly what the pair would: `FORGOTTEN` for the old Fact, then `LEARNED` for the new one. If both sides are equal, nothing changes and nothing fires.
- `TO` here is a destination, one of the two closed exceptions to the rule that `TO` introduces a Goal (chapter 01, ADR 0043). The retired spelling `CHANGE f TO f2` is an error (`R0808`).
## Goals

### Pursuing

```regia
TO dinner:
    PURSUE find_food                     # waits until find_food is reached
    DO eat_food

WHEN dawn:
    PURSUE patrol, WITHOUT WAITING       # starts patrol and carries on
    PRINT("Patrol started")
```

- **`PURSUE g` waits.** The Body stops at the Statement until a Plan for `g` finishes, then continues, the same way each Statement finishes before the next one.
- **`, WITHOUT WAITING`** is a trailing clause in the `,` shape reserved for message Statements (chapter 07). The Body goes on at once, and `g` is pursued alongside it.
- `ASK` never waits, as chapter 07 says. Doing something yourself is sequential, but sending isn't.
- **Every `PURSUE` starts a Pursuit of its own** (chapter 05), also when the Agent already pursues `g` with the same arguments. A waiting `PURSUE` waits for the Pursuit it started and no other.
- If no `TO` Plan applies, or the recipe fails, `g` fails (chapter 11). A waiting Body fails with it; a Body that used `WITHOUT WAITING` isn't affected.

### Repeating

A recipe repeats by ending with a `PURSUE` of its own Goal, `WITHOUT WAITING`:

```regia
TO patrol:
    DO walk_to(gate)
    DO walk_to(tower)
    PURSUE patrol, WITHOUT WAITING       # a new Pursuit starts, and this one is reached
```

- **Each round is a Pursuit of its own.** `REACHED` and `ENDED` fire at the end of every round.
- **From the second round on the Goal has no Sender**: the Agent gave it to itself, and it is `FROM ME` (chapter 05). A recipe written `TO patrol, FROM DIRECTOR:` runs one round, then fails for want of a recipe, with a warning at build time (`R3805`, chapter 38); one that the Director starts and that repeats is written `TO patrol, FROM DIRECTOR OR ME:`. A Director that asked for `patrol` hears `REACHED` after the first round and nothing after.
- `DROP patrol` stops the round under way, and no further round starts.
- **The waiting form doesn't repeat.** `PURSUE patrol` inside `TO patrol` waits on a new Pursuit, which waits on another, and none is ever reached. With the recipe's own arguments and no `GIVEN` or `IF` around it, it is a warning (`R0806`). Under a condition it is ordinary recursion and is not reported.
- Loops proper are post-2.0 (chapter 06).

### Dropping

```regia
WHEN apology(?s):
    DROP avenge(?s)

WHEN avenge(?s) DROPPED:
    PRINT("Let it go.")
```

`DROP g` does this for **every Pursuit of `g`** the Agent has (chapter 05), in this order:

1. stops the Pursuit's running `TO` Plan, at once, even if that Plan is the one running `DROP` (the rest of its Body doesn't run);
2. stops every Pursuit that Plan was **waiting** on, and every Pursuit those were waiting on, in turn;
3. fires `WHEN g DROPPED`, then `WHEN g ENDED`;
4. stops the Body that was **waiting** on this Pursuit with `PURSUE g`, if there is one. If that Body is a recipe, its own Pursuit is dropped in the same way, and so on upward.

- **A drop spreads as a drop, in both directions.** Everything stopped in steps 2 and 4 fires `DROPPED` and `ENDED`, never `FAILED`, and no Failure is written (ADR 0018). `FAILED` always means that something went wrong, and `DROPPED` that someone chose to stop.
- Downward they fire innermost first, before `g`'s own; then upward, each level after the one below it (chapter 05).
- A waiting `WHEN` Plan stopped in step 4 has no Goal, so nothing fires. The Trace records that it stopped (chapter 34).
- Goals started `WITHOUT WAITING` are not stopped, and a Body that started `g` `WITHOUT WAITING` is not stopped: they were deliberately set loose.
- **Dropping a Goal that isn't being pursued does nothing**, and `DROPPED` doesn't fire.
- **`DROP` can't pick one Pursuit of several.** `DROP bring(roast)` stops both orders of roast.
- A stopped Plan leaves behind whatever it already did; nothing is undone (chapter 11).

## Sending

`TELL`, `ASK … TO` and `SIGNAL` keep the names and meaning of chapter 07. `BROADCAST` is gone; the recipient `EVERYONE` replaces it.

## `PRINT`

```regia
PRINT("Ouch! Lost", ?dmg, "health")     # Ouch! Lost 12 health
```

- Takes **any number of Expressions**, in parentheses, separated by `,`. They are printed in order, joined by single spaces. There is no `+` on strings (chapter 04).
- The parentheses stay so that a `,` list is never confused with a trailing clause.
- Output goes wherever the Target logs. It is for debugging and doesn't affect the Agent.

## `WAIT`

`WAIT 3 SECONDS` pauses the Body for a Duration (`SECONDS` or `MINUTES`, always written). It pauses only its own Body, and fails only when the Duration isn't a Number. The clock belongs to the Target. All of this is in chapter 12 (`12-time.md`).

## Custom Actions

```regia
WHEN intruder_seen(?x):
    DO walk_to(gate)                      # waits until the game says it's done
    DO shout(?x), WITHOUT WAITING         # carries on once the game has started it
```

- **`DO a` waits until the Action is done**, like every other Statement (ADR 0005). It fails if the game refuses the Action or reports that it failed (chapter 11).
- **`DO a, WITHOUT WAITING`** carries on as soon as the game has **accepted** the Action. It fails only if the game refuses it. A later failure can't reach a Body that has moved on: it is only recorded in the Trace.
- **A Plan that needs to know how a set-loose Action went puts it in a Goal.** The Goal waits on the Action, the Body starts the Goal `WITHOUT WAITING`, and the Goal's `REACHED` and `FAILED` say how it went (chapter 11):

  ```regia
  WHEN cup_unwatched:
      PURSUE poison_cup, WITHOUT WAITING
      DO look_innocent

  TO poison_cup:
      DO pour_poison

  WHEN poison_cup REACHED:
      LEARN poured
  ```

  There is no Trigger on an Action's result in 2.0.
- **The game decides what "done" means** for each Action (arrived, animation finished, at once). The `ACTION` declaration's doc comment is where that is written down.
- **A waiting `DO` whose Plan is stopped calls its Action off.** When `have_dinner` is dropped during `DO eat(roast)`, or the Playbook is taken away, the Phase left, the Staging ended or the Agent leaves, the game is told to stop `eat(roast)`. What stopping means is the game's, like "done", and the doc comment says it. An Action started `WITHOUT WAITING` is never called off, and a dotted Action can't be (chapter 37, ADR 0038).
- **Every game Action can be refused**: the game may not know it, the character may be unable to act, or the Agent may have no body (chapter 37). So a declaration has no word for "can be refused". Nor does it say that an Action ends the Agent (a `leave_hall` after which the Agent leaves the Program): that is not in 2.0, and the doc comment says it.
- **An Action with a dotted External name is the Target's own code** (chapter 10), not the game's: it is done when that code returns, and fails if the code fails.
- How the Jason Target sends Actions and hears their results: chapter 37.

## Reserved words

`LEARN`, `FORGET`, `UPDATE`, `PURSUE`, `DROP`, `PRINT`, `WAIT`, `FAIL` (chapter 11), `SHIFT` (chapter 14), `PASS` (chapter 01), and the clause `WITHOUT WAITING`; plus chapter 07's `TELL`, `ASK`, `SIGNAL`, `EVERYONE`. `BELIEVE` and `ACHIEVE` are no longer keywords.


## Transpiler checks

**Errors**

- `R0801` A blank (an unfilled Placeholder) in a Basic Action's argument (for `FORGET`, the hint suggests `FOR EACH`).
- `R0802` A name whose kind doesn't suit the Action: `LEARN`/`FORGET`/`UPDATE` with a Cue or a Goal, `PURSUE`/`DROP` with a Fact or a Cue, `DROP` with a Plot (hint: `DROP SUBPLOT P`, chapter 17), `DO` with anything but a Custom Action (the message suggests the right Action).
- `R0803` A Custom Action without `DO`, or `DO` before a Basic Action.
- `R0804` `UPDATE f TO f2` with two different Facts.
- `R0805` A trailing clause other than `, WITHOUT WAITING`, or one on a Statement other than `PURSUE` and `DO`.
- `R0808` The retired `CHANGE f TO f2` (hint: `UPDATE f TO f2`).
**Warnings**

- `R0806` A waiting `PURSUE g` in a `TO g` Plan, with the Trigger's own arguments and no `GIVEN` or `IF` around it: the Goal can never be reached (hint: `, WITHOUT WAITING` repeats).
- `R0807` `LEARN`, `FORGET` or `UPDATE` on a game Fact, by an Agent or a Director: the game may undo it (hint: record a Fact of the Program's own).

## Trace entries

**Failures**

- `T0801` `UPDATE f TO f2` when `f` isn't known.

## ASL mapping notes

For *The full ASL mapping* to pick up:

- `LEARN`, `FORGET`, `UPDATE`, `PRINT` and `PASS` in Jason: chapter 39 (`39-jason-plan-bodies.md`). Any Target must raise no event when `LEARN` or `FORGET` changes nothing, so `LEARNED`/`FORGOTTEN` Plans don't run.
- `PURSUE g` maps to `!g`, and `PURSUE g, WITHOUT WAITING` to `!!g`. Nothing is joined: a second `!g` is a second Pursuit. Any Target must give each Pursuit an identity its endings and the Trace can carry. In Jason, the `regia_pursuit(Id)` annotation (chapters 39 and 40).
- `PURSUING g` in a `TO g` Plan must leave out the Plan's own Pursuit. In Jason, `regia.pursuing(G, Except)` (chapter 40).
- `DROP g` must stop every level of chapter 08's steps and raise `DROPPED` and `ENDED` for each, innermost first. A waiting Body whose Goal is dropped stops with no failure. In Jason, `regia.drop(G)`, whose walker `regia.stop_playbook` shares (chapter 40).

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025). A recipe that repeats still has no Sender from its second round on; it just can't be written `FROM ME`. The build-time warning for `TO patrol, FROM DIRECTOR:` is `R3805`, which is later, so in 1.5 that round fails at run time with `T1104` only.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`). `UPDATE`, which replaced `CHANGE`, and `R0808` in the ticket *`TO` and `FROM` outside Triggers* (`.scratch/syntax-review/issues/05-to-and-from.md`).

## Not decided here

- Picking an Action at random: a Random choice, `RANDOMLY:` with `OPTION:` Blocks (chapter 09). There are no Groups.
- A Director can use all of these except `PURSUE`, `DROP`, `SIGNAL` and `SHIFT`, and gives Goals with `ASK` (chapter 20).
- Changing or dropping everything that matches a blank: `FOR EACH`, chapter 26 (`26-match-selection.md`).
