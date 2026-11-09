# Visual Editor architecture

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 29

## Question

How is the Visual Editor put together around the WASM Workspace (spec 23)? Decide:
- Where project files live and how they get into the Workspace: a folder on disk (File System Access API), browser storage, or both; folders and tabs, one tab per Plot.
- Whether projects get import roots or search paths (2.0 only has relative paths, spec 10).
- How `.regin` Instancing files and builds are shown and edited, and what happens to `build()`'s output files (download, zip) (spec 21, spec 23).
- Syntax highlighting: a Monaco Monarch grammar, semantic tokens from the WASM Transpiler, or tree-sitter.
- Quick fixes: text edits attached to a diagnostic, offered as Monaco code actions (deferred from spec 23).

## Comments

- Graduated from the map's fog when [Transpiler architecture](29-transpiler-architecture.md) resolved.
- What the graph shows is a separate question, still in the fog.
- Mid-session: asked what to keep in mind for a future VS Code extension that shows the graph next to VS Code's editor. Answered with LSP shapes at the WASM boundary, a graph package independent of its host, and a package split (Q16–Q19).

- Added after resolution (2026-11-09, while resolving [What the graph shows](31-what-the-graph-shows.md)): the editor follows Material 3 through its design tokens and components of our own, in a `regia-theme` package (spec 24, *Design system: Material 3*).

## Answer

Spec: `docs/spec/24-visual-editor-architecture.md`. Spec 23 updated (LSP shapes at the boundary, `fixes`, `semanticTokens`, `moveFile`); spec 10's note on roots updated. Glossary: **Project**, **Build**. No ADR: nothing here is hard to reverse.

- **Platform:** a static web app (Vite, React, Monaco, React Flow `@xyflow/react`, zustand), with no backend. The Workspace runs in a Web Worker behind an async Comlink client that debounces rebuilds and drops stale results. Tauri isn't in 2.0; it would be one more store backend.
- **Project store:** one interface with two backends. **Disk folder** uses the File System Access API (Chromium only); **browser project** uses OPFS (every browser). Both import and export `.zip`. Autosave after a debounce; disk folders are rescanned when the window regains focus. If a file changed on disk while its tab has edits not yet saved, the user chooses which version to keep.
- **Files:** no import roots or search paths; the Project only bounds the file set. The tree hides hidden folders and `build/`. Only `.regia` and `.regin` files go into the Workspace.
- **Layout:** a file tree, Monaco tabs (one per file), and a graph pane that follows the active `.regia` file with one tab per Plot.
- **Monaco models:** every source file gets a model when the Project loads, and every edit, typed or from the core, goes through `pushEditOperations`. Undo is per file, plus an "Undo all" toast after an edit that touches several files.
- **Highlighting:** a lexical Monarch grammar plus semantic tokens from a new `semanticTokens(path)` call. No tree-sitter.
- **Quick fixes:** `Diagnostic.fixes` (a title plus text edits), offered as Monaco code actions and shown in the CLI as a `help:` title. The first fix is the missing import.
- **`moveFile(from, to)`:** a core edit operation that rewrites every affected `IMPORT`, applied when a file is renamed or moved in the tree.
- **Builds:** the Build menu lists every `.regin`, plus every `.regia` that no `.regin` reaches. A build needs zero errors. Output goes to `build/<entry>/` (cleared before each run) on a disk folder, or is downloaded as a zip for a browser project. Instancing is edited as text only in 2.0.
- **Packages:** an npm-workspaces monorepo: `regia-wasm` (wasm-pack output plus a typed Workspace client), `regia-graph` (the React Flow component behind a host interface: graph view and selection in; `requestEdit` and `reveal(span)` out), `regia-web` (the app).
- **Toward VS Code:** the WASM boundary uses LSP shapes (0-based lines with UTF-16 characters, `Diagnostic`, `TextEdit`/`WorkspaceEdit`, `CodeAction`, semantic tokens), and Monaco conversion is done in TypeScript. The graph runs as is in a webview over `postMessage`. The TextMate grammar, the way edits are applied, and the file store would be rewritten for VS Code, on purpose. Native or WASM language server is left to that effort.

