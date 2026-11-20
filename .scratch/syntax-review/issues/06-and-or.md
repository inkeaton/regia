# `AND`, `OR` and `EITHER`

Type: grilling
Status: closed
Assignee: claude (with Edoardo)
Blocked by: 01, 02

## Question

`AND` is boolean, but it also joins the Propensities of a Label (`SUITS a AT x AND b AT y`), the Moods of `SHIFT`, and the Roles of `KIND … PLAYS Guest AND Drunkard`. `OR` is boolean, but it is also the Option header `OR:` of a Random choice and, in 2.0, the Sender alternatives `FROM a OR b`.

Decide whether the list uses become `,` lists under the comma rule (*The comma*), and whether Random choice keeps `EITHER:` / `OR:` or takes another pair of words. Done when chapters 05, 06, 09, 14 and 21 and their examples are edited.

## Resolution

Grilled with the user on 2026-11-20. Applies ADR 0041 and the one-meaning rule; no new ADR.

1. **`AND` is only the boolean operator.** Its list uses become `,` lists: `SUITS a AT x, b AT y, SHIFTS m BY n:`, `SHIFT a BY x, b BY y.`, `KIND …, LIKE noble, PLAYS Guest, Drunkard:` (and `AGENT`). The list ends at a clause keyword after `,` (*The comma*). `AND` there is a retired spelling: `R1412` (chapter 14), `R2125` (chapter 21). A repeated Label stays `R1401`.
2. **`FROM a OR b` keeps `OR`**: it is the boolean `OR` over who sent it, never a `,` list. Chapter 05 says so; chapter 01 states that `AND`/`OR` never join list items.
3. **Random choice is a container**: `RANDOMLY:` holding `OPTION:` Blocks (`OPTION, WEIGHT e:`). Only `OPTION` Blocks stand directly under it. `RANDOMLY` was chosen over `ONE OF` (clashes with `n OF`, owned by *Quantities*) and `CHOOSE` (reads as a reasoned choice). `WEIGHT` is left to *Quantities*.
4. **Checks (chapter 09):** `R0901` a `RANDOMLY` with no Option (error); `R0902` an `OPTION` outside `RANDOMLY` or another Statement directly under it (error); `R0905` a single Option (warning: it always runs, but a generator may produce it); `R0906` the retired `EITHER:` / `OR:` headers (error with hint; `EITHER` stays reserved). The lowered subgoal is renamed `regia_randomly__N`.
5. **Glossary:** Random choice and Option reworded.

Edited: chapters 01, 04, 05, 06, 08, 09, 11, 13, 14, 15, 16, 21, 26, 34, 35, 39; `GLOSSARY.md`; cases `09-random-choice/randomly-without-options.regia` (was `either-without-or`), `09-random-choice/either-is-retired.regia`, `14-labels/and-in-a-label-is-retired.regia`, and `21-instancing/plays-a-role-the-root-plot-lacks/game.regin`. The Conformance cases have no annotation for warnings, so `R0905` has no case.
