# Groups

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 03

## Question

What does a Group mean, and how is it used (primer ch.3)? A Group is a named set of Vocabulary items, distinct from Multi-definition. Decide its syntax (`FACT GROUP name: a, b, c`?), whether Groups can mix kinds, how they are used (random choice of an Action, "any Fact in group" in a Context, …), and whether that choice can be weighted.

## Comments

From *Parameters and variables* (03): "pick one at random" and "for every match" over a Context's matches are in the map's fog under match selection. If Groups bring a random-choice construct, check whether the same construct should also cover Placeholder matches.
- From *Basic Action set* (07): no Basic Action works over Groups yet. Decide whether picking an Action from a Group (e.g. at random, weighted) is a Statement of its own, and how it reads next to `DO`. See `docs/spec/08-basic-actions.md`.

## Answer

Spec chapter: `docs/spec/09-random-choice.md`. Glossary: *Group* removed; *Random choice*, *Option*, *Weight* added; *Multi-definition* and *Statement* revised. No ADR (dropping Groups is easy to reverse).

- **No Groups.** A declared Group adds nothing the rest of the language lacks: random choice is a Body Block, "any of a family" in a Context is a parameterised Fact (`GIVEN mood(?m)`), a reusable choice is a Goal whose recipe chooses, and Multi-definition declares several items at once. `GROUP` is not reserved, and nothing goes into the fog.
- **Random choice:** `EITHER:` followed by one or more `OR:` Blocks at the same indentation; exactly one Option runs, then the Body carries on. An Option is any Block (inline or indented), mixing Statement kinds and nesting. `EITHER` with no `OR` is an error (use `IF … RANDOM` for "sometimes"). Options have no conditions of their own; use an `IF` inside, or a weight of 0.
- **Weights:** trailing clause `, WEIGHT <Expression>` on the header, 1 by default, relative to the sum. All weights are worked out once, before the roll. 0 means never; a negative weight counts as 0 and writes a runtime warning; a non-Number fails the Plan; if every weight is 0, nothing runs, a runtime warning is logged (when the Target has a log), and the Body carries on. Named levels (`OFTEN`) are not in 2.0.
- **Placeholders** filled inside an Option live only in that Option; sibling Options may reuse a name (the `IF` branch rule, spec 06).
- **Match selection** (random or every match of a Context) stays in the fog; `EITHER` covers written Options only.
- **ASL:** weights into fresh variables, clamp with a warning, `math.random(T)`, an `if`/`elif` chain on running sums; for Targets without a native `if`, a generated subgoal like `IF` lowering.
