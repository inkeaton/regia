# Map: The Regia 1.5 Transpiler

Label: wayfinder:map

## Destination

A Regia 1.5 Transpiler in `transpiler/` that runs `check`, `build`, `explain`, and `test` for check cases, built by the user as a way of learning Rust. The architecture of chapter 23 is first revised together, so that it is clear before it is built.

Charted with the user on 2026-11-25.

## Notes

- **This map carries execution.** Decision tickets and build tickets share one numbering and one frontier (open, unblocked, unclaimed, lowest number first). Tickets are cut **one milestone ahead**; later milestones stay below as fog.
- **Types.** Decisions: `grilling`, `prototype`, `research`, `task`. Build: `implementation`, and `exercise` for a drill large enough for its own ticket.
- **Size.** A build ticket is one sitting of 1–3 hours, with at most one new Rust concept and one construct, check or rule. Its sections are *Goal*, *Spec*, *Rust*, *Test first*, *Done when*, *Not here*.
- **Testable.** A build ticket closes on one named test, red first, plus something visible when run: token dumps (lexer), tree dumps and "prints back the same bytes" (parser), Conformance cases (Model, Validate), ASL snapshots (emit).
- **Closing** needs the checks of `CLAUDE.md` step 5, a review against `CODING_STANDARDS.md`, the 2–3 understanding questions, and the `docs/.dev/LEARNING_LOG.md` entry. The user writes the Rust (`docs/.dev/CLAUDE.md`) and decides when to commit.
- **Review tickets** work one concrete example by hand. The user explains the boundary back at the end. What changes goes into chapter 23.
- **Emit is judged** against ASL taken by hand from the chapter's own example before the code. Accepted risk: no emitted ASL is executed until the `regia-jason` effort.
- Skills: `grilling` and `domain-modeling` for grilling tickets; `tdd` and the `rust-*` skills for build tickets.
- `.scratch/implementation/continuous-integration.md` can be taken up once M0 is done.
- The ticket that adds rowan also adds the `wasm32-unknown-unknown` build of `regia-core` to the step 5 checks and CI (*Review: how we test*).

## Milestones

| # | Milestone | You can see | State |
|---|---|---|---|
| M0 | Workspace and CLI printing a file | `regia` echoes a file | cut: tickets 08–11 |
| M1 | Lexer, then its move into `regia-core` | a token dump of the showcase, printed back byte for byte | cut: tickets 14–34 |
| M2 | Thin path: `CUE`, `ACTION`, `PLAYBOOK`, `WHEN`, `DO` through every pass | one name error; `regia build` on a one-Playbook `.regia` file (ADR 0049) writes its `.asl` | cut by ticket 35 |
| M3 | Case runner and pending list | check cases run under `cargo test` | fog |
| M4 | Whole parser, 2.0 constructs included | every showcase file parses; `R0109` | fog |
| M5 | Files, imports and names in the Model | `regia check` finds unresolved names | fog |
| M6 | Checks, chapter by chapter | the pending list empties | fog |
| M7 | Emit, chapters 28–40, and the whole `regia build` | a full Build of the banquet | fog |
| M8 | `explain`, `test`, command line options | chapter 23's CLI, minus `run` | fog |
| M9 | Measure and optimize | a benchmark report | fog |

## Decisions so far

<!-- one line per resolved ticket: [title](issues/NN-slug.md): gist -->

- [Review: text to tokens](issues/01-text-to-tokens.md): lex is `scan` then `layout`; `layout` owns lines and indentation, the parser owns `:`, `.` and `;`; columns place comments; `R0112`–`R0115` added.
- [Review: tokens to tree to accessors](issues/02-tokens-to-tree.md): the parser writes events, the tree builder owns comments and rowan; soft and hard errors; `Option` accessors; rowan runs in WebAssembly.
- [Review: files to Model](issues/03-files-to-model.md): reach, collect, resolve, whole Program; a reference is an `Option`, `None` already reported; absence checks are silent about what wasn't read.
- [Review: Diagnostics and where checks live](issues/04-diagnostics.md): a check lives in the first pass with all it reads; return values into one `check`; cascades prevented, not filtered; allows marked, `R0205` only without errors; `enum Code`; 30 absence checks listed.
- [Review: Model to Target](issues/05-model-to-target.md): `Target` with `check` and `emit(&Model) -> Vec<OutputFile>`; Jason emit is Program-wide tables, then one writer per file, then the source map; an `AslPlan` struct and text under `Vars`; labels per owner; emit can't fail; generated ASL must read like the Plan (chapter 28).
- [Review: how we test](issues/06-how-we-test.md): a test kind per pass, `insta` snapshots, dumps as core functions; the case runner in `regia-cli`'s library reads `docs/spec/cases/` in place; an exact-path pending list where a passing listed case fails; `ok` cases need no guard (chapter 23, *Tests*).
- [Cut M1 into tickets](issues/07-cut-m1.md): tickets 14–34 in the Rust Book's order, ch 4 to 8; the move into `regia-core` sits mid-milestone (after ch 6); new lexer codes write their case first, which runs from M3.
- [The first crate](issues/08-first-crate.md): `regia-cli` is a workspace member whose `[[bin]]` `regia` points at `src/main.rs`; an integration test runs it via `CARGO_BIN_EXE_regia`.

Settled while charting:

- A `.regia` Entry can be built, without a Root Plot or a cast (ADR 0049, carried into the spec and guide).
- The lexer is built whole, then a thin path through every pass, then each pass is widened; parsing widens first, as a block.

## Not yet specified

- M4: the construct families the parser is cut into.
- M5–M6: the order of the chapters, and placing each of about 230 checks by the rule of *Where a check lives* (chapter 23).
- M6: how Conformance cases are written to reach chapter 27's coverage, and who writes them.
- M7: what stands in for Infrastructure ASL that isn't written, once *Readable generated ASL* has named it.
- M9: the performance budget (chapter 22 gives an example, not a number).

## Out of scope

- `regia-jason`, the Infrastructure ASL, `run` and behaviour cases: a later effort, since none can be tested alone.
- `edit` and `regia-wasm`: the Visual Editor's effort.
