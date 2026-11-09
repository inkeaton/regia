# Transpiler architecture

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 26, 27

## Question

How is the Rust Transpiler put together? Decide:
- The passes and what each hands to the next (parse to lossless tree, typed accessors, AST or not, validate, instance, emit), and whether the 1.0 preprocess pass survives now that comments are in the grammar (spec 02).
- The error model: all errors in one run, hints, one diagnostic format across passes, and how it maps to Monaco markers (`relatedInformation` or Hint markers). Our own diagnostic type or miette.
- The library surface the Visual Editor uses through WASM: parse, diagnostics, the tree view the graph needs, and the domain edit operations that return text edits per file (spec 22). Which data crosses the JS–WASM boundary, and in what shape.
- The crate split (core, CLI, WASM) and import resolution behind an interface, so the core does no file I/O (ADR 0010).

## Comments

- Graduated from the map's fog when [Bidirectional editing model](27-bidirectional-editing-model.md) resolved.
- Keep the handoff constraint in mind: the developer is new to Rust, so prefer fewer, simpler moving parts.
- Mid-session: explained the Model against the CST and AST (bytes, shape, meaning), how imports are found by parsing (parsing checks shape only, names are resolved later), and why miette was passed over (macro-heavy, terminal-first; a plain struct is easier to sort, serialize and test).

## Answer

Spec: `docs/spec/23-transpiler-architecture.md`. ADR 0012. Rule added to spec 01.

- **Passes:** lex, parse (lossless tree per file), typed accessors (they are the AST; no owned AST), Model build, validate, emit through a `Target` trait. No preprocess pass and no Target-neutral IR.
- **Model:** owned plain data, one per Program, names resolved across files, ids between items, an origin (file + range) on every item. Resolved but not desugared: each Target lowers sugar at emit. Rebuilt in full on every change (no salsa); best effort on broken code.
- **Parsing never depends on declarations** (spec 01), so each file parses alone and imports are found before names are resolved.
- **Files:** the core takes a file set (path → text) and Entry files, and walks `IMPORT` lines itself. The CLI gathers files from disk. In the Visual Editor every `.regin` is an Entry, and a `.regia` no Entry reaches is checked as its own Entry.
- **Diagnostics:** our own plain struct (severity, stable code, message, primary span, labels, hint), not miette; rendered by `annotate-snippets` in the CLI. All passes collect, none stop early; sorted and deduplicated; emit only with zero errors. Byte offsets in the core; 1-based line and UTF-16 column only in the WASM crate. Monaco: code to marker code with a docs link, labels to `relatedInformation`, hint appended as `help: …`. Quick fixes deferred.
- **Crates:** `regia-core` (`syntax`, `ast`, `model`, `validate`, `edit`, `diagnostics`, `targets/jason`; no I/O, no global state), `regia-cli` (`check`, `build`), `regia-wasm` (glue).
- **WASM surface:** a stateful Workspace (`setFile`, `removeFile`, `diagnostics`, `graph`, `edit`, `build`). Only serde data crosses, with TS types from `tsify`. Graph views are built from the Model. Edit operations are addressed by structural keys; a stale key or a broken construct returns a diagnostic.
- **Targets** return `(path, text)` files plus diagnostics; only the CLI writes to disk.
