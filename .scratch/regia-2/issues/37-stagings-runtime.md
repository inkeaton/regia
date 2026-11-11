# Stagings and Subplots runtime in ASL

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 34, 35, 36

## Question

How do Stagings and Subplots run in Jason (spec 17)? Decide:
- A runtime identity per Staging, carried in Givings and Signals.
- Starting a Subplot's Director with its cast.
- The children-first ending walk, with its `ended` message to the parent.

## Answer

Spec chapter: `docs/spec/31-jason-stagings.md`, checked against Jason 3.2.1. Chapter 29's records and messages lose their Staging argument; chapter 28's `regia_plays` row is retired; chapters 17 and 30 point to the new chapter.

- **Identity**: one `regia.DirectorAgent` per Staging, and the Staging *is* the Director's agent name. `regia_given(Playbook, Director, Target, Rank, Bindings)`; `regia_give`/`regia_take` carry no Staging; the cast copy is `regia_cast(Director, Role, Agent)`, sent as `regia_cast_copy([…])`. `FROM DIRECTOR` reads `regia_given`, not names.
- **Names**: Root `regia_director__<plot>` in the `.jcm`; children via `regia.start_staging(Plot, Name)`, wrapping `createAgent` with `agentClass("regia.DirectorAgent")` and returning Jason's unique name (`regia_director__honorDuel`, then numbered). Names aren't parsed; game-reported Agent names may not start with `regia_`.
- **Records**: `regia_staging(Plot)` (initial belief), `regia_parent(D)`, `regia_child(D, Plot)`, `regia_ending(Outcome)`. `regia_plays` retired: the cast copy says it.
- **Start**: one atomic step on the parent: resolve the cast now, create the child, record it, send the percept snapshot, then `regia_start(Cast)`. The child takes its parent from `[source]` and runs `regia_begin`. An empty mapped Role starts empty.
- **End**: one path for every ending. Stop and run `EXITED` (Phase, then PLOT), remove `regia_phase`, send `regia_end` to the children and wait for each `regia_ended`, then `regia_end_staging` to the cast (one atomic take-away of every Giving and the cast copy, replacing per-Playbook `regia_take`), `regia_ended(Plot, Outcome)` to the parent, `.kill_agent`. A child ended by its parent runs its `EXITED` too.
- **`regia_ended`** is both the ack (parent ending: no Trigger) and the notification (posts `regia_subplot_ended`); one from a child no longer on record is ignored, which settles the `END SUBPLOT` race. `END SUBPLOT` removes the records and sends `regia_end` without waiting.
- **Deaf while ending**: `DURING PLOT` Trigger plans, forwarding and `DO`-relay are guarded by `regia_phase(_)`; no Phase means ending.
- **`WHEN P ENDED`**: plans for `regia_subplot_ended(p, O)`, each excluding the patterns above it, plus a do-nothing catch-all. Outcome is `none` or the Event term.
- **Root `END PLOT`**: same walk, but the Root agent stays alive and idle; telling the game is *Custom Actions through VEsNA*.

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
- From *Giving and taking Playbooks at runtime* (35): `regia_given` and `regia_cast` carry an opaque `Staging` argument whose shape is decided here; the giving Director's agent name is stored separately, so the Staging id needn't be it. A Staging ending sends `regia_take(P, S, all)` to its cast for each Playbook it gave (chapter 29).
- From *Director runtime in ASL* (36): game percepts go down the tree, so each Director's record of its children is read for forwarding `regia_percept`, and a child accepts `regia_percept` only from its parent. Before a child's start message, the parent sends it a snapshot of the `source(percept)` Facts its Plot hears (`regia.add_percepts`). Directors run `regia.DirectorAgent` with no body. `END PLOT` reuses `regia_transition`'s steps 1–2, then `regia_exited(plot)`. Agents must recognise a Director as a Sender for `FROM DIRECTOR`, so decide Director agent names here (chapter 30).
