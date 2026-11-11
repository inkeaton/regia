# Director runtime in ASL

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 34, 35

## Question

How does a Director run in Jason? Decide:
- Routing game percepts to the right Directors.
- Phase switching: `EXITED` inside the atomic switch, `ENTERED` after it, and dropping a Phase's running intentions on leaving it (spec 20).
- Each Director's ordered record of standing Givings (spec 19).
- Running Role setups at Staging start and when an Agent joins, as Director messages (spec 16).
- One-Agent Givings and Mappings (spec 20).

## Answer

Spec chapter: `docs/spec/30-jason-directors.md`, checked against the latest VEsNA-Pro (`vesna-pro-main/`). Chapter 28 gains the Director class and two state rows, and its External-names section points to *Custom Actions through VEsNA*. Chapters 07, 16, 19, 20 and 29 point to the new chapter.

- **Agent class**: `regia.DirectorAgent` extends Jason's `Agent`, not `VesnaAgent`. Directors have no Temper, and `VesnaAgent` can't start without a port. Its body is optional: the Root Director has one and Subplot Directors don't. Ranking is a helper shared with the Agents' class.
- **Game messages**: `regia-jason` adds `regia_event` {name, args} (momentary) and `regia_fact` {add/remove, name, args} (`source(percept)` beliefs). VEsNA's `signal` has a fixed shape, and 1.0's `regia_event` is gone upstream.
- **Routing**: only the Root Director talks to the game. Percepts go down the Staging tree as `regia_percept(event|learned|forgotten)`, filtered by compile-time `regia_hears(Plot, Name, Arity)`; a Plot hears what it names plus everything its Subplots hear. `regia.perceive` replays a percept exactly as the body would. A new Subplot gets a snapshot of the parent's `source(percept)` Facts it hears, with no `LEARNED`. Rejected: a body per Director, a router agent.
- **Phases**: `regia_phase(P)` plus a guard and a `regia_phase(P)` label annotation on every Phase plan. The atomic `regia_transition` stops the old Phase (`regia.stop_phase`, skipping the caller), runs `EXITED` inline (a failure is traced and the transition continues), clears Quotas through a hook, swaps the Phase, posts `ENTERED` with `!!`, and ends the caller's Body (`regia.end_body`).
- **Start and join**: an atomic `regia_begin` sets the initial Phase, sends `regia_cast_copy(S, …)` to the whole cast, and runs the Role setups in declaration order. It then posts PLOT `ENTERED` and Phase `ENTERED`, which start in that order. An atomic `regia_join(Agent, Roles)` sends the cast copy, runs the setups, replays the standing Givings by `Seq`, then posts `JOINED`. A setup Statement that can fail is its own subgoal with a tracing `-!`.
- **Standing record**: `regia_standing(Seq, Playbook, Role, Rank, Bindings)`, for whole-Role `ASSIGN`s only. A repeated `ASSIGN` keeps its `Seq`. It is removed only by `UNASSIGN … FROM Role` or the end of the Staging, never by leaving a Phase.
- **One Agent**: `?who` Givings and Mappings check `regia_cast(S, _, Who)`. An Agent outside the cast, whether it left or never belonged, is dropped with a Trace warning.
- **`EVERYONE`**: a `.broadcast` of `regia_everyone(Ilf, Content)`. Agents unwrap it with `regia.deliver`, which keeps the real Sender; Directors ignore it.
- **Subplot `DO`**: passed up the tree as `regia_act(A)` and performed by the Root Director. What reaches the game is *Custom Actions through VEsNA* (new ticket).

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
- From *Giving and taking Playbooks at runtime* (35): Givings are `achieve regia_give(…)`/`regia_take(…)` messages (chapter 29). The Director tracks no holders; `regia_standing` only needs what replaying to a joiner requires. Send the cast before the first Giving to an Agent.
