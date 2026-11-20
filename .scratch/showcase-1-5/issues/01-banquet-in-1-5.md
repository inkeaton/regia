# The banquet in 1.5

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

How does the royal banquet of the old showcase (`docs/guide/showcase/README.md`) become a world written in Regia 1.5?

Decide:

- How `arrival` and `feast` end without Quota Triggers: the Director's own records, compared with `COUNT(? PLAYS Guest)`, or something else the story wants.
- What replaces Wagering's counted Signals (`3 OF Spectator`, `SENT`) and the `HIGHEST` wager Pick that read them.
- What replaces hearing how an asked Goal ended (`BY`), wherever the old Program listened for it.
- The `latecomer` kind and the two `JOINED` Plans: removed, and what (if anything) the farewell and the abandoned duel keep of cast changes (`LEFT`, `EMPTIED`).
- The dotted External names that break `R2801`, and `hall.guards.seize`.
- The world's faults in *Review notes* and *Gaps in the showcase*: the Defender who never stands, the double `duel_won`, the fight that never waits for the handkerchief, the `IF hungry` case undercut by `DROP have_dinner`.
- Plots, Phases, Roles, Playbooks and Agent kinds as a list, so that the coverage ticket can map onto them.

## Resolution

Resolved on 2026-11-18, with the user. Facts found first: `R2801` is retired (chapter 28), so dotted Fact and Cue External names are fine; and the old Program never used `BY`, so every "done" was already a hand-written Signal.

**Endings without Quotas.** `arrival` and `feast` count by hand: the Director learns `seated(?g)` on `took_seat FROM Guest ?g` and `finished(?g)` on `finished_eating`, and compares `COUNT` over them with `COUNT(? PLAYS Guest)`. `arrival` waits for all of them, `feast` for 75% (`COUNT(finished(?)) * 4 >= COUNT(? PLAYS Guest) * 3`). The check is repeated in a `WHEN Guest ?g LEFT` Plan, which also forgets the leaver's Facts: a departure sends no Signal. The repetition is what the "In 2.0" note points at.

**Wagering.** `wagered(?stake)` and `LEARN wager(?who, ?stake)` stay. The `cheered` Quota and the bare `cheered` Signal go (`DO cheer` stays). `challenge` closes betting with `AFTER 20 SECONDS`, picks `HIGHEST ?stake, AT RANDOM` and asks the backer to `give_signal`; the backer Signals `handkerchief_dropped`, and only that transitions to `fighting`. With no wager, the `ELSE` transitions at once.

**Done-Signals.** Written once per Goal in an `ENDED` Plan of the Playbook that pursues it (`WHEN take_seat ENDED: SIGNAL took_seat.`, `WHEN have_dinner ENDED: SIGNAL finished_eating.`), never at the end of a recipe. Specific endings (`take_seat FAILED` → `stand_by(wall)`) do their own work and leave the Signal to `ENDED`. Each gets an "In 2.0" note: the Director would hear `ENDED BY`. Checked: chapter 05 makes a Goal asked by a Director the pursuer's own Pursuit.

**Joining and leaving.** `latecomer`, both `JOINED` Plans and `guest_arrived` are removed. `farewell` ends on `Guest EMPTIED`, the walked-out Defender ends the duel through `Defender EMPTIED`, and the `LEFT` Plans above close the old "no `LEFT` Plan" gap.

**Names.** The five dotted Fact and Cue names stay, declared `GAME FACT` / `GAME CUE`. `seize(person)` becomes a plain game Action. Whether the showcase has one real dotted Action (Target code) is ticket 02's.

**Faults of the world.**

- The Defender does `DO stand_up` before `pick_up_glove` when accepting.
- The double `duel_won`: a yielding duellist forgets its `stamina`; the lunge Plan, chosen `GIVEN stamina(?)`, re-checks `IF stamina(?):` after its `WAIT`. This is the showcase's `GIVEN` versus `IF` case.
- `Dining` keeps `WHEN hungry FORGOTTEN: DROP have_dinner.` and loses `IF hungry … ELSE push_away`.
- The handkerchief: fixed by the wagering above.
- Unreached Plans (`resent`, gossip, scowl, a finished dinner): the test casts must reach them; how many runs is ticket 04's.

**Review notes answered by the revision.** The victim tells gossip about itself apart with `ME`; Spectators are `Guest EXCEPT` both duellists (exact form checked when writing); `HonorDuel(offender)` with `GIVEN NOT HonorDuel(?offender) RUNNING`, so one duel per offender and two Stagings can still run; `Dining` reacts to hunger with `WHEN ASSIGNED`, and the Director's `ASK Guest TO have_dinner` goes; `Duelling` tidies `stamina` with `WHEN UNASSIGNED`; `MAPPING Host TO host` goes (same names bind ignoring case); `SELF OVER Poisoning ON scandal` goes (ADR 0032). Kept: the winner names itself with `duel_won`, an insult outside `feast` shows in the Trace as `unheard`, `purse(RANDOM(5, 20))` rolled per Agent.

**The world.**

Plots:

- `RoyalBanquet` (Root). Roles `Host`, `Guest`, `Servant`, `Guard`. `CAST STARTS WITH: ASSIGN Courtesy.`; Role setups keep what differs (`take_seat`, `purse`, `craves`, `Hosting`, `Keeping_watch`, `on_duty`). Phases: `arrival` (hand count of `seated`, also on `LEFT`), `reception` (`ASSIGN NobleSocializing`, toast), `feast` (`Dining` and `Serving` as Phase setups, `UNTIL EXITED`; `Poisoning`; duels; 75% hand count of `finished`; `WHEN EXITED: DO clear_tables`), `farewell` (`UNASSIGN NobleSocializing`, `take_leave`, ends on `Guest EMPTIED`). `DURING PLOT`: Subplot endings, `Host EMPTIED`. Precedence: `Keeping_watch OVER NobleSocializing ON scandal`, `HonorDuel OVER Poisoning`.
- `HonorDuel(offender)`. Roles `Challenger`, `Defender`, `Spectator` (`Guest EXCEPT` the duellists). Phases `challenge` (wagers, `AFTER 20 SECONDS`, `handkerchief_dropped`) and `fighting` (`duel_won FROM ?winner`, the two-minute timeout as `AFTER` ending with `duel_abandoned`). `Challenger`/`Defender EMPTIED` end it abandoned. `PARENT OVER SELF ON scandal`.
- `Poisoning`. No Phases. `1 OF Guest` → `Poisoner`, `Guard` → `Watchman`.

Playbooks (9): `Courtesy`, `Hosting` (new: `open_feast`, `honour`, from `Host`'s setup), `NobleSocializing`, `Dining`, `Serving`, `Keeping_watch`, `Duelling`, `Wagering`, `Scheming`, changed as above.

Agent kinds: `king` (Host), `noble`, `hothead` (Guest), `knight` (Guest and Guard), `servant` (Servant).

Instancing: `banquet.regin` for the full cast; the test casts are ticket 04's.

Vocabulary: `EVENT` → `CUE`; `GAME FACT`/`GAME CUE` on the five dotted names; `seize(person)` plain; new Cue `handkerchief_dropped`; `cheered` (as a Cue) and `guest_arrived` removed; Director Facts `seated(person)`, `finished(person)`, `wager(person, stake)`.

Changed: nothing in the spec, ADRs or glossary. Handed on: the dotted Action to *What the showcase must show*; the casts that reach every Plan to *The walkthrough's shape*.
