# An owned, resolved Model sits between the tree and the Targets

The Transpiler has two representations of a Program. The lossless tree holds the text, read through typed accessors that act as the AST. The Model is plain Rust data owned by the core: one per Program, with every name resolved across files and every item pointing back to its place in the tree. Validation, emit, graph views and edit operations all read the Model. The Model keeps the constructs as the designer wrote them, so a Role setup is still a Role setup there. Each Target lowers that sugar when it emits.

Without a Model, every pass would answer "what does `Brawling` mean here?" again by searching every file. The Visual Editor's graph would need the same answers. Owned data with ids also keeps lifetimes on tree nodes out of most of the code, which matters for a first Rust project (ADR 0010).

## Considered Options

- **No Model: passes read the typed accessors directly.** Fewer types, but name resolution, Mapping defaults and precedence get computed again in validate, in each Target and in the graph view.
- **An owned AST plus a Model** (1.0 built an owned AST). An extra copy of the tree's shape with nothing new in it, since the accessors already give typed access.
- **A fully desugared Model** (Role setup turned into Director messages, and so on). Emit gets simpler, but the graph view loses the constructs the designer wrote, and Targets that lower differently can't.
- **A Target-neutral IR after the Model.** Postponed: 2.0 has one Target, and what Targets share is still open.

## Consequences

- The Model is rebuilt from scratch on every change, the same as the full reparse in chapter 22. An incremental engine (salsa) comes in only if the performance budget fails.
- Each Target owns its lowering of sugar, and code shared between Targets is factored out once there is a second Target.
- Edit operations find constructs by structural keys resolved against the Model, never by Model ids, which change on every rebuild.
