# Stagings and Subplots in Jason

How the Jason Target runs Stagings: what identifies a Staging, how Directors are named, how a parent starts a Subplot's Director with its cast, how a Staging ends children first, and how the parent hears a Subplot's ending. Decided in the ticket *Stagings and Subplots runtime in ASL* (`.scratch/regia-2/issues/37-stagings-runtime.md`). It builds on chapter 28's layout, chapter 29's Givings and chapter 30's Directors, and implements chapter 17 (Subplots and Stagings) and the ending parts of chapter 20. It was checked against Jason 3.2.1 (`.create_agent`, `.kill_agent`), before Regia moved to Jason 3.3.2 (chapter 28). A Role that starts empty was settled in the ticket *What a Staging runs when it starts* (`.scratch/showcase-1-5/issues/17-staging-start.md`). Plot arguments, `RUNNING`, `END SUBPLOT` (now `DROP SUBPLOT`) with a pattern, the parent's ending Plans after ADR 0030, `EXITED, BY PARENT` and the Root's Action relay while it ends were decided in the ticket *Subplot arguments and endings in ASL* (`.scratch/showcase-1-5/issues/19-subplot-endings.md`). The relay was replaced by each Director sending its own Actions in the ticket *A Director doing its own Actions* (`.scratch/director-game-link/issues/04-doing-its-own-actions.md`). `FINISHED` and `DROP SUBPLOT` replaced `ENDED WITH`, `ENDED WITHOUT OUTCOME` and `END SUBPLOT` in the ticket *Endings and kind words* (`.scratch/syntax-review/issues/10-endings-and-kind-words.md`, ADR 0047).

## One Director agent per Staging

Every Staging is **its own Jason agent** running its Plot's Director file (chapter 28) on `regia.DirectorAgent` (chapter 30). Two duels are two agents running `directors/HonorDuel.asl`. This is why chapter 30's Director beliefs (`regia_phase`, `regia_standing`, …) carry no Staging argument.

### The Staging's identity is the Director's name

A Staging is identified by **its Director's Jason agent name**. Nothing else names it.

- Agents learn it from `[source]`, never from a message's arguments, so it can't be forged or go stale.
- The Giving record therefore has **one column** for both: `regia_give` and `regia_take` no longer carry a Staging, and the record is `regia_given(Playbook, Director, Target, Rank, Bindings, Until)` (chapter 29).
- The cast copy is keyed by it: `regia_cast(Director, Role, Agent)`.
- A `SIGNAL` goes to the `Director` of each Giving, which is its Staging (chapter 07).
- `FROM DIRECTOR` (chapter 05) matches a Sender `D` when the Agent holds some `regia_holds(P, D, …)` (a Giving, or one in a closing's snapshot, chapter 29) for the Playbook whose Plan is being matched. It is read from the record, not from the name.

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
| Its Plot's arguments | Subplot Director of a Plot with parameters | `regia_args([Value, …])`, from `regia_start` |
| A running child Staging | Director | `regia_child(Director, Plot, Args, Until)` |
| Ending, and with which Outcome | Director | `regia_ending(Outcome)` |

- The Root Director has no `regia_parent`.
- Chapter 28's `regia_plays` row is **retired**: an Agent plays `Role` in Staging `D` exactly when it holds `regia_cast(D, Role, Me)` from the cast copy, which every cast Agent gets (chapter 30).
- No Director reads `regia_child` to pass a percept on: each hears the game for itself (chapter 30, *Hearing the game*). `DO` going up the tree (chapter 30) reads `regia_parent`.

## Starting a Subplot

`START SUBPLOT HonorDuel(?offender), MAPPING …` compiles to `!regia_start_subplot__honorDuel__N`, an `[atomic]` plan on the parent:

1. **Work out the arguments**: the list `Args` of the Plot's arguments in parameter order, `[Offender]` for `royal_banquet.regia:92`. They are filled (`R1710`). A Plot without parameters has `[]`.
2. **Resolve the cast** (chapter 17): a whole-Role Mapping takes everyone in the parent's `regia_cast(Me, Role, _)` **now**; a counted pick picks at random, no Agent twice in one Statement (chapter 15). A Role with `EXCEPT` is read through `regia_reach` (chapter 30), so `MAPPING Guest EXCEPT ?offended, ?offender AS Spectator` leaves both duellists out of the snapshot. The result is a list `[cast(challenger, alice), cast(spectator, bob), …]`.
3. **Create the child** with `regia.start_staging(honorDuel, Child)`.
4. **Record it**: `+regia_child(Child, honorDuel, Args, Until)`. `Until` is `phase(feast)` for `START SUBPLOT …, UNTIL EXITED` in a `DURING feast` Plan, and `staging` otherwise, as for `regia_give` (chapter 29). Leaving the Phase ends the child (chapter 30, *`ENTER`*, step 3).
5. **Send the start**: `.send(Child, achieve, regia_start([cast(…), …], Prefix, Args))`, where `Prefix` is the parent's `regia_rank_prefix` plus HonorDuel's level under this Plot (chapter 32).

The parent's Body carries on at once (chapter 17). It sends the child no game Facts: the child asks the game for them when it attaches (chapter 30, *Hearing the game*).

On the child, `regia/director.asl` handles it in two steps. The start stores what the parent sent and attaches:

```
@regia_start[atomic]
+!regia_start(Cast, Prefix, Args)[source(P)] : not regia_parent(_)
   <- +regia_parent(P);
      +regia_rank_prefix(Prefix);   // chapter 32
      if (Args \== []) { +regia_args(Args) };
      // add regia_cast(Me, Role, A) for each cast(Role, A) in Cast
      regia.attach.          // chapter 30: register, and ask the game for its starting state
```

When the game's reply comes through the link, the Director's intake adds its Facts without events and posts `regia_attached` with the Agents of the cast that have already left (chapter 30):

```
@regia_attached[atomic]
+!regia_attached(Left)
   <- // remove regia_cast(Me, _, A) for each A in Left
      !regia_begin.          // chapter 30: initial Phase, cast copies, setups, EMPTIED, ENTERED
```

The Root takes the same second step after its own start (chapter 33).

### Plot arguments

A Plot's parameter is a Placeholder filled in every Block of the Plot (chapter 17). The child keeps its arguments as one belief, `regia_args([alice])`, added before `!regia_begin`, so the setups already read it. A Plot without parameters has no such belief, and neither does the Root, which takes none (`R2114`).

Every generated plan whose Block names a parameter reads it at the head of its context, right after the Phase guard. This holds for Trigger plans, `ENTERED`, `EXITED` and `EXITED, BY PARENT` plans, `AFTER` bodies and setups. The parameter becomes the Jason variable chapter 39 names for its Placeholder (`?offender` → `Offender`). The showcase's `HonorDuel` never names `?offender` in its own Blocks: the argument only tells its Stagings apart for the parent. If a Challenger setup did tell the Challenger who to face (`TELL ?offender …`) and a `fight` Plan waited for `conceded(?offender)`, they would be:

```
+!regia_setup(plot, challenger, A) : regia_args([Offender])
   <- …
+conceded(Offender)[source(S)] : regia_phase(fight) & regia_args([Offender]) & regia_cast(_, defender, S)
   <- …
```

- Jason unifies the trigger before it tests the context, so a Trigger that names a parameter (`WHEN conceded(?offender)`) binds it from the event, and `regia_args` then **tests** it, as for any filled Placeholder (chapter 03).
- A plan that names no parameter doesn't read the belief.

- A Role mapped from a parent Role that is empty when `START SUBPLOT` runs **starts empty**, and so does one whose `MAPPING ?who` was dropped because `?who` had left (chapter 30, *One Agent*). That is not an error. `!regia_begin` posts `regia_role_emptied` for it after the setups and before the entry Plans (chapter 30), so `WHEN Defender EMPTIED: END PLOT WITH duel_abandoned.` (`honor_duel.regia:66`) ends a duel whose Defender never came. An entry Plan that has already begun is stopped by that ending, like any other Plan of the Staging (*The walk*).
- How the **Root** Director gets its starting cast (from the `.jcm`'s Agents and the game) is an initial belief, `regia_start_cast`, compiled in (chapter 33); the Agents' names are chapter 36. It then runs the same `!regia_begin`, which also runs the setup lines of kinds and individual Agents (chapter 30).

## Ending a Staging

Every ending follows **one path**, whether the Staging ended itself with `END PLOT`, its parent ended it (`DROP SUBPLOT`, or the parent ending), or it is the Root.

### The walk

On Director `D`, with Outcome `O` (`none`, or the Cue term of `END PLOT WITH`, such as `duel_settled(alice)`), and `By` (`self` for its own `END PLOT`, `parent` for `regia_end`):

1. **Stop and exit** (`[atomic]`, `!regia_end_plot(O, By)`): chapter 30's transition step 1 for the current Phase (stop its Plans), then the exit Plans, each to completion: with `By = parent`, `!regia_exited_by_parent(phase(Ph))`, then `!regia_exited(phase(Ph))`, then `!regia_exited_by_parent(plot)`, then `!regia_exited(plot)`; with `By = self`, only the two `regia_exited`. A failing one is traced and the ending carries on. Then **remove `regia_phase`**, stop every remaining intention of the Director except this one, and add `regia_ending(O)`. Write the `staging` entry (chapter 34): `ENDED BY PARENT` when `By = parent`, else `FINISHED WITH O`, or `FINISHED` when `O` is `none`.
2. **End the children**: send `achieve regia_end` to every `regia_child(C, _, _, _)`, then **wait** for a `regia_ended` from each.
3. **Take the Givings away**: send `achieve regia_end_staging` to every Agent in `regia_cast(Me, _, _)` (below).
4. **Tell the parent**: send `achieve regia_ended(Plot, O)` to `regia_parent`, if there is one.
5. **Go**: `.kill_agent` on itself, which detaches it from the game link. The Root Director first tells the game the story has ended, with `regia.end_story(O)` (chapter 37).

Steps 3 to 5 are `!regia_finish`, an `[atomic]` plan run as soon as no `regia_child` is left: at the end of step 1 if `D` has no children, otherwise when the last child's `regia_ended` arrives.

**Why wait.** Chapter 17 ends children before parents. On an Agent cast in both, that means the child's Givings go before the parent's, so a Plan of the Subplot's Playbook is never left running on a Goal whose recipe the parent's Playbook just lost. Jason doesn't order messages from different senders, so the only way to get that order is for the parent to send its take-aways after its children have sent theirs.

### A child ended by its parent

A child receiving `regia_end` from its `regia_parent` runs the **same walk**, with Outcome `none` and `By = parent`:

- It runs its current Phase's `EXITED` and `DURING PLOT`'s `EXITED`, exactly as with its own `END PLOT`. A duel cut short by the guards can still `TELL` its Spectators. `EXITED` can't `WAIT` (chapter 20), so it can't hold the ending up.
- **`EXITED, BY PARENT`** (chapter 20) runs before each plain `EXITED`. `regia_end` is the only way a parent ends a child, whether by `DROP SUBPLOT`, by `UNTIL EXITED` or by ending itself, and it is accepted only from the parent, so the message needs no flag: receiving it is what "by parent" means. Each `WHEN EXITED, BY PARENT` Block compiles to a plan for the generated Goal `regia_exited_by_parent(phase(fight))` or `regia_exited_by_parent(plot)`, with a catch-all that does nothing, as for `regia_exited` (chapter 30). The Root is never ended from above and never runs it.
- `honor_duel.regia:72` and `poisoning.regia:19` both `DO` an Action there. The child sends it on the game link itself, as every Director does (chapter 30, *Custom Actions in a Director*), so a parent that is ending, or the Root, plays no part in it. The `DO` waits for the game inside the atomic walk, as in a Phase's `EXITED` (chapter 30, *A `DO` in `EXITED`*).
- A child **already ending** (it has `regia_ending(_)`) ignores `regia_end`: it will send `regia_ended` anyway.
- `regia_end` is accepted only from the `regia_parent`.

### `regia_ended`: the ack and the notification are one message

The parent's `regia/director.asl` accepts `regia_ended(Plot, O)` only from a Director it holds as `regia_child(C, Plot, Args, _)`, and in one `[atomic]` step:

- **If the parent is ending**, it is an ack: remove `regia_child(C, Plot, Args, _)`, and run `!regia_finish` if none is left. No Trigger fires; the parent is going too (chapter 17).
- **Otherwise** the child ended on its own: remove the record, reading `Args` from it, and post `!!regia_subplot_endings(Plot, Args, How)`, with `How` being `finished(O)`, `O` being the Outcome or `none` (*The parent's ending Plans*, below).
- **From a Director it no longer holds as a child**, it is ignored. This settles the race between `DROP SUBPLOT` and a child that ends itself at the same moment: `DROP SUBPLOT` has already removed the record and posted the `DROPPED` ending, so the parent hears that Staging's ending once, as `DROPPED`.

### `DROP SUBPLOT`

`DROP SUBPLOT HonorDuel(?q).` is one `[atomic]` step. For every `regia_child(C, honorDuel, Args, _)` whose `Args` unify with the written pattern (`[Q]` with `?q` filled, `[_]` for `?` or an unfilled Placeholder, `[]` for a Plot without parameters):

1. remove the record;
2. send `achieve regia_end` to `C`;
3. post `!!regia_subplot_endings(honorDuel, Args, dropped)`, once per Staging ended, with that Staging's own arguments.

`DROP SUBPLOT HonorDuel(?)` (`royal_banquet.regia:107`) is `regia_child(C, honorDuel, [_], _)`, so it ends every duel. It **doesn't wait** and doesn't stop the Body (chapter 17). The posted endings are picked after the Body, so a Statement written after `DROP SUBPLOT` runs first. Each child ends its own subtree children first, and its later `regia_ended` is ignored. With no such child, it does nothing. Each child stops hearing the game when its own walk detaches it. An `UNTIL EXITED` child ended at `ENTER` step 3 takes the same three steps (chapter 30).

### `RUNNING`

`<Plot> RUNNING` reads the record (chapter 17). It holds from the moment `START SUBPLOT` adds the record until the record is removed: by `DROP SUBPLOT`, by `ENTER` step 3, or by the child's `regia_ended`, each before the ending is posted. So a `DROPPED` or `ENDED` Plan already sees the Staging gone.

| Regia | ASL |
| --- | --- |
| `HonorDuel(?o) RUNNING`, `?o` filled or not | `regia_child(_, honorDuel, [O], _)` |
| `NOT HonorDuel(?offender) RUNNING` (`royal_banquet.regia:91`) | `not regia_child(_, honorDuel, [Offender], _)` |
| `COUNT(HonorDuel(?) RUNNING)` | `.setof(A, regia_child(_, honorDuel, A, _), L) & .length(L, N)` |
| `Poisoning RUNNING` | `regia_child(_, poisoning, [], _)` |

`COUNT` goes through `.setof` on the argument list, so two duels over the same quarrel count once, as chapter 17's distinct Matches require.

### An ending Director hears nothing

While it waits for its children, a Director has **no current Phase**, and that is what "ending" means to the generated code:

- Phase plans are already guarded by `regia_phase(feast)` (chapter 30).
- Every **`DURING PLOT` Trigger plan** now starts its context with `regia_phase(_)` too. Without a Phase, no Trigger, Signal, percept, `JOINED`, `LEFT` or `ENDED` Plan applies.
- The generated `regia_exited(plot)` and `regia_exited_by_parent(plot)` plans have no guard, so step 1 can still run them.
- **It stops hearing the game** at step 1, with `regia.stop_hearing`, once `regia_phase` is removed (chapter 30, *Hearing the game*): the link delivers it no more Facts or Cues. It stays attached, so it still gets leaves and keeps its cast right for step 3 (chapter 33, *Every Director hears a leave*), until step 5's kill detaches it. A percept already in its mailbox finds no `regia_phase` and is ignored. Of what the children send, only `regia_ended` is handled.
- **It still acts.** Its `EXITED` Plans' `DO`s go out on the game link, and their replies still reach it after `regia.stop_hearing`, which stops Facts and Cues only (chapter 37, *Custom Actions in a Director*). Stopping its other intentions at step 1 calls off their waiting Actions (ADR 0038). If it detaches with an Action still waiting, the link calls that Action off; a `WITHOUT WAITING` Action's late outcome is traced by the link and never delivered.
- No new belief is needed for this: `regia_ending(O)` only keeps the Outcome until step 4.

### What an Agent does: `regia_end_staging`

Chapter 29's per-Playbook `regia_take(p, S, all)` on ending is **replaced** by one message per cast Agent, handled by an `[atomic]` plan in `regia/agent.asl`:

```
@regia_end_staging[atomic]
+!regia_end_staging[source(D)]
   <- // remove every regia_given(_, D, _, _, _, _), every regia_aside(_, D, _, _, _, _) and every regia_cast(D, _, _)
      // the Playbooks whose last Giving went close, in one take step (chapter 29): their removed
      // regia_given go to the closing's snapshot, then regia.stop_playbook and regia_close
```

- The Director doesn't track what it gave (chapter 29), and the Agent's own record says which Playbooks lose their last Giving.
- It is one atomic step, so the Agent never holds half of an ending Staging.
- Without the cast copy, `TELL host` through a `live` binding of that Staging finds nobody, and `FROM DIRECTOR` no longer matches `D`.

### The Root Director's `END PLOT`

The Root Staging ends by the same walk, so every Staging ends and every Agent loses every Giving. At step 5, the Root Director sends the game `regia_story_ended` with the Outcome through the game link (chapter 37), and is then **killed like any other Director**. It holds nothing the run still needs: the connection belongs to the game link, which keeps killing Agents that leave and drops joins (chapter 33). Agents keep running with no Givings.

- Revised in the ticket *Messages for the whole run* (`.scratch/director-game-link/issues/05-messages-for-the-whole-run.md`). **Rejected:** keeping the Root's agent alive and idle to create and kill agents after the story. It kept one Director doing Program-wide work for the game.

## The parent's ending Plans

A Subplot's ending is heard like a Goal's (chapter 17, ADR 0030, ADR 0047): the specific Trigger's Plan, then the plain `ENDED` Plan. The translation follows chapter 40's ending goals. There is one generated Goal per kind:

| Trigger | Generated goal |
| --- | --- |
| `WHEN P FINISHED WITH e` | `+!regia_subplot_finished(p, Args, e, Heard)` |
| `WHEN P FINISHED` | `+!regia_subplot_finished(p, Args, _, Heard)` |
| `WHEN P DROPPED` | `+!regia_subplot_dropped(p, Args, Heard)` |
| `WHEN P ENDED` | `+!regia_subplot_ended(p, Args, Heard)` |

- **One intention runs both.** Every ending posts `!!regia_subplot_endings(p, Args, How)`: `finished(O)` from `regia_ended`, with `O` the Outcome or `none` for a bare `END PLOT`, and `dropped` from `DROP SUBPLOT` and `ENTER` step 3. That plan, in `regia/director.asl`, runs the specific goal for `How`, then `regia_subplot_ended`, each as a subgoal **to completion**, as chapter 40's `regia_endings` does.
- **Each subgoal is picked when it is posted**, so it is heard like any Director Trigger: the plan of the Phase current at that moment, else `DURING PLOT`'s, ranked by chapter 32. Every plan has its Phase guard; `DURING PLOT`'s plans have `regia_phase(_)`.
- **The arguments are matched in the trigger**, as a Trigger's always are (chapter 17): `WHEN HonorDuel(?) FINISHED WITH duel_settled(?winner)` (`royal_banquet.regia:125`) is `+!regia_subplot_finished(honorDuel, [_], duel_settled(Winner), Heard)`. Placeholders filled from the arguments or from `O` can be recipients, `ASSIGN` targets or `MAPPING`s (chapter 17).
- **`FINISHED` Blocks are tried in written order**, the first that matches runs (chapter 17), as chapter 40's `FAILED WITH` and plain `FAILED`. The `FINISHED` Blocks of one Phase, or of `DURING PLOT`, with and without `WITH`, share the Item `subplot_finished(p)` at their written `Pos`, and chapter 32's step 3 keeps the lowest applicable `Pos`. A plain `FINISHED` leaves the Outcome unbound, so it matches `none` too. When an ending matches none of them, the catch-all runs and `ENDED` still follows.
- **An `ENTER` or `END PLOT` in the specific Plan ends that Plan only.** `regia.end_body` drops the frames of the Plan that ran it (chapter 30, *`ENTER`*, step 7), so the dispatcher carries on with `regia_subplot_ended`, which is then picked under the new Phase or `DURING PLOT`. `WHEN Poisoning FINISHED WITH poison_taken: ENTER farewell` (`royal_banquet.regia:137`) would still run a plain `Poisoning ENDED` Plan, under `farewell`. After `END PLOT` the Director has no Phase, and only the catch-all applies.
- **A catch-all for each goal** does nothing but bind `Heard`. Chapter 17's "the ending is ignored" is that plan.

### `Heard` and `T3802`

`Heard` is an out-argument. Every generated plan of the four goals binds it to `heard` as its first step, and each catch-all binds it to `unheard`. Jason passes a subgoal's bindings back to the caller when it finishes (`TransitionSystem.java`, `joinRenamedVarsIntoIntentionUnifier`), so the dispatcher reads both:

```
+!regia_subplot_endings(P, Args, How)
   <- !regia_subplot_specific(P, Args, How, H1);   // the goal for How
      !regia_subplot_ended(P, Args, H2);
      if (H1 == unheard & H2 == unheard & How \== dropped) {
          regia.trace(unheard, info, "T3802", …)
      }.
```

`regia_subplot_specific` is shorthand for the per-kind goal, which the plan chooses by `How` with one clause per kind. `T3802` names the Subplot, its arguments, the Outcome (or says the ending was bare) and the parent's Phase (chapter 38). A `DROPPED` ending nobody hears writes nothing, since the parent caused it (chapter 17). An ending Plan that fails stops and writes `T2002` (chapter 20), and the dispatcher carries on: `regia/director.asl` holds one `-!` plan per goal, as chapter 40's `-!regia_<kind>` catchers, which writes the entry, binds `Heard` to `heard` and succeeds.

## Infrastructure state

Rows added to chapter 28's table, and one retired:

| Concept | Held by | Functor and arguments |
| --- | --- | --- |
| The Plot this Director runs | Director (initial belief of its file) | `regia_staging(Plot)` |
| Its parent Staging | Subplot Director | `regia_parent(Director)` |
| Its Plot's arguments | Subplot Director of a Plot with parameters | `regia_args([Value, …])` |
| A running child Staging | Director | `regia_child(Director, Plot, Args, Until)` |
| An ending in progress | Director | `regia_ending(Outcome)` |
| ~~A Role the Agent plays in a Staging~~ | | `regia_plays`: retired, read `regia_cast(D, Role, Me)` |

## Messages

| Message | From → to | Meaning |
| --- | --- | --- |
| `achieve regia_start(Cast, Prefix, Args)` | parent → new child | start the Staging with this cast and these arguments, at this place in the tree (chapter 32) |
| `achieve regia_end` | parent → child | end, with Outcome `none`, running `EXITED, BY PARENT` |
| `achieve regia_ended(Plot, Outcome)` | child → parent | the child has ended: an ack if the parent is ending, else the parent's ending Plans |
| `achieve regia_end_staging` | Director → each cast Agent | take away every Giving and the cast copy of this Staging |

## `regia-jason` additions

- Internal action `regia.start_staging(Plot, Name)`.

## Trace entries

None of its own. A failed `EXITED`, `EXITED, BY PARENT` or ending Plan writes chapter 20's `T2002`, and the ending carries on. A Subplot's own ending that no Plan hears writes chapter 38's `T3802` (*`Heard` and `T3802`*).

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025).

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- The Root Director's `.jcm` entry: chapter 36. Its starting cast is chapter 33.
- An Agent of a Subplot's cast leaving between `START SUBPLOT` and `regia_start`, and a `SIGNAL` or Message sent to a Director that has ended (`.kill_agent`): decided in chapter 33: the leave needs no special case, and sends go through `regia.send`.
- Telling the game the Root Staging has ended: chapter 37.
- Trace entries for an ending: chapters 34 (`staging` entries) and 35.
