# Context vs control flow

Type: grilling
Status: open

## Question

Should the Context of a Plan be separate from control flow inside its Body (primer ch.4)? In 1.0, the `IF`s directly under a `WHEN` behave as mutually exclusive Contexts (like `ELSE IF`). The proposal is to use `GIVEN` for the Context and let `IF`/`ELSE` behave as in general-purpose languages. Decide the keywords and semantics, whether the 1.0 grouping shorthand survives, and what operators logical expressions use and in what order.

## Comments

From *Parameters and variables* (03): Placeholders (`?name`) are filled in the Trigger and Context and used in the Body. Decide whether an `IF` inside a Body can also fill Placeholders, and if it can, where they can be used. Inside its branch only? The "only what's certainly filled" rule (`NOT`, `OR`) applies either way. See `docs/spec/03-parameters-and-placeholders.md`.
