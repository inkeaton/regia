# Decide: Showcase README coverage

Type: grilling
Status: open
Assignee:
Blocked by:

## Question

The showcase `README.md`'s *Coverage* promises things the showcase doesn't do:

- F34: `?offender` is said to be "used inside" `HonorDuel`, which never reads it. Should the README say it only tells the Stagings apart, or should the duel read it (for example in a Role setup)? (Guide: shows the use in a throwaway variation.)
- F42 (the README half): the printed Interfaces are placed in `runs/evening` and `runs/two_duels`, which don't exist yet. Keep them as a promise for the runs, or mark them as not yet written?
- F47: `NO AGENT percival` in `runs/short_evening` would get `R21_22-unknown-agent-argument` while `KIND hothead` learns `grudge(percival, 2)`. Writing the run is out of scope; should the README's line for it note the fix the run will need?

Prefer fixing the README over changing the showcase (map Notes).

Applying the answers is *Apply: Showcase README coverage*.
