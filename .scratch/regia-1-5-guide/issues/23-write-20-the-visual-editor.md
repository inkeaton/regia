# Write guide chapter 20, The Visual Editor

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05

## Question

Write `docs/guide/20-the-visual-editor.md`, *The Visual Editor*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 24, 25, 22.
- **Covers:** platform, projects, layout, highlighting, quick fixes, the Phase map, the Nested Plans view, the Inspector and the Docs tab, editing from the graph, extents, the text as the source of truth.
- **Quotes most:** `royal_banquet.regia` (the Phase map), `courtesy.regia`.
- **"In 2.0" notes:** none expected.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Written: [`docs/guide/20-the-visual-editor.md`](../../../docs/guide/20-the-visual-editor.md).

- Sections: a Project; the window (Active Entry, undo); highlighting and quick fixes; building; the Phase map with timeouts; layers (with `DURING PLOT` in some Phases, and what the map leaves out); the Nested Plans view (`HonorDuel`); names from other files; the Inspector (with the Interface check); the Docs page (`Courtesy`); editing from the graph (the text as source of truth, operations, what an edit writes, broken text); adding a transition (a new Cue landing in `vocabulary.regia`'s Signals section); renaming (`HonorDuel` → `Duel`, a throwaway name-order flip); deleting and Extents (deleting `reception`); how it is built (packages, host interface, graph view, Material 3, VS Code).
- One "In 2.0" note, against the ticket's "none expected": the picker's `FROM GAME`, `OR` and quantity field.
- Throwaways: `short_evening.regin` (a second Entry), the transitive `↗↗` mark, the Extent rules' `Guest` Playbook (spec 22), the banquet after a drop.
- No `Guide:` line: the showcase README has no *Coverage* heading for chapters 22, 24 or 25.
- Snippets checked verbatim against the showcase; no retired spellings; humanizer pass done.
- Eleven non-blocking findings. The largest: chapter 25 predates `AFTER`; the guide draws `AFTER` Plans as dotted edges labelled with their Trigger.
