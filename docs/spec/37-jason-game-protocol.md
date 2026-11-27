# The game protocol in Jason

How a Jason Build and the game talk to each other: how a Custom Action reaches the game and how its result comes back, how `regia-jason` reads game messages inside VEsNA-Pro's agent, how a Director's Custom Actions travel on the game link, and what the game hears when the story ends. Decided in the ticket *Custom Actions through VEsNA* (`.scratch/regia-2/issues/43-custom-actions-through-vesna.md`). It builds on chapter 08's `DO`, chapter 11's Failures, chapter 28's External names, chapters 30–33's game messages and chapter 35's test mode. It was checked against VEsNA-Pro's `VesnaAgent`, `WsClient` and `vesna.walk` (`vesna-pro-main/src/agt/vesna/`). Calling off an Action and pausing the clock were added in the ticket *Time and Actions in the game* (`.scratch/regia-revision/issues/19-time-and-actions.md`), with ADR 0038.

## The envelope

Every message between a body and the game uses VEsNA's JSON envelope, `{"sender", "receiver", "type", "data"}`. Regia's message types:

| Type | Direction | `data` | Chapter |
| --- | --- | --- | --- |
| `regia_cue` | game → body | `{"name", "args"}` | 30 |
| `regia_fact` | game → body | `{"op": "add" \| "remove", "name", "args"}` | 30 |
| `regia_join` | game → game link → Root Director | `{"kind", "name", "port"}` | 33, 36 |
| `regia_leave` | game → game link → every attached Director | `{"name"}` | 33 |
| `regia_action` | body → game | `{"id", "name", "args"}` | here |
| `regia_action_result` | game → body | `{"id", "status", "reason"?}` | here |
| `regia_action_cancel` | body → game | `{"id"}` | here |
| `regia_state` | game link → game, for an attaching Director | `{"id", "facts": [name, …], "agents": [name, …]}` | 30, here |
| `regia_state_result` | game → game link → that Director | `{"id", "facts": [{"name", "args"}, …], "left": [name, …]}` | 30, here |
| `regia_pause`, `regia_resume` | game → game link (the clock) | `{}` | here |
| `regia_story_ended` | Root Director → game, through the game link | `{"outcome"}` | here |

Directors reach the game through one shared **game link** (chapter 28), and the game never learns about Stagings. On the link's connection, the link's name is **`regia_game_link`**: the game writes it as `receiver`, and the link writes it as `sender` on everything it sends, whichever Director it sends for (ticket *The game link's shape*, `.scratch/director-game-link/issues/02-game-link-shape.md`). The rows above that say "body" also travel on the link for a Director: `regia_cue`, `regia_fact` and the Action messages. Where `regia_join`, `regia_leave`, `regia_pause`, `regia_resume` and `regia_story_ended` go was decided in the ticket *Messages for the whole run* (`.scratch/director-game-link/issues/05-messages-for-the-whole-run.md`). How a Director hears the game through the link, and the state request, were decided in the ticket *A Director hearing the game for itself* (`.scratch/director-game-link/issues/03-hearing-the-game.md`). How a Director's Actions travel on the link, which replaced the Root's Action relay, was decided in the ticket *A Director doing its own Actions* (`.scratch/director-game-link/issues/04-doing-its-own-actions.md`).

### Arguments

`args` is a JSON array, encoded the same way in every message type and in both directions:

| Regia value | JSON |
| --- | --- |
| a Number | a JSON number |
| a name, or an Agent's name | a JSON string |
| a list | a JSON array |

The game never parses Jason term text. `regia-jason` turns JSON into Jason terms on the way in (a string becomes an atom) and back on the way out.

## Custom Actions

### Sending

A Custom Action whose External name has **no dots** is a **game Action** (chapter 10). `DO walk_to(?p)` compiles to

```
regia.act("walk_to", walk_to(P))
```

The first argument is the External name, the second the Action under its Regia name, so the Trace and the mind inspector show Regia's name.

`regia.act` is an internal action in `regia-jason`. It sends `regia_action` through the agent's body (`VesnaAgent.perform`, which is public), and then **suspends the intention** until the reply it needs arrives, the same way `.wait` suspends: in Jason's pending intentions, never through `ConcurrentInternalAction` or `.suspend`, whose suspended flag would hide a waiting Pursuit from `.intend` (`PURSUING`, chapter 40). It is an internal action because it leaves the agent through its body or the game link (chapter 28, reason 1). Other intentions keep running in the meantime: a waiting `DO` holds back only the rest of its own Body.

```json
{"sender": "guard_1", "receiver": "body", "type": "regia_action",
 "data": {"id": 7, "name": "walk_to", "args": ["door"]}}
```

- `name` is the External name (chapter 10), sent exactly as written: the Regia name when the declaration has no `AS`.
- `id` is a whole number from a counter kept per body, starting at 1. A reply names it. A Director's Action takes its `id` from the game link's one counter (*Custom Actions in a Director*, below).
- A Custom Action with **dots** in its External name is a Java internal action, the Jason form of the Target's own code (chapters 10, 28). A game can't name an Action with a dot. See *The Target's own code*, below.
- Rejected: leaving the Action as a plain Jason environment action and adding an agent architecture whose `act()` sends it. A JaCaMo `.jcm` sends environment actions through CArtAgO's architecture, which finds no artifact for them, and Regia would have to stack its own architecture against that chain.

### The Target's own code

A dotted Action goes through `regia.act` too, so every `DO` has one entry point, for Agents and Directors alike. `DO play_fanfare`, with `ACTION hall.music.fanfare AS play_fanfare`, compiles to

```
regia.act("hall.music.fanfare", play_fanfare)
```

- `regia.act` sees the dot in `N` and **sends nothing**: no body, no game link and no `id` are involved. It finds the internal action through the agent's internal-action table (Jason's `Agent.getIA`), runs it **synchronously** with the Action's arguments, and writes both Trace entries (*The Trace*, below).
- It is `done` when the code returns `true`. It **fails** when the code returns `false` or throws, with the exception's message as `reason`, and the Plan fails with chapter 11's "Custom Action failed" cause, as for a game Action.
- **A missing class** fails the same way, with the reason `no Java class <External name>`. Nothing checks for it before the run: the classes live in the Project's `lib/` jars (chapter 28), which `regia check` and `regia build` never read.
- `WITHOUT WAITING` changes nothing: the code has returned before the next Statement either way.
- Decided in the ticket *The Target's own code in a Build* (`.scratch/showcase-1-5/issues/21-target-code.md`). Rejected: writing the bare internal action into the ASL between two `regia.trace` calls, which leaves no `FAILED` entry when the code fails.

### The game's replies

The game answers each `regia_action` with one or two `regia_action_result` messages:

```json
{"sender": "body", "receiver": "guard_1", "type": "regia_action_result",
 "data": {"id": 7, "status": "done"}}
```

| `status` | Means | Final? |
| --- | --- | --- |
| `accepted` | the game has started the Action | no |
| `refused` | the game couldn't start it: an unknown Action, a missing target, a character that can't act | yes |
| `done` | the Action is finished | yes |
| `failed` | the Action was started but couldn't be finished | yes |

- `reason` is an optional string. It is shown in the Trace only, and never reaches the Regia program.
- A `done` or `failed` without an `accepted` before it implies acceptance. An instant Action (`play_sound`) needs just one reply, `done`.
- **The game decides what "done" means for each Action**, as it decides which Cues exist. For `walk_to`, it means the character has arrived. Regia never checks the world itself (chapter 11). The `ACTION` declaration's doc comment records the agreement between the designer and the game programmer, and the Visual Editor shows it:

  ```regia
  #@desc: Done when the Agent has arrived. Refused if the place can't be reached.
  ACTION walk_to(place)
  ```

- A reply with an unknown `id`, or an `id` that has already had its final reply, is ignored, with a Trace warning.

### Waiting

| Statement | Waits for | Fails on |
| --- | --- | --- |
| `DO a` | the final reply | `refused` or `failed` |
| `DO a, WITHOUT WAITING` | `accepted`, or a final reply | `refused` |

- **`DO a` waits until the Action is done**, the same way each Statement finishes before the next one (chapter 08, ADR 0005).
- **`DO a, WITHOUT WAITING`** carries on once the game has accepted the Action. A `failed` that comes later can't fail a Body that has moved on, as with `PURSUE g, WITHOUT WAITING` (chapter 11): it is recorded in the Trace and nothing else. A designer who cares about the outcome either waits, or has the game send a Cue (`WHEN arrived(door):`), which is how 1.0 programs were written.
- **No timeout.** 2.0 has none on a `DO` (chapter 12). A game that never answers leaves a waiting `DO` waiting until its Plan is stopped, and then the Action is called off (below).
- **No body, no Action.** If the agent's body isn't connected (it never connected, or the connection dropped), `regia.act` sends nothing and fails at once as if the game had refused, with the reason `no body`. A Director's Action fails the same way when the game link isn't connected, with the reason `no game link` (chapter 28). A Director's Action already sent when the link is lost fails too (*Custom Actions in a Director*).

### A Plan that stops while waiting

If a waiting `DO`'s Plan is stopped (its Goal is dropped, its Phase is exited, its Playbook is taken away, its Staging ends, its Agent leaves), **the Action is called off**: the body sends the game

```json
{"sender": "guest_2", "receiver": "body", "type": "regia_action_cancel",
 "data": {"id": 7}}
```

- **The game decides what calling off means** for each Action, as it decides what "done" means: the Guest puts down the fork, a `walk_to` stops where it is, an instant Action has nothing to stop. The `ACTION` doc comment records it.
- **It has no reply.** Any reply the game sends later under that `id` is dropped silently, with no `T37_01-stray-action-result`.
- **Only a waiting `DO` is called off.** An Action started `WITHOUT WAITING` was set loose and is never called off, as a Goal started `WITHOUT WAITING` isn't dropped (chapter 08). A Plan that **fails** never has an Action under way: it stops at the failing Statement.
- **A dotted (Java) Action can't be called off**: it runs synchronously, so no Plan is ever stopped while it waits on one.
- **A Director's Action** is called off the same way, on the game link (*Custom Actions in a Director*, below).
- In `regia-jason`, `regia.act` keeps the suspended intention of each waiting Action; when Jason drops that intention (`.drop_desire`, a Phase's intentions dropped, a Playbook taken away), a circumstance listener sees it go and sends the cancel. See ADR 0038.

## Game messages in an Agent

An Agent runs on `regia.RegiaAgent`, which extends VEsNA-Pro's `VesnaAgent` (chapter 28). `VesnaAgent` passes every message from its body to **`myHandleMsg(String)`**. That method is public, and the body's handler calls it on the agent object, so a subclass's override is the one that runs. `regia.RegiaAgent` overrides it:

- `regia_cue` and `regia_fact` are taken in as chapter 30 says.
- `regia_action_result` resumes the intention waiting in `regia.act`.
- **Every other type** (`signal`, `sight`, `rcc`, `exploration`, …) is passed to `super.myHandleMsg`, so VEsNA behaves as before.

Nothing changes in VEsNA-Pro.

### VEsNA-Pro's own actions

VEsNA-Pro's built-in internal actions (`vesna.walk`, `vesna.jump`, `vesna.rotate`) are **outside the Regia interface**. They send fire-and-forget commands, and report completion through VEsNA's `signal` messages (`movement(completed, destination_reached)`), which bypasses everything above. A Regia game exposes movement as a game Action like any other (`walk_to`, done when the character arrives). The Transpiler doesn't reject `ACTION vesna.walk AS walk`, since dotted names are Java internal actions the project may write itself, but its waiting and failure aren't Regia's.

## Game messages on the game link

No Director has a body (chapter 30). The game link reads every message the game sends on its connection: `regia_cue`, `regia_fact`, `regia_state_result`, `regia_join`, `regia_leave`, `regia_action_result`, `regia_pause` and `regia_resume`. It handles `regia_pause` and `regia_resume` itself, and delivers the rest to the attached Directors that should have them (chapters 28, 30, 33): a Fact or Cue to every Director that hears it, a `regia_state_result` to the Director that asked, a `regia_action_result` to the Director that sent the Action. Any other type is ignored, with `T37_02-unknown-message-type`. A Director takes in what the link delivers in its own Java message intake (chapter 30, *Hearing the game*).

### The game's starting state

When a Director attaches (chapter 30), the link asks the game for the state that Director starts with:

```json
{"sender": "regia_game_link", "receiver": "body", "type": "regia_state",
 "data": {"id": 4, "facts": ["door_open", "seated_at"], "agents": ["alice", "bob"]}}
```

```json
{"sender": "body", "receiver": "regia_game_link", "type": "regia_state_result",
 "data": {"id": 4, "facts": [{"name": "seated_at", "args": ["alice", "table_2"]}], "left": ["bob"]}}
```

- `facts` in the request are the External names of the Facts the Director's Plot hears. The reply lists **every instance of them true now**, in `regia_fact`'s `name` and `args` form (chapter 30). A Fact with no instance true is just absent.
- `agents` are the Agents of the Director's starting cast. `left` names those that have already left the game. The game keeps no record of Stagings: each request is a question about its own state, asked under an `id`.
- `id` comes from the link's counter, which Directors' Actions share (*Custom Actions in a Director*, below). A reply with an unknown `id`, or a second reply to one, is ignored with `T37_03-stray-state-result`.
- **The game must answer every request**, in order with the rest of what it sends: the reply describes the game when it is sent, and what changes after it is sent after it. A game that never answers holds that Director unstarted (chapter 30).
- **The first request is the Root's.** Subplots start only from a running Director, so the game knows the story has begun once it has answered the first `regia_state`, and sends **no `regia_join` before** it: the link would drop it (`T33_05-join-before-root-state`, chapter 33).
- With no link, there is no request: the Director starts with no game Facts and nobody left (chapter 30).

## Custom Actions in a Director

A Director writes `DO` exactly as an Agent does (chapter 20), and **every Director sends its own Actions** through the game link, the Root included. No Director has a body (chapter 30), and none performs an Action for another. Decided in the ticket *A Director doing its own Actions* (`.scratch/director-game-link/issues/04-doing-its-own-actions.md`).

- **Sending.** A Director's `regia.act` hands the Action to the link. The link takes an `id` from **its one counter**, the same one `regia_state` uses, so every `id` the link sends is unique on its connection. It records the `id` against the requesting Director and sends `regia_action` with `sender: "regia_game_link"`. The game never learns which Director acted. Agents keep their counters per body.
- **Replies.** The link routes each `regia_action_result` **by `id` alone** and delivers it into the requesting Director's mailbox with `receiveMsg`, like a Fact or a Cue. A reply therefore keeps its place in socket order: a `regia_fact` the game sent before a `done` is a belief before the Plan's next Statement runs. `regia.DirectorAgent`'s Java intake resumes `regia.act`, with the same code as an Agent's `myHandleMsg`, and no ASL plan is involved. A suspended atomic intention still wakes on a message, so a `DO` in an `EXITED` Plan wakes inside the atomic transition (chapter 30, *A `DO` in `EXITED`*). `regia.stop_hearing` stops Facts and Cues only, so an ending Director still gets its Action replies until it detaches. The link forgets an `id` at its final reply.
- **Calling off.** When a waiting Director Action's intention is dropped, the same circumstance listener as an Agent's sees it (*A Plan that stops while waiting*, above). `regia.act` asks the link to send `regia_action_cancel {id}`, and the link forgets the `id`, so a later reply under it is dropped silently with no `T37_01-stray-action-result`. ADR 0038 holds unchanged; only the transport differs from an Agent's.
- **Detaching with Actions in flight.** A Director's walk can't reach its kill with a **waiting** `DO`: step 1 stops the other intentions, which calls their Actions off, and `EXITED` waits for its own (chapter 31). A Director that dies some other way is killed without any intention being dropped, so when it **detaches** (chapter 30, its stop hook) the link calls off each of its waiting Actions itself: it sends `regia_action_cancel` and writes `DO <action> CANCELLED`. An Action that Director started **`WITHOUT WAITING`** stays in flight. The link keeps its `id` until the final reply and then writes the outcome entry itself, under that Director's name. It never delivers the reply to an agent: Jason reuses a killed agent's name, so a new Director of the same name must not receive it.
- **A lost link.** If the link's connection closes, every Director Action still in flight gets a final `failed` with the reason `no game link`, since no reply can come any more. A waiting `DO` fails its Plan, a `DO` in an atomic `EXITED` no longer holds its Director (and every ancestor's walk) forever, and a `WITHOUT WAITING` one gets its `FAILED` entry. A new Action fails at once (*Waiting*, above).
- **Rejected:** the Root's **Action relay**: a Subplot Director sent `achieve regia_act(N, A, ReqId)` to the Root, which sent the Action under its own `id`, kept `regia_relay(Id, Requester, ReqId)` and told each reply back as `regia_act_result`. The Root ran ASL and kept records for other Stagings, its relay plans had to stay unguarded while it ended, and a relayed reply to an ended requester needed `regia.send`'s catch. **Resuming the intention straight from the socket thread** (`runAtBeginOfNextCycle`): the resume could overtake a Fact the game sent before the reply, still waiting in the mailbox. **A separate Action counter on the link**: it gives nothing back, and the same `id` would name two requests on one connection.

## Pausing

The game tells the game link when it pauses and resumes. The link stops and starts the clock itself; no Director is involved:

```json
{"sender": "body", "receiver": "regia_game_link", "type": "regia_pause", "data": {}}
```

- **A run has one clock** (chapter 12), shared by every Agent and Director in it, held in `regia-jason`. `regia_pause` stops it and `regia_resume` starts it again. Every `regia.wait`, with or without a condition, and every `AFTER`, is measured on it.
- **Only Durations stop.** Messages, Cues and Actions go on: an Agent's body that is still sending Cues while the game is paused is the game's choice.
- A second `regia_pause` while paused, or a `regia_resume` while running, does nothing.
- Each change writes a `time` entry, `CLOCK PAUSED` or `CLOCK RESUMED` (chapter 34), written by the link.
- **A lost link starts the clock again.** If the link's connection never opens or is lost while the clock is stopped, no `regia_resume` can come, so the link starts the clock and writes `CLOCK RESUMED` (chapter 28).

## The end of the story

When the Root Staging ends (chapter 31), the Root Director sends the game one message through the game link, with the internal action `regia.end_story(O)` (no ASL plan is involved), after the last `regia_ended` from its children and before it is killed like any other Director (chapter 31, *The walk*, step 5):

```json
{"sender": "regia_game_link", "receiver": "body", "type": "regia_story_ended",
 "data": {"outcome": "banquet_over"}}
```

- `outcome` is the Root's Outcome (chapter 17) as a JSON string, or `null` when `END PLOT` has none.
- The game decides what to do with it (credits, a menu). It sends no reply.
- **After it**, no Director is left. The link drops every `regia_join` (`T33_04-join-after-root-ended`, chapter 33), still kills Agents the game reports as leaving, and still stops and starts the clock. Agents keep running with no Givings, on their own bodies.

## The Trace

Each game Action writes **two** `action` entries (chapter 34):

| When | Console text |
| --- | --- |
| `regia_action` is sent | `DO <action>` |
| its final reply arrives | `DO <action> DONE`, `DO <action> FAILED` or `DO <action> REFUSED`, with `reason` when given |
| its Plan stops while it waits | `DO <action> CANCELLED` |

- The two entries are linked by the Action's `id`. The outcome entry has `of: <seq of the sent entry>`.
- `accepted` writes no entry. A sent entry with no outcome entry tells you the game either never saw the Action or never finished it.
- Both are written by `regia.act` and the reply intake in `regia.RegiaAgent` and `regia.DirectorAgent`, not by generated ASL. A Director's Action is traced by that Director. An outcome that arrives after it has detached, and a call-off made at its detach, are written by the game link under its name (*Custom Actions in a Director*).
- A waiting Action whose Plan stops gets `CANCELLED` as its outcome entry, and nothing the game sends later under its `id` gets one. An Action started `WITHOUT WAITING` whose Plan has moved on still gets its outcome entry when the reply comes.
- A `no body` refusal writes both entries at once.
- A `FAILED` or `REFUSED` that fails a waiting Plan is followed by chapter 34's failure chain, starting with chapter 11's "Custom Action failed" cause.
- A dotted (Java) Custom Action writes the same two entries, sent and `DONE` or `FAILED`, both by `regia.act` (*The Target's own code*), so every `DO` looks alike in the Trace.

## Test mode

`ScriptedGame` (chapter 35) plays the game's side of the Action protocol, on the Agents' bodies and on the game link alike:

- It never sees a dotted Action, which runs the project's own Java from `lib/` for real (chapter 35), so no standing rule holds it or makes it fail.
- By default, it answers every `regia_action` with a single `done` at once, under the `id` it came with: a body's own, or the link's shared one for a Director's Action.
- Standing rules match an Action by name and arguments, never by `sender`, so a Director's Action (`sender: "regia_game_link"`) is held and finished like an Agent's (chapter 34).
- The standing rules of chapter 34 (`> action fails`, `refused`, `holds`, `succeeds`) change how it answers Actions matching a pattern from then on: `failed` after `accepted`, `refused`, `accepted` with no final reply, or the default.
- `> action done <pattern>` and `> action failed <pattern>` send the final reply to every held Action that matches.
- It records every `regia_action_cancel` and stops holding that Action. A case expects the call-off through the `DO <action> CANCELLED` entry; a later `> action done` no longer matches it. A call-off the link makes for a detaching Director is the same: the entry is written under that Director's name.
- It answers every `regia_state` at once, from the Facts it has reported on the link and the Agents that have left (chapter 35, *The game's state*).
- It sends `regia_pause` and `regia_resume` on the link for the steps `> pause` and `> resume` (chapter 34).
- `> lose link` closes the link's connection: every Director Action in flight fails with `no game link`, and a paused clock starts again (*Custom Actions in a Director*, *Pausing*).
- It ignores `regia_story_ended`, which is already visible in the Trace as the Root's `STAGING … ENDED` entry.
- A run whose only intentions are waiting on held Actions counts as **settled**, as one waiting in `regia.wait` does.

## Infrastructure state

No rows for chapter 28's table. The relay's `regia_relay(Id, Requester, ReqId)` is retired with the relay.

An Agent's `id` counter and the waiting intentions live in `regia.act`'s Java state, like `.wait`'s pending intentions, since they hold suspended intentions and aren't something an ASL plan reads. For a Director, the counter and each in-flight `id`'s Director are the game link's plumbing (chapter 28), and the waiting intentions are still `regia.act`'s.

## `regia-jason` additions

- `regia.act(N, A)`, the reply intake, and the `myHandleMsg` override in `regia.RegiaAgent`. `regia.act` also runs a dotted Action's Java class itself.
- The cancel sent when a waiting `regia.act` intention is dropped, through a Jason circumstance listener.
- The run's clock, stopped and started by `regia_pause` and `regia_resume` at the game link.
- The game link's `regia_state` request on attach, and its routing of the reply to the Director that asked.
- The game link's Actions: the shared `id` counter, routing replies by `id`, sending a Director's cancel, calling off a detaching Director's waiting Actions and tracing its late outcomes, and failing in-flight Actions when the link is lost.
- Internal action `regia.end_story(Outcome)`.
- `ScriptedGame`'s Action rules and steps.

## Trace entries

**Warnings**

- `T37_01-stray-action-result` A `regia_action_result` with an unknown `id`, or after the final reply, ignored.
- `T37_02-unknown-message-type` A message of an unknown type on the game link, ignored.
- `T37_03-stray-state-result` A `regia_state_result` with an unknown `id`, or a second one for the same `id`, ignored.

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025).

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- An Agent's body lost with an Action in flight: a waiting `DO` gets no reply and waits until its Plan is stopped. Directors fail theirs with `no game link` (*Custom Actions in a Director*); whether Agents should match is outside the map *Directors and the game, without a gateway*, which leaves Agents' bodies alone.
- How Godot implements the protocol: out of scope (VEsNA/Godot internals).
