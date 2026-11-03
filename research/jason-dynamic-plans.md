# Research: how Jason/JaCaMo agents gain and lose plans at runtime

Status: findings only, no decision. Written for the Regia 2.0 design effort (how Directors give and take away Playbooks).
Date: 2026-11-03.

## Question

How can a Jason agent gain and lose plans at runtime? Compare:

1. `.add_plan` / `.remove_plan`, including Directors pushing plans with `.send` `tellHow` / `untellHow`;
2. `{ include(...) }` (and its runtime twin `.include`);
3. plan labels together with `.relevant_plans` / `.plan_label`;
4. the current Regia v0.2 approach: every Playbook a Role could receive is included in the role file, and each plan is gated by `playbook_active(Name, _)` in its context.

Cover performance, debuggability, how label annotations survive (`priority(N)`, VEsNA-Pro `temper([...])` / `effects([...])`), and VEsNA constraints.

## Sources and how far to trust them

| Tag | Source | Notes |
|---|---|---|
| **[J]** | Jason source, `jason-lang/jason` `master` at commit [`84e131b`](https://github.com/jason-lang/jason/tree/84e131bcdeed694e5176ba7a502c8b382c75490f) (2026-10-30). Paths below are relative to `jason-interpreter/src/main/`. | Primary. Line numbers refer to this commit. |
| **[J3.1]** | `jason-3.1.jar` from the first VEsNA release (`~/Documenti/PhD Kit/1 Ricerca/VEsNA/01 VEsNA (prima versione)/JaCaMo/libs/`) | Used to spot-check that the APIs below already exist in an older release (same `PlanLibrary.add/remove/getCandidatePlans` signatures, same `tellHow`/`untellHow` KQML plans, same "There already is a plan with label" error). |
| **[JD]** | Jason docs in the same repo: `doc/tech/performatives.adoc`, `doc/tech/annotations.adoc`, `doc/release-notes.adoc` | Primary (first-party docs). |
| **[V]** | VEsNA-Pro (temper) sources, `08 vesna-pro (temper).zip`, `vesna-temper/src/agt/vesna/` | Primary for VEsNA. It pins `org.jacamo:jacamo:1.2` (`build.gradle`), so it runs on an older Jason than `master`. |
| **[R]** | Regia v0.2 output in `docs/primer/examples/*.asl` (main checkout, not committed) and the design notes in `docs/first reasonings/` | What Regia emits today. |
| Book | Bordini, Hübner, Wooldridge, *Programming Multi-Agent Systems in AgentSpeak using Jason* (Wiley 2007), ch. 6 (communication: `tellHow`/`untellHow`/`askHow`) | **Not re-read for this note.** Every claim below rests on [J]/[JD]; the book is listed as background only. |

Caveat: VEsNA-Pro runs on JaCaMo 1.2. The core mechanisms below date back many releases (see [J3.1] and [JD]), but line-level details such as the `applyFindOp` fast path, the `l__` label stripping in `.add_plan` and the KQML fast path for `tell`/`achieve`/`signal` were read on `master`. Check them on the pinned version before relying on them.

---

## 1. How the plan library works (the facts every option rests on)

**Indexing.** `PlanLibrary` keeps every plan in an ordered `List<Plan> plans` and also in a hash map `relPlans: PredicateIndicator -> List<Plan>` keyed by the trigger's predicate indicator (operator + type + functor / arity, e.g. `+insult_heard/0`). [J `java/jason/pl/PlanLibrary.java` L36-48; `java/jason/asSyntax/Trigger.java` L196-203]
Plans whose trigger is a variable go into a separate `varPlans` list and are copied into **every** same-type entry. [J PlanLibrary.java L192-203]

**Candidate lookup per event** is one hash lookup: `getCandidatePlans(te)` returns `relPlans.get(te.getPredicateIndicator())`. [J PlanLibrary.java L399-425] So the cost of an event depends on how many plans share **that** trigger, not on how big the whole library is.

**Relevance and applicability.** For each candidate the interpreter unifies the trigger (`isRelevant`) and then evaluates the context (`logicalConsequence`). [J `java/jason/asSemantics/Agent.java` L683-790]
There are two code paths:

- **Fast path `FindOp`.** It stops at the first plan that is relevant and applicable. [J `java/jason/asSemantics/TransitionSystem.java` L646-720]
- **Full path `RelPl` → `ApplPl` → `SelAppl`.** It builds the full relevant list, then evaluates the context of **every** relevant plan, then calls `selectOption`. [J TransitionSystem.java L522-545; Agent.java L739-790]

The full path is used whenever the agent class overrides `selectOption`, or in debug mode (verbose 2). [J TransitionSystem.java L477-480; Agent.java `checkCustomSelectOption` ~L1155-1166] **`vesna.VesnaAgent` overrides `selectOption`** [V `VesnaAgent.java` L217], so VEsNA agents always take the full path: every relevant plan's context is evaluated on every event.

**Default choice is plan-library order.** The default `selectOption` returns the first applicable option. [J Agent.java L631-640] VEsNA-Pro also falls back to `options.remove(0)` when no option carries a `temper` annotation, and breaks ties to the lowest index. [V `VesnaAgent.java` L217-225; `Temper.java` `getMostSimilarIdx`] **Plan order is behaviour.**

**Events are generated only if a plan might care.** Percept additions and deletions are turned into events only `if (ts.getC().hasListener() || pl.hasCandidatePlan(te))`. [J Agent.java ~L865, ~L900] Test-goal events behave the same way. [J TransitionSystem.java L1037] So the presence of a plan, even one whose context can never hold, makes the agent queue events for that trigger. (VEsNA's Godot events arrive as `signal` messages to self and become signal events whether or not a plan exists. [V `VesnaAgent.sense`; J TransitionSystem.java L362-366])

**Label identity.** Labels are keyed by `functor + args` only. **Annotations are not part of a label's identity.** [J PlanLibrary.java `getStringForLabel` L265-275]
Adding a *different* plan under an existing label throws `JasonException("There already is a plan with label ...")`. Adding an *equal* plan only adds a source. [J PlanLibrary.java L155-164; also in [J3.1]]
Plan equality is trigger + context + body. **The label is ignored.** [J `java/jason/asSyntax/Plan.java` L254-263]

**Sources work like reference counts.** `add(p, source, before)` gives an equal existing plan an extra `source(...)` annotation on its label. `remove(label, source)` removes that one source, and drops the plan only when no source is left. [J PlanLibrary.java L112-135, L332-347]

**Running intentions keep their plan.** An `IntendedMeans` keeps a direct reference to the `Plan` and its body. [J `java/jason/asSemantics/IntendedMeans.java` L32-35] Removing a plan from the library does not abort intentions that already use it. The same holds for flipping a gating belief, because contexts are checked only when a plan is selected.

**`[atomic]` blocks event selection.** While an atomic intention exists, `applySelEv` selects no event. [J TransitionSystem.java L395-401] This matters for the races in §3.

**Built-in label annotations** are only `atomic`, `breakpoint` and `all_unifs`. [J Plan.java L32-34; ASSyntax.java L71-73] Jason gives every other label annotation (`priority(N)`, `temper(...)`, `effects(...)`) no meaning. They are inert data that a custom agent class may read.

---

## 2. The mechanisms

### 2.1 `.add_plan(Plans[, Source[, begin|end]])`

- It accepts a plan term `{ ... }`, a string, or a list of either. Source defaults to `self`. Position defaults to `end`; `begin` puts the plan first. [J `java/jason/stdlib/add_plan.java` doc + L111-131]
- Plan terms have been first-class since Jason 1.3, so they can sit in beliefs, be passed as arguments, and be built by unification. [JD release-notes.adoc, "version 1.3", L669-693]
- On `master`, a label whose functor starts with `l__` (an old auto-label) is deleted before the plan is added, and its annotations go with it. [J add_plan.java L159-162] Regia always emits explicit `@pb__...` labels, so this does not bite Regia today. It would bite if the compiler ever dropped explicit labels.
- If any added plan is a goal-state meta-event plan, a goal listener is installed. [J add_plan.java L130-131]

### 2.2 `.remove_plan(Labels[, Source])`

- It takes a label, a list of labels, or a plan term (its label is used). Source defaults to `self`. [J `java/jason/stdlib/remove_plan.java` doc + L101-119]
- **It returns `true` even if no such plan exists.** The return value of `PlanLibrary.remove` is ignored. [J remove_plan.java L113-118] A wrong label fails silently.
- The documented ways to remove sets of plans [J remove_plan.java doc] are
  - `.relevant_plans({+!g}, _, LL); .remove_plan(LL)`, or
  - `for (.plan_label(P, L[url("file:g.asl")])) { .remove_plan(P) }`.

### 2.3 `.send(Ag, tellHow, Plans)` / `.send(Ag, untellHow, Labels)`

- The receiver handles these with the default KQML plans [J `resources/asl/kqmlPlans.asl` L118-130, identical in [J3.1]]:
  ```
  @kqmlReceivedTellHow   +!kqml_received(Sender, tellHow, Content, _)
     <- .remove_source_annot(Content, ContentAn); .add_plan(ContentAn, Sender).
  @kqmlReceivedUnTellHow +!kqml_received(Sender, untellHow, Content, _)
     <- .remove_plan(Content, Sender).
  ```
  So `tellHow` is `.add_plan` with `source(Sender)` and position `end`. `untellHow` is `.remove_plan` with that source. [JD performatives.adoc L42-45]
- **Unlike `tell`/`achieve`/`signal`, there is no fast path.** `tellHow` always becomes a `+!kqml_received` goal, then an intention that runs over later cycles. [J TransitionSystem.java L346-375] The plan reaches the library only when that intention's `.add_plan` step runs.
- Plan terms in the *sender's* code go through `capply(un)` before the send: internal-action arguments are instantiated with the sender plan's current unifier. [J `java/jason/asSemantics/DefaultInternalAction.java` L42-48] A plan term written inside a Director plan therefore gets every variable it shares by name with that Director plan bound (e.g. `Sender`, `Me`, `Agents`). Generated code would need fresh variable names, or should send strings.
- An agent may override the KQML plans: user-defined `kqml_received` plans set `hasUserKqmlReceived`. [J PlanLibrary.java L179-186] That is how a project would make `tellHow` atomic or add plans at `begin`.

### 2.4 `{ include("f.asl") }` and `.include("f.asl"[, NS])`

- The `{ include }` directive runs at **parse time**. It parses the file into a temporary `Agent`, whose components the outer agent then imports. [J `java/jason/asSyntax/directives/Include.java` `process`] Nothing can be "un-included".
- **`.include` is the runtime version** (since Jason 2.0 [JD release-notes.adoc L320]). It calls the same directive and then `importComponents`, `addInitialBelsInBB` and `addInitialGoalsInTS`. [J `java/jason/stdlib/include.java` L60-80; Agent.java L565-591] So it also adds any initial beliefs and initial goals in the file every time it runs.
- Plans loaded from a file get a `url("file:...")` label annotation. [J PlanLibrary.java L174-176] That annotation is the hook the `remove_plan` doc uses to remove "everything from file X".
- `.include` has no source argument: plans always get `source(self)`. Including the same file twice adds `source(self)` to equal plans a second time, which changes nothing. One `.remove_plan` then removes the plan. **No per-Director reference counting.**
- `.include` reads the file again from disk / URL and parses it again on every call.
- The optional namespace argument puts the file's plans and beliefs in `NS`. [J Include.java, namespace handling; `doc/tech/modules-namespaces.pdf`] Triggers then live in `NS::`, so they will **not** react to default-namespace percepts unless the playbook writes `default::` explicitly. That is useful for isolating private helper beliefs, but it changes how triggers match.

### 2.5 Labels, `.plan_label`, `.relevant_plans`

These are **query** tools, not a separate mechanism. They make removal and introspection possible:

- `.plan_label(P, L)`: with `L` bound it returns the plan with that label (a clone, as a plan term, variables made anonymous). With both unbound it **backtracks over a copy of all plans**, so it is safe to call `.remove_plan` inside the `for`. Unification against the label includes annotations, so a pattern such as `L[playbook(noblesocializing)]` or `L[source(D)]` selects by annotation. [J `java/jason/stdlib/plan_label.java` `execute`]
- `.relevant_plans({Trigger}, Plans[, Labels])` returns every plan relevant to a trigger, as clones. [J `java/jason/stdlib/relevant_plans.java`] It powers `askHow` [J kqmlPlans.asl L132-138] and "remove all plans for trigger T".
- Unification cannot match a label functor by prefix, so `pb__NobleSocializing__*` cannot be selected by naming convention alone. To remove a Playbook, either the compiler emits the explicit label list (it knows the labels statically), or every plan carries a marker annotation such as `playbook(noblesocializing)` and removal goes through `.plan_label(P, L[playbook(...)])`.

### 2.6 Current Regia approach: include everything, gate with a belief

From [R] `role_royalbanquet_guest.asl` and `playbook_noblesocializing.asl`:

- `{ include("playbook_noblesocializing.asl") }` sits at the top of the role file, so playbook plans come **before** the role's own plans in library order.
- Every playbook plan context starts with `playbook_active(noblesocializing, _) & ...`.
- `+!add_playbook(Name)[source(S)]` / `+!remove_playbook` add or remove `playbook_active(Name, S)`. `+!plot_ended(P)` removes `playbook_active(_, P)`.
- None of these management plans is `[atomic]`.

---

## 3. Comparison

Options considered:

- **A.** Status quo: include all, gate with a belief.
- **B.** The role agent `.include`s the playbook file at runtime, and removes it with a `.plan_label` filter on `url(...)` or on a marker annotation.
- **C.** The role agent `.add_plan`s plan terms it already holds (e.g. from a generated rule or belief `playbook_plans(Name, [...])`), with `Source = Director`.
- **D.** The Director pushes plans with `tellHow` and withdraws them with `untellHow`.

Labels, `.plan_label` and `.relevant_plans` are the removal and introspection layer for B, C and D (§2.5).

### 3.1 Semantics

| Concern | A: gate belief | B: `.include` | C: `.add_plan` role-local | D: `tellHow`/`untellHow` |
|---|---|---|---|---|
| Two Directors give the same Playbook | Natural: two `playbook_active(N, D)` beliefs | No refcount (`source(self)` only); Regia must count | Built-in refcount through `source(D)` (§1) | Built-in refcount through `source(Sender)` |
| Plot ends and cleans up | `-playbook_active(_, P)` | Remove by `url`/marker; refcount is Regia's problem | `for (.plan_label(X, L[source(P)])) {.remove_plan(X, P)}` | Same as C, or the Director sends `untellHow` with the label list |
| Director dies without cleanup | Ghost beliefs remain | Ghost plans remain | Ghost plans with `source(dead)` remain | Same as C |
| Order relative to role plans | Playbooks first (include at top) | Appended at end | `end` by default, `begin` available | Always `end` unless the KQML plans are overridden |
| Event arriving right after assignment | Race: `+!add_playbook` is not atomic | Race unless the include runs inside an `[atomic]` plan | Same; fixable with `[atomic]` (§1) | Race is structural: `tellHow` is a non-atomic KQML intention (§2.3); fixable only by overriding the KQML plans |
| Intentions already running when a Playbook is removed | Keep running | Keep running | Keep running | Keep running |
| `-!g` failure plans inside a removed Playbook | Present but gated, so failures look unhandled | Gone | Gone | Gone |
| Where the plan text lives | Role file (all playbooks) | Separate files, read at runtime | Role file or generated data, outside the plan library | Director file, as plan terms or strings |
| Identical plans in two Playbooks | Never identical (each context names its playbook) | Merged into one plan (equality ignores label); removing by the second label silently does nothing | Same merge hazard | Same merge hazard |

That last row is a real hazard. Without the gate, two Playbooks containing the same `WHEN` (same trigger, context, body) produce *equal* plans. `PlanLibrary.add` merges them under the first label [J PlanLibrary.java L115-129], and `.remove_plan` on the second label does nothing and reports success [J remove_plan.java L113-118].

### 3.2 Performance

No benchmark was run for this note. These points come from reading the code.

- **Cost per event** = (number of candidates with the same trigger PI) × (trigger unification + context evaluation). Under VEsNA, *every* candidate's context is evaluated, because the custom `selectOption` forces the full path (§1).
- **A**: every Playbook the Role *could* receive adds candidates for its triggers, active or not. Inactive ones fail at the first conjunct `playbook_active(N, _)`. That is a belief-base lookup by predicate indicator, then a scan over the `playbook_active` facts, so it is cheap but not free. A also makes the agent **queue events** for every trigger mentioned in any included playbook, because `hasCandidatePlan` is true (§1). Those events are dropped after the failed context checks. For Godot `signal` events this changes nothing, since they are queued anyway.
- **B / C / D**: only active Playbooks are candidates, and percept events for triggers that no active plan handles are never created. The extra costs come at assignment time:
  - `add`: O(1) amortised per plan, plus a pass over `varPlans` the first time a trigger PI is seen.
  - `remove`: O(n) `ArrayList.remove` over the whole `plans` list and the PI's list. [J PlanLibrary.java L350-389]
  - B parses the file from disk again on every `.include`. Strings in C/D are parsed on every add (`ASSyntax.parsePlan`); plan terms are not.
- At the expected scale (tens to low hundreds of plans per Role, few plans per trigger), the gap is likely small either way. If it matters, the thing to measure is plans-per-trigger under VEsNA's full path, not total library size.

### 3.3 Debuggability

- **A**
  - The Mind Inspector shows every plan, including inactive ones. Which Playbooks are active shows only as `playbook_active/2` beliefs.
  - When an `achieve` arrives for an inactive Playbook, Jason reports "no **applicable** plan". If no `-!` handler exists, it re-evaluates and logs every candidate's context at FINE level, so the failing `playbook_active` conjunct is visible. [J TransitionSystem.java L554-585]
  - Every emitted context has an extra conjunct, and the `else` branches become `playbook_active(...) & not(...)` ([R] `pb__NobleSocializing__insult_heard__1`).
- **B / C / D**
  - The library shows exactly what the agent can do now.
  - Each plan's label carries `source(Director)` (C/D) or `url(file)` (B). The plan library's text dump (`getAsTxt`) groups plans by source file and puts plans added from strings or terms under "plans without file". [J PlanLibrary.java `getAsTxt` L465-496] So in C/D provenance comes from the `source` annotation, not the file.
  - An `achieve` for a missing Playbook reports "no **relevant** plan", which is clearer but carries less context.
  - The silent `true` from `.remove_plan` and the label-merge hazard (§3.1) can hide errors.
  - The behaviour now depends on assignment history (the order of `add_plan` calls), not only on the source files, so a run is harder to reproduce from the files alone.

### 3.4 Do label annotations survive?

| Path | Label annotations (`priority`, `temper`, `effects`, custom markers) | Added or removed |
|---|---|---|
| `{include}` / `.include` | Kept (parsed as written) | `+source(self)`, `+url("file:...")` [J PlanLibrary.java L170-176] |
| `.add_plan` with a plan term or string | Kept (`ASSyntax.parsePlan` / term as is). Exception: the whole label is dropped if its functor starts with `l__` (master) [J add_plan.java L159-162] | `+source(S)` |
| `tellHow` | Kept: `remove_source_annot` deletes only `source(...)` from the label [J `stdlib/remove_source_annot.java` `processTerm`; Pred.java `delSources` L507-519] | Sender's sources stripped, then `+source(Sender)` |
| `.plan_label` / `.relevant_plans` (to copy or forward a plan) | Kept on a clone, including `source`/`url`; variables renamed to anonymous ones | none |
| Plan-term text round trip | `toASString` prints `@label[annots]` [J Plan.java L338-342] | none |

- **VEsNA-Pro reads annotations from the selected plan's label at decision time.** `Temper.computeWeight` reads `label.getAnnot("temper")`. `selectIntention` reads `getAnnot("effects")` on the intention's top plan and applies the mood changes. [V `Temper.java` L89-118, L160-180; `OptionWrapper.getLabel`] It caches nothing at load (`initTemper` parses only the `.jcm` temper and strategy [V `VesnaAgent.initTemper`]). So plans added at runtime take part in temper selection exactly like included ones. The extra `source(...)` / `url(...)` annotations do not interfere, because it looks up annotations by functor.
- **`priority(N)` is inert today.** Neither Jason (§1) nor VEsNA-Pro reads it ([V] has no occurrence of `priority`). The Regia design notes already flag PRIORITY as unimplemented ([R] `docs/first reasonings/2 - Language Architecture.md` L13, `4 - Plans and Playbooks.md` L36). Under every option, what actually decides between applicable plans is **library order**, and under VEsNA-Pro the temper distance with ties going to the lowest index. Option B/C/D appending at `end` therefore changes which plan wins compared with A, where playbooks are included first.

### 3.5 VEsNA constraints found

1. `VesnaAgent` overrides `selectOption` (and `selectIntention`), so Jason always takes the full relevant-and-applicable path. Plans per trigger cost more than under stock Jason (§1, §3.2).
2. Temper selection works with dynamically added plans (§3.4). Nothing in VEsNA-Pro assumes a fixed plan library.
3. Godot events reach the mind as `signal` messages to self [V `VesnaAgent.sense`] and become `+event[signal, source(self)]`-style events regardless of plans. So option A's "extra events" cost applies only to percepts and beliefs, not to VEsNA signals.
4. VEsNA-Pro pins JaCaMo 1.2 (older Jason). See the caveat under *Sources*.
5. Incidental, outside this ticket: in `Temper.updateDynTemper`, a mood that would go below `-1.0` is clamped to `0.0`, not to `-1.0` [V `Temper.java`, `updateDynTemper`]. This looks like a bug.

---

## 4. Summary of the options (no recommendation)

- **A: status quo (include all + gate belief).**
  - Simple, static, reproducible from the files, and multi-Director semantics are natural.
  - Costs: every possible Playbook is a candidate on every relevant event (all contexts evaluated under VEsNA), percept events are queued for triggers no active Playbook handles, every context carries an extra conjunct, and the role file grows with every Playbook it might receive.
- **B: runtime `.include`.**
  - Keeps playbooks as separate files and the library minimal.
  - Costs: no per-source refcount, a disk read and parse on every assignment, it also replays any initial beliefs and goals in the file, and removal needs `url(...)` or marker filtering.
- **C: role-local `.add_plan` with `Source = Director`.**
  - Minimal library, built-in refcount through sources, can be made race-free with `[atomic]`, and `begin` keeps playbook-first ordering.
  - Costs: the plan text still has to live somewhere the role can reach (generated data or rules), a silent no-op removal on a wrong label, and identical plans across Playbooks merge.
- **D: Director-side `tellHow` / `untellHow`.**
  - Same library and refcount benefits as C, and the plans live with the Director that owns the Playbook.
  - Costs: plan terms are instantiated with the Director's unifier, plans are always appended at `end`, there is a structural race between `tellHow` and the Director's next message unless the KQML plans are overridden, and the merge and silent-removal hazards are the same as C.
- **Shared building blocks** for B, C and D: a `playbook(Name)` marker annotation on every generated label, and `.plan_label(P, L[playbook(N)])` or `L[source(D)]` for removal and introspection. Annotations survive every path, so this is cheap.

## Open questions for the decision

- Does Regia want Playbook-first or Role-first precedence? Today it is an accident of include placement, and it decides between applicable plans while PRIORITY is unimplemented.
- Should a removed Playbook also abort its running intentions (e.g. `.drop_intention` by label or annotation)? No option does this by itself.
- Is it acceptable for generated Playbooks to contain identical plans? If yes, B/C/D need a way to keep them from being equal. Equality ignores labels, so this means a distinguishing context or body element.
- Measure plans-per-trigger under VEsNA's full path at a realistic scale before treating performance as a deciding factor.
