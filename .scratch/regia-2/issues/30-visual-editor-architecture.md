# Visual Editor architecture

Type: grilling
Status: open
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
