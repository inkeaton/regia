# Regia Editor Architecture

> **Scope**: This document explains the internal architecture of the Regia visual editor (`editor/`) and its Python backend (`server.py`). It covers the full data flow from user keystrokes in the code editor, through the compiler backend, to the interactive phase-transition graph rendered on the canvas.

---

## 1. Overview

The Regia editor is a two-panel web application that lets developers write Regia scripts and see an interactive visual representation of the Plot's phase-state machine update in real time. It also supports **direct graph editing**: phases and transitions can be added from the canvas without touching source code.

```
  ┌────────────────────────────────────────────────────────────┐
  │                        Browser                             │
  │                                                            │
  │   ┌──────────────────┐        ┌────────────────────────┐  │
  │   │  Left panel (40%)│        │  Right panel (60%)     │  │
  │   │                  │        │                        │  │
  │   │  CodeEditor      │        │  AstCanvas             │  │
  │   │  (Monaco editor) │        │  (React Flow graph)    │  │
  │   │                  │        │                        │  │
  │   └────────┬─────────┘        └────────────────────────┘  │
  │            │ code string               ▲  nodes & edges    │
  │            ▼  (Zustand store)          │  (Zustand store)  │
  │       useStore.parseCode()      convertAstToGraph()        │
  │            │                    getLayoutedElements()      │
  └────────────┼────────────────────────────────────────────── ┘
               │ POST /parse { source_code }
               ▼
  ┌────────────────────────┐
  │  server.py (FastAPI)   │
  │  port 8000             │
  │  compile_source() ──── │──► Regia compiler pipeline
  │  ASTEncoder            │         (Phases 0-4, no emit)
  │  200 OK: AST JSON      │
  │  400 Bad Request:      │
  │    [CompilerMessage]   │
  └────────────────────────┘
```

**Technology stack:**

| Layer | Technology | Version |
|---|---|---|
| Build tool | Vite | ^8.1.1 |
| UI framework | React | ^19.2.7 |
| Language | TypeScript | ~6.0.2 |
| Code editor | Monaco Editor (`@monaco-editor/react`) | ^4.7.0 |
| Graph canvas | React Flow | ^11.11.4 |
| Graph layout | Dagre | ^0.8.5 |
| State management | Zustand | ^5.0.14 |
| Image export | html-to-image | ^1.11.13 |
| Backend framework | FastAPI + uvicorn | — |
| Linter | OXLint | ^1.71.0 |

---

## 2. Application Shell

### `main.tsx`

The application entry point. Creates the React root and renders `<App />` inside `<StrictMode>`. Imports `index.css` to apply the global design system.

### `App.tsx`

The root component. Establishes the two-column layout:
- **Left (40%)**: `<CodeEditor />` wrapped in `.editorPanel`
- **Right (60%)**: `<AstCanvas />` wrapped in `.canvasPanel`

`App.tsx` contains no logic or state — it is a pure layout component.

### `App.module.css`

Defines the outer flexbox shell:

```css
.appShell     { display: flex; width: 100vw; height: 100vh; }
.editorPanel  { width: 40%;  flex-shrink: 0; ... }
.canvasPanel  { flex: 1;     position: relative; ... }
```

`position: relative` on `.canvasPanel` is required by React Flow's internal absolute positioning.

### `index.css`

The global design system. Defines all CSS custom properties (design tokens) used across every CSS module in the application. No component uses hard-coded colours or spacing values — all reference these variables.

**Token groups:**

| Group | Example tokens | Purpose |
|---|---|---|
| Colors | `--color-bg-editor`, `--color-accent-primary` | Background layers, interactive elements |
| Spacing | `--space-xs` … `--space-xl` | Consistent margins and padding |
| Border radius | `--radius-sm` … `--radius-lg` | Card corners |
| Typography | `--font-ui`, `--font-code`, `--font-size-*` | Font families and sizes |
| Shadows | `--shadow-sm` … `--shadow-lg` | Depth and elevation |
| Transitions | `--transition-fast`, `--transition-normal` | Animation durations |

The palette uses a dark purple-blue scheme:
- `--color-bg-canvas: #13131f` (darkest — the graph background)
- `--color-bg-editor: #1a1a2a` (slightly lighter — the code panel)
- `--color-accent-primary: #7c7cff` (brand purple-blue — all interactive/highlighted elements)
- `--color-accent-initial: #4ade80` (green — the INITIAL phase badge)

---

## 3. Global State (`store/useStore.ts`)

All cross-component state is managed by a single [Zustand](https://zustand-demo.pmnd.rs/) store. No prop drilling or React context is used.

### State Shape (`EditorState`)

```typescript
type EditorState = {
    code:             string;           // Raw Regia source text
    ast:              Program | null;   // Last successfully parsed AST
    isParsing:        boolean;          // True while HTTP request is in flight
    errors:           string[];         // Flat human-readable error strings
    compilerMessages: CompilerMessage[];// Structured messages (line/col) for Monaco

    setCode:    (newCode: string) => void;
    parseCode:  () => Promise<void>;
};
```

### `setCode`

Updates the `code` field in the store. Does **not** trigger parsing. It is called by the Monaco `onChange` callback on every keystroke, and also by `useGraphEditing` whenever the user performs a canvas edit that writes back to source.

### `parseCode`

The async action that drives the core editing loop:

1. Early-returns if `code.trim()` is empty (clears AST and errors).
2. Sets `isParsing: true` and clears previous errors.
3. Calls `fetchAst(code)` (the `api/parser.ts` façade).
4. **On success**: stores the new `ast`, sets `isParsing: false`, clears `compilerMessages`.
5. **On failure**: receives a `TransportError`. If it carries structured `CompilerMessage[]` items, stores them both as raw messages (for Monaco squiggles) and derives a flat `errors: string[]` array (for backward compatibility). Sets `ast: null`.

### Initial Code

On first load, the store initialises `code` with a hardcoded example program (`INITIAL_CODE`). This gives new users a working Regia file to explore immediately. In a future VSCode extension context, this default would be replaced by the active file's content injected via the transport.

---

## 4. Backend Server (`server.py`)

The Python backend is a minimal [FastAPI](https://fastapi.tiangolo.com/) application that exposes the Regia compiler pipeline over HTTP.

### Configuration

- Runs on `http://127.0.0.1:8000` via `uvicorn`.
- CORS is configured with `allow_origins=["*"]` to permit requests from the Vite dev server (typically `localhost:5173`) without origin restriction.

### `CodePayload`

A Pydantic `BaseModel` with a single field `source_code: str`. FastAPI automatically parses and validates the JSON request body into this model.

### `POST /parse`

The sole API endpoint. Its logic:

1. Calls `compile_source(payload.source_code)` — the compiler pipeline's Phase 0–4 entry point (no emission). This never writes files and always returns a `CompileResult`.
2. **On failure** (`result.success == False`): Serialises each `CompilerMessage` from `result.messages`. The `severity` field is an `Enum`, so it is manually converted to its `.name` string (`"ERROR"`, `"WARNING"`) before JSON serialisation. Raises `HTTPException(status_code=400, detail=safe_errors)`.
3. **On success**: Serialises `result.ast` via `ASTEncoder` and returns the plain dict (FastAPI serialises it again as JSON for the response body).

### `ASTEncoder`

A custom `json.JSONEncoder` that handles Python `@dataclass` objects:

```python
def default(self, obj):
    if dataclasses.is_dataclass(obj):
        d = obj.__dict__.copy()   # Shallow dict of this level only
        d["type"] = obj.__class__.__name__  # Inject the class name
        return d                  # Forces recursive calls for child dataclasses
    if hasattr(obj, "value"):     # Handles Enum members (e.g. Severity)
        return obj.value
    return super().default(obj)
```

The key insight is using `__dict__.copy()` (shallow) instead of `dataclasses.asdict()` (deep). A shallow copy leaves child dataclass objects unconverted, which forces `json.dumps` to call `default()` again for each child. This is what causes the `"type"` field injection to happen recursively at every level of the AST tree — exactly what the React frontend needs to identify node types.

---

## 5. Transport Layer

The transport layer abstracts the communication mechanism between the frontend and the backend, making the frontend portable across deployment contexts.

### `Transport` Interface (`services/transport.ts`)

```typescript
interface Transport {
    parse(sourceCode: string): Promise<Program>;
    // Future: emitRegia(ast: Program): Promise<string>;  // POST /emit-regia
}
```

Any future transport (VSCode WebView `postMessage`, Pyodide WASM, etc.) must implement only this interface. No other file in the codebase imports from `services/transport.ts` directly — they go through the `api/` façade.

### `HttpTransport`

The current implementation. Makes a `POST` to `http://127.0.0.1:8000/parse` with `{ source_code }` as a JSON body.

**Error handling:**
- **Network error** (server not running, CORS): the `fetch()` call itself throws. This is caught and converted to a friendly `TransportError` with `messages: []` and a human-readable `"Cannot reach the Regia server..."` message.
- **HTTP 400** (compiler errors): the response body `{ "detail": [...] }` is parsed. The `detail` array is mapped to `CompilerMessage[]` and wrapped into a `TransportError`.

### `createTransport()` Factory

Constructs and returns the active transport. Currently always returns `HttpTransport`. In the future it can detect the VSCode WebView context (`window.acquireVsCodeApi`) and return a different implementation. The singleton `transport` is exported and imported by `api/parser.ts`.

### `api/parser.ts`

A thin façade with a single export:

```typescript
export const fetchAst = (sourceCode: string): Promise<Program> =>
    transport.parse(sourceCode);
```

Its purpose is to decouple the store from the transport layer. The store calls `fetchAst()` and never needs to know whether the transport is HTTP, WebView, or WASM.

---

## 6. Type System (`types/`)

### `types/ast.ts`

Mirrors the Python `ast_nodes.py` dataclasses exactly in TypeScript. Every type is a `type` alias (not `interface`) using intersection with `ASTNode` to add the discriminated `type: "ClassName"` field.

**Key types:**

```
Program
├── TopLevelItem (discriminated union)
│   ├── ActionDecl / EventDecl / FactDecl
│   ├── PlaybookDef
│   │   └── PbWhenBlock
│   │       ├── PbIfBranch  (condition: ConditionExpr)
│   │       └── PbElseBranch
│   ├── PlotDef
│   │   ├── PhaseDecl
│   │   ├── RoleDecl
│   │   └── DuringBlock
│   │       ├── OnEnter / OnExit   (stmts: ImperativeStmt[])
│   │       ├── PlotWhenBlock
│   │       ├── PlotWhenSubplotEndsBlock
│   │       └── PlotWhenRoleSignalsBlock     ← NEW
│   │           ├── PlotIfBranch
│   │           └── PlotElseBranch
│   └── ImportDecl
└── doc_comments?: DocAnnotation[]
```

`ConditionExpr = ConditionOr | ConditionAnd | ConditionNot | FactRef` mirrors the recursive union in Python.

`ImperativeStmt = AssignStmt | UnassignStmt | WorldDoStmt | RoleDoStmt | InlineTransitionStmt | StartSubplotStmt | PlotEndStmt`

`SourceLoc` carries `line`, `column`, and `filename` for every node — reserved for click-to-navigate (a planned future feature).

#### `PlotWhenRoleSignalsBlock`

Added to support the `WHEN ROLE <RoleName> SIGNALS <EventName>:` grammar construct:

```typescript
export type PlotWhenRoleSignalsBlock = ASTNode & {
    type:         "PlotWhenRoleSignalsBlock";
    role_name:    string;
    event:        string;
    priority:     number | null;
    prefix_stmts: ImperativeStmt[];
    branches:     PlotIfBranch[];
    else_branch:  PlotElseBranch | null;
    loc:          SourceLoc;
};
```

`DuringBlock.when_blocks` is typed as `(PlotWhenBlock | PlotWhenSubplotEndsBlock | PlotWhenRoleSignalsBlock)[]`.

### `types/transport.ts`

Defines the wire-format types separate from the AST types:

| Type | Description |
|---|---|
| `ParseRequest` | `{ source_code: string }` — sent to `POST /parse` |
| `ParseResponse` | Alias for `Program` — the success body |
| `CompilerMessage` | `{ message, severity, filename, line, column }` — error detail item |
| `TransportError` | `{ message, messages: CompilerMessage[] }` — thrown by transport on failure |

---

## 7. Code Editor (`components/editor/CodeEditor.tsx`)

`CodeEditor` wraps the `@monaco-editor/react` component and owns all Monaco-specific integration logic.

### Responsibilities

1. **Language registration**: calls `registerRegiaLanguage(monaco)` inside the `beforeMount` callback — this fires once before the editor instance is created.
2. **Debounced parse trigger**: uses `useDebounce(code, 500)` to delay parse calls until 500ms after the user stops typing. A `useEffect` fires `parseCode()` whenever the debounced value changes.
3. **Inline error markers**: a second `useEffect` watches `compilerMessages`. Whenever the array changes, it maps each `CompilerMessage` to a Monaco `IMarkerData` object (with severity, line, column, and "underline to end of line" extent) and calls `monaco.editor.setModelMarkers()` to push them as squiggles onto the current model.
4. **Refs**: holds `editorRef` and `monacoRef` to persist the editor and Monaco API instances across re-renders so the marker sync effect can access them without re-subscribing.

### Monaco Options

| Option | Value | Rationale |
|---|---|---|
| `minimap.enabled` | `false` | Source files are short; minimap adds no value |
| `fontSize` | `14` | Matches `--font-size-base` token |
| `fontFamily` | JetBrains Mono / Fira Code / Cascadia Code | Matches `--font-code` token |
| `scrollBeyondLastLine` | `false` | Cleaner feel for short Regia files |
| `automaticLayout` | `true` | Recalculates layout on panel resize |
| `wordWrap` | `"on"` | Prevents horizontal scroll for long lines |
| `cursorBlinking` | `"smooth"` | Visual polish |

### Severity Mapping

```typescript
const SEVERITY_MAP: Record<string, MonacoType.MarkerSeverity> = {
    ERROR:   4,  // MonacoType.MarkerSeverity.Error
    WARNING: 2,  // MonacoType.MarkerSeverity.Warning
    INFO:    1,  // MonacoType.MarkerSeverity.Hint
};
```

The numeric values match Monaco's internal `MarkerSeverity` enum. The backend sends severity as a plain string (`"ERROR"`, `"WARNING"`), so the map converts them.

---

## 8. Monaco Language Service (`services/regiaLanguage.ts`)

Registers a custom Monarch tokeniser, editor theme, and language configuration with Monaco before the editor first mounts.

### Monarch Tokeniser

The tokeniser is a state-machine lexer (`IMonarchLanguage`) with two states: `root` and `string`.

Keyword groups (used in the `cases` matcher for all-uppercase identifiers):

| Group | Examples | Token class | Color |
|---|---|---|---|
| `declarationKeywords` | `ACTION EVENT FACT PLAYBOOK PLOT PHASE ROLE IMPORT` | `keyword.declaration` | `#7c7cff` bold |
| `flowKeywords` | `DURING WHEN IF ELSE ON ENTER EXIT TRANSITION ENDS SIGNALS` | `keyword.flow` | `#9898ff` |
| `actionKeywords` | `DO ASSIGN UNASSIGN WORLD SIGNAL START SUBPLOT END MAPPING TO AS` | `keyword.action` | `#4ade80` |
| `builtinKeywords` | `TELL BROADCAST ACHIEVE BELIEVE FORGET PRINT WAIT` | `keyword.builtin` | `#4ade80` italic |
| `modifierKeywords` | `PRIORITY TEMPER EFFECTS INITIAL SELF ENVIRONMENT FROM AND OR NOT` | `keyword.modifier` | `#9898b8` |

The tokeniser matches uppercase sequences first, dispatching through the `cases` object to determine the token type. Identifiers that match none of the keyword lists fall through to `"identifier.type"` (PascalCase names like `SingerInBackstage`) or `"identifier"` (all-lowercase names like `greet_back`).

Doc comments (`#@...` and `#-...`) are matched with `/#[@-].*$/` before the ordinary comment pattern `/#.*$/`, giving them a distinct italic style.

### Custom Theme (`REGIA_THEME`)

A complete `IStandaloneThemeData` derived from `vs-dark` with `inherit: false`, meaning no Monaco defaults bleed through. All colour values are the CSS variable values from `index.css` expressed as hex strings (since Monaco does not read CSS variables at runtime).

Notable customisations:
- `editor.selectionBackground: #7c7cff44` — accent colour at 27% opacity for selections.
- `editorCursor.foreground: #7c7cff` — cursor uses the accent colour.
- Squiggle underline colours are left at Monaco defaults (red/yellow) because they reliably signal errors/warnings without custom configuration.

### Language Configuration (`LANGUAGE_CONFIG`)

Enables editor-level features:
- `lineComment: "#"` — `Ctrl+/` toggles `#` comments.
- `brackets: [["(", ")"]]` — bracket-matching highlights.
- `autoClosingPairs` — automatically inserts `)` and `"` when opening pair is typed.
- `surroundingPairs` — wraps selected text when a bracket or quote is typed.

---

## 9. Custom Hook (`hooks/useDebounce.ts`)

`useDebounce<T>(value: T, delay: number): T` is a generic hook that delays propagating a value until `delay` milliseconds after the last update.

Implementation:
1. Stores the debounced value in local state.
2. In a `useEffect`, sets a `setTimeout` for `delay` ms. The cleanup function calls `clearTimeout` so every new `value` resets the timer.
3. Returns the debounced state value.

Used by `CodeEditor` with `delay = 500`. This means the store's `parseCode()` is only called once the user has stopped typing for half a second, preventing an HTTP request on every keystroke.

---

## 10. Graph Canvas (`components/canvas/AstCanvas.tsx`)

`AstCanvas` renders the interactive React Flow canvas and orchestrates the full AST-to-graph pipeline. It also hosts the interactive graph-editing UI.

### Behaviour

- Reads `ast` and `errors` from the Zustand store.
- When `ast` changes (via a `useEffect`), runs the full graph conversion and layout pipeline:
  1. `convertAstToGraph(ast)` → raw `{ nodes, edges }` (no positions).
  2. `getLayoutedElements(rawNodes, rawEdges, "TB")` → positioned `{ nodes, edges }`.
  3. Stores positioned data in local component state (`useState`).
- If `errors.length > 0`, applies `styles.canvasWrapperDimmed` to visually dim the canvas, indicating the graph is stale (the AST has not been updated since the last error).
- If the AST has no `PlotDef` (e.g. a Playbook-only file), the canvas is cleared rather than showing a partial graph.

### React Flow Configuration

- `nodeTypes = { phaseNode: PhaseNode }` — registers the custom phase node renderer.
- `edgeTypes = { transitionEdge: TransitionEdge }` — registers the custom edge renderer with staggered label support.
- `fitView` with `padding: 0.2` — fits all nodes in view after every layout recalculation.
- `onConnect` — wired to `useGraphEditing().onConnect` to intercept user-drawn connections.
- `nodesDraggable: false` — phases cannot be repositioned manually; layout is always Dagre-computed.
- `nodesConnectable: true` — enables drag-to-connect handles on each phase node.
- `Background`, `Controls` — built-in React Flow plugins for the dotted grid background and zoom/pan buttons.

### Info Panel (top-left)

Shown when a Plot is loaded. Displays:
- The Plot name.
- Chip badges for each declared Role.
- An **"+ Add Phase"** button that triggers `useGraphEditing().onPaneDoubleClick()`.

### Export Panel (top-right)

Contains two buttons (PNG and SVG) that call `exportCanvas()` from `export/toImage.ts`. Currently hardcoded to `plotName = "plot"`.

### Modals

Two overlay modals are rendered conditionally on top of the canvas:

| Modal | Condition | Purpose |
|---|---|---|
| `<AddPhaseModal />` | `isAddingPhase === true` | Prompts the user for a phase name, then calls `confirmAddPhase` |
| `<EventPickerModal />` | `pendingConnection !== null` | Prompts the user to pick or type an event name for a new transition, then calls `confirmAddTransition` |

### Custom Node Type Registry

New node types are registered in the `NODE_TYPES` constant object at the top of the file:

```typescript
const NODE_TYPES = {
    phaseNode: PhaseNode,
};
```

The key (`"phaseNode"`) must match the `type` field set by `astToGraph.ts` when constructing nodes.

---

## 11. Graph Editing (`hooks/useGraphEditing.ts` + `services/codeTransformer.ts`)

The graph editing subsystem enables **bidirectional (canvas → source)** editing: when the user adds a phase or draws a transition on the canvas, the source code is updated to reflect the change. The debounced `parseCode()` then re-parses the new code, and the graph re-renders from the fresh AST.

### `useGraphEditing` Hook

Manages the interaction state machine and coordinates between React Flow events and the code transformer:

```typescript
// State
pendingConnection: PendingConnection | null  // set when a drag-to-connect completes
isAddingPhase:     boolean                   // set when "Add Phase" button is clicked

// Handlers wired to React Flow
onConnect(connection)        // called when user drags an edge between two handles
onPaneDoubleClick()          // called by the "Add Phase" button

// Confirmed actions
confirmAddPhase(phaseName)   // called by AddPhaseModal on submit
confirmAddTransition(event)  // called by EventPickerModal on submit
cancelPending()              // dismisses any open modal
```

**Interaction flow for a new transition:**
1. User drags from a source handle to a target handle on the canvas.
2. React Flow calls `onConnect(connection)`. A `PendingConnection { source, target }` is stored.
3. `<EventPickerModal />` appears (because `pendingConnection !== null`).
4. User types or selects an event name and confirms.
5. `confirmAddTransition(eventName)` is called. It delegates to `addTransition()`.
6. The store's `code` is updated. `parseCode()` fires after the debounce delay.

**Interaction flow for a new phase:**
1. User clicks "**+ Add Phase**" in the info panel.
2. `onPaneDoubleClick()` sets `isAddingPhase: true`.
3. `<AddPhaseModal />` appears.
4. User types a name and confirms.
5. `confirmAddPhase(phaseName)` delegates to `addPhase()`.
6. The store's `code` is updated. `parseCode()` fires after the debounce delay.

### `services/codeTransformer.ts`

Pure functions that perform **AST-aware string manipulation** on the source code. They operate by finding the correct insertion line from the AST's `loc` metadata and then inserting lines at that position. They do **not** generate or parse a complete AST — the Python server handles that after the edit.

#### `addPhase(code, ast, rawName): string`

Inserts a new phase into the source. `rawName` is converted to `snake_case`.

1. **PhaseDecl**: Finds the last `PhaseDecl` in the Plot header (by `loc.line`) and inserts `PHASE name.` on the next line.
2. **DuringBlock**: Appends a new `DURING name: ON ENTER: WORLD DO PRINT("name started").` skeleton at the end of the file (after all existing `DURING` blocks).

The skeleton body ensures the new phase is immediately valid — it has a `DURING` block with an `ON ENTER` hook — so the compiler does not reject it.

#### `addTransition(code, ast, sourcePhaseName, targetPhaseName, rawEventName): string`

Inserts a `WHEN event: TRANSITION TO target.` block inside the source phase's `DURING` block.

1. **Event declaration**: checks whether the event already exists in the AST. If not, inserts `EVENT eventName.` right before the `PLOT` declaration, then tracks a `linesShifted` offset.
2. **WHEN block**: finds the `DuringBlock` whose `phase_name === sourcePhaseName`. Inserts `WHEN event: TRANSITION TO target.` just before the start of the next `DuringBlock` (or at EOF if it is the last one), accounting for the `linesShifted` offset from step 1.

---

## 12. Phase Node (`components/canvas/PhaseNode.tsx`)

`PhaseNode` is the custom React Flow node renderer for Regia phases.

### `PhaseNodeData`

```typescript
type PhaseNodeData = {
    label:     string;   // Phase name (e.g. "backstage")
    isInitial: boolean;  // True for the INITIAL phase
    line:      number;   // Source line number (reserved for click-to-navigate)
};
```

### Handles

Each `PhaseNode` exposes **six connection handles** to support the smart edge routing in `astToGraph.ts`:

| Handle ID | Position | Type | Purpose |
|---|---|---|---|
| `top-t` | Top | target | Forward transitions (incoming) |
| `bottom-s` | Bottom | source | Forward transitions (outgoing) |
| `right-s` | Right (40%) | source | Lateral/reverse edges (outgoing) |
| `right-t` | Right (60%) | target | Lateral/reverse edges (incoming) |
| `left-s` | Left (40%) | source | Second lateral slot (outgoing) |
| `left-t` | Left (60%) | target | Second lateral slot (incoming) |

The left/right handle pairs at different vertical offsets prevent source and target handles from occupying the same pixel, avoiding visual ambiguity for bidirectional edges.

### Visual Style

The INITIAL phase receives both `.nodeCard` and `.nodeCardInitial` CSS classes, giving it a green border and accent colour defined by `--color-accent-initial`. Non-initial phases use only `.nodeCard`.

The node footer displays the source line number. This is currently cosmetic; it is intended as data for a future click-to-navigate feature.

---

## 13. Transition Edge (`components/canvas/TransitionEdge.tsx`)

`TransitionEdge` is a custom React Flow edge renderer that draws transition arrows with staggered labels to avoid collision when multiple edges are present.

### Props Used

- `label` — the event name string (e.g. `"emergency"`, `"ROLE Hero SIGNALS warning"`).
- `data.slot` — an integer assigned by `astToGraph.ts` indicating which collision-avoidance slot this edge occupies.
- Standard React Flow geometry props (`sourceX/Y`, `targetX/Y`, `sourcePosition`, `targetPosition`).

### Label Staggering

The `slot` value drives a vertical `yOffset` applied to the label `translate`:
- **Slot 0** (immediate forward / straight line): no offset — label sits at the midpoint.
- **Odd slots** (right-arc edges): label shifts **up** by `25 × ⌈slot/2⌉` px.
- **Even slots > 0** (left-arc edges): label shifts **down** by `25 × ⌈slot/2⌉` px.

This ensures that even when many edges share the same label midpoint region, their labels fan out vertically instead of overlapping.

---

## 14. Layout Engine (`layout/`)

### `astToGraph.ts` — AST → Graph Mapper

`convertAstToGraph(ast)` converts a `Program` AST into unpositioned React Flow nodes and edges.

**Node creation**: Iterates `plot.phases` and creates one `Node` per `PhaseDecl`:

```typescript
{
    id:   phase.name,       // Used as node ID and edge source/target
    type: "phaseNode",
    position: { x: 0, y: 0 },  // Placeholder; dagre will override
    data: { label, isInitial, line },
}
```

A `phaseIndexMap` records each phase's declaration order, used to classify edges as "immediate forward" or "lateral/reverse".

**Edge creation**: Iterates all `DuringBlock.when_blocks` (skipping `DURING PLOT` blocks, which have `phase_name = null`). For each `when_block` of any type, scans `prefix_stmts`, `branches[*].stmts`, and `else_branch.stmts` for `InlineTransitionStmt` nodes. Each one becomes a directed edge. The edge **label** is determined by the when block's type:

| Block type | Label format |
|---|---|
| `PlotWhenBlock` | `event` — the bare event name |
| `PlotWhenSubplotEndsBlock` | `"SUBPLOT <name> ENDS"` |
| `PlotWhenRoleSignalsBlock` | `"ROLE <role> SIGNALS <event>"` |

**Smart edge routing**: Decides the handle pair and edge type based on two criteria:

1. **Immediate forward** (`targetIdx - sourceIdx === 1`) + **first edge between this pair** (`slot === 0`): uses `"smoothstep"` routing with `bottom-s` → `top-t`. These are the common, vertical arrows in a top-to-bottom layout.
2. **All other edges** (reverse, skip, bidirectional): uses `"default"` (Bezier) routing through alternating left/right lateral handles. A `lateralCounter` alternates between right-side and left-side pairs to prevent all curved edges from stacking on the same side.

An `edgePairCounts` dict keyed by the **unordered** node pair (`[source, target].sort().join("-")`) tracks how many edges already exist for each pair, ensuring a second edge in the same direction still gets lateral routing.

All edges are of type `"transitionEdge"` (the custom `TransitionEdge` component), and carry `data.slot` for label staggering.

**Current limitation**: only the first `PlotDef` in the program is visualised. Multi-Plot support is documented as deferred.

### `autoLayout.ts` — Dagre Positioning

`getLayoutedElements(nodes, edges, direction)` takes unpositioned nodes and lays them out using [Dagre](https://github.com/dagrejs/dagre):

1. Creates a `dagre.graphlib.Graph` configured with `rankdir`, `ranksep`, and `nodesep` from `constants.ts`.
2. Registers every node with its dimensions (`NODE_WIDTH × NODE_HEIGHT`).
3. Registers every edge (source → target only; direction is sufficient for layout).
4. Calls `dagre.layout()`.
5. Reads back the computed center positions from `dagreGraph.node(id)`, offsets by half the node dimensions (since React Flow uses top-left corners), and returns new node objects with updated `position` values.

### `constants.ts` — Single Source of Truth

All geometry values in one place:

| Constant | Value | Used in |
|---|---|---|
| `NODE_WIDTH` | 220px | `autoLayout.ts` + `PhaseNode.module.css` |
| `NODE_HEIGHT` | 100px | `autoLayout.ts` |
| `LAYOUT_RANK_SEP` | 150px | `autoLayout.ts` (vertical gap between rows) |
| `LAYOUT_NODE_SEP` | 120px | `autoLayout.ts` (horizontal gap within a row) |
| `EDGE_COLOR` | `#7c7cff` | `astToGraph.ts` (matches `--color-edge`) |
| `EDGE_STROKE_WIDTH` | 2 | `astToGraph.ts` |
| `EDGE_MARKER_WIDTH/HEIGHT` | 20 | `astToGraph.ts` (arrowhead size) |

### `graphToAst.ts` — Reverse Mapper (stub)

`convertGraphToAst(nodes, edges, plotName): PlotDef` is a **not yet implemented** stub. When Phase 5 (bidirectional editing) is tackled, this function will:

1. Map each `phaseNode` back to a `PhaseDecl`.
2. Map each edge back to an `InlineTransitionStmt` inside a `PlotWhenBlock`.
3. Wrap them into `DuringBlock`s and a `PlotDef`.
4. Call `transport.emitRegia(ast)` (`POST /emit-regia`) to get back a Regia source string.
5. Update the store's `code` field.

The `emitRegia` method stub is already declared in the `Transport` interface as a comment, and the corresponding `/emit-regia` server endpoint is planned. The round-trip guarantee is that the Python server is the authoritative source for both parsing and emission.

> **Note**: Direct graph editing (§11) currently works by writing Regia source text directly, bypassing this round-trip. `convertGraphToAst` will be needed only if the canonical edit path switches to AST-first emission.

---

## 15. Export (`export/toImage.ts`)

`exportCanvas(format, plotName)` captures the React Flow viewport and downloads it as an image.

Implementation:
1. Queries the `.react-flow__viewport` element — React Flow's internal container that holds all nodes and edges.
2. **Temporarily resets** the element's `transform` to `translate(0px, 0px) scale(1)`. This is necessary because React Flow's pan/zoom is implemented as a CSS transform; leaving it in place would capture only the currently visible portion at the current zoom, rather than the full graph.
3. Calls either `toPng()` or `toSvg()` from `html-to-image`, which serialises the DOM subtree to an image.
4. For PNG: `pixelRatio: 2` produces a high-resolution (2×) output suitable for display at retina densities.
5. Creates a temporary `<a>` element with the `download` attribute and programmatically clicks it to trigger the browser's native file download.
6. **Restores** the original transform in the `finally` block to return the user to their previous pan/zoom position.

---

## 16. Module Map

```
editor/src/
├── main.tsx                        App entry point; creates the React root.
├── App.tsx                         Root component; two-column layout shell.
├── App.module.css                  Flexbox split layout (40/60).
├── index.css                       Global reset, design tokens, scrollbar.
│
├── api/
│   └── parser.ts                   Thin façade: exports `fetchAst()`.
│
├── services/
│   ├── transport.ts                Transport interface, HttpTransport, factory.
│   ├── regiaLanguage.ts            Monaco language: Monarch tokeniser, theme, config.
│   └── codeTransformer.ts         AST-aware source mutations: addPhase, addTransition.
│
├── store/
│   └── useStore.ts                 Zustand store: code, ast, errors, actions.
│
├── hooks/
│   ├── useDebounce.ts              Generic debounce hook.
│   └── useGraphEditing.ts          Interaction state machine for canvas editing.
│
├── types/
│   ├── ast.ts                      TypeScript mirror of Python ast_nodes.py.
│   └── transport.ts                Wire types: ParseRequest, CompilerMessage, TransportError.
│
├── components/
│   ├── editor/
│   │   ├── CodeEditor.tsx          Monaco wrapper; debounced parse; inline markers.
│   │   └── CodeEditor.module.css   Editor panel layout.
│   └── canvas/
│       ├── AstCanvas.tsx           React Flow canvas; orchestrates layout + editing.
│       ├── AstCanvas.module.css    Canvas wrapper, dimmed state, export/info panels.
│       ├── PhaseNode.tsx           Custom React Flow node: phase card + 6 handles.
│       ├── PhaseNode.module.css    Phase card styles (initial badge, colours).
│       ├── TransitionEdge.tsx      Custom React Flow edge: Bezier path + staggered labels.
│       ├── AddPhaseModal.tsx       Modal for naming a new phase.
│       ├── AddPhaseModal.module.css
│       ├── EventPickerModal.tsx    Modal for selecting/typing a transition event.
│       └── EventPickerModal.module.css
│
├── layout/
│   ├── astToGraph.ts               AST → React Flow nodes/edges (smart routing).
│   ├── autoLayout.ts               Dagre-based automatic positioning.
│   ├── constants.ts                Node/edge geometry constants.
│   └── graphToAst.ts               Reverse mapper (stub, not yet implemented).
│
└── export/
    └── toImage.ts                  PNG/SVG export via html-to-image.
```

---

## 17. Key Data Flow: Keystroke to Graph

This section traces one complete update cycle from the user pressing a key to the graph updating.

```
User types a character in Monaco
        │
        ▼
handleChange(value) → store.setCode(value)
        │                (store.code updated, no parse yet)
        ▼
useDebounce(code, 500ms)
        │   (timer resets on each keystroke)
        │   (fires 500ms after last keystroke)
        ▼
useEffect([debouncedCode]) → store.parseCode()
        │
        ▼
fetchAst(code) → transport.parse(sourceCode)
        │          POST http://127.0.0.1:8000/parse
        │          { source_code: "..." }
        │
        ▼  (Python server)
compile_source(source)
        │  Phase 0: Preprocess
        │  Phase 1: Parse (Lark)
        │  Phase 2: Build AST
        │  Phase 3: Attach doc comments
        │  Phase 4: Validate
        ▼
result.ast (Program dataclass)
        │
json.dumps(result.ast, cls=ASTEncoder)
        │  injects "type" at every AST level
        ▼
HTTP 200 { "type": "Program", "items": [...] }
        │
        ▼  (frontend)
store.ast = parsedAst (Program TypeScript object)
        │
        ▼
AstCanvas useEffect([ast])
        │
        ├── convertAstToGraph(ast)
        │       iterates plot.phases → Node[]
        │       iterates during_blocks → Edge[] (InlineTransitionStmt)
        │       smart routing: immediate-forward vs lateral/reverse
        │       edge labels: event / SUBPLOT ENDS / ROLE SIGNALS
        │
        ├── getLayoutedElements(rawNodes, rawEdges, "TB")
        │       dagre.layout() computes optimal positions
        │       offsets from center to top-left
        │
        └── setNodes(layoutedNodes) + setEdges(layoutedEdges)
                    │
                    ▼
        React Flow re-renders with new nodes and edges
        PhaseNode renders each phase card (INITIAL badge if is_initial)
        TransitionEdge renders Bezier paths with staggered event labels
```

---

## 18. Canvas Edit Flow: Graph to Source

This section traces an edit initiated from the canvas (e.g. drawing a transition).

```
User drags from PhaseA.bottom-s to PhaseB.top-t
        │
        ▼
React Flow fires onConnect({ source: "phaseA", target: "phaseB" })
        │
        ▼
useGraphEditing.onConnect()
        │  sets pendingConnection = { source, target }
        ▼
<EventPickerModal /> renders (pendingConnection !== null)
        │
User types "quest_started" and clicks Confirm
        │
        ▼
confirmAddTransition("quest_started")
        │
        ▼
addTransition(code, ast, "phaseA", "phaseB", "quest_started")
        │  1. EVENT quest_started not found → inserts "EVENT quest_started." before PLOT
        │  2. Finds DURING phaseA block → inserts:
        │       WHEN quest_started:
        │           TRANSITION TO phaseB.
        ▼
store.setCode(newCode)   ← store.code updated
        │
        ▼
useDebounce fires after 500ms
        │
        ▼
store.parseCode() → POST /parse → fresh AST
        │
        ▼
AstCanvas re-renders with the new edge phaseA → phaseB (label: "quest_started")
```

---

## 19. Error Flow: Compile Failure to Monaco Squiggles

```
compile_source() returns result.success = False
        │
server.py serialises CompilerMessage[] as:
{ "detail": [{ message, severity, filename, line, column }, ...] }
        │
HTTP 400 response
        │
HttpTransport.parse() catches non-ok response
→ throws TransportError { message, messages: CompilerMessage[] }
        │
store.parseCode() catches TransportError
→ set({ ast: null, errors: ["..."], compilerMessages: [...] })
        │
CodeEditor useEffect([compilerMessages])
→ maps each CompilerMessage to IMarkerData:
    { severity: 4, startLineNumber: line, endColumn: lineMaxColumn, ... }
→ monaco.editor.setModelMarkers(model, "regia-compiler", markers)
        │
Monaco draws red squiggles at the reported lines
AstCanvas dims (hasSyntaxErrors = true → .canvasWrapperDimmed)
```
