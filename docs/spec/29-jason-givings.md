# Givings in Jason

How the Jason Target gives Playbooks to Agents and takes them away at runtime: which Plans an Agent holds, how a Giving is recorded, the messages between Director and Agent, how the record is read, and what stops when a Playbook is taken away. Decided in the ticket *Giving and taking Playbooks at runtime* (`.scratch/regia-2/issues/35-giving-playbooks-at-runtime.md`). It builds on chapter 28's layout and the research *Dynamic plan loading in Jason*, and answers the last `#discuss` of primer ch.8. It implements chapters 10 (local items), 15 (Givings and bindings), 16 (Role setup), 19 (standing Givings) and 20 (`?who` Givings). Rank values come from chapter 32. The message forms in *Reading the record* were decided in the ticket *Messages and told Facts in ASL* (`.scratch/showcase-1-5/issues/12-messages-in-asl.md`), and the Plans' side of them is in chapter 39. The `Target` and `Until` arguments, `EXCEPT` in a binding, Givings set aside and given back, and the take-away messages were decided in the ticket *Exclusions, one Agent and a Phase in the Giving record* (`.scratch/showcase-1-5/issues/15-giving-record.md`). `ASSIGNED`, the closing of a Playbook taken away and `regia_holds` were decided in the ticket *A Playbook's opening and closing in ASL* (`.scratch/showcase-1-5/issues/16-opening-and-closing.md`), following chapter 15 and ADR 0021.

## Plans are compiled in, Givings switch them on

- An Agent's files hold **every Playbook it can be given** in its lifetime: its Role file includes them (chapter 28). Giving a Playbook never adds plans, and taking it away never removes them. The Jason Target never uses `.add_plan`, `.remove_plan`, `tellHow` or a runtime `.include`.
- Why: the research found that adding plans at runtime merges plans shared by two Playbooks (plan equality ignores labels), appends at the end of the library and can race with the Director's next message (`tellHow`), lets plan terms pick up values from the Director's variables, and that `.remove_plan` reports success when nothing matched. Compiled-in plans behave the same on every run and can be read from the Build's files.
- Cost: the Plans of a Playbook that isn't given are still candidates for their Triggers, and their percepts still create events. The guard below rejects them cheaply.

### Which Playbooks a Role file includes

A Role file includes every Playbook a Root Plot Role can be given, following Subplot Mappings down the Plot tree (chapter 28). A Giving to `?who` (`ASSIGN Brawling TO ?who`, chapter 20) in Plot X could reach any Agent in X's Staging, so the Playbook counts as reachable for **every Root Plot Role that maps to any Role of X**. Narrowing this (for example to the Role a `JOINED Guest` bound `?who` from) is not in 2.0.

**`MAPPING ?who AS r` reaches the same way.** In `START SUBPLOT` run by Plot X, the Playbooks that Subplot Role `r` can be given (its Role setups, its Givings, and its own Subplots' Mappings, down the tree) count as reachable for every Root Plot Role that maps to any Role of X. In the showcase, `RoyalBanquet` maps `?offender AS Defender` and the Root is X itself, so `Host`, `Guest`, `Servant` and `Guard` all include `Duelling`. `?offender` comes from a Cue's argument, so narrowing by where the Placeholder was filled wouldn't help there. Through chapter 14's emission rules, `king` and the `servant` kind therefore get a `temper` for `bravery`, `sympathy` and `aggressiveness`, which do nothing for Agents whose other Plans carry no Labels.

Decided in the ticket *Roles an Agent reads* (`.scratch/showcase-1-5/issues/14-roles-an-agent-reads.md`), with *Who plays a Playbook Role* below.

Each Role file lists the Playbooks it includes as initial beliefs, `regia_playbook(nobleSocializing).`, so the Infrastructure can check a Giving against them. Playbook files stay Plans only.

## The guard

Every plan generated from Playbook P starts its context with a test that P is given, the rule `regia_is_given` of `regia/agent.asl`:

```
regia_is_given(P) :- regia_given(P, _, _, _, _, _).
regia_given_or_closing(P, C) :- regia_is_given(P) | regia_closing(C, P, _, _, _, _, _).

+!greet(G) : regia_is_given(nobleSocializing) & <designer's Context> <- …
```

- It covers **every** plan of P: the designer's Plans, its ending Plans and the plans of P's Local Goals. Nothing a designer wrote in a Playbook that isn't given can run.
- **Two exceptions, both for closing** (*Taking a Playbook away*, below). P's `DROPPED` and `ENDED` plans are guarded by `regia_given_or_closing(p, Closing)`, where `Closing` is the ending goal's own argument (chapter 40): they also run for the drops of a closing of P, and for nothing else. P's `REMOVED` plans have no Givings guard, since only a closing posts `regia_removed`.
- **The generated `-!g` plans are not guarded** (chapter 40). They live in `goals.asl`, one per Goal, not in a Playbook, and a `-!g` whose context is false would drop the whole intention, waiting Plans of still-given Playbooks included.
- It comes first, so the designer's Context isn't evaluated for a Playbook that isn't given.
- Selection (chapter 13) still happens in `selectOption`. It reads the same beliefs for the rank, so the guard and the rank never disagree about what is given.

## The Giving record

Each Giving an Agent holds is one belief:

```
regia_given(Playbook, Director, Target, Rank, Bindings, Until)
```

| Argument | Holds |
| --- | --- |
| `Playbook` | the Playbook's Jason name (`nobleSocializing`) |
| `Director` | the Jason agent name of the giving Director, taken from the message's `[source]`, never from its arguments. It is also the giving Staging's identity: each Staging is its own Director agent (chapter 31) |
| `Target` | `role(guest)` for a Giving to a Role: whole, counted, with or without `EXCEPT`, or from the Role's setup. `role(cast)` for a Giving to `CAST`: whole, counted, with or without `EXCEPT`, or from the `CAST` setup. `agent(Name)` for a Giving to `?who`. The `EXCEPT` of a target isn't recorded here: an Agent left out never receives the Giving, and the Director's standing record keeps the list (chapter 30) |
| `Rank` | the rank key of this Giving (chapter 13); a path of levels from the Root Plot down, chapter 32 |
| `Bindings` | one entry per Playbook Role: `bind(host, live(host, Except))` for a whole-Role Mapping, resolved live in that Director's Staging (*`EXCEPT` in a binding*, below); `bind(rival, fixed([a1, a2]))` for a counted pick or `MAPPING ?who` |
| `Until` | `staging` for a Giving that lasts until it is taken away or the Staging ends; `phase(feast)` for a Giving made **for a Phase**: from the Phase's setup, or carrying `UNTIL EXITED` (chapters 15, 16) |

- **There is no Giving id.** A Giving is identified by Playbook, Director, Target and `Until`. Two identical Givings (the same `ASSIGN` running again with the same bindings) are the same belief, and Givings that differ only in bindings or rank add up as spec 15 says. Taking away matches on Playbook, Director and Target, so it removes all of them at once, which is what `REMOVE` means anyway (chapter 15).
- **`Until` is an argument, not an annotation.** Jason merges the annotations of identical literals, so a Plot-level Giving and an identical `UNTIL EXITED` one would become one belief, and leaving the Phase would take both. As separate beliefs they are two Givings, and leaving the Phase takes only its own.
- **"A target that includes `Guest`"** (chapter 15) is `role(guest)`, or `role(cast)` when the Agent plays `Guest` in that Director's cast copy at the time of the take. A Giving to `agent(Name)` never includes a Role: it was never made to the Guests.
- **The Director's address is the Staging's identity** (chapter 31), so a `SIGNAL` always has someone to send to.
- The record holds no Agent lists for whole-Role bindings. Who plays a Role is read from the Agent's copy of the cast (below).
- **A Giving to one Agent next to a Role's.** `ASSIGN Keeping_watch TO ?winner` (`royal_banquet.regia:127`) for a knight who already holds `Keeping_watch` from the Guard setup (`:32`–`:33`) is a second belief, `regia_given(keeping_watch, banquet, agent(percival), …)`, next to the one with target `role(guard)`. `REMOVE Keeping_watch FROM Guard` leaves it, and `REMOVE Keeping_watch FROM ?winner` takes only it. A `SIGNAL` still reaches the Director once (*What reads it*), and no `ASSIGNED` fires: the Playbook was already held.

### Givings set aside

`REMOVE P FROM Guest ?who` takes `?who` out of Givings that go on for everyone else, and `ASSIGN P TO Guest ?who` gives it back with their bindings (chapter 15). The Director doesn't track counted Givings or setup Givings, so the Agent keeps what it lost:

```
regia_aside(Playbook, Director, Target, Rank, Bindings, Until)
```

- `regia_set_aside` moves every matching `regia_given` to `regia_aside`, unchanged. `regia_restore` moves them back.
- The guard and every reader ignore `regia_aside`. A Playbook whose Givings are all set aside isn't held: its Plans stop, as on any take-away, and `REMOVED` fires (chapter 15). Restoring one fires `ASSIGNED`.
- A full take clears what was set aside too: `REMOVE … FROM Guest` and `FROM CAST`, the Phase being left, the Staging ending. After `FROM Guest` there is nothing left to give back (chapter 15).
- A leaver is dropped from the `fixed` lists of `regia_aside` as from those of `regia_given` (chapter 33).

### The cast copy

A whole-Role binding is live: `TELL host f` reaches whoever plays `Host` in that Staging **now** (chapter 15). Every Agent holding a Giving from a Staging therefore keeps a **copy of that Staging's cast**, as `regia_cast(Director, Role, Agent)`, the same functor the Director uses for its own record (chapter 28).

- The Director sends its cast to an Agent before the first Giving it sends that Agent. Jason keeps one sender's messages in order, so the copy is there before the Giving arrives.
- Keeping the copies up to date when Agents join and leave: `regia_cast_joined` and `regia_cast_left`, chapter 33.
- Rejected alternatives: asking the Director at every send or arrival (slow, and it blocks the Plan), and relaying Messages through the Director (the Sender becomes the Director, which breaks `FROM` and the per-sender ordering promised in chapter 07).

## Messages between Director and Agent

The Director gives and takes away with `achieve` messages. The Agent handles them with fixed `[atomic]` plans in `regia/agent.asl`, so no other event is handled halfway through.

```
// Director side (ASSIGN NobleSocializing TO Guest, MAPPING Host AS host), per Agent playing Guest
.send(alice, achieve, regia_give(nobleSocializing, role(guest), Rank, [bind(host, live(host, []))], staging))

// Agent side, in regia/agent.asl
@regia_give[atomic]
+!regia_give(P, T, R, B, U)[source(D)] : regia_playbook(P)
   <- +regia_given(P, D, T, R, B, U)
      // if P was neither held nor closing just before: !!regia_assigned(P) (Opening, below)
+!regia_give(P, _, _, _, _)[source(D)]
   <- // trace warning: P isn't in this Agent's files (a Transpiler bug); the Giving is ignored

@regia_take[atomic]
+!regia_take(P, What)[source(D)]
   <- // remove every regia_given(P, D, T, …) and regia_aside(P, D, T, …) that What matches:
      //   role(R)  T includes R (role(R), or role(cast) while regia_cast(D, R, Me))
      //   agent    T = agent(Me); only regia_given. Nothing matched: T1505
      //   all      any T
      // if no regia_given(P, …) remains: stop P (below)

@regia_set_aside[atomic]
+!regia_set_aside(P, R)[source(D)]
   <- // move every regia_given(P, D, T, …) whose T includes R to regia_aside. Nothing moved: T1505
      // if no regia_given(P, …) remains: stop P (below)

@regia_restore[atomic]
+!regia_restore(P, R, Resent)[source(D)]
   <- // move every regia_aside(P, D, T, …) whose T includes R back to regia_given
      // nothing moved and Resent = false: T1506
      // if P was neither held nor closing just before: !!regia_assigned(P) (Opening, below)

@regia_take_phase[atomic]
+!regia_take_phase(Ph)[source(D)]
   <- // remove every regia_given(_, D, _, _, _, phase(Ph)) and regia_aside(…, phase(Ph))
      // for each Playbook left with no regia_given: stop it (below)
```

- `regia_give` carries the record without the Director, which is also the Staging; the Agent adds `D` from `[source]`. A forged or stale argument can't make a Giving look like it came from another Director.
- A `regia_give` for a Playbook the Agent's files don't hold is a Transpiler bug, not a designer error. The Agent writes a Trace warning and ignores it.
- A newly given Playbook starts counting its Quota Triggers just by being given: counting is active while some `regia_given` exists (chapter 33). A Playbook given twice keeps both Givings; `selectOption` takes the best Rank per item (chapter 32).

### What each Director Statement sends

| Statement | Sent to | Message |
| --- | --- | --- |
| `ASSIGN P TO Guest` (whole Role, standing) | each Agent playing `Guest` in the Staging; later each joiner (chapter 19) | `regia_give(p, role(guest), …)` |
| `ASSIGN P TO Guest EXCEPT Guard, ?who` | each Agent playing `Guest`, not `Guard`, and not `?who` (chapter 30) | `regia_give(p, role(guest), …)` |
| `ASSIGN P TO CAST`, and the `CAST` setup's `ASSIGN P` | each cast Agent, once | `regia_give(p, role(cast), …)` |
| `ASSIGN P TO 2 OF Guest` | each picked Agent | `regia_give(p, role(guest), …)` |
| A Role setup's `ASSIGN P` (chapter 16) | the Agent starting or joining the Role | `regia_give(p, role(guest), …)` |
| `ASSIGN P TO ?who` | that Agent | `regia_give(p, agent(who), …)` |
| A kind's or individual Agent's `ASSIGN P` (chapter 21) | that Agent, from the Root Director | `regia_give(p, agent(a), …, staging)` (chapter 30) |
| `REMOVE P FROM Guest` | each Agent in the Staging's cast | `regia_take(p, role(guest))`: a Guest loses its `role(guest)` Givings and its `role(cast)` ones, so the `CAST` Givings are narrowed |
| `REMOVE P FROM CAST` | each Agent in the Staging's cast | `regia_take(p, all)` |
| `REMOVE P FROM ?who` | that Agent | `regia_take(p, agent)`: only the Givings made to it. A Guard setup's Giving stays (chapter 15) |
| `REMOVE P FROM Guest ?who` | that Agent, if it plays `Guest`; else `T1505` on the Director | `regia_set_aside(p, guest)` |
| `REMOVE P FROM CAST ?who` | that Agent | `regia_take(p, all)` |
| `ASSIGN P TO Guest ?who` | that Agent, if it plays `Guest`; else `T1506` on the Director | any resent `regia_give`s (chapter 30), then `regia_restore(p, guest, Resent)` |
| Leaving a Phase (chapter 30) | each Agent in the Staging's cast | `regia_take_phase(feast)` |
| A Staging ending (chapter 17) | each Agent in its cast | `regia_end_staging`, which takes away every Giving from that Director, set aside or not, and its cast copy (chapter 31) |

- **The `Until` argument** of `regia_give` is `phase(feast)` for a Giving from `feast`'s setup or with `UNTIL EXITED` in a `DURING feast` Plan, and `staging` otherwise.
- **Only the Agent knows what it holds**, so it writes the `T1505` and `T1506` that depend on that: a `FROM ?who` with no Giving to it, a `FROM Guest ?who` with nothing to set aside, and an `ASSIGN … TO Guest ?who` with nothing to give back. `Resent` is `true` when the Director resent a standing Giving whose written `EXCEPT` left `?who` out (chapter 30). Per-sender ordering means that Giving has already arrived, and the Agent doesn't warn then.

The Director doesn't track which Agents hold which Givings. A take-away goes to the whole cast, and each Agent removes whatever matches in its own record. Sending to an Agent that has left is caught and traced (chapter 19): every send goes through `regia.send`, not `.send` (chapter 33).

## Reading the record

Every reader goes through **`regia_holds`**, a rule in `regia/agent.asl` that holds for each Giving in effect: the Agent's `regia_given` beliefs, and the snapshot of a closing (*The closing*, below):

```
regia_holds(P, D, T, R, B, U) :- regia_given(P, D, T, R, B, U).
regia_holds(P, D, T, R, B, U) :- regia_closing(_, P, D, T, R, B, U).
```

Outside a closing the two are the same. A closing Plan therefore speaks through the Givings as they were just before the taking (chapter 15). If P is given back while closing, P's Plans read both, old and new, until the closing ends. Only the guard's rules read `regia_given` directly.

### Who plays a Playbook Role

A Playbook Role is read through **one rule** in `regia/agent.asl`. It holds when Agent `A` is in the union, over every Giving of `P`, of Role `R`'s bindings:

```
regia_plays(P, R, A) :-
    regia_holds(P, D, _, _, B, _) & .member(bind(R, X), B) &
    ( X = live(cast, Ex) & regia_cast(D, _, A) & not regia_excepted(D, Ex, A)
    | X = live(PR, Ex) & PR \== cast & regia_cast(D, PR, A) & not regia_excepted(D, Ex, A)
    | X = fixed(L) & .member(A, L) ).

regia_excepted(_, Ex, A) :- .member(agent(A), Ex).
regia_excepted(D, Ex, A) :- .member(role(XR), Ex) & regia_cast(D, XR, A).
```

- It leaves the Agent itself in. A recipient leaves it out where the recipients are collected; `PLAYS` doesn't (chapter 15).
- It may give one Agent more than once (two Givings, or `CAST` and a knight's two Roles). Every reader collects with `.setof`, or only tests a bound `A`, so that never counts twice.
- Every reader of a Playbook Role goes through it: generated code never reads `bind` itself. Extending a binding (for example with `EXCEPT`, below) changes this rule only.

### `EXCEPT` in a binding

A whole-Role binding always carries a list: `live(Role, Except)`, which is `[]` when nothing is left out. `MAPPING Guest EXCEPT Guard, ?who AS spectator` is `bind(spectator, live(guest, [role(guard), agent(alice)]))`.

- A `role(guard)` item is read **live**, from the same cast copy as the Role it narrows. An `agent(alice)` item is the Agent the Placeholder held **when the Statement ran** (chapter 15), so the Director writes the name in.
- A Placeholder holding no Agent is left out of the list by the Director, which writes `T1504`. The list's other items still apply.
- A counted Mapping with `EXCEPT` is drawn by the Director from what is left (chapter 30), and arrives as `fixed`.

### What reads it

| Language | What the Infrastructure does |
| --- | --- |
| A Plan of P runs | the guard: `regia_is_given(p)` |
| `SIGNAL e` in P | `?regia_directors(p, L)`, every distinct Director in `regia_holds(p, Director, …)`, then `regia.send(L, signal, e)` (chapters 07, 30 and 39) |
| `TELL host f` in P | `?regia_audience(p, host, L)`, the Role's union without the Agent itself, then `regia.send(L, tell, f)`. A Cue goes as `signal` (chapter 39) |
| `TELL 2 OF host f`, `ASK 50% OF host TO g` in P | the same pool, drawn by the Infrastructure plan `!regia_draw` each time the Statement runs (chapter 39) |
| `?x PLAYS host`, `ME PLAYS host` in P | `regia_plays(p, host, X)`, the Agent itself left in (chapter 39) |
| `WHEN …, FROM host` in P | `regia_from_role(p, host, S)` for the Sender, the trigger's `source(S)`, tested in the plan's context (chapter 39) |
| `WHEN …, FROM DIRECTOR` in P | `regia_from_director(p, S)`, which is `regia_holds(p, S, _, _, _, _)` (chapter 39) |
| A Quota Trigger over `host` in P | counts against `regia_plays(p, host, _)` (chapter 18) |
| Precedence | `selectOption` reads `Rank` from `regia_holds` for each candidate's Playbook and takes the best for the candidate's item (chapter 32) |

## Opening: `ASSIGNED`

`ASSIGNED` fires when the Agent goes from holding no Giving of P to holding one (chapter 15). `regia_give` and `regia_restore` test, before they add, whether some `regia_given(P, …)` exists:

- **P was held**: nothing fires. A second Giving, like `ASSIGN Keeping_watch TO ?winner` for a Guard, is only a second belief.
- **P was neither held nor closing**: after adding the belief, the atomic plan posts **`!!regia_assigned(P)`**, which runs on a new intention once the atomic plan ends. From `dining.regia:10`, `Dining` given at the start of `feast` runs `WHEN ASSIGNED` there, and `PURSUE have_dinner, WITHOUT WAITING` starts yet another intention.
- **P was closing** (below): nothing is posted. The closing runs `ASSIGNED` as its last step, after its `REMOVED` Plans. A re-entered Phase therefore fires `REMOVED`, then `ASSIGNED` (chapter 15). P's other Plans run as soon as the new Giving is in, next to the closing Plans: only `ASSIGNED` waits.

P's `WHEN ASSIGNED:` plans are plans for `+!regia_assigned(p)`, with the Givings guard and chapter 32's annotation with the Item `assigned`. `agent.asl` holds a `regia_noop` plan for `regia_assigned(_)` and for `regia_removed(_)`, so a Playbook with neither Plan needs nothing, and a `-!` catcher for each, which writes the failing Plan's `failure` entry and succeeds, as for the ending goals (chapter 40).

## Taking a Playbook away

Removing a Giving removes its record. If the Agent **still holds another Giving of P**, nothing else happens: P's Plans keep running, and the bindings of the remaining Givings are all that `TELL host` and `FROM host` see.

When the **last** Giving of P goes, P **closes** (chapter 15, ADR 0021). A Playbook on an Agent is given, closing, or not given.

### The take step

Each of the atomic plans that can take a last Giving, `regia_take`, `regia_set_aside`, `regia_take_phase` and `regia_end_staging` (chapter 31), is one **take step**. Let `Ps` be every Playbook that lost its last Giving in it: leaving `feast` can take `Dining` and the Phase's other Givings together. Still inside the atomic plan:

1. **Snapshot the Givings.** Each removed `regia_given(P, D, T, R, B, U)` of a P in `Ps` becomes `regia_closing(C, P, D, T, R, B, U)`. Removed `regia_aside` records are not kept: they weren't in effect. A Playbook that keeps another Giving is not in `Ps`, and its removed records are just deleted.
2. **Stop P's running Plans**: `regia.stop_playbook(C, Ps)`, below.
3. **Clear P's Quota counts** (chapter 18): every `regia_quota(p, …)` is removed (chapter 33).
4. **Start the closing**: `!!regia_close(C, Ps, Steps)`, below.

`C`, the **closing's id**, is the `seq` of the step's first `TAKE` entry (chapter 34), as a Pursuit's id is the `seq` of its `PURSUED` entry (chapter 40).

### Stopping P's Plans: `regia.stop_playbook`

It shares `regia.drop`'s walker (chapter 40), starting from P's frames instead of a `+!g` frame:

1. **Find** every intention holding a frame of a Playbook in `Ps` (found by its `regia_rank(P, _, _)` annotation, chapter 32), running, suspended or waiting. It **skips** the steps of a closing whose own `Ps` holds P: those are P's closing Plans, and they run to their end, even when P was given back and is now taken again.
2. **Take each intention whole**, as a `DROP` does: every goal frame on it is dropped as a level, P's and the still-given Playbooks' alike, and what was waiting on a dropped Goal is dropped too (chapter 08, ADR 0018). It never fails. In a closing intention of another take, only the frames above its `regia_close` frame are taken, and that closing goes on with its next step (chapter 40).
3. **Call off** a `DO` the intention is waiting on (chapter 37).
4. **Write the Trace**: each Pursuit stopped writes `GOAL … DROPPED` with `because:` the step's first `TAKE` entry, where a `DROP` writes its own `at`. A `WHEN` Plan at the bottom writes chapter 40's `plan … stopped`, at `info`, with the same `because`.
5. **Remove** the intentions.
6. **Hand back the endings**: for each removed intention, `regia_dropped(G, Sender, Id, C)` then `regia_ended(G, Sender, Id, C)` per goal frame, innermost first. Intentions come in creation order (Jason's intention id). These go into the closing's `Steps`, not onto intentions of their own as a `DROP`'s do.

Goals started `WITHOUT WAITING` from a Plan of P run on their own intention. If their recipe is in P, that intention has a plan of P and stops too. This is how P's **Local Goals are dropped** (chapter 10): their recipes are only in P.

### The closing

`regia_close(C, Ps, Steps)` is an Infrastructure plan of `agent.asl`. It runs, in order, on one intention:

1. the endings handed back by `regia.stop_playbook`;
2. `regia_removed(P)` for each P in `Ps`, in name order;
3. removing every `regia_closing(C, …)`;
4. `regia_assigned(P)` for each P in `Ps` that is held again (*Opening*, above), in name order.

**The closing is that intention.** P is closing from the take step until it ends. Running one step after the other is what keeps chapter 15's order, each drop's `DROPPED` and `ENDED`, then `REMOVED`. A `WAIT` in one closing Plan delays the steps after it.

- **The guard.** The endings of step 1 carry `C`, so P's `DROPPED` and `ENDED` plans pass their guard through `regia_closing(C, p, …)` (*The guard*, above). Any other ending of P's Goals while P is closing carries `none` and finds no plan of P: a still-given Playbook reaching `have_dinner` on its own recipe runs neither `Dining`'s `REACHED` nor its `ENDED`. The still-given Playbooks' ending plans run through their own `regia_given`.
- **What a closing Plan can start.** It is an ordinary Plan. A `PURSUE` of a Goal whose only recipe is in P finds no plan (`T1104`, chapter 40), and its endings carry `none`, so P's `FAILED` Plan doesn't run (chapter 15).
- **What a closing Plan speaks through**: `regia_holds`, the snapshot included (*Reading the record*). From `dining.regia:48`, `WHEN have_dinner ENDED: SIGNAL finished_eating` runs in the closing of `Dining` that leaving `feast` started, and reaches `banquet`, whose `farewell` ignores it (`T3801`, chapter 30).
- **A Staging that has ended.** `regia_end_staging` removes that Staging's cast copy, and its Director is gone (chapter 31). A live binding through it reaches nobody, and a `fixed` one still reaches its Agents. A `SIGNAL` to its Director is caught by `regia.send` (chapter 33), which is not `T3303`'s warning: chapter 15 promises that such a Director hears nothing. The `SIGNAL`'s `message` entry lists that Director as `ENDED`, at `info` (chapter 34). From `royal_banquet.regia:107`, `DROP SUBPLOT HonorDuel(?)` closes `Duelling`, and `WHEN REMOVED` (`duelling.regia:56`) forgets `stamina`.
- **A failing step** is caught by its kind's `-!` catcher (chapter 40, *Opening* above), and the closing goes on with the next step.
- **P's local Facts stay** (chapter 10), unless a closing Plan forgets them. The guard hides the Plans that read them; they are there again if P is given back.

Messages already queued for P's Triggers after it is taken away find no applicable plan (the guard). A queued Goal for P then fails like any Goal with no applicable recipe (chapter 11).

## Infrastructure state

Rows filled in or added in chapter 28's table:

| Concept | Held by | Functor and arguments |
| --- | --- | --- |
| A Giving of a Playbook | Agent | `regia_given(Playbook, Director, Target, Rank, Bindings, Until)` |
| A Giving set aside by `REMOVE … FROM Role ?who` | Agent | `regia_aside(Playbook, Director, Target, Rank, Bindings, Until)` |
| A Giving as it was before a take, kept while the Playbook closes | Agent | `regia_closing(Closing, Playbook, Director, Target, Rank, Bindings, Until)` |
| A Giving in effect: given, or in a closing's snapshot | Agent (a rule in `regia/agent.asl`) | `regia_holds(Playbook, Director, Target, Rank, Bindings, Until)` |
| A Playbook in the Agent's files | Agent (initial beliefs of its Role file) | `regia_playbook(Playbook)` |
| A Role's members | Director, and a copy in each Agent holding a Giving from that Staging | `regia_cast(Director, Role, Agent)` |
| Who plays a Playbook Role | Agent (a rule in `regia/agent.asl`) | `regia_plays(Playbook, Role, Agent)` |
| An Agent left out by a binding's `EXCEPT` | Agent (a rule in `regia/agent.asl`) | `regia_excepted(Director, Except, Agent)` |


## Trace entries

**Warnings**

- `T2901` A `regia_give` for a Playbook the Agent's files don't hold (a Transpiler bug), ignored.

A Plan stopped because its Playbook was taken away is not a warning: it writes chapter 40's `plan … stopped` at `info`, `because:` the `TAKE` entry. `T2902`, which used to be that warning, is retired; its number is not reused.

Chapter 15's `T1505` and `T1506` are written by the Agent when its record holds nothing to take, set aside or give back (*What each Director Statement sends*), and `T1504` by the Director.

## Regia 1.5

In 1.5 (ADR 0025), except the Quota parts: a Playbook starting its Quota counts when given, the Quota row of *Reading the record*, and clearing counts when it is taken away. A standing Giving reaches no joiner, since 1.5 has none.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- The Staging's identity (its Director's name), and taking a whole Staging's Givings away when it ends: chapter 31.
- The Director's standing-Giving record (`regia_standing`), replaying it for joiners, and the cast copy's message (`regia_cast_copy`): chapter 30.
- Keeping cast copies and counted picks up to date on join and leave, and starting and clearing Quota counts: chapter 33.
- The Trace entries' format: chapters 34 and 35.
- How Role files combine for an Agent kind that plays several Roles, so that `regia_playbook` beliefs and Playbook includes aren't duplicated: a combination file (chapter 36).
