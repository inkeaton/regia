# Context vs control flow

Type: grilling
Status: open

## Question

Should the Context of a Plan be separate from control flow inside its Body (primer ch.4)? In 1.0, the `IF`s directly under a `WHEN` behave as mutually exclusive Contexts (like `ELSE IF`). The proposal is to use `GIVEN` for the Context and let `IF`/`ELSE` behave as in general-purpose languages. Decide the keywords and semantics, whether the 1.0 grouping shorthand survives, and what operators logical expressions use and in what order.

## Comments

From *Parameters and variables* (03): Placeholders (`?name`) are filled in the Trigger and Context and used in the Body. Decide whether an `IF` inside a Body can also fill Placeholders, and if it can, where they can be used. Inside its branch only? The "only what's certainly filled" rule (`NOT`, `OR`) applies either way. See `docs/spec/03-parameters-and-placeholders.md`.

From *Numbers and arithmetic* (04): in a Context, `=` only compares and never fills; in a Body, `?name = Expression.` names a value (ADR 0002). Comparisons bind tighter than `NOT`/`AND`/`OR`; the order among `NOT`/`AND`/`OR` is left to this ticket. If Body `IF`s can fill Placeholders by matching Facts, the rule that a name is usable after an `IF` only if every branch fills it already applies to Body naming. See `docs/spec/04-numbers-and-expressions.md`.
- From *Goals and Trigger kinds* (05): a Context can test `PURSUING g` (matching as for Facts); Events can never be tested. See `docs/spec/05-goals-and-triggers.md`.
