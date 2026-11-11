# Stagings and Subplots in Jason

How the Jason Target runs Stagings: what identifies a Staging, how Directors are named, how a parent starts a Subplot's Director with its cast, how a Staging ends children first, and how the parent hears `WHEN <Plot> ENDED`. Decided in the ticket *Stagings and Subplots runtime in ASL* (`.scratch/regia-2/issues/37-stagings-runtime.md`). It builds on chapter 28's layout, chapter 29's Givings and chapter 30's Directors, and implements chapter 17 (Subplots and Stagings) and the ending parts of chapter 20. It was checked against Jason 3.2.1 (`.create_agent`, `.kill_agent`).

## One Director agent per Staging

Every Staging is **its own Jason agent** running its Plot's Director file (chapter 28) on `regia.DirectorAgent` (chapter 30). Two duels are two agents running `directors/HonorDuel.asl`. This is why chapter 30's Director beliefs (`regia_phase`, `regia_standing`, …) carry no Staging argument.

### The Staging's identity is the Director's name

A Staging is identified by **its Director's Jason agent name**. Nothing else names it.

- Agents learn it from `[source]`, never from a message's arguments, so it can't be forged or go stale.
- The Giving record therefore has **one column** for both: `regia_give` and `regia_take` no longer carry a Staging, and the record is `regia_given(Playbook, Director, Target, Rank, Bindings)` (chapter 29).
- The cast copy is keyed by it: `regia_cast(Director, Role, Agent)`.
- A `SIGNAL` goes to the `Director` of each Giving, which is its Staging (chapter 07).
- `FROM DIRECTOR` (chapter 05) matches a Sender `D` when the Agent holds some `regia_given(P, D, …)` for the Playbook whose Plan is being matched. It is read from the record, not from the name.

### Director names

- The **Root Director** is declared in the `.jcm` as `regia_director__<plot>`, for example `regia_director__royalBanquet` (chapter 36).
- A **Subplot Director** is created at runtime by `regia.start_staging(Plot, Name)`, a `regia-jason` internal action. It calls Jason's `createAgent` with the base name `regia_director__<plot>` (`regia_director__honorDuel`), the source `directors/<Plot>.asl` and `agentClass("regia.DirectorAgent")`, starts the agent, and unifies `Name` with the name Jason actually gave it. Jason makes a clashing name unique by adding a number, so two duels get two names.
- Names exist to be unique and readable in the mind inspector. The Infrastructure never parses them.
- Because Generated names start with `regia_`, Agent names the game reports must not (checked where joins are reported, chapter 33).
- Rejected: 1.0's names built from the clock's milliseconds, which can clash, and a wrapper is needed anyway because `.create_agent` returns the name only through an unbound first argument and can't set the agent class otherwise.

## A Director's records

| Concept | Held by | Functor and arguments |
| --- | --- | --- |
| The Plot this Director runs | Director (initial belief of its file) | `regia_staging(Plot)` |
| Its parent | Subplot Director | `regia_parent(Director)`, from the `[source]` of `regia_start` |
| A running child Staging | Director | `regia_child(Director, Plot)` |
| Ending, and with which Outcome | Director | `regia_ending(Outcome)` |

- The Root Director has no `regia_parent`.
- Chapter 28's `regia_plays` row is **retired**: an Agent plays `Role` in Staging `D` exactly when it holds `regia_cast(D, Role, Me)` from the cast copy, which every cast Agent gets (chapter 30).
- Percept forwarding (chapter 30) reads `regia_child` and `regia_hears`. `DO` going up the tree (chapter 30) reads `regia_parent`.

## Starting a Subplot

`START SUBPLOT HonorDuel, MAPPING …` compiles to `!regia_start_subplot__honorDuel__N`, an `[atomic]` plan on the parent:

1. **Resolve the cast** (chapter 17): a whole-Role Mapping takes everyone in the parent's `regia_cast(Me, Role, _)` **now**; a counted pick picks at random, no Agent twice in one Statement (chapter 15). The result is a list `[cast(challenger, alice), cast(spectator, bob), …]`.
2. **Create the child** with `regia.start_staging(honorDuel, Child)`.
3. **Record it**: `+regia_child(Child, honorDuel)`.
4. **Send the percept snapshot** (chapter 30): `regia.add_percepts` of the parent's `source(percept)` Facts that HonorDuel hears.
5. **Send the start**: `.send(Child, achieve, regia_start([cast(…), …], Prefix))`, where `Prefix` is the parent's `regia_rank_prefix` plus HonorDuel's level under this Plot (chapter 32).

The parent's Body carries on at once (chapter 17). Jason keeps one sender's messages in order, so the snapshot is in place before the start.

On the child, `regia/director.asl` handles it:

```
@regia_start[atomic]
+!regia_start(Cast, Prefix)[source(P)] : not regia_parent(_)
   <- +regia_parent(P);
      +regia_rank_prefix(Prefix);   // chapter 32
      // add regia_cast(Me, Role, A) for each cast(Role, A) in Cast
      !regia_begin.          // chapter 30: initial Phase, cast copies, Role setups, ENTERED
```

- A Role mapped from a parent Role that is empty when `START SUBPLOT` runs **starts empty**. That is not an error; the Director can `END PLOT` in `WHEN … EMPTIED` or never needs that Role.
- How the **Root** Director gets its starting cast (from the `.jcm`'s Agents and the game) is an initial belief, `regia_start_cast`, compiled in (chapter 33); the Agents' names are chapter 36. It then runs the same `!regia_begin`.

## Ending a Staging

Every ending follows **one path**, whether the Staging ended itself with `END PLOT`, its parent ended it (`END SUBPLOT`, or the parent ending), or it is the Root.

### The walk

On Director `D`, with Outcome `O` (`none`, or the Event term of `END PLOT WITH`, such as `duel_settled(alice)`):

1. **Stop and exit** (`[atomic]`, `!regia_end_plot(O)`): chapter 30's transition steps 1 and 2 for the current Phase (stop its Plans, run its `EXITED` to completion), then `!regia_exited(plot)` to completion; a failing `EXITED` is traced and the ending carries on. Then **remove `regia_phase`**, stop every remaining intention of the Director except this one, and add `regia_ending(O)`.
2. **End the children**: send `achieve regia_end` to every `regia_child(C, _)`, then **wait** for a `regia_ended` from each.
3. **Take the Givings away**: send `achieve regia_end_staging` to every Agent in `regia_cast(Me, _, _)` (below).
4. **Tell the parent**: send `achieve regia_ended(Plot, O)` to `regia_parent`, if there is one.
5. **Go**: `.kill_agent` on itself. The Root Director is **not** killed (below).

Steps 3 to 5 are `!regia_finish`, an `[atomic]` plan run as soon as no `regia_child` is left: at the end of step 1 if `D` has no children, otherwise when the last child's `regia_ended` arrives.

**Why wait.** Chapter 17 ends children before parents. On an Agent cast in both, that means the child's Givings go before the parent's, so a Plan of the Subplot's Playbook is never left running on a Goal whose recipe the parent's Playbook just lost. Jason doesn't order messages from different senders, so the only way to get that order is for the parent to send its take-aways after its children have sent theirs.

### A child ended by its parent

A child receiving `regia_end` from its `regia_parent` runs the **same walk**, with Outcome `none`:

- It runs its current Phase's `EXITED` and `DURING PLOT`'s `EXITED`, exactly as with its own `END PLOT`. A duel cut short by the guards can still `TELL` its Spectators. `EXITED` can't `WAIT` (chapter 20), so it can't hold the ending up.
- A child **already ending** (it has `regia_ending(_)`) ignores `regia_end`: it will send `regia_ended` anyway.
- `regia_end` is accepted only from the `regia_parent`.

### `regia_ended`: the ack and the notification are one message

The parent's `regia/director.asl` accepts `regia_ended(Plot, O)` only from a Director it holds as `regia_child(C, Plot)`, and in one `[atomic]` step:

- **If the parent is ending**, it is an ack: remove `regia_child(C, Plot)`, and run `!regia_finish` if none is left. No Trigger fires; the parent is going too (chapter 17).
- **Otherwise** the child ended on its own: remove `regia_child(C, Plot)` and post `!!regia_subplot_ended(Plot, O)`, which runs `WHEN <Plot> ENDED` (below).
- **From a Director it no longer holds as a child**, it is ignored. This settles the race between `END SUBPLOT` and a child that ends itself at the same moment: `END SUBPLOT` has already removed the record, and chapter 17 says the parent hears nothing when it ended the child on purpose.

### `END SUBPLOT`

`END SUBPLOT HonorDuel.` is one `[atomic]` step: for every `regia_child(C, honorDuel)`, remove the record and send `achieve regia_end` to `C`. It **doesn't wait** and doesn't stop the Body (chapter 17). Each child ends its own subtree children first, and its later `regia_ended` is ignored. With no such child, it does nothing. Percepts stop being forwarded to those children at once, since forwarding reads `regia_child`.

### An ending Director hears nothing

While it waits for its children, a Director has **no current Phase**, and that is what "ending" means to the generated code:

- Phase plans are already guarded by `regia_phase(feast)` (chapter 30).
- Every **`DURING PLOT` Trigger plan** now starts its context with `regia_phase(_)` too. Without a Phase, no Trigger, Signal, percept, `JOINED`, `LEFT` or `ENDED` Plan applies.
- The generated `regia_exited(plot)` plan has no guard, so step 1 can still run it.
- Forwarding percepts to children and passing `DO` up are guarded by `regia_phase(_)` as well. Only `regia_ended` from children is handled.
- No new belief is needed for this: `regia_ending(O)` only keeps the Outcome until step 4.

### What an Agent does: `regia_end_staging`

Chapter 29's per-Playbook `regia_take(p, S, all)` on ending is **replaced** by one message per cast Agent, handled by an `[atomic]` plan in `regia/agent.asl`:

```
@regia_end_staging[atomic]
+!regia_end_staging[source(D)]
   <- // remove every regia_given(_, D, _, _, _) and every regia_cast(D, _, _)
      // for each Playbook whose last Giving went: regia.stop_playbook (chapter 29)
```

- The Director doesn't track what it gave (chapter 29), and the Agent's own record says which Playbooks lose their last Giving.
- It is one atomic step, so the Agent never holds half of an ending Staging.
- Without the cast copy, `TELL host` through a `live` binding of that Staging finds nobody, and `FROM DIRECTOR` no longer matches `D`.

### The Root Director's `END PLOT`

The Root Staging ends by the same walk, so every Staging ends and every Agent loses every Giving. But the Root Director's **agent stays alive**, because it holds the game connection (chapter 30). It is idle: with no Phase, it ignores everything. Agents keep running with no Givings. Before going idle, it sends the game `regia_story_ended` with the Outcome (chapter 37).

## `WHEN <Plot> ENDED`

`!!regia_subplot_ended(Plot, O)` is an ordinary Director Goal, heard like any Director Trigger: the current Phase's Plan, else `DURING PLOT`'s, ranked as chapter 30 says.

- Each `WHEN HonorDuel ENDED [WITH e(…)]` Block becomes a plan for `+!regia_subplot_ended(honorDuel, O)`. Its context matches its own Outcome pattern (`e(…)` for `WITH`, anything for a plain `ENDED`, `none` for nothing) and **excludes the patterns of the Blocks written above it** in the same Phase or `DURING PLOT`. So the Blocks of one Phase are exclusive, and the first that matches in written order runs (chapter 17).
- A bare `END PLOT` arrives as `none`, which only a plain `ENDED` matches.
- A catch-all plan that does nothing handles an ending no Block matches, as for `ENTERED` and `EXITED` (chapter 30). Chapter 17's "the ending is ignored" is that plan.
- Placeholders in `WITH e(?w)` are filled from `O`, so `?w` can be a recipient, an `ASSIGN` target or a `MAPPING` (chapter 17).

## Infrastructure state

Rows added to chapter 28's table, and one retired:

| Concept | Held by | Functor and arguments |
| --- | --- | --- |
| The Plot this Director runs | Director (initial belief of its file) | `regia_staging(Plot)` |
| Its parent Staging | Subplot Director | `regia_parent(Director)` |
| A running child Staging | Director | `regia_child(Director, Plot)` |
| An ending in progress | Director | `regia_ending(Outcome)` |
| ~~A Role the Agent plays in a Staging~~ | | `regia_plays`: retired, read `regia_cast(D, Role, Me)` |

## Messages

| Message | From → to | Meaning |
| --- | --- | --- |
| `achieve regia_start(Cast, Prefix)` | parent → new child | start the Staging with this cast, at this place in the tree (chapter 32) |
| `achieve regia_end` | parent → child | end, with Outcome `none` |
| `achieve regia_ended(Plot, Outcome)` | child → parent | the child has ended: an ack if the parent is ending, else `WHEN <Plot> ENDED` |
| `achieve regia_end_staging` | Director → each cast Agent | take away every Giving and the cast copy of this Staging |

## `regia-jason` additions

- Internal action `regia.start_staging(Plot, Name)`.


## Trace entries

None of its own. A failed `EXITED` during an ending writes chapter 20's `T2002`, and the ending carries on.

## Not decided here

- The Root Director's `.jcm` entry: chapter 36. Its starting cast is chapter 33.
- An Agent of a Subplot's cast leaving between `START SUBPLOT` and `regia_start`, and a `SIGNAL` or Message sent to a Director that has ended (`.kill_agent`): decided in chapter 33: the leave needs no special case, and sends go through `regia.send`.
- Telling the game the Root Staging has ended: chapter 37.
- Trace entries for an ending: chapters 34 (`staging` entries) and 35.
