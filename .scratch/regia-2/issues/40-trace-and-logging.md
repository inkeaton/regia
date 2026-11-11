# Trace and logging

Type: grilling
Status: open
Blocked by: 34

## Question

What trace does a running Program leave, for debugging and runtime verification? Decide the format, routing and runtime monitoring of the trace that failures and runtime warnings leave (spec 11), and the logging of Agent actions.

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
- From *How a spec chapter proves itself* (33): this ticket must also define the `.trace` expectation format for behaviour Conformance cases, and how a case scripts its run (Events from the game, Agents joining and leaving). See `docs/spec/27-conformance.md`.
- From *Director runtime in ASL* (36): new Trace sources are a failed `EXITED` Plan (the transition carries on), a skipped Role setup Statement, and a `?who` Giving or Mapping dropped because the Agent isn't in the cast (chapter 30).
- From *Stagings and Subplots runtime in ASL* (37): new Trace sources are a failed `EXITED` during an ending (the ending carries on), and an ending Staging (chapter 31).
