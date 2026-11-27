# Transpiler architecture

How the Rust Transpiler is put together: its passes, what each one hands to the next, the error model, the crates, and the library surface the Visual Editor uses through WebAssembly. Decided in the ticket *Transpiler architecture* (`.scratch/regia-2/issues/29-transpiler-architecture.md`). It builds on ADR 0010 (Rust, hand-written parser), chapter 22 and ADR 0011 (text edits on a read-only tree), and chapter 10 (imports). ADR 0012.

The person writing the Transpiler is new to Rust, so every choice here prefers fewer, simpler moving parts.

## Passes

```
text ─lex─▶ tokens ─parse─▶ lossless tree ─(typed accessors)─▶ Model ─validate─▶ diagnostics
           (per file)       (per file)                         (per Program)
                                                                 └─emit (Target)─▶ output files
```

1. **Lex.** One file's text becomes tokens, plus lexical diagnostics: whitespace and comments kept as tokens, INDENT/DEDENT from an indent stack (ADR 0010). It is two functions, *scan* and *layout* (below).
2. **Parse.** Tokens become a lossless tree (rowan, behind the core's `syntax` module, chapter 22), plus syntax diagnostics. It is the *parser* and then the *tree builder* (below). Each file is parsed on its own. The parser always produces a tree, even for broken text.
3. **Typed accessors.** Hand-written typed wrappers over tree nodes (`Plot`, `WhenBlock`, `AssignStmt`, …), in the rust-analyzer style. They are the AST: **there is no separate owned AST.** They still describe one file, and only its shape: `AssignStmt::playbook()` gives the name `Brawling` as text, not the Playbook it means.
4. **Model build.** The accessors of every file in the Program become one **Model** (below). Imports, the flat namespace, kinds and parameter counts (ADR 0006), Role Mappings, precedence ranks (chapter 13) and Instancing are resolved here, with diagnostics for what can't enter the Model as written.
5. **Validate.** Checks on what the built Model means run on it and produce diagnostics: one Plan's flow, absence checks, the whole Program, the Target's own checks.
6. **Emit.** A Target turns the Model into output files (below).

There is no preprocess pass. 1.0 merged files and stripped comments before parsing; in 2.0 comments are in the grammar (chapter 2) and imports are resolved from the parsed files (below). There is no Target-neutral intermediate form either: each Target reads the Model directly.

### What the lexer hands to the parser

- **`scan`** turns text into raw tokens, knowing nothing about lines. **`layout`** turns raw tokens into final ones: it joins continuation lines and adds NEWLINE, INDENT and DEDENT. The parser sees only `layout`'s output.
- **NEWLINE** is the line break that ends a logical line. Breaks in continuation lines, on blank lines and on comment-only lines are whitespace, and those inside a multiline comment are part of its token. At the end of a file without a final break, NEWLINE is zero-width.
- **INDENT and DEDENT** follow code lines only, and always balance: a deeper line is an INDENT whether or not a header came before it, and the end of the file closes every level. Where they fall around comments is in chapter 22.
- **`:`, `.` and `;`** are plain tokens, and the parser makes structure of them. After a header's `:`, NEWLINE INDENT is an indentation Block, NEWLINE alone an empty one, and anything else an Inline block that ends at `;` or before NEWLINE.
- **`.`** ending a Statement is its own kind (STOP), told apart in `scan` by the character after it. A dotted name is one token.
- **A Placeholder** is one token, the `?` included. **A `-`** is always a token of its own, which the parser joins to a number where a Value starts.
- **Every reserved word** has a kind of its own, with the 2.0, later and retired words included. Context never decides whether a word is a keyword.
- **Diagnostics** come back as a list beside the tokens. The lexer reports `R01_03-mixed-tabs-and-spaces`, `R01_04-dedent-to-unopened-level`, `R01_05-continuation-not-indented`, `R01_12-stray-character`, `R01_13-malformed-string`, `R02_01-unclosed-comment`, `R02_02-doc-comment-mid-line` and `R04_01-unsupported-number-form`; everything else about a file's syntax is the parser's, `R01_01-indented-body-after-inline`, `R01_02-keyword-in-dotted-name`, `R01_06-block-without-body`, `R01_08-stray-semicolon`, `R01_14-indent-opens-no-block` and `R01_15-unexpected-text` included.
- **Malformed text keeps the kind it was meant to have:** an unclosed String is a String up to the end of its line, an unclosed comment a comment up to the end of the file, `0xFF` a number. A stray character is an ERROR token, which the parser steps over silently. So no mistake is reported by both, and printing every token gives back the source.

For example, with whitespace left out:

```text
WHEN food_served:                 WHEN NAME COLON NEWLINE
    IF is_hungry: DO eat_food     INDENT IF NAME COLON DO NAME NEWLINE
    # TODO: a retort              COMMENT
                                  DEDENT
# --- eating ---                  COMMENT
WHEN idle:                        WHEN NAME COLON NEWLINE
```

### From tokens to the tree

- **The parser** writes a flat list of events: open a node, take a token, close a node. It sees neither whitespace nor comments. Wrapping a node already finished (`1 + 2`) is an edit to the list.
- **The tree builder** turns the events and the full token list into the tree. It alone applies the Extent rules (chapter 22) and it alone builds rowan nodes. It drops zero-width tokens: INDENT, DEDENT and an end-of-file NEWLINE are never in the tree.
- **The grammar is loose about places.** Any declaration, Plan or Statement parses in any ordinary body, whatever the file's extension, and a later check reports one that is misplaced. Only bodies whose lines start with a name have a grammar of their own, chosen by the header: `PRECEDENCE`, `KIND`, `AGENT` and `TARGET`.
- **A soft error** is reported and nothing is skipped: a missing `,` (`R01_11-clause-without-comma`), `)`, or `:` before NEWLINE INDENT, or a keyword used as a name (`R01_10-keyword-as-name`). Nothing stands in the tree for what is missing.
- **A hard error** puts the unexpected tokens in one Error node, up to the first STOP, SEMI, NEWLINE, INDENT, DEDENT or end of file, or a token the current rule was waiting for (`:` in a header, `,` or `)` in arguments). A Statement keyword doesn't end it, since `TO` also appears inside Statements. A Statement or a header has at most one, and a broken header keeps its body.
- **A retired spelling** is reported with its code and becomes the same node as the new spelling, so nothing cascades: `CHANGE f TO f2` is an `UPDATE_STMT` whose first token is `CHANGE`. One with no counterpart is an Error node with the retired code.
- **A 2.0 construct** is parsed in full into ordinary nodes. The parser reports `R01_09-later-regia-construct` where the tokens show it. A Goal's ending in a Plot needs the name's kind (`WHEN take_seat ENDED:` and `WHEN HonorDuel ENDED:` have the same tokens), so Model build reports that one. The enclosing Plan or Statement is left out of the Model, so it gets no other diagnostic (*From files to the Model*). Which version this build is, is tested in one function.
- **`parse(text)`** returns a `Parse`: the root, and the diagnostics. `syntax` wraps rowan in its own newtypes, with only the methods the core needs, and nothing stores a tree node: the Model keeps a file and a range. So it doesn't matter that rowan's nodes can't be shared between threads.

**Accessors** return an `Option` for one part and an iterator for several. `None` means that the part isn't there, whether it is optional or was lost to an error; an accessor doesn't look inside Error nodes, invents nothing, never panics and reports nothing. A name is returned as its token, so its text and range go together.

For example, with whitespace left out:

```text
PLAYBOOK Guest:
    # Reacts to rudeness         PLAN
    WHEN insulted, FROM ?who:      COMMENT
                                   TRIGGER      WHEN NAME_REF
                                   FROM_CLAUSE  COMMA FROM PLACEHOLDER
                                   COLON NEWLINE
                                   BLOCK
        DO ) scowl   # broken        DO_STMT    DO ERROR[CLOSE_PAREN NAME] COMMENT NEWLINE
        DO laugh                     DO_STMT    DO NAME_REF NEWLINE
```

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

### From files to the Model

One function takes the parsed file set and an Entry, and returns the Model and its diagnostics. A file's parse is kept and shared by every Program that reaches it. A Model belongs to one Entry.

**Steps.** Each finishes before the next starts:

1. **Reach.** Follow the imports, giving each file the set of files it can see.
2. **Collect.** Give every declaration its id: names, kinds, parameter counts, Roles, Phases and Local Vocabulary. No Plan is visited.
3. **Resolve.** Visit the bodies and turn names into ids. Implicit Mappings are filled in here, since every Role is known. A Plan's Trigger is resolved before its Body.
4. **Whole Program.** Instancing overrides and the Root Plot, then precedence ranks.

**Ids and names**

- There is one list per sort of item, and an id is a position in it. `RoleId` is Program-wide, and a Role records its owner, a Plot or a Playbook.
- There is one name table per Program, and one per owner for local names. A lookup finds the item, then checks that the file reaches one of its declaring files. An item found but not reached is `R10_04-name-out-of-scope` with its hint.
- An item declared several times has a list of origins, in file order: the Entry, then its imports depth-first as written.
- After an `R05_01-declared-as-two-kinds` or an `R10_05-conflicting-redeclaration` the first declaration keeps the name and the item is marked *conflicted*: checks that read what may conflict (kind, parameter count, External name, `GAME`) skip it. After an `R10_06-duplicate-playbook-or-plot` the second Playbook or Plot has an id of its own, so that its body is checked, and the name leads to the first.

**Faulty imports.** A misplaced import (`R10_01-misplaced-import`) and one in a cycle (`R10_03-import-cycle`) are followed. A `.regia` importing a `.regin` (`R21_01-import-of-instancing-file`) is not, and isn't missing either, since a `.regin` declares no names a `.regia` could use. An import that leads to no file (`R10_02-missing-import-file`) or has no readable path is a **missing import**.

**What is kept of broken code**

- **A reference is an `Option`, and `None` means that a diagnostic was already reported.** A name that leads nowhere, or to the wrong kind, is `None`, and the rest of its Statement is still checked. A check that needs the missing part steps over it. Emit never meets a `None`, since it runs only without errors.
- **A Statement** missing a part it can't mean anything without is left out, and its neighbours stay.
- **A Plan** whose Trigger is missing or broken is left out with its body. A broken Statement doesn't remove its Plan.
- **A Playbook, Plot, Role or Phase** with a readable name is always kept. One without a name is left out, contents included.
- **A refused Goal's ending in a Plot** (`R01_09-later-regia-construct`): once the Trigger resolves to a Goal, the Plan is left out and its body is never visited.

**Absence checks.** An absence check reports that nothing in some scope, a Plan, a Playbook or Plot, or the Program, does something: nothing declares a name (`R10_04-name-out-of-scope`), nothing fills a Placeholder (`R03_04-unfilled-placeholder`), nothing sends a Cue (`R38_07-cue-never-sent`), nothing uses a Placeholder (`R03_07-unused-placeholder`). Adding the missing thing anywhere in that scope would make it go away. A check that a Statement or Plan can never run because of what is written above it (`R11_02-statement-after-fail`, `R13_07-unreachable-trigger-block`) is not one: all it reads is there. It is silent when what it looks for may be in text that wasn't read, so that one mistake gives one report:

- The Model keeps the **unread names**: every name and Placeholder written in an Error node or in a left-out construct, as text, compared ignoring case. An absence check skips a name in that set, and a Placeholder only within its own Plan.
- A file that reaches a missing import gets no `R10_04-name-out-of-scope` for a file-level name. A name that is always local, such as a Plot's Role or Phase, is still reported. Absence checks over the whole Program don't run.

The absence checks are a closed list. Each is marked in its own chapter:

| Scope | Checks |
| --- | --- |
| Plan | `R03_04-unfilled-placeholder` (its *never filled* part), `R03_07-unused-placeholder`, `R03_08-placeholder-only-under-not` |
| Playbook or Plot | `R05_08-by-for-unasked-goal`, `R13_03-relation-to-absent-item` (its *never* parts), `R13_06-relation-without-shared-trigger`, `R14_09-unused-propensity`, `R17_04-subplot-never-started`, `R17_05-ignored-end-plot-with`, `R17_06-unknown-subplot-outcome`, `R17_08-unheard-subplot-ending`, `R17_12-subplot-never-dropped`, `R17_13-unheard-until-exited-ending`, `R19_05-joined-outside-root-plot`, `R20_11-unreachable-phase`, `R20_12-goal-never-asked`, `R20_15-ignored-exited-by-parent`, `R38_01-unheard-signal`, `R38_02-cue-never-signalled`, `R38_03-unheard-message` |
| Program | `R02_05-stale-allow`, `R10_04-name-out-of-scope`, `R21_10-root-role-never-played`, `R21_12-plot-never-reached`, `R21_17-agent-plays-nothing`, `R21_21-undeclared-name-after-no`, `R38_04-reason-never-given`, `R38_05-pursue-without-me-recipe`, `R38_06-ask-only-me-recipes`, `R38_07-cue-never-sent` |

For example, with no `lost.regia`:

```text
hub.regia     IMPORT "scene"           reaches scene, moves, and a missing import
              IMPORT "lost"            R10_02-missing-import-file

scene.regia   IMPORT "moves"           reaches moves only
              DO wave                  silent: `wave` is an unread name
              DO curtsy                R10_04-name-out-of-scope: this file reaches no missing import
              DO nod                   DO_STMT with Some(nod)

moves.regia   ACTION ) wave            a syntax error; `wave` is unread
              ACTION nod
```

**A `.regia` Entry** is built by the same code. The Root Plot is an `Option`, `None` here: there is no cast and no ranking across Plots, while each Plot's own `PRECEDENCE` relations are kept. Checks that need a Root Plot step over the `None`. A `.regin` Entry whose `ROOT` is missing or bad (`R21_04-missing-or-wrong-root`) has the same `None`, so nothing cascades. The Model records the Entry's extension, since only a `.regin` owes a `ROOT`.

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
    code,                           // the whole code, e.g. "R13_01-precedence-cycle"; each code has a docs page
    message,
    primary: Span,                  // file + byte range
    labels: Vec<(Span, String)>,    // other places that explain the problem
    hint: Option<String>,           // how to fix it
    fixes: Vec<Fix>,                // quick fixes: a title and the text edits that apply it
}
```

### Where a check lives

A check belongs to the first pass that has everything it reads:

| Pass | Reads | Reports |
| --- | --- | --- |
| Lex | the characters of one line | the codes listed under *What the lexer hands to the parser* |
| Parse | the tokens of one construct, not where it sits | grammar errors, retired spellings, `R01_09-later-regia-construct` where the tokens show it, `R02_03-detached-doc-comment` and `R02_04-allow-names-error` on the finished tree |
| Model build | where a construct sits, and what its names mean | what can't enter the Model as written: a misplaced construct (`R15_08-misused-assigned-or-removed`, `R17_14-running-in-playbook`, `R03_09-me-in-plot`), a name that leads nowhere or to the wrong kind or count (`R10_04-name-out-of-scope`, `R03_01-wrong-argument-count`), duplicates (`R10_05-conflicting-redeclaration`), import faults, a precedence cycle (`R13_01-precedence-cycle`, since ranks can't be computed), the late `R01_09-later-regia-construct`, `R21_04-missing-or-wrong-root` |
| Validate | the built Model | everything else: flow (`R03_04-unfilled-placeholder`, `R17_02-statement-after-end-plot`), absence checks (`R03_07-unused-placeholder`, `R38_07-cue-never-sent`), the whole Program, the Target's checks |

A construct Model build reports is left out, and its names become unread (*From files to the Model*). So a check that "needs only one Plan", such as `R03_07-unused-placeholder`, still runs in Validate.

**Passes hand diagnostics over as return values.** `parse` returns them in its `Parse`, Model build beside the Model, `validate` as its result. One function, `check`, gathers them, applies allows, removes exact duplicates and sorts.

**The code** is a Rust enum with one variant per code. The enum alone gives each code's number, Code name and severity, so a check can't report a warning's code as an error, or print a name that isn't its number's. A message takes arguments and is written where the check reports. A test compares the enum with every chapter's *Transpiler checks*.

- **Two severities**: an error stops the Build, a warning doesn't. There is no third. What used to be a note is either a warning (something written has no effect) or a line of a report (the language doing what it says, such as a default left out, chapter 13).
- Codes follow chapter 27: `R`, the number (the defining chapter's two digits, `_`, the check's number in that chapter's `Transpiler checks` section), then `-` and the Code name. A code is printed whole, and the severity is always printed beside it (`warning[R13_05-competition-ordered-by-name]`), never read from it. The Conformance cases in `docs/spec/cases/` pin down which code each Program gets.
- Every pass collects diagnostics and none stops early, so all problems come back from one run.
- Diagnostics are returned in one list, sorted by file and position. Exact duplicates (same code, same primary span) are removed.
- **Cascades are prevented where they would start, never filtered afterwards**: a stray character is stepped over by the parser, a reference that leads nowhere is `None`, a broken construct is left out and its names are unread, a conflicted item is skipped. A Conformance case that shows a cascade is a bug in the check that made it.
- **Allowed warnings** (`#@allow`, chapter 02). Each `Parse` carries its file's allow scopes: the range of the declaration, and each code with where it is written. After validation, `check` marks a warning *allowed* when its primary span lies in a scope naming its code. The CLI hides allowed warnings unless `--all-warnings` is given, the Visual Editor shows them faded, and Conformance cases match them (chapter 27). `R02_05-stale-allow` is reported only when the Program has no errors, since an error can silence the warning an allow was written for.
- **Emit runs only when there are no errors.** Warnings don't block it.
- The CLI renders diagnostics with `annotate-snippets` (rustc's renderer).

### Positions

Inside the core every position is a byte offset (rowan's `TextRange`): diagnostics, node spans in graph views, and text edits. Line and column numbers exist only at the edges, computed from a per-file line index:

- the WASM crate converts to **LSP positions**: 0-based lines and UTF-16 characters;
- the CLI shows 1-based lines and character columns;
- a Target's source map (chapter 35) writes 1-based lines and character columns, as the CLI shows them.

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

- **check**: given the Model, return the Target's own diagnostics (`R13_10-suits-without-selection-function`, `R14_08-unsupported-label`, chapter 36's port and name checks). It runs in validate, so `regia check` and `regia build` always report the same diagnostics, and a Program that passes `check` never fails to build with an error that was there all along.
- **emit**: given the Model, return output files as `(relative path, text)` pairs. It runs only when there are no errors and reports nothing of its own.

The core never writes files: the CLI writes them into the Build folder (below), and the Visual Editor gets the same list from `build()`. The Target is chosen on the command line (`--target`, default `jason`) or in the Visual Editor's project settings, and Instancing only configures it (chapter 21). 2.0 has one Target, Jason.

```rust
trait Target {
    fn check(&self, model: &Model) -> Vec<Diagnostic>;
    fn emit(&self, model: &Model) -> Vec<OutputFile>;   // OutputFile { path, text }
}
```

- **One Model in, no options.** Whether the Build has a Root Plot is read from the Model, not passed in. `--target none` is no Target at all, an `Option`, not a Target that does nothing.
- **Emit can't fail.** It returns no `Result` and no Diagnostics. A `None` reference or a broken invariant met while emitting is a Transpiler bug, since `check` reported it or it can't happen, so emit panics with an `expect` naming the check. Anything that could stop a Build is a Target check instead. The case runner emits every case with no errors, so a check that misses something shows up as a failed case, not as a bad Build.
- **Same bytes every time.** Output files are sorted by path, Plans are emitted in source order within their owner, and the maps of a generated JSON file are sorted by key.

### How the Jason Target emits

Worked by hand on `courtesy.regia` in the ticket *Review: Model to Target*.

1. **The Program-wide tables.** One walk over the Model fills one struct with what crosses files: the Playbooks each Role file includes (chapter 29), the Goals for `goals.asl` (chapter 40), the told Cues for `unheard.asl` (chapter 39), the game items each top-level file needs (chapter 28). They belong to the Jason Target, not the Model, since lowering is each Target's (ADR 0012).
2. **The file writers.** Each output file has its writer, which reads the Model and the tables and nothing else. What is local to one file is computed there: a Plan's rank `Pos` (chapter 32) is its place among the same Playbook's Plans for the same Item, counted going down the file. So adding a Role to a Plot changes the tables and the Role files, and leaves `Serving.asl` as it was.
3. **The source map** (chapter 35) is written last, from what each writer recorded.

**A plan is a small struct, not an ASL tree.** Several chapters contribute to one plan: its label (chapter 28), its annotation (chapter 32), its trigger (chapters 39, 40), the conjuncts of its context (the Givings guard of chapter 29, the Sender test and the designer's Context of chapter 39) and its body steps. The writer gathers them in an `AslPlan` (label, annotations, trigger, context conjuncts, body steps) and prints it in one place. Terms and formulas are written straight to text: nothing reads the ASL back, and snapshots compare text.

**Variables.** Every term is written under a `Vars`, one per plan: each Placeholder's Jason variable (chapter 39) and a counter per kind of generated variable (`Regia_each__N`). A Context written again under other names, as in the negated `GIVEN` siblings of chapter 39, is written under a copy of the `Vars` with some entries renamed. A generated variable is never written by hand: a `.setof` over `A` would join a Placeholder `?a`.

**Lines for the source map.** An ASL writer counts the lines it writes. Each plan and each Statement records its ASL line with its origin as it is written. Each file writer returns its text and those records, and the source map turns each origin into a line and column through the file's line index (*Positions*).

**A `.regia` Entry** goes through the same steps: the tables read that the Model has no Root Plot, and the writers leave out what chapter 28's *A Build of a `.regia` Entry* leaves out.

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
- **`build`** takes one Entry. A `.regia` Entry gives Target code only, with no Root Plot and no cast (chapter 21, *A `.regia` Entry*, ADR 0049).
- **`run`** takes one `.regin` Entry. A `.regia` Entry is an error of the command line: a run needs a `ROOT`.
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

A Build is written to **`build/<Entry path>/`**: the Entry's path relative to the current directory (the Project, in the Visual Editor), without the `.regin` extension. `tests/test.regin` builds into `build/tests/test/`, so two `test.regin` files in different folders never share one. A `.regia` Entry keeps its extension, so `banquet.regia` builds into `build/banquet.regia/` and never shares a folder with `banquet.regin`.

- A build replaces everything in the Build folder **except `traces/`**, so files for renamed or removed Playbooks don't linger.
- `traces/` holds the Traces of past runs (chapter 35). Neither the CLI nor the Visual Editor ever clears it.

## Crates

A Cargo workspace with three crates:

| Crate | Kind | Holds |
| --- | --- | --- |
| `regia-core` | library | Modules `syntax` (lexer, parser, rowan wrapper), `ast` (typed accessors), `model`, `validate`, `edit` (domain edit operations, chapter 22), `diagnostics`, `targets/jason`. No file I/O, no global state. |
| `regia-cli` | native binary, with a library target | The commands above; gathers files from disk, renders diagnostics, writes the Build folder, starts runs. Its library holds the case runner (*Tests*, below). |
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
| `diagnostics()` | Current diagnostics per file, in LSP shape: for a file several Programs reach, the union of theirs with exact duplicates removed. |
| `semanticTokens(path)` | Semantic tokens for one file: each name coloured by what it resolves to (chapter 24). |
| `graph(plot)` | The graph view of one Plot. |
| `docs(path)` | The Docs page data of one file: its Plots, Playbooks and Vocabulary with their doc comments and Interfaces (chapter 25). |
| `preview(operation)` | What an edit operation would do, before it is applied: for `rename`, the references, doc comments, file and name-order flips; for deleting a Phase, the Plans removed and the references left broken (chapter 25). |
| `edit(operation)` | Text edits per file for one domain edit operation (chapter 22), including `moveFile(from, to)`, which rewrites every `IMPORT` affected by renaming or moving a file (chapter 24). |
| `build(entry)` | The Target's output files for one Entry file, `.regin` or `.regia`. |
| `report(entry, kind)` | The conflict report or an Interface, as `regia explain` prints it. |

- Only plain serializable data crosses the boundary (diagnostics, semantic tokens, text edits, graph views, output files), through `serde` and `serde-wasm-bindgen`, with TypeScript types generated by `tsify`. Tree nodes and Model items never cross.
- **Graph views** are data made in Rust from the Model, carrying spans and structural keys (chapter 22). What they contain (a Plot's Phases, Roles and Plans with their effects, plus where each name comes from) is in chapter 25.
- **Edit operations are addressed by structural keys** (`RoyalBanquet/feast/WHEN insult_heard#0`), never by Model ids (they change on every rebuild) or byte offsets (the Visual Editor doesn't do text logic). The core resolves the key against the current Model, follows the origin to the tree node and its Extent, and computes the text edits. A key that no longer resolves, or a construct whose Extent contains an error, returns a diagnostic instead of edits.

## Tests

Each pass is tested in the form that shows its output best:

| Pass | Tests |
|---|---|
| scan, layout | unit tests on short text; snapshots of a token dump; print-back over every showcase and case file |
| parser, tree builder | snapshots of a tree dump; print-back of the tree |
| `ast` | unit tests |
| Model, Validate, Target checks | Conformance check cases (chapter 27) only |
| emit | ASL snapshots; a `#[should_panic]` test on a hand-built Model |
| command line | integration tests that run the binary: exit status, options, the Build folder |

- **Dumps** are functions of the core that tests call: one token per line with its kind, range and text (virtual tokens with empty text), and rowan's indented `KIND@start..end` tree. The command line has no dump command.
- **Snapshots** use `insta`: inline for short dumps, files for ASL. ASL snapshots aren't Conformance cases (chapter 27).
- **The case runner** is the `cases` module of `regia-cli`'s library. It finds cases, reads their annotations and matches them against the Diagnostics the core returns. `regia test` calls it, and so does `regia-cli/tests/conformance.rs`, which runs every case in `docs/spec/cases/` in place under `cargo test`. It isn't in `regia-core` because it reads files, and only the command line runs cases.
- **The pending list**, `regia-cli/tests/pending.txt`, names the cases the Transpiler doesn't pass yet, one path per line relative to `docs/spec/cases/`. A listed case that fails is pending and doesn't fail the run. A listed case that passes fails it ("remove from pending"), and so does a listed path that doesn't exist. A case that isn't listed must pass. Folders are never listed, so a new case can't hide in one. On failure the runner prints the failing paths in the list's form.
- **What runs.** A 1.5 build skips `regia: 2.0` cases and counts them. A behaviour case's Entry is checked against its annotations; its Trace is reported as skipped until the Target's runtime exists.
- **Accepting cases** need no guard against passing while a check is missing. An `ok` case fails while the parser doesn't know its constructs, then guards against false positives; the check's error case, red first, is what proves the check exists. A rule lands with both.
- **Codes.** `regia-core/tests/codes.rs` reads every chapter's `## Transpiler checks` section and checks that its codes, retired ones included, match `enum Code`.
- **WebAssembly.** `cargo build -p regia-core --target wasm32-unknown-unknown` is one of the standing checks once the core depends on rowan.

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025), the command line and the Build folder included. *What the lexer hands to the parser* was decided in the ticket *Review: text to tokens* (`.scratch/transpiler/issues/01-text-to-tokens.md`), *From tokens to the tree* in *Review: tokens to tree to accessors* (`.scratch/transpiler/issues/02-tokens-to-tree.md`), *From files to the Model* in *Review: files to Model* (`.scratch/transpiler/issues/03-files-to-model.md`), *Where a check lives*, cascades and allows in *Review: Diagnostics and where checks live* (`.scratch/transpiler/issues/04-diagnostics.md`), the `Target` trait and *How the Jason Target emits* in *Review: Model to Target* (`.scratch/transpiler/issues/05-model-to-target.md`), and *Tests* in *Review: how we test* (`.scratch/transpiler/issues/06-how-we-test.md`). The command line, the two severities and the Build folder were decided in the ticket *The command line, Programs and Diagnostics* (`.scratch/regia-revision/issues/16-command-line-and-diagnostics.md`).

A Transpiler build has one version. `regia --version` prints it, and no option picks 1.5 or 2.0: a 1.5 Program is valid in 2.0, so a 2.0 build needs no 1.5 mode. A 1.5 build reports `R01_09-later-regia-construct` for what is later (chapter 01). `regia test` runs only the cases whose `regia:` line fits its version (chapter 27). Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).
