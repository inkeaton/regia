# Regia: Plan Precedence and Composition (Proposal)

Nov 5, 2026 · @Mari

## Status and scope

This is a draft proposal for discussion, not an accepted design. It proposes how Regia lets authors declare precedence between plans of independently written playbooks, and how the compiler and runtime resolve it deterministically.

**In scope**

- Precedence between WHEN blocks of different playbooks that react to the same trigger, on the same agent.
- Precedence between WHEN blocks of a Director (`DURING PLOT` vs `DURING <phase>`).
- Declaring whether competing WHEN blocks are exclusive or may all run.
- How static precedence interacts with TEMPER-based selection (VEsNA).
- A new story-level compilation unit that fixes the starting plot.

**Out of scope**

- Playbooks loaded at runtime that the compiler has never seen. Today every playbook is known at compile time; this proposal relies on that.
- Intention scheduling between unrelated events (which running intention progresses next).
- Changes to how TEMPER scores options.

## Problem

Playbooks are written in isolation, but an agent can hold several at once, and several may react to the same event. Today the winner is decided by accident: the order of `{ include }` lines and of WHEN blocks in the generated ASL.

What the Regia v0.2 output does now:

1. **`PRIORITY` is an annotation only.** It compiles to `[priority(5)]`. Jason's default option selection ignores annotations and takes the first applicable plan in plan-library order.
2. **One plan per event.** For an external event such as `+insult_heard`, Jason runs exactly one applicable plan. A second active playbook handling the same event is silently skipped.
3. **IF/ELSE branches never compete.** They compile to plans with mutually exclusive contexts, so the real unit of competition is the WHEN block, not the plan.
4. **Fall-through exists but is unspecified.** A WHEN with `IF` and no `ELSE` (for example `digestion_check`) is simply not applicable when the condition fails, so a lower-ranked handler runs instead.
5. **An agent's playbooks span plots.** `START SUBPLOT HonorDuel MAPPING Guest TO Challenger` makes a Guest agent also a Challenger, but the Guest role file only includes RoyalBanquet's playbooks. Any playbook assigned to Challenger would be missing.
6. **Directors have the same issue.** A `DURING PLOT` handler and a `DURING <phase>` handler for one event are ordered only by file position.

## Goals and requirements

The design must let authors state precedence where they have the knowledge to do so, and must never leave the outcome to file order.

| ID | Requirement |
| --- | --- |
| R1 | Playbooks stay authorable in isolation: a playbook never needs to name another playbook to be valid. |
| R2 | Precedence can be declared between whole playbooks or between individual WHEN blocks. |
| R3 | Precedence is declared at composition: in the plot that assigns playbooks, or in a story that combines plots. |
| R4 | Given the same agent state and the same event, selection is deterministic. |
| R5 | Selection never depends on include order, file order or load order. |
| R6 | Authors can say that competing WHEN blocks should all run, in a declared order. |
| R7 | Authors can leave a choice to TEMPER on purpose, and only on purpose. |
| R8 | Contradictions are compile errors; undeclared competition is a compile error. |
| R9 | The runtime contract is small enough to implement on targets other than Jason. |

## Terminology

| Term | Meaning |
| --- | --- |
| Handler | One WHEN block in a playbook or Director, identified as `Playbook.label` or `Playbook.<event>#<n>`. All its IF/ELSE branches form one handler. |
| Trigger | The event, signal or lifecycle hook a handler reacts to (`insult_heard`, `ROLE Guest SIGNALS insult_thrown`). |
| Candidate | A handler whose playbook is active and at least one of whose branches would fire now. |
| Competitors | Two or more handlers with the same trigger that may be candidates on the same agent at the same time. |
| Agent kind | An agent identified by its entry role in the starting plot (for example `Guest`), with every role it can reach through subplot mappings. |
| Precedence graph | A directed graph over handlers; an edge `a → b` means a beats b. |
| Tier | An equivalence class of handlers after resolution. Lower tier number = higher precedence. |
| Combination mode | Per trigger: `EXCLUSIVE` (one handler runs) or `ALL` (every candidate runs, in order). |

## Syntax

Precedence is written at three levels. Each level only states what its author can know: the playbook author knows its own handlers, the plot author knows what it assigns, and the story author knows the whole graph.

### Playbook level (author-local, optional)

A playbook may name a layer and label its handlers. It never names another playbook (R1).

```
PLAYBOOK NobleSocializing LAYER social:

    WHEN insult_heard AS retort PRIORITY 5 TEMPER sympathy(-0.5) EFFECTS aggressiveness(0.2):
        ...
```

- `LAYER <name>` is a vocabulary word. Its position is fixed later, by the story (CSS cascade layers work the same way).
- `AS <label>` names the handler. Unlabelled handlers are addressed as `Playbook.<event>#<n>`, counting from 0 in source order.
- `PRIORITY <int>` keeps its current meaning as an author hint. It only breaks ties inside a layer (see Semantics).

### Plot level

A plot may order the playbooks it assigns, inside a `PRECEDENCE` block or as a shorthand on `ASSIGN`.

```
PLOT RoyalBanquet.
    ...
    PRECEDENCE:
        Brawling OVER NobleSocializing.
        NobleSocializing.retort OVER Drunkard ON insult_heard.
        NobleSocializing WITH Gossip ON food_served.

    DURING feast:
        ON ENTER:
            ASSIGN Brawling TO Guest OVER NobleSocializing.
```

### Story level (new compilation unit)

A story fixes the starting plot, the layer order and cross-plot precedence per agent kind.

```
STORY Banquet:
    START RoyalBanquet.
    LAYERS reflex, safety, social, idle.

    PRECEDENCE FOR Guest:
        Duelling OVER NobleSocializing.
        NobleSocializing TIES Drunkard ON digestion_check.
        NobleSocializing WITH Gossip ON food_served PARALLEL.
```

### Relation statements

All three precedence blocks share one statement form:

```
relation  := selector OP selector [ON trigger] [PARALLEL] "."
OP        := OVER | TIES | WITH
selector  := Playbook | Playbook.label | Playbook.<event>#<n>
```

| Statement | Meaning |
| --- | --- |
| `A OVER B` | Every competing handler of A beats every competing handler of B. |
| `A OVER B ON e` | Same, restricted to trigger `e`. |
| `A.lbl OVER B` | One handler of A beats B's handlers on the same trigger. |
| `A TIES B ON e` | Same tier on purpose: TEMPER decides between them. |
| `A WITH B ON e` | Trigger `e` becomes `ALL` mode for these handlers; A runs before B. |
| `... PARALLEL` | With `WITH` only: handlers start concurrently, with no ordering guarantee between them. |

Layers are listed lowest-first or highest-first: see open question Q2.

## Semantics

Resolution happens at compile time, separately for each agent kind K and each trigger e. The result is an ordered list of tiers; at runtime the best-tier candidate wins.

&#91;embedded content: precedence resolution · 4 compile steps, 4 runtime steps\]

The top row runs once in the compiler; the runtime only reads the emitted tier table.

### Candidates and fall-through

A handler is a candidate when its playbook is active on the agent and at least one of its branches would fire. A handler with an `ELSE` is a candidate whenever its playbook is active. A handler whose `IF` fails and has no `ELSE` is not a candidate, so the next tier gets the event. This makes today's accidental fall-through the specified behaviour.

### Building the precedence graph

1. **Collect handlers.** H(K, e) = every handler with trigger e in any playbook that K can hold (see Story reachability).
2. **Expand selectors.** `A OVER B ON e` becomes an edge from each of A's handlers on e to each of B's. Without `ON`, the statement applies to every trigger A and B share.
3. **Merge ties.** `TIES` puts handlers into one class. A class is treated as a single node from here on.
4. **Add edges by level.** Story relations first, then the relations of every plot K can reach. A plot edge that contradicts an accepted story edge is dropped, with a note in the compile report.
5. **Check cycles.** A cycle left after step 4 is a compile error that prints the cycle path.

### From graph to tiers

Tiers come from a topological sort (Kahn's algorithm) that, at each step, takes the ready node with the best key:

1. layer position, from the story's `LAYERS` list (an unlayered playbook sits in an implicit default layer, see Q3);
2. `PRIORITY`, higher first;
3. stable key: playbook name, then handler index.

Each node becomes its own tier, so tiers are a strict order except inside `TIES` classes. Explicit relations always beat layers and priorities; layers and priorities only order handlers that the relations leave unordered. Because tiers are computed over everything K can ever hold, restricting them to the playbooks active at runtime still gives a valid order.

### Combination modes

- Default mode is `EXCLUSIVE`: only the best-tier candidate runs.
- `WITH` relations group handlers into co-run groups (connected components over `WITH`).
- When the winning candidate belongs to a co-run group, every other candidate in that group also runs, in tier order. Candidates outside the group do not run.
- `PARALLEL` on a group starts its handlers concurrently instead of in sequence.

### Directors

Director handlers follow the same rules, with one extra default key: a `DURING <phase>` handler beats a `DURING PLOT` handler for the same trigger (specificity). `PRIORITY` overrides specificity, which keeps the current `assassin_spotted PRIORITY 9` working as intended. Remaining ties fall back to source order, which is acceptable here because a Director has a single author.

### Diagnostics

| Situation | Result |
| --- | --- |
| Cycle in the precedence graph | Error, with the cycle path |
| Two relations at the same level contradict each other | Error, naming both statements |
| `TIES` between handlers already ordered by an edge | Error |
| Selector names a playbook or label that does not exist | Error |
| Selector names a playbook K can never hold | Warning; the relation is ignored |
| Competitors ordered only by the stable key | Error: undeclared competition |
| `TIES` across different layers | Warning; the class takes the best member's layer |
| Plot relation overridden by the story | Note in the compile report |

## Story reachability and conflict detection

The story's `START` plot lets the compiler compute, for each agent kind, every playbook it may hold in its lifetime. That set decides what each agent's code includes and which handlers can compete.

### Reachability

1. Each role of the starting plot defines an agent kind: `Guest` and `Host` for RoyalBanquet.
2. Walk the plot graph from (start plot, role). At each (plot P, role r): add every playbook P assigns to r; for every `START SUBPLOT Q MAPPING r TO r2`, visit (Q, r2).
3. Stop at a fixed point. A plot reached twice is visited once per role, so recursive subplots terminate.

For the example, kind `Guest` reaches (RoyalBanquet, Guest) and (HonorDuel, Challenger), so it may hold NobleSocializing plus anything HonorDuel assigns to Challenger.

Consequence for code generation: one agent file is generated per agent kind and includes every reachable playbook. This replaces the current per-(plot, role) inclusion, which misses playbooks from subplots.

### Conflict report

For every agent kind and trigger with two or more handlers, the compiler lists how the competition was resolved:

```
Guest, insult_heard:
  1. NobleSocializing.retort   (relation: story)
  2. Drunkard.insult_heard#0   (relation: story)
Guest, digestion_check:
  1. {NobleSocializing.digestion_check#0, Drunkard.digestion_check#0}  TIES -> TEMPER
error: Guest, food_served: Gossip and Feasting are ordered by name only; declare a relation
```

### Two precision levels

- **v1, reachable:** two handlers compete if both playbooks are reachable for the kind. Simple and safe, but it raises errors for pairs that can never be active together, forcing declarations nobody needs. Since undeclared competition is an error, this makes v2 more pressing.
- **v2, co-active:** two handlers compete only if their playbooks may be active at the same time. Assignment happens on phase entry and removal on phase exit, and subplots start in known phases, so active intervals can be computed over the phase graph (a may-happen-in-parallel analysis). This removes false warnings and can be added later without changing the language.

## Runtime contract

All graph work happens in the compiler. A runtime only needs a tier table and a three-step selection rule, which in Jason fits inside the VEsNA `selectOption` override.

### Where the tiers live

Tiers depend on the agent kind, but playbook files are shared between kinds. So tiers are not written into plan annotations. Instead:

- each handler has a stable id, and the trigger plans that `selectOption` sees carry it as a `handler(<id>)` annotation;
- each agent-kind file carries a table of `prec_tier(<handler id>, <tier>)` beliefs for that kind.

The existing `priority(N)` annotation is no longer read at runtime. `PRIORITY` only feeds the compile-time ordering.

### Selection in `EXCLUSIVE` mode

Given the applicable options for one event (Jason has already checked contexts, so fall-through is automatic):

1. **Filter.** Keep the options whose handler has the best (lowest) tier.
2. **Temper.** If more than one remains, which only happens inside a `TIES` class, apply the existing VEsNA TEMPER selection to them.
3. **Stable key.** Break any remaining tie by handler id.

All branches of one handler share its tier. They have mutually exclusive contexts, so at most one of them is applicable.

Infrastructure plans (`add_playbook`, `plot_ended`, and so on) carry no `handler` annotation and never share a trigger with a handler. A shared trigger is a compile error, so the filter never has to compare the two.

### `ALL` mode (`WITH` groups)

`selectOption` returns a single option, so co-run groups cannot be handled there. For each trigger that has a co-run group, the compiler generates a dispatcher instead:

- the trigger gets a single plan that collects candidates, orders them by tier and runs them;
- each handler's body moves to a `+!handle(<handler id>)` goal, with its branches as before;
- candidate tests move into belief-base rules, so the dispatcher can query them.

Within a co-run group, handlers in the same `TIES` class have no declared order. Whether TEMPER orders them is open question Q6.

### What any target must provide

| Capability | Jason implementation |
| --- | --- |
| Read a handler id from an option | `handler(Id)` plan annotation |
| Look up a tier for the agent kind | `prec_tier/2` beliefs in the agent-kind file |
| Choose among same-tier options | VEsNA TEMPER selection |
| Deterministic final tie-break | Compare handler ids |
| Run several handlers in order | Generated dispatcher plan |

## Compilation to ASL

The proposed output splits each handler into a kind-independent part (in the playbook file) and a kind-specific part (in the agent-kind file). This keeps playbook files shared while letting each kind have its own tiers and modes.

### Playbook file: bodies and candidate rules

Each handler compiles to a candidate rule and a `+!handle` goal, with branches as today. The candidate rule is the disjunction of the branch conditions (`true` when there is an `ELSE`).

```
// playbook_noblesocializing.asl
trigger_of(noblesocializing__retort, insult_heard).
candidate(noblesocializing__retort) :- playbook_active(noblesocializing, _).

+!handle(noblesocializing__retort) : not (is_drunk) & hates(host) <-
    complain;
    !signal_directors(noblesocializing, insult_thrown).
+!handle(noblesocializing__retort) : not (not (is_drunk) & hates(host)) <-
    toast(host).

trigger_of(noblesocializing__digestion_check_0, digestion_check).
candidate(noblesocializing__digestion_check_0) :-
    playbook_active(noblesocializing, _) & is_hungry.   // no ELSE: falls through
```

### Agent-kind file: tiers and triggers in `EXCLUSIVE` mode

One trigger plan per handler. These plans are the options `selectOption` sees, so they carry the `handler` and TEMPER annotations.

```
// agent_banquet_guest.asl
{ include("playbook_noblesocializing.asl") }
{ include("playbook_drunkard.asl") }

prec_tier(noblesocializing__retort, 0).
prec_tier(drunkard__insult_heard_0, 1).

@trig__noblesocializing__retort[handler(noblesocializing__retort), temper([sympathy(-0.5)]), effects([aggressiveness(0.2)])]
+insult_heard : candidate(noblesocializing__retort) <- !handle(noblesocializing__retort).

@trig__drunkard__insult_heard_0[handler(drunkard__insult_heard_0)]
+insult_heard : candidate(drunkard__insult_heard_0) <- !handle(drunkard__insult_heard_0).
```

### Agent-kind file: a dispatcher in `ALL` mode

For a trigger with a co-run group, the kind file gets one dispatcher plan instead of per-handler trigger plans.

```
co_group(noblesocializing__food_served_0, g1).
co_group(gossip__food_served_0, g1).

+food_served <- !dispatch(food_served).

+!dispatch(E) <-
    .findall(t(T, H), trigger_of(H, E) & candidate(H) & prec_tier(H, T), L);
    .sort(L, Sorted);
    !run_winner(Sorted, Sorted).

+!run_winner([t(_, Best) | _], All) : co_group(Best, G) <-
    for ( .member(t(_, H), All) ) {
        if (co_group(H, G)) { !handle(H) }
    }.
+!run_winner([t(_, Best) | _], _) <- !handle(Best).
+!run_winner([], _) <- true.
```

The dispatcher bypasses `selectOption`, so TEMPER does not run here. Ties inside the dispatcher fall to the stable key until Q6 is settled.

### Costs of this split

- One extra goal level per handler, and the candidate condition is checked twice: once to select, once inside `+!handle`.
- Possible optimisation: when a playbook's trigger is `EXCLUSIVE` for every kind that includes it, emit the trigger plan directly in the playbook file, as v0.2 does, with the `handler` annotation added.

## Determinism guarantees

The proposal guarantees a deterministic choice for a given agent state and event. It does not, by itself, guarantee reproducible runs of a whole multi-agent system.

| Guarantee | Holds because |
| --- | --- |
| Same source, same tiers | Tiers come from relations, layers, priorities and names only; never from file, include or load order. |
| Same state and event, same handler | Filter, TEMPER and stable key are all deterministic functions of the options and the agent's state. |
| Adding a playbook never reorders two others | Tiers are computed over everything the kind can hold; activating a playbook only adds candidates. |
| Removing a playbook never reorders two others | Restricting a valid order to a subset keeps it valid. |

**What is not guaranteed.** TEMPER depends on personality and mood, and `EFFECTS` change that state after each choice. Selection therefore depends on history. In a multi-agent Jason system, the order of events and messages can differ between runs, so two runs of the same story can diverge. Full replay would need a deterministic scheduler and environment, which is outside this proposal.

## Alternatives considered

| Alternative | Why not chosen |
| --- | --- |
| Numeric priorities only (as in rule-engine salience) | Authors in isolation must guess numbers that only make sense relative to playbooks they cannot see; inserting a new playbook can force renumbering. Kept as a tie-breaker instead. |
| Rely on include or plan-library order | Violates R5; order changes when files are reorganised. |
| Relations declared inside playbooks (`BEFORE OtherPlaybook`) | Violates R1: a playbook would depend on others existing. Composition-level relations put that knowledge where it is available. |
| Undeclared ties go to TEMPER | Personality would silently decide competitions nobody thought about. TEMPER is used only for explicit `TIES` (R7). |
| Do all arbitration in a generated dispatcher, never in `selectOption` | Fully portable, but bypasses TEMPER in `EXCLUSIVE` mode and adds a dispatcher for every trigger. Used only for `ALL` mode. |
| Resolve order at runtime from the active set | Unnecessary while all playbooks are known at compile time, and it moves cycle errors from compile time to runtime. Revisit if dynamic loading is added. |
| Learned or utility-based plan selection | Not deterministic by design, and outside what authors can declare. |

## Open questions

These need a decision before the proposal can be accepted. Each is phrased so the answer changes the spec.

1. **Q1 — Keywords.** Are `OVER`, `TIES` and `WITH` the right words, or should relations use symbols (`>`, `~`, `+`)?
2. **Q2 — Layer list direction.** Is `LAYERS reflex, safety, social, idle` listed highest precedence first, or lowest first as in CSS?
3. **Q3 — Unlayered playbooks.** Where does the implicit default layer sit: below all named layers, above them, or must every playbook name a layer once a story declares `LAYERS`?
4. **Q4 — Default mode.** Is `EXCLUSIVE` the right default for a narrative engine, or should competing reactions all run unless told otherwise?
5. **Q5 — Level override.** Should the story always override plots, or may a plot mark a relation as non-negotiable so the story cannot drop it?
6. **Q6 — TEMPER in dispatchers.** Inside a co-run group, should tied handlers be ordered by TEMPER scores (needs an internal action that exposes them) or by the stable key?
7. **Q7 — Failure in `ALL` mode.** If one handler in a co-run group fails, do the remaining handlers still run?
8. **Q8 — Agent kinds.** Are all agents created through the starting plot's roles, or can agents join later with roles outside it? The latter needs a way to declare extra entry roles.
9. **Q9 — Signal triggers.** Should `WHEN ROLE Guest SIGNALS insult_thrown` handlers in Directors compete with plain `WHEN insult_thrown` handlers, or are they distinct triggers?

## Prior art and sources

| Work | What this proposal takes from it |
| --- | --- |
| [Padgham & Singh, Situational Preferences for BDI Plans (AAMAS 2013)](https://ifmas.csc.liv.ac.uk/Proceedings/aamas2013/docs/p1013.pdf) | Ranking applicable plans instead of over-constraining context conditions; aggregating several preferences. |
| [Visser, Thangarajah, Harland & Dignum, Preference-based reasoning in BDI agent systems (JAAMAS 2016)](https://link.springer.com/doi/10.1007/s10458-015-9288-2) | User-specified preferences applied at plan-selection choice points. |
| [Nunes & Luck, Softgoal-based Plan Selection in Model-driven BDI Agents (AAMAS 2014)](https://aamas.csc.liv.ac.uk/Proceedings/aamas2014/aamas/p749.pdf) | Utility-based selection as the quantitative alternative (not adopted). |
| [Ma et al., Plan Selection for Probabilistic BDI Agents (ICTAI 2014)](https://research-information.bris.ac.uk/en/publications/plan-selection-for-probabilistic-bdi-agents/) | Selecting a consistent subset of plans to run, behind `ALL` mode. |
| [Nagy, Bergmans & Akşit, Composing Aspects at Shared Join Points (2005)](https://ris.utwente.nl/ws/files/5292624/NagyBerAks2005.pdf) | Separate ordering constraints from control constraints at a shared trigger. |
| [Clarke, Helvensteijn & Schaefer, Abstract Delta Modeling](https://core.ac.uk/download/301659132.pdf) | Partial order over independently written modules, linearised into a unique composition. |
| [Schaefer et al., Delta-Oriented Programming of Software Product Lines (SPLC 2010)](https://link.springer.com/doi/10.1007/978-3-642-15579-6_6) and [Damiani & Schaefer, Dynamic Delta-Oriented Programming (2011)](https://doi.org/10.1145/2019136.2019175) | Composition-time ordering of modules, including at runtime reconfiguration. |
| [Maher, Propositional Defeasible Logic has Linear Complexity](https://arxiv.org/pdf/cs/0405090) | The superiority relation: local, acyclic, declared only between competing rules. |
| [CSS Cascade Layers explainer](https://css.oddbird.net/layers/explainer/) | Named layers whose order is fixed once, independent of load order. |

Also drawn on, without a source opened here: systemd `Before=`/`After=` (ordering separate from presence), Gradle `mustRunAfter`/`shouldRunAfter` (hard and soft constraints), and Soar's indifferent preference (the model for `TIES`).
