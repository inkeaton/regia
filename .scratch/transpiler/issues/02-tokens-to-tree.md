# Review: tokens to tree to accessors

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 01

## Question

How do tokens become a lossless tree, and what do accessors promise?

Work by hand: the tree of one `WHEN` with a trailing comment and one Error node, and its accessors.

Decide: the parser's marks and events; how Error recovery picks its known tokens; where ownership of comments happens; what an accessor returns for a missing part; how a 2.0 construct is parsed for `R0109` and a retired spelling for its own code; how the `syntax` module hides rowan.

Chapters 01, 22, 23; ADRs 0010, 0011.

## Resolution

Agreed with Edoardo on 2026-11-25. The answer is in chapter 23, *From tokens to the tree*.

- **Parser and tree builder.** The parser writes events and never sees a comment. The tree builder alone applies the Extent rules and touches rowan. `R0203` is a look at the finished tree.
- **Rule 2.** A trailing comment and its NEWLINE go to the outermost construct that started on that line and ends there (chapter 22).
- **Recovery.** Soft errors skip nothing; a hard error is one Error node up to a known token, at most one per Statement or header. Soft or hard is not a property of a code: `R0115` can be either.
- **Loose grammar.** Misplaced constructs parse, and a later check reports them. `PRECEDENCE`, `KIND`, `AGENT` and `TARGET` bodies have their own grammar.
- **Accessors.** `Option` or an iterator, never a report; names are tokens.
- **Retired spellings** become the new spelling's node. **`R0109`**: the parser where tokens show it, Validate for a Goal's ending in a Plot.
- **Broken for graph edits** means a lexer or parser error inside the Extent.
- **rowan.** INDENT and DEDENT stay out of the tree; `syntax` wraps rowan in newtypes; nothing stores a node.
- **WebAssembly, checked 2026-11-25.** rowan 0.17.0 with Rust 1.100.0 built for `wasm32-unknown-unknown` (64 KB release, no imports) and ran in Node 26: builder, checkpoint, print-back, ranges, parents. Not covered: `wasm-bindgen`, a browser. The target isn't installed in the user's toolchain (`rustup target add wasm32-unknown-unknown`).
- **For *Review: how we test*:** place a standing build for `wasm32-unknown-unknown`, from the ticket that adds rowan.
- **For *Review: files to Model* and *Diagnostics and where checks live*:** leaving a Plan out of the Model must not cause new Diagnostics (a Cue that then looks unused), and the Goal's-ending `R0109` is known only once names are resolved.
- **Teach-back.** The user worked a second example (two Plans, a missing `:`, `CHANGE`, a stray `)`), and placed the boundary.
- No ADR: each choice is local to `syntax` and cheap to change.
