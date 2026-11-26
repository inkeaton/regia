# Sweep cases for unsent Cues

Type: task
Status: open
Assignee:
Blocked by: none

## Question

About 25 cases in `docs/spec/cases/` declare a plain `CUE`, wait on it, and never send it, so under chapter 38 each also gets `warning R3807`, which no annotation expects. They fail once the case runner (M3) runs them.

Do: in each case, declare a Cue the game sends as `GAME CUE`, unless the case is about `R3807`. Check the result case by case for other unannotated Diagnostics (absence checks, chapter 23).

From *Review: Diagnostics and where checks live*.
