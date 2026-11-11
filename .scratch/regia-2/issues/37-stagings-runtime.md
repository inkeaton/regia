# Stagings and Subplots runtime in ASL

Type: grilling
Status: open
Blocked by: 34, 35, 36

## Question

How do Stagings and Subplots run in Jason (spec 17)? Decide:
- A runtime identity per Staging, carried in Givings and Signals.
- Starting a Subplot's Director with its cast.
- The children-first ending walk, with its `ended` message to the parent.

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
- From *Giving and taking Playbooks at runtime* (35): `regia_given` and `regia_cast` carry an opaque `Staging` argument whose shape is decided here; the giving Director's agent name is stored separately, so the Staging id needn't be it. A Staging ending sends `regia_take(P, S, all)` to its cast for each Playbook it gave (chapter 29).
