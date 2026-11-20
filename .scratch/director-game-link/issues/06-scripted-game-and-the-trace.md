# ScriptedGame and the Trace on the game link

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 02, 03, 04, 05

## Question

How the Conformance harness and the Trace chapters follow the game link (chapters 28, 30, 33 and 37 as edited on this map). Chapter 35 still describes the Root with a body of its own (lines 77–89).

Decide:

- **`ScriptedGame`'s wiring.** It reads the `.jcm` (chapter 36). It now plays the far side of `regia.GameLink`'s `platform:` connection on `base_port` as well as each Agent's body. Decide how it tells the two apart, and what it answers on the link: `regia_state` from its scripted Facts and leaves, and Directors' `regia_action`s under the link's shared ids.
- **Steps addressed to a Director.** `> cue director:Banquet poison_drunk` (chapters 34, 35): now that the game never names a Director, such a step goes out once on the link, and every Director hearing it gets it. Decide whether the `director:` address survives, changes meaning, or goes.
- **Held Actions.** `> action done <pattern>` and the standing rules match Actions by name and arguments. A Director's Action reaches `ScriptedGame` with `sender: "regia_game_link"`. Decide whether matching needs the sender at all, and how a case expects a link-side `CANCELLED` (Director detached) or a late outcome traced by the link.
- **A lost link.** Whether a case can script `T2802`/`T2803` and in-flight Actions failing with `no game link`, and with which step.
- **Settled.** Whether chapter 35's *settled* rule needs the link: a Director unstarted while its `regia_state` waits, and Actions held on the link.
- **Trace entries.** Where chapters 34/35 list `T2802`, `T2803`, `T3305`, `T3703`, and whether new entries are needed (a message no attached Director hears; a reply for a detached Director). Chapter 34's code table (line 116) still lists `T3701`, `T3702` only.

Closes when chapters 34 and 35 are edited (and 37's *Test mode*).

## Comments

## Resolution

Decided with the user on 2026-11-19.

- **`ScriptedGame` tells the link from a body by port.** The `.jcm`'s `platform: regia.GameLink(address, base_port)` port is the link's, and every other port belongs to its Agent. It never looks at `sender`.
- **`director:` steps are gone; `link` takes their place.** `> cue link x` and `> fact link ±x` send one message on the link. The External name comes from the Build's Director files (Subplots' included), or the Regia name is sent if none lists it. Every running Director that hears the item gets it, and one nobody hears is dropped with no entry, which is not a case error. A `*` step goes to every body that uses the item and then once on the link if any Director file lists it, and its `script` line lists `link` last.
- **`T2801` is Agents only.** A Director never receives an item it doesn't hear, and the link writes nothing for a message no attached Director hears.
- **Held Actions match by name and arguments, never by sender.** A call-off or late outcome the link writes for a detached Director is under that Director's name, so a case expects it like any other.
- **A lost link is scriptable.** `> lose link` closes the connection (`T2803`, in-flight Director Actions `FAILED` with `no game link`, the clock started again, and later `link` steps are case errors). `#! game link: none` leaves the link's port unserved (`T2802` at start).
- **The game's state.** `ScriptedGame` keeps the Facts it has reported on the link and the Agents named by `> leave`, and answers every `regia_state` at once. `> fact link +…` steps before `> start` set the starting Facts without sending anything. State replies can't be held, so `T3305`/`T3703` aren't scriptable.
- **Settled** adds "nothing sent is still on its way on any connection, the link's included". A Director waiting for its state reply needs no rule of its own.
- **Codes.** Chapter 34's table now lists `T2801`–`T2803`, `T3301`–`T3305` and `T3701`–`T3703`. No new codes.

Edited: chapter 34 (step table, *A Cue or a Fact names who receives it*, new bullets on the game never naming a Director, the game's state, a lost link and matching held Actions, settled, headers, the `script` console text, the code table, intro), chapter 35 (*Test mode* steps 1–4, new *The game's state*, the `action` row of the writer table, intro), chapter 37 (*Test mode*), chapter 28 (`T2801` and *External names*), chapter 30 (`T2801` line in *What the game sends*).
