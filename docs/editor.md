# RegiaScript Editor — Structure Summary

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Framework | React + TypeScript + Vite | Component framework, type safety, fast dev/build |
| Canvas | React Flow (`@xyflow/react`) | Node/edge graph rendering, pan/zoom, minimap, connections |
| Auto-layout | Dagre | Hierarchical top-down graph positioning |
| State | Zustand | Global store for project data and UI selection state |
| Styling | Tailwind CSS | Utility-first styling, no separate stylesheets |
| Animation | Framer Motion | Node/panel transitions, toast animations, highlights |
| Image export | html-to-image | PNG/SVG snapshot of the canvas |
| IDs | nanoid | Unique IDs for all entities (stories, phases, agents, plans, transitions) |
| RGS import | Hand-written tokenizer + recursive descent parser | Zero-dependency `.rgs` → project conversion |

No backend — everything runs client-side in the browser. Desktop wrapping (Tauri) is deferred.

---

## Directory Structure

```
regiascript-editor/
├── src/
│   ├── types/
│   │   └── story.ts                 ← Core data model (mirrors the grammar)
│   │
│   ├── store/
│   │   ├── useStore.ts              ← Main Zustand store (project + CRUD)
│   │   ├── useToastStore.ts         ← Toast notification store
│   │   └── history.ts               ← Undo/redo snapshot manager
│   │
│   ├── layout/
│   │   ├── autoLayout.ts            ← Dagre wrapper
│   │   └── storyToGraph.ts          ← Story → React Flow nodes/edges
│   │
│   ├── components/
│   │   ├── canvas/
│   │   │   ├── StoryCanvas.tsx      ← React Flow wrapper, connections, fitView
│   │   │   └── PhaseNode.tsx        ← Custom node component (phase box)
│   │   │
│   │   ├── panels/
│   │   │   ├── Sidebar.tsx          ← Story list, add story/default
│   │   │   ├── PropertiesPanel.tsx  ← Right panel — story vs phase switch
│   │   │   ├── StoryProperties.tsx  ← Story name/priority/doc + declarations
│   │   │   ├── PhaseProperties.tsx  ← Phase settings, transitions, agents
│   │   │   ├── DeclarationList.tsx  ← Generic actions/events/conditions editor
│   │   │   ├── AgentEditor.tsx      ← Collapsible agent block, plan list
│   │   │   ├── PlanEditor.tsx       ← WHEN/IF/DO editor for one plan
│   │   │   ├── TransitionEditor.tsx ← TRANSITION TO/WHEN/IF editor
│   │   │   ├── ExportMenu.tsx       ← Export/import dropdown menu
│   │   │   └── HistoryControls.tsx  ← Undo/redo buttons
│   │   │
│   │   └── ui/
│   │       └── ToastContainer.tsx   ← Toast notification display
│   │
│   ├── export/
│   │   ├── toRegiaScript.ts         ← Project → .rgs text emitter
│   │   ├── projectIO.ts             ← JSON export/import, file download
│   │   └── toImage.ts               ← PNG/SVG canvas export
│   │
│   ├── import/
│   │   ├── tokenizer.ts             ← .rgs → token stream
│   │   ├── fromRegiaScript.ts       ← Token stream → Project (recursive descent)
│   │   └── errors.ts                ← ImportError with line/column
│   │
│   ├── hooks/
│   │   └── useKeyboardShortcuts.ts  ← Ctrl+Z/Y, Delete, Escape
│   │
│   ├── App.tsx                      ← Root layout, wires everything together
│   ├── main.tsx                     ← React entry point
│   └── index.css                    ← Tailwind + React Flow imports
│
├── vite.config.ts                   ← Vite + Tailwind plugin config
├── package.json
└── tsconfig.json
```

---

## What Each File Does

### Type System

**`types/story.ts`** — The single source of truth for the data model. Defines `RegiaProject` (top-level: version + stories), `Story` (name, priority, declarations, phases), `Phase` (name, isInitial/isAlways flags, agents, transitions), `AgentInPhase` (local declarations + plans), `Plan` (WHEN block: event, origin, condition, DO sequence), `TransitionRule` (TO/WHEN/IF), `CondExpr`/`CondAnd`/`CondAtom` (DNF condition representation), and `Origin` (the five origin tags). Every other file imports from here. This mirrors `src/symbol_table.py` and the grammar's structure on the Python side — **if the grammar changes, this file changes first**.

---

### State Management

**`store/useStore.ts`** — The central Zustand store holding `project: RegiaProject` plus UI selection state (`activeStoryId`, `activePhaseId`, `activeTransitionId`). Contains all CRUD operations: stories, phases, story-level declarations (actions/events/conditions), agents-in-phase, plans, transitions. Two helper functions `mapStory`/`mapPhase` provide immutable nested updates. `setProject` accepts a `resetSelection` flag so undo/redo can restore state without clearing the UI selection.

**`store/history.ts`** — Standalone undo/redo manager (not a Zustand store itself — uses plain module-level arrays + a subscriber pattern). Subscribes to `useStore` changes, debounces rapid edits (500ms) into single undo steps, maintains `past`/`future` stacks (max 50). Exposes `undo()`, `redo()`, `canUndo()`, `canRedo()`, `clearHistory()`, `subscribeHistory()`.

**`store/useToastStore.ts`** — Tiny Zustand store for transient notifications. `push(kind, text)` adds a toast that auto-removes after 3.5s.

---

### Layout Engine

**`layout/autoLayout.ts`** — Thin wrapper around Dagre. Takes React Flow nodes/edges, returns nodes with computed `x`/`y` positions for a top-down (`TB`) hierarchical layout.

**`layout/storyToGraph.ts`** — Converts a `Story` object into React Flow `nodes`/`edges`. Creates one `phaseNode` per phase plus an always-present `__end__` node. Builds edges from `TransitionRule`s, resolving `toPhase` (name or `'END'`) to node IDs. Accepts an optional `activeTransitionId` to highlight the corresponding edge (thicker, indigo, animated). Calls `applyDagreLayout` before returning.

---

### Canvas Components

**`components/canvas/StoryCanvas.tsx`** — Wraps `<ReactFlow>`. Converts story to graph via `storyToGraph`, manages local node/edge state via `useNodesState`/`useEdgesState`, re-layouts on story or active-transition change. `onConnect` handles drag-to-connect: creates a new `TransitionRule` via `addTransition` and opens it in the properties panel. Exposes `fitView` globally (`window.__regiaFitView`) for image export to use. Must be wrapped in `<ReactFlowProvider>` by the parent.

**`components/canvas/PhaseNode.tsx`** — Custom node renderer for phases. Color-coded by role: green border/bg = initial phase, blue = `DURING ALWAYS`, red = `END`, amber = normal phase. Shows agent count. Animated entrance via Framer Motion. Has top/bottom connection handles.

---

### Panel Components

**`components/panels/Sidebar.tsx`** — Left dark sidebar. Lists all stories (DEFAULT shown distinctly), click to select, buttons to add a new named story or the DEFAULT story (disabled once DEFAULT exists). Animated list via Framer Motion `AnimatePresence`.

**`components/panels/PropertiesPanel.tsx`** — Right panel container. Switches between `StoryProperties` (nothing selected) and `PhaseProperties` (a phase node is selected), animated crossfade/slide via Framer Motion.

**`components/panels/StoryProperties.tsx`** — Edits story name, priority (hidden for DEFAULT), doc comment fields (`@NAME`/`@MEANING`). Renders three `DeclarationList`s (actions, events, conditions). Delete story button.

**`components/panels/DeclarationList.tsx`** — Generic reusable editor for actions/events/conditions at story level. Configured via a `kind` prop (`'action' | 'event' | 'condition'`); shows an origin dropdown for events/conditions but not actions. Add/rename/delete rows.

**`components/panels/PhaseProperties.tsx`** — Edits phase name, `isInitial`/`isAlways` checkboxes (mutually exclusive — checking ALWAYS clears initial and renames to "ALWAYS"). Lists `TransitionEditor`s (hidden for ALWAYS phases) and `AgentEditor`s. Delete phase button. "+ Add" buttons for both transitions and agents.

**`components/panels/AgentEditor.tsx`** — Collapsible block per agent. Editable agent name, remove button, list of `PlanEditor`s, "+ Add WHEN block" button.

**`components/panels/PlanEditor.tsx`** — Full editor for one WHEN block: event dropdown (auto-fills origin from the event's declared origin), origin override dropdown, IF condition list (flat AND list — NOT checkbox + condition dropdown per term, "+ Add condition"), DO sequence (action/believe/forget rows with target dropdowns pulling from story actions/conditions).

**`components/panels/TransitionEditor.tsx`** — Same pattern as `PlanEditor` but for `TRANSITION TO`: target phase dropdown (includes `END`), event+origin, IF condition list. Sets itself as the "active transition" on hover/focus to drive the canvas edge highlight.

**`components/panels/ExportMenu.tsx`** — Dropdown menu (click-away to close). Export section: `.rgs`, `.json`, `.png`, `.svg`. Import section: `.json` and `.rgs` file pickers. All actions report success/failure via `useToastStore`. Imports call `clearHistory()` after loading.

**`components/panels/HistoryControls.tsx`** — Two buttons (↶/↷) bound to `undo()`/`redo()` from `history.ts`, subscribed to history changes for enabled/disabled state.

---

### UI Components

**`components/ui/ToastContainer.tsx`** — Fixed-position bottom-right stack of animated toast messages, color-coded by kind (success/error/info), click to dismiss early.

---

### Export Pipeline

**`export/toRegiaScript.ts`** — The TypeScript mirror of the Python emitter's *grammar shape* (not its AgentSpeak logic — just the source text structure). Walks `RegiaProject` → `Story` → declarations → `PHASE` decls → `DURING` blocks (ordered: named phases first, ALWAYS last) → `TRANSITION TO` rules → `AGENT` blocks → local declarations → `WHEN`/`IF`/`DO` blocks. Includes a DNF-aware `condExprToRgs` (OR of ANDs, with `NOT`) and doc comment emission (`# @NAME:` / `# @MEANING:`). **This is the file most likely to need updates whenever the grammar changes**, alongside `types/story.ts`.

**`export/projectIO.ts`** — `projectToJSON`/`jsonToProject` (with basic shape validation) and a generic `downloadText` helper using Blob URLs.

**`export/toImage.ts`** — `exportCanvasAsPng`/`exportCanvasAsSvg`. Calls the globally-exposed `fitView` before capturing `.react-flow__viewport` via `html-to-image`, waits a frame for layout to settle.

---

### Import Pipeline

**`import/tokenizer.ts`** — Hand-written lexer. Recognizes all keywords (including `TRANSITION`, `TO`, `END`, all origins), identifiers, numbers, punctuation, doc comments (`# @KEY: value`) vs plain comments (skipped), whitespace (skipped). Mirrors `RegiaScript.g4`'s lexer rules.

**`import/fromRegiaScript.ts`** — Recursive descent parser mirroring the grammar's parser rules one-to-one (`parseStoryDef`, `parseDuringBlock`, `parseTransitionRule`, `parseAgentBlock`, `parseWhenBlock`, `parseDoSequence`, etc.). Includes a small `Cursor` helper class for token navigation with lookahead-past-doc-comments (`peekKind`). Condition expressions are parsed into an AST (`CAst`) and then **normalized to DNF** via `astToDNF`/`negateDNF` (De Morgan + distribution), so any validly-nested `NOT`/`AND`/`OR`/parens expression converts into the editor's flat OR-of-ANDs model. Handles merging — the same phase or agent appearing across multiple `DURING`/`AGENT` blocks in the source accumulates into one editor entity. **This is the second file most likely to need updates whenever the grammar changes** — it must stay in lockstep with `toRegiaScript.ts` and `types/story.ts`.

**`import/errors.ts`** — `ImportError` class carrying line/column for precise error messages shown via toast.

---

### Hooks

**`hooks/useKeyboardShortcuts.ts`** — Global `keydown` listener (skipped while typing in inputs/textareas). `Ctrl/Cmd+Z` → undo, `Ctrl/Cmd+Shift+Z` or `Ctrl+Y` → redo, `Delete`/`Backspace` → delete selected phase, `Escape` → deselect phase then story.

---

### Root

**`App.tsx`** — Top-level layout: `Sidebar` | (toolbar + `StoryCanvas` wrapped in `ReactFlowProvider`) | `PropertiesPanel`, plus `ToastContainer`. Toolbar shows story name/priority, `HistoryControls`, "+ Add Phase" (named stories only), `ExportMenu`. Calls `initHistory()` once on mount and `useKeyboardShortcuts()`.

---

## What to Touch When the Grammar Changes

If RegiaScript's grammar evolves (new keywords, new constructs, changed semantics), these files form the change checklist on the editor side, in dependency order:

1. **`types/story.ts`** — add/modify the TypeScript types representing the new construct
2. **`store/useStore.ts`** — add CRUD actions for the new construct if user-editable
3. **`export/toRegiaScript.ts`** — emit the new syntax
4. **`import/tokenizer.ts`** — add new keywords if any
5. **`import/fromRegiaScript.ts`** — parse the new construct
6. **UI panels** (`PhaseProperties.tsx`, `AgentEditor.tsx`, `PlanEditor.tsx`, `TransitionEditor.tsx`, or a new panel) — expose editing for the new construct
7. **`layout/storyToGraph.ts`** / **`PhaseNode.tsx`** — if the new construct affects the visual graph

This mirrors the Python-side checklist (`grammar.g4` → `symbol_table.py` → `emitter.py`), keeping both halves of the system in sync.