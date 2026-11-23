# Write guide chapter 16, Precedence and Labels

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 05

## Question

Write `docs/guide/16-precedence-and-labels.md`, *Precedence and Labels*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 13, 14.
- **Covers:** one Plan per Trigger, falling through, order inside a Playbook, `PRECEDENCE`, a Plot and its Subplots, a Director's own Plans, Labels, Propensities, Suits, `SHIFT`, reading the order.
- **Quotes most:** `scheming.regia`, `duelling.regia`, `royal_banquet.regia`.
- **"In 2.0" notes:** none expected.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-20 (task). [`docs/guide/16-precedence-and-labels.md`](../../../docs/guide/16-precedence-and-labels.md), about 620 lines, written from the template:

- An opening table of what each construct decides and where it is written.
- Sections, simple to full: One Plan per Trigger (the knight's three `scandal` Plans, candidates, the three-step rank, a mermaid flowchart of the knight's fall-through); Inside a Playbook (`scandal(ME)` before `scandal(?victim)`, `Dining`'s two `FAILED` Plans, the swap as a throwaway for `R1307`); `PRECEDENCE` (the banquet's Block, what `A`/`B` name, a table of `ON` forms with banquet items in place of the showcase gap), with *Name order*; A Plot and its Subplots (`Scheming` falling through, `PARENT OVER SELF ON scandal`, who names what, a default giving way on `scandal`, the `idle`/`scandal` order table); A Director's own Plans (throwaway `culprit_seized` in `feast`, `DURING PLOT OVER DURING feast`); Propensities; Labels; Suits alternatives (insult and challenge); Shifts (`SHIFTS` and `SHIFT`); Tied Playbooks (`Dining TIES NobleSocializing ON insulted`); Reading the order (defaults table, a conflict-report excerpt in the spec's sample layout, the Trace's `plan`/`mood` entries).
- No "In 2.0" notes, as expected.
- Every showcase snippet checked against its file by script (19 linked snippets). Codes appear in *Checks* only.
- `Guide: Precedence and Labels` added under *13 Plan selection* and *14 Labels* in the showcase README.
- Grep for retired spellings: only `AND` between Propensities, on purpose, in the `R1412` check. The humanizer pass removed bold on bullet leads (the template forbids it) and one not-X-but-Y line.

Two non-blocking findings: `R1307` against the *Defaults* wording for a Phase that catches a `DURING PLOT` Trigger; the conflict report's full stops for Blocks with a Value or narrower `FROM`, and what "per Role" means for a Subplot's Roles.

