# Context vs control flow

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo

## Question

Should the Context of a Plan be separate from control flow inside its Body (primer ch.4)? In 1.0, the `IF`s directly under a `WHEN` behave as mutually exclusive Contexts (like `ELSE IF`). The proposal is to use `GIVEN` for the Context and let `IF`/`ELSE` behave as in general-purpose languages. Decide the keywords and semantics, whether the 1.0 grouping shorthand survives, and what operators logical expressions use and in what order.

## Answer

Spec chapter: `docs/spec/06-context-and-control-flow.md`. ADR: `docs/adr/0004-given-is-the-context-if-is-control-flow.md`. Glossary: Context, Plan, Trigger, Statement, Block revised.

- **`GIVEN` is the Context**, checked once when the Plan is chosen; **`IF`/`ELSE IF`/`ELSE` are Body Statements**, checked when reached, nestable.
- **Grouping kept (1.0 shape)**: `GIVEN` is a Block nested under the Trigger; several `GIVEN`s under one Trigger are separate Plans, first in the text whose Context holds wins, optional `ELSE:` last. A Trigger Block holds either a Body or `GIVEN`/`ELSE` Blocks; 1.0 prefix Statements are dropped. Plans in a group share the whole Trigger (Placeholders, `FROM`, header Labels). Doc comment above the Trigger covers all; above a `GIVEN` covers one. Warning for a `GIVEN` an earlier one always catches. No new term for the group.
- **Operators**: `AND`/`OR`/`NOT`/`( )`, comparisons > `NOT` > `AND` > `OR`; mixing `AND` and `OR` without parentheses is an error.
- **Placeholders in `IF`**: filled by matching, usable only in that branch; sibling branches may reuse a name, reuse elsewhere in the Plan is an error. Maps 1:1 onto Jason's `if/elif/else`.
- **ASL**: each `GIVEN` plan's context is ANDed with the negation of the earlier siblings', with fresh variable names for Placeholders not filled by the Trigger, so exclusivity doesn't depend on plan order.
- **Targets without `if`** (in-house interpreters): an `IF` chain is lowered to an internal subgoal with one plan per branch (same negation encoding, empty `ELSE` generated). The encoding is picked with an Instancing comment such as `#% ASL_VERSION = JASON/GENERIC`, decided in *Instancing comments*.
- **No loops** in 2.0 (deferred).

## Comments

From *Parameters and variables* (03): Placeholders (`?name`) are filled in the Trigger and Context and used in the Body. Decide whether an `IF` inside a Body can also fill Placeholders, and if it can, where they can be used. Inside its branch only? The "only what's certainly filled" rule (`NOT`, `OR`) applies either way. See `docs/spec/03-parameters-and-placeholders.md`.

From *Numbers and arithmetic* (04): in a Context, `=` only compares and never fills; in a Body, `?name = Expression.` names a value (ADR 0002). Comparisons bind tighter than `NOT`/`AND`/`OR`; the order among `NOT`/`AND`/`OR` is left to this ticket. If Body `IF`s can fill Placeholders by matching Facts, the rule that a name is usable after an `IF` only if every branch fills it already applies to Body naming. See `docs/spec/04-numbers-and-expressions.md`.
- From *Goals and Trigger kinds* (05): a Context can test `PURSUING g` (matching as for Facts); Events can never be tested. See `docs/spec/05-goals-and-triggers.md`.
