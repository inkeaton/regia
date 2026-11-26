# Review: how we test

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

What kinds of test does each pass have, and how do Conformance cases run before the Transpiler is whole?

Decide:

- Test kinds per pass, and the dump formats.
- Where the case runner lives, given that the core does no I/O and `regia test` is in `regia-cli`, and that `cargo test` must run it too.
- Whether cases are read in place from `docs/spec/cases/` (chapter 27 leaves vendoring to us).
- The pending list: format, and that a listed case which passes fails the run.
- How an `ok` case is kept from passing only because nothing is reported yet.
- Snapshots: a crate or plain files.

Chapter 27; `docs/standards/comments-rust.md` (test layout).
- Where a standing build for `wasm32-unknown-unknown` goes, from the ticket that adds rowan (*Review: tokens to tree to accessors*).

## Resolution

Agreed with Edoardo on 2026-11-26. The answer is in chapter 23, *Tests*, and chapter 27, *Case files* (cases are read in place).

- **Worked example.** `13-plan-selection/precedence-cycle.regia` through the runner: annotations to an expected set of (severity, code, line), the core's Diagnostics to a reported set, exact comparison. Pending at M2 (the thin parser reports syntax errors on `PLOT`), off the list in the R1301 ticket of M6.
- **Per pass.** scan/layout: unit tests, token-dump snapshots, print-back over the showcase and every case. Parser: tree-dump snapshots (rowan's `KIND@start..end`), print-back. `ast`: unit tests. Model, Validate, Target checks: Conformance cases only. Emit: ASL snapshots plus the `#[should_panic]` test. CLI: integration tests running the binary. Dumps are core functions used by tests; no dump command.
- **Runner.** A `cases` module in a library target of `regia-cli`, called by `regia test` and by `regia-cli/tests/conformance.rs`. Annotation parsing and matching are pure functions with unit tests.
- **In place.** Cases are read from `docs/spec/cases/` through `CARGO_MANIFEST_DIR`; no vendored copy. Chapter 27 edited.
- **Pending list.** `regia-cli/tests/pending.txt`, exact paths relative to `docs/spec/cases/`, `#` comments. Listed and failing: pending. Listed and passing: fails ("remove from pending"). Listed and missing: fails. Unlisted: must pass. No folders. The runner prints failing paths in the list's form.
- **`ok` cases.** No extra guard: red while the parser doesn't know their constructs, then a guard against false positives. The error case, red first, proves a check; a rule's ticket adds both.
- **Skipped.** `regia: 2.0` cases skipped and counted. Behaviour cases: the Entry's Diagnostics checked now, the Trace reported skipped until `regia-jason` (not pending).
- **Snapshots.** `insta`, inline for short dumps, files for ASL, `cargo-insta` installed in the first ticket that uses it; version and API checked with crate-researcher then. expect-test was weighed: lighter and inline-first, weaker for long ASL files reviewed in bulk.
- **WebAssembly.** The ticket that adds rowan adds `cargo build -p regia-core --target wasm32-unknown-unknown` to CLAUDE.md step 5 and `.scratch/implementation/continuous-integration.md`, with `rustup target add wasm32-unknown-unknown` in its *Done when*.
- **Codes.** `regia-core/tests/codes.rs` matches every chapter's `## Transpiler checks` codes against `enum Code`; lands in M3.
- **Teach-back.** Questions a–d (the four verdicts, a passing pending case, why an early-green `ok` case is fine, where the runner lives) were not known and were walked through; then a′ (an unlisted case that starts failing fails the run) and b′ (a listed folder hides any new case) right.
- No ADR: each choice is local to the test suite and cheap to change. No new glossary term: pending list and case runner are the Transpiler's, not the language's.
