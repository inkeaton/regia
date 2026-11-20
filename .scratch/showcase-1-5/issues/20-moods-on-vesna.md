# Moods and Labels on VEsNA-Pro

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05, 10

## Question

Group K of the [inventory](../jason-open-questions.md#k-temper-and-moods-moods-and-labels-on-vesna-pro): chapter 14 promises Moods in [-1, 1] and `SHIFTS` when a Plan runs, and its notes say VEsNA-Pro keeps [0, 1] and shifts only a contested choice.

Decide:

- what a negative Mood is in the `.jcm` and in `most_similar` (with the research on `Temper`);
- whether, and how, a `SHIFTS` Label applies on a Plan that runs uncontested;
- how `regia.shift` and the Trace's hooks reach `Temper`: an upstream patch, a subclass, or reflection.

Closes when chapters 14 (notes), 28 and 36 are edited.

## Comments

**Upgrade test (2026-11-18).** VEsNA-Pro builds and runs on JaCaMo 1.3.1, which resolves Jason 3.3.2 and CArtAgO 3.1, with only `jacamo:1.2` → `jacamo:1.3.1` changed in `build.gradle`. Built with Jason's `gradlew` (Gradle 9.7.1) on JDK 21; Gradle 9.7.1 can't run on the default JDK 27. Its example `vesna.jcm`, run against a stub WebSocket game, prints the same output on JaCaMo 1.2 and 1.3.1: four `ciao`, then `ciao ciao`, once the `effects` have shifted `prop3`. It sends the same `walk`, `rotate` and `jump` messages too. A headless run needs a `logging.properties` in the project folder with a `ConsoleHandler`. So moving VEsNA-Pro to Jason 3.3.2 is an option for this ticket to decide, next to how `regia.shift` reaches `Temper`.

The upgrade, the `Temper` changes and the bugs the research found are collected in [*Changes to VEsNA-Pro for Regia*](../../implementation/vesna-pro-for-regia.md). Decide here which of them Regia relies on, and update that list.

## Resolution

Grilled with the user on 2026-11-19. Chapters 14, 28, 32, 34, 35 and 36 were edited (and a version note added to 23, 31, 33, 39 and 40), along with the list [*Changes to VEsNA-Pro for Regia*](../../implementation/vesna-pro-for-regia.md).

1. **Negative Moods need nothing.** `Temper` already takes Moods, targets and `effects` in [-1, 1]. Chapter 14's "Regia follows the code, [0, 1]" note was wrong and is gone. `most_similar` compares |Mood − target|, and the `.jcm` writes negative values as they are.
2. **The language promises when a `SHIFTS` Label applies**: once, when the Plan is chosen, before its first Statement, whether or not it was contested, on every Target. A Mood is kept within [-1, 1]. `R1410` is retired, and the item leaves chapter 14's *Not in 2.0*.
3. **`SHIFTS` stays a plan annotation** (`effects([…])`). The user wants plain, universal ASL wherever possible, with as few custom internal actions as possible. `RegiaAgent.selectOption`, which Jason calls once for every event once it is overridden, applies the chosen plan's `effects` through `Temper.shift` and writes the `mood` entries. Only the `SHIFT` Statement, whose amount is known only at run time, uses `regia.shift`.
4. **Temper never schedules intentions.** VEsNA's `selectIntention` picks the next running intention by Mood, which lets unlabelled intentions (all the `regia_*` plans too) always step first, and it applies `effects` on every step. `RegiaAgent.selectIntention` is Jason's round-robin `intentions.poll()`.
5. **An upstream patch** to VEsNA-Pro, with only `VesnaAgent.getTemper()`, `Temper.shift(mood, delta)` (clamped, which fixes the below -1 → 0 bug), and `random` weights that fall as the `most_similar` score rises (with `computeWeight` returning that score under both strategies). `strategy = random` stays accepted. Fits come from the public `computeWeight` in `selectOption` (chapter 32, new step 5), so there's no Trace hook in `Temper`.
6. **JaCaMo 1.3.1 / Jason 3.3.2** is adopted (chapter 28, *Platform versions*), as part of the same patch.
7. **Moods live only in `Temper`**, the Agent's own state, with no mirror belief. The `TEMPER` `cast` entry and the `mood` entries show them.

No glossary terms and no ADR: these are Target choices, easy to change.
