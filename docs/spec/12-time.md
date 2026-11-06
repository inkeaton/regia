# Time

How Regia deals with time: writing a Duration, pausing a Body with `WAIT`, and what measures the time. Decided in the ticket *Time and timers* (`.scratch/regia-2/issues/12-time-and-timers.md`). It builds on chapters 03, 04, 08 and 11, and replaces `WAIT()` in primer ch.4.

## The clock belongs to the Target

- **The language fixes Durations, and the Target owns the clock.** A Plan says "3 seconds". The Target decides what measures them: wall-clock time, or game time that stops when the game is paused and follows its time scale.
- **One Program uses one clock.** Every Duration in it is measured the same way, so two Agents waiting 3 seconds wait the same length of time.
- Facts about the time of day (`is_night`) are ordinary Facts, usually External ones that the game keeps up to date (chapter 10). They have nothing to do with this chapter.

## Durations

```regia
WAIT 3 SECONDS.
WAIT 0.5 SECONDS.
WAIT 1 MINUTE.
WAIT RANDOM(2, 5) SECONDS.
WAIT ?delay * 2 SECONDS.
```

- A **Duration** is an Expression (chapter 04) followed by a unit word: `SECONDS` or `MINUTES`. `SECOND` and `MINUTE` are accepted too, and the singular and plural forms are interchangeable (`1 SECONDS` and `2 MINUTE` are both fine).
- **The unit is always written.** `WAIT 3.` is an error.
- There are no symbol shorthands (`3s`) and no smaller units. Fractions cover them: `0.1 SECONDS`.
- The unit word comes after the whole Expression: `WAIT ?delay * 2 SECONDS.` waits `?delay * 2` seconds.
- Placeholders in the Expression must be **certainly filled** before the `WAIT` (chapter 03).

## `WAIT`

`WAIT <Duration>.` is a Basic Action (chapter 08), written without `DO`.

```regia
WHEN food_served:
    DO sniff_air.
    WAIT RANDOM(1, 3) SECONDS.
    DO eat_food.
```

- **It pauses only the Body it's in.** The Agent keeps reacting while it waits, and its other Plans run as usual.
- **A waiting Plan is still running.** If it is the recipe for a Goal `g`, then `g` is still being pursued, and Bodies waiting on `g` with `PURSUE g.` keep waiting.
- **The Duration is worked out once**, when the Body reaches the `WAIT`.
- **`WAIT 0 SECONDS.` carries on at once.**
- **A negative Duration counts as 0**, and the Agent writes a **runtime warning** to the trace (chapter 11), the same as a negative Weight (chapter 09). The Body carries on.
- **A Duration that isn't a Number fails the Plan**, like any Body arithmetic (chapter 04). This is the only way `WAIT` fails. What failing does is in chapter 11.
- **A Plan stopped during a `WAIT`** (by `DROP`, or because its Playbook is taken away) just stops. The wait isn't a failure of its own. What gets reported is whatever stopped it, such as the Goal's `DROPPED` (chapter 08).
- `WAIT` means the same wherever it's allowed. Whether a Director's Plans can use it is decided in *Director capabilities*.

## Transpiler checks

- **Warning:** a negative Number written directly as the Duration (`WAIT -2 SECONDS.`).
- **Error:** `WAIT` without a unit word, or with a unit word that isn't one of the four above.

## Not in 2.0

2.0 has only `WAIT`. These belong to later versions (map: *Out of scope*):

- **Repeating Triggers** (`EVERY 10 SECONDS:`). Until they exist, a repeating Event such as `digestion_check` is an External Event that the game sends.
- **Delayed Triggers** (`AFTER 30 SECONDS:`), counted from entering a Phase or from a Playbook being given, for timeouts on a Phase. Until then, a Director can only approximate them with `WAIT` in a Phase Plan, if *Director capabilities* allows it.
- **Timeout clauses** on waiting Statements (`PURSUE g, WITHIN 30 SECONDS`), and the reserved trailing clauses on Message Statements (chapter 07).

So in 2.0, nothing to do with time can fail a Plan except a Duration that isn't a Number.

## Reserved words

`WAIT` (chapter 08), `SECOND`, `SECONDS`, `MINUTE`, `MINUTES`.

## ASL mapping notes

For *The full ASL mapping* and *Supporting multiple Targets* to pick up:

- **Wall clock (Jason):** `WAIT d SECONDS.` maps to `.wait(D)`, where `D` is the Duration in milliseconds (`d * 1000`, or `d * 60000` for minutes). `.wait` suspends only its own intention, as required. A constant Duration is folded by the Transpiler. Otherwise the Body works it out into a fresh variable, clamps negatives to 0 with a trace warning, and calls `.wait` on the result, as for Weights (chapter 09).
- Dropping the intention (`.drop_desire`, chapter 08) during a `.wait` removes it, which gives the "just stops" behaviour.
- **Game clock (VEsNA/Godot):** the Target must wait on the game's time, for example by asking the environment to send a generated wake-up Event after `D` game-time milliseconds and waiting for that Event. Which clock a Target uses, and how it is chosen, is per Target (*Supporting multiple Targets* fog).

## Not decided here

- Whether a Director's Plans can use `WAIT`: *Director capabilities*.
- Timers, repeating and delayed Triggers, and timeouts: out of scope for 2.0.
- How a Target picks its clock: *Supporting multiple Targets*.
