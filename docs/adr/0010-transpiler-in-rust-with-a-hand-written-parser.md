# The Transpiler is written in Rust, with a hand-written parser

The 2.0 Transpiler is written in Rust and leaves Python and Lark behind. It must run in the Visual Editor as WebAssembly with no server, and also ship as one native binary per platform with nothing to install or unpack. Python can only do the first with Pyodide (about 13 MB before our own code) and the second with one-file builds that unpack at every launch. The parser is written by hand in the rust-analyzer style. A lexer keeps whitespace and comments as tokens. One recursive-descent function per grammar rule marks where nodes start and finish, and a lossless tree is built from those marks. Error recovery is the same everywhere: wrap the unexpected token in an Error node and skip ahead to a known token.

## Considered Options

- **Python with Lark** (1.0): known to the team, with indentation support built in. It fails both distribution requirements, and Lark drops whitespace and comments, which is the information a lossless tree needs. In 1.0, Lark saved only the 477-line grammar. The 1,140-line tree builder, the 848-line node classes and the comment preprocessor were hand-written anyway.
- **C++**: reaches native and WASM (Emscripten) too, but has no lossless-tree or diagnostics libraries, needs two toolchains, and memory safety is manual.
- **A Rust core with Python bindings** (Ruff, LibCST): nothing in Python needs the Transpiler as a library. The core stays free of global state, with plain data in and out, so bindings can be added later.
- **A parser generator** (lelwel, tree-sitter, lalrpop, pest, chumsky; findings on branch `research/grammar-driven-parsing-rust`). The lexer is hand-written in every option, because no tool generates Regia's indent stack, line continuation and nestable comments. pest stops at the first error. tree-sitter puts the lexing in C and gives no error messages. lalrpop leaves the lossless tree to hand-written code. lelwel fits best but is young, with one maintainer. A hand-written parser is about 1,000–1,500 lines with no third-party dependency, and each rule is a small, separate piece of code.

## Consequences

- A new construct means one parser function plus one typed accessor. Accessors are hand-written at first and may later be generated from a grammar file, as rust-analyzer does.
- The person writing the code is new to Rust. Development is planned as a learning effort with small steps and exercises (map Notes, `.scratch/regia-2/map.md`).
- lelwel builds the same kind of tree from the same kind of steps. Its code is a reference for patterns, and switching to it later stays cheap.
- Diagnostics are converted once, inside the Transpiler, into a form Monaco can show.
