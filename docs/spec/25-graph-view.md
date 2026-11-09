# The graph view

What the Visual Editor's graph shows for a Plot, how it is laid out, how doc comments and imported names appear, and which edits can be made from it. Decided in the ticket *What the graph shows* (`.scratch/regia-2/issues/31-what-the-graph-shows.md`), after a prototype over RoyalBanquet. It builds on chapter 22 (edit operations, structural keys), chapter 23 (`graph(plot)`) and chapter 24 (the `regia-graph` package and its host interface), and answers the primer's ch.7 `#discuss` points (what to draw without overwhelming the reader, toggling elements, showing doc comments).

## Two views

The graph pane shows one Plot at a time (one tab per Plot, chapter 24) in one of two views. A switch in the pane's toolbar changes between them.

| View | What it is | Default |
| --- | --- | --- |
| **Phase map** | A state machine: Phases are nodes, transitions are edges labelled with their Trigger. | yes |
| **Nested Plans** | Boxes inside boxes: a `DURING PLOT` frame holds a box per Phase, and each Phase box holds a card per Plan. Transitions start from the Plan that makes them. | no |

Both views are drawn from the same graph view data (below). Neither stores anything in the source. Their colours, type and shapes come from the editor's Material 3 tokens (chapter 24), in light and dark.

## Layout

- **elkjs**, the layered algorithm, **top to bottom**, with orthogonal edge routing. The Nested Plans view uses elkjs's compound layout (boxes inside boxes). dagre is not used: it can't nest boxes, and one engine is simpler.
- **The designer never arranges the graph** (primer ch.7). There are no node positions to drag, store or keep in sync. Every change redraws the layout from scratch (chapter 22: nothing is stored between parses).
- Pan and zoom are view state only. After a redraw the view stays where it was; switching Plot or view fits the graph to the pane.

## The Phase map

### Always drawn

| Element | How |
| --- | --- |
| Phases | A node with the Phase's name. |
| The initial Phase | A start dot with an arrow into it. |
| Transitions | An edge per Plan of `DURING <phase>` that runs `TRANSITION TO`, labelled with the Trigger as written: `food_served`, `insult_thrown FROM Guest ?who`, `HonorDuel ENDED WITH apology`. A Plan under a `GIVEN` adds its Context to the label (`food_served · GIVEN hungry`). A Plan whose `IF` branches go to two different Phases gives one edge to each. |
| Timeouts | A `WHEN ENTERED` Plan that transitions is drawn dotted, labelled `after <Duration>` when a `WAIT` comes before the `TRANSITION` (chapter 20), otherwise `on entry`. |
| Endings | An `END PLOT` node per Outcome (`END PLOT · ruined`, plus a plain one for a bare `END PLOT`), with an edge from each Plan that ends the Plot. Endings are drawn because they are where a transition goes. |
| Import marks | On every name in a label (below). |

A Phase node shows nothing else unless a layer is on. Everything else about a Phase is in the Inspector.

### Layers

Layers are toggles in the pane's toolbar. They are **off by default**, and the editor remembers them per user, not in the source.

| Layer | Adds |
| --- | --- |
| DURING PLOT | An "any phase" node, with the edges of `DURING PLOT` Plans that transition or end the Plot (`assassin_spotted → END PLOT · ruined`). |
| Entry and exit | On each Phase node, the Custom Actions and `WAIT` of its `WHEN ENTERED` and `WHEN EXITED` Plans. |
| Givings | On each Phase node, `ASSIGN` (`+`) and `UNASSIGN` (`−`) lines from its Plans. |
| Messages | On each Phase node, `TELL` and `ASK` lines from its Plans. |
| Subplots | A dashed node per Subplot the Plot starts, with a dashed "starts" edge from the Phase that starts it. |
| Roles | A box listing the Plot's Roles and their Role setups. |
| Plain comments | The plain comments that belong to a Plan's Extent (chapter 22), on its Phase node. |

### Things the Phase map doesn't draw

Plans that neither transition nor end the Plot appear only through the layers above and in the Inspector. Doc comments are never drawn on the canvas (below).

## The Nested Plans view

- A dashed `DURING PLOT` frame holds the `DURING PLOT` Plans and a box per Phase. The initial Phase is marked `INITIAL`.
- Each Plan is a card: its Trigger, then a short summary of its Body (Custom Actions, Givings, Messages, `START SUBPLOT`). `TRANSITION` and `END PLOT` are the card's outgoing edges, not lines on it.
- Edges go from a Plan card to the target Phase's box or an `END PLOT` node. Timeouts are dotted, as in the Phase map.
- A Subplot is a collapsed node with a "starts" edge from the Plan that starts it. **Expanding it** draws the Subplot's own Phase map inside it, from that Plot's graph view (another `graph(plot)` call, whatever file the Plot is in). Expanding is read-only; editing a Subplot means opening its own tab.
- Layers: **Plans without a way out** (cards for Plans that neither transition nor end, on by default) and **Plain comments**. Import marks are always drawn.

## Selection, the Inspector and the Docs tab

- Clicking a node, a Plan card or an edge label **selects** it and calls `reveal(span)` (chapter 24). Moving the text cursor into a construct selects it on the graph. Clicking empty canvas clears the selection.
- The graph pane has a side panel with two tabs:
  - **Inspector**: the selection's kind, structural key and file position; its doc comments; its Body or Plans; a **Names used** table giving each name's kind and where it comes from; and buttons for the edit operations that apply to it. With nothing selected it shows the Plot itself (doc comments, `PRECEDENCE`, a "+ Phase" button).
  - **Docs**: a documentation page for the current Plot, generated live from its doc comments and its graph view: the Plot's `desc` and `version`, its Roles with their descriptions and Role setups, and its Phases with their descriptions, transitions and endings. It is read-only.

### Doc comments

- Doc comments (chapter 02) are **never drawn on the canvas**. They appear in the Inspector for the selected declaration and in the Docs tab.
- Writing documentation files for a whole Project (a "Generate docs" command) is not part of 2.0.

## Names from other files

Every name in a label, a node line or the Inspector carries its origin. Names declared in this file look plain.

| Origin | Mark | Example |
| --- | --- | --- |
| Declared in the file being shown | none | `assassin_spotted` |
| A file this file imports directly | `↗` after the name, dotted underline | `HonorDuel` from `duel.regia` |
| Reached only through another file's import (chapter 10, transitive) | `↗↗` after the name, dashed amber underline | `food_served`, declared in `shared/events.regia`, reached through `shared/social` |

- Hovering a marked name shows its kind, the declaring file and the chain of imports that reaches it. A transitive name's tooltip says it breaks if that import goes away, since that error would show up in a file nobody edited (chapter 10).
- Import marks are always drawn. They don't change the layout.

## Edit operations

Every edit is a domain operation sent with `requestEdit` and addressed by structural key (chapters 22, 24). The core returns text edits, possibly across files, applied as one undo step ("Undo all" when several files change, chapter 24). The graph never edits text itself, and it never redraws from its own guess: it waits for the reparse.

| Operation | From | Text edit |
| --- | --- | --- |
| `addPhase(plot, name)` | "+ Phase", or double-click on empty canvas | A `PHASE name.` line after the last `PHASE`. The Phase has no `DURING` Block yet and is drawn with no incoming edge until a transition reaches it. |
| `rename(key, name)` | Inspector | Every reference in every file (a Model-level rename). |
| `delete(key)` | Inspector | The construct's Extent. Deleting a Phase deletes its `PHASE` line and its `DURING` Block. `TRANSITION TO` lines pointing at it are **left in place** and become "unknown Phase" errors for the user to fix. |
| `setInitial(phase)` | Inspector | Moves `INITIAL` from the old initial Phase to this one. |
| `addTransition(from, to, trigger)` | Drag between Phases, or "+ Transition" then a click on the target | See below. |
| `retargetTransition(plan, to)` | Drag an edge's arrowhead onto another Phase, or Inspector | Rewrites that Plan's `TRANSITION TO`. |
| `removeTransition(plan)` | Inspector | Deletes the `TRANSITION` line, or the whole Plan if that line was its whole Body. |
| `changeTrigger(plan, trigger)` | Inspector | Rewrites the Plan's `WHEN` line. |
| `addPlan(phase, trigger)` | Inspector | A new Plan at the end of the Phase's `DURING` Block, creating the Block if needed. |
| `deletePlan(plan)` | Inspector | The Plan's Extent. |

Opening a Subplot's own graph ("Open HonorDuel") is a host navigation request, not an edit.

### Adding a transition

1. The designer drags from a Phase's handle and drops on another Phase (or on the same one, to re-enter it, chapter 20). Dropping anywhere else cancels.
2. A **Trigger picker** opens, listing:
   - Events declared in this file;
   - Events reached through imports, each with its import mark and file;
   - `WHEN ENTERED` with a `WAIT` (a timeout);
   - the endings of the Subplots this Plot starts (`WHEN HonorDuel ENDED`);
   - cast changes (`WHEN Guest LEFT`, …);
   - **a new Event**, by name.
3. The core adds `WHEN <trigger>:` with `TRANSITION TO <to>` at the end of the source Phase's `DURING` Block, creating the Block if there is none.
   - If the Phase already has a Trigger Block for that Trigger holding a single Plan that neither transitions nor ends the Plot, the `TRANSITION` is appended to that Plan's Body instead.
   - If that Trigger Block already transitions or ends, or holds `GIVEN` Blocks (chapter 06), the core returns a diagnostic instead of edits, and the designer edits that Plan in the text.

### Where a new declaration lands

A new Event made from the Trigger picker is declared in one of three places. The picker offers all three:

1. **This file** (the default): after the last `EVENT` declaration, or after the imports if there is none.
2. **The Plot's Local Vocabulary** (chapter 10): at the top of the Plot. Only this Plot can use it.
3. **Another file** that already declares Events this file uses (for RoyalBanquet, `shared/events.regia`). If the current file doesn't reach that file yet, the same operation also adds the `IMPORT`.

The same rule serves any later operation that needs a new declaration.

### Canvas gestures

| Gesture | Operation |
| --- | --- |
| Drag from one Phase's handle to another Phase | `addTransition`, through the Trigger picker |
| Drag an edge's arrowhead onto another Phase | `retargetTransition` |
| Double-click empty canvas | `addPhase`, asking for the name in place |

All other edits go through the Inspector's buttons. Gestures work only in the Phase map. A construct whose Extent contains a syntax error is drawn but can't be edited until the text is fixed (chapter 22).

## The graph view data

`graph(plot)` (chapter 23) returns the Plot's **meaning**, not a drawing. `regia-graph` turns it into nodes and edges, so switching a view or a layer never calls the core.

- The Plot: name, key, span, doc comments, `PRECEDENCE` relations.
- Its Roles: name, key, span, doc comments, Role setup Statements.
- Its Phases: name, key, `INITIAL`, doc comments, the spans of the `PHASE` line and of the `DURING` Block.
- Its Plans, in `DURING PLOT` and in each Phase: key, span, Trigger (text and kind), the plain comments of its Extent, and its Body summarised as effects: `TRANSITION` targets, `END PLOT` Outcome, a `WAIT` before a transition, Givings, Messages, Custom Actions, `START SUBPLOT` with its Mappings.
- **Name origins**: for every name the view mentions, its kind, the file that declares it, and the import chain that reaches it from the shown file.

Spans are LSP ranges and keys are structural keys, as everywhere at the WASM boundary (chapters 22, 23). A Model built from broken code still produces a view (chapter 23). A transition to a Phase that doesn't exist is drawn to a placeholder node marked as an error.

## Handed off

- Writing documentation files for a Project (a "Generate docs" command): post-2.0.
- A form editor for Instancing: post-2.0 (chapter 24).
- Edit operations beyond this list (Givings, Messages and Plan Bodies from the graph) are added during development as they are needed. Each is a core operation tested as *source before, operation, expected source after* (chapter 22).
