# A Director hearing the game for itself

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 02

## Question

How a Director hears the game through the game link, replacing chapter 30's *Routing percepts to Directors* and *Game Facts a Subplot starts with*.

Decide:

- when a Director attaches and detaches, and what it registers: its own Plot's `regia_hears` only, so `regia_hears` no longer includes what descendants hear;
- what replaces the parent's snapshot of game Facts at a child's start: the link keeping the game's current Facts, or something else, and whether that cache is game state or Regia state;
- **ordering**: `regia_start` comes from the parent, while percepts come from the link, a different sender, so per-sender order no longer puts the snapshot before the start, or the start before the first percept. What a Director does with a percept that arrives before `regia_start`, and how `LEARNED` stays silent for starting state;
- how an ending Director stops hearing (detaching at the walk's first step, chapter 31's *An ending Director hears nothing*), and whether `regia_percept`, `regia.perceive` and `regia.add_percepts` survive;
- how the Root Director hears, now that it has no body of its own (or keeps one);
- **reconciling the cast at attach** (from *Messages for the whole run*): a Subplot drops every Agent of its `regia_start` cast that has already left the Program before `!regia_begin`. Decide how it learns who has left (asking the link, or the link's state at attach) and how this is ordered with `regia_start`. It is the same race as the Fact snapshot (chapter 33, *Every Director hears a leave*).

Closes when chapters 30 and 31 are edited.

## Comments

**From *The game link's shape* (2026-11-19).** The link is `regia.GameLink`, a JaCaMo platform up before any Director, delivering with `LocalAgArch.receiveMsg` under the sender of its choice. Hard constraint from the user: **game information never lives in Java**, so the link keeps no cache of the game's current Facts. A Subplot's starting Facts must come from the game or from agents' beliefs. The Root has no body, so it hears through the link like any Director (that bullet of the question is settled). A lost link means Directors simply hear nothing more.

## Resolution

Decided with the user on 2026-11-19.

- **`regia_hears` covers the Director's own Plot only.** Attaching registers its name, those names (External), and whether it is the Root, as the link's routing table.
- **Starting state comes from the game.** On attach the link sends `regia_state` `{"id", "facts": [names], "agents": [cast]}`, and the game answers `regia_state_result` `{"id", "facts": [{"name","args"}], "left": [names]}`. No parent snapshot and no cache in the link. Rejected: the parent's `regia_hears` covering descendants with a snapshot (fails the test), a Fact cache in the link (game information in Java), asking the runtime who has left (Jason's local `killAgent` kills on its own thread, so a fresh leaver may still look alive).
- **Ordering.** A Subplot attaches on `regia_start` (the Root on `regia_start_cast`). The link registers it when it sends the request but delivers nothing to it until the reply has gone through. The link reads the socket in order, so nothing is lost or counted twice, and nothing is buffered. The reply's Facts are added without events in Java, then `!regia_attached(Left)` drops the leavers from the cast and runs `!regia_begin`. So `LEARNED` stays silent for starting state, and this also closes *Messages for the whole run*'s cast race.
- **Intake in Java.** `regia.DirectorAgent` turns `regia_cue`/`regia_fact` into events and beliefs with the Agents' `myHandleMsg` code. `regia_percept`, `regia.perceive` and `regia.add_percepts` are gone. `regia.attach` and `regia.stop_hearing` come in.
- **Ending.** At walk step 1, `regia.stop_hearing` ends Facts and Cues, but the Director stays attached for leaves (keeping chapter 33's ending rule). Its stop hook detaches it at the kill or on any death.
- **The Root** hears the same way. It is always the first to attach, so the game sends no `regia_join` before answering the first `regia_state`, and one sent earlier is dropped (`T3305`).
- **No link** at attach, or lost before the reply: the attach completes at once with nothing, and the Staging starts. A connected game that never answers holds that Director unstarted; avoiding that is the game's job.

Edited: chapter 30 (intro, *What the game sends*, *Hearing the game* replacing *Routing percepts to Directors* and *Game Facts a Subplot starts with*, *Starting a Staging*, *Signals*, *Infrastructure state*, additions), chapter 31 (records, *Starting a Subplot* and the child's two plans, `END SUBPLOT`, *An ending Director hears nothing*), chapter 33 (the Root's start, *Reports that make no sense*, *Every Director hears a leave*, `T3305`, *Not decided here*), chapter 37 (envelope, *Game messages on the game link*, new *The game's starting state*, `T3703`, additions), chapter 28 (*The game link*), chapter 20 (one line), ADR 0040 (one consequence clause).

