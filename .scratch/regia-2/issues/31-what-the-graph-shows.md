# What the graph shows

Type: prototype
Status: open
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
