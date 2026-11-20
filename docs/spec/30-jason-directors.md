# Directors in Jason

How the Jason Target runs a Director: its agent class, how each Director hears the game for itself, how the game reports Facts and Cues, how Phases are switched, what the Director does when a Staging starts and when an Agent joins, its record of standing Givings, Givings and Mappings for one Agent, how it receives Signals, and `EVERYONE`. Decided in the ticket *Director runtime in ASL* (`.scratch/regia-2/issues/36-director-runtime.md`); *Signals*, and the form of a game Cue and of a told Cue, in the ticket *Messages and told Facts in ASL* (`.scratch/showcase-1-5/issues/12-messages-in-asl.md`). The standing record's `Except` and `Until`, `EXCEPT` on recipients and Mappings, giving back to one Agent, and taking a Phase's Givings in the ticket *Exclusions, one Agent and a Phase in the Giving record* (`.scratch/showcase-1-5/issues/15-giving-record.md`). *Starting a Staging*, its setups, the setup lines of kinds and individual Agents, and `EMPTIED` at start in the ticket *What a Staging runs when it starts* (`.scratch/showcase-1-5/issues/17-staging-start.md`). *`ENTER`*'s steps, `UNTIL EXITED` Subplots, `AFTER`, `IN` and a waiting `DO` in `EXITED` in the ticket *Entering and leaving a Phase in ASL* (`.scratch/showcase-1-5/issues/18-phase-change.md`). The `DROPPED` ending at step 3, `regia.end_body` ending only its own Plan, and the Root's Action relay while it ends in the ticket *Subplot arguments and endings in ASL* (`.scratch/showcase-1-5/issues/19-subplot-endings.md`). *Hearing the game*, which replaced routing percepts down the Staging tree and the start snapshot of game Facts, in the ticket *A Director hearing the game for itself* (`.scratch/director-game-link/issues/03-hearing-the-game.md`). *Custom Actions in a Director*, which replaced the Root's Action relay, and a `DO` in `EXITED` waking, in the ticket *A Director doing its own Actions* (`.scratch/director-game-link/issues/04-doing-its-own-actions.md`). It builds on chapter 28's layout and chapter 29's Givings, and implements chapters 16 (Role setup), 19 (cast changes) and 20 (Directors). It was checked against the latest VEsNA-Pro source (`vesna-pro-main/`).

## The Director's agent class

A Director runs on **`regia.DirectorAgent`**, a class of `regia-jason` that extends Jason's `Agent`, **not** VEsNA-Pro's `VesnaAgent`.

- A Director has no Propensities (chapter 20), so it never needs VEsNA's Temper.
- **No Director has a body**, the Root included. Every Director attaches to the run's one **game link** (chapter 28), which holds the only connection Directors have to the game. The Root's `.jcm` entry has no `address` or `port` (chapter 36), and the Root differs from other Directors only in attaching *as* the Root, which is how it alone receives `regia_join` (chapter 33). Decided in the ticket *The game link's shape* (`.scratch/director-game-link/issues/02-game-link-shape.md`).
- Why not `VesnaAgent`: its body setup is private and parses `port` unconditionally, so an agent without a port fails to start, and a subclass can't skip that step.
- Directors still rank their Plans (a Phase over `DURING PLOT`, chapter 13). The ranking code is a helper shared by `regia.DirectorAgent` and the Agents' class (chapter 28), and doesn't live in either class.
- Every Staging is its own `regia.DirectorAgent`, and its name is the Staging's identity (chapter 31).

## What the game sends

VEsNA's own message types don't fit Regia. `signal` has a fixed `type(status, reason)` shape, and 1.0's `regia_event` type is gone from VEsNA-Pro. `regia-jason` adds two message types that Agents and the Root Director both understand:

| Type | `data` | Becomes |
| --- | --- | --- |
| `regia_cue` | `{"name": "insult_thrown", "args": [...]}` | a momentary event `+insult_thrown(…)[source(percept)]`, of Jason's `signal` type: no belief is kept. A told Cue is the same kind of event (chapter 39) |
| `regia_fact` | `{"op": "add" \| "remove", "name": "door_open", "args": [...]}` | `+door_open(…)[source(percept)]`; or `door_open(…)` removed **with every source**, so a Fact an Agent was also told goes too (chapter 39) |

- `name` is the External name of a game item (chapter 10). `regia-jason` translates it into the Regia name through the receiver's `regia_game` beliefs before anything else, so the table's `insult_thrown` and `door_open` are always Regia names. An Agent drops a name with no entry with `T2801` (chapter 28). A Director translates with its own `regia_game` beliefs, as an Agent does, but never meets a name it has no entry for: the link delivers it only what its `regia_hears` lists (*Hearing the game*, below).
- `args` is a JSON array of numbers, strings and arrays (chapter 37), turned into Jason terms on the way in.
- A game Cue and a game Fact are marked **`source(percept)`**. VEsNA's own `signal` messages to itself are marked `source(self)`, and its `addBel` marks beliefs `source(self)`, the same as a Director's own `LEARN`; the explicit source lets a Director tell what the game reported from what it learned itself (below).
- An Agent receives these by `regia.RegiaAgent` overriding VEsNA-Pro's public `myHandleMsg`. A Director receives them from the game link (chapter 28) through `regia.DirectorAgent`'s own message intake, which runs the same code (*Hearing the game*, below). Custom Actions and their results: chapter 37.

## Hearing the game

**Every Director hears the game for itself**, through the one game link (chapter 28). No Director passes a percept on to another, and none keeps game Facts for another Staging. Decided in the ticket *A Director hearing the game for itself* (`.scratch/director-game-link/issues/03-hearing-the-game.md`).

- **Which Facts and Cues a Plot hears is known at compile time.** Each Director file lists, as initial beliefs, `regia_hears(Plot, Name, Arity)` for **its own Plot only**: every Cue and Fact its Triggers and Contexts name. What its Subplots hear is theirs.
- **Attaching.** A Director attaches when it gets its start: a Subplot Director on `regia_start` (chapter 31), the Root on its `regia_start_cast` (chapter 33). `regia.attach` registers with the link the Director's name, the External names of what its `regia_hears` lists, and whether it is the Root. That registration is the link's routing table, which is plumbing.
- **Asking the game for its starting state.** Attaching makes the link send the game a **state request**, `regia_state` (chapter 37), naming the Facts this Director hears and the Agents of its starting cast. The game answers with `regia_state_result`: every instance of those Facts true now, and which of those Agents have already left. The game keeps no record of Stagings: it answers a question about its own state. Game information stays in the game: no parent and no link keeps it for a Director that starts later.
- **Nothing reaches a Director before its reply.** The link reads the game's messages one at a time, in arrival order. It registers a Director when it sends the request, but delivers nothing to it until the reply has gone through. The reply describes the game when the game sent it, and everything the game sends after it follows on the socket, so no Fact change and no leave is missed or counted twice. The link buffers nothing: what it doesn't deliver, the reply already covers.
- **Beginning.** The reply's Facts are added as `source(percept)` beliefs **without generating events**, in Java, and then `!regia_attached(Left)` is posted. Its plan drops every Agent of `Left` from the starting cast (chapter 33, *Every Director hears a leave*) and runs `!regia_begin` (*Starting a Staging*, below). So the setups, `EMPTIED` and the cast copies never see an Agent that has already gone, and **`LEARNED` doesn't fire** for starting state, just as joining Triggers don't fire for a starting Cast (chapter 19). Later changes arrive live and fire as usual.
- **Taking in a Fact or a Cue.** `regia.DirectorAgent`'s message intake turns a `regia_cue` or `regia_fact` from the link straight into the momentary event or the `source(percept)` belief, with the same Java code as an Agent's `myHandleMsg` (*What the game sends*, above). No ASL plan is involved, so `WHEN e:`, `WHEN f LEARNED:` and `GIVEN f` behave as in an Agent, and a game percept never looks like a Signal or a `FROM Role` Message.
- **Facts a Director learned itself** (`LEARN`, `source(self)`) stay its own: Facts belong to one Staging (chapter 20).
- **Stopping hearing, and detaching.** At the first step of its ending walk (chapter 31, *An ending Director hears nothing*), a Director calls `regia.stop_hearing`, and the link delivers it no more Facts or Cues. It stays attached, so it still gets a leave and keeps its cast right while it ends (chapter 33, *Every Director hears a leave*). It **detaches** only when its agent stops: `regia.DirectorAgent`'s stop hook detaches it, whether it is killed at the end of its walk or dies some other way, so the link never routes to a dead agent. A percept already in the mailbox of an ending Director finds no `regia_phase` and is ignored.
- **The Root** hears the game the same way. It differs only in attaching as the Root, which is how it alone gets `regia_join` (chapter 33). The Root is always the first Director to attach, since Subplots start only from a running Director. So the Root's request is the first `regia_state` the game sees, and the game sends no `regia_join` before it has answered it (chapter 37).
- **A missing link.** If the link is down when a Director attaches, or is lost before the reply comes, the attach completes at once with no Facts and nobody left, and the Staging starts. It can't hear the game anyway, and `T2802` or `T2803` says why (chapter 28). A game that is connected but never answers holds that Director unstarted. Avoiding that is the game's job, as for a `DO` with no reply (chapter 37).
- Which Facts and Cues the game sends the link is up to the game. A message no attached Director hears is dropped.
- **Rejected:** passing percepts down the Staging tree, with a parent's `regia_hears` covering its descendants and a **snapshot** of its own beliefs sent to a starting child. The parent kept game Facts and ran ASL on other Stagings' behalf. **The link caching the game's current Facts**, which would keep game information in Java (chapter 28). **Asking the runtime who has left**: Jason's local `killAgent` stops and removes an agent on a thread of its own, so a just-killed leaver may still look alive.

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

### `IN`

`IN feast` compiles to `regia_phase(feast)`, and `NOT IN feast` to `not regia_phase(feast)`, wherever a condition goes: a Context or an `IF` (chapter 39). From `royal_banquet.regia:115`:

```
IF IN arrival AND COUNT(seated(?)) >= COUNT(? PLAYS Guest)
   →  if (regia_phase(arrival) & .count(seated(_), S) & … )
```

The hidden `regia_phase__plot` is never named: `IN` in a Plot with no Phases is `R2014`.

### `AFTER`

Each `AFTER` Plan is its own generated Goal, **`regia_after(Scope, N)`**, numbered from 1 in source order within its Block: `regia_after(phase(betting), 1)` and `regia_after(phase(betting), 2)` for `honor_duel.regia:37` and `:43`, `regia_after(plot, 1)` for an `AFTER` in `DURING PLOT`. One event runs one plan, so two `AFTER`s of one Phase can't share a Goal.

Every Director file lists them, so fixed Infrastructure can post them:

```
regia_afters(phase(betting), [1, 2]).
regia_afters(phase(fight), [1]).
```

A Block with no `AFTER` has no line. The plan, from `honor_duel.regia:37`:

```
@regia_after__betting__1[regia_phase(betting)]
+!regia_after(phase(betting), 1) : regia_phase(betting)
   <- regia.wait(20000);                    // honor_duel.regia:37
      !regia_after_body(phase(betting), 1).

+!regia_after_body(phase(betting), 1) : <the Plan's Context>
   <- <the Body>.
+!regia_after_body(_, _).                    // catch-all
+!regia_after(_, _).                         // catch-all
```

- **The Duration is worked out once**, at the start of the plan, as for `WAIT` (chapter 39); a non-constant one goes into a generated variable first. `regia.wait` runs on the run's one clock, so a paused game holds the count (chapter 12).
- **The Context is tested when the time is up**: the `AFTER` Trigger fires then, so its Context and `GIVEN`s are those of `regia_after_body`. A false Context, or a Phase left before the event was picked, runs a catch-all, with no entry.
- **A Phase's `AFTER`s are posted right after its `ENTERED`**, in number order: at step 6 of `ENTER` (below) and step 7 of `regia_begin`. Both read `regia_afters`.
- **`DURING PLOT`'s count from the start of the Staging.** `regia_begin` posts them, in number order, after both entry Plans. Their plans carry no `regia_phase` annotation and have `regia_phase(_)` as their context, like every `DURING PLOT` Trigger plan, so they stop only when the Staging ends.
- **Two counts that end at the same moment** run in the order they were posted. `regia.wait` wakes them in that order, and so does `ScriptedGame`'s virtual clock (chapter 35).

### `ENTER`

`ENTER x.` calls `!regia_enter(x)`, an `[atomic]` plan in `regia/director.asl`. It follows chapter 20's six steps, plus a last one that ends the Body:

1. **Stop the old Phase's Plans.** `regia.stop_phase(Old)`, a `regia-jason` internal action like `regia.stop_playbook` (chapter 29), drops every intention running a plan annotated `regia_phase(Old)`. It drops them silently: Directors have no Goals, so nothing fires and nothing is traced. It **skips the intention running the `ENTER`**, which ends at step 7. It also drops the Phase's **queued entry events**, `+!regia_entered(phase(Old))` and `+!regia_after(phase(Old), _)`, the way `.drop_desire` removes queued events. An `ENTERED` Plan that transitions at once would otherwise leave its Phase's `AFTER` events queued, and on a re-entry they would find `regia_phase(Old)` true again and start a second count. The Phase's queued Trigger events (Signals, Cues, `LEFT`) are left in the queue, so the new Phase hears them.
2. **Run `EXITED` to completion**, as the subgoal `!regia_exited(phase(Old))`, inside the atomic plan. If it fails, a `-!regia_exited` plan writes the Trace entry (chapter 20) and the transition carries on: a Director Statement never fails. A `DO` in it waits for the game's reply, and the transition with it (*A `DO` in `EXITED`*, below).
3. **Take away what was given for the old Phase.**
   - Send `regia_take_phase(Old)` to every cast Agent (chapter 29), and remove every `regia_standing(_, _, _, _, phase(Old), _, _)`. A re-entered Phase's Givings are taken here and given again by its setups at step 5, so the Agents hear `REMOVED` and then `ASSIGNED` (chapter 15).
   - **End its `UNTIL EXITED` Subplots.** For each `regia_child(C, P, Args, phase(Old))` (chapter 31), remove the record, send `achieve regia_end` to `C`, and post `!!regia_subplot_endings(P, Args, dropped)`, as `DROP SUBPLOT` does. The transition doesn't wait for the child's `regia_ended`, which is ignored when it comes (chapter 31). The event is queued before `ENTERED`'s and is picked after the atomic plan, when `regia_phase(x)` already holds, so the `DROPPED` Plan **starts first** and is one of the new Phase's or `DURING PLOT`'s (chapter 17). It runs the `DROPPED` Plan and then the plain `ENDED` Plan (chapter 31, *The parent's ending Plans*).
4. **Change the Phase.** Replace `regia_phase(Old)` with `regia_phase(x)`, and write the `phase` Trace entry (chapter 34).
5. **Run the new Phase's setups**: `!regia_run_setups(phase(x))` (*Setups*, below), inside the atomic plan. Every setup Giving is in place before any of the Phase's Plans starts.
6. **Post the entry Plans**: `!!regia_entered(phase(x))`, then `!!regia_after(phase(x), N)` for each `N` of `regia_afters(phase(x), L)`. They start after the atomic plan, as ordinary intentions of the new Phase: they may `WAIT`, and they are stopped if the Phase is left.
7. **End the Body.** `regia.end_body` drops, silently, the frames of the Plan that ran the `ENTER`, with everything above them on its intention. `ENTER` ends its Body (chapter 20) even inside an `IF` branch with Statements after the `IF`, and in a `DURING PLOT` Plan too. For a Trigger's Plan that is the whole intention. For a Plan run as a subgoal of Infrastructure, such as a Subplot's `FINISHED WITH` Plan under `regia_subplot_endings` (chapter 31), the Infrastructure frame below carries on, so a plain `ENDED` Plan still runs after a specific one that transitioned. `END PLOT` ends its Body the same way.

Quota counts aren't cleared in 1.5 (*Regia 1.5*, below). When they are, `!regia_quota_clear(Old)` (chapter 33) runs at step 4, before the Phase changes.

`ENTER` naming the current Phase takes the same path, so it re-enters the Phase. `END PLOT` reuses steps 1 and 2 for the current Phase, then runs `!regia_exited(plot)` the same way. The rest of `END PLOT` is chapter 31.

The order of events after a transition from `feast` to `farewell` (`royal_banquet.regia:100`): any Signal or Cue that came in while `EXITED` waited on `clear_tables` was queued first, then `Poisoning`'s `dropped`, then `farewell`'s `ENTERED`. They start in that order, all with `regia_phase(farewell)` holding, and none waits for the one before.

### A `DO` in `EXITED`

An `EXITED` Plan may `DO` an Action and wait for it (`DO clear_tables.`, `royal_banquet.regia:103`). `WAIT` there is still `R2003`: a `DO` is the game's time, not the Plot's.

- **While it waits, the Director runs nothing else.** A suspended `[atomic]` intention holds back every other intention and event (research note *How Jason behaves where the translation waits*, branch `research/jason-facts`). Messages and the game's Cues and Facts are still read, and their events queue. They are heard after the transition, by the new Phase.
- **Every Director's `DO` resumes from Java.** The game link delivers `regia_action_result` into the mailbox of the Director that sent the Action (chapter 37, *Custom Actions in a Director*). `regia.DirectorAgent`'s Java intake takes it there and resumes `regia.act`, with no ASL plan involved. A suspended atomic intention still wakes on a message (`TransitionSystem.java:1620`), so the reply is read and the `DO` wakes inside the atomic plan. The Root and a Subplot's Director behave the same.
- **A game that never replies holds the Director forever.** That is the game's to avoid, as for any `DO` (chapter 37).
- A refused or failed `DO` fails the `EXITED` Plan, which writes `T2002`, and the transition carries on (step 2).

## Starting a Staging

Every Director file carries two initial beliefs about its Plot:

```
regia_initial_phase(arrival).
regia_roles([host, guest, servant, guard]).
```

- `regia_roles` lists the Plot's Roles as Jason names, in declaration order. `CAST` isn't in it.
- A Plot with no Phases has `regia_initial_phase(regia_phase__plot)`, its hidden Phase (*Phases*, above).

Once the Director has its cast (from `regia_start` or `regia_start_cast`, chapters 31 and 33) and the game's reply to its state request, with the Agents that have left dropped (*Hearing the game*, above), it runs `!regia_begin`, an `[atomic]` plan in `regia/director.asl`:

1. Add `regia_phase(Initial)`, read from `regia_initial_phase`. The initial Phase is current from the start. Write the Trace's start of the Staging (chapter 34): the `STAGING … STARTED` entry with the cast, then `PHASE -> <Initial>` (none for `regia_phase__plot`), then one `FACT +…` entry for each game Fact the state reply gave it. The `staging` entry is the Director's first, so the writer gives it its number there (chapter 35).
2. Send every cast Agent the **cast copy** (chapter 29) as one message: `achieve regia_cast_copy([cast(Role, Agent), …])`. `regia/agent.asl` replaces any copy it holds from that Director, the `[source]`, which is the Staging (chapter 31). Every cast Agent gets it, so the Director needn't track who already has one. It comes before every setup, so a live binding in a setup's Giving already finds its Agents.
3. **Run the Plot's setups**: `!regia_run_setups(plot)` (below).
4. **Run the initial Phase's setups**: `!regia_run_setups(phase(Initial))`.
5. **Run the setup lines of kinds and individual Agents**, on the Root Director only: for each `agent(A, Source, _)` of `regia_start_cast` (chapter 33), in its order, `!regia_instance_setup(Source, A)` (below). A Subplot Director has no `regia_start_cast`, and this step does nothing.
6. **Post `EMPTIED` for each Role that starts empty**: for each Role of `regia_roles`, in order, with no `regia_cast(Me, Role, _)`, `!!regia_role_emptied(Role)` (chapter 33); then `!!regia_role_emptied(cast)` if the cast is empty.
7. **Post the entry Plans**: `!!regia_entered(plot)`, then `!!regia_entered(phase(Initial))`, then `DURING PLOT`'s `AFTER`s, `!!regia_after(plot, N)`, then the initial Phase's, `!!regia_after(phase(Initial), N)`, each in number order (*`AFTER`*, above).

This is chapter 16's order (`CAST` setup, Role setups, the initial Phase's setups), then chapter 21's lines, then chapter 19's `EMPTIED` and chapter 20's entry Plans. Every setup is in place before any start-up Trigger runs.

Jason picks events in the order they were posted, so the `EMPTIED` Plans **start** first, then `DURING PLOT`'s `ENTERED`, then the Phase's. "Before" in chapters 19 and 20 means it starts first, not that it finishes first: a `WAIT` in one doesn't hold up the next. An `EMPTIED` Plan that ends the Plot (`WHEN Defender EMPTIED: END PLOT WITH duel_abandoned.`, `honor_duel.regia:66`) may therefore find an entry Plan already begun. The ending stops it and takes away what it gave (chapter 31), and an entry Plan not yet started finds no `regia_phase` and runs its catch-all.

Running the `EMPTIED` Plans to completion before posting `ENTERED` was rejected: a `WAIT` in an `EMPTIED` Plan would hold up the Staging's start, and `EMPTIED` on a leave doesn't hold anything up either.

### Setups

Every setup Block of the Plot (chapter 16) is one plan of the generated Goal **`regia_setup(Scope, Role, A)`**:

| Block | Plan |
| --- | --- |
| `CAST:` | `+!regia_setup(plot, cast, A)` |
| `ROLE Guest:` | `+!regia_setup(plot, guest, A)` |
| `DURING feast:` `ROLE Guest:` | `+!regia_setup(phase(feast), guest, A)` |

A catch-all plan that does nothing, `+!regia_setup(_, _, _).`, covers a Role with no setup, as for `ENTERED` and `EXITED`.

`!regia_run_setups(Scope)` is fixed Infrastructure in `regia/director.asl`. It runs `!regia_setup(Scope, cast, A)` for each Agent of `.setof(A, regia_plays(cast, A), L)`, then, for each Role `R` of `regia_roles` in order, `!regia_setup(Scope, R, A)` for each Agent of `.setof(A, regia_plays(R, A), L)`. A knight who is `Guest` and `Guard` gets the `CAST` setup once and each Role's setup once. Entering a Phase runs the same `!regia_run_setups(phase(x))`, at step 5 of `ENTER`.

A setup plan sends its Statements to `A` in the order written (chapter 16):

| Setup Statement | Sent |
| --- | --- |
| `ASSIGN P[, MAPPING …]` | `achieve regia_give(p, role(guest), Rank, Bindings, Until)` (chapter 29), with `Until` `staging` in the Plot's setup and `phase(feast)` in `feast`'s. The `CAST` setup's target is `role(cast)` |
| `LEARN f` | `tell f` |
| `PURSUE g` | `achieve g` |

- The Agent sees the Director as `[source]`, so `FROM DIRECTOR` matches (chapter 16).
- Every send goes through `regia.send`, so a `LEARN` writes `TELL <agent> <fact>` and a `PURSUE` writes `ASK <agent> TO <goal>` on the Director, with the setup line as `at` (chapter 34). A setup is not a Plan and writes no `plan` entry; its `ASSIGN` shows as the Agent's `GIVE` entry.
- A Statement whose arguments use Body arithmetic, the only kind that can go wrong, is compiled as its own subgoal with a `-!` plan that writes the Trace entry and returns, so the next Statement still runs. That is chapter 16's "skipped". Its Expressions are worked out inside the plan, for this Agent, so each Agent gets its own rolls (`LEARN purse(RANDOM(5, 20))`, `royal_banquet.regia:27`).
- **A setup's Givings are not standing**: no `regia_standing` record is written (*The standing-Giving record*). The setup itself runs again for a joiner, and a Phase setup's Givings are taken away on leaving the Phase by their `Until`, through `regia_take_phase` (chapter 29).

### Setup lines of kinds and individual Agents

The setup lines of a `KIND` or an `AGENT` (chapter 21) are run by the Root Director, at step 5 of `regia_begin`. Each kind and each individual Agent with lines is one plan of the generated Goal **`regia_instance_setup(Source, A)`**, with `Source` being `kind(hothead)` or `agent(percival)`:

```
+!regia_instance_setup(kind(hothead), A)
   <- regia.send(A, tell, grudge(percival, 2)).   // banquet.regin:19
```

- **`LIKE` is resolved at compile time.** A plan holds every line the kind or Agent ends up with: its bases' lines in `LIKE` order, then its own, with a line of its own replacing what it took (chapter 21). `AGENT percival, LIKE knight` gets `knight`'s lines, which are none, so it has no plan; it is not a `hothead` and holds no grudge.
- A catch-all plan that does nothing covers a kind or Agent with no lines.
- The lines are sent as a Role setup's are (*Setups*, above), with one difference: an `ASSIGN` is a Giving to that Agent, `regia_give(p, agent(a), Rank, Bindings, staging)`. Only `REMOVE P FROM ?who`, `FROM CAST ?who` and the Staging's ending take it away (chapter 29). It is not standing either.
- The plan is per kind, not per Agent, because a line's `RANDOM` is rolled for each Agent, inside the plan. A joiner (chapter 33) runs the same `!regia_instance_setup(kind(K), A)` after its Role setups.

## An Agent joining

How the game reports a join, and how the Director's `regia_cast` and the other Agents' copies are updated, are in chapter 33. Once that is done, the Director runs `!regia_join(Agent, Kind, Roles)`, an `[atomic]` plan:

1. Send the joiner the cast copy.
2. Run the `CAST` setup and each joined Role's setup for it, in Role declaration order, then the current Phase's (`regia_setup`, above), then its kind's lines (`!regia_instance_setup(kind(Kind), Agent)`).
3. **Replay the standing Givings** of the joined Roles and of `CAST`, in `Seq` order (below), as `regia_give(p, role(r), Rank, Bindings, Until)`, skipping each one whose `Except` leaves the joiner out (`regia_reach`, below).

After the atomic plan, it posts `!!regia_joined(Role, Agent)` for each joined Role in declaration order, which runs the `WHEN Role [?who] JOINED` Plans. This is chapter 19's order: setups, then standing Givings, then `JOINED`.

## The standing-Giving record

Each standing Giving is one belief on the Director:

```
regia_standing(Seq, Playbook, Role, Except, Until, Rank, Bindings)
```

| Argument | Holds |
| --- | --- |
| `Seq` | from a per-Director counter, `regia_standing_seq(N)`. Replay follows the order the Givings were made |
| `Role` | the target: `guest`, or `cast` for `ASSIGN P TO CAST` |
| `Except` | the target's list: `role(guard)` and `agent(alice)` items, as in a binding (chapter 29). It starts as the written `EXCEPT` and grows by narrowing (below) |
| `Until` | `staging`, or `phase(feast)` for `UNTIL EXITED` in a `DURING feast` Plan (chapter 29) |
| `Rank`, `Bindings` | as sent in `regia_give` |

- **Only a whole-Role `ASSIGN` is standing**, with or without `EXCEPT`. A counted pick and a Giving to `?who` aren't (chapter 19). A Role setup's `ASSIGN` isn't either: the setup itself runs again for a joiner.
- **An identical `ASSIGN` running again keeps its first `Seq`**, so its place in the replay order doesn't move. It is the same Giving (chapter 29).
- **A standing Giving lasts until `REMOVE`, the end of the Staging, or, with `phase(Ph)`, the Phase being left** (*`ENTER`*, step 3). Leaving another Phase doesn't remove it. 1.0's take-away in `on_exit` is gone.
- The record holds only what a replay and a giving back need (chapter 29): the Director doesn't track who holds which Giving.

What each Statement does to the record:

| Statement | `regia_standing` |
| --- | --- |
| `REMOVE P FROM Guest` | removes every record of `p` with `Role` `guest`, and adds `role(guest)` to the `Except` of every record of `p` with `Role` `cast` (chapter 15's narrowing) |
| `REMOVE P FROM CAST` | removes every record of `p` |
| `REMOVE P FROM Guest ?who` | adds `agent(who)` to the `Except` of every record of `p` whose target includes `Guest`: `Role` `guest`, or `cast` while `?who` plays `Guest` |
| `ASSIGN P TO Guest ?who` | removes `agent(who)` from the `Except` of those records. For each one where a **written** `EXCEPT` had left `?who` out, it resends `regia_give` to `?who` from the record, before the `regia_restore` (chapter 29) |
| `REMOVE P FROM ?who`, `FROM CAST ?who` | no change: `FROM CAST ?who` takes `?who`'s Givings, and none of the records was made to it |

- **What giving back lifts.** `ASSIGN P TO Guest ?who` lifts only what was done to `?who`: what `REMOVE … FROM Guest ?who` set aside, and a written `EXCEPT ?who` on a standing Giving. It lifts nothing that a whole-Role `REMOVE P FROM Guest` ended, so a `role(guest)` item on a `cast` record stays. A written `EXCEPT ?who` on a counted Giving isn't lifted either, since a pick never grows. When nothing is lifted, the Agent writes `T1506` (chapter 29).
- The record holds only what a replay needs (chapter 29): the Director doesn't track who holds which Giving.

## One Agent

`ASSIGN P TO ?who`, `REMOVE P FROM ?who` and `MAPPING ?who AS r` first check `regia_cast(Me, _, Who)`: is that Agent in this Staging's cast **now**?

- **If it is**, the Giving is `regia_give(p, agent(who), Rank, Bindings)` (chapter 29), or the Mapping is `bind(r, fixed([who]))`.
- **If it isn't**, the Giving or Mapping is dropped with a Trace warning. That covers an Agent that has left (chapter 20) **and** an Agent that was never in this Staging, such as one named by a game Cue's argument. A Director directs its own cast. Since every cast Agent already has the cast copy, nothing more needs tracking.

## Who plays a Role here

A Director reads its own Roles through a rule in `regia/director.asl`, the Plot-side twin of the Agents' `regia_plays/3` (chapter 29):

```
regia_plays(cast, A) :- .my_name(Me) & regia_cast(Me, _, A).
regia_plays(R, A)    :- R \== cast & .my_name(Me) & regia_cast(Me, R, A).
```

- `?x PLAYS Guest` in a Director's Context or `IF` is `regia_plays(guest, X)`.
- `COUNT(? PLAYS Guest)` is `.setof(A, regia_plays(guest, A), L) & .length(L, N)`, never `.count`: under `CAST` a knight, who plays `Guest` and `Guard`, would be counted twice (`royal_banquet.regia:62`).
- It reads the cast as it is now: a leaver is already gone from `regia_cast` when the `LEFT` Plan runs (chapter 33), so the recount at `royal_banquet.regia:115` sees the smaller hall.
- A counted pick (`MAPPING 1 OF Guest AS Poisoner`) draws from the same Agents, with `regia.pick` (chapter 39).

### A Role with `EXCEPT`

Every Director use of `Role EXCEPT …` reads one more rule, built on `regia_plays/2`:

```
regia_reach(R, Ex, A) :-
    regia_plays(R, A) & not .member(agent(A), Ex) &
    not (.member(role(XR), Ex) & regia_plays(XR, A)).
```

- `Ex` is the list as in a binding (chapter 29): `role(guard)` items, and `agent(alice)` items holding the Agent the Placeholder held when the Statement ran. A Placeholder holding no Agent is left out of the list, with `T1504`.
- It serves a **recipient** (`TELL Spectator EXCEPT ?offender duel_on`: `.setof(A, regia_reach(spectator, [agent(Offender)], A), L)`), the target of an `ASSIGN`, the pool of a **counted pick** (`ASSIGN Poisoning TO 1 OF Guest EXCEPT Guard`), a joiner's replay (*An Agent joining*), and the **Subplot Mapping** of chapter 31's step 1. `MAPPING Guest EXCEPT ?offended, ?offender AS Spectator` (`royal_banquet.regia:95`) is resolved there into the child's cast, a snapshot that needs no record.
- A whole-Role Mapping with `EXCEPT` in an `ASSIGN` isn't resolved here: it travels with the Giving as `live(guest, Ex)` and is read by the Agent (chapter 29).

Decided in the ticket *Roles an Agent reads* (`.scratch/showcase-1-5/issues/14-roles-an-agent-reads.md`).

## Signals

An Agent's `SIGNAL c` reaches the Director as a `signal` message, the same as a told Cue (chapter 39). The Director's plan for `WHEN c` is a plan for `+c[source(S)]`, with the Phase guard of *Phases*, and `S` is the signalling Agent:

| Trigger | Plan |
| --- | --- |
| `WHEN took_seat, FROM Guest ?g:` | `+took_seat[source(G)] : regia_phase(arrival) & regia_cast(_, guest, G)` |
| `WHEN took_seat, FROM Host:` | `+took_seat[source(S)] : regia_phase(arrival) & regia_cast(_, host, S)` |
| `WHEN duel_won, FROM ?winner:` | `+duel_won[source(Winner)] : regia_phase(…) & Winner \== percept` |
| `WHEN culprit_seized(?):` | `+culprit_seized(_)[source(_)] : regia_phase(_)`: no Sender test, so a game Cue of that name is heard too |

- A Director holds only its own Staging's `regia_cast` records, so the first argument is `_`.
- The cast test never rejects a real Signal by mistake. An Agent holds Givings only from Stagings whose cast it is in (*One Agent*, above), so only cast Agents can Signal this Director.
- A Signal is never `percept`, and a game Cue from the link is (*Hearing the game*, above), so a Sender form never matches the game.

### Nothing heard: `T3801`

For each Cue some Agent can Signal to this Plot, the Director file has one catch-all, chosen only when no other plan is (chapter 32), as the Agent's for `T0702` (chapter 39):

```
@regia_unheard__took_seat[regia_unheard]
+took_seat[source(S)] : S \== percept & regia_phase(Ph)
   <- regia.trace(unheard, info, "T3801", [cue(took_seat), sender(S), plot(royalBanquet), phase(Ph)]).
```

- It writes the entry when no plan of the current Phase or of `DURING PLOT` runs, including when every `GIVEN` fails: `finished_eating` arriving in `farewell` from `Dining`'s closing Plans (`dining.regia:48`), or `insult_thrown` outside `feast` (`noble_socializing.regia:29`).
- A Director that is ending has no `regia_phase` and hears nothing, so a Signal reaching it is dropped with no entry.
- A game Cue no plan takes is dropped silently.

## Messages from a Director

- `TELL Role f`, `TELL Role c` and `ASK Role TO g` send `tell f`, `signal c` (a Cue, chapter 39) or `achieve g` to each Agent with `regia_cast(Me, Role, A)` when the Statement runs (chapter 20). With `EXCEPT`, to each Agent of `regia_reach` (*A Role with `EXCEPT`*). A send to an Agent that has left is caught and traced by `regia.send` (chapter 33).
- A filled Placeholder recipient is a single `.send`.

### `EVERYONE`

`TELL EVERYONE f`, `TELL EVERYONE c` and `ASK EVERYONE TO g`, from an Agent or a Director, are one `.broadcast(achieve, regia_everyone(tell, f))`, `.broadcast(achieve, regia_everyone(signal, c))` or `.broadcast(achieve, regia_everyone(achieve, g))`.

- `regia/agent.asl` unwraps it with `regia.deliver(Ilf, Content, Sender)`, a `regia-jason` internal action that puts the inner message in the Agent's mailbox as if `Sender` had sent it directly. `FROM` still sees the real Sender.
- `regia/director.asl` ignores it, so `EVERYONE` reaches every Agent and no Director (chapter 07).
- `.broadcast` never sends to the sender itself, which is chapter 07's "except the sender".
- Nothing has to know every Agent in the game.

## Custom Actions in a Director

**Every Director sends its own Actions** through the game link, the Root included. `DO play_music.` is `regia.act("play_music", play_music)` as in an Agent. It waits, fails and is called off as anywhere else (chapter 37, *Custom Actions in a Director*). No Director performs an Action for another, and an ending Root plays no part in its children's `EXITED, BY PARENT` Actions. Decided in the ticket *A Director doing its own Actions* (`.scratch/director-game-link/issues/04-doing-its-own-actions.md`).

- **Rejected:** the Root's **Action relay**, where a Subplot Director sent `achieve regia_act(N, A, ReqId)` to the Root and got `tell regia_act_result(…)` back. The Root ran ASL and kept `regia_relay` records for other Stagings, and its relay plans had to stay unguarded while it ended.

## Infrastructure state

Rows filled in or added in chapter 28's table:

| Concept | Held by | Functor and arguments |
| --- | --- | --- |
| The current Phase | Director | `regia_phase(Phase)` |
| The Plot's initial Phase | Director (initial belief of its file) | `regia_initial_phase(Phase)` |
| The Plot's Roles, in declaration order | Director (initial belief of its file) | `regia_roles([Role, …])` |
| A standing Giving | Director | `regia_standing(Seq, Playbook, Role, Except, Until, Rank, Bindings)` |
| Who a Role with `EXCEPT` reaches here | Director (a rule in `regia/director.asl`) | `regia_reach(Role, Except, Agent)` |
| The next standing Giving's number | Director | `regia_standing_seq(N)` |
| What its own Plot hears from the game | Director (initial beliefs of its file) | `regia_hears(Plot, Name, Arity)` |
| A game Fact | Agent or Director | the Fact itself, `[source(percept)]` |

## `regia-jason` additions

- `regia.DirectorAgent`, the Directors' class (above), and a ranking helper shared with the Agents' class.
- The `regia_cue` and `regia_fact` message types.
- `regia.DirectorAgent`'s message intake for the game link: `regia_cue`, `regia_fact`, `regia_state_result` and `regia_action_result`, sharing its code with `regia.RegiaAgent`'s `myHandleMsg`.
- Detaching from the link in `regia.DirectorAgent`'s stop hook.
- Internal actions: `regia.attach`, `regia.stop_hearing`, `regia.stop_phase`, `regia.end_body`, `regia.deliver`. `regia.perceive` and `regia.add_percepts` are gone, with the `regia_percept` message.


## Trace entries

**Warnings**

- `T3001` A Giving or Mapping to a `?who` who was never in this Staging (such as an Agent named by a game Cue's argument), dropped.

A Signal no plan takes writes chapter 38's `T3801` (*Signals*, above). A failed `EXITED` Plan writes chapter 20's `T2002`, and the transition carries on; a Giving or Mapping to an Agent who has left writes `T2001`.

## Regia 1.5

In 1.5 (ADR 0025), except *An Agent joining*, and replaying the standing-Giving record for a joiner. The record is kept: `REMOVE`, leaving a Phase, and giving back with `ASSIGN … TO <Role> ?who` still read it and its `Except` lists. Clearing Quota counts on `ENTER` (step 4) is later.

A game Fact is still marked `source(percept)`, but nothing in 1.5 reads the mark: `LEARNED, FROM GAME` is later.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- The Staging's identity (its Director's name), Director names, a Director's record of its children, starting a child Director with its cast, and the rest of `END PLOT`: chapter 31 (`31-jason-stagings.md`).
- The game reporting joins and leaves, keeping `regia_cast` and the cast copies up to date, catching sends to Agents that have left, and the Quota-clearing hook: chapter 33.
- How `regia-jason` hooks into VEsNA-Pro's message handling, Custom Actions reaching the game, and Action results: chapter 37.
- The Root Director's `.jcm` entry (its `address` and `port`, and `ag-class: regia.DirectorAgent`): chapter 36.
- The format of Trace entries: chapters 34 and 35.
