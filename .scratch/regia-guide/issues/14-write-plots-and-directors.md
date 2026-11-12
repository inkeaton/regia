# Write: Plots and Directors

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Task

Write `docs/guide/11 - Plots and Directors.md`.

Covers: Plot Roles, Phases and `INITIAL`, `DURING`, transitions, the Director and its Statements (`ASSIGN`, `UNASSIGN`, `TRANSITION`, `END PLOT`), Role setup with `STARTS WITH`, the Root Plot.

Sources: 16, 20; ADR 0009.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-12: [`docs/guide/11 - Plots and Directors.md`](../../../docs/guide/11%20-%20Plots%20and%20Directors.md), about 4,850 words counting snippets, tables and the diagram, over ten sections (a Plot, Roles of a Plot, Role setup, Phases, entering and leaving a Phase, `DURING PLOT`, what a Director knows, Director Statements, ending a Plot, the Root Plot). The longest chapter so far: the ticket covers Role setup, Phases and the Root Plot next to the Director itself. Givings, Mappings and `UNASSIGN` are left to *Playbooks and Roles*, a Director's `TELL` and `ASK` to *Messages*. Not yet read by the user.

Checked by hand against spec chapters 10, 13, 15, 16, 17, 18, 19, 20, 21 and 30, ADR 0009 and primer chapter 5 (for *Since 1.0*).

Showcase: `feast` in `RoyalBanquet` got a `WHEN EXITED: DO clear_tables.` Plan, and the Vocabulary the Action `clear_tables`, since no Plot had an `EXITED` Plan. No existing line changed, so cuts quoted by other chapters still hold.

Fifteen `#revise`, six of them carried over from the README's notes (naming an Agent of the Cast, setups running before the first Phase, the unheard `insult_thrown`, the Root Plot and the latecomer, the `RANDOM` in a setup by pointer to *Randomness*, `PURSUE` by pointer to *Goals and Failure*). New here:

- `LEARN` in a setup, `TELL` in a Director's Plan and `LEARN` in a Director's Plan: two spellings of one thing and one spelling of two.
- A setup is the same for every Agent and Instancing gives only Propensity values, so no starting Fact differs per Agent except by a roll.
- No way to say "everyone in the Plot": `ASSIGN Courtesy, …` is written four times.
- Which Phase follows which is written nowhere in one piece.
- A Phase's timeout is the tail of its entry Plan.
- `WAIT` is an error in `EXITED`, but a `DO` there waits for the game and holds the Plot between Phases.
- `EXITED` doesn't know where the Plot goes, nor `ENTERED` where it came from.
- A Phase's Plan replaces `DURING PLOT`'s on the same Trigger and can't add to it.
- No condition asks which Phase the Plot is in; a `TRANSITION` from `DURING PLOT` can re-enter the current one.
- The Director's Facts about its Agents are a hand-kept copy (a `wager` of a Spectator who left).
- A `GOAL` declared in a Plot can't be used by anything.

Three *Spec wording* entries and one *Gaps in the showcase* entry were added to the showcase README.
