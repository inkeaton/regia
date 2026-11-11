# Giving and taking Playbooks at runtime

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 34

## Question

How are Playbooks given to and taken from Agents in Jason at runtime (the last open `#discuss` of primer ch.8)? Decide:
- Adding and removing plans (building on the Jason dynamic-plans research), against compiling every possible Playbook in.
- Dropping local Goals when a Playbook is taken away (spec 10).
- The per-Giving record of Role bindings and counted picks, and expanding Role recipients and `FROM Role` against it (spec 15).

## Answer

Spec chapter: `docs/spec/29-jason-givings.md`. Chapter 28's state table filled in (`regia_given` arguments, new `regia_playbook`, `regia_cast` copied in Agents). `UNASSIGN` wording sharpened in chapters 15, 19 and 20. Chapters 10, 13 and 16 point to the new chapter.

- **Compiled in**: no `.add_plan`, `tellHow` or runtime `.include`. Role files hold every reachable Playbook (chapter 28), listed as `regia_playbook(P)` initial beliefs. A `?who` Giving in Plot X counts as reachable for every Root Role mapping to any Role of X.
- **Guard**: every plan of P (designer Plans, Local Goal plans, generated `-!g`/`DROPPED`/helper plans) starts its context with `regia_given(p, …)`. Ranking still happens in `selectOption`, reading the same beliefs.
- **Record**: `regia_given(Playbook, Staging, Director, Target, Rank, Bindings)`, one belief per Giving. There's no Giving id: identical Givings collapse, and taking away matches Playbook + Staging + Target. `Director` comes from `[source]`, never from the message, so `SIGNAL` always has an address. `Target` is `role(R)` (whole, counted or setup) or `agent(A)`. `Bindings` hold `live(PlotRole)` or `fixed([…])`.
- **Cast copy**: Agents holding a Giving from a Staging keep `regia_cast(Staging, Role, Agent)`, sent by the Director before its first Giving. Live recipients, `FROM Role` and Quotas resolve locally. Asking the Director and relaying through it were rejected.
- **Protocol**: `achieve regia_give(P, S, T, R, B)` and `regia_take(P, S, T | all)`, handled by `[atomic]` plans in `regia/agent.asl`. A Giving for a Playbook missing from the Agent's files gets a Trace warning and is ignored. The Director tracks no holders: a take-away goes to the whole cast.
- **`UNASSIGN` meaning**: `FROM Role` removes every Giving this Staging made to that Role (whole, counted, setup) and its standing record. `FROM ?who` removes that Agent's Givings of P from this Staging, whatever the target, and leaves the standing record.
- **Taking the last Giving away**: `regia.stop_playbook(P)` (a `regia-jason` internal action) stops, on each intention, the outermost plan of P and everything above it, as `DROP` does. Goals fire `DROPPED` innermost first, a still-given Plan waiting with `PURSUE` fails, non-Goal Plans stop with a Trace entry, and Local Goals go with them. Local Facts stay. Quota counts are cleared.

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
- See [Research: dynamic plan loading in Jason](23-research-jason-dynamic-plans.md).
