# Custom Actions through VEsNA

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo

## Question

How do Custom Actions and Regia's game messages work with VEsNA-Pro (`vesna-pro-main/`)? Decide:
- How a dot-less Custom Action (chapter 28's "environment action") reaches the game: VEsNA-Pro today only sends its own internal actions (`vesna.walk`, `jump`, `rotate`) through `perform()`, fire-and-forget.
- Whether `DO` waits for the game's answer, and how the game reports a failed Action (spec 11 relies on it).
- How the Root Director performs Actions passed up from Subplot Directors (`regia_act(A)`, chapter 30) and returns their result.
- How `regia-jason` receives its `regia_event` and `regia_fact` messages (chapter 30) inside an Agent's `VesnaAgent` body, whose message handler is private and logs unknown types: an upstream hook in VEsNA-Pro, or something else.

## Answer

Spec chapter: `docs/spec/37-jason-game-protocol.md`, checked against VEsNA-Pro's `VesnaAgent`, `WsClient` and `vesna.walk`. Chapters 08, 11, 28, 30, 31, 33–36 and the glossary's *Custom Action* point to it. No ADR: a waiting `DO` follows ADR 0005, and the rest is cheap to change.

- **Sending**: a dot-less `DO a(x)` compiles to `regia.act(a(x))`, which sends `regia_action {id, name, args}` through the body's public `perform` and suspends only its own intention. Dotted names stay Java internal actions. A custom `act()` architecture was rejected (JaCaMo routes environment actions through CArtAgO).
- **Replies**: `regia_action_result {id, status, reason?}`, with `accepted`, `refused`, `done` or `failed`; `done`/`failed` alone imply `accepted`. The game defines "done" for each Action, and the `ACTION` doc comment records it.
- **Waiting**: `DO a.` waits for done, and fails on `refused`/`failed`. `DO a, WITHOUT WAITING.` waits for `accepted`, and fails only on `refused`; a later `failed` is Trace only. There's no timeout. With no connected body, the Action is refused locally (`no body`). A Plan stopped while waiting doesn't cancel the Action; late replies are traced and ignored.
- **Arguments**: JSON numbers, strings and arrays, the same for `regia_event`, `regia_fact` and `regia_action`.
- **Intake**: `regia.RegiaAgent` overrides VEsNA's public `myHandleMsg` for `regia_*` and passes the rest to `super`, so nothing changes upstream. `regia.DirectorAgent` reads its own body's messages.
- **Directors**: a Subplot Director's `DO` goes directly to the Root (`achieve regia_act(A, ReqId)`), which performs it under its own `id` (`regia_relay`) and relays replies. Hop-by-hop forwarding was rejected.
- **Story end**: the Root sends `regia_story_ended {outcome}` once, with no reply expected.
- **Trace**: two `action` entries per Action, `DO a` when sent and `DO a DONE`/`FAILED`/`REFUSED` at the final reply, linked by `of`. `accepted` gets no entry.
- **Test mode**: `ScriptedGame` sends `done` at once by default. Standing rules: `> action fails`/`refused`/`holds`/`succeeds`. One-off steps: `> action done P` and `> action failed P`. A run waiting only on held Actions counts as settled.
- **VEsNA built-ins** (`vesna.walk`, …) are outside the Regia interface; movement is a game Action like any other.

## Comments

- Surfaced by *Director runtime in ASL* (36), 2026-11-11.
- From *Stagings and Subplots runtime in ASL* (37): the Root Director's `END PLOT` leaves its agent alive and idle; decide whether and how the game hears that the story has ended (chapter 31).
- From *Quota counts and cast changes in ASL* (39): the Root Director's body also receives `regia_join` and `regia_leave` (chapter 33).
- From *Trace and logging* (40): `action` Trace entries are written when an Action's result comes back, so the design here must give the agent architecture that result. Behaviour cases run against `ScriptedGame` (ADR 0014), a WebSocket server that speaks the game's JSON protocol and must fake whatever result messages are decided here (success unless `> action fails`). The answer also fixes what the `regia_event`/`regia_fact` intake looks like to `ScriptedGame` (chapter 35).
- From *.jcm generation* (41): `regia_join` carries exactly `{kind, name, port}`; the Build writes `cast.json` (starting Agents with kind and port, the Root Director's port) for the game (chapter 36).
