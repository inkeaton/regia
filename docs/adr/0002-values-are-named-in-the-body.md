# Values are named in the Body, never in the Context

A Plan's Body can name a computed value with `?name = Expression.`, filling a Placeholder once and never reassigning it. In a Context, `=` only compares and never fills anything. We chose this so that a Context stays a list of conditions on the world, and calculations happen as steps in the Body, where a designer expects things to be done. It also gives `=` one meaning in each place, so a reader never has to scan back to tell whether it compares or fills. The main need it covers is reusing one random roll (`?dmg = RANDOM(1, 6).`), which inline Expressions can't do.

## Considered Options

- **`=` fills in the Context too** (as in Jason, where `X = Y + 1` unifies): one way to name things everywhere, but a Context then hides calculation steps among its conditions, and `=` compares or fills depending on what came before.
- **No naming at all**: Expressions are repeated, and anything reused is stored as a Fact. This is the simplest option, but a random roll can't be used twice in one Plan run.
- **Random as a Context condition that fills** (`?dmg IS RANDOM 1 TO 6`): it keeps naming out of the Body, but it's a special case for one function and still puts a calculation in the Context.
- **A `LET ?x BE …` keyword**: impossible to mistake for a comparison, but an extra keyword that reads like programming.

## Consequences

- This amends ADR 0001: Placeholders are filled by matching in the Trigger and Context, **or** by naming in the Body. They are still filled once and never reassigned.
- Naming an already-filled Placeholder is an error. A name can be used only after its Statement, and after an `IF` only if every branch names it.
- If repeated Expressions in Contexts turn out to hurt, Context-side naming could be added later without breaking existing code.
