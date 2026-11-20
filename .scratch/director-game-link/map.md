# Map: Directors and the game, without a gateway

Label: wayfinder:map

## Destination

A decided design for how a Director reaches the game in the Jason Target, with no Director running or keeping anything on behalf of another Staging. Every Director attaches to one shared **game link**, hears the game for itself, and sends its own Actions. The design is carried into spec chapters 28, 30, 31, 33, 36 and 37, with one ADR (0040). It replaces the percept forwarding down the Staging tree and the Root's Action relay. It holds for Regia 1.5 and 2.0.

Charted with the user on 2026-11-19.

## Notes

- **Plan, don't do.** Tickets decide. A Jason decision closes only when the spec chapters it touches are edited, as on the showcase map. No `regia-jason` code is written here.
- **The test of "decentralised".** No Director's ASL runs, or keeps state, on behalf of another Staging. Relay plans, Facts kept for descendants, forwarding while ending and the Root as gateway all fail it. Shared Java plumbing passes (a single connection object and its routing table), as long as everything that means something to Regia stays in beliefs. Chapter 28's "no state on the Java side" is loosened to "no *Regia* state on the Java side"; the shared clock (chapter 37) already sits there.
- **The game stays unaware of Stagings.** It keeps sending to the Program as chapter 37's envelope says; `regia-jason` sorts each message out to the Directors that hear it.
- **Words.** The shared connection is **the game link**; a Director **attaches** to it and **detaches** from it. "Body" stays for an Agent's own VEsNA connection (and, in the language, a Plan's Body). These are Target words: they go in chapter 28, not in `GLOSSARY.md`.
- **What it reopens.** Decisions of *Director runtime in ASL* (`.scratch/regia-2/issues/36-director-runtime.md`), *Entering and leaving a Phase in ASL* and *Subplot arguments and endings in ASL* (`.scratch/showcase-1-5/issues/18-…`, `19-…`). The showcase map's reference Build waits for this map.
- Tickets: `.scratch/director-game-link/issues/NN-<slug>.md`, with `Type:`, `Status:`, `Assignee:` and `Blocked by:` lines. The frontier is the open, unblocked, unclaimed tickets, lowest number first.
- Skills: `grilling` and `domain-modeling` for every grilling ticket. Local sources first: `references/jason-main/`, the Jason book, `references/vesna-pro-main/` (memory *Local references*).

## Decisions so far

<!-- one line per resolved ticket: [title](issues/NN-slug.md): gist -->

- [How Jason and VEsNA can share one game connection](issues/01-sharing-one-connection.md): JaCaMo 1.2 never creates a Jason `Environment`, so that route is a dead end. One VEsNA `WsClient` with a dispatcher works as it stands, and `LocalAgArch.receiveMsg` delivers into a Director's mailbox in order and wakes it. Note on branch `research/game-link`.
- [Messages for the whole run](issues/05-messages-for-the-whole-run.md): the link delivers `regia_leave` to every attached Director and kills the leaver, with no `regia_left` passed down the tree. A Subplot reconciles its cast when it attaches. Joins go to the Root only. The Root is killed at its end like any Director, and later joins are dropped. Pause and resume go straight to the clock. Subplot–cast messaging already passes the rule. Chapters 33, 37 and 31 were edited, and chapter 28 got a *game link* section.
- [The game link's shape](issues/02-game-link-shape.md): `regia.GameLink`, a JaCaMo `platform:` wrapping one `WsClient`, up before any agent and outliving the Root, on `base_port`, named `regia_game_link` in the envelope. No Director has a body. Java holds plumbing only, never game information. A failed link lets the run go on (`no game link`, `T2802`/`T2803`). ADR 0040.
- [A Director hearing the game for itself](issues/03-hearing-the-game.md): `regia_hears` covers the own Plot only. On attach the link asks the game (`regia_state`) for the Director's starting Facts and which of its cast have left, and delivers it nothing until the reply. Intake is in Java, and percept forwarding and the snapshot are gone. An ending Director stops hearing at step 1 but stays attached until its kill. No joins before the first reply (`T3305`).
- [A Director doing its own Actions](issues/04-doing-its-own-actions.md): every Director, the Root included, sends its own Actions on the link. Ids come from the link's one counter and replies go by id into the requester's mailbox, so a `DO` in `EXITED` wakes inside the transition. Cancels go on the link (ADR 0038 unchanged). A detaching Director's waiting Actions are called off, its `WITHOUT WAITING` outcomes are traced by the link, and a lost link fails every in-flight Action. The relay is gone, and the Root ends the story with `regia.end_story`. Chapters 37, 30, 31 and 28 were edited.
- [ScriptedGame and the Trace on the game link](issues/06-scripted-game-and-the-trace.md): `ScriptedGame` tells the link from bodies by port. `director:` steps become `link` steps, and `*` reaches the link last. `T2801` is now Agents only. Held Actions match without sender. `> lose link` and `#! game link: none` script `T2803`/`T2802`. `ScriptedGame` answers `regia_state` from link Facts and leaves, with `> fact link` before `> start` as the starting state. No new codes. Chapters 34, 35, 37, 28 and 30 were edited.

## Not yet specified

Nothing left: the way to the destination is clear.

## Out of scope

- Agents' bodies: every Agent keeps its own VEsNA connection and sends its own Actions. Subplot–cast messaging is audited (in *Messages for the whole run*), not redesigned.
- Writing `regia-jason`: implementation work.
- A body per Director, with the game learning about Stagings: rejected by the user when charting.
- The showcase's reference Build (`docs/showcase/jason/`) following chapters 28, 30, 31, 33, 34, 35 and 37 as edited here. That's the showcase map's work, which this map now unblocks. *ScriptedGame and the Trace on the game link* needed nothing extra for it.
