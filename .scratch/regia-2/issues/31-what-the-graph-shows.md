# What the graph shows

Type: prototype
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 30

## Question

What does the graph view of a Plot (`graph(plot)`, spec 23) contain and how does it look, inside the `regia-graph` package and its host interface (spec 24)? Decide:
- Which elements are drawn (Phases, transitions and their Triggers, Roles, Subplots, Director Statements, …) and which are layers you can turn on and off, so the graph stays readable.
- How doc comments are shown, and whether they also become generated documentation.
- How the graph shows names a file uses through other files' imports (spec 10).
- Which graph edit operations exist, and where a new declaration lands, for example an Event that a new transition needs, possibly in another file (spec 22).
- The layout engine (dagre or elkjs), with the rule that the designer never arranges the graph by hand (primer ch.7).

## Comments

- Graduated from the map's fog when [Visual Editor architecture](30-visual-editor-architecture.md) resolved.
- A rough React Flow prototype over a hand-written graph view of `RoyalBanquet` (primer examples) is the cheapest way to react to the layers.
- Prototype: branch `prototype/graph-view`, file `.scratch/regia-2/prototypes/31-graph/graph-prototype.html` (throwaway, never merged). Three variants of RoyalBanquet: A Phase map (state machine with layers, dagre/elkjs toggle), B Cast board (Phases × who is affected, no graph engine), C Nested Plans (elkjs compound: Plot > Phase > Plan cards, Subplot expandable). Stub edit operations log `requestEdit` and the text edits the core would return.

## Answer

Spec: `docs/spec/25-graph-view.md`. Specs 22, 23 and 24 now point to it. Glossary: **Graph view**, **Layer**. No ADR: nothing here is hard to reverse.

- **Views:** the **Phase map** is the default. **Nested Plans** (a `DURING PLOT` frame, a box per Phase, a card per Plan, Subplots expandable in place, read-only) is the alternative, switched in the pane's toolbar. The Cast board variant (Phases × Roles) was dropped.
- **Layout:** elkjs, layered, top to bottom, orthogonal edges; compound layout for Nested Plans. No dagre. Nothing is placed by hand or stored.
- **Always drawn in the Phase map:** Phases and their names, the initial marker, transitions labelled with their Trigger as written (timeouts dotted, `after <Duration>`), `END PLOT` nodes per Outcome, and import marks. The node shows nothing else by default.
- **Layers, off by default and kept per user:** DURING PLOT ("any phase" node), Entry and exit, Givings, Messages, Subplots, Roles, Plain comments.
- **Doc comments:** never on the canvas. Shown in the Inspector, and in a **Docs** tab next to it that renders a page for the current Plot live. Writing doc files for a Project is post-2.0.
- **Imported names:** `↗` for a direct import, `↗↗` with a dashed amber underline for a name reached only through another file's import; the tooltip gives the import chain. Always drawn.
- **Edit operations:** `addPhase`, `rename`, `delete` (dangling `TRANSITION TO` left as errors), `setInitial`, `addTransition` (through a Trigger picker), `retargetTransition`, `removeTransition`, `changeTrigger`, `addPlan`, `deletePlan`. A transition onto a Trigger Block that already transitions or has `GIVEN`s is refused with a diagnostic.
- **New declarations:** a new Event lands in this file after the last `EVENT` by default; the picker also offers the Plot's Local Vocabulary or a file that already declares Events this file uses (adding the `IMPORT` if needed).
- **Canvas gestures (Phase map only):** drag from one Phase's handle to another to add a transition, drag an arrowhead to retarget, double-click empty canvas to add a Phase. Everything else goes through the Inspector.
- **Graph view data:** `graph(plot)` returns meaning, not a drawing: Phases, Roles, Plans with their effects, spans, keys, doc comments and name origins. `regia-graph` derives nodes, edges and layers, so toggling never calls the core.
