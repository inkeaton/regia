# Directors share one game link that holds only plumbing

In the Jason Target, only the Root Director had a connection to the game. It forwarded game percepts down the Staging tree, kept the game Facts its descendants needed, relayed every Subplot Director's Actions and answered for them while it ended. So a Director's ASL ran, and kept state, on behalf of other Stagings.

We decided that every Director, the Root included, attaches to **one game link** for the whole run: `regia.GameLink` in `regia-jason`, wrapping one VEsNA `WsClient`, started as a JaCaMo `platform:` before any agent and living as long as the MAS. It delivers each game message straight into the mailbox of each Director that should have it, and Directors send to the game through it. No Director has a body. The game stays unaware of Stagings: it sees one party, `regia_game_link`, on one port, `base_port`.

The link holds **only plumbing**: the connection, who is attached and what each hears, Actions in flight, and the clock. Game information lives in the game or in agents' beliefs, never in Java, and what the link needs to know about the Program it reads from Jason when it needs it. This loosens chapter 28's "no state on the Java side" to "no Regia state on the Java side". If the link can't connect or loses its connection, the run goes on without the game.

## Considered options

- **Keep the Root as the gateway**: the Root's ASL ran relay plans and kept Facts for other Stagings, and had to stay up while ending to answer them.
- **A Jason `Environment`**: JaCaMo 1.2 never creates one and sends every action to CArtAgO; its percepts are beliefs, so it can't carry a momentary Cue.
- **A body per Director**: the game would have to learn about Stagings and Directors spawned at runtime.
- **The link owned by the Root Director**: it would die with the Root, and the link must keep killing leavers and running the clock after the story ends.

## Consequences

- The Root Director's `.jcm` entry has no `address` or `port`; the `.jcm` gains a `platform:` line; `cast.json` names the link instead of the Root.
- Percept forwarding, the start snapshot of game Facts and the Root's Action relay are replaced by each Director hearing and acting for itself (tickets *A Director hearing the game for itself* and *A Director doing its own Actions*). A Subplot that attaches late can't get its starting Facts from a cache in the link, so the link asks the game for them (`regia_state`, chapter 37).
- In Regia 1.5.
