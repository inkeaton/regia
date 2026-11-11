# The game protocol in Jason

How a Jason Build and the game talk to each other: how a Custom Action reaches the game and how its result comes back, how `regia-jason` reads game messages inside VEsNA-Pro's agent, how a Subplot Director's Custom Actions are performed, and what the game hears when the story ends. Decided in the ticket *Custom Actions through VEsNA* (`.scratch/regia-2/issues/43-custom-actions-through-vesna.md`). It builds on chapter 08's `DO`, chapter 11's Failures, chapter 28's External names, chapters 30–33's game messages and chapter 35's test mode. It was checked against VEsNA-Pro's `VesnaAgent`, `WsClient` and `vesna.walk` (`vesna-pro-main/src/agt/vesna/`).

## The envelope

Every message between a body and the game uses VEsNA's JSON envelope, `{"sender", "receiver", "type", "data"}`. Regia's message types:

| Type | Direction | `data` | Chapter |
| --- | --- | --- | --- |
| `regia_event` | game → body | `{"name", "args"}` | 30 |
| `regia_fact` | game → body | `{"op": "add" \| "remove", "name", "args"}` | 30 |
| `regia_join` | game → Root Director | `{"kind", "name", "port"}` | 33, 36 |
| `regia_leave` | game → Root Director | `{"name"}` | 33 |
| `regia_action` | body → game | `{"id", "name", "args"}` | here |
| `regia_action_result` | game → body | `{"id", "status", "reason"?}` | here |
| `regia_story_ended` | Root Director → game | `{"outcome"}` | here |

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

A Custom Action whose External name has **no dots** is a **game Action**. `DO walk_to(?p).` compiles to

```
regia.act(walk_to(P))
```

`regia.act` is an internal action in `regia-jason`. It sends `regia_action` through the agent's body (`VesnaAgent.perform`, which is public), and then **suspends the intention** until the reply it needs arrives, the same way `.wait` suspends. Other intentions keep running in the meantime: a waiting `DO` holds back only the rest of its own Body.

```json
{"sender": "guard_1", "receiver": "body", "type": "regia_action",
 "data": {"id": 7, "name": "walk_to", "args": ["door"]}}
```

- `name` is the External name (chapter 28), emitted exactly as written.
- `id` is a whole number from a counter kept per body, starting at 1. A reply names it.
- A Custom Action with **dots** in its External name stays a Java internal action (chapter 28). It runs synchronously in the agent, so it is `done` as soon as it returns, and it fails if the Java code fails.
- Rejected: leaving the Action as a plain Jason environment action and adding an agent architecture whose `act()` sends it. A JaCaMo `.jcm` sends environment actions through CArtAgO's architecture, which finds no artifact for them, and Regia would have to stack its own architecture against that chain.

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
- **The game decides what "done" means for each Action**, as it decides which Events exist. For `walk_to`, it means the character has arrived. Regia never checks the world itself (chapter 11). The `ACTION` declaration's doc comment records the agreement between the designer and the game programmer, and the Visual Editor shows it:

  ```regia
  ## Walks to the place. Done when the character arrives;
  ## fails if no path exists.
  ACTION walk_to(place)
  ```

- A reply with an unknown `id`, or an `id` that has already had its final reply, is ignored, with a Trace warning.

### Waiting

| Statement | Waits for | Fails on |
| --- | --- | --- |
| `DO a.` | the final reply | `refused` or `failed` |
| `DO a, WITHOUT WAITING.` | `accepted`, or a final reply | `refused` |

- **`DO a.` waits until the Action is done**, the same way each Statement finishes before the next one (chapter 08, ADR 0005).
- **`DO a, WITHOUT WAITING.`** carries on once the game has accepted the Action. A `failed` that comes later can't fail a Body that has moved on, as with `PURSUE g, WITHOUT WAITING.` (chapter 11): it is recorded in the Trace and nothing else. A designer who cares about the outcome either waits, or has the game send an Event (`WHEN arrived(door):`), which is how 1.0 programs were written.
- **No timeout.** 2.0 has none (chapter 12). A game that never answers leaves a waiting `DO` waiting until its Plan is stopped.
- **No body, no Action.** If the agent's body isn't connected (it never connected, or the connection dropped), `regia.act` sends nothing and fails at once as if the game had refused, with the reason `no body`.

### A Plan that stops while waiting

If a waiting `DO`'s Plan is stopped (its Goal is dropped, its Phase is exited, its Playbook is taken away, its Staging ends), **the game is not told**. The Action carries on in the game. Its later replies still get their Trace entry (below) and are otherwise ignored. Cancelling an Action is post-2.0.

## Game messages in an Agent

An Agent runs on `regia.RegiaAgent`, which extends VEsNA-Pro's `VesnaAgent` (chapter 28). `VesnaAgent` passes every message from its body to **`myHandleMsg(String)`**. That method is public, and the body's handler calls it on the agent object, so a subclass's override is the one that runs. `regia.RegiaAgent` overrides it:

- `regia_event` and `regia_fact` are taken in as chapter 30 says.
- `regia_action_result` resumes the intention waiting in `regia.act`.
- **Every other type** (`signal`, `sight`, `rcc`, `exploration`, …) is passed to `super.myHandleMsg`, so VEsNA behaves as before.

Nothing changes in VEsNA-Pro.

### VEsNA-Pro's own actions

VEsNA-Pro's built-in internal actions (`vesna.walk`, `vesna.jump`, `vesna.rotate`) are **outside the Regia interface**. They send fire-and-forget commands, and report completion through VEsNA's `signal` messages (`movement(completed, destination_reached)`), which bypasses everything above. A Regia game exposes movement as a game Action like any other (`walk_to`, done when the character arrives). The Transpiler doesn't reject `ACTION vesna.walk AS walk`, since dotted names are Java internal actions the project may write itself, but its waiting and failure aren't Regia's.

## Game messages in the Root Director

The Root Director runs on `regia.DirectorAgent`, not `VesnaAgent` (chapter 30), and reads its own body's messages: `regia_event`, `regia_fact`, `regia_join`, `regia_leave` and `regia_action_result`. Any other type is ignored, with a Trace warning.

## Custom Actions in a Director

A Director writes `DO` exactly as an Agent does (chapter 20).

- **The Root Director** performs it through its own body, as above.
- **A Subplot Director** has no body. Its `regia.act` sends the Action **directly to the Root Director**, whose agent name (`regia_director__<plot>`, chapter 31) is known at compile time, as `achieve regia_act(A, ReqId)`. The Root sends `regia_action` under an `id` of its own, records `regia_relay(Id, Requester, ReqId)`, and passes each reply back to the requester as `tell regia_act_result(ReqId, Status, Reason)`. It forgets the record once the final reply is relayed.
- The requester waits and fails exactly as an Agent would (above).
- A relayed reply whose requester has ended is caught by `regia.send` (chapter 33).
- Rejected: passing the Action up one parent at a time, as chapter 30 first said. Percepts go down hop by hop because each level filters them; an Action needs no filtering on the way up, and the extra hops would only add relay state to every Director in between.

## The end of the story

When the Root Staging ends (chapter 31), the Root Director sends the game one message, after the last `regia_ended` from its children and before it goes idle:

```json
{"sender": "regia_director__royalBanquet", "receiver": "body", "type": "regia_story_ended",
 "data": {"outcome": "banquet_over"}}
```

- `outcome` is the Root's Outcome (chapter 17) as a JSON string, or `null` when `END PLOT` has none.
- The game decides what to do with it (credits, a menu). It sends no reply.

## The Trace

Each game Action writes **two** `action` entries (chapter 34):

| When | Console text |
| --- | --- |
| `regia_action` is sent | `DO <action>` |
| its final reply arrives | `DO <action> DONE`, `DO <action> FAILED` or `DO <action> REFUSED`, with `reason` when given |

- The two entries are linked by the Action's `id`. The outcome entry has `of: <seq of the sent entry>`.
- `accepted` writes no entry. A sent entry with no outcome entry tells you the game either never saw the Action or never finished it.
- Both are written by `regia.act` and the reply intake in `regia.RegiaAgent` and `regia.DirectorAgent`, not by generated ASL. For a Subplot Director's Action, the requesting Director writes them; the Root's relay writes nothing.
- An outcome that arrives after its Plan has stopped still gets its entry.
- A `no body` refusal writes both entries at once.
- A `FAILED` or `REFUSED` that fails a waiting Plan is followed by chapter 34's failure chain, starting with chapter 11's "Custom Action failed" cause.
- A dotted (Java) Custom Action writes the same two entries, sent and `DONE` or `FAILED`, so every `DO` looks alike in the Trace.

## Test mode

`ScriptedGame` (chapter 35) plays the game's side of the Action protocol:

- By default, it answers every `regia_action` with a single `done` at once.
- The standing rules of chapter 34 (`> action fails`, `refused`, `holds`, `succeeds`) change how it answers Actions matching a pattern from then on: `failed` after `accepted`, `refused`, `accepted` with no final reply, or the default.
- `> action done <pattern>` and `> action failed <pattern>` send the final reply to every held Action that matches.
- It ignores `regia_story_ended`, which is already visible in the Trace as the Root's `STAGING … ENDED` entry.
- A run whose only intentions are waiting on held Actions counts as **settled**, as one waiting in `regia.wait` does.

## Infrastructure state

New rows for chapter 28's table:

| Concept | Held by | Functor |
| --- | --- | --- |
| A Subplot Director's Action being performed | Root Director | `regia_relay(Id, Requester, ReqId)` |

The `id` counter and the waiting intentions live in `regia.act`'s Java state, like `.wait`'s pending intentions, since they hold suspended intentions and aren't something an ASL plan reads.

## `regia-jason` additions

- `regia.act(A)`, the reply intake, and the `myHandleMsg` override in `regia.RegiaAgent`.
- The Root Director's relay plans for `regia_act` and `regia_story_ended`, in `regia/director.asl`.
- `ScriptedGame`'s Action rules and steps.

## Trace entries

**Warnings**

- `T3701` A `regia_action_result` with an unknown `id`, or after the final reply, ignored.
- `T3702` A message of an unknown type at the Root Director's body, ignored.

## Not decided here

- Cancelling an Action when its Plan stops: post-2.0.
- How Godot implements the protocol: out of scope (VEsNA/Godot internals).
