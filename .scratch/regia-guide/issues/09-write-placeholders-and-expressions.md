# Write: Placeholders and Expressions

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Task

Write `docs/guide/5 - Placeholders and Expressions.md`.

Covers: `?name`, filling by matching in Trigger and Context, naming in the Body with `?name = …`, filled once, arithmetic and Expressions.

Sources: 03, 04; ADR 0001, 0002, 0006.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-12: [`docs/guide/5 - Placeholders and Expressions.md`](../../../docs/guide/5%20-%20Placeholders%20and%20Expressions.md), about 2,900 words counting snippets, tables and the diagram, over seven sections (a blank in a Trigger, blanks in the Context, the bare `?`, only what is certainly filled, blanks filled in a Body, naming a value, Expressions). Not yet read by the user.

- **Checked against** spec chapters 03, 04, 05 (`FROM`), 06, 09, 15, 16, 18, 21 and 26, and ADRs 0001, 0002 and 0006. Snippets under a path line are cut from the showcase; the eight without one are throwaway variants.
- **Showcase changed**: `TO fetch(?dish, ?place)` in `Serving` never used `?place`, which earns chapter 03's unused-Placeholder warning. It is now `TO fetch(?dish, ?)`. No chapter quoted the line.
- **Eight `#revise`**: a Placeholder that is tested and one that is filled look the same; a bare `?` hides what it ignores, and naming it for the reader earns a warning; the laughing alternative in `NobleSocializing` carries an unused `?who` to match its siblings; a name filled by an `IF` is gone after its branch and still can't be reused; `=` compares after `IF` and names at the start of a line, both in a Body; a name made in every branch of an `IF` can be used afterwards and one made in every Option of an `EITHER` can't (chapters 04 and 09 disagree); nothing rounds, so `RANDOM(1, ?gold / 2)` rolls whole or decimal depending on the purse; a count in a Mapping, a Quota quantity and an Instancing value look alike and allow different amounts of calculation.
- **README**: one new entry under *Gaps in the showcase* (no Value in a Trigger slot, no joined Context, no Placeholder under `NOT`, no `IF` that fills, no naming in a branch) and three under *Spec wording* (comparison written before the Fact that fills it; what "the same Trigger" means for Suits alternatives; reusing a name in a second `FOR EACH`).
- **Drift for the consistency pass**: *Matching*'s *Since 1.0* says 1.0 Facts took no parameters; the primer and *Vocabulary* say they took fixed ones, and this chapter follows them.
- `humanizer:humanizer` run as the last pass.
