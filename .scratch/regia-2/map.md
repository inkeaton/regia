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
- [Statement and block syntax](issues/01-statement-and-block-syntax.md): indentation and explicit `.`/`;` mix freely; every header (`PLOT` too) ends with `:`; a body on the header's line is an Inline block ending at `;` or at the end of the line; `.` ends a Statement only before a space or the end of the line; Python indentation rules; `,`/`(` continue lines. Spec: `docs/spec/01-statements-and-blocks.md`.
- [Comment syntax](issues/02-comment-syntax.md): `#` / `#[ … ]#` (nestable) for plain comments, `#@key:` / `#@key[ … ]#` for doc comments, `#%` / `#%[ … ]#` reserved for Instancing comments; `## … ##` dropped. Doc comments are grammar nodes attached to the declaration directly below; open key set (`desc`, `author`, `version` known). Spec: `docs/spec/02-comments.md`.
- [Parameters and variables](issues/03-parameters-and-variables.md): every kind of Vocabulary item takes untyped parameters, Events included. A slot holds a Value or a Placeholder (`?name`): a blank filled by matching in the Trigger or Context, once per Plan run, never reassigned. Only what's certainly filled can be used. Which match is used is unspecified. Spec: `docs/spec/03-parameters-and-placeholders.md`, ADR 0001.
- [Numbers and arithmetic](issues/04-numbers-and-arithmetic.md): one Number kind; `< > <= >= =` and `+ - * /`; `RANDOM(a, b)` inclusive. The Context only tests (`=` compares); a Body names values with `?name = Expression.`, once and never reassigned. Non-Numbers make a Context comparison false and Body arithmetic fail the Plan. Spec: `docs/spec/04-numbers-and-expressions.md`, ADR 0002.
- [Goals and Trigger kinds](issues/05-goals-and-trigger-kinds.md): achievement Goals only, declared like Facts, reached when their Plan finishes; Events are momentary; Trigger kinds are `WHEN e:`, `WHEN f LEARNED/FORGOTTEN:`, `TO g:`, `WHEN g DROPPED:`; `WHEN` replaces `ON`; `FROM Role ?who` / `FROM DIRECTOR` on anything sent. Spec: `docs/spec/05-goals-and-triggers.md`, ADR 0003.
- [Context vs control flow](issues/06-context-vs-control-flow.md): `GIVEN` is the Context, a Block under the Trigger; several `GIVEN`s share a Trigger, first match in the text wins, optional `ELSE`, no prefix Statements. `IF`/`ELSE IF`/`ELSE` are Body Statements; their Placeholders live in their branch. `AND`/`OR` mixing needs parentheses. ASL: negate earlier siblings with fresh names. No loops. Spec: `docs/spec/06-context-and-control-flow.md`, ADR 0004.
- [Messaging between Agents](issues/08-messaging.md): `TELL <recipient> <fact or event>`, `ASK <recipient> TO <goal>`, `SIGNAL <event>` (to every Director giving the Playbook). Recipients are a filled Placeholder, a Role or `EVERYONE` (`BROADCAST` gone), never a named Agent. Messages only add; sending never waits. A told Fact is the receiver's own, with no source; `LEARNED FROM` fires only if new. Cooperation words reserved (`REFUSE`, `AGREED`/`REFUSED`/`REACHED`/`FAILED`, `TOLD`, trailing clauses). Spec: `docs/spec/07-messaging.md`.

## Not yet specified

- **Match selection**: explicit ways to choose among a Context's matches (pick one at random, run for every match, rank by priority or by a value). Also the place for any looping construct, since 2.0 has no `WHILE`/`FOR`. Related to [Groups](issues/09-groups.md) and [Priority model](issues/14-priority-model.md).
- **Sugar and math over Numbers**: a shorthand comparison on a one-slot Fact (`health < 20`), a small math library (`abs`, `round`, `min`, `max`), and naming values in a Context (`?x = …`) if repeated Expressions hurt. Revisit once the core constructs are stable.
- **Richer Goals and Events**: Goals kept true (maintenance) or reached when a Fact holds (declarative); `FROM SELF`; renaming `EVENT` to `CUE` so "Event" can become the umbrella term. Revisit once the core constructs are stable.
- **Optional parameter types** (`param: type`): for Transpiler checks and Visual Editor hints. Not in 2.0's core. Revisit once the core constructs are stable.
- **The full ASL mapping**: how Playbooks are given and taken away at runtime (after the Jason research), shared infrastructure files instead of copying them into each file, what infrastructure state each agent holds (its Playbooks and which Plots gave them), logging of Agent actions for debugging and runtime verification, generating `.jcm` files.
- **Supporting multiple Targets**: what is shared across Targets vs specific to each, and how Labels and instancing comments map per Target (Jason, plus the custom Python and C++ interpreters as config targets). Includes per-Target lowering of control flow (Jason's native `if` vs subgoal plans for the in-house interpreters, chosen with an Instancing comment such as `ASL_VERSION`), depending on what each interpreter supports: suspending subgoals, `not` and `|` in contexts, failure propagation from a subgoal. See spec 06's ASL mapping notes.
- **Transpiler architecture**: the passes (preprocess, parse, CST, AST, validate, instance, emit), what is exposed as a library for the Visual Editor, and the error model (all errors at once, hints, one format across passes, Monaco-compatible). Depends on [Implementation language for the Transpiler](issues/26-implementation-language.md) and [Bidirectional editing model](issues/27-bidirectional-editing-model.md).
- **Visual Editor architecture**: the Transpiler running in-browser (WASM), a file system with folders and tabs, one tab per Plot.
- **What the graph shows**: which elements, toggling layers on and off, staying readable; how doc comments are shown or turned into generated documentation.
- **Testing strategy for the language spec**: how a spec chapter proves itself (examples, conformance cases). Not the development process.
- **Agent cooperation and undoing Messages**: a receiver refusing an `ASK` (`REFUSE`), replies to the asker as Goal kind words (`AGREED`, `REFUSED`, `REACHED`, `FAILED`), trailing clauses on message Statements (wait, timeout, expect reply), negotiation; Messages that make another Agent forget a Fact or drop a Goal; Fact provenance (`WHEN f TOLD FROM ?who`). Words reserved in spec 07. Post-2.0 unless the core needs it.

## Out of scope

- Development process, roadmap and milestones: the next effort, once this design is done.
- The custom Python and C++ interpreters, and VEsNA/Godot internals: we only design what Regia emits for them.
- The 1.0 demo game and the questionnaire pipeline.
- The synthetic code generator and benchmarks: tooling for after the Transpiler exists.
- Dialogue trees: a post-2.0 feature; core constructs must be stable first.
