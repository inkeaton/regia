# Print-back over the showcase and every case

Type: implementation
Status: open
Assignee:
Blocked by: 33

## Goal

Every file in `docs/showcase/` and `docs/spec/cases/` lexes and prints back byte for byte, and a showcase file has a token-dump snapshot. M1 is done.

## Spec

Chapter 23, *Tests*: print-back over every showcase and case file; cases are read in place through `CARGO_MANIFEST_DIR` (*Review: how we test*). The core does no I/O; its integration test does.

## Rust

Walking a directory with `std::fs::read_dir` (ahead of ch 12), `env!("CARGO_MANIFEST_DIR")`, and a test that collects every failing path before failing, instead of stopping at the first.

## Test first

The test in `regia-core/tests/print_back.rs`, run before any fix: whatever fails is a lexer bug to fix, one by one. A file snapshot of `docs/showcase/playbooks/courtesy.regia`'s dump, read through once.

## Done when

The test passes over every file; the snapshot is accepted; the four checks are clean.

## Not here

Checking the Diagnostics of the cases (the case runner, M3).
