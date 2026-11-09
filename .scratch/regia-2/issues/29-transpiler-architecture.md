# Transpiler architecture

Type: grilling
Status: open
Blocked by: 26, 27

## Question

How is the Rust Transpiler put together? Decide:
- The passes and what each hands to the next (parse to lossless tree, typed accessors, AST or not, validate, instance, emit), and whether the 1.0 preprocess pass survives now that comments are in the grammar (spec 02).
- The error model: all errors in one run, hints, one diagnostic format across passes, and how it maps to Monaco markers (`relatedInformation` or Hint markers). Our own diagnostic type or miette.
- The library surface the Visual Editor uses through WASM: parse, diagnostics, the tree view the graph needs, and the domain edit operations that return text edits per file (spec 22). Which data crosses the JS–WASM boundary, and in what shape.
- The crate split (core, CLI, WASM) and import resolution behind an interface, so the core does no file I/O (ADR 0010).

## Comments

- Graduated from the map's fog when [Bidirectional editing model](27-bidirectional-editing-model.md) resolved.
- Keep the handoff constraint in mind: the developer is new to Rust, so prefer fewer, simpler moving parts.
