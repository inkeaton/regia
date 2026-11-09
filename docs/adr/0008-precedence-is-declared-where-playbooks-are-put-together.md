# Precedence is declared where Playbooks are put together

When several Playbooks on one Agent could react to the same Trigger, the order between them is written by whoever puts them together, as relations (`Brawling OVER NobleSocializing`), never by the Playbooks themselves and never as numbers. A Plot orders the Playbooks it gives out, its Phases, and its direct Subplots, each Subplot counting together with everything it starts. A Subplot can only refer to the Plot that started it as `PARENT`. Only independent Plots (no common ancestor) are ordered by Instancing (since *Instancing comments*, a Program has one Root Plot, so independent Plots never occur and Instancing orders nothing; see `docs/spec/21-instancing.md`). With nothing declared, a Subplot beats its parent, a Phase beats `DURING PLOT`, and anything else falls back to name order with a warning (`docs/spec/13-plan-selection.md`).

Playbooks are written in isolation and Plots describe only their own scenario (primer ch.2). Whoever decides that two Playbooks end up on the same Agent is the only author who can see both, so that is where the order goes. Ordering Plots as whole subtrees means no author ever names something it can't see, such as a Subplot's internal Playbooks.

## Considered Options

- **Numeric `PRIORITY` on each Plan** (primer, JACK ranks, AgentSpeak(RT)): easy to read locally, but authors working in isolation must guess numbers that only mean something next to Playbooks they can't see. The primer's own examples already use 5, 9 and 10 with no shared scale.
- **Plan-library or include order** (Jason's default): no syntax, but invisible, and it changes when files are reorganised or Playbooks are loaded at runtime.
- **Global layers ordered once** (the proposal's `LAYERS`, subsumption, dual utility): strong guarantees across many Plots, but a Program-wide vocabulary 2.0 doesn't need. Kept as a possible later addition.
- **Naming individual Playbooks across Plot boundaries** (the proposal's story-level `Duelling OVER NobleSocializing`): finer control, but the parent must know the Subplot's internals and breaks when they change.
- **A new top-level `STORY` unit**: one more construct, overlapping the Root Plot.
- **Undeclared competition as a compile error**: stricter, but the Transpiler only knows which Playbooks an Agent can hold, not which are given at the same time, so it would demand relations for pairs that never meet.

## Consequences

- `PRIORITY` is removed from the language.
- Mood (the Selection function) decides only among Mood alternatives and Playbooks declared `TIES`, and never overrides precedence.
- At runtime, each given Playbook carries a rank key built from the Plot tree, and Jason's `selectOption` compares keys instead of trusting plan order.
- Names matter: renaming a Playbook can change what name order decides, which is why it always comes with a warning.
