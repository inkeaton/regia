# Cast changes and Quota counts in Jason

How the Jason Target handles the Cast changing and counts Quota Triggers. It covers the Root Director's starting cast, how the game reports Agents joining and leaving, who creates and kills their Jason agents, how a leave travels down the Staging tree, how Agents keep their cast copies and fixed bindings up to date, how a send to an agent that is gone is caught, and how Quota Triggers are counted in ASL. Decided in the ticket *Quota counts and cast changes in ASL* (`.scratch/regia-2/issues/39-quota-and-cast-changes.md`). It builds on chapter 28's layout, chapter 29's Givings, chapter 30's Directors, chapter 31's Stagings and chapter 32's ranks, and implements chapters 18 (Quota Triggers) and 19 (cast changes). It was checked against Jason 3.2.1 (`.send`) and the latest VEsNA-Pro source (`vesna-pro-main/src/agt/vesna/VesnaAgent.java`).

## The Root Director's starting cast

The Transpiler names the starting Agents (`noble_1` …, chapter 36), so it knows the Root Plot's starting cast at compile time. The Root Director's file carries it as an initial belief, next to `regia_rank_prefix([])` (chapter 32):

```
regia_start_cast([cast(guest, noble_1), cast(guest, noble_2), cast(host, lord_1)]).
!regia_root_start.
```

`regia/director.asl` handles the initial goal: add `regia_cast(Me, Role, A)` for each entry, then `!regia_begin` (chapter 30). A Subplot Director gets its cast from `regia_start` instead (chapter 31), so it has no `regia_start_cast`.

- Starting Agents are **never reported** as joins. Starting is not joining (chapter 19).
- An Agent kind with no `COUNT` contributes no entries (chapter 21).

## What the game reports

Two more message types arrive on the Root Director's body, next to `regia_event` and `regia_fact` (chapter 30). They are sent **to the Root Director only**:

| Type | `data` | Meaning |
| --- | --- | --- |
| `regia_join` | `{"kind": "noble", "name": "noble_7", …}` | the game spawned an Agent of this kind, with this name |
| `regia_leave` | `{"name": "noble_7"}` | the game removed this Agent from the Program |

- The fields the new agent's body needs to connect to the game (its port, for example) also travel in `regia_join`. A join carries exactly `kind`, `name` and `port` (chapter 36).
- A body closing is **not** a leave. VEsNA-Pro kills an agent whose WebSocket errors or closes (`VesnaAgent.myHandleError`). That is VEsNA's business: the Agent stays in every cast, and sends to it are caught (below). Only `regia_leave` removes an Agent from the Program (chapter 19).

### Reports that make no sense

The Root Director **ignores** these reports and writes a Trace warning, never a failure:

- a `regia_join` whose name starts with `regia_` (chapter 31: Generated names start with it), or which names an Agent already in the Program;
- a `regia_join` for a kind that has no Agent declaration;
- a `regia_leave` for an Agent that isn't in the Program.

## Joining

The Root Director handles `regia_join` in one `[atomic]` plan:

1. **Check** the report (above).
2. **Create the agent** with `regia.spawn_agent(Kind, Name, Body)`, a `regia-jason` internal action. It creates a Jason agent of the kind's agent class and Role file(s), with the kind's settings and Propensity values (`RANDOM` drawn here, chapter 21) and the body fields from the report. It finds the kind in the Root Director's `regia_kind` beliefs (chapter 36).
3. **Add it to the cast**: `regia_cast(Me, Role, A)` for each of the kind's Roles.
4. **Tell the rest of the cast**: send `achieve regia_cast_joined(Role, A)` to every other Agent in `regia_cast(Me, _, _)`, once per Role.
5. **Run the join**: `!regia_join(A, Roles)` (chapter 30): the joiner's cast copy, its Role setups, the standing Givings, then `JOINED`.

The new agent is created before any message reaches it, so Jason queues the cast copy and the Givings until it runs.

- Joining never triggers a Quota check (chapter 19). It only raises the denominator of `ALL` and `PERCENT`, which the next check reads live.
- Joiners join only the Root Plot (chapter 19), so no `regia_cast_joined` goes down the tree.
- After the Root Staging has ended (chapter 31), the Root Director still creates and kills agents for the game, but there is no cast to join: steps 3 to 5 are skipped and the join is traced.

## Leaving

### The leave walk

The Root Director handles `regia_leave(A)` by running the **leave walk** on itself. A Subplot Director runs the same walk when it gets `achieve regia_left(A)` from its `regia_parent`. On Director `D`, in one `[atomic]` plan:

1. **Not in my cast**: if there is no `regia_cast(Me, _, A)`, do nothing, and don't pass it on.
2. **Remove it**: note A's Roles here, then remove every `regia_cast(Me, _, A)`.
3. **Tell the rest of the cast**: send `achieve regia_cast_left(A)` to every remaining Agent in `regia_cast(Me, _, _)`.
4. **Pass it down**: send `achieve regia_left(A)` to every `regia_child(C, _)`.
5. **Quota counts**: remove every `regia_quota(_, _, _, _, _, A)`, then check every Quota Trigger that still has counts against the smaller Role (below). Each one now met posts `!!regia_quota_met(…)`.
6. **Director Triggers**: for each Role A played here, in Role declaration order, post `!!regia_role_left(Role, A)`, then `!!regia_role_emptied(Role)` if no `regia_cast(Me, Role, _)` is left.

Steps 5 and 6 are chapter 19's order: Quotas first, then `LEFT` and `EMPTIED`, Role by Role. The Plans for `regia_role_left` and `regia_role_emptied` are the designer's `WHEN Role [?who] LEFT` and `WHEN Role EMPTIED` Blocks. Each Goal has an empty failure plan for `error(no_applicable)` and `error(no_relevant)`, so a Role nobody listens for is silent (as for `regia_when__…`, below).

On the Root Director, after the walk, **kill the agent** with `.kill_agent(A)`, caught if it is already gone. The Root doesn't wait for its descendants to finish their walks; a child that sends to A in the meantime is caught by `regia.send` (below). A Program never leaves an Agent running after it has left.

### Passing a leave down

A leave goes down the Staging tree the way percepts do (chapter 30), **pruned by cast**. A Subplot's cast is drawn from its parent's, and only the Root ever gains Agents, so an Agent missing from a Director's cast is missing from every Staging below it. Step 1 stops the walk there.

- **An Agent leaving between `START SUBPLOT` and `regia_start`** needs no special case. `START SUBPLOT`'s plan is atomic (chapter 31), so the leave walk runs either before it, and the cast is resolved without A, or after it. In that case the child is already a `regia_child`, and per-sender order delivers `regia_left` after `regia_start`.
- **An ending Director** (no `regia_phase`, chapter 31) still runs the walk, so its cast is right when it sends `regia_end_staging`. The Goals of steps 5 and 6 find no applicable plan, since every Director Trigger plan is guarded by `regia_phase(_)`, and stay silent.

### What an Agent does

`regia/agent.asl` keeps the cast copies (chapter 29) up to date with two `[atomic]` plans:

```
@regia_cast_joined[atomic]
+!regia_cast_joined(Role, A)[source(D)]
   <- +regia_cast(D, Role, A).

@regia_cast_left[atomic]
+!regia_cast_left(A)[source(D)]
   <- // remove every regia_cast(D, _, A)
      // in every regia_given(P, D, T, R, B), drop A from each fixed([…]) list in B
      // remove every regia_quota(_, _, _, _, _, A), then check this Agent's Quota counts again
```

- **Fixed lists are stripped per Director.** A counted pick or a `MAPPING ?who` from Director `D` only ever names Agents of `D`'s cast (chapter 30), so the `regia_cast_left` from `D` reaches every list that can hold A. The pick is not refilled (chapter 15).
- A leaver that played in several Stagings sends one `regia_cast_left` from each Director. The first removes A's Quota counts; the others find none, and their checks find nothing new.
- **Rejected:** one broadcast `regia_left(A)` from the Root to every Agent. It needs fewer messages, but it races with Givings still coming from other Directors. Re-sending the whole cast copy on every change was also rejected: it is O(n²) messages for a crowd.

## Sends to agents that are gone

Jason's `.send` to an agent that doesn't exist throws `ReceiverNotFoundException` ("Receiver '…' does not exist!"). The action fails, and so does the sending plan. Chapter 19 needs that to be a trace entry, not a failure.

Every send in generated and Infrastructure code goes through **`regia.send(Receiver, Ilf, Content)`**, a `regia-jason` internal action. It does what `.send` does, catches the exception, writes a Trace entry, and **never fails**. Generated code never uses `.send`.

It covers:

- a `TELL` or `ASK` to a Placeholder holding an Agent that has left (chapter 19);
- a send racing with a leave: a Director that hasn't run its leave walk yet, or a body that closed before the game reported the leave;
- a `SIGNAL` or any message to a Director that has ended with `.kill_agent` (chapter 31). For example, an Agent signals before its `regia_end_staging` arrives.

`.broadcast` (for `EVERYONE`, chapter 30) never targets a missing agent and stays as it is.

- Why Java: catching a Jason infrastructure failure is the same kind of glue as the body. An ASL version that checks `.all_names` first leaves a window where the agent dies between the check and the send.

## Quota counts

Quota counting is **ASL**. `regia-jason` adds nothing for it (ADR 0013).

### The count

One belief per counted sender, per argument value:

```
regia_quota(Owner, Event, Quantity, Role, Args, Sender)
```

| Argument | Holds |
| --- | --- |
| `Owner` | the Playbook's Jason name in an Agent; `plot` in a Director. A Playbook Role belongs to its Playbook (chapter 15), so two Playbooks' `neighbour` are two Triggers |
| `Event` | the Event's Jason name |
| `Quantity` | `all`, `of(3)` or `percent(50)` |
| `Role` | the Plot Role (Director) or Playbook Role (Agent) |
| `Args` | the Event's arguments, as a list. Counts are kept per argument value (chapter 18) |
| `Sender` | the Agent counted |

`(Owner, Event, Quantity, Role)` is a **Quota Trigger** (chapter 18): one count, shared by every Block written with it.

### What is watched

The Transpiler writes, as initial beliefs:

- `regia_quota_watch(Owner, Event, Quantity, Role)`: one per Quota Trigger. In a Director's file for its own Plot; in an Agent's Role file for each Playbook it includes. Playbook files stay Plans only (chapter 28).
- `regia_quota_in(Event, Quantity, Role, Where)` in Director files: each Phase (`phase(feast)`) or `plot` that has a Block with that Quota Trigger.

### The dispatcher

Jason handles one plan per event, but chapter 18 needs both the plain Trigger and the count for the same Signal. For every Event **name** that some Quota Trigger watches anywhere in the Program, the Transpiler emits a **dispatcher**. It is the only plan for the incoming event, and it moves the designer's plain Blocks for that Event to a generated Goal:

```
// one per watched Event, in each Director file and Role file that handles it
@regia_dispatch__ready[atomic]
+ready[source(S)]
   <- !!regia_when__ready(S);          // the plain Trigger, first
      !regia_count(ready, [], S).      // the count, in regia/director.asl or regia/agent.asl

// the designer's plain `WHEN ready FROM Guest ?g:` in Phase reception
@regia_plan__12[regia_phase(reception), regia_rank(0, 0)]
+!regia_when__ready(G) : regia_phase(reception) & regia_cast(_, guest, G) <- …

// nothing applicable, or no plain Block at all: silent, like an unhandled Event (chapter 11)
-!regia_when__ready(_)[error(no_applicable)].
-!regia_when__ready(_)[error(no_relevant)].
```

- The dispatcher takes over the trigger the plain Plans would have had, whatever form the incoming Event has.
- The **Sender is an argument** of `regia_when__<e>`, after the Event's own arguments. `FROM Guest ?g`, `FROM DIRECTOR` (chapter 31) and `FROM host` (chapter 29) compile to tests on it. Jason adds `source(self)` to Goals it posts itself, so an annotation wouldn't carry the Sender through.
- **The plain Trigger starts first**, then the count, which may post `regia_quota_met`. In chapter 18's example, `TELL ?g welcome` starts before `TRANSITION TO feast`. They are separate intentions, so "starts first" is all that is promised, as with `ENTERED` (chapter 30).
- A real failure in a plain Plan carries another `error(…)`, so the two empty plans don't swallow it. It reaches the Trace as chapter 11 says.
- **Precedence is unchanged.** Plans for `regia_when__ready` carry the same `regia_rank` as `+ready` plans would (`Item` `when(ready)`, chapter 32), and `selectOption` reads the annotation, not the trigger.
- Events no Quota Trigger watches compile as before, without a dispatcher. Whether an Event is watched is a whole-Program fact, and the Transpiler always sees the whole Program (chapter 23).
- An Agent kind playing several Roles gets each dispatcher once. A combination file includes it once, as for `regia_playbook` (chapter 36).

### Counting

`!regia_count(Event, Args, S)` is an `[atomic]` plan in the Infrastructure. For each `regia_quota_watch(Owner, Event, Quantity, Role)` that is **active**, and whose Role has S as a **member**:

1. Add `regia_quota(Owner, Event, Quantity, Role, Args, S)`. A second Signal from S changes nothing, since each Agent counts once.
2. **Check** that Trigger for `Args` (below).

| | Director | Agent |
| --- | --- | --- |
| Active | `regia_phase(Ph)` and `regia_quota_in(Event, Quantity, Role, phase(Ph))` or `… plot)` | some `regia_given(Owner, …)` |
| Members of `Role` | `regia_cast(Me, Role, A)` | the union, over every `regia_given(Owner, …)`, of the `Role` bindings (chapter 29), **minus the Agent itself** |

An Agent never receives its own Messages, since recipients exclude the sender (chapter 29). So it is left out of its own denominators. Otherwise an Agent that is its own `neighbour` could never meet `ALL` (chapter 18).

### Checking

For a Trigger and an `Args` value, with `n` counted senders that are still members and `m` members:

| Quantity | Met when |
| --- | --- |
| `all` | `m > 0` and `n = m` |
| `of(k)` | `n ≥ k` |
| `percent(p)` | `m > 0` and `n × 100 ≥ p × m` (at least that share, no rounding, chapter 18) |

When it is met, remove every `regia_quota(Owner, Event, Quantity, Role, Args, _)`, so that value's count starts again from zero (chapter 18). Then post `!!regia_quota_met(Owner, Event, Quantity, Role, Args)`.

- The designer's Quota Blocks are plans for `+!regia_quota_met(…)`, with the usual `regia_phase` guard (Director) or `regia_given` guard (Agent) and `regia_rank`. Placeholders in the Event's arguments are filled from `Args`.
- The count is reset **before** any Block is chosen, and `regia_quota_met` has the same two empty failure plans as `regia_when__<e>`. If no Block is a candidate, nothing runs and the count is still reset (chapter 18).
- Checks run on a count (above) and on a leave (the walk's step 5 in Directors, `regia_cast_left` in Agents). They never run on a join.

### Clearing counts

- **Director, on `TRANSITION`**: chapter 30's step 3 calls `!regia_quota_clear(Old)`. It removes the counts of every Quota Trigger with `regia_quota_in(…, phase(Old))` and no `regia_quota_in(…, plot)`. This also happens for a `TRANSITION` to the current Phase: re-entering starts the count afresh, as it re-fires `ENTERED`.
- **Director, on ending**: nothing to clear. Without `regia_phase` no count is active, and the agent is killed (chapter 31). The Root Director, which stays alive, removes every `regia_quota(plot, …)` when it removes `regia_phase`.
- **Agent, when the last Giving of P goes**: the `regia_take` and `regia_end_staging` plans remove every `regia_quota(p, …)` right after `regia.stop_playbook(p)` (chapters 29 and 31). This is ASL, not part of the internal action.
- Counting starts on a Playbook's first Giving with nothing to do: the count is active as soon as a `regia_given` exists. Senders before that were never counted.

## Infrastructure state

Rows filled in or added in chapter 28's table:

| Concept | Held by | Functor and arguments |
| --- | --- | --- |
| A Role's members | Director, and a copy in Agents | `regia_cast(Director, Role, Agent)` |
| The Root Plot's starting cast | Root Director (initial belief) | `regia_start_cast([cast(Role, Agent), …])` |
| A Quota Trigger count | Agent or Director | `regia_quota(Owner, Event, Quantity, Role, Args, Sender)` |
| A Quota Trigger to count | Agent (Role file) or Director (initial beliefs) | `regia_quota_watch(Owner, Event, Quantity, Role)` |
| Where a Director's Quota Trigger has Blocks | Director (initial beliefs) | `regia_quota_in(Event, Quantity, Role, Where)` |

## Messages

| Message | From → to | Meaning |
| --- | --- | --- |
| `regia_join` (body) | game → Root Director | an Agent of this kind entered the Program |
| `regia_leave` (body) | game → Root Director | this Agent left the Program |
| `achieve regia_left(A)` | parent → child Director | run the leave walk for A |
| `achieve regia_cast_joined(Role, A)` | Root Director → each other cast Agent | add A to the cast copy |
| `achieve regia_cast_left(A)` | Director → each remaining cast Agent | remove A from the cast copy, the fixed bindings and the Quota counts |

## Generated Goals

| Goal | Runs |
| --- | --- |
| `regia_when__<e>(Args…, Sender)` | the plain `WHEN e` Blocks of a watched Event |
| `regia_quota_met(Owner, Event, Quantity, Role, Args)` | Quota Trigger Blocks |
| `regia_role_left(Role, A)`, `regia_role_emptied(Role)` | `WHEN Role [?who] LEFT`, `WHEN Role EMPTIED` |

## `regia-jason` additions

- Internal actions `regia.spawn_agent(Kind, Name, Body)` and `regia.send(Receiver, Ilf, Content)`.
- Nothing for Quota counting (ADR 0013).


## Trace entries

**Warnings**

- `T3301` A `regia_join` that makes no sense: a name starting with `regia_`, an Agent already in the Program, a kind with no Agent declaration, or a missing or invalid `port` (chapter 36). It is ignored.
- `T3302` A `regia_leave` for an Agent that isn't in the Program, ignored.
- `T3303` An Infrastructure send to an agent that doesn't exist, caught by `regia.send`. A designer's `TELL` or `ASK` to an Agent who has left writes chapter 19's `T1901` instead.
- `T3304` A join after the Root Staging has ended: the agent is created, but joins no cast.

## Not decided here

- The `regia_join` body fields, the kind's settings and Propensity values in the Root Director's file (`regia_kind`), and the `.jcm` names of starting Agents: chapter 36.
- How the Root Director's body receives `regia_join` and `regia_leave` next to `regia_event` and `regia_fact`: chapter 37.
- The Trace entries for nonsensical reports, caught sends, and joins after the Root Staging has ended: chapters 34 and 35.
- How a Conformance case scripts joins and leaves: `> join` and `> leave` steps, played by `ScriptedGame` as `regia_join`/`regia_leave` (chapters 34 and 35).
