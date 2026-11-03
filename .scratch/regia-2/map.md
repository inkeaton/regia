# Map: Regia 2.0 design

Label: wayfinder:map

## Destination

A complete design spec for Regia 2.0. It covers the language (syntax, constructs, semantics), the instancing layer, the ASL mapping, and the architecture of the Transpiler and Visual Editor. It is written as docs (`GLOSSARY.md`, decision records in `docs/adr/`, spec chapters in `docs/spec/`), with every `#discuss` in `docs/primer/` either resolved or explicitly deferred, and is ready to hand to a separate effort that plans development.

## Notes

- Domain: language design for a BDI-based DSL aimed at game designers. Input is `docs/primer/` (frozen: superseded, never edited), plus the 1.0 code and docs in `1.0/` as a reference.
- Every grilling session calls the `grilling` and `domain-modeling` skills. Settled terms go straight into `GLOSSARY.md` (designer-facing names; BDI and ASL terms only as _Avoid_ aliases). Decision records only when a decision is hard to reverse, surprising, and a real trade-off.
- Readability rules for every syntax decision: as few symbols as possible, plain wording over BDI jargon, modular constructs (primer ch.1).
- Tickets: `.scratch/regia-2/issues/NN-<slug>.md`, with `Type:`, `Status:` and `Blocked by:` lines. The frontier is the open, unblocked, unclaimed tickets, lowest number first. Language core comes first.
- Plan, don't do: no code in this effort, only decisions and docs.

## Decisions so far

<!-- one line per resolved ticket: [title](issues/NN-slug.md): gist -->

- [Research: dynamic plan loading in Jason](issues/23-research-jason-dynamic-plans.md): adding plans at runtime is possible, and source counting handles several Directors; filtering with a belief is simpler and keeps plan order. Nothing reads `priority` today; plan order decides. Input for the ASL mapping and the priority model.
- [Research: implementation language for the Transpiler](issues/25-research-implementation-language.md): Rust is strongest on lossless CST (rowan), WASM and single-binary distribution; C++ means more code by hand; Python struggles with WASM size and single-binary distribution. A Rust core with Python bindings is a sixth option. Input for [Implementation language for the Transpiler](issues/26-implementation-language.md).
- [Research: lossless syntax trees and round-tripping](issues/24-research-lossless-cst.md): lossless means tokens plus whitespace and comments reproduce the source exactly. A rowan/Roslyn-style tree has edit APIs; tree-sitter and Lezer mean patching text and reparsing. Indentation comes from a lexer with an indent stack. Open questions became [Bidirectional editing model](issues/27-bidirectional-editing-model.md).
- [Research: plan conflict resolution in BDI and game AI](issues/13-research-plan-conflict-resolution.md): "priority" is four decisions (event, plan, pre-emption, actions that can't run together). Jason only has source order and `[atomic]`, with `select__option/4` as a hook. JACK layers rank over order, GOAL has a first-vs-all switch, and game AI favours rank plus weight (dual utility). Input for [Priority model](issues/14-priority-model.md).

## Not yet specified

- **The full ASL mapping**: how Playbooks are given and taken away at runtime (after the Jason research), shared infrastructure files instead of copying them into each file, what infrastructure state each agent holds (its Playbooks and which Plots gave them), logging of Agent actions for debugging and runtime verification, generating `.jcm` files.
- **Supporting multiple Targets**: what is shared across Targets vs specific to each, and how Labels and instancing comments map per Target (Jason, plus the custom Python and C++ interpreters as config targets).
- **Transpiler architecture**: the passes (preprocess, parse, CST, AST, validate, instance, emit), what is exposed as a library for the Visual Editor, and the error model (all errors at once, hints, one format across passes, Monaco-compatible). Depends on [Implementation language for the Transpiler](issues/26-implementation-language.md) and [Bidirectional editing model](issues/27-bidirectional-editing-model.md).
- **Visual Editor architecture**: the Transpiler running in-browser (WASM), a file system with folders and tabs, one tab per Plot.
- **What the graph shows**: which elements, toggling layers on and off, staying readable; how doc comments are shown or turned into generated documentation.
- **Testing strategy for the language spec**: how a spec chapter proves itself (examples, conformance cases). Not the development process.

## Out of scope

- Development process, roadmap and milestones: the next effort, once this design is done.
- The custom Python and C++ interpreters, and VEsNA/Godot internals: we only design what Regia emits for them.
- The 1.0 demo game and the questionnaire pipeline.
- The synthetic code generator and benchmarks: tooling for after the Transpiler exists.
- Dialogue trees: a post-2.0 feature; core constructs must be stable first.
