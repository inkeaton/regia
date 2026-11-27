# Cast changes and Quota counts in Jason

How the Jason Target handles the Cast changing and counts Quota Triggers. It covers the Root Director's starting cast, how the game reports Agents joining and leaving, who creates and kills their Jason agents, how every Director hears a leave, how Agents keep their cast copies and fixed bindings up to date, how a send to an agent that is gone is caught, and how Quota Triggers are counted in ASL. Decided in the ticket *Quota counts and cast changes in ASL* (`.scratch/regia-2/issues/39-quota-and-cast-changes.md`); the shape of `regia_start_cast` in *What a Staging runs when it starts* (`.scratch/showcase-1-5/issues/17-staging-start.md`). It builds on chapter 28's layout, chapter 29's Givings, chapter 30's Directors, chapter 31's Stagings and chapter 32's ranks, and implements chapters 18 (Quota Triggers) and 19 (cast changes). It was checked against Jason 3.2.1 (`.send`), before Regia moved to Jason 3.3.2 (chapter 28), and the latest VEsNA-Pro source (`vesna-pro-main/src/agt/vesna/VesnaAgent.java`). Where joins and leaves arrive, who kills a leaver, and joins after the story has ended were revised in the ticket *Messages for the whole run* (`.scratch/director-game-link/issues/05-messages-for-the-whole-run.md`): Directors reach the game through one shared **game link** (chapter 28), and no Director passes a game message on for another Staging.

## The Root Director's starting cast

The Transpiler names the starting Agents (`noble_1` …, chapter 36), so it knows the Root Plot's starting cast at compile time. In the Build of a `.regin` Entry, the Root Director's file carries it as an initial belief, next to `regia_rank_prefix([])` (chapter 32):

```
regia_start_cast([agent(king, agent(king), [host]),
                  agent(percival, agent(percival), [guest, guard]),
                  agent(hothead_1, kind(hothead), [guest]),
                  …]).
!regia_root_start.
```

- One `agent(Agent, Source, Roles)` entry per starting Agent, **in port order** (chapter 36): individual Agents by name, then the kinds' Agents.
- `Source` is `kind(hothead)` for an Agent of a kind, or `agent(percival)` for an individual Agent. It names the plan of the Agent's setup lines, `regia_instance_setup(Source, A)` (chapter 30).
- `Roles` are the Agent's Root Plot Roles as Jason names, in declaration order.

`regia/director.asl` handles the initial goal: add `regia_cast(Me, Role, A)` for each Role of each entry, then attach to the game link with `regia.attach`. On the game's reply, `!regia_attached(Left)` drops the starting Agents that have already left and runs `!regia_begin`, as for a Subplot (chapters 30 and 31). The setup lines run at `regia_begin`'s step 5, in this list's order, skipping an entry whose Agent is in `Left`. A Subplot Director gets its cast from `regia_start` instead (chapter 31), so it has no `regia_start_cast`.

- Starting Agents are **never reported** as joins. Starting is not joining (chapter 19).
- An Agent kind with no `COUNT` contributes no entries (chapter 21).

## What the game reports

Two more message types arrive on the game link, next to `regia_cue` and `regia_fact` (chapter 30). The game doesn't address them to any Director; the link delivers them:

| Type | `data` | Meaning |
| --- | --- | --- |
| `regia_join` | `{"kind": "noble", "name": "noble_7", …}` | the game spawned an Agent of this kind, with this name |
| `regia_leave` | `{"name": "noble_7"}` | the game removed this Agent from the Program |

- **A join goes to the Root Director only.** Joiners join only the Root Plot (chapter 19), so a join is the Root Staging gaining a cast member: its own business. The Root spawns the agent itself, from its own `regia_kind` beliefs, so the kinds never move into Java.
- **A leave goes to every attached Director** (*Leaving*, below). Each decides from its own cast whether it is concerned.
- The fields the new agent's body needs to connect to the game (its port, for example) also travel in `regia_join`. A join carries exactly `kind`, `name` and `port` (chapter 36).
- A body closing is **not** a leave. VEsNA-Pro kills an agent whose WebSocket errors or closes (`VesnaAgent.myHandleError`). That is VEsNA's business: the Agent stays in every cast, and sends to it are caught (below). Only `regia_leave` removes an Agent from the Program (chapter 19).

### Reports that make no sense

These reports are **ignored** with a Trace warning, never a failure:

- a `regia_join` whose name starts with `regia_` (chapter 31: Generated names start with it), or which names an Agent already in the Program: checked by the Root Director;
- a `regia_join` for a kind that isn't declared, or was removed with `NO KIND` (chapter 21): checked by the Root Director;
- a `regia_join` that arrives after the Root Staging has ended: dropped by the link, since there is no Program left to join and no Root Director to spawn it (`T3304`);
- a `regia_join` that arrives before the game has answered the Root's state request (chapter 30, *Hearing the game*): dropped by the link (`T3305`). The Root is the first Director to attach, so the game knows the story has begun once it has answered the first `regia_state`;
- a `regia_leave` for an Agent that isn't in the Program: checked by the link, which delivers it to no Director.

## Joining

The Root Director handles `regia_join` in one `[atomic]` plan:

1. **Check** the report (above).
2. **Create the agent** with `regia.spawn_agent(Kind, Name, Body)`, a `regia-jason` internal action. It creates a Jason agent of the kind's agent class and Role file(s), with the kind's settings and Propensity values (`RANDOM` drawn here, chapter 21) and the body fields from the report. It finds the kind in the Root Director's `regia_kind` beliefs (chapter 36).
3. **Add it to the cast**: `regia_cast(Me, Role, A)` for each of the kind's Roles.
4. **Tell the rest of the cast**: send `achieve regia_cast_joined(Role, A)` to every other Agent in `regia_cast(Me, _, _)`, once per Role.
5. **Run the join**: `!regia_join(A, Kind, Roles)` (chapter 30): the joiner's cast copy, its setups and its kind's lines, the standing Givings, then `JOINED`.

The new agent is created before any message reaches it, so Jason queues the cast copy and the Givings until it runs.

- Joining never triggers a Quota check (chapter 19). It only raises the denominator of `ALL` and `n% OF`, which the next check reads live.
- Joiners join only the Root Plot (chapter 19), so no `regia_cast_joined` goes down the tree.
- After the Root Staging has ended (chapter 31), the Root Director's agent is gone, and the link drops every `regia_join` with `T3304`. No agent is created: an Agent with no cast and no Director would do nothing for the Program. The game's character is left without a Jason agent.

## Leaving

### The leave walk

The link delivers `regia_leave(A)` to **every attached Director**, Root and Subplots alike, and each runs the **leave walk** on itself. On Director `D`, in one `[atomic]` plan:

1. **Not in my cast**: if there is no `regia_cast(Me, _, A)`, do nothing.
2. **Remove it**: note A's Roles here, then remove every `regia_cast(Me, _, A)`.
3. **Tell the rest of the cast**: send `achieve regia_cast_left(A)` to every remaining Agent in `regia_cast(Me, _, _)`.
4. **Quota counts**: remove every `regia_quota(_, _, _, _, _, A)`, then check every Quota Trigger that still has counts against the smaller Role (below). Each one now met posts `!!regia_quota_met(…)`.
5. **Director Triggers**: for each Role A played here, in Role declaration order, post `!!regia_role_left(Role, A)`, then `!!regia_role_emptied(Role)` if no `regia_cast(Me, Role, _)` is left.

Steps 4 and 5 are chapter 19's order: Quotas first, then `LEFT` and `EMPTIED`, Role by Role. The Plans for `regia_role_left` and `regia_role_emptied` are the designer's `WHEN Role [?who] LEFT` and `WHEN Role EMPTIED` Blocks. Each Goal has an empty failure plan for `error(no_applicable)` and `error(no_relevant)`, so a Role nobody listens for is silent (as for `regia_when__…`, below).

**The link kills the agent** with Jason's `killAgent`, once it has handed the leave to every attached Director, caught if the agent is already gone. Removing an Agent from the Program is plumbing for the whole run, not one Plot's job, so no Director does it. Nobody waits for the Directors' walks: a Director that sends to A after the kill is caught by `regia.send` (below). A Program never leaves an Agent running after it has left. The link still kills leavers after the Root Staging has ended.

### Every Director hears a leave

No Director passes a leave on for another Staging: there is no `regia_left` message. Every Director gets the leave from the link at about the same moment, and step 1 makes it a no-op on every Staging whose cast doesn't hold A.

- **An Agent leaving between `START SUBPLOT` and the child attaching** is the one race. The parent's atomic `START SUBPLOT` plan resolves the cast either before its own walk, and so without A, or after it. In the second case A is in the child's `regia_start` cast, while the leave reached the attached Directors before the child attached, so the child never hears it. A Subplot Director therefore **reconciles its cast when it attaches**: it drops every Agent of its `regia_start` cast that has already left the Program before `!regia_begin`, so its setups, `EMPTIED` and cast copies never see A. It learns who has left from the game, in the reply to its state request, `left` (chapters 30 and 37). The link delivers it nothing until that reply has gone through, so a leave the game sent before the reply is in `left`, and one sent after it is delivered and runs its walk as usual. The Root reconciles its starting cast the same way. Asking the Jason runtime instead was rejected: its local `killAgent` stops the agent on a thread of its own, so a leaver the link has just killed may still look alive.
- **An ending Director** (no `regia_phase`, chapter 31) is still attached and still runs the walk, so its cast is right when it sends `regia_end_staging`. The Goals of steps 4 and 5 find no applicable plan, since every Director Trigger plan is guarded by `regia_phase(_)`, and stay silent.
- **A Director that has gone** (`.kill_agent`, chapter 31) has detached and hears nothing.
- **Rejected:** walking the leave down the Staging tree, pruned by cast, on the grounds that a child's cast is drawn from its parent's. It made every Director in between pass a game message on for its children, and made a Subplot hear a leave only while its parent was running.

### What an Agent does

`regia/agent.asl` keeps the cast copies (chapter 29) up to date with two `[atomic]` plans:

```
@regia_cast_joined[atomic]
+!regia_cast_joined(Role, A)[source(D)]
   <- +regia_cast(D, Role, A).

@regia_cast_left[atomic]
+!regia_cast_left(A)[source(D)]
   <- // remove every regia_cast(D, _, A)
      // in every regia_given(P, D, T, R, B, U), regia_aside(P, D, T, R, B, U) and
      // regia_closing(C, P, D, T, R, B, U) (chapter 29), drop A from each fixed([…]) list in B
      // remove every regia_quota(_, _, _, _, _, A), then check this Agent's Quota counts again
```

- **Fixed lists are stripped per Director.** A counted pick or a `MAPPING ?who` from Director `D` only ever names Agents of `D`'s cast (chapter 30), so the `regia_cast_left` from `D` reaches every list that can hold A. The pick is not refilled (chapter 15).
- A leaver that played in several Stagings sends one `regia_cast_left` from each Director. The first removes A's Quota counts; the others find none, and their checks find nothing new.
- **Rejected:** one broadcast from the Root to every Agent that A has left. It needs fewer messages, but it races with Givings still coming from other Directors. Re-sending the whole cast copy on every change was also rejected: it is O(n²) messages for a crowd.

## Sends to agents that are gone

Jason's `.send` to an agent that doesn't exist throws `ReceiverNotFoundException` ("Receiver '…' does not exist!"). The action fails, and so does the sending plan. Chapter 19 needs that to be a trace entry, not a failure.

Every send in generated and Infrastructure code goes through **`regia.send(Receiver, Ilf, Content)`**, a `regia-jason` internal action. It does what `.send` does, catches the exception, writes a Trace entry, and **never fails**. Generated code never uses `.send`.

It covers:

- a `TELL` or `ASK` to a Placeholder holding an Agent that has left (chapter 19);
- a send racing with a leave: a Director that hasn't run its leave walk yet, or a body that closed before the game reported the leave;
- a `SIGNAL` or any message to a Director that has ended with `.kill_agent` (chapter 31). For example, an Agent signals before its `regia_end_staging` arrives. A closing Plan's `SIGNAL` to a Director whose Staging has ended is expected (chapter 15), so it is not `T3303`: the `SIGNAL`'s own `message` entry lists that Director as `ENDED`, at `info` (chapters 29 and 34).

`.broadcast` (for `EVERYONE`, chapter 30) never targets a missing agent and stays as it is.

- Why Java: catching a Jason infrastructure failure is the same kind of glue as the body. An ASL version that checks `.all_names` first leaves a window where the agent dies between the check and the send.

## Quota counts

Quota counting is **ASL**. `regia-jason` adds nothing for it (ADR 0013).

### The count

One belief per counted sender, per argument value:

```
regia_quota(Owner, Cue, Quantity, Role, Args, Sender)
```

| Argument | Holds |
| --- | --- |
| `Owner` | the Playbook's Jason name in an Agent; `plot` in a Director. A Playbook Role belongs to its Playbook (chapter 15), so two Playbooks' `neighbour` are two Triggers |
| `Cue` | the Cue's Jason name |
| `Quantity` | `all`, `of(3)` or `share(50)` |
| `Role` | the Plot Role (Director) or Playbook Role (Agent) |
| `Args` | the Cue's arguments, as a list. Counts are kept per argument value (chapter 18) |
| `Sender` | the Agent counted |

`(Owner, Cue, Quantity, Role)` is a **Quota Trigger** (chapter 18): one count, shared by every Block written with it.

### What is watched

The Transpiler writes, as initial beliefs:

- `regia_quota_watch(Owner, Cue, Quantity, Role)`: one per Quota Trigger. In a Director's file for its own Plot; in an Agent's Role file for each Playbook it includes. Playbook files stay Plans only (chapter 28).
- `regia_quota_in(Cue, Quantity, Role, Where)` in Director files: each Phase (`phase(feast)`) or `plot` that has a Block with that Quota Trigger.

### The dispatcher

Jason handles one plan per event, but chapter 18 needs both the plain Trigger and the count for the same Signal. For every Cue **name** that some Quota Trigger watches anywhere in the Program, the Transpiler emits a **dispatcher**. It is the only plan for the incoming event, and it moves the designer's plain Blocks for that Cue to a generated Goal:

```
// one per watched Cue, in each Director file and Role file that handles it
@regia_dispatch__ready[atomic]
+ready[source(S)]
   <- !!regia_when__ready(S);          // the plain Trigger, first
      !regia_count(ready, [], S).      // the count, in regia/director.asl or regia/agent.asl

// the designer's plain `WHEN ready, FROM Guest ?g:` in Phase reception
@regia_plan__royalBanquet__3[regia_phase(reception), regia_rank(0, 0)]
+!regia_when__ready(G) : regia_phase(reception) & regia_cast(_, guest, G) <- …

// nothing applicable, or no plain Block at all: the unheard entry for a Signal or a told Cue,
// and silence for a game Cue (chapters 30 and 39)
// (in a Director file; an Agent's Role file writes "T0702" with no plot and phase)
-!regia_when__ready(S)[error(no_applicable)] : S \== percept & regia_phase(Ph)
   <- regia.trace(unheard, info, "T3801", [cue(ready), sender(S), plot(royalBanquet), phase(Ph)]).
-!regia_when__ready(S)[error(no_relevant)] : S \== percept & regia_phase(Ph)
   <- regia.trace(unheard, info, "T3801", [cue(ready), sender(S), plot(royalBanquet), phase(Ph)]).
-!regia_when__ready(_)[error(no_applicable)].
-!regia_when__ready(_)[error(no_relevant)].
```

- The dispatcher takes over the trigger the plain Plans would have had, whatever form the incoming Cue has.
- The **Sender is an argument** of `regia_when__<e>`, after the Cue's own arguments. `FROM Guest ?g`, `FROM DIRECTOR` (chapter 31) and `FROM host` (chapter 29) compile to tests on it. Jason adds `source(self)` to Goals it posts itself, so an annotation wouldn't carry the Sender through.
- **The plain Trigger starts first**, then the count, which may post `regia_quota_met`. In chapter 18's example, `TELL ?g welcome` starts before `ENTER feast`. They are separate intentions, so "starts first" is all that is promised, as with `ENTERED` (chapter 30).
- A real failure in a plain Plan carries another `error(…)`, so the failure plans don't swallow it. It reaches the Trace as chapter 11 says.
- The failure plans are the dispatched Cue's catch-all: no `regia_unheard` plan is emitted for a dispatched Cue (chapters 30 and 39). They have no `regia_rank`, so `selectOption` leaves them to Jason's order, and the entry-writing pair comes first.
- **Precedence is unchanged.** Plans for `regia_when__ready` carry the same `regia_rank` as `+ready` plans would (`Item` `when(ready)`, chapter 32), and `selectOption` reads the annotation, not the trigger.
- Cues no Quota Trigger watches compile as before, without a dispatcher. Whether a Cue is watched is a whole-Program fact, and the Transpiler always sees the whole Program (chapter 23).
- An Agent kind playing several Roles gets each dispatcher once. A combination file includes it once, as for `regia_playbook` (chapter 36).

### Counting

`!regia_count(Cue, Args, S)` is an `[atomic]` plan in the Infrastructure. For each `regia_quota_watch(Owner, Cue, Quantity, Role)` that is **active**, and whose Role has S as a **member**:

1. Add `regia_quota(Owner, Cue, Quantity, Role, Args, S)`. A second Signal from S changes nothing, since each Agent counts once.
2. **Check** that Trigger for `Args` (below).

| | Director | Agent |
| --- | --- | --- |
| Active | `regia_phase(Ph)` and `regia_quota_in(Cue, Quantity, Role, phase(Ph))` or `… plot)` | `regia_is_given(Owner)` |
| Members of `Role` | `regia_cast(Me, Role, A)` | the union, over every `regia_given(Owner, …)`, of the `Role` bindings (chapter 29), **minus the Agent itself** |

An Agent never receives its own Messages, since recipients exclude the sender (chapter 29). So it is left out of its own denominators. Otherwise an Agent that is its own `neighbour` could never meet `ALL` (chapter 18).

### Checking

For a Trigger and an `Args` value, with `n` counted senders that are still members and `m` members:

| Quantity | Met when |
| --- | --- |
| `all` | `m > 0` and `n = m` |
| `of(k)` | `n ≥ k` |
| `share(p)` | `m > 0` and `n × 100 ≥ p × m` (at least that share, no rounding, chapter 18) |

When it is met, remove every `regia_quota(Owner, Cue, Quantity, Role, Args, _)`, so that value's count starts again from zero (chapter 18). Then post `!!regia_quota_met(Owner, Cue, Quantity, Role, Args)`.

- The designer's Quota Blocks are plans for `+!regia_quota_met(…)`, with the usual `regia_phase` guard (Director) or `regia_given` guard (Agent) and `regia_rank`. Placeholders in the Cue's arguments are filled from `Args`.
- The count is reset **before** any Block is chosen, and `regia_quota_met` has the two empty failure plans of `regia_when__<e>`, and no entry-writing pair: a Quota met with no Block writes chapter 18's `T1802` from the check. If no Block is a candidate, nothing runs and the count is still reset (chapter 18).
- Checks run on a count (above) and on a leave (the walk's step 5 in Directors, `regia_cast_left` in Agents). They never run on a join.

### Clearing counts

- **Director, on `ENTER`**: chapter 30's step 3 calls `!regia_quota_clear(Old)`. It removes the counts of every Quota Trigger with `regia_quota_in(…, phase(Old))` and no `regia_quota_in(…, plot)`. This also happens for an `ENTER` naming the current Phase: re-entering starts the count afresh, as it re-fires `ENTERED`.
- **Director, on ending**: nothing to clear. Without `regia_phase` no count is active, and the agent is killed (chapter 31), the Root Director too.
- **Agent, when the last Giving of P goes**: the take step (`regia_take`, `regia_set_aside`, `regia_take_phase`, `regia_end_staging`) removes every `regia_quota(p, …)` right after `regia.stop_playbook` and before starting the closing (chapters 29 and 31). This is ASL, not part of the internal action.
- Counting starts on a Playbook's first Giving with nothing to do: the count is active as soon as a `regia_given` exists. Senders before that were never counted.

## Infrastructure state

Rows filled in or added in chapter 28's table:

| Concept | Held by | Functor and arguments |
| --- | --- | --- |
| A Role's members | Director, and a copy in Agents | `regia_cast(Director, Role, Agent)` |
| The Root Plot's starting cast | Root Director (initial belief) | `regia_start_cast([agent(Agent, Source, Roles), …])` |
| A Quota Trigger count | Agent or Director | `regia_quota(Owner, Cue, Quantity, Role, Args, Sender)` |
| A Quota Trigger to count | Agent (Role file) or Director (initial beliefs) | `regia_quota_watch(Owner, Cue, Quantity, Role)` |
| Where a Director's Quota Trigger has Blocks | Director (initial beliefs) | `regia_quota_in(Cue, Quantity, Role, Where)` |

## Messages

| Message | From → to | Meaning |
| --- | --- | --- |
| `regia_join` (game link) | game → Root Director | an Agent of this kind entered the Program |
| `regia_leave` (game link) | game → every attached Director | this Agent left the Program |
| `achieve regia_cast_joined(Role, A)` | Root Director → each other cast Agent | add A to the cast copy |
| `achieve regia_cast_left(A)` | Director → each remaining cast Agent | remove A from the cast copy, the fixed bindings and the Quota counts |

## Generated Goals

| Goal | Runs |
| --- | --- |
| `regia_when__<e>(Args…, Sender)` | the plain `WHEN e` Blocks of a watched Cue |
| `regia_quota_met(Owner, Cue, Quantity, Role, Args)` | Quota Trigger Blocks |
| `regia_role_left(Role, A)`, `regia_role_emptied(Role)` | `WHEN Role [?who] LEFT`, `WHEN Role EMPTIED` |

## `regia-jason` additions

- Internal actions `regia.spawn_agent(Kind, Name, Body)` and `regia.send(Receiver, Ilf, Content)`.
- Nothing for Quota counting (ADR 0013).


## Trace entries

**Warnings**

- `T3301` A `regia_join` that makes no sense: a name starting with `regia_`, an Agent already in the Program, a kind that isn't declared or was removed, or a missing or invalid `port` (chapter 36). It is ignored.
- `T3302` A `regia_leave` for an Agent that isn't in the Program, ignored by the link.
- `T3303` An Infrastructure send to an agent that doesn't exist, caught by `regia.send`. A designer's `TELL` or `ASK` to an Agent who has left writes chapter 19's `T1901` instead.
- `T3304` A join after the Root Staging has ended, dropped by the link: no agent is created.
- `T3305` A join before the game has answered the Root's state request, dropped by the link: no agent is created. The game must send no `regia_join` before it has answered the first `regia_state` (chapter 37).

## Regia 1.5

In 1.5 (ADR 0025): the Root Director's starting cast, `regia_leave` and the leave walk without step 4's Quota counts, the link killing a leaver, and catching sends to agents that are gone.

Later: *Joining*, `regia.spawn_agent`, `T3304`, and all of *Quota counts*. In 1.5 the Root Director answers every `regia_join` by ignoring it, as with a report that makes no sense, and writes `T1902` (chapter 19). The body the game started for it is never given a cast.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- The `regia_join` body fields, the kind's settings and Propensity values in the Root Director's file (`regia_kind`), and the `.jcm` names of starting Agents: chapter 36.
- The game link itself: chapter 28, *The game link*. It keeps no list of the Program's Agents: whether a leaver is one (`T3302`) is asked of the Jason runtime, and a join is dropped when no Root is attached with its reply through: `T3305` before the Root's reply has passed, `T3304` once the Root has detached.
- How a Subplot's attaching is ordered with its `regia_start`, so it can reconcile its cast: ticket *A Director hearing the game for itself* (`.scratch/director-game-link/issues/03-hearing-the-game.md`).
- The Trace entries for nonsensical reports, caught sends, and joins after the Root Staging has ended: chapters 34 and 35.
- How a Conformance case scripts joins and leaves: `> join` and `> leave` steps, played by `ScriptedGame` as `regia_join`/`regia_leave` (chapters 34 and 35).
