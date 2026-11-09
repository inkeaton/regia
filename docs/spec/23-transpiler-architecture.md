# Transpiler architecture

How the Rust Transpiler is put together: its passes, what each one hands to the next, the error model, the crates, and the library surface the Visual Editor uses through WebAssembly. Decided in the ticket *Transpiler architecture* (`.scratch/regia-2/issues/29-transpiler-architecture.md`). It builds on ADR 0010 (Rust, hand-written parser), chapter 22 and ADR 0011 (text edits on a read-only tree), and chapter 10 (imports). ADR 0012.

The person writing the Transpiler is new to Rust, so every choice here prefers fewer, simpler moving parts.

## Passes

```
text ─lex─▶ tokens ─parse─▶ lossless tree ─(typed accessors)─▶ Model ─validate─▶ diagnostics
           (per file)       (per file)                         (per Program)
                                                                 └─emit (Target)─▶ output files
```

1. **Lex.** One file's text becomes tokens: whitespace and comments kept as tokens, INDENT/DEDENT from an indent stack (ADR 0010).
2. **Parse.** Tokens become a lossless tree (rowan, behind the core's `syntax` module, chapter 22), plus syntax diagnostics. Each file is parsed on its own. The parser always produces a tree, even for broken text.
3. **Typed accessors.** Hand-written typed wrappers over tree nodes (`Plot`, `WhenBlock`, `AssignStmt`, …), in the rust-analyzer style. They are the AST: **there is no separate owned AST.** They still describe one file, and only its shape: `AssignStmt::playbook()` gives the name `Brawling` as text, not the Playbook it means.
4. **Model build.** The accessors of every file in the Program become one **Model** (below). Imports, the flat namespace, kinds and parameter counts (ADR 0006), Role Mappings, precedence ranks (chapter 13) and Instancing are resolved here.
5. **Validate.** Checks that need the whole Program run on the Model and produce diagnostics.
6. **Emit.** A Target turns the Model into output files (below).

There is no preprocess pass. 1.0 merged files and stripped comments before parsing; in 2.0 comments are in the grammar (chapter 2) and imports are resolved from the parsed files (below). There is no Target-neutral intermediate form either: each Target reads the Model directly.

### Three views of the same code

| View | What it holds | Used for |
| --- | --- | --- |
| Lossless tree | Every byte: tokens, whitespace, comments, terminators. | Printing the file back, Extents, text edits (chapter 22). |
| Typed accessors | The tree's shape, typed, per file. Names are text. | Building the Model. |
| Model | The Program's meaning, across files, with names resolved. | Validate, emit, graph views, edit operations. |

## The Model

The Model is plain Rust data owned by the core, not a view onto the tree. Items link to each other by ids (`PlaybookId`, `RoleId`, …), and every item keeps an **origin**: its file and text range in the tree, which is how diagnostics and edit operations get back to the text.

```rust
Stmt::Assign {
    playbook: PlaybookId(7),          // the Brawling declared in brawling.regia
    role: RoleId(2),                  // Guest of RoyalBanquet
    mappings: [ /* implicit same-name Mappings filled in */ ],
    origin: (FileId(0), 112..136),
}
```

- **Resolved, not desugared.** The Model keeps the constructs the designer wrote: a Role setup stays a Role setup. What it adds is resolution: names point to their declarations, implicit Mappings are filled in, precedence ranks are computed. Turning sugar into Target mechanics (Role setup as Director messages, Quota counts as generated Facts) is each Target's job at emit, since Targets may lower differently (chapter 6's ASL notes).
- **Rebuilt in full** on every change, debounced, like the full reparse in chapter 22. There is no incremental engine (such as salsa). The development effort checks a performance budget together with the parse budget.
- **Best effort on broken code.** Constructs inside Error nodes are skipped, and the rest of the Model is still built, so the graph and the other diagnostics stay available while the user types.

## Parsing never depends on declarations

Every construct can be parsed from its tokens alone, without knowing what any name is declared as (chapter 1). That is what lets each file be parsed on its own and imports be found before any name is resolved.

## Files and imports

The core does no file I/O. It is given a **file set** (path → text) and the Entry files (chapter 10).

1. Parse each Entry file and read its `IMPORT` lines (strings in the tree).
2. Parse the imported files and read their imports, until nothing new turns up.
3. Build the Model from all of them.

An import that isn't in the file set, or an import cycle, is a diagnostic on the `IMPORT` line. How the file set is gathered belongs to the host:

- **CLI:** reads the Entry files named on the command line, then each import from disk, repeating until nothing new turns up, and hands the core the full set.
- **Visual Editor:** already holds every project file in memory and sets them all into the Workspace (below). Every `.regin` file in the project is an Entry file, and each is its own Program and build. A `.regia` file that no Entry reaches is checked as if it were its own Entry, so it still gets name errors while being written. Every file gets its syntax diagnostics either way.

## Diagnostics

One diagnostic type is shared by every pass. It is plain data, the core's own (not miette):

```rust
Diagnostic {
    severity,                       // Error, Warning, Info
    code,                           // stable, e.g. "R0412"; each code has a docs page
    message,
    primary: Span,                  // file + byte range
    labels: Vec<(Span, String)>,    // other places that explain the problem
    hint: Option<String>,           // how to fix it
}
```

- Every pass collects diagnostics and none stops early, so all problems come back from one run.
- Diagnostics are returned in one list, sorted by file and position. Duplicates and cascades from one broken construct are removed.
- **Emit runs only when there are no errors.** Warnings don't block it.
- The CLI renders diagnostics with `annotate-snippets` (rustc's renderer).

### Positions

Inside the core every position is a byte offset (rowan's `TextRange`): diagnostics, node spans in graph views, and text edits. Line and column numbers exist only at the edges, computed from a per-file line index:

- the WASM crate converts to Monaco's 1-based lines and UTF-16 columns;
- the CLI shows 1-based lines and character columns.

### Monaco markers

| Diagnostic | Monaco marker |
| --- | --- |
| `severity` | `MarkerSeverity.Error` / `Warning` / `Info` (`Hint` unused) |
| `code` | `code`, linking to the code's docs page |
| `message`, `hint` | `message`, with the hint appended after a blank line as `help: …` |
| `labels` | `relatedInformation` |

Quick fixes (text edits attached to a diagnostic, offered as code actions) are not part of 2.0's core.

## Targets

A Target is a Rust trait with one job: given the Model, return output files as `(relative path, text)` pairs, plus diagnostics (for example the warning for an unsupported Label, chapter 14). The core never writes files: the CLI writes them under its output folder, and the Visual Editor gets the same list from `build()`. The Target is chosen by Instancing (chapter 21). 2.0 has one Target, Jason.

## Crates

A Cargo workspace with three crates:

| Crate | Kind | Holds |
| --- | --- | --- |
| `regia-core` | library | Modules `syntax` (lexer, parser, rowan wrapper), `ast` (typed accessors), `model`, `validate`, `edit` (domain edit operations, chapter 22), `diagnostics`, `targets/jason`. No file I/O, no global state. |
| `regia-cli` | native binary | `regia check` and `regia build`; gathers files from disk, renders diagnostics, writes output files. |
| `regia-wasm` | WebAssembly library | wasm-bindgen glue only: the Workspace, conversions and serialization. |

More crates (a separate syntax crate, one per Target) are split out later only if compile times or reuse call for it.

## The Workspace (WASM surface)

The Visual Editor talks to one stateful **Workspace** object held in WASM:

| Call | Does |
| --- | --- |
| `setFile(path, text)` | Adds or replaces a file, reparses it and rebuilds the Model. |
| `removeFile(path)` | Removes a file. |
| `diagnostics()` | Current diagnostics, as Monaco markers per file. |
| `graph(plot)` | The graph view of one Plot. |
| `edit(operation)` | Text edits per file for one domain edit operation (chapter 22). |
| `build(entry)` | The Target's output files for one Entry file. |

- Only plain serializable data crosses the boundary (diagnostics, text edits, graph views, output files), through `serde` and `serde-wasm-bindgen`, with TypeScript types generated by `tsify`. Tree nodes and Model items never cross.
- **Graph views** are data made in Rust from the Model, carrying spans and structural keys (chapter 22). What they contain belongs to the open question of what the graph shows.
- **Edit operations are addressed by structural keys** (`RoyalBanquet/feast/WHEN insult_heard#0`), never by Model ids (they change on every rebuild) or byte offsets (the Visual Editor doesn't do text logic). The core resolves the key against the current Model, follows the origin to the tree node and its Extent, and computes the text edits. A key that no longer resolves, or a construct whose Extent contains an error, returns a diagnostic instead of edits.
