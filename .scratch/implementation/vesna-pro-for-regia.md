# Changes to VEsNA-Pro for Regia

Type: task (implementation)
Status: draft
Assignee:
Blocked by: none. How Regia reaches `Temper` was decided in [*Moods and Labels on VEsNA-Pro*](../showcase-1-5/issues/20-moods-on-vesna.md) on the showcase map (2026-11-19): an upstream patch, with only what's below.

## Question

What has to change in VEsNA-Pro (`references/vesna-pro-main/`) for the Jason Target to run Regia Programs? Collect each change here as the planning maps find it, with where it was found. Apply them when the Jason Target is implemented.

## Changes Regia relies on

1. **Move to JaCaMo 1.3.1, so Jason 3.3.2.** One line in `build.gradle`: `org.jacamo:jacamo:1.2` → `1.3.1` (CArtAgO becomes 3.1). Tested on 2026-11-18: VEsNA-Pro compiles unchanged, and its example `vesna.jcm`, run against a stub WebSocket game, behaves exactly as on 1.2. It needs JDK 21 or later. Gradle 9.7.1 also has to run on JDK 21, since it can't run on JDK 27. A headless run needs a `logging.properties` with a `ConsoleHandler` in the project folder. Not yet tried: percepts from the game, many agents, load on virtual threads. Adopted: chapter 28 says Regia runs on Jason 3.3.2.
2. **`VesnaAgent.getTemper()`**, public. The `temper` field and `initTemper` are private, so a subclass can't reach the Agent's `Temper` (chapter 14, *ASL mapping notes*).
3. **`Temper.shift(String mood, double delta)`**, public. It adds `delta` to the Mood and keeps it within [-1, 1]; a Mood the Agent doesn't hold is skipped. `regia.shift` (the `SHIFT` Statement) and `RegiaAgent.selectOption` (a `SHIFTS` Label's `effects`) both call it. This also fixes the bug where a Mood pushed below -1 is set to 0.
4. **`random` weights fixed.** `computeWeight` returns the `most_similar` score (Σ |agent − plan|) under both strategies, and `random` draws with weights that fall as that score rises, so the closest fit is the likeliest. Today `random` weighs by Σ Mood × target, which goes wrong for negative values, and its draw is wrong for fractional or negative weights. `RegiaAgent` reads `computeWeight` for the `plan` entry's `fits` (chapter 32, step 5).

Dropped: a hook in `Temper` for the Trace. `RegiaAgent` applies `effects` itself and reads fits through the public `computeWeight`, so it writes the Trace with no help from `Temper`.

## Fixes Regia doesn't rely on

- Leaving out `strategy` throws a `NullPointerException`. Chapter 36 always writes `strategy` with `temper`.
- The readme's `nearest` strategy is rejected.
- Two error messages state the wrong ranges ([0, 1] and [-100, 100]).

## Not a change

- Reading game messages: `regia.RegiaAgent` overrides the public `myHandleMsg` (chapter 37: "Nothing changes in VEsNA-Pro").
- Intention selection: `regia.RegiaAgent.selectIntention` overrides VEsNA's with Jason's round-robin (chapter 28), so VEsNA's `selectIntention`, and the `effects` it applies, are never used. Nothing changes upstream.
- The Directors' body: `regia.DirectorAgent` doesn't extend `VesnaAgent` (chapter 30), so its private, port-parsing body setup stays as it is.
