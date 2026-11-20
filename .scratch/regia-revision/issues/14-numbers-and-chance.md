# Numbers, rolls and repetition

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

Fix the rules for rolls and names that disagree, and settle the ones the spec doesn't give.

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- B4 A roll is whole or decimal by how its bounds are written
- B6 A name made in every branch outlives an `IF` and not an `EITHER`
- D15 Rules the spec doesn't give (the roll in a setup, the seed's coverage, wrong Weights)
- F5 No loop, and no weighted Pick
- F10 the short spellings (`CHANGE`, "only sometimes", `COUNT … = 0`, bare `HIGHEST`)

Decide:

- When a roll is whole, in a Body and in a `.regin` file, and whether anything rounds.
- One rule for names made in every branch.
- A setup's roll: once, or per Agent.
- What the seed covers.
- Loops, weighted Picks and the short spellings: 2.0, later, or a warning.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

## Resolution

Resolved on 2026-11-17, with the user. Each fix follows the map's rule on language and game design: what can be meant is allowed without a warning.

- **B4** fixed.
  - A roll's kind comes from the source: it is decimal when a bound is a decimal number written out, and whole otherwise, whatever Placeholders and Expressions hold. A whole roll gives the whole numbers from `a` to `b` (`RANDOM(1, 6.5)` gives 1 to 6). This is the only rounding a roll does.
  - Bounds in either order are the same range. A whole roll with no whole number between its bounds fails the Plan in a Body (new `T0403`), makes its comparison false in a Context, and is skipped in a setup.
  - A starting Propensity value in Instancing is always a decimal roll.
  - No exception for `WAIT`: a whole-second wait can be meant, and "any wait" is `RANDOM(1, 3.0)`.
- **B6** fixed. A name made in every Option of a Random choice outlives it, as with `IF`/`ELSE`. Sibling Options still reuse names. `R0904` narrowed.
- **D15** (the roll in a setup, the seed's coverage, wrong Weights) fixed.
  - A setup is the same Statements for every Agent, with its Expressions worked out per Agent, so a roll is made once per Agent. `ME` stays out of setups.
  - The seed covers every random draw the language makes, as a rule instead of a list. On Jason, all of them go through one seeded source, `regia.random`.
  - A negative Weight counts as 0, and all-zero Weights run no Option. Both get plain Trace entries (`T0902`, `T0903`), not warnings, and the runtime log lines are gone. A non-Number Weight still fails the Plan.
- **F5** fixed in part, deferred for the rest.
  - Fixed: a weighted Pick, `, WEIGHT <Expression>`, worked out per Match. It stands alone (`R2601`) and uses the same rules for wrong Weights. If every Match weighs 0, the condition has no Match (new `T2601`). A non-Number Weight leaves its Match out on a `GIVEN` and fails the Plan on a Body `IF`. New `R2605` for a Weight's Placeholders.
  - Deferred past 2.0: `WHILE` and counted loops. "Until the plate is empty" is a recipe that ends with `PURSUE g, WITHOUT WAITING.`
- **F10** (the short spellings) fixed in part, kept for the rest.
  - Fixed: an empty Option gets no `R0106`, so "only sometimes" is `EITHER, WEIGHT 3: …` followed by `OR, WEIGHT 7:` with an empty Block.
  - Kept: `CHANGE` repeating its Fact, since a shorter form would need new syntax to name a slot. `COUNT(…) = 0` next to `NOT`, since the shorter form already exists. A bare `HIGHEST` with ties left open gets no warning, since open ties can be meant.

Changed:

- Spec:
  - Chapter 01: empty Options are an exception to `R0106`.
  - Chapter 04: a roll's kind, rounding, reversed and empty bounds, new `T0403`, names made in every Option.
  - Chapter 09: empty Options, wrong Weights as Trace entries, names made in every Option outlive the choice, `R0904` narrowed; the ASL notes use `regia.random` and `regia.trace`.
  - Chapter 15: the draw of a counted pick is covered by the seed.
  - Chapter 16: per-Agent Expressions and rolls in a setup.
  - Chapter 21: a Propensity roll is always a decimal.
  - Chapter 26: *A weighted Pick*, when a Pick changes whether a condition holds, `R2601` and `R2603` widened, new `R2605` and `T2601`, the ASL notes for `WEIGHT` and the seeded draw, loops deferred, bare `HIGHEST` kept.
  - Chapter 34: what the seed covers.
  - Chapter 35: one seeded source, `regia.random` and `regia.weighted_pick`.
  - Chapter 36: Propensity draws are decimals.
- ADR: new ADR 0034 *A roll's kind is written*.
- Glossary: *Pick* and *Weight* revised; *Roll* and *Seed* added.

Handed on:

- Not this ticket's: choosing a run's seed is in [*The command line, Programs and Diagnostics*](16-command-line-and-diagnostics.md), and calling off an Action is in [*Time and Actions in the game*](19-time-and-actions.md).
- To the guide (fog on the map): *Randomness* shows `RANDOM(1, 3.0)`, the empty Option and the weighted Pick; *Matching* uses `IF NOT on_plate(?):` and the repeating recipe; *Placeholders and Expressions* drops the `#revise` on Options.
- To [*Words that do several jobs, and syntax nobody used*](20-words-and-syntax.md): `WEIGHT` now appears on Options and on Picks.

1.5, from [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md):

- B4, B6, D15, the weighted Pick (F5) and F10: in. A setup's roll per Agent is in for the starting cast. Rolling for a joiner comes with joining, which is later, and a 1.5 setup doesn't need it.
- Loops (F5): later, deferred past 2.0.
