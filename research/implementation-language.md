# Research: Implementation language for the Regia 2.0 Transpiler

**Question.** Which language should the 2.0 Transpiler be written in: Rust, C++, or Python with its downsides addressed?

**Scope.** This note lays out options and evidence. It does **not** make the decision. Sources were checked on 2026-11-03. Each claim links to the source that owns it (official docs, source code, first-party blogs). Where a source could not be verified, the note says so.

**2.0 requirements this note checks against** (from the ticket and `docs/first reasonings/6 - Transpiler.md`):

| # | Requirement |
|---|---|
| R1 | Single binary, few dependencies |
| R2 | Runs inside the web-based Visual Editor, ideally as WebAssembly |
| R3 | Lossless CST that can be printed back to text (bidirectional editing) |
| R4 | Indentation-sensitive grammar |
| R5 | Multiple diagnostics per run, with hints, mappable to Monaco markers |
| R6 | Modular multi-pass architecture (preprocess, parse, CST to AST, validate, instance, emit to several Targets) |
| R7 | Maintainable by a very small team (a recent Master's graduate plus collaborators) |

---

## 0. Baseline: what 1.0 does today

- The parser is Lark with `parser="lalr"` and `propagate_positions=True` (`1.0/language/src/regia/parser.py`). The grammar is about 480 lines (`grammars/regia.lark`). The whole package is about 5.8k lines of Python.
- 1.0 does **not** use Lark's `Indenter`, so the 1.0 grammar is not indentation-sensitive.
- The Visual Editor (`1.0/editor`, React + Vite) does not run the Transpiler in the browser. It calls a FastAPI server (`1.0/server.py`) that imports `compile_source`. R2 would therefore be a change of architecture, not a port.
- **Measured performance** (`1.0/language/benchmarks/results/fits/fits.md`): compile time grows roughly linearly with input size. The pooled fit is **about 17.6 ms per kLOC of Regia** (power-law exponent k = 1.03, R² = 0.989). This number covers compilation only. It does not include interpreter start-up or import time.

---

## 1. Parser options

### 1.1 Rust

| Library | What it is | Indentation (R4) | Lossless (R3) | Error recovery (R5) |
|---|---|---|---|---|
| **rowan** | "A library for lossless syntax trees," inspired by Swift's libsyntax; MIT/Apache-2.0 ([repo](https://github.com/rust-analyzer/rowan)) | Not a parser. Indentation lives in your lexer (emit INDENT/DEDENT tokens). | **Yes, by design.** "All comments and whitespace get preserved." You get the original text back by joining the tokens in order ([rust-analyzer syntax doc](https://github.com/rust-lang/rust-analyzer/blob/master/docs/book/src/contributing/syntax.md)). | Your hand-written parser decides. rust-analyzer wraps bad input in `ERROR` nodes and sends errors to a separate sink. |
| **chumsky** | Parser combinators; "Flexible error recovery strategies out of the box," zero-copy, `no_std` ([repo](https://codeberg.org/zesterer/chumsky)). Latest is 0.13.0 (2026-05-06, [docs.rs](https://docs.rs/crate/chumsky/latest)). Still 0.x. The GitHub repo is archived and development moved to Codeberg. | Supports context-sensitive grammars and names "Python-style semantic indentation" as an example. | Produces whatever output type you build. It is not a CST library, but you can feed a rowan builder. | Strong: built to return several errors plus a partial AST. |
| **lalrpop** | LR(1) parser generator | Through a custom lexer that emits INDENT/DEDENT tokens. Ruff/RustPython used exactly this setup before 2024. | Not built in | `!` error-recovery alternatives inject an error token, then skip input. "Error recovery can only handle errors reported at the parser level, not the lexer level" ([book](https://lalrpop.github.io/lalrpop/tutorial/008_error_recovery.html)). |
| **logos** | Lexer generator. A `#[derive(Logos)]` enum compiles to one deterministic state machine, "faster than anything you'd write by hand" ([repo](https://github.com/maciejhirsz/logos)) | A lexer only. INDENT/DEDENT needs a small wrapper around it. | Keeps trivia if you emit it as tokens instead of `skip` | n/a |
| **tree-sitter** (Rust bindings) | Incremental GLR-ish parser generator with a C11 runtime ([site](https://tree-sitter.github.io/tree-sitter/)) | Needs an **external scanner written in C**. The docs name "Indent and dedent tokens in Python" as the standard case ([docs](https://tree-sitter.github.io/tree-sitter/creating-parsers/4-external-scanners.html)). | Has nodes for every token, including punctuation ([docs](https://tree-sitter.github.io/tree-sitter/using-parsers/2-basic-parsing.html)). Whitespace is `extras` and is not a node, but byte ranges let you rebuild the text from the source buffer. Lossless in practice only together with the original text. | Robust. Inserts `MISSING` nodes and marks errors ([api.h](https://github.com/tree-sitter/tree-sitter/blob/master/lib/include/tree_sitter/api.h)), but it **does not produce error messages**, so you write those yourself. |
| **pest** | PEG with a separate grammar file | `PUSH`/`PEEK_ALL`/`DROP` stack operations can match indentation ([book](https://pest.rs/book/grammars/syntax.html)) | Implicit `WHITESPACE`/`COMMENT` rules are usually silent (dropped). You can make them visible. | **Weak:** "Currently, pest terminates early on the first error." Multi-error recovery is only a pest3 proposal ([discussion](https://github.com/pest-parser/pest/issues/885)). |

**Real Rust projects with similar needs:**
- **rust-analyzer** uses a hand-written "recursive descent + pratt" parser over rowan. The parser never sees trivia, which is attached afterwards ([syntax doc](https://github.com/rust-lang/rust-analyzer/blob/master/docs/book/src/contributing/syntax.md)).
- **Biome** uses "an internal fork of rowan." Its CST "keeps track of all the information of a program, trivia included," with leading and trailing trivia attached to nodes and "Bogus" nodes for bad syntax ([architecture](https://biomejs.dev/internals/architecture/)).
- **Ruff** (an indentation-sensitive language: Python) **replaced LALRPOP with a hand-written recursive-descent parser** in v0.4.0. It got about 2.2 to 2.4x faster parsing. The team said the generator made new syntax hard to support, and that "A hand-written parser enables us to support error recovery" ([blog](https://astral.sh/blog/ruff-v0.4.0)).
- **LibCST** (a lossless Python CST) ships its default parser in Rust through PyO3: "By default the LibCST APIs use this module for all parsing" ([native README](https://raw.githubusercontent.com/Instagram/LibCST/main/native/libcst/README.md)).
- **Typst** keeps its parser and syntax tree in a separate `typst-syntax` crate ([docs.rs](https://docs.rs/typst-syntax/latest/typst_syntax/)). Whether that tree is lossless was not confirmed from first-party docs.

### 1.2 C++

| Option | Indentation (R4) | Lossless (R3) | Error recovery (R5) | Notes |
|---|---|---|---|---|
| **tree-sitter** (native C API) | External C scanner, as above | As above | `MISSING`/error nodes, no messages | The runtime is plain C11 and "embedded in any application." The grammar is written in JS and generated to C by the CLI. |
| **ANTLR 4** (C++ target) | No built-in support. The grammars-v4 Python3 grammar ships a hand-written `Python3LexerBase.cpp/.h` for each target ([listing](https://github.com/antlr/grammars-v4/tree/master/python/python3/Cpp)). | `-> channel(HIDDEN)` keeps whitespace and comments as tokens instead of discarding them ([lexer rules](https://github.com/antlr/antlr4/blob/master/doc/lexer-rules.md)). Tying them back to tree nodes is your job. | The default strategy does single-token insertion and deletion | **The tool needs Java 11+ at build time** ([getting started](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md)). C++ is one of 10 runtime targets ([targets](https://github.com/antlr/antlr4/blob/master/doc/targets.md)). The targets page says nothing about WebAssembly. |
| **Hand-written** | Full control | Full control (you design the tree) | Full control | Example: Carbon's C++ toolchain. Its parser is a state-stack machine with per-state handlers, a flat postorder tree, `InvalidParse` nodes and skip-to-statement-end recovery ([parse.md](https://github.com/carbon-language/carbon-lang/blob/trunk/toolchain/docs/parse.md)). C++ has no rowan equivalent, so you build the green/red tree yourself. |

C++ has no first-party equivalent of ariadne, miette or codespan, so rendering diagnostics is also hand-written.

### 1.3 Python

| Option | Indentation (R4) | Lossless (R3) | Error recovery (R5) |
|---|---|---|---|
| **Lark** (current) | **Built in:** `Indenter` is "a postlexer that 'injects' indent/dedent tokens," used with `parser='lalr', postlex=...` ([classes](https://lark-parser.readthedocs.io/en/latest/classes.html), [example](https://lark-parser.readthedocs.io/en/latest/examples/indented_tree.html)). `postlex` works only with the basic and contextual lexers. | **Not built in.** `keep_all_tokens` keeps punctuation. `%ignore`d tokens (whitespace, comments) are dropped from the tree. `lex(dont_ignore=True)` returns them as a token stream, and `lexer_callbacks` can collect them. Attaching trivia to nodes is custom work. | `on_error` for LALR: "Return true to resume parsing." Writing the recovery logic is up to you. |
| **LibCST-style** | n/a (Python-specific) | The model to copy: "preserves all whitespace and can be reprinted exactly," with "granular whitespace ownership" assigned to nodes, "a lossless CST that looks and feels like an AST" ([why LibCST](https://libcst.readthedocs.io/en/latest/why_libcst.html)) | n/a |

**Note:** LibCST itself moved its parser to Rust. The standard Python example of a lossless CST therefore ends up in the "Rust core, Python bindings" hybrid (see section 7).

---

## 2. Diagnostics (R5) and Monaco compatibility

**What Monaco needs.** `IMarkerData` has `severity`, `message`, `code?` (a string, or `{value, target: Uri}`), `source?`, `startLineNumber`, `startColumn`, `endLineNumber`, `endColumn`, `relatedInformation?[]` and `tags?` ([monaco-editor 0.52.2 `editor.api.d.ts`](https://cdn.jsdelivr.net/npm/monaco-editor@0.52.2/esm/vs/editor/editor.api.d.ts)).

There is **no "help" or "hint" field.** Hints must go into `message` or `relatedInformation`, or be separate markers with `MarkerSeverity.Hint`. Monaco positions are 1-based lines and columns, so a byte-offset span from any backend needs converting. Doing that conversion once, on the backend, is a design point whatever language is chosen.

| Library | Data model | Output | Status |
|---|---|---|---|
| **ariadne** (Rust) | Multi-label, multi-file, label priority, notes | Terminal and any `Write`. **No structured or JSON output** mentioned. | GitHub repo **archived 2026-03-26**, moved to [Codeberg](https://codeberg.org/zesterer/ariadne) ([GitHub](https://github.com/zesterer/ariadne)). Same author as chumsky. |
| **miette** (Rust) | A `Diagnostic` trait with derive: code, help, url, severity, labelled spans, related errors | Graphical (`fancy`), a narratable (screen-reader) printer, **and a JSON handler** ([docs.rs, 7.6.0](https://docs.rs/miette/latest/miette/)) | Active. JSON plus `help` maps most directly to Monaco markers. |
| **codespan-reporting** (Rust) | `Diagnostic { severity, code: Option<String>, message, labels, notes }` ([docs.rs](https://docs.rs/codespan-reporting/latest/codespan_reporting/diagnostic/struct.Diagnostic.html)) | Terminal back-end (`term`). `serde` is an optional dependency. | 0.13.1. Its fields are close to `IMarkerData`. |
| C++ | None of comparable reach found | Hand-written | |
| Python | 1.0 already has custom `errors.py` and `syntax_errors.py` | Hand-written | Lark exceptions carry line and column |

In every language the cleanest design is likely the same: an internal diagnostic struct, serialised to JSON for the editor and rendered for the terminal. The Rust libraries cover the terminal side and give a ready data model. They do not remove the need for the JSON-to-`IMarkerData` mapping.

---

## 3. WebAssembly (R2)

### Rust
- **wasm-bindgen** is "a Rust library and CLI tool that facilitate high-level interactions between Wasm modules and JavaScript," passing strings, objects and classes ([guide](https://rustwasm.github.io/docs/wasm-bindgen/)).
- **Governance change:** the rustwasm GitHub org was being shut down (archive in September 2025). wasm-bindgen moved to a new neutral org, [github.com/wasm-bindgen](https://github.com/wasm-bindgen) ([Inside Rust blog](https://blog.rust-lang.org/inside-rust/2025/07/21/sunsetting-the-rustwasm-github-org/)). **wasm-pack** now lives at [wasm-bindgen/wasm-pack](https://github.com/wasm-bindgen/wasm-pack) and is active, with a 2026 copyright notice. It builds npm-publishable packages.
- `wasm32-unknown-unknown` is **Tier 2**. `std::fs` always errors, `println!` does nothing, threads panic ([rustc book](https://doc.rust-lang.org/rustc/platform-support/wasm32-unknown-unknown.html)). The core passes must therefore take strings in and return data, with no file I/O. That suits R6 anyway: the preprocessor's import resolution sits behind a trait.
- **Real projects:**
  - **Ruff** ships `@astral-sh/ruff-wasm-{bundler,web,nodejs}`, "a WASM version of the Ruff API which can be used to lint/format Python in a browser" ([ruff_wasm](https://github.com/astral-sh/ruff/tree/main/crates/ruff_wasm)).
  - **Gleam** builds its compiler for the browser with `wasm-pack build --release --target web` ([compiler-wasm](https://github.com/gleam-lang/gleam/tree/main/compiler-wasm)).
- **tree-sitter from Rust to wasm:** the core crate's `build.rs` now handles `wasm32-unknown-unknown` with a bundled libc subset ([build.rs](https://github.com/tree-sitter/tree-sitter/blob/master/lib/binding_rust/build.rs)). The grammar's generated C, and any C scanner, still needs a C compiler that targets wasm. Most browser users instead use **web-tree-sitter**, which loads `tree-sitter.wasm` plus one `.wasm` per grammar, built with wasi-sdk since v0.26.1 ([README](https://github.com/tree-sitter/tree-sitter/blob/master/lib/binding_web/README.md)). Measured: `web-tree-sitter.wasm` 0.27.1 is **about 210 KB** (jsDelivr, 2026-11-03).

### C++
- **Emscripten** is "a complete Open Source compiler toolchain to WebAssembly," LLVM/Clang-based, with "very good" C/C++ standard library and exception support ([about](https://emscripten.org/docs/introducing_emscripten/about_emscripten.html)).
- **Embind** binds C++ functions and classes to JS. "Each binding increases the code size." Raw pointers with complicated lifetimes are not supported ([embind](https://emscripten.org/docs/porting/connecting_cpp_and_javascript/embind.html)).
- A second toolchain (emsdk) has to be kept next to the native compiler(s). ANTLR adds a Java dependency at build time.

### Python
- **Pyodide** core files: `pyodide.asm.wasm`, `pyodide.asm.mjs` and `python_stdlib.zip` ([deploying](https://pyodide.org/en/stable/usage/downloading-and-deploying.html)). The full distribution is "200+ megabytes." Measured for **Pyodide 314.0.7** (jsDelivr, 2026-11-03):

  | File | Uncompressed | gzip |
  |---|---|---|
  | `pyodide.asm.wasm` | 9.6 MB | about 3.6 MB |
  | `python_stdlib.zip` | 2.5 MB | (already zipped) |
  | `pyodide.asm.mjs` | 1.25 MB | not measured |
  | **Total core** | **about 13.4 MB** | |

  These sizes do not include the app code.
- **micropip** installs pure-Python wheels from PyPI. Packages with compiled code (C *or Rust*) need a wheel built for Pyodide ([micropip](https://micropip.pyodide.org/en/stable/project/usage.html)). Lark is pure Python (wheel about 111 KB), so it works. A PyO3 or mypyc-compiled core would need its own Emscripten build.
- Pyodide versus a Rust core: about 13 MB plus interpreter start-up, against a single wasm module per transpiler (and about 210 KB for the tree-sitter runtime). No first-party size number for a comparable Rust compiler wasm was found, so measure it in a prototype.
- **No-wasm option:** keep the 1.0 approach, where the Transpiler runs as a server (FastAPI). That fails R2's "ideally as WebAssembly" and needs a backend for the editor.

---

## 4. Distribution as a single binary (R1)

| Language | Mechanism | Evidence and caveats |
|---|---|---|
| Rust | `cargo build --release`. Rust's standard library is linked statically by default. Size options: `opt-level = "s"/"z"`, `lto`, `strip`, `codegen-units` ([Cargo profiles](https://doc.rust-lang.org/cargo/reference/profiles.html)). Docs warn "s"/"z" are "not necessarily smaller." | Fully static Linux binaries through `x86_64-unknown-linux-musl` (Tier 2 with host tools). `aarch64-apple-darwin` and `x86_64-pc-windows-msvc` are Tier 1 ([platform support](https://doc.rust-lang.org/rustc/platform-support.html)). Ruff and Gleam both ship as single native binaries. |
| C++ | Static linking (`-static`, `-static-libstdc++`, or musl). Dependencies come from vcpkg or Conan; there is no standard package manager. | Doable, but every platform needs its own toolchain and linker setup. Fully static glibc builds are a well-known pain point (the glibc FAQ could not be retrieved because of bot protection, so this is unverified here). |
| Python: **PyInstaller** | One-file mode "creates a temporary folder" (`_MEI…`) and unpacks into it on every launch. Starts slower than one-folder mode. Won't run where `/tmp` is mounted noexec. "Specific to the active operating system and the active version of Python," so no cross-building ([operating mode](https://pyinstaller.org/en/stable/operating-mode.html)). | |
| Python: **Nuitka** | "Translates the Python modules into a C level program" using libpython. `--mode=onefile` "extracts itself on the target, before running the program," by default to a temp dir. **AGPL-3.0 with a runtime exception** ([repo](https://github.com/Nuitka/Nuitka), [use cases](https://nuitka.net/user-documentation/use-cases.html)). Docs point to per-OS CI builds. | |
| Python: **mypyc** | Compiles typed modules to **C extensions**, not a standalone binary. 1.5 to 5x faster for existing annotated code, 5 to 10x when tuned. mypy got 4x. Alpha. Needs a separate build for each Python release ([intro](https://mypyc.readthedocs.io/en/latest/introduction.html)). | Speeds up the code, but does not deliver R1. Pair it with PyInstaller or Nuitka for that. |

---

## 5. Performance

- **1.0 baseline:** about 17.6 ms/kLOC in CPython plus Lark LALR (see section 0). A 2 kLOC Regia project compiles in about 35 ms, before start-up time. For interactive editing (re-parse on keystroke), raw throughput is **probably not the binding constraint** at expected Regia file sizes. Start-up and wasm load time may matter more.
- **Rust reference points:**
  - Ruff's hand-written parser was 2.2 to 2.4x faster than its LALRPOP parser ([blog](https://astral.sh/blog/ruff-v0.4.0)). That compares Rust with Rust, not Rust with Python.
  - logos benchmarks at about 1 to 1.5 GB/s for lexing (README; hardware not stated).
  - No first-party benchmark comparing Rust with Lark directly was found.
- **Python speed-ups:** mypyc gives 1.5 to 10x (first-party claim). Lark's LALR mode is its fastest mode, and 1.0 already uses it.
- **Incremental parsing:** only tree-sitter offers it out of the box ("efficiently update the syntax tree as the source file is edited"). rowan-based tools (rust-analyzer, Biome) reparse and get speed from sharing green nodes.

---

## 6. Learning curve and maintainability (R7)

- **Rust:**
  - Google's internal survey: over two-thirds of respondents felt "confident in contributing to a Rust codebase within two months or less." A third were as productive as in their other languages within two months, over half within four. Only 9% were unhappy with compiler diagnostics ([Google OSS blog, 2023](https://opensource.googleblog.com/2023/06/rust-fact-vs-fiction-5-insights-from-googles-rust-journey-2022.html)). Caveat: these were professional engineers with mentoring.
  - The 2024 State of Rust survey: "slow compilation was at the top of the list" of productivity limits. "Around 31%" of non-users cite perceived difficulty ([survey](https://blog.rust-lang.org/2025/02/13/2024-State-Of-Rust-Survey-results/)).
  - The parsing ecosystem has churn. chumsky and ariadne moved to Codeberg and chumsky is still 0.x. wasm-bindgen and wasm-pack changed org in 2025. Ruff dropped LALRPOP.
- **C++:**
  - No standard package manager or build system. Memory safety is manual.
  - No CST or diagnostics libraries comparable to rowan or miette, so more code is written by hand.
  - Two toolchains (native plus Emscripten), plus Java if ANTLR is used.
  - This research found no first-party survey data on C++ ramp-up time comparable to Google's Rust data.
- **Python:**
  - The team already knows it, and there is a working 5.8k-line codebase. Lark already handles indentation (R4).
  - The costs are in R1 (temp-dir extraction in one-file builds, per-OS builds), R2 (about 13 MB Pyodide) and R3 (trivia attachment is custom work).

---

## 7. Option matrix (evidence summary, not a ranking)

| | R1 single binary | R2 wasm | R3 lossless CST | R4 indentation | R5 multi-error diagnostics | R7 small team |
|---|---|---|---|---|---|---|
| **Rust** (logos + hand-written RD + rowan + miette or codespan) | Native, `cargo` | wasm-bindgen/wasm-pack. Ruff and Gleam do this. | rowan: proven lossless (rust-analyzer, Biome) | Custom lexer emits INDENT/DEDENT (Ruff's approach) | Full control, plus miette JSON | Steep start (about 2 to 4 months per Google data), slow compiles |
| **Rust** (chumsky) | same | same | Build the CST yourself | Built-in context-sensitive support | Built-in recovery | Less code, but 0.x and moved to Codeberg |
| **Rust or C++ + tree-sitter** | Yes | web-tree-sitter (about 210 KB runtime) or Rust-to-wasm | Byte ranges plus source text; whitespace not in nodes | External C scanner | Recovers, but no messages | Grammar in JS, scanner in C: a third language. Same grammar can drive editor highlighting. |
| **C++** (hand-written or ANTLR) | Static linking per platform | Emscripten + Embind | Build it yourself. ANTLR hidden channel keeps trivia tokens. | Hand-written lexer base class | Hand-written | Most manual work; Java needed for ANTLR |
| **Python** (Lark + PyInstaller/Nuitka) | One-file builds extract to temp; Nuitka is AGPL | Pyodide, about 13.4 MB core | Custom trivia attachment over `lex(dont_ignore=True)` | `Indenter` built in | `on_error` plus custom code | Lowest ramp-up; existing code |
| **Hybrid: Rust core + Python bindings** (PyO3/maturin, LibCST and Ruff style) | The Rust CLI is the binary | The Rust core goes to wasm directly | rowan | as Rust | as Rust | Two languages, but the Rust core is reused by the CLI, wasm and Python ([maturin](https://www.maturin.rs/)) |

### Open questions a prototype could answer
1. Size of the gzip'd wasm for a Rust Regia parser plus emitter (no first-party figure found for comparable projects).
2. How hard it is to attach Lark trivia losslessly, compared with rowan's built-in model, on a real Regia sample.
3. Whether the editor also wants tree-sitter for highlighting. If so, a tree-sitter grammar might be shared, or maintained twice.
4. Whether hints should map to `relatedInformation`, to `MarkerSeverity.Hint` markers, or both.
