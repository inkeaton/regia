# Research: implementation language for the Transpiler

Type: research
Status: resolved

## Question

Which language should the Regia Transpiler be written in: Rust, C++, or Python with its downsides addressed? Criteria: shipping a single binary with few dependencies, compiling to WebAssembly so it can run inside the Visual Editor, parser libraries (with support for indentation-sensitive and lossless parsing), error reporting libraries (ariadne/miette-style, Monaco-compatible diagnostics), performance, and maintainability for a small team. For Python, cover options like Pyodide, mypyc and Nuitka.

## Comments

Research running on throwaway branch `research/implementation-language` (file `research/implementation-language.md`). Never merged.

## Answer

Full findings are on branch `research/implementation-language`, file `research/implementation-language.md`. The note lays out the options without deciding.

- **1.0 baseline:** Lark LALR, not indentation-sensitive, editor calls a FastAPI server. About 17.6 ms per kLOC, so raw speed is probably not the deciding factor.
- **Rust:** rowan is a proven lossless CST (rust-analyzer, Biome). Ruff moved to a hand-written parser (2.2–2.4x faster, better error recovery). chumsky is 0.x and moved to Codeberg; pest stops at the first error; tree-sitter needs a C scanner for indentation and gives no error messages. wasm-bindgen/wasm-pack is the browser route (Ruff and Gleam ship this way). cargo builds a single binary natively (musl for fully static Linux).
- **C++:** tree-sitter, ANTLR (Java at build time, hand-written indentation lexer) or a hand-written parser like Carbon's. No ready CST or diagnostics library, so more code by hand. Emscripten plus Embind for WASM.
- **Python:** Lark has indentation support built in, but a lossless CST is custom work. Pyodide core is about 13.4 MB (wasm about 3.6 MB gzipped). PyInstaller and Nuitka one-file builds unpack to a temp folder on every launch; Nuitka is AGPL-3.0; mypyc does not produce a standalone binary.
- **Hybrid:** a Rust core with Python bindings (the Ruff/LibCST approach).
- **Diagnostics:** miette has help text plus JSON output and maps most directly to Monaco; ariadne moved to Codeberg. Monaco markers have no hint field and use 1-based positions, so a conversion layer is needed in any language.
- **Learning curve:** Google reports Rust confidence in about 2 months and productivity in 2–4; slow compiles are the top complaint.
- **Not confirmed:** gzipped wasm size for a comparable Rust compiler; whether Typst's tree is lossless.
