# Placeholders are filled by matching, not assigned

Regia has no mutable variables and no assignment statement. A Plan's unknowns are Placeholders (`?name`): blanks filled by matching in the Trigger and Context, filled once per Plan run, and used read-only in the Body. Anything an Agent must remember or change over time lives in Facts. We chose this because it maps one-to-one to BDI logic variables in the Target, and because it keeps the audience (game designers) away from the hardest part of programming, which is state that changes over time. We call them Placeholders rather than variables so that designers don't expect assignment.

## Considered Options

- **Programming-style variables** (`x = 5`, reassignable): familiar from Twine and Blueprints, but they don't exist in the BDI model, so the Transpiler would have to simulate them, and they would compete with Facts as a place to keep state.
- **Trigger parameters only, with names taken from the declaration** (`WHEN insult_heard:` and then using `speaker`): no new symbol, but no open questions in Contexts (`IF hates(?someone)`), no Triggers that filter on a Value, and an implicit second way to name things.
- **Marking Placeholders with capitals (as in Jason) or `$`**: capitals clash with Role names, and `$` suggests mutable variables. `?` is used by PDDL, CLIPS and SPARQL for the same concept, and reads as a question.

## Consequences

- When a Context has several matches, which one is used is unspecified. Explicit choice (random, every match, ranking) has to be its own construct.
- If `LET`-style naming of computed values is added (see *Numbers and arithmetic*), it must also be filled once and never reassigned.
