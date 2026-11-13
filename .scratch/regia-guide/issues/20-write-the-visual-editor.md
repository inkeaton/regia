# Write: The Visual Editor

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Task

Write `docs/guide/17 - The Visual Editor.md`.

Covers: Projects, the split view, the Phase map and Nested Plans Graph views, Layers, editing from the graph and what it does to the text, Extents, the Docs tab.

Sources: 22, 24, 25; ADR 0011.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-13: [`docs/guide/17 - The Visual Editor.md`](../../../docs/guide/17%20-%20The%20Visual%20Editor.md), about 5,000 words counting snippets, tables, sketches and the three diagrams, over ten sections (a Project, the split view, the Phase map, Layers, the Nested Plans view, selecting and the Inspector, editing from the graph, drawing a transition, Extents, the Docs tab). Every drawing, Inspector panel and Docs page is put together by hand from chapters 22, 24 and 25, and the chapter says so. The showcase Program is unchanged. The package split, the Workspace calls, the Material 3 tokens and the road to a VS Code extension are left out as matters of building the editor. Not yet read by the user.

Nineteen `#revise`, among them:
- Eleven of the fourteen files have no drawing: the graph is of a Plot, and the eight Playbooks have none.
- The default Phase map leaves out everything in `DURING PLOT`, so the banquet shows one of its two ways into `farewell` and one of its two endings.
- `END SUBPLOT`, a Director's `LEARN`, and the Givings and Messages of `DURING PLOT` Plans are on no Layer.
- A new Event from the Trigger picker is declared by default in the Plot's file, where no Playbook can reach it to Signal it.
- The picker offers Events with no Sender and no quantity, so none of the banquet's three arrows could have been drawn.
- Deleting a Phase from the drawing deletes Plans the drawing didn't show.
- Undo is per file, so half of a rename can be taken back.
- The Docs tab is per Plot, and the Doc comments of Playbooks and Vocabulary items are shown nowhere.
- A `.regia` file reached by two `.regin` files is in two Programs, and nothing says which one its markers and its graph come from.

Nine entries were added to the README's *Spec wording* (one a contradiction: chapter 25 puts a new Event in a Plot's Local Vocabulary, which chapter 10 forbids) and one to *Gaps in the showcase*. *Subplots and Stagings* was corrected where it had the Phase map's "starts" edge leave a Plan: it leaves the Phase.
