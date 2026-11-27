# Sweep cases for unsent Cues

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

About 25 cases in `docs/spec/cases/` declare a plain `CUE`, wait on it, and never send it, so under chapter 38 each also gets `warning R3807`, which no annotation expects. They fail once the case runner (M3) runs them.

Do: in each case, declare a Cue the game sends as `GAME CUE`, unless the case is about `R3807`. Check the result case by case for other unannotated Diagnostics (absence checks, chapter 23).

From *Review: Diagnostics and where checks live*.

## Resolution

Done on 2026-11-27. Each case was read against chapter 27's exact matching and the absence checks of chapter 23.

- **`R3807`**: 26 cases now declare the Cue they wait on as `GAME CUE`. The two traces (`failed-action-fails-its-goal`, `spawn-refused-in-1-5`) confirm the game sends theirs. Two plain `CUE`s stay, since their cases are about `R3807`'s silence: `welcome` in `misplaced-plan-is-left-out` (its only `TELL` is in the left-out Plan) and `scandal` in `cue-sent-in-broken-statement`.
- **`R0307`**: `clause-without-its-comma` and `later-word-in-a-1-5-build` filled `?s` and never used it. Whether the Plan is kept after `R0111` or `R0109` is a recovery detail, so both now write `?`. In `percent-only-before-of`, `?half` is now used by a `PRINT`. If the `LET` is kept, `?half` is used; if it is left out, `?half` is an unread name.
- **`R1004`**: `plot-parameter-in-a-setup` and `retired-starts-with` `LEARN` Facts they never declared. They now declare them (`FACT grievance(quarrel), accused(person)`; `FACT invited, banquet_tonight`).

Left open, outside this sweep: `randomly-without-options` has a `RANDOMLY:` with no body, so it may also get `R0106` beside `R0901`. Chapters 01 and 09 don't say whether `R0901` replaces it.
