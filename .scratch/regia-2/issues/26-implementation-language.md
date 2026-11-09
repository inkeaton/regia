# Implementation language for the Transpiler

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 24, 25, 28

## Question

Which language is the Regia Transpiler written in: Rust, C++, Python, or a Rust core with Python bindings? Weigh the findings of the implementation-language research (25) and the lossless-CST research (24) against this team's skills and the requirements: a single binary, running in the Visual Editor through WASM, a lossless CST, an indentation-sensitive grammar, and multi-error diagnostics compatible with Monaco. Also decide whether the parser is hand-written or generated.

## Comments

- Opened [Research: grammar-driven parsing in Rust](28-research-grammar-driven-parsing-rust.md) mid-session, when the question of a Lark-like generator came up.

## Answer

Rust, with a hand-written parser. ADR 0010.

- **Hard requirements:** the Visual Editor runs the Transpiler in the browser as WebAssembly, with no server. The CLI ships as one native binary per platform (Linux, macOS, Windows), built by CI, with no runtime to install and no unpacking at launch. The core is a library: strings in, data out, no file I/O and no global state.
- **Language:** Rust. C++ is rejected (no lossless-tree or diagnostics libraries, two toolchains, manual memory safety). Python is rejected because it fails both requirements above.
- **No Python bindings in 2.0.** The core stays easy to bind later. Python callers use the CLI.
- **Parser:** hand-written in the rust-analyzer style, with matklad's "Resilient LL Parsing" tutorial as the reference:
  - A hand-written lexer keeps whitespace and comments as tokens and produces INDENT/DEDENT from an indent stack.
  - One recursive-descent function per grammar rule marks where nodes start and finish, and a lossless tree is built from those marks.
  - Error recovery is the same everywhere: an Error node, then skip ahead to a known token.
  - Typed accessors are hand-written at first; generating them from a grammar file stays an option.
  - No parser generator. lelwel was the best generator candidate but is young with one maintainer. Its code is a reference for useful patterns, and switching to it later stays cheap because it builds the same kind of tree.
- **Size, compared with 1.0:** Lark saved only the 477-line grammar. The 1,140-line builder, the 848-line node classes and the comment preprocessor were hand-written anyway. The 2.0 hand-written parser is about 1,000–1,500 lines and replaces most of that.
- **Order of the parser criteria:** the hard requirements first, then as few places to change per language change as possible, then the learner understanding everything.
- **Handoff constraint for the development effort** (also in the map's Notes): the person writing the code is new to Rust, and building the Transpiler is a learning experience. Tickets are cut smaller than usual. Claude writes less code and sets exercises for the learner to write parts. Use `vibe-wise:learn`, `mattpocock-skills:teach` and `mattpocock-skills:scaffold-exercises`. The first exercise is the check suggested in ticket 28: parse the spec chapter 1 and 2 examples, print them back byte for byte, get two errors from one file, and build for `wasm32-unknown-unknown`.
- **Left to other decisions:** whether the tree is the rowan crate or our own, and whether it carries edits, goes to [Bidirectional editing model](27-bidirectional-editing-model.md). The diagnostics library (miette or our own type) and the hint-to-Monaco mapping go to the Transpiler architecture fog. Editor highlighting (Monarch, semantic tokens from the WASM, or tree-sitter) goes to the Visual Editor architecture fog.
