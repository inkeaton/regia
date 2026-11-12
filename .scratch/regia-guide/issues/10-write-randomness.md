# Write: Randomness

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Task

Write `docs/guide/7 - Randomness.md`.

Covers: `EITHER`/`OR` and Weights, random rolls in Expressions, `, AT RANDOM` Picks, `RANDOM` in Instancing, the seed.

Sources: 09, 04, 26, 21.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-12: [`docs/guide/7 - Randomness.md`](../../../docs/guide/7%20-%20Randomness.md), about 2,650 words counting snippets and tables, over seven sections (one of several Options, Weights, rolls, Picks at random, a random part of a Role, random starting values, the seed). No diagram: nothing here is a relation between parts. Not yet read by the user.

- **Checked against** spec chapters 04, 09, 12, 13, 14, 15, 16, 21, 26, 34, 35 and 36, and chapter 01 for empty Blocks. Snippets under a path line are cut from the showcase; the three without one are throwaway variants.
- **Wider than the ticket**: counted Mappings (`1 OF Guest`, chapter 15) got a section of their own, since they are a fifth place where chance enters and the showcase's Poisoner depends on one. The seed is not in the ticket's sources (09, 04, 26, 21): it is in chapters 34 to 36, and only as the header of a behaviour case.
- **Showcase unchanged.**
- **Eleven `#revise`**: `OR` is a condition operator and an Option header; "only sometimes" needs an empty Option (which warns) or `IF RANDOM(1, 100) <= 30:`, which states a chance in hundredths while Weights state it in shares; a wrong Weight is repaired, skipped or fails the Plan depending on how it is wrong; a roll is whole or decimal by how its bounds are written (`WAIT RANDOM(1, 3) SECONDS.` never waits 1.4); Options have Weights and Matches don't, so "the bigger the grudge, the likelier" can't be written; `bravery AT RANDOM(-1, 1)` has whole bounds; the seed can only be set in a behaviour case, so a real run can't be replayed; the seed's coverage is a list of constructs that leaves out Body rolls and counted Mappings; two sibling `GIVEN`s with the same roll don't have the same chance; the Role setup roll, once or per Agent (repeats the README's note); `1 OF Guest` can cast a knight as Poisoner and Watchman of one Staging, and a counted Mapping can't exclude anyone.
- **README**: one new entry under *Gaps in the showcase* (Options of one Statement only, no nested or Director Random choice, no roll in a condition, `AT RANDOM` only after `HIGHEST`, one plain counted Mapping) and two under *Spec wording* (what the seed covers; whole bounds in an Instancing `RANDOM`).
- **Drift for the consistency pass**: this chapter says a runtime warning goes "to the Trace" (chapter 34), where chapter 09 still says "the log". *Placeholders and Expressions* already holds the `#revise` on names made in Options, and *Matching* the one on the three readings of `AT`; this chapter points to the first and doesn't repeat the second.
- `humanizer:humanizer` run as the last pass.
