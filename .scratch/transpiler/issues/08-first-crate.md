# The first crate

Type: implementation
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Goal

`transpiler/crates/regia-cli` exists, and `cargo run` prints one line.

## Spec

Chapter 23, *Crates*. The package is `regia-cli`; the command is `regia` (*The command line*), so the binary target is named `regia`.

## Rust

Book ch 1 (Cargo, packages, `main`). New concept: a workspace member and the binary it builds.

## Test first

An integration test runs the binary and expects the line on standard output. It fails first because the binary prints something else.

## Done when

The test passes; the crate opts into the workspace lints; all four checks of `CLAUDE.md` step 5 are clean; the crate doc comment follows `comments-rust.md`.

## Not here

Arguments and files.

## Resolution

Done on 2026-11-26. `transpiler/crates/regia-cli` is a workspace member; it inherits `version`, `edition`, `publish` and the lints from the workspace. Its binary target is `[[bin]] name = "regia"` with `path = "src/main.rs"`: without `path`, Cargo looks for a bin not named after the package in `src/bin/`. `src/main.rs` beside a later `src/lib.rs` is the layout M3 needs. `tests/cli.rs` runs `env!("CARGO_BIN_EXE_regia")` and checks its line on standard output; it was seen failing first. All four checks clean; `Cargo.lock` is committed with the workspace.

Note for the next crates: `cargo new` made a nested `.git` here; use `cargo new --vcs none`.
