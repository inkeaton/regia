# A Director doing its own Actions

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 02

## Question

How a Director's `DO` reaches the game through the game link, replacing chapter 37's *Custom Actions in a Director* and the Root's relay (`regia_act`, `regia_relay`, `regia_act_result`, `regia_act_cancel`).

Decide:

- how `regia.act` sends an Action on the link and how the game's replies find the requesting Director (chapter 37's `id`s, now per link and not per body);
- how a Director's `DO` inside an atomic `EXITED` Plan wakes (chapter 30, *A `DO` in `EXITED`*), now that no `tell` from the Root resumes it;
- a stopped Plan calling off its Action (ADR 0038), and a Director that ends or is killed with an Action pending: who sends the cancel, and what happens to a late reply;
- what goes away: the relay plans, their Phase-guard exception while the Root ends, and the `regia.send` catch for a relayed reply.

Closes when chapters 30, 31 and 37 are edited.

## Comments

**From *The game link's shape* (2026-11-19).** The link sends every Director's Action with `sender: "regia_game_link"`, so the game never sees which Director acted; replies must be routed back by `id`, which is per link. While the link isn't connected, a Director's Action fails at once with the reason `no game link` (chapter 37, *No body, no Action*). Pending Action ids are plumbing and may live in the link's Java state (chapter 28, *Infrastructure state*).

**From *A Director hearing the game for itself* (2026-11-19).** The link now sends `regia_state` requests under an `id` from its own counter (chapter 37, *The game's starting state*). Decide whether Action `id`s share that counter. Also, an ending Director stops hearing at step 1 but stays attached until its kill, so the link still knows it while its `EXITED BY PARENT` Actions are pending.

## Resolution (2026-11-19)

Every Director sends its own Actions through the game link, the Root included; nothing passes through another Director.

- **Ids.** One counter on the link for everything it sends (`regia_state` and Actions), so ids are unique on the connection. The link records each id against the requesting Director and routes replies by id alone. Agents keep per-body counters.
- **Replies.** Delivered into the requesting Director's mailbox (`receiveMsg`), so a reply keeps socket order with Facts and Cues. `regia.DirectorAgent`'s Java intake resumes `regia.act` (shared code with `myHandleMsg`). A suspended atomic intention still wakes on a message (`TransitionSystem.java:1620`), so a `DO` in `EXITED` wakes inside the transition. `regia.stop_hearing` stops Facts and Cues only; Action replies still arrive until detach. Rejected: resuming straight from the socket thread (could overtake an earlier Fact).
- **Calling off.** The same circumstance listener as an Agent; `regia.act` asks the link to send `regia_action_cancel`, and the link forgets the id (late reply dropped silently). ADR 0038 unchanged.
- **Detach with Actions in flight.** A normal walk can't reach its kill with a waiting `DO`. If a Director dies otherwise, its detach makes the link call off its waiting Actions (cancel + `CANCELLED`). `WITHOUT WAITING` ids stay until their final reply; the link writes the outcome entry under the Director's name and never delivers it (Jason reuses agent names).
- **Lost link.** Every in-flight Director Action gets a final `failed` with `no game link`, so an atomic `EXITED` never hangs on a dead link. The same gap for Agents' bodies is noted in chapter 37's *Not decided here* (out of this map's scope).
- **Gone.** The relay plans, `regia_act`/`regia_act_result`/`regia_act_cancel`, `regia_relay`, chapter 31's unguarded-relay exception and the `regia.send` catch for relayed replies. The end of the story is sent by the Root at step 5 with the internal action `regia.end_story(Outcome)`.

Edited: chapter 37 (*Custom Actions in a Director* rewritten, *Sending*, *Waiting*, *A Plan that stops while waiting*, the game link section, *The end of the story*, *The Trace*, *Infrastructure state*, additions, *Not decided here*); chapter 30 (*A `DO` in `EXITED`*, *Custom Actions in a Director*, additions); chapter 31 (step 5, *A child ended by its parent*, *An ending Director hears nothing*); chapter 28 (*The game link*, *Acting*); ADR 0038's consequence line.
