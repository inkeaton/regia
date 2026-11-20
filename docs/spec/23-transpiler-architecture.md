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

The core does no file I/O. It is given a **file set** (path → text) and one Entry file (chapter 10).

1. Parse the Entry file and read its `IMPORT` lines (strings in the tree).
2. Parse the imported files and read their imports, until nothing new turns up.
3. Build the Model from all of them.

An import that isn't in the file set, or an import cycle, is a diagnostic on the `IMPORT` line. How the file set is gathered belongs to the host:

- **CLI:** for each Entry file named on the command line, reads it, then each import from disk, repeating until nothing new turns up, and hands the core that set. Several Entry files are several Programs, checked one after the other.
- **Visual Editor:** already holds every project file in memory and sets them all into the Workspace (below). Every `.regin` file in the project is an Entry file, and each is its own Program and build. A `.regia` file that no Entry reaches is checked as its own Entry, with no Root Plot (chapter 21), so it still gets name errors while being written. Every file gets its syntax diagnostics either way.

## Diagnostics

One diagnostic type is shared by every pass. It is plain data, the core's own (not miette):

```rust
Diagnostic {
    severity,                       // Error, Warning
    code,                           // stable, e.g. "R0412"; each code has a docs page
    message,
    primary: Span,                  // file + byte range
    labels: Vec<(Span, String)>,    // other places that explain the problem
    hint: Option<String>,           // how to fix it
    fixes: Vec<Fix>,                // quick fixes: a title and the text edits that apply it
}
```

- **Two severities**: an error stops the Build, a warning doesn't. There is no third. What used to be a note is either a warning (something written has no effect) or a line of a report (the language doing what it says, such as a default left out, chapter 13).
- Codes follow chapter 27: `R`, the defining chapter's two digits, and the check's number in that chapter's `Transpiler checks` section. The severity is always printed beside the code (`warning[R1305]`), never read from it. The Conformance cases in `docs/spec/cases/` pin down which code each Program gets.
- Every pass collects diagnostics and none stops early, so all problems come back from one run.
- Diagnostics are returned in one list, sorted by file and position. Duplicates and cascades from one broken construct are removed.
- **Allowed warnings** (`#@allow`, chapter 02) are removed from the list after validation. The CLI's `--all-warnings` keeps them, marked *allowed*, and the Visual Editor shows them faded.
- **Emit runs only when there are no errors.** Warnings don't block it.
- The CLI renders diagnostics with `annotate-snippets` (rustc's renderer).

### Positions

Inside the core every position is a byte offset (rowan's `TextRange`): diagnostics, node spans in graph views, and text edits. Line and column numbers exist only at the edges, computed from a per-file line index:

- the WASM crate converts to **LSP positions**: 0-based lines and UTF-16 characters;
- the CLI shows 1-based lines and character columns.

### LSP shapes at the boundary

Everything the WASM crate hands out has the shape the Language Server Protocol uses, so a future language server for a VS Code extension can forward it unchanged (chapter 24). The Visual Editor converts to Monaco in TypeScript, adding 1 to lines and columns.

| Diagnostic | LSP `Diagnostic` | Monaco marker (in the Visual Editor) |
| --- | --- | --- |
| `severity` | `Error` / `Warning` (`Information` and `Hint` unused) | `MarkerSeverity.Error` / `Warning` (`Info` and `Hint` unused) |
| `code` | `code`, with `codeDescription` linking to the code's docs page | `code`, with the same link |
| `message`, `hint` | `message`, with the hint appended after a blank line as `help: …` | the same |
| `labels` | `relatedInformation` | `relatedInformation` |
| `fixes` | `CodeAction`s carrying a `WorkspaceEdit` | code actions |

Text edits are LSP `TextEdit`s grouped per file as a `WorkspaceEdit`. Semantic tokens use LSP's encoding, which Monaco shares. The CLI shows a fix only by its title, as a `help:` line.

## Targets

A Target is a Rust trait with two jobs:

- **check**: given the Model, return the Target's own diagnostics (`R1310`, `R1408`, chapter 36's port and name checks). It runs in validate, so `regia check` and `regia build` always report the same diagnostics, and a Program that passes `check` never fails to build with an error that was there all along.
- **emit**: given the Model, return output files as `(relative path, text)` pairs. It runs only when there are no errors and reports nothing of its own.

The core never writes files: the CLI writes them into the Build folder (below), and the Visual Editor gets the same list from `build()`. The Target is chosen on the command line (`--target`, default `jason`) or in the Visual Editor's project settings, and Instancing only configures it (chapter 21). 2.0 has one Target, Jason.

## The command line

```
regia check <entry>…                 Diagnostics for each Entry, Target checks included
regia build <entry>                  check, then write the Build
regia run <entry>                    build, then start it
regia test <case or folder>…         run Conformance-format cases of our own
regia explain <entry> precedence     the conflict report (chapter 13)
regia explain <entry> interface <Playbook or Plot>
                                     an Interface (chapter 38)
```

- **`check`** takes any number of Entry files, each its own Program (chapter 10). A `.regia` Entry is checked without a Root Plot (chapter 21).
- **`build`** and **`run`** take one `.regin` Entry. A `.regia` Entry is an error of the command line: a Build needs a `ROOT`.
- **`run`** starts the Build with the Target's runtime, which the CLI carries (for Jason: the MAS from the `.jcm`, with `regia-jason` on the class path, and every jar in the Project's `lib/` folder, chapter 35). The game connects as it always does. The writer never writes a class path.
- **`lib/`** is where a Project keeps the Target's own code (chapter 10), already built: jars, for Jason. `run` and `test` put them on the class path. The CLI never compiles them, never reads them in `check` or `build`, and never copies them into a Build.
- **`test`** runs cases in the format of chapter 27: check cases against their annotations, and behaviour cases against their `.trace` in test mode (chapter 35), with chapter 34's matching. It is how a writer keeps cases of their own, such as "the banquet reaches `farewell`". A folder is searched for cases.
- **`explain`** prints reports that aren't Diagnostics. `precedence` is chapter 13's conflict report, with full stops, unreachable candidates and defaults left out. `interface` is chapter 38's inferred Interface of one Playbook or Plot. Both work on a `.regia` Entry too, with what can be known without a Root Plot.

Options:

| Option | On | Does |
| --- | --- | --- |
| `--target <name>` | all | the Target; default `jason`. `--target none` skips the Target's checks. |
| `--seed <n>` | `run` | the run's seed. It beats the Build's `SEED`; with neither, the run picks one and the Trace records it (chapters 21, 34). |
| `--console all\|warnings\|off` | `run` | how much of the Trace the console shows (chapter 35); default `all`. The Trace file always gets everything. |
| `--deny-warnings` | `check`, `build`, `test` | a warning fails the command, for continuous integration. |
| `--all-warnings` | `check`, `build` | shows allowed warnings too, marked *allowed*. |
| `-q` | all | prints only Diagnostics. |

The exit status is 0 on success and 1 when an error (or, with `--deny-warnings`, a warning) was reported, or a case failed.

## The Build folder

A Build is written to **`build/<Entry path>/`**: the Entry's path relative to the current directory (the Project, in the Visual Editor), without its extension. `tests/test.regin` builds into `build/tests/test/`, so two `test.regin` files in different folders never share one.

- A build replaces everything in the Build folder **except `traces/`**, so files for renamed or removed Playbooks don't linger.
- `traces/` holds the Traces of past runs (chapter 35). Neither the CLI nor the Visual Editor ever clears it.

## Crates

A Cargo workspace with three crates:

| Crate | Kind | Holds |
| --- | --- | --- |
| `regia-core` | library | Modules `syntax` (lexer, parser, rowan wrapper), `ast` (typed accessors), `model`, `validate`, `edit` (domain edit operations, chapter 22), `diagnostics`, `targets/jason`. No file I/O, no global state. |
| `regia-cli` | native binary | The commands above; gathers files from disk, renders diagnostics, writes the Build folder, starts runs and matches cases. |
| `regia-wasm` | WebAssembly library | wasm-bindgen glue only: the Workspace, conversions and serialization. |

More crates (a separate syntax crate, one per Target) are split out later only if compile times or reuse call for it.

## The Workspace (WASM surface)

The Visual Editor talks to one stateful **Workspace** object held in WASM:

| Call | Does |
| --- | --- |
| `setFile(path, text)` | Adds or replaces a file, reparses it and rebuilds the Model. |
| `removeFile(path)` | Removes a file. |
| `setActiveEntry(entry)` | Sets the Active Entry (chapter 24): the Program whose meaning the calls below report for a file several Entries reach. |
| `entriesReaching(path)` | The `.regin` Entry files whose Program holds a file. |
| `diagnostics()` | Current diagnostics per file, in LSP shape. |
| `semanticTokens(path)` | Semantic tokens for one file: each name coloured by what it resolves to (chapter 24). |
| `graph(plot)` | The graph view of one Plot. |
| `docs(path)` | The Docs page data of one file: its Plots, Playbooks and Vocabulary with their doc comments and Interfaces (chapter 25). |
| `preview(operation)` | What an edit operation would do, before it is applied: for `rename`, the references, doc comments, file and name-order flips; for deleting a Phase, the Plans removed and the references left broken (chapter 25). |
| `edit(operation)` | Text edits per file for one domain edit operation (chapter 22), including `moveFile(from, to)`, which rewrites every `IMPORT` affected by renaming or moving a file (chapter 24). |
| `build(entry)` | The Target's output files for one `.regin` Entry file. |
| `report(entry, kind)` | The conflict report or an Interface, as `regia explain` prints it. |

- Only plain serializable data crosses the boundary (diagnostics, semantic tokens, text edits, graph views, output files), through `serde` and `serde-wasm-bindgen`, with TypeScript types generated by `tsify`. Tree nodes and Model items never cross.
- **Graph views** are data made in Rust from the Model, carrying spans and structural keys (chapter 22). What they contain (a Plot's Phases, Roles and Plans with their effects, plus where each name comes from) is in chapter 25.
- **Edit operations are addressed by structural keys** (`RoyalBanquet/feast/WHEN insult_heard#0`), never by Model ids (they change on every rebuild) or byte offsets (the Visual Editor doesn't do text logic). The core resolves the key against the current Model, follows the origin to the tree node and its Extent, and computes the text edits. A key that no longer resolves, or a construct whose Extent contains an error, returns a diagnostic instead of edits.

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025), the command line and the Build folder included. The command line, the two severities and the Build folder were decided in the ticket *The command line, Programs and Diagnostics* (`.scratch/regia-revision/issues/16-command-line-and-diagnostics.md`).

A Transpiler build has one version. `regia --version` prints it, and no option picks 1.5 or 2.0: a 1.5 Program is valid in 2.0, so a 2.0 build needs no 1.5 mode. A 1.5 build reports `R0109` for what is later (chapter 01). `regia test` runs only the cases whose `regia:` line fits its version (chapter 27). Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).
