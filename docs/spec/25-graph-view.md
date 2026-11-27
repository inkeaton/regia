# The graph view

What the Visual Editor's graph shows for a Plot, how it is laid out, how doc comments and imported names appear, and which edits can be made from it. Decided in the ticket *What the graph shows* (`.scratch/regia-2/issues/31-what-the-graph-shows.md`), after a prototype over RoyalBanquet. It builds on chapter 22 (edit operations, structural keys), chapter 23 (`graph(plot)`) and chapter 24 (the `regia-graph` package and its host interface), and answers the primer's ch.7 `#discuss` points (what to draw without overwhelming the reader, toggling elements, showing doc comments). Revised in the ticket *The Visual Editor* (`.scratch/regia-revision/issues/18-visual-editor.md`): `DURING PLOT` drawn by default, every Statement drawn somewhere, a Docs page for every file, a Trigger picker built from the Interface, and a rename preview.

Only Plots are drawn. A Playbook or a Vocabulary file has no drawing; it has a Docs page (below). A Playbook drawing is post-2.0.

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
| Transitions | An edge per Plan of `DURING <phase>` that runs `ENTER`, labelled with the Trigger as written: `food_served`, `insult_thrown, FROM Guest ?who`, `HonorDuel FINISHED WITH apology`. A Plan under a `GIVEN` adds its Context to the label (`food_served · GIVEN hungry`). A Plan whose `IF` branches go to two different Phases gives one edge to each. |
| Timeouts | A `WHEN ENTERED` Plan that transitions is drawn dotted, labelled `after <Duration>` when a `WAIT` comes before the `ENTER` (chapter 20), otherwise `on entry`. |
| Endings | An `END PLOT` node per Outcome (`END PLOT · ruined`, plus a plain one for a bare `END PLOT`), with an edge from each Plan that ends the Plot. Endings are drawn because they are where a transition goes. |
| Import marks | On every name in a label (below). |

A Plot with no Phases (chapter 20) draws a single unnamed node for the whole Plot, with the start dot and its endings.

A Phase node shows nothing else unless a layer is on. Everything else about a Phase is in the Inspector.

### Layers

Layers are toggles in the pane's toolbar. **DURING PLOT is on by default**, so the default map shows every way the Plot can move, not only the evening on which nothing goes wrong; the other layers are off by default. The editor remembers them per user, not in the source.

The layers that write lines on Phase nodes (Entry and exit, Givings, Messages, Knowledge, Plain comments) write the lines of `DURING PLOT` Plans on the "any phase" node, so `ASSIGN Keeping_watch TO ?winner` in a `DURING PLOT` Plan has a place. With the DURING PLOT layer off, those lines aren't drawn.

| Layer | Adds |
| --- | --- |
| DURING PLOT (on by default) | An "any phase" node, with the edges of `DURING PLOT` Plans that transition or end the Plot (`assassin_spotted → END PLOT · ruined`). A Plan whose Context holds only in some Phases, by `IN p` (chapter 20), is drawn **from each such Phase** instead, dashed and marked as a `DURING PLOT` Plan, so the map shows where the Plot can really be when the edge is taken: `GIVEN IN feast` draws from `feast`, `GIVEN IN feast OR IN reception` from both. `NOT IN p` leaves the edge on "any phase", with the Context in its label (`poison_taken · GIVEN NOT IN farewell`). |
| Entry and exit | On each Phase node, the Custom Actions and `WAIT` of its `WHEN ENTERED` and `WHEN EXITED` Plans. Lines from a `WHEN EXITED, BY PARENT` Plan are marked as coming from the parent (`↑`). |
| Givings | On each Phase node, `ASSIGN` (`+`) and `REMOVE` (`−`) lines from its Plans. |
| Messages | On each Phase node, `TELL`, `ASK` and `SIGNAL` lines from its Plans. On an edge, the Message lines of its Plan, when another edge has the same endpoints and Trigger: two Plans that differ by an `ASK` are two edges, each showing its `ASK`. |
| Knowledge | On each Phase node, the Director's `LEARN`, `FORGET` and `UPDATE` lines from its Plans. |
| Subplots | A dashed node per Subplot the Plot starts, with a dashed "starts" edge from the Phase that starts it, and an "ends" mark on the Phase whose Plan runs `DROP SUBPLOT` for it. |
| Roles | A box listing the Plot's Roles and their Role setups. |
| Plain comments | The plain comments that belong to a Plan's Extent (chapter 22), on its Phase node. |

### Things the Phase map doesn't draw

Plans that neither transition nor end the Plot appear only through the layers above and in the Inspector. Every Statement a Director can run is drawn by some layer. Doc comments are never drawn on the canvas (below).

## The Nested Plans view

- A dashed `DURING PLOT` frame holds the `DURING PLOT` Plans and a box per Phase. The initial Phase is marked `INITIAL`. A Plot with no Phases (chapter 20) draws only the frame.
- Each Plan is a card: its Trigger, then a short summary of **every Statement** of its Body (Custom Actions, `WAIT`, Givings, Messages, `LEARN`/`FORGET`/`UPDATE`, `SHIFT`, `START SUBPLOT`, `DROP SUBPLOT`, and `IF`/`PICK` shown as their branches). No card is empty. `ENTER` and `END PLOT` are the card's outgoing edges, not lines on it.
- Edges go from a Plan card to the target Phase's box or an `END PLOT` node. Timeouts are dotted, as in the Phase map.
- A Subplot is a collapsed node with a "starts" edge from the Plan that starts it. **Expanding it** draws the Subplot's own Phase map inside it, from that Plot's graph view (another `graph(plot)` call, whatever file the Plot is in). Expanding is read-only; editing a Subplot means opening its own tab.
- Layers: **Plans without a way out** (cards for Plans that neither transition nor end, on by default), **Roles** (the Plot's Roles and their Role setups, as in the Phase map, and a Phase's Role setups in its box) and **Plain comments**. Import marks are always drawn.

## Selection, the Inspector and the Docs tab

- Clicking a node, a Plan card or an edge label **selects** it and calls `reveal(span)` (chapter 24). Moving the text cursor into a construct selects it on the graph. Clicking empty canvas clears the selection.
- The graph pane has a side panel with two tabs:
  - **Inspector**: the selection's kind, structural key and file position; its doc comments; its Body or Plans; a **Names used** table giving each name's kind, its `#@desc`, and where it comes from; and buttons for the edit operations that apply to it. With nothing selected it shows the Plot itself (doc comments, `PRECEDENCE`, a "+ Phase" button). A selected `ASSIGN` or `START SUBPLOT` also shows the Interface check between the two sides (chapter 38), with any `R38_01-unheard-signal`, `R38_02-cue-never-signalled`, `R38_03-unheard-message` or `R17_08-unheard-subplot-ending` in place.
  - **Docs**: a read-only documentation page, generated live from doc comments, the graph view and the Interfaces (chapter 38). It exists for **every `.regia` file**, Plot or not, and for a file with no Plot the pane shows only this tab.

### The Docs page

| For | The page holds |
| --- | --- |
| A Plot | Its `desc` and `version`; its Roles with their descriptions and Role setups; its Phases with their descriptions, Role setups, transitions and endings; its `DURING PLOT` Plans as a section of their own; and its **Interface**: the Signals it hears and from which Role, the endings it sends upward, and the Goals it asks. |
| A Playbook | Its `desc`; its Local Vocabulary; its Goals with their recipes; its Plans grouped by Trigger; and its **Interface**: the Signals it sends and to whom, the Cues it can be told, the Goals it can be asked, and the Roles it is given to in the Program. |
| A file's top-level Vocabulary | Each declaration with its kind, parameters and description. |

A file holding several of these shows each in turn. What depends on the whole Program (Interfaces, the Roles a Playbook is given to) is taken from the Active Entry (chapter 24).

### Doc comments

- Doc comments (chapter 02) are **never drawn on the canvas**. They appear in the Inspector for the selected declaration and in the Docs tab.
- Writing documentation files for a whole Project (a "Generate docs" command) is not part of 2.0.

## Names from other files

Every name in a label, a node line or the Inspector carries its origin. Names declared in this file look plain.

| Origin | Mark | Example |
| --- | --- | --- |
| Declared in the file being shown | none | `assassin_spotted` |
| A file this file imports directly | dotted underline, no mark (hovering names the file) | `HonorDuel` from `duel.regia` |
| Reached only through another file's import (chapter 10, transitive) | `↗↗` after the name, dashed amber underline | `food_served`, declared in `shared/cues.regia`, reached through `shared/social` |

- Hovering a marked name shows its kind, the declaring file and the chain of imports that reaches it. A transitive name's tooltip says it breaks if that import goes away, since that error would show up in a file nobody edited (chapter 10).
- Import marks are always drawn. They don't change the layout.

## Edit operations

Every edit is a domain operation sent with `requestEdit` and addressed by structural key (chapters 22, 24). The core returns text edits, possibly across files, applied as one undo step, across files too (chapter 24). The graph never edits text itself, and it never redraws from its own guess: it waits for the reparse.

| Operation | From | Text edit |
| --- | --- | --- |
| `addPhase(plot, name)` | "+ Phase", or double-click on empty canvas | A `PHASE name` line after the last `PHASE`. The Phase has no `DURING` Block yet and is drawn with no incoming edge until a transition reaches it. |
| `rename(key, name)` | Inspector | Every reference in every file (a Model-level rename), and what the preview below keeps ticked. |
| `delete(key)` | Inspector | The construct's Extent. Deleting a Phase deletes its `PHASE` line and its `DURING` Block. References to it elsewhere are **left in place** and become errors for the user to fix. A Phase is deleted only after a confirmation (below). |
| `setInitial(phase)` | Inspector | Moves `INITIAL` from the old initial Phase to this one. |
| `addTransition(from, to, trigger)` | Drag between Phases, or "+ Transition" then a click on the target | See below. |
| `retargetTransition(plan, to)` | Drag an edge's arrowhead onto another Phase, or Inspector | Rewrites that Plan's `ENTER`. |
| `removeTransition(plan)` | Inspector | Deletes the `ENTER` line, or the whole Plan if that line was its whole Body. |
| `changeTrigger(plan, trigger)` | Inspector | Rewrites the Plan's `WHEN` line. |
| `addPlan(phase, trigger)` | Inspector | A new Plan at the end of the Phase's `DURING` Block, creating the Block if needed. |
| `deletePlan(plan)` | Inspector | The Plan's Extent. |

Opening a Subplot's own graph ("Open HonorDuel") is a host navigation request, not an edit.

No 2.0 operation moves an Extent. The Extent rules (chapter 22) serve `delete` now and a move operation later; a Plan is moved to another Phase in the text.

### Deleting a Phase

Before `delete` removes a Phase, the editor shows what goes and what breaks, from the core:

- the Plans that are removed, saying how many of them the current drawing doesn't show;
- every reference left behind: `ENTER` the Phase, `IN p` in a Context, a Giving or a Subplot tied to it with `UNTIL EXITED` (chapters 16, 17), and Plans elsewhere that take back what only this Phase gave (`farewell` taking away a Playbook nobody is given any more).

The designer confirms or cancels. Nothing outside the Phase's own lines is rewritten.

### The rename preview

`rename` shows a preview before it applies. It lists:

1. every reference it rewrites, by file;
2. **doc comments** in the Program that hold the exact old name as a whole word, rewritten too, each one can be unticked;
3. **the file**, when the construct is a Playbook or Plot and the file is named after it (`HonorDuel` in `honor_duel.regia`): renamed through `moveFile` (chapter 24), which can be unticked;
4. **competitions that flip**: every pair of Plans decided only by name order (chapter 13) whose winner the new name changes, as "`WHEN insult_heard` in `Duelling` will now beat the one in `Courtesy`".

Plain comments are never rewritten. The designer confirms or cancels. The whole rename is one undo step (chapter 24).

### Adding a transition

1. The designer drags from a Phase's handle and drops on another Phase (or on the same one, to re-enter it, chapter 20). Dropping anywhere else cancels.
2. A **Trigger picker** opens. It is built from the Interface (chapter 38) and the Vocabulary, and offers only what can reach this Plot:
   - Signals that a Playbook this Plot gives can send, each with its possible senders (`FROM Host`, `FROM Guest ?who`) and "anyone";
   - `GAME CUE`s (chapter 10), with `FROM GAME` and "anyone";
   - `WHEN ENTERED` with a `WAIT` (a timeout);
   - the endings of the Subplots this Plot starts (`WHEN HonorDuel ENDED`);
   - cast changes (`WHEN Guest LEFT`, …);
   - **a new Cue**, by name (below).

   A Cue nobody sends is not offered: no arrow is drawn on what can't happen. Each name carries its import mark and file. For a Signal a Quota can count, the picker has a **quantity** field (`ALL`, `n OF`, `n% OF`, chapter 18). Senders may be combined with `OR` (chapter 07).
3. The core adds `WHEN <trigger>:` with `ENTER <to>` at the end of the source Phase's `DURING` Block, creating the Block if there is none. The Trigger is written whole, with its Sender and quantity.
   - If the Phase already has a Trigger Block for that Trigger holding a single Plan that neither transitions nor ends the Plot, the `ENTER` is appended to that Plan's Body instead.
   - If that Trigger Block already transitions or ends, or holds `GIVEN` Blocks (chapter 06), the core returns a diagnostic instead of edits, and the designer edits that Plan in the text.

### Where a new declaration lands

A new Cue made from the Trigger picker is a Signal, so the Plot and the Playbook that sends it must both see it. A Plot's file can't be reached from its Playbooks' files (that would be an import cycle, chapter 10), and a Plot holds no `CUE` (chapter 10). So:

1. The picker asks **which Playbook sends it**, among those this Plot gives.
2. It offers the files that **both** this Plot's file and that Playbook's file reach, and that already declare Cues (for the banquet, `vocabulary.regia`). If several qualify, it lists them. If none does, it says so and offers a file the Playbook reaches, adding the `IMPORT` to the Plot's file.
3. In the chosen file it lists the **comment sections**: a run of comment lines that belongs to no construct (chapter 22) followed by declarations. The line goes at the end of the chosen section. The default is the section holding the most Cues this Plot already uses; a file with no section gets the line after its last `CUE`, or after its imports.

The new Cue is declared and the transition drawn; the `SIGNAL` that sends it is written by hand in the Playbook. Until then the Plan carries the Interface warning `R38_02-cue-never-signalled` (chapter 38).

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
- Its Plans, in `DURING PLOT` and in each Phase: key, span, Trigger (text and kind), the plain comments of its Extent, and its Body summarised as effects: `ENTER` targets, `END PLOT` Outcome, a `WAIT` before a transition, Givings, Messages, `LEARN`/`FORGET`/`UPDATE`, `SHIFT`, Custom Actions, `START SUBPLOT` with its Mappings, `DROP SUBPLOT`.
- Its Interface (chapter 38), and for the Docs page of a file with no Plot, the same for its Playbooks and Vocabulary (`docs(path)`, chapter 23).
- **Name origins**: for every name the view mentions, its kind, the file that declares it, and the import chain that reaches it from the shown file.

Spans are LSP ranges and keys are structural keys, as everywhere at the WASM boundary (chapters 22, 23). A Model built from broken code still produces a view (chapter 23). A transition to a Phase that doesn't exist is drawn to a placeholder node marked as an error.

## Handed off

- Writing documentation files for a Project (a "Generate docs" command): post-2.0.
- A drawing of a Playbook: post-2.0. In 2.0 a Playbook has a Docs page.
- An operation that moves an Extent (dragging a Plan card to another Phase box): post-2.0.
- A form editor for Instancing: post-2.0 (chapter 24).
- Edit operations beyond this list (Givings, Messages and Plan Bodies from the graph) are added during development as they are needed. Each is a core operation tested as *source before, operation, expected source after* (chapter 22).

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025), except what follows systems that 1.5 leaves out: the picker's quantity field (Quota Triggers), and its `FROM GAME` and `OR` sender choices. The 1.5 picker is the 2.0 picker with fewer choices, so nothing is rewritten later.
