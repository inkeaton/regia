# Coding standards

This file is the entry point for how code in this repo is written. Agents and
reviewers (including the `code-review` skill) start here.

## Sources, in order of precedence

When two sources disagree, the higher one wins.

1. **`docs/spec/`**: what the code must do, and the Transpiler's
   architecture (chapter 23). It says nothing about style.
2. **The guides in `docs/standards/`**, each for its own area:
   - `comments-rust.md`: comments, doc comments, file layout, section
     dividers, test layout. Read `comments.md` first; the Rust guide
     adapts it and wins where they differ.
   - `docs.md`: prose documentation for maintainers. It builds on the
     `diataxis` skill (from oxidecomputer/claude-plugins) and wins where
     they differ.
3. **`GLOSSARY.md`**: the project's domain terms. Names in code, docs and
   tests use these terms, not the ones it lists under _Avoid_.
4. **`docs/adr/`**: recorded design decisions.
5. **Rust skills** `rust-*` (from dawidpereira/rust-skills, installed
   locally): Rust technique: ownership, errors, types, API design,
   performance, quality, tests, macros. They decide *how to write the Rust*,
   never how to comment or lay it out.
6. **Rust API Guidelines / std conventions**, for anything not covered above.

The Matt Pocock skills (plugin `mattpocock-skills`) are workflow, not
standards: grilling, specs, tickets, TDD, code review, domain modeling. They
read this file and `GLOSSARY.md`; they don't add rules of their own.

## Known conflicts with the Rust skills

These rust-skills recommendations are overridden here:

| Rust skill says | This repo does instead |
|---|---|
| `rust-api` (documentation.md): runnable `# Examples` on every public item | `# Examples` is optional and rare. In `regia-cli`, a binary crate, code in docs uses `` ```text `` (comments-rust.md, "Doctests"). |
| `rust-api`: Errors as "Returns an error if:" prose list | One list entry per failure, naming what the caller gets as an intra-doc link (comments-rust.md, "Structure"). |
| `rust-quality` (linting.md): `pedantic` with `missing_errors_doc` and `missing_panics_doc` allowed | Both are `warn`, with `check-private-items = true`. `# Errors`/`# Panics` are never folded away. |
| `rust-tests` (unit-tests.md): tests may live in a separate `*_tests.rs` via `#[path]` | `#[cfg(test)] mod tests` is the last block of the file it tests, under `// == Tests ===`. |
| `rust-tests`: undocumented test helpers | Helpers and fixtures get full item docs in a first `// == Fixtures ===` section. |

If a Rust skill's example code shows a doc or comment style, treat it as
illustrating the Rust technique only and rewrite the comments to this
repo's style.

## Lint configuration

The lints are in `transpiler/Cargo.toml` (`[workspace.lints]`) and
`transpiler/clippy.toml`; the reasons are in comments-rust.md, "Tooling".
Every crate opts in with:

```toml
[lints]
workspace = true
```

Nothing checks the 80-column comment limit, the divider form or the
section order; reviews check those by hand.
