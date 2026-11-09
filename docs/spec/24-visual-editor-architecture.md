# Visual Editor architecture

How the Visual Editor is put together around the WASM Workspace: where the platform runs, how project files are stored and fed to the Workspace, the layout, highlighting, quick fixes, builds, and the package split that keeps the core and the graph reusable in a future VS Code extension. Decided in the ticket *Visual Editor architecture* (`.scratch/regia-2/issues/30-visual-editor-architecture.md`). It builds on chapter 10 (imports), chapter 21 (Instancing), chapter 22 (bidirectional editing) and chapter 23 (Transpiler architecture). What the graph draws is still open.

## Platform

- A **static web app**: Vite, React, Monaco (`@monaco-editor/react`), React Flow (`@xyflow/react`) and zustand, as in 1.0. There is no backend. The HTTP calls 1.0 made to the Python Transpiler are replaced by the WASM Workspace (chapter 23).
- The graph layout engine (dagre or elkjs) is decided together with what the graph shows.
- The Workspace runs in a **Web Worker**. The UI reaches it through an async client (Comlink). The client also debounces rebuilds and drops results that a newer change has made stale, so typing never waits on a Model rebuild.
- A desktop wrapper (Tauri) is not part of 2.0. It could be added later as one more project store backend (below), without changing anything else.

## Projects and the project store

A **Project** is a folder of files. Every file access goes through one small **project store** interface (list, read, write, rename, delete) with two backends:

| Backend | Where files live | Browsers |
| --- | --- | --- |
| Disk folder | A folder on disk opened with the File System Access API. Edits change the user's real files. | Chromium only (Chrome, Edge) |
| Browser project | The Origin Private File System (OPFS). | All, including Firefox and Safari |

- Both backends can **import and export a Project as a `.zip`**. That's how a browser project moves to disk or into git.
- The editor offers only the backends the browser supports. Where "Open folder" is missing, a note explains why.
- There are **no import roots or search paths**: imports stay relative to the importing file (chapter 10). The Project only bounds which files the Workspace holds. Roots can be added later without breaking anything, since a relative path stays valid.

### What the Workspace is given

- The file tree shows the Project folder except hidden folders (`.git`, …) and `build/`.
- Only `.regia` and `.regin` files are set into the Workspace. Other plain-text files open in Monaco without language features, and other files are listed but don't open.
- Target output never goes back into the Workspace.

### Saving and outside changes

- Edits are **autosaved** to the store after a short debounce, with no save step. The Workspace gets `setFile` on every change, so what is built is always what is on screen.
- Disk folders can't be watched portably, so the editor **rescans the folder when the window regains focus** and sets changed files into the Workspace. This covers editing in another tool or running `git pull`.
- If a file changed on disk while its tab has edits that aren't saved yet, the editor asks whether to keep those edits or take the version on disk.

## Layout

```
┌───────────┬──────────────────────────┬──────────────────────────┐
│ file tree │ [banquet.regia] [test…]  │ [RoyalBanquet] [Duel]    │
│           │                          │                          │
│ banquet…  │   Monaco                 │   graph of the Plot      │
│ duel…     │                          │                          │
│ test.regin│                          │                          │
└───────────┴──────────────────────────┴──────────────────────────┘
```

- **Text tabs, one per open file.**
- The **graph pane** follows the active `.regia` tab and has **its own tabs, one per Plot** in that file. A file with no Plot shows an empty pane with a short note.
- `.regin` tabs show no graph.

### Monaco models and undo

- When a Project loads, every `.regia` and `.regin` file gets its own **Monaco model**. Opening a tab only shows that model.
- Every edit, typed or from the core, lands in a model through `pushEditOperations` (chapter 22) and is autosaved like typing. This includes edits to files that aren't open: graph edits that add a declaration to another file, and `moveFile` (below).
- **Undo is per file**, as in Monaco. After an edit that touches several files, the editor shows a toast with one "Undo all" for that operation.

## Highlighting

Highlighting has two layers:

1. **A Monarch grammar** gives instant lexical colours: keywords, plain comments including nested `#[ ]#`, doc comments, Instancing comments, strings, numbers and `?variables`. It knows nothing about meaning, so it can't drift from the parser on what a name means.
2. **Semantic tokens** from the Workspace (`semanticTokens(path)`, chapter 23) colour each name by what it resolves to after a rebuild: Event, Fact, Goal, Playbook, Role, Plot. That shows a designer whether a name is the thing they meant.

There is no tree-sitter grammar (ADR 0010).

## Quick fixes

A diagnostic may carry **fixes**: a title and the text edits that apply it (chapter 23). The editor offers them as Monaco code actions. Which diagnostics get a fix is decided per diagnostic code during development. The first one is chapter 10's missing import ("Add `IMPORT "shared/food"`").

## Renaming and moving files

Renaming or moving a file breaks every `IMPORT` that points at it, and the moved file's own imports. When a file is renamed or dragged in the tree, the editor asks the core for the `moveFile(from, to)` edit operation (chapter 23). It returns text edits that rewrite every affected `IMPORT` string across the Project. The editor applies them as one multi-file edit, then renames the file in the store. Path logic lives only in the core.

## Instancing and builds

- `.regin` files and `#%` Instancing comments are **edited as text** in 2.0, with the same highlighting and diagnostics as `.regia` files. A form editor for Agents, counts and Propensities comes later.
- The **Build menu** lists every Entry the Workspace checks: every `.regin` file, plus every `.regia` file that no `.regin` reaches (chapter 23). A `.regia` file that some `.regin` reaches isn't listed, because building it alone would ignore that `.regin`'s overrides (chapter 21). Each `.regin` tab also has a Build button.
- A build runs only with **zero errors** (chapter 23). Otherwise the editor shows the diagnostics and builds nothing.
- **Output** is the `(path, text)` list from `build(entry)`:
  - **Disk folder:** written to `build/<entry name>/` in the Project. The folder is cleared first, so files for renamed or removed Playbooks don't linger. "Download as zip" is offered too.
  - **Browser project:** downloaded as `<entry name>.zip`.

## Packages

The frontend is an npm-workspaces monorepo next to the Cargo workspace:

| Package | Holds | Depends on |
| --- | --- | --- |
| `regia-wasm` | The wasm-pack output of the `regia-wasm` crate, plus a typed async **Workspace client**. The client hides whether the Workspace runs in a Web Worker or, later, in Node. | — |
| `regia-graph` | The graph component: React Flow, layout, and the graph's edit gestures. | `regia-wasm` (types only) |
| `regia-web` | The app: project store, Monaco, the Monaco adapters, tabs, layout, builds. | both |

### The graph's host interface

`regia-graph` never touches Monaco, the project store or the Workspace. It talks to its host through one small interface of plain data:

| Direction | Message |
| --- | --- |
| host → graph | The current graph view of a Plot, and which node is selected (following the text cursor). |
| graph → host | `requestEdit(operation)`: a domain edit operation by structural key (chapter 22). |
| graph → host | `reveal(span)`: show this text, for example when a node is clicked. |

In `regia-web` the host is plain function calls. This boundary also lets the graph be tested alone with fixture graph views.

## Toward a VS Code extension

A VS Code extension that shows the graph next to VS Code's own text editor is a post-2.0 effort. The 2.0 architecture keeps that path open:

- **The WASM boundary uses LSP's shapes** (chapter 23): 0-based lines with UTF-16 characters, LSP-shaped diagnostics, text edits, workspace edits, code actions and semantic tokens. `regia-web` converts to Monaco in TypeScript. A language server would forward the same values unchanged.
- **The graph moves as is.** In VS Code, `regia-graph` runs in a webview and its host messages travel through `postMessage`.
- **Parts that are rewritten, on purpose:**
  - **Lexical highlighting:** VS Code uses a TextMate grammar instead of Monarch. Sharing one TextMate grammar now would need an Oniguruma loader in the web app, so the duplication is accepted. Semantic tokens are shared.
  - **Applying edits:** VS Code applies a workspace edit with its own undo across files, and file renames reach `moveFile` through LSP's `workspace/willRenameFiles`. The "Undo all" toast is web-only.
  - **Files:** the VS Code workspace replaces the project store.
- Whether the language server is a native Rust binary or the WASM build running in Node is left to that effort. Both work because the core does no I/O.
