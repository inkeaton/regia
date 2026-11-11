# Givings in Jason

How the Jason Target gives Playbooks to Agents and takes them away at runtime: which Plans an Agent holds, how a Giving is recorded, the messages between Director and Agent, how the record is read, and what stops when a Playbook is taken away. Decided in the ticket *Giving and taking Playbooks at runtime* (`.scratch/regia-2/issues/35-giving-playbooks-at-runtime.md`). It builds on chapter 28's layout and the research *Dynamic plan loading in Jason*, and answers the last `#discuss` of primer ch.8. It implements chapters 10 (local items), 15 (Givings and bindings), 16 (Role setup), 19 (standing Givings) and 20 (`?who` Givings). Rank values come from *Precedence encoding in ASL*.

## Plans are compiled in, Givings switch them on

- An Agent's files hold **every Playbook it can be given** in its lifetime: its Role file includes them (chapter 28). Giving a Playbook never adds plans, and taking it away never removes them. The Jason Target never uses `.add_plan`, `.remove_plan`, `tellHow` or a runtime `.include`.
- Why: the research found that adding plans at runtime merges plans shared by two Playbooks (plan equality ignores labels), appends at the end of the library and can race with the Director's next message (`tellHow`), lets plan terms pick up values from the Director's variables, and that `.remove_plan` reports success when nothing matched. Compiled-in plans behave the same on every run and can be read from the Build's files.
- Cost: the Plans of a Playbook that isn't given are still candidates for their Triggers, and their percepts still create events. The guard below rejects them cheaply.

### Which Playbooks a Role file includes

A Role file includes every Playbook a Root Plot Role can be given, following Subplot Mappings down the Plot tree (chapter 28). A Giving to `?who` (`ASSIGN Brawling TO ?who`, chapter 20) in Plot X could reach any Agent in X's Staging, so the Playbook counts as reachable for **every Root Plot Role that maps to any Role of X**. Narrowing this (for example to the Role a `JOINED Guest` bound `?who` from) is not in 2.0.

Each Role file lists the Playbooks it includes as initial beliefs, `regia_playbook(nobleSocializing).`, so the Infrastructure can check a Giving against them. Playbook files stay Plans only.

## The guard

Every plan generated from Playbook P starts its context with a test that P is given:

```
+!greet(G) : regia_given(nobleSocializing, _, _, _, _) & <designer's Context> <- …
```

- It covers **every** plan of P: the designer's Plans, the plans of P's Local Goals, and the generated plans for P's Goals (`-!g`, `DROPPED`, the `regia_if__N` and `regia_either__N` helpers). Nothing of a Playbook that isn't given can run.
- It comes first, so the designer's Context isn't evaluated for a Playbook that isn't given.
- Selection (chapter 13) still happens in `selectOption`. It reads the same beliefs for the rank, so the guard and the rank never disagree about what is given.

## The Giving record

Each Giving an Agent holds is one belief:

```
regia_given(Playbook, Director, Target, Rank, Bindings)
```

| Argument | Holds |
| --- | --- |
| `Playbook` | the Playbook's Jason name (`nobleSocializing`) |
| `Director` | the Jason agent name of the giving Director, taken from the message's `[source]`, never from its arguments. It is also the giving Staging's identity: each Staging is its own Director agent (chapter 31) |
| `Target` | `role(guest)` for a Giving to a Role: whole, counted, or from a Role setup. `agent(Name)` for a Giving to `?who` |
| `Rank` | the rank key of this Giving (chapter 13); its encoding is decided by *Precedence encoding in ASL* |
| `Bindings` | one entry per Playbook Role: `bind(host, live(host))` for a whole-Role Mapping, resolved live in that Director's Staging; `bind(rival, fixed([a1, a2]))` for a counted pick or `MAPPING ?who` |

- **There is no Giving id.** A Giving is identified by Playbook, Director and Target. Two identical Givings (the same `ASSIGN` running again with the same bindings) are the same belief, and Givings that differ only in bindings or rank add up as spec 15 says. Taking away matches on Playbook, Director and Target, so it removes all of them at once, which is what `UNASSIGN` means anyway (chapter 15).
- **The Director's address is the Staging's identity** (chapter 31), so a `SIGNAL` always has someone to send to.
- The record holds no Agent lists for whole-Role bindings. Who plays a Role is read from the Agent's copy of the cast (below).

### The cast copy

A whole-Role binding is live: `TELL host f` reaches whoever plays `Host` in that Staging **now** (chapter 15). Every Agent holding a Giving from a Staging therefore keeps a **copy of that Staging's cast**, as `regia_cast(Director, Role, Agent)`, the same functor the Director uses for its own record (chapter 28).

- The Director sends its cast to an Agent before the first Giving it sends that Agent. Jason keeps one sender's messages in order, so the copy is there before the Giving arrives.
- Keeping the copies up to date when Agents join and leave belongs to *Quota counts and cast changes in ASL*.
- Rejected alternatives: asking the Director at every send or arrival (slow, and it blocks the Plan), and relaying Messages through the Director (the Sender becomes the Director, which breaks `FROM` and the per-sender ordering promised in chapter 07).

## Messages between Director and Agent

The Director gives and takes away with `achieve` messages. The Agent handles them with fixed `[atomic]` plans in `regia/agent.asl`, so no other event is handled halfway through.

```
// Director side (ASSIGN NobleSocializing TO Guest, MAPPING Host TO host), per Agent playing Guest
.send(alice, achieve, regia_give(nobleSocializing, role(guest), Rank, [bind(host, live(host))]))

// Agent side, in regia/agent.asl
@regia_give[atomic]
+!regia_give(P, T, R, B)[source(D)] : regia_playbook(P)
   <- +regia_given(P, D, T, R, B).
+!regia_give(P, _, _, _)[source(D)]
   <- // trace warning: P isn't in this Agent's files (a Transpiler bug); the Giving is ignored

@regia_take[atomic]
+!regia_take(P, T)[source(D)]
   <- // remove every regia_given(P, D, T', _, _) with T' matching T (T = all matches any Target)
      // if no regia_given(P, …) remains: stop P (below)
```

- `regia_give` carries the record without the Director, which is also the Staging; the Agent adds `D` from `[source]`. A forged or stale argument can't make a Giving look like it came from another Director.
- A `regia_give` for a Playbook the Agent's files don't hold is a Transpiler bug, not a designer error. The Agent writes a Trace warning and ignores it.
- Whether a newly given Playbook starts any Quota counts, and how ranks are combined when it is given twice, belong to *Quota counts and cast changes in ASL* and *Precedence encoding in ASL*.

### What each Director Statement sends

| Statement | Sent to | Message |
| --- | --- | --- |
| `ASSIGN P TO Guest` (whole Role, standing) | each Agent playing `Guest` in the Staging; later each joiner (chapter 19) | `regia_give(p, role(guest), …)` |
| `ASSIGN P TO 2 OF Guest` | each picked Agent | `regia_give(p, role(guest), …)` |
| A Role setup's `ASSIGN P` (chapter 16) | the Agent starting or joining the Role | `regia_give(p, role(guest), …)` |
| `ASSIGN P TO ?who` | that Agent | `regia_give(p, agent(who), …)` |
| `UNASSIGN P FROM Guest` | each Agent in the Staging's cast | `regia_take(p, role(guest))` |
| `UNASSIGN P FROM ?who` | that Agent | `regia_take(p, all)` |
| A Staging ending (chapter 17) | each Agent in its cast | `regia_end_staging`, which takes away every Giving from that Director and its cast copy (chapter 31) |

The Director doesn't track which Agents hold which Givings. A take-away goes to the whole cast, and each Agent removes whatever matches in its own record. Sending to an Agent that has left is caught and traced (chapter 19).

## Reading the record

| Language | What the Infrastructure does |
| --- | --- |
| A Plan of P runs | the guard: some `regia_given(p, …)` exists |
| `SIGNAL e` in P | sends `e` to every distinct `Director` in `regia_given(p, Director, …)` (chapter 07) |
| `TELL host f` in P | the union, over every `regia_given(p, …)`, of each `host` binding: `live(R)` reads `regia_cast(Director, R, A)`, `fixed(L)` reads `L`; minus the Agent itself (chapter 15) |
| `WHEN … FROM host` in P | the Sender is in that same union, checked when the Message arrives |
| A Quota Trigger over `host` in P | counts against the same union (chapter 18) |
| Precedence | `selectOption` reads `Rank` from the `regia_given` beliefs of each candidate's Playbook (chapter 13) |

## Taking a Playbook away

Removing a Giving removes its record. If the Agent **still holds another Giving of P**, nothing else happens: P's Plans keep running, and the bindings of the remaining Givings are all that `TELL host` and `FROM host` see.

When the **last** Giving of P goes, inside the same atomic `regia_take` (or `regia_end_staging`, chapter 31) plan:

1. **P's running Plans stop.** On each intention, the outermost plan of P (found by its `playbook(P)` annotation, chapter 13) and everything above it on the stack stop, as `DROP` would stop them (chapter 08).
   - If that plan was pursuing a Goal, the Goal is dropped: it fires `DROPPED`, and the sub-Goals stopped above it fire theirs first, innermost first. The `DROPPED` Plans run only if their Playbook is still given (the guard), so P's own `WHEN g DROPPED` Plans don't run.
   - A Plan of another, still-given Playbook that was waiting on that Goal with `PURSUE` **fails**, as with any dropped Goal (chapter 08). Chapter 12's "what gets reported is whatever stopped it" is that `DROPPED`.
   - A stopped Plan whose Trigger isn't a Goal (`WHEN hit_by(?x)`) just stops, with a Trace entry saying its Playbook was taken away.
   - Goals started `WITHOUT WAITING` from a Plan of P run on their own intention. If their recipe is in P, that intention has a plan of P and stops too. This is how P's **Local Goals are dropped** (chapter 10): their recipes are only in P.
2. **P's local Facts stay** (chapter 10). The guard hides the Plans that read them; they are there again if P is given back.
3. **P's Quota counts are cleared** (chapter 18). How is decided by *Quota counts and cast changes in ASL*.

Step 1 is a `regia-jason` internal action, `regia.stop_playbook(P)`, since walking intentions by their plans' annotations is clumsy in ASL. It generates the `DROPPED` events and Trace entries itself.

Messages already queued for P's Triggers after it is taken away find no applicable plan (the guard). A queued Goal for P then fails like any Goal with no applicable recipe (chapter 11).

## Infrastructure state

Rows filled in or added in chapter 28's table:

| Concept | Held by | Functor and arguments |
| --- | --- | --- |
| A Giving of a Playbook | Agent | `regia_given(Playbook, Director, Target, Rank, Bindings)` |
| A Playbook in the Agent's files | Agent (initial beliefs of its Role file) | `regia_playbook(Playbook)` |
| A Role's members | Director, and a copy in each Agent holding a Giving from that Staging | `regia_cast(Director, Role, Agent)` |

## Not decided here

- The Staging's identity (its Director's name), and taking a whole Staging's Givings away when it ends: chapter 31.
- The `Rank` encoding, and how two Givings' ranks combine: *Precedence encoding in ASL*.
- The Director's standing-Giving record (`regia_standing`), replaying it for joiners, and the cast copy's message (`regia_cast_copy`): chapter 30.
- Keeping cast copies and counted picks up to date on join and leave, and starting and clearing Quota counts: *Quota counts and cast changes in ASL*.
- The Trace entries' format: *Trace and logging*.
- How Role files combine for an Agent kind that plays several Roles, so that `regia_playbook` beliefs and Playbook includes aren't duplicated: *.jcm generation*.
