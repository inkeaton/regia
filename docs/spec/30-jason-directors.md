# Directors in Jason

How the Jason Target runs a Director: its agent class, how game percepts reach every Director, how the game reports Facts and Events, how Phases are switched, what the Director does when a Staging starts and when an Agent joins, its record of standing Givings, Givings and Mappings for one Agent, and `EVERYONE`. Decided in the ticket *Director runtime in ASL* (`.scratch/regia-2/issues/36-director-runtime.md`). It builds on chapter 28's layout and chapter 29's Givings, and implements chapters 16 (Role setup), 19 (cast changes) and 20 (Directors). It was checked against the latest VEsNA-Pro source (`vesna-pro-main/`).

## The Director's agent class

A Director runs on **`regia.DirectorAgent`**, a class of `regia-jason` that extends Jason's `Agent`, **not** VEsNA-Pro's `VesnaAgent`.

- A Director has no Propensities (chapter 20), so it never needs VEsNA's Temper.
- **Its body is optional.** The Root Director has one: a WebSocket to the game, opened with VEsNA's `WsClient` from the `address` and `port` in the `.jcm` (chapter 36). A Subplot Director has none.
- Why not `VesnaAgent`: its body setup is private and parses `port` unconditionally, so an agent without a port fails to start, and a subclass can't skip that step.
- Directors still rank their Plans (a Phase over `DURING PLOT`, chapter 13). The ranking code is a helper shared by `regia.DirectorAgent` and the Agents' class (chapter 28), and doesn't live in either class.
- Every Staging is its own `regia.DirectorAgent`, and its name is the Staging's identity (chapter 31).

## What the game sends

VEsNA's own message types don't fit Regia. `signal` has a fixed `type(status, reason)` shape, and 1.0's `regia_event` type is gone from VEsNA-Pro. `regia-jason` adds two message types that Agents and the Root Director both understand:

| Type | `data` | Becomes |
| --- | --- | --- |
| `regia_event` | `{"name": "insult_thrown", "args": [...]}` | a momentary event `+insult_thrown(…)`, as VEsNA's `signal` does: no belief is kept |
| `regia_fact` | `{"op": "add" \| "remove", "name": "door_open", "args": [...]}` | `+door_open(…)[source(percept)]` or `-door_open(…)[source(percept)]` |

- `name` is the External name (chapter 28). `args` is a JSON array of numbers, strings and arrays (chapter 37), turned into Jason terms on the way in.
- A game Fact is marked **`source(percept)`**. VEsNA's own `addBel` marks beliefs `source(self)`, the same as a Director's own `LEARN`; the explicit source lets a Director tell what the game reported from what it learned itself (below).
- An Agent receives these by `regia.RegiaAgent` overriding VEsNA-Pro's public `myHandleMsg`; the Root Director reads its own body. Custom Actions and their results: chapter 37.

## Routing percepts to Directors

**Only the Root Director talks to the game.** Every other Director hears the game through its parent, so game percepts are passed **down the Staging tree**:

- When a Director takes in a percept, from its body or from its parent, it passes it on to each running child Staging whose Plot **hears** it, as an `achieve regia_percept(P)` message, with `P` being `event(e)`, `learned(f)` or `forgotten(f)`.
- The child accepts `regia_percept` only from its parent and applies it with `regia.perceive(P)`, a `regia-jason` internal action that does what the body would have done: the same momentary event, or the same `source(percept)` belief added or removed. So `WHEN e:`, `WHEN f LEARNED:` and `GIVEN f` behave exactly as for a Director that hears the game directly, and a forwarded percept never looks like a Signal or a `FROM Role` Message.
- Forwarding reads the Director's `regia_child(Child, Plot)` records (chapter 31), and stops while the Director is ending.
- **Which Facts and Events a Plot hears is known at compile time.** Each Director file lists, as initial beliefs, `regia_hears(Plot, Name, Arity)` for its own Plot and for every Plot below it. A Plot hears every Event and Fact its Triggers and Contexts name, **plus everything its Subplots hear**, so a Director keeps the game Facts its descendants need, even ones it never uses itself.
- Which percepts the game sends the Root Director is up to the game. Regia only filters on the way down.
- Rejected: a VEsNA body for every Director (the game would have to learn about Stagings and runtime-spawned agents), and a central router agent (one more agent, which duplicates the parent's record of its children).

### Game Facts a Subplot starts with

A Subplot started after the game reported `door_open` starts **knowing** `door_open`:

- When it starts a child Staging, the parent sends the child a **snapshot** of its own `source(percept)` beliefs that the child's Plot hears. The child adds them with `regia.add_percepts(L)`, which adds beliefs **without generating events**.
- The snapshot is starting state, so **`LEARNED` doesn't fire** for it, just as joining Triggers don't fire for a starting Cast (chapter 19). Later changes are forwarded live and fire as usual.
- Facts the parent learned itself (`LEARN`, `source(self)`) are never passed on: Facts belong to one Staging (chapter 20).
- The snapshot is sent before the child's start message, so per-sender ordering puts it in place before the child's Role setups. The start message itself is `regia_start` (chapter 31).

## Phases

### The current Phase

The Director holds its current Phase as `regia_phase(Phase)`. Each Director is one Staging, so the belief needs no Staging argument.

A Plot that declares no Phases (chapter 20) gets one hidden Phase, the Generated name `regia_phase__plot`, as its initial Phase. Everything below works unchanged: the Director has a current Phase, so its `DURING PLOT` plans hear, and the hidden Phase has no plans of its own and is never left. It writes no `phase` Trace entry, and the source map folds it away (chapter 35).

Every plan generated from a `DURING feast` Block:

- starts its context with `regia_phase(feast)`, so it applies only in that Phase (the same guard pattern as Givings, chapter 29);
- carries a `regia_phase(feast)` annotation in its label, so the intentions running it can be found when the Phase is left;
- carries a `regia_rank(Level, Pos)` annotation, resolved at compile time, which ranks it against `DURING PLOT` (chapter 32). `DURING PLOT` Trigger plans carry one too.

`DURING PLOT` Trigger plans have no `regia_phase` annotation, and their context starts with `regia_phase(_)`: a Director with no current Phase is ending and hears nothing (chapter 31).

`ENTERED` and `EXITED` Plans are compiled to plans for the generated Goals `regia_entered(phase(feast))`, `regia_entered(plot)`, `regia_exited(phase(feast))` and `regia_exited(plot)`. Each has a catch-all plan that does nothing, so a Phase without an `ENTERED` or `EXITED` Plan, or one whose `GIVEN`s don't match, is fine.

### `TRANSITION`

`TRANSITION TO x.` calls `!regia_transition(x)`, an `[atomic]` plan in `regia/director.asl`. It follows chapter 20's four steps:

1. **Stop the old Phase's Plans.** `regia.stop_phase(Old)`, a `regia-jason` internal action like `regia.stop_playbook` (chapter 29), drops every intention running a plan annotated `regia_phase(Old)`. It drops them silently: Directors have no Goals, so nothing fires and nothing is traced. It **skips the intention running the `TRANSITION`**, which ends at step 5.
2. **Run `EXITED` to completion**, as the subgoal `!regia_exited(phase(Old))`, inside the atomic plan. If it fails, a `-!regia_exited` plan writes the Trace entry (chapter 20) and the transition carries on: a Director Statement never fails.
3. **Clear the old Phase's Quota counts**, with `!regia_quota_clear(Old)` (chapter 33), then replace `regia_phase(Old)` with `regia_phase(x)`.
4. **Post `ENTERED`** with `!!regia_entered(phase(x))`. It starts after the atomic plan, as an ordinary intention of the new Phase: it may `WAIT`, and it is stopped if the Phase is left.
5. **End the Body.** `regia.end_body` drops the intention that ran the `TRANSITION`, silently. `TRANSITION` ends its Body (chapter 20) even inside an `IF` branch with Statements after the `IF`, and in a `DURING PLOT` Plan too.

`TRANSITION` to the current Phase takes the same path, so it re-enters the Phase. `END PLOT` reuses steps 1 and 2 for the current Phase, then runs `!regia_exited(plot)` the same way. The rest of `END PLOT` is chapter 31.

## Starting a Staging

Once the Director has its cast (from `regia_start`, chapter 31), it runs `!regia_begin`, an `[atomic]` plan:

1. Add `regia_phase(Initial)`. The initial Phase is current from the start.
2. Send every cast Agent the **cast copy** (chapter 29) as one message: `achieve regia_cast_copy([cast(Role, Agent), …])`. `regia/agent.asl` replaces any copy it holds from that Director, the `[source]`, which is the Staging (chapter 31). Every cast Agent gets it, so the Director needn't track who already has one.
3. **Run the Role setups**: for each Role in declaration order, for each Agent playing it, `!regia_setup__guest(Agent)`.

After the atomic plan, it posts `!!regia_entered(plot)` and then `!!regia_entered(phase(Initial))`. Jason picks events in the order they were posted, so `DURING PLOT`'s `ENTERED` **starts** first. "Before" in chapter 20 means it starts first, not that it finishes first: a `WAIT` in it doesn't hold up the Phase's `ENTERED`.

### Role setups

Each `ROLE Guest STARTS WITH:` Block is a generated Director plan `regia_setup__guest(A)`. It sends its Statements to `A` in the order written (chapter 16):

| Setup Statement | Sent |
| --- | --- |
| `ASSIGN P[, MAPPING …]` | `achieve regia_give(p, role(guest), Rank, Bindings)` (chapter 29) |
| `LEARN f` | `tell f` |
| `PURSUE g` | `achieve g` |

- The Agent sees the Director as `[source]`, so `FROM DIRECTOR` matches (chapter 16).
- A Statement whose arguments use Body arithmetic, the only kind that can go wrong, is compiled as its own subgoal with a `-!` plan that writes the Trace entry and returns, so the next Statement still runs. That is chapter 16's "skipped".

## An Agent joining

How the game reports a join, and how the Director's `regia_cast` and the other Agents' copies are updated, are in chapter 33. Once that is done, the Director runs `!regia_join(Agent, Roles)`, an `[atomic]` plan:

1. Send the joiner the cast copy.
2. Run each joined Role's setup for it, in Role declaration order.
3. **Replay the standing Givings** of the joined Roles, in `Seq` order (below), as `regia_give(p, role(r), Rank, Bindings)`.

After the atomic plan, it posts `!!regia_joined(Role, Agent)` for each joined Role in declaration order, which runs the `WHEN Role [?who] JOINED` Plans. This is chapter 19's order: setups, then standing Givings, then `JOINED`.

## The standing-Giving record

Each standing Giving is one belief on the Director:

```
regia_standing(Seq, Playbook, Role, Rank, Bindings)
```

- **`Seq`** comes from a per-Director counter, `regia_standing_seq(N)`. Replay follows the order the Givings were made.
- **Only a whole-Role `ASSIGN` is standing.** A counted pick and a Giving to `?who` aren't (chapter 19). A Role setup's `ASSIGN` isn't either: the setup itself runs again for a joiner.
- **An identical `ASSIGN` running again keeps its first `Seq`**, so its place in the replay order doesn't move. It is the same Giving (chapter 29).
- `UNASSIGN P FROM Role` removes every `regia_standing(_, p, role, _, _)`. `UNASSIGN P FROM ?who` leaves the record alone (chapter 15).
- **A standing Giving lasts until `UNASSIGN` or the end of the Staging.** Leaving the Phase that made it doesn't remove it. 1.0's take-away in `on_exit` is gone.
- The record holds only what a replay needs (chapter 29): the Director doesn't track who holds which Giving.

## One Agent

`ASSIGN P TO ?who`, `UNASSIGN P FROM ?who` and `MAPPING ?who TO r` first check `regia_cast(Me, _, Who)`: is that Agent in this Staging's cast **now**?

- **If it is**, the Giving is `regia_give(p, agent(who), Rank, Bindings)` (chapter 29), or the Mapping is `bind(r, fixed([who]))`.
- **If it isn't**, the Giving or Mapping is dropped with a Trace warning. That covers an Agent that has left (chapter 20) **and** an Agent that was never in this Staging, such as one named by a game Event's argument. A Director directs its own cast. Since every cast Agent already has the cast copy, nothing more needs tracking.

## Messages from a Director

- `TELL Role f` and `ASK Role TO g` send `tell f` or `achieve g` to each Agent with `regia_cast(Me, Role, A)` when the Statement runs (chapter 20). A send to an Agent that has left is caught and traced by `regia.send` (chapter 33).
- A filled Placeholder recipient is a single `.send`.

### `EVERYONE`

`TELL EVERYONE f` and `ASK EVERYONE TO g`, from an Agent or a Director, are one `.broadcast(achieve, regia_everyone(tell, f))` or `.broadcast(achieve, regia_everyone(achieve, g))`.

- `regia/agent.asl` unwraps it with `regia.deliver(Ilf, Content, Sender)`, a `regia-jason` internal action that puts the inner message in the Agent's mailbox as if `Sender` had sent it directly. `FROM` still sees the real Sender.
- `regia/director.asl` ignores it, so `EVERYONE` reaches every Agent and no Director (chapter 07).
- `.broadcast` never sends to the sender itself, which is chapter 07's "except the sender".
- Nothing has to know every Agent in the game.

## Custom Actions in a Subplot Director

A Subplot Director has no body, so `DO play_music.` there is sent **directly to the Root Director** as `achieve regia_act(A, ReqId)`. The Root performs it through its body and relays the game's replies back, so the Subplot Director's `DO` waits and fails as anywhere else (chapter 37). Unlike percepts, an Action needs no filtering on the way, so it skips the Directors in between.

## Infrastructure state

Rows filled in or added in chapter 28's table:

| Concept | Held by | Functor and arguments |
| --- | --- | --- |
| The current Phase | Director | `regia_phase(Phase)` |
| A standing Giving | Director | `regia_standing(Seq, Playbook, Role, Rank, Bindings)` |
| The next standing Giving's number | Director | `regia_standing_seq(N)` |
| What a Plot hears from the game | Director (initial beliefs of its file) | `regia_hears(Plot, Name, Arity)` |
| A game Fact | Agent or Director | the Fact itself, `[source(percept)]` |

## `regia-jason` additions

- `regia.DirectorAgent`, the Directors' class (above), and a ranking helper shared with the Agents' class.
- The `regia_event` and `regia_fact` message types.
- Internal actions: `regia.perceive`, `regia.add_percepts`, `regia.stop_phase`, `regia.end_body`, `regia.deliver`.


## Trace entries

**Warnings**

- `T3001` A Giving or Mapping to a `?who` who was never in this Staging (such as an Agent named by a game Event's argument), dropped.

A failed `EXITED` Plan writes chapter 20's `T2002`, and the transition carries on; a Giving or Mapping to an Agent who has left writes `T2001`.

## Not decided here

- The Staging's identity (its Director's name), Director names, a Director's record of its children, starting a child Director with its cast, and the rest of `END PLOT`: chapter 31 (`31-jason-stagings.md`).
- The game reporting joins and leaves, keeping `regia_cast` and the cast copies up to date, catching sends to Agents that have left, and the Quota-clearing hook: chapter 33.
- How `regia-jason` hooks into VEsNA-Pro's message handling, Custom Actions reaching the game, and Action results: chapter 37.
- The Root Director's `.jcm` entry (its `address` and `port`, and `ag-class: regia.DirectorAgent`): chapter 36.
- The format of Trace entries: chapters 34 and 35.
