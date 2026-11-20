# Names are declared

Every Name written in the source is declared with `NAME`, and a Name that isn't is an error (spec 03). Vocabulary items were already declared and checked, but the Values that fill them were not: `DO walk_to(kitchn)` compiled and sent the Servant to a place the game had never heard of, and `craves(roast)` matched the kitchen's `roast` only if both sides spelt it alike.

Only the source is checked. Names that arrive at runtime, from the game or in Messages, are not, since the game may use Names the Program never writes.

## Considered Options

- **Typed parameters** (`walk_to(place: Place)`): they would also catch a correct Name in the wrong slot, but need a type system for Numbers, Names and Agents. Deferred past 2.0; the `name: type` form stays free.
- **A Placeholder known to hold an Agent of a Role** (`?winner: Guest`): needs types first. Deferred with them.
- **Leave Names undeclared**: the mistake shows only at runtime, as a Plan that silently does nothing.

## Consequences

- A Program lists its Names, usually in the shared Vocabulary file. A Playbook file may re-declare the ones it uses.
- Names share the program-wide namespace with Vocabulary items, Playbooks and Plots.
- A Name can still go in a slot it doesn't suit. Types are what will catch that.
- In Regia 1.5 (ADR 0025).
