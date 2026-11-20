# Time

How Regia deals with time: writing a Duration, pausing a Body with `WAIT`, and what measures the time. Decided in the ticket *Time and timers* (`.scratch/regia-2/issues/12-time-and-timers.md`). It builds on chapters 03, 04, 08 and 11, and replaces `WAIT()` in primer ch.4. A wait that ends on a condition (`UNTIL`), the Phase timeout `AFTER`, and a clock that stops while the game is paused were added in the ticket *Time and Actions in the game* (`.scratch/regia-revision/issues/19-time-and-actions.md`).

## The clock belongs to the Target

- **The language fixes Durations, and the Target owns the clock.** A Plan says "3 seconds". The Target decides what measures them: wall-clock time, or game time that stops when the game is paused and follows its time scale.
- **One Program uses one clock.** Every Duration in it is measured the same way, so two Agents waiting 3 seconds wait the same length of time.
- **The clock stops while the game is paused.** The game says when it pauses and resumes (chapter 37), and while it is paused no Duration runs: not a `WAIT`, not the limit of a `WAIT … UNTIL`, not an `AFTER`. Agents and Directors still react to Messages and Cues. Following the game's time scale is not in 2.0 (below).
- Facts about the time of day (`is_night`) are ordinary Facts, usually External ones that the game keeps up to date (chapter 10). They have nothing to do with this chapter.

## Durations

```regia
WAIT 3 SECONDS
WAIT 0.5 SECONDS
WAIT 1 MINUTE
WAIT RANDOM(2, 5) SECONDS
WAIT ?delay * 2 SECONDS
```

- A **Duration** is an Expression (chapter 04) followed by a unit word: `SECONDS` or `MINUTES`. `SECOND` and `MINUTE` are accepted too, and the singular and plural forms are interchangeable (`1 SECONDS` and `2 MINUTE` are both fine).
- **The unit is always written.** `WAIT 3` is an error.
- There are no symbol shorthands (`3s`) and no smaller units. Fractions cover them: `0.1 SECONDS`.
- The unit word comes after the whole Expression: `WAIT ?delay * 2 SECONDS` waits `?delay * 2` seconds.
- Placeholders in the Expression must be **certainly filled** before the `WAIT` (chapter 03).

## `WAIT`

`WAIT <Duration>` is a Basic Action (chapter 08), written without `DO`.

```regia
WHEN food_served:
    DO sniff_air
    WAIT RANDOM(1, 3) SECONDS
    DO eat_food
```

- **It pauses only the Body it's in.** The Agent keeps reacting while it waits, and its other Plans run as usual.
- **A waiting Plan is still running.** If it is the recipe for a Goal `g`, then `g` is still being pursued, and Bodies waiting on `g` with `PURSUE g` keep waiting.
- **The Duration is worked out once**, when the Body reaches the `WAIT`.
- **`WAIT 0 SECONDS` carries on at once.**
- **A negative Duration counts as 0**, and the Agent writes a **runtime warning** to the trace (chapter 11), the same as a negative Weight (chapter 09). The Body carries on.
- **A Duration that isn't a Number fails the Plan**, like any Body arithmetic (chapter 04). This is the only way `WAIT` fails. What failing does is in chapter 11.
- **A Plan stopped during a `WAIT`** (by `DROP`, or because its Playbook is taken away) just stops. The wait isn't a failure of its own. What gets reported is whatever stopped it, such as the Goal's `DROPPED` (chapter 08).
- `WAIT` means the same wherever it's allowed. A Director's Plans can use it, except in an `EXITED` Plan; leaving a Phase stops its paused Plans silently (chapter 20).

## `WAIT … UNTIL`

A wait can end as soon as a condition holds:

```regia
TO have_dinner:
    WAIT 1 MINUTE, UNTIL on_plate(roast)
    IF on_plate(roast):
        DO eat(roast)
    ELSE:
        FAIL WITH no_roast

WHEN door_opened:
    WAIT UNTIL NOT guard_near           # no limit
    DO slip_out
```

- **`WAIT <Duration>, UNTIL <condition>`** waits until the condition holds, or until the Duration has run out, whichever comes first. **`WAIT UNTIL <condition>`** has no limit.
- **The condition is anything an `IF` can test** in that Block (chapter 06): the Agent's Facts, or in a Director its own Facts, `IN <phase>`, `PLAYS` and `RUNNING`. It is checked when the Body reaches the `WAIT`, and again whenever what it tests changes. If it already holds, the Body carries on at once.
- **Running out of time is not a failure.** The Body carries on either way, and an `IF` after the `WAIT` tells the two endings apart. `WAIT … UNTIL` fails only as `WAIT` does, on a Duration that isn't a Number.
- **The condition names no new Values.** Its Placeholders must be certainly filled before the `WAIT`, or be blanks (`?`), because after a timeout nothing would fill them. To use what was found, test it again with `IF` or `GIVEN`.
- **A wait with no limit may never end.** Whether the condition can come true is the game's design, not the language's, so there is no warning. A Plan stopped while it waits just stops, as with `WAIT`.
- It is the Agent's own choice to wait, so it belongs in Playbooks as well as in Plots.

## `AFTER`: a timeout in a Plot

A Phase Block, or `DURING PLOT`, can run a Plan once a Duration has passed:

```regia
DURING reception:
    WHEN ENTERED:
        DO play_music

    AFTER 30 SECONDS:
        ENTER feast

    WHEN food_served:
        ENTER feast
```

- **`AFTER <Duration>:`** is a Trigger kind of Director Plans. In a Phase Block it counts from entering the Phase; in `DURING PLOT`, from the start of the Staging.
- **The Duration is an Expression, worked out once** when the count starts. A Duration that isn't a Number fails the Plan, as for `WAIT`.
- **Its Context is tested when the time is up**, since that is when the Trigger fires. A false Context means the Plan doesn't run, with no entry.
- **It starts alongside the `ENTERED` Plan** (chapter 20, step 6 of a transition, and step 3 of starting a Staging), and runs as an ordinary Plan of its Block: it may have a Context, `WAIT`, `ENTER` and `END PLOT`.
- **Leaving the Phase stops it silently**, counting or running, like every Plan of the Phase (chapter 20). `DURING PLOT`'s stop when the Staging ends. Re-entering the Phase starts the count again.
- **A Block may have several `AFTER` Plans**, each counting on its own.
- **`AFTER` is for Plots only.** A Playbook describes what its Agent decides, and a timeout imposed from outside is the Plot's nudge (chapter 20). An Agent that chooses to wait writes `WAIT` or `WHEN ASSIGNED: WAIT …`.

## Transpiler checks

**Errors**

- `R1201` `WAIT` without a unit word, or with a word that isn't `SECOND`, `SECONDS`, `MINUTE` or `MINUTES`.
- `R1202` A Duration whose Placeholders aren't certainly filled before the `WAIT`.
- `R1204` A Placeholder in a `WAIT … UNTIL` condition that isn't certainly filled before the `WAIT` and isn't a blank.
- `R1205` `AFTER` in a Playbook (hint: `WAIT`, or `WHEN ASSIGNED: WAIT …`).

**Warnings**

- `R1203` A negative Number written directly as the Duration (`WAIT -2 SECONDS`).

## Trace entries

**Failures**

- `T1201` A Duration that isn't a Number.

**Warnings**

- `T1202` A negative Duration, counted as 0.

## Not in 2.0

2.0 has only `WAIT`. These belong to later versions (map: *Out of scope*):

- **Repeating Triggers** (`EVERY 10 SECONDS:`). Until they exist, a repeating Cue such as `digestion_check` is an External Cue that the game sends.
- **Timeout clauses** on waiting Statements (`PURSUE g, WITHIN 30 SECONDS`, `DO a, WITHIN …`), and the reserved trailing clauses on Message Statements (chapter 07). A Body that must not wait too long on a Goal starts it `WITHOUT WAITING` and uses `WAIT d, UNTIL` on a Fact its `REACHED` Plan learns.
- **The game's time scale.** The clock stops while the game is paused, but a game running at double speed doesn't make Durations shorter. That needs a clock the game owns.

So in 2.0, nothing to do with time can fail a Plan except a Duration that isn't a Number, and the limit of a `WAIT … UNTIL` running out is not a failure.

## Reserved words

Every keyword is listed in chapter 01, *Reserved words* (`01-statements-and-blocks.md`).

## ASL mapping notes

For *The full ASL mapping* and *Supporting multiple Targets* to pick up:

- **Jason:** `WAIT` maps to `regia.wait(D)` and `WAIT … UNTIL` to `regia.wait(Cond, D)`, both on the run's one clock (chapter 39, `39-jason-plan-bodies.md`). A negative Duration is clamped to 0 with `T1202`.
- Dropping the intention (`.drop_desire`, chapter 08) during a `regia.wait` removes it, which gives the "just stops" behaviour.
- **`WAIT … UNTIL`** suspends only its own intention, tests the condition when it is reached and again whenever what it tests changes, never fails on running out of time, and writes a `time` entry saying whether the condition was met or the time ran out (chapter 39).
- **`AFTER d:`** compiles to a generated Goal of its own, posted right after `ENTERED`'s, whose plan waits `D` with `regia.wait` and then tests the Context and runs the Body. In a Phase its intention is tagged with the Phase like `ENTERED`'s, so leaving the Phase drops it. Two counts that end together run in the order they were posted. See chapter 30, *`AFTER`*.
- **Pausing** stops the run's one clock, held in `regia-jason`: `regia_pause` and `regia_resume` reach the game link (chapter 37), and every `regia.wait` in the run, in Agents and Directors, is measured on that clock.
- **Game clock (VEsNA/Godot):** the Target must wait on the game's time, for example by asking the environment to send a generated wake-up Cue after `D` game-time milliseconds and waiting for that Cue. Which clock a Target uses is per Target. The Jason Target uses the wall clock, stopped while the game is paused, with no setting (chapter 28); a clock that follows the game's time scale is post-2.0.

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025): `WAIT … UNTIL`, `AFTER` and the paused clock included.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- A Director's Plans can use `WAIT` (chapter 20).
- Timers, repeating Triggers, and timeout clauses: out of scope for 2.0.
- How Targets other than Jason pick their clock: out of scope for 2.0 (Jason: chapter 28).
