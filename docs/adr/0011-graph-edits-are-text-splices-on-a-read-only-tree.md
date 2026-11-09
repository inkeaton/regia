# Graph edits are text splices computed from a read-only tree

The Visual Editor's graph edits don't change the syntax tree. The Transpiler core reads the tree, works out text edits (replace this range with this text, per file), and the Visual Editor applies them to Monaco and parses again. The text is the only source of truth. Comment ownership is still structural: the tree builder places the comments that belong to a construct inside that construct's node, so a construct's extent is its node's text range.

The preferred design was the other one: make the tree the edit model, as Roslyn and rust-analyzer's `SyntaxEditor` do, then print it and turn the printed difference into text edits. It needs node builders for new constructs, a tree-edit step, a printer, and whitespace created for new nodes, which is a lot to build in a first Rust project (ADR 0010). Graph edits are coarse, files are small and a full reparse is cheap, so text splices are enough for 2.0.

## Considered Options

- **The tree is the edit model** (Roslyn, rust-analyzer `SyntaxEditor`, LibCST). More general, and moved nodes carry their comments without any splice logic. Postponed, not rejected.
- **A read-only index with text splices** (tree-sitter, Lezer, the 1.0 editor's line inserts). Chosen, but on our own lossless tree with ownership fixed by the parser, unlike 1.0's line-number arithmetic.
- **Projectional editing** (MPS). Rejected: the text belongs to the user and stays a first-class view.

## Consequences

- Switching to the tree-as-edit-model later only replaces the code inside the core that computes text edits. These stay the same and are what make the switch cheap:
  - the edit API is made of domain operations (add a Phase, move a construct), never byte offsets;
  - the result is per-file text edits in both designs, so the Visual Editor doesn't notice the switch;
  - ownership is already in the tree's structure;
  - the before/operation/after tests check the new engine against the old one.
- rowan 0.17's `GreenNodeBuilder` and `replace_with` are enough for the later design, so the tree library doesn't block it.
- Every edit costs a full reparse of the changed files. That's acceptable at Regia's file sizes, with a performance budget checked in development (spec chapter 22).
