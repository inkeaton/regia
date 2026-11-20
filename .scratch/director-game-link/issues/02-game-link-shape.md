# The game link's shape

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 01

## Question

What the game link is, in `regia-jason`: a Jason `Environment` (each agent's percepts and `executeAction` are per agent by design), or a shared object of its own that each `regia.DirectorAgent` attaches to, wrapping one VEsNA `WsClient`.

Decide:

- which of the two, with the research's facts on runtime-created agents, momentary events and long pending Actions;
- who opens the connection, and at which `address`/`port` (the Root Director's `.jcm` entry and `base_port` today, chapter 36), and what happens if it never opens or closes mid-run;
- what state the link holds in Java (who is attached, what each hears, pending Actions) and how that squares with chapter 28's *Infrastructure state*, loosened to "no Regia state in Java";
- what the Root Director still is once it isn't the gateway: its `.jcm` entry, its port, its body.

Closes when chapter 28 (*The Java library*, *Infrastructure state*) and chapter 30 (*The Director's agent class*) are edited, and the ADR is written.

## Comments

**From the research (2026-11-19, *How Jason and VEsNA can share one game connection*).** Two findings weigh heavily here:
- **JaCaMo 1.2 never creates a Jason `Environment`**, and its architecture sends every action to CArtAgO, so the `Environment` option is a dead end unless VEsNA-Pro leaves JaCaMo or a later JaCaMo changes this. Environment percepts are also state, not momentary Cues.
- **One `WsClient` with a dispatcher on `receiver` works as the API stands**, and `LocalAgArch.receiveMsg` puts a message in a Director's mailbox in order with its other messages and wakes it. Its sender can be set (to `percept`, say), and a `signal` message is the only way to get a momentary event.

Also decide what the link does when its socket errors or closes (VEsNA's own handler kills its agent), and what `receiver` the game writes for messages to the link (chapter 37's `regia_pause` example still names the Root). From *Messages for the whole run*: the link also kills leavers, checks `T3302`, drops joins after the story (`T3304`), and runs the clock, so it needs to know the Program's Agents, which Director is the Root, and whether the Root Staging has ended.

## Resolution

Decided with the user on 2026-11-19.

- **A `regia-jason` object, not a Jason `Environment`.** `regia.GameLink` wraps one VEsNA `WsClient`, sorts each game message out to attached Directors and delivers it with `LocalAgArch.receiveMsg`; Directors call it to send. The `Environment` is recorded as rejected, not left open: under JaCaMo 1.2 it is never created, and its percepts are state, so it can't carry a Cue.
- **A JaCaMo platform.** `platform: regia.GameLink("<address>", "<base_port>")` in the `.jcm`. JaCaMo `init`s platforms before `createAgs` (checked in the 1.2 bytecode), so the link connects, with a bounded wait, before any Director exists. It lives as long as the MAS, outliving the Root, and closes in `stop`. Directors reach it through a static accessor.
- **Ports.** The link takes `base_port`; starting Agents keep `+1, +2, …`. `cast.json` names `game_link` instead of the Root Director.
- **The Root Director has no body**, nor any Director. Its `.jcm` entry keeps only `ag-class`. It attaches *as* the Root, which is how it alone gets `regia_join`.
- **Java holds plumbing only**: the connection, who is attached and what each hears, Actions in flight, the clock. In the user's words: this is plumbing to move game information, and that information lives in the game or in agents, never in Java. So no cache of game Facts. Regia-shaped answers are read from Jason when needed: `T3302` asks the runtime whether the leaver is an Agent, `T3304` is "no Root attached".
- **`regia_game_link`** is the link's name in the envelope: the game's `receiver`, and the link's `sender` on everything it sends, Actions and `regia_story_ended` included. No Director name reaches the game. The link routes on `type` and item name, not `receiver`.
- **A failing link.** Never opened or lost mid-run: the run goes on (the MAS starts even if `init` couldn't connect), Directors stay attached, Directors' Actions fail at once with `no game link`, a paused clock starts again with `CLOCK RESUMED`, and the Trace gets `T2802` (couldn't connect) or `T2803` (connection lost). No reconnecting in 2.0; the link never kills a Director.

Edited: chapter 28 (*The Java library*, *The game link*, *Infrastructure state*, `T2802`/`T2803`), chapter 30 (*The Director's agent class*, *What the game sends*), chapter 33 (*Not decided here*), chapter 36 (*Ports and addresses*, the `.jcm` example and its bullets, `cast.json`, *Not decided here*), chapter 37 (envelope, *No body, no Action*, *Game messages on the game link* replacing *Game messages in the Root Director*, *Custom Actions in a Director*'s Root bullet, *Pausing*, *The end of the story*, *Not decided here*). ADR 0040, *Directors share one game link that holds only plumbing* (`docs/adr/0040-directors-share-one-game-link-that-holds-only-plumbing.md`).
