# Research: grammar-driven parsing in Rust for the Regia 2.0 Transpiler

**Status:** research only. This note lays out options and evidence. It does not choose one.
**Date:** 2026-11-09 (all release dates and repo activity checked on this day).
**Ticket:** `.scratch/regia-2/issues/28-research-grammar-driven-parsing-rust.md`, input for *Implementation language for the Transpiler* (26). Rust is already decided.
**Builds on (not repeated here):** `research/implementation-language.md` (branch `research/implementation-language`) and `research/lossless-cst.md` (branch `research/lossless-cst`).

**Method.** Versions and dates come from the crates.io API (`/api/v1/crates/<name>/versions`) and the GitHub API. Behaviour claims come from each project's README, book or source. **No Rust toolchain was available on the research machine, so nothing was compiled or run.** Claims marked *unverified* are reasoned from docs, not tested.

---

## 1. Requirements, restated

The person writing the Transpiler is new to Rust and wants as much of the parser as possible generated from a grammar file, the way 1.0 used Lark (`1.0/language/src/regia/grammars/regia.lark`, 477 lines, LALR, whitespace and comments `%ignore`d, not indentation-sensitive).

| # | Requirement |
|---|---|
| G1 | Lossless tree: every token, whitespace and comment kept; prints back byte for byte, also for invalid input |
| G2 | Several errors per run, with recovery, so the tree is still usable while the user types |
| G3 | Indentation-sensitive (INDENT/DEDENT from an indent stack), mixed with optional `.`/`;` terminators and Inline blocks |
| G4 | `.` ends a Statement only before a space, end of line, `;` or `#` |
| G5 | Nestable `#[ … ]#` comments |
| G6 | Builds for `wasm32-unknown-unknown` (Visual Editor, Monaco) as well as natively |
| G7 | Low effort when the grammar changes |
| G8 | Rust-novice friendly: as much generated as possible, little clever Rust |

---

## 2. How hard is Regia 2.0 to lex?

Read from `docs/spec/01-statements-and-blocks.md` and `docs/spec/02-comments.md`. This matters because **no candidate below generates the lexing part**. Every one of them needs a stateful lexer (or tree-sitter "external scanner") written by hand. The difference between tools is where that code lives and in which language.

| Rule | What the lexer has to do | Regular (generator-friendly)? |
|---|---|---|
| INDENT/DEDENT from an indent stack | Measure leading whitespace at each logical line start, push/pop a stack, emit zero-width INDENT/DEDENT tokens, error on dedent to a level never opened | No. Needs a stack |
| Blank, comment-only lines and lines spanned by `#[ … ]#` don't count | Look past trivia before deciding the line's indent | No |
| Tabs or spaces, consistent per file | Remember the first indent character seen | No (one bit of state) |
| Continuation: line ends with `,` or has an unclosed `(` | Paren depth counter, plus look ahead past trailing spaces/comments for a final `,`; check continuation lines are indented further | No |
| `.` ends a Statement only before space/EOL/`;`/`#` | Mostly handled by maximal munch: a dotted-name regex `ident(\.ident)*` and a number regex `\d+\.\d+` swallow the "glued" dots, so a lone `.` is a terminator. `complain.SIGNAL` then lexes as one dotted name, which is what the spec wants (error plus hint). Any remaining case is a one-character peek in a callback | Nearly regular |
| `#[ … ]#` nests, and `#@key[`/`#%[` openers count as levels inside it | Depth counter loop in a callback | No (nesting) |
| `#@key[ … ]#` and `#%[ … ]#` do **not** nest; run to the first `]#` | Plain regex | Yes |
| Doc/instancing comments must start their own line | Check "only whitespace since line start" | Small state |
| Inline block ends at `;` **or end of line** | Can live in the grammar (see below) or the lexer can emit a virtual "close inline" token at end of line for each unclosed Inline block | Grammar problem, see below |

**The Inline-block ambiguity is a grammar problem, not a lexer one.** In `IF a: IF b: DO c; DO d`, a `;` after `DO c` could close the inner block (spec: "Each `;` closes one Block") or, if the inner block were closed by "end of line or ε", the outer one. This is the dangling-else pattern. An LL tool resolves it by "prefer the inner block" (lelwel has a constant-true predicate `?t` for exactly this, see 3.1). An LR tool without conflict resolution (lalrpop) reports a conflict, so the grammar needs two block shapes, "closed by `;`" and "open until end of line", the second allowed only last on a line. That is doable but is exactly the kind of grammar surgery a Rust novice will find hard.

**Estimate (opinion, not measured):** the hand-written lexer is about 200 to 400 lines of Rust whatever tool is chosen. The lelwel Python 2.7 example (below) does INDENT/DEDENT, paren depth and blank/comment lines in roughly 120 lines of lexer callbacks, which supports this order of magnitude. Regia adds nested comments, continuation by `,`, tab/space consistency, and the own-line check for doc comments.

---

## 3. Candidates

### 3.1 lelwel (LL(1) recursive-descent generator, lossless CST)

- **What it is.** "generates recursive descent parsers for Rust using LL(1) grammars with extensions for direct left recursion, operator precedence, semantic predicates (which also enable arbitrary lookahead), semantic actions …, and a restricted ordered choice." "The parser creates a homogeneous, lossless, concrete syntax tree (CST)." Name: "Language for Extended LL(1) parsing With Error resilience and Lossless syntax trees" ([README](https://github.com/0x2a-42/lelwel)).
- **Maturity.** 0.10.4 (2026-04-08); 0.10.0 to 0.10.4 between 2025-11 and 2026-04. Last push 2026-11-01; recent commits add `stacksafe` generation (#72, 2026-09-29). 201 stars, 14 open issues, 3 reverse dependencies on crates.io. **Single maintainer, small user base, pre-1.0.** That is the main risk. Dual MIT/Apache-2.0.
- **Grammar file.** `.llw`, close to EBNF/Lark in feel: `token` lines, `skip` tokens, `start`, rules with `[]`, `*`, `+`, `|`. Its own parser is written in lelwel. There is a language server, `lelwel-ls`, which reports "conflicts or errors" in the grammar as you type ([README](https://github.com/0x2a-42/lelwel)). The generated parser is written to `OUT_DIR` from `build.rs` (not a proc macro), so it "can be debugged with standard tools".
- **Lossless (G1).** Skip tokens (whitespace, comments) "will however still be part of the syntax tree". The CST is lelwel's own flat, arena-style structure (`Cst`, `NodeRef`, `Node::Rule`/`Node::Token`, spans into the source string; see `src/skeleton/generated.rs`). It is **not rowan**, and it has no edit API. If the Visual Editor needs rowan's green/red tree and `SyntaxEditor`-style edits (`research/lossless-cst.md`), a tree walk that feeds a `rowan::GreenNodeBuilder` is needed. That is short, but hand-written (*unverified*, not tried).
- **Error recovery (G2).** Built in and automatic. Errors go to `create_diagnostic`; an "active error state" stops cascades; the parser either skips the expected token, or wraps an unexpected token in an `error` node, or breaks out of a loop when the token is in the recovery set. Recovery sets are computed automatically "by using the follow sets of the dominators in the directed graph induced by the grammar". The lexer can emit an `Error` token that the parser always skips. This follows matklad's resilient-LL design ([tutorial](https://matklad.github.io/2023/05/21/resilient-ll-parsing-tutorial.html)). The README shows its tree for broken C next to tree-sitter's.
- **Indentation (G3).** Not a grammar feature. **But the repository ships a Python 2.7 example** (`examples/python2/src/lexer.rs`) whose lexer keeps an indent stack, paren depth and pending INDENT/DEDENT counters, skips blank and comment lines, and errors with "unindent does not match any outer indentation level". The grammar then uses `Indent`/`Dedent`/`Newline` like any token. The parser asks for tokens through `create_tokens(source, diags) -> (Vec<Token>, Vec<Span>)`, so **the lexer is a free-standing pre-pass you own completely**. That suits Regia's logical-line joining. (That example uses `herring`, the author's own lexer generator, 0.1.2 from 2025-03, rather than logos. logos is the default and works the same way.)
- **The Inline-block `;` ambiguity.** LL(1) conflicts are reported. "The syntax `?t` can be used to define a constant `true` predicate, which is useful for disambiguation, where one parse is always prioritized (e.g. dangling else problem)" ([README](https://github.com/0x2a-42/lelwel)). This fits "each `;` closes the innermost Inline block".
- **wasm (G6).** The generated code is plain Rust with logos and codespan; no C. The **lelwel playground** (`0x2a-42.github.io/playground.html`) loads each example parser, including `python2`, as a wasm-bindgen module (`parsers/lelwel_python2.js` loads `lelwel_python2_bg.wasm`), which means wasm32-unknown-unknown builds of lelwel parsers exist and run in the browser.
- **Hand-written.** The lexer (`lexer.rs`, Regia's stateful rules), predicate/action callbacks in `parser.rs` (one small function each), diagnostics wording, and any typed AST. Lelwel does **not** generate typed AST accessors; lelwel's own frontend writes them with a small `ast_node!` macro over `Cst` (`src/frontend/ast.rs`).
- **Cost of a grammar change.** Edit `.llw`, rebuild. The language server flags new conflicts. New predicates need a callback. Typed AST wrappers need a manual update.

### 3.2 tree-sitter (+ type-sitter or rust-sitter)

- **Maturity.** tree-sitter 0.27.2 (2026-11-07), very active, used by major editors. MIT.
- **Grammar file.** `grammar.js` (JS DSL) compiled by `tree-sitter generate` into C (`parser.c`). Node.js is the default runtime; since 0.26 `--js-runtime native` uses a bundled QuickJS, and `grammar.json` can regenerate without JS ([CLI generate](https://tree-sitter.github.io/tree-sitter/cli/generate.html)). GLR, so conflicts can be declared instead of removed.
- **Lossless (G1).** Every token is a node; whitespace usually exists only as gaps between node byte ranges; the tree stores no text, so printing means slicing the original buffer (`research/lossless-cst.md` §4.3). For a rowan-style CST, a walk that fills gaps as trivia tokens is needed (hand-written).
- **Error recovery (G2).** Robust: `ERROR` and `MISSING` nodes, many per tree. It **does not produce error messages**; you write them from the tree (`research/implementation-language.md` §1.1). Incremental reparsing is built in; no other candidate has it.
- **Indentation (G3) and nested comments (G5).** Need an **external scanner written in C**: "a set of C functions that you, the grammar author, can write by hand", in `src/scanner.c`, with `create`, `destroy`, `serialize`, `deserialize`, `scan`. State must fit `TREE_SITTER_SERIALIZATION_BUFFER_SIZE`. During error recovery `scan` is called with "all tokens marked as valid", which the scanner must handle ([external scanners](https://tree-sitter.github.io/tree-sitter/creating-parsers/4-external-scanners.html)). Python's indent/dedent is the docs' own example. For Regia, **all of section 2 would be written in C**, not Rust, and must stay correct under incremental reparsing and serialization. For a Rust newcomer that is a second language and the hardest part of the job.
- **wasm (G6).** The Rust binding's `build.rs` compiles the C runtime for `wasm32-unknown-unknown` against a bundled libc subset: "wasm32-unknown-unknown has no libc, so compile in the subset from src/wasm-stdlib" (`lib/binding_rust/build.rs`, master). Needs clang with a wasm32 target. **Unverified:** whether a grammar's own `parser.c` plus a C `scanner.c` link cleanly into a `wasm32-unknown-unknown` Rust crate with only that subset. Alternatively the browser could use `web-tree-sitter` directly, but then the editor and the Rust Transpiler run different parser builds.
- **Typed wrappers.**
  - **type-sitter** 0.10.1 (2026-05-14): "generate typed wrappers for tree-sitter grammars from node-types.json and queries", via proc macro, build script or CLI; "Typed error, missing, and extra nodes". "type-sitter is in alpha"; README says it depends on tree-sitter 0.26 (one minor behind); generated files can exceed 30,000 lines; 50 stars ([repo](https://github.com/Jakobeha/type-sitter)).
  - **rust-sitter** 0.4.5 (2025-05-06), last push 2025-06-18, so **no activity for about 17 months**. Grammar written as annotated Rust types; default runtime is a forked pure-Rust tree-sitter that targets `wasm32-unknown-unknown`. Its README does not mention external scanners, so there is no documented way to get INDENT/DEDENT ([repo](https://github.com/hydro-project/rust-sitter)). Poor fit for Regia.
- **Hand-written.** C external scanner, error messages, gap-filling for a lossless tree, CST to AST.
- **Cost of a grammar change.** Edit `grammar.js`, regenerate (CLI), regenerate type-sitter wrappers. Cheap for the grammar itself; scanner changes are C.

### 3.3 lalrpop + logos

- **Maturity.** lalrpop 0.23.2 (2026-10-19), active, 3.5k stars. logos 0.16.1 (2026-01-30), active. Both MIT/Apache-2.0, pure Rust.
- **Grammar file.** `.lalrpop`, LR(1)/LALR(1), with Rust action code inline in each rule. The book's external-lexer chapter uses logos: tokens arrive as `Result<(Loc, Tok, Loc), Error>` triples, mapped to terminals in an `extern` block, and whitespace and `#` comments are `skip`ped in the logos enum ([book, external lib](https://lalrpop.github.io/lalrpop/lexer_tutorial/005_external_lib.html)).
- **Lossless (G1).** Not built in. Trivia is removed before the parser. To be lossless you attach trivia to tokens in the lexer wrapper and build the tree (e.g. rowan) yourself **in every rule's action code**. That is the bulk of the work and it all changes when the grammar changes.
- **Error recovery (G2).** `!` alternatives: the parser injects an error token, runs what actions it can, then "discards input tokens until it finds one that lets parsing proceed". Collecting errors is your job (push into a `Vec`). "Error recovery can only handle errors reported at the parser level, not the lexer level" ([book](https://lalrpop.github.io/lalrpop/tutorial/008_error_recovery.html)). Recovery points are placed by hand.
- **Indentation (G3).** Through the logos wrapper emitting INDENT/DEDENT; this is how Ruff and RustPython did Python before 2024. Ruff then **replaced LALRPOP with a hand-written parser**, saying "A hand-written parser enables us to support error recovery" ([Ruff v0.4.0](https://astral.sh/blog/ruff-v0.4.0)).
- **Inline-block `;`.** Becomes an LR conflict that must be removed by restructuring the grammar (section 2).
- **wasm (G6).** Pure Rust, generated at build time; no known obstacle (*unverified* by build).
- **Hand-written.** Lexer wrapper, all tree-building actions, recovery placement, lossless trivia plumbing.
- **Cost of a grammar change.** Grammar plus actions; conflicts can appear in unrelated places (LR). Moderate to high.

### 3.4 grmtools (lrpar + lrlex)

Not in the ticket; included as the strongest LR option for recovery.

- **Maturity.** lrpar/lrlex 0.15.0 (2026-07-22), push 2026-09-21, softdevteam (King's College London). Pure Rust.
- **Recovery (G2).** Automatic, grammar-neutral: "`lrpar` implements the `CPCT+` error recovery algorithm", which "reports multiple repair sequences" so "users [can] fix all their syntax errors in one go". Limits: an internal timeout (fails on "less than 2% of real-world inputs"), syntax only; lexing errors stop the lexer unless a catch-all rule turns them into parse errors ([book](https://softdevteam.github.io/grmtools/latest_release/book/errorrecovery.html)).
- **Lossless (G1).** Not built in. Generic parse trees exist only as a deprecated action kind (`action_generictree`, `Node` deprecated, [docs.rs](https://docs.rs/lrpar/latest/lrpar/)). Same plumbing as lalrpop.
- **Indentation (G3).** Custom lexer needed (*unverified* how cleanly a non-lrlex lexer plugs in).
- **Verdict.** Better recovery than lalrpop with less hand work, same losslessness gap, Yacc-style grammar.

### 3.5 pest

- **Maturity.** 2.9.5 (2026-10-26), very active, 5.4k stars, pure Rust.
- **Grammar file.** `.pest`, PEG. Closest to Lark in "write a grammar, get a tree". Typed AST helpers exist as third-party crates (`pest-ast` 0.3.6, `pest_typed_derive` 0.20.11, both 2025).
- **Lossless (G1).** Output is `Pairs` with spans. Implicit `WHITESPACE`/`COMMENT` rules are inserted "at every sequence and between every repetition"; the book says to mark them silent "unless you want to see them included", so they can be kept ([book](https://pest.rs/book/grammars/syntax.html)). Feasible, but on failure there is no tree at all, which breaks "lossless also for invalid input".
- **Error recovery (G2). Fails.** "Currently, pest terminates early on the first error." Multi-error recovery is a pest3 proposal in discussion #885, open since 2023-07 with no release ([discussion](https://github.com/pest-parser/pest/discussions/885)).
- **Indentation (G3).** `PUSH`/`PEEK_ALL`/`DROP` can match indentation in-grammar (book example). Regia's extra rules (comment lines don't count, continuation lines, tab/space consistency) make that awkward; a pre-lexer would fight pest's character-level design.
- **Verdict.** Fails G2 outright.

### 3.6 chumsky

- **Maturity.** 0.13.0 (2026-05-06). (crates.io's `max_version` shows `1.0.0-alpha.8`, but that is from 2025-01-22, older than 0.13.0.) Development moved from GitHub (archived) to Codeberg ([repo](https://codeberg.org/zesterer/chumsky)).
- **Grammar file. None.** Chumsky is a parser-combinator library: the grammar is Rust code. That contradicts the "generate from a grammar file" wish.
- **Recovery (G2).** Strong: "Flexible error recovery strategies out of the box"; it returns a partial output plus errors ([docs.rs](https://docs.rs/chumsky/latest/chumsky/)).
- **Lossless (G1).** Not built in; no CST support mentioned. You build rowan events yourself.
- **Indentation (G3).** "supports context-sensitive grammars via a set of dedicated combinators", naming "Python-style semantic indentation". Or lex first.
- **wasm (G6).** Pure Rust, `no_std` capable.
- **Novice fit (opinion).** Heavy generic types; type errors from deep combinator chains are long. Better for someone already fluent in Rust.

### 3.7 The rust-analyzer approach (ungrammar + codegen over a hand-written parser)

- **What is generated.** "Ungrammar describes concrete syntax tree — a set of data types"; it is "paired with a hand-written parser" ([ungrammar post](https://rust-analyzer.github.io/blog/2020/10/24/introducing-ungrammar.html)). rust-analyzer generates `SyntaxKind` and typed AST accessors (`mod_token()`, `item_list()`, …) from `crates/syntax/rust.ungram` with its own in-repo code generator (`xtask/src/codegen/grammar.rs`, about 40 KB, plus `ast_src.rs`). **The parser itself is not generated.**
- **Maturity.** The `ungrammar` crate's last release is 1.16.1 (2022-03-05). Its repo `rust-analyzer/ungrammar` is **archived**; the README says "This crate now lives in https://github.com/rust-lang/rust-analyzer/tree/master/lib/ungrammar". The codegen is not a reusable crate; you would copy and adapt it. rowan itself is active (0.18.0-alpha.2, 2026-10-21; see `research/lossless-cst.md` for the trivia-model change in 0.18).
- **Lossless, recovery, indentation.** All yours, and all fully controllable. The recipe is well documented (matklad's resilient-LL tutorial: event list `Open`/`Close`/`Advance`, recovery sets, "fuel", `advance_with_error`). Ruff, rust-analyzer and Biome all chose a hand-written parser for these reasons.
- **wasm.** Pure Rust (rowan has no C).
- **Hand-written.** The entire parser and lexer. Generated: syntax kinds and typed AST. Keeping parser and grammar in sync relies on tests; the post does not describe any mechanism for it.
- **Cost of a grammar change.** Edit `.ungram` and the matching parser function(s) by hand. Highest effort per change, but each change is local and plain Rust.

### 3.8 Others looked at

| Option | Status | Why it is or isn't a fit |
|---|---|---|
| **parol** 5.0.4 (2026-10-31), active | LL(k) and LALR(1) generator from a grammar file; "generate types that resemble the AST of your grammar automatically"; scanner states; "As of version 0.24.0 generated parsers can recover from syntax errors automatically" ([README](https://github.com/jsinger67/parol)) | The only generator that also derives typed AST types. **Unverified:** whether its parse tree is lossless (README silent), whether it reports several errors, and how a custom INDENT/DEDENT lexer plugs in. Worth a short spike if lelwel is rejected |
| **Lady Deirdre** 2.2.0 (2025-08) | Incremental, error-resistant, wasm-compatible framework; grammar via derive macros on enums | **Proprietary, source-available license** ("This work is proprietary software with source-available code", [repo](https://github.com/Eliah-Lakhin/lady-deirdre)). Excluded on licensing |
| **rowan-peg** 0.2.10 (2025-10) | ABNF-like grammar to rust-peg that builds rowan trees | Very small user base (about 3.7k downloads). PEG recovery limits similar to pest (*unverified*) |
| **sipha** 3.0.0 (2026-03) | "PEG parser, syntax trees, and code generation" | About 1.1k downloads; too young to judge |
| **cstree** 0.14.0 (2026-04), **syntree** 0.19.0 (2026-10) | Tree libraries, not parsers | Alternatives to rowan as the tree a parser feeds |

---

## 4. Where each option leaves the Regia-specific work

| Regia need | lelwel | tree-sitter | lalrpop/grmtools | pest | chumsky | RA approach |
|---|---|---|---|---|---|---|
| Stateful lexer (indent, continuation, nested comments) | Rust, free-standing pre-pass | **C** external scanner | Rust lexer wrapper | partly in-grammar | Rust | Rust |
| Inline-block `;` ambiguity | `?t` predicate | GLR `conflicts` / precedence | rewrite grammar (LR conflict) | ordered choice | combinator order | code order |
| Lossless tree | generated (own CST) | gaps + buffer | hand-written in actions | spans, valid input only | hand-written | hand-written (rowan) |
| Multiple errors | generated | generated (no messages) | `!` by hand / CPCT+ automatic | no | yes | hand-written |
| Typed AST | hand-written (macro) | type-sitter (alpha) | your action types | third-party crates | your types | generated from `.ungram` |

---

## 5. Which options fit best (not a decision)

- **lelwel matches the brief most closely.** It is the only candidate that generates a resilient, lossless CST from a grammar file, in plain Rust, with a documented Python-style INDENT/DEDENT example and browser wasm builds already running. What stays hand-written is the part every option leaves hand-written (the lexer), plus small callbacks and the typed AST. **Main risk:** a single maintainer, pre-1.0, 3 dependents on crates.io. Mitigation: the generated parser is ordinary Rust in `OUT_DIR`; if lelwel stalls, the generated code can be vendored and maintained as a hand-written parser, which is the rust-analyzer approach.
- **tree-sitter is the most mature and the only one with incremental reparsing**, but Regia's hardest part (section 2) would be written in C and must survive tree-sitter's error-recovery and serialization rules. The lossless tree and the error messages are hand-written on top. Better if Monaco highlighting and editor integration matter more than the Transpiler's diagnostics.
- **The rust-analyzer approach is the proven endpoint** (Ruff, rust-analyzer, Biome), but it is the opposite of "generated from a grammar". Keep it as the fallback, and possibly as where a lelwel parser ends up.
- **lalrpop + logos, grmtools and pest are weak fits**: the first two leave losslessness entirely to action code, pest stops at the first error. **chumsky** has no grammar file. **parol** is the one unexplored generator worth a one-day spike.
- **Suggested spike (any option):** the 50-line example at the top of `01-statements-and-blocks.md` plus the nested-comment examples of `02-comments.md`, checked for `print(parse(src)) == src`, two-errors-in-one-file, and a `wasm32-unknown-unknown` build.

## 6. What could not be verified

- Nothing was compiled: no Rust toolchain on the research machine.
- tree-sitter: whether a grammar crate with a C `scanner.c` links for `wasm32-unknown-unknown` using only the runtime's `wasm-stdlib` subset.
- lelwel: exact behaviour of `?t` on the nested Inline-block case; cost of converting its CST to rowan.
- parol: losslessness, multi-error reporting, custom lexer integration.
- grmtools: plugging in a non-lrlex lexer.
- type-sitter: wasm build; its tree-sitter 0.27 support.
- The 200 to 400 line lexer estimate is an estimate from the lelwel Python example, not a measurement.

## 7. Comparison

| Option | Latest release (activity) | Grammar file → parser generated? | Lossless tree | Multiple errors + recovery | Indentation | `wasm32-unknown-unknown` | Hand-written part | Grammar change cost |
|---|---|---|---|---|---|---|---|---|
| **lelwel** | 0.10.4, 2026-04 (push 2026-11; 1 maintainer) | Yes (`.llw`, LL(1)+predicates) | Yes, own CST (not rowan) | Yes, automatic recovery sets | Lexer pre-pass in Rust (Python 2.7 example) | Yes (playground ships wasm-bindgen builds) | Lexer, callbacks, typed AST, rowan bridge if wanted | Low |
| **tree-sitter** (+type-sitter) | 0.27.2, 2026-11 (very active); type-sitter 0.10.1 alpha | Yes (`grammar.js`, GLR) | Via source buffer + gaps | Yes (ERROR/MISSING), no messages | **C** external scanner | Runtime yes; grammar+scanner C *unverified* | C scanner, messages, lossless bridge | Low (grammar), high (scanner) |
| **rust-sitter** | 0.4.5, 2025-05 (stalled) | Yes (Rust types) | As tree-sitter | As tree-sitter | No external scanner documented | Yes (pure-Rust fork) | — | — |
| **lalrpop + logos** | 0.23.2, 2026-10; logos 0.16.1, 2026-01 | Yes (`.lalrpop`, LR(1)) | No, by hand in actions | `!` rules by hand; no lexer-level recovery | Rust lexer wrapper | Likely (pure Rust) | Lexer, all tree building, recovery | Medium–high |
| **grmtools** | 0.15.0, 2026-07 | Yes (Yacc, LR) | No | Yes, automatic CPCT+ | Custom lexer | Likely (pure Rust) | Lexer, tree building | Medium |
| **pest** | 2.9.5, 2026-10 | Yes (`.pest`, PEG) | Spans, valid input only | **No** (first error) | In-grammar stack ops | Likely (pure Rust) | Typed AST, error handling | Low, but fails G2 |
| **chumsky** | 0.13.0, 2026-05 (Codeberg) | **No** (combinators in Rust) | No | Yes | Combinators or pre-lexer | Yes (`no_std`) | Everything, concisely | Medium |
| **RA approach** (ungrammar + rowan) | ungrammar 1.16.1, 2022 (moved into RA repo); rowan 0.18.0-alpha.2, 2026-10 | No (only kinds + typed AST) | Yes (rowan) | Yes, by hand | Rust lexer | Yes | Parser and lexer | High per change, but local |
| **parol** | 5.0.4, 2026-10 | Yes (LL(k)/LALR(1)) + AST types | *Unverified* | Recovery since 0.24; multi *unverified* | Scanner states; INDENT *unverified* | Likely | *Unverified* | Low–medium |
