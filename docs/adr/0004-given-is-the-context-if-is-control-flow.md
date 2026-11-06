# GIVEN is the Context; IF is control flow

A Plan's Context is written with `GIVEN`, as a Block nested under its Trigger, and is checked once when the Plan is chosen. `IF`/`ELSE` are Statements in the Body, checked when execution reaches them. Several `GIVEN` Blocks under one Trigger are separate Plans, and only the first in the text whose Context holds runs, else the `ELSE`. In 1.0, `IF` meant both. It read like general-purpose control flow but behaved as an exclusive Context. Any Statements written before it actually ran after it had been checked, and real branching inside a Body was impossible.

We keep 1.0's grouping (several Plans under one Trigger) because designers think in "when X: if happy…, if angry…, else…". We made "first match wins" a guarantee of the language, not a side effect of ASL plan order. In ASL, each Plan's context is ANDed with the negation of the earlier ones, and Placeholders not filled by the Trigger get fresh names in the negated copies.

## Considered Options

- **Keep 1.0's `IF` as the Context**: no change for 1.0 users, but no real branching, and the misleading order of execution stays.
- **`GIVEN` as a header clause** (`WHEN e GIVEN c:`): one header is one Plan, and nothing nests, but grouping several Contexts under one Trigger is lost.
- **`GIVEN` as a clause line inside the Plan**: no extra indentation, but it's a line that looks like a Statement and isn't one.
- **Rely on source order for exclusivity**, as 1.0 did: simpler emitted ASL, but it silently breaks if anything reorders plans at runtime (loading Playbooks at runtime, a priority model using `select__option/4`).

## Consequences

- Every Plan with a Context takes an extra indentation level (or a nested Inline block on one line).
- 1.0 code needs migrating: `IF` directly under `WHEN` becomes `GIVEN`, and prefix Statements must be moved into each Plan.
- The Transpiler renames Placeholders in the negated contexts, and warns about a `GIVEN` that an earlier one always catches.
- Emitted ASL contexts grow quadratically with the length of a `GIVEN` chain.
