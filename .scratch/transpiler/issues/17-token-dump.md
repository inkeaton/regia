# The token dump

Type: implementation
Status: open
Assignee:
Blocked by: 16

## Goal

A dump function prints one token per line, and the first `insta` snapshot holds one.

## Spec

Chapter 23, *Tests*: one token per line with its kind, range and text; virtual tokens with empty text. Dumps are functions of the core used by tests; there is no dump command.

## Rust

An external crate as a dev-dependency (Book ch 7, *Using External Packages*, met in ch 2). Building a `String` with `format!` and `push_str`. Check `insta`'s current version and inline-snapshot API with crate-researcher and docs-researcher first; install `cargo-insta`.

## Test first

An inline snapshot of the dump of `WHEN food_served\n`, written empty, filled and reviewed with `cargo insta review`.

## Done when

The snapshot is accepted after reading it; the four checks are clean.

## Not here

File snapshots (ASL, M7).
