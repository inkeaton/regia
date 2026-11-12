# Write: Plans

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Task

Write `docs/guide/4 - Plans.md`.

Covers: Trigger and Trigger kinds, several Plans under one Trigger, `GIVEN` (Context) versus `IF` (control flow), the Body, Basic Actions, Custom Actions with `DO` and `WITHOUT WAITING`, `WAIT`.

Sources: 05, 06, 08, 12; ADR 0003, 0004.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-12: [`docs/guide/4 - Plans.md`](../../../docs/guide/4%20-%20Plans.md), about 3,200 words counting snippets, tables and the diagram, over eight sections (a Trigger and a Body, Trigger kinds, the Context, several Plans under one Trigger, `IF`, Basic Actions, Custom Actions, `WAIT`). The longest chapter so far: it carries the Trigger kinds, the conditions and the Basic Action set that later chapters only point back to. Not yet read by the user.

- **Showcase**: the Program is unchanged. Two lines were added to the README's *Gaps in the showcase*: no `OR`, parentheses, `PURSUING` or `ELSE IF` anywhere; and the `IF hungry` case in `Dining` is undercut by the Playbook's own `WHEN hungry FORGOTTEN: DROP have_dinner.`
- **Throwaway snippets**: an `IF`/`ELSE IF`/`ELSE` chain, a `PRINT`, and `Wagering`'s `duel_on` rewritten with an `IF`.
- **`#revise`** (nine):
  - ten kind words across Playbooks and Plots, and the Goal recipe alone written `TO` with none;
  - a missing `ELSE` means "the Goal fails" or "falls through" depending on the Trigger kind, and the showcase comments it by hand all four times;
  - with prefix Statements gone, `Wagering` and `HonorDuel` repeat the closing lines of sibling Plans;
  - a `GIVEN`/`ELSE` chain and an `IF`/`ELSE` chain as the whole Body do the same, and nothing says which to write;
  - `IF hungry`'s `ELSE` races the `DROP` from `WHEN hungry FORGOTTEN`, and the order of turns isn't visible in the source;
  - every `CHANGE` follows a condition matching the same Fact, so the Fact is written three times;
  - after `, WITHOUT WAITING` the Agent can never learn how the Action ended;
  - `WAIT` can wait only for the clock;
  - "which Plan runs for this Trigger" has two shapes with two rules: `GIVEN` siblings and Suits alternatives.
- **Checked against** spec chapters 05, 06, 08, 11, 12, 13 and 20, and ADRs 0003 and 0004. Two things could not be confirmed from the spec or the primer and are worded loosely in *Since 1.0*: that 1.0 Triggers had no kinds, and whether 1.0's `DO` waited.
