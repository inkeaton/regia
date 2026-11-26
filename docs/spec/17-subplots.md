# Subplots and Stagings

How a Plot starts another Plot as its Subplot, how the Subplot's Roles are cast, how parent and child end and hear about each other, and how several Stagings of one Plot live side by side. Decided in the ticket *Subplots and Stagings* (`.scratch/regia-2/issues/18-subplots-and-stagings.md`). It builds on chapters 05, 07, 08, 11, 13, 15 and 16, and answers the "how should parents and children cooperate" and "alert parent and children plots" notes in primer ch.5. The condition `RUNNING`, the `DROPPED` form, and a parent hearing an ending it caused were decided in the ticket *What a Director knows about itself, and how a Subplot's ending is heard* (`.scratch/regia-revision/issues/09-director-state-and-endings.md`), with ADR 0030. `FINISHED` for an ending the Subplot chose itself, and `DROP SUBPLOT` for `END SUBPLOT`, were decided in the ticket *Endings and kind words* (`.scratch/syntax-review/issues/10-endings-and-kind-words.md`), with ADR 0047.

## Starting a Subplot

```regia
PLOT RoyalBanquet:
    ROLE Host
    ROLE Guest
    PHASE reception INITIAL
    PHASE duel_interruption
    ...
    DURING duel_interruption:
        WHEN insult_heard:
            START SUBPLOT HonorDuel, MAPPING 1 OF Guest AS Challenger, MAPPING 1 OF Guest AS Defender, MAPPING Guest AS Spectator
```

- `START SUBPLOT <Plot>` followed by `MAPPING` clauses, with the form, implicit same-name Mappings, errors and counted picks of chapter 15.
- **It never waits.** The parent's Body carries on at once, like `ASK` (chapter 08). The Subplot starts in its own time: it casts its Roles, runs their Role setups (chapter 16), then the initial Phase's entry Plans. The parent learns how it went only through `WHEN … FINISHED`, `DROPPED` and `ENDED` (below).
- **Every `START SUBPLOT` makes a new Staging**, even if a Staging of the same Plot started by this parent is still running, with the same arguments or not. Two insults, two duels. A parent that wants one at a time asks first with `RUNNING` (*Running Stagings*, below).

### Plot parameters

A Plot may take parameters, written after its name as a Goal's are (chapter 03), and the `START SUBPLOT` passes their arguments (ADR 0028):

```regia
PLOT HonorDuel(quarrel):
    ROLE Challenger
    ROLE Defender
    ROLE Challenger:
        LEARN grievance(?quarrel)
    ...

# in RoyalBanquet
WHEN insult_thrown(?insult), FROM Guest ?offended:
    START SUBPLOT HonorDuel(?insult), MAPPING ?offended AS Challenger, …
```

- **A parameter is a Placeholder filled in every Block of the Plot**: its Role setups (the one Placeholder a setup may use, chapter 16), `DURING PLOT` and every Phase. `quarrel` is read as `?quarrel`. It is fixed for the Staging: a Plan can't fill it again, and a Trigger that names it tests it, as any filled Placeholder (chapter 03).
- **The arguments must be filled** when `START SUBPLOT` runs: Values or filled Placeholders, as for `END PLOT WITH`. An Agent is allowed, and the Subplot can send it Messages and test it with `PLAYS`. A Role is not a Value and can't be an argument (ADR 0023).
- **A Plot has one parameter count** (ADR 0006). A Plot with parameters is always written with them in `START SUBPLOT`, its ending Triggers and `DROP SUBPLOT`, with `?` where any value will do. A Plot without parameters is written bare. `PRECEDENCE` names the Plot bare either way: it ranks the Plot, and all its Stagings share that rank (*Precedence*, below).
- **The Root Plot takes none.** Instancing starts it with nothing to pass (chapter 21, `R2114`).
- The parameters are part of the Plot's Interface, and are declared, not inferred: the header says them (chapter 38).

### Casting

A Subplot's Roles are **played**, unlike a Playbook's Roles, which are only addresses (chapter 15). Its Agents get Role setups and Givings and are reached by its Director's Statements. So a Subplot's Roles are **cast when it starts**:

- A whole-Role Mapping (`MAPPING Guest AS Spectator`) casts everyone playing the parent's `Guest` in the parent's Staging **when `START SUBPLOT` runs**. An Agent who starts playing `Guest` later does not become a Spectator. **This is a copy, unlike the same clause on `ASSIGN`**: `ASSIGN Dining TO Guest, MAPPING Servant AS waiter` binds `waiter` to the Servants live, so a new Servant is a `waiter` at once (chapter 15). A Subplot's Roles are played, so who plays them is fixed at its start; a Playbook's Roles are addresses, looked up when used.
- "Everyone else" is written with `EXCEPT`, and the whole parent Cast with `CAST` (chapter 15): `MAPPING CAST EXCEPT Duellist AS Spectator`. Both are read when `START SUBPLOT` runs, like any whole-Role Mapping here.
- Inside the Subplot, `CAST` is the Subplot's own Cast.
- A counted pick (`1 OF Guest`) works as in chapter 15: once, at random, no Agent twice in one Statement.
- Role setups run for this cast, per chapter 16.
- **A Role that starts empty fires `EMPTIED`**, after the setups and before the initial Phase's entry Plans, in Role declaration order, `CAST` last (chapter 19). It happens when the parent's Role was empty at that moment, or a counted pick found nobody. The Subplot's `EMPTIED` Plan handles it as it handles the last Agent leaving: a duel with no Defender ends itself instead of waiting.
- Agents joining the parent's Role **don't** carry through to a running Subplot. An Agent leaving the Program leaves every Staging, the Subplot's included, and its Director hears `LEFT`/`EMPTIED` (chapter 19).
- **A Plot doesn't say whether it is the Root Plot.** It is written the same either way, and Instancing names the Root, never infers it (chapter 21, ADR 0036). A `JOINED` Plan in a Plot that is never the Root can't fire, and is a warning (`R1905`, chapter 19).

### Being in both

An Agent cast into a Subplot **keeps** its Roles and Givings in the parent. It now plays Roles in two Stagings.

- A `SIGNAL` in a Playbook the Subplot gave reaches the Subplot's Director, since it is the one giving that Playbook (chapter 07). A Signal in a Playbook the parent gave reaches the parent's Director, as before.
- In the parent, `FROM Guest` still means the parent's own `Guest` in its own Staging. A parent never sees its Subplots' Roles.
- **Being cast in a Subplot adds and never takes away.** A Challenger still holds `Dining`. Precedence decides the Triggers both Playbooks have a Plan for (chapter 13). A parent that wants the duellists out of the dinner takes it from them and gives it back itself: `REMOVE Dining FROM Guest ?offended` before the `START SUBPLOT`, `ASSIGN Dining TO Guest ?a` in the `ENDED` Plan, with the duellists passed as arguments (chapter 15). That Plan runs however the duel ended, the parent's own `DROP SUBPLOT` included (*The parent's Triggers*, below), so the giving back is written once. Pausing a Playbook while a Subplot runs is not in 2.0.

### An Agent in two Stagings of one Plot

An Agent may play Roles in two running Stagings of the same Plot: Ada fighting two duels, or watching both. The language allows it. Whether it makes sense is a question of the game being designed, and guarding against it is the writer's: with the Plot's arguments, Facts of the parent's own, and `RUNNING` (below): `GIVEN NOT HonorDuel(?) RUNNING` allows one duel at a time.

What follows from it is the writer's to know, because a Plan doesn't know which Giving it runs for (chapter 15, *Not in 2.0*):

- A Playbook given by both Stagings is held twice and runs **one** set of Plans. A Playbook Role is the union of both bindings: Ada's `opponent` is both opponents, and `TELL opponent hit` strikes both.
- A `SIGNAL` reaches **both** Directors, whichever Director's Message started the Plan: a Spectator's `cheered` counts in both duels, and Ada's `duel_won` reaches both.

The Trace marks the Staging's start when an Agent of its Cast already plays in another running Staging of the same Plot (chapter 34). It is not a warning.

## Stagings

A **Staging** is one running copy of a Plot (glossary). Stagings have **no names in the language**. Each Staging knows its parent (if it is a Subplot) and the Subplots it started. Everything a Director writes is about its own Staging: its Roles, its Phase, its Givings, its Subplots.

- **A parent tells its Subplots' Stagings apart by their arguments**, matched as a Goal's are: `WHEN HonorDuel(?q) ENDED` says which quarrel ended, and `DROP SUBPLOT HonorDuel(?q)` ends only the Stagings whose arguments match (below). Two Stagings with the same arguments are told apart by nothing, and a Statement that matches one matches both.
- Telling Stagings apart at runtime belongs to the Target. In Jason, a Staging is identified by its Director agent's name (chapter 31).

### Running Stagings

`<Plot> RUNNING` is a condition: it holds while a Staging of that Plot that **this Staging started** is running. A Plot with parameters is written with them, matched as in its ending Triggers, filling Placeholders or testing filled ones:

```regia
WHEN insult_thrown(?insult), FROM Guest ?offended:
    GIVEN NOT HonorDuel(?) RUNNING:            # one duel at a time
        START SUBPLOT HonorDuel(?insult), MAPPING ?offended AS Challenger, …

WHEN guards_arrived:
    GIVEN COUNT(HonorDuel(?) RUNNING) > 1:
        DO ring_bell
```

- It is written wherever a condition goes: a Context, an `IF`, under `NOT`, inside `COUNT(…)`, with Picks and `FOR EACH` (chapter 26). Its Matches are distinct, as every condition's are (chapter 26): one per distinct set of arguments, not one per Staging. Two duels over the same quarrel are one Match, so `COUNT(HonorDuel(?) RUNNING)` counts the quarrels being fought, and `COUNT(Poisoning RUNNING)`, with no blanks, is 1 or 0. This is the same limit as everywhere else: Stagings with the same arguments can't be told apart (*Stagings*, above).
- A Staging is running from its `START SUBPLOT` until it ends: by itself, from above, or with its parent. It no longer counts **before** its ending is heard, so a `WHEN HonorDuel ENDED` Plan already sees it gone.
- Only the Stagings this Staging started. A Subplot can't ask about its parent, its siblings, or Stagings its own Subplots started.
- Naming a Plot this Plot never starts is an error (`R1704`), as for `DROP SUBPLOT`. `RUNNING` is for Directors only; in a Playbook it is an error (`R1714`).

## A Subplot outlives its Phase

A Subplot belongs to the parent's **Staging**, not to the Phase that started it. When RoyalBanquet moves from `duel_interruption` to `feast`, HonorDuel keeps running. It stops only when it ends itself, when the parent drops it with `DROP SUBPLOT`, or when the parent ends.

A Subplot meant to last a Phase says so where it is started: `START SUBPLOT HonorDuel, …, UNTIL EXITED` in a Plan of that Phase. It is then ended when the Phase is left, as by `DROP SUBPLOT` (chapter 15), and the parent hears it as `DROPPED` (below). The Phase that started it has been left by then, so its Plans can't hear it: the ending is heard by the new Phase's Plan, else by `DURING PLOT`. A `DROPPED` or `ENDED` Plan for it written only in the Phase that started it is a warning (`R1713`).

## Ending

### `END PLOT`

`END PLOT` ends the Staging it runs in.

- **It stops its Body.** A Statement after it in the same branch is an unreachable-code error.
- **Its Subplots end too**, all the way down, children before parents. Each ending Staging's Givings are taken away (chapter 16's table: running Plans stop, local Goals are dropped, Facts stay).
- **It tells the parent**, if the Staging is a Subplot: the parent's `WHEN <Plot> FINISHED` fires, then `WHEN <Plot> ENDED`. A Subplot ended because its parent is ending tells nobody: the parent is going too.

### Outcomes: `END PLOT WITH`

A Subplot can end with an **Outcome**, one Cue handed to the parent:

```regia
PLOT HonorDuel:
    ROLE Challenger
    ROLE Defender
    ...
    DURING fighting:
        WHEN yielded, FROM Defender:
            END PLOT WITH duel_settled(?winner)    # ?winner filled earlier in the Plan
```

- `END PLOT WITH <event>` takes exactly one Cue declared in the Vocabulary. Different endings use different Cues (`duel_settled`, `duel_abandoned`).
- Its arguments must be filled: Values or filled Placeholders, as for any Action (chapter 08). An Agent is allowed (`?winner`); the parent's Director can send it Messages, give it Playbooks and map it onto Roles (chapter 20).
- The child declares no list of its endings: they are part of its Interface, worked out by the Transpiler (chapter 38). The Transpiler warns when a parent matches an Outcome the child never ends with, and when the child has an ending that no Plan of the parent hears (`R1706`, `R1708`).
- A local Cue of a Playbook can't be an Outcome: a Plot can't see it (`R1004`, chapter 10).
- A plain `END PLOT` ends with no Outcome. In a Plot that isn't a Subplot, `WITH` has no one to tell and is ignored with a warning.

### The parent's Triggers: `FINISHED`, `DROPPED`, `ENDED`

A Subplot's endings are heard the way a Goal's are (chapter 05, ADR 0030, ADR 0047): a **specific** Trigger for how it ended, **then** plain `ENDED` for every ending.

```regia
DURING PLOT:
    WHEN HonorDuel(?q) FINISHED WITH duel_settled(?w):   # it ended itself, with this Outcome
        ASK Host TO honour(?w)
    WHEN HonorDuel(?q) FINISHED:                         # it ended itself any other way
        TELL Guest duel_abandoned(?q)
    WHEN HonorDuel(?q) DROPPED:                          # this Staging ended it (DROP SUBPLOT, UNTIL EXITED)
        TELL Guest duel_stopped(?q)
    WHEN HonorDuel(?q) ENDED:                            # every ending, after the specific one
        DO play_music
```

| Trigger | Fires when the Subplot |
|---|---|
| `WHEN P FINISHED WITH e` | ended itself with `END PLOT WITH e` |
| `WHEN P FINISHED` | ended itself, with an Outcome no `FINISHED WITH` Plan above it matched, or with a bare `END PLOT` |
| `WHEN P DROPPED` | was ended by this Staging: `DROP SUBPLOT`, or `UNTIL EXITED` when the Phase was left |
| `WHEN P ENDED` | ended in any of these ways, **after** the specific Trigger's Plan |

- These are Trigger kinds for Directors, past tense like `LEARNED`, `FORGOTTEN`, `DROPPED`, `FAILED` (chapter 05). A name has one kind in the Program (ADR 0006), so no `SUBPLOT` word is needed, and `DROPPED` or `ENDED` after a Goal's name is the Goal's ending (chapters 05, 20).
- **The words are shared with Goals, each with one meaning** (chapter 01, ADR 0047). `FINISHED` is the Subplot's own word for "ended by itself", as `REACHED` and `FAILED` are a Goal's: a Subplot has no success or failure, and its Outcome says how it went. `DROPPED` is "stopped on purpose by whoever started it", for a Goal and a Subplot alike. `ENDED` is "over, however it went", never takes a complement, and always fires after the specific Trigger.
- A Plot with parameters is written with them: `WHEN HonorDuel(?q) FINISHED WITH duel_settled(?w):`. The arguments are matched as a Trigger's always are, filling Placeholders or testing filled ones, so the Plan knows which Staging ended.
- **`WITH <event>` after `FINISHED` matches an Outcome**, filling Placeholders as any Trigger does (chapter 03), as `WITH` after `FAILED` matches a Reason (chapter 11).
- **One Trigger, first match wins.** The `FINISHED` Plans of one Phase (or of `DURING PLOT`), with and without `WITH`, share a Trigger and are tried in written order; the first that matches runs, as for `FAILED` (chapter 11). A plain `FINISHED` matches every ending the Subplot chose itself, with an Outcome or without, so it goes last: written above a `FINISHED WITH` Plan it also matches, it shadows it, with a warning (`R1716`). A bare `END PLOT` is heard only by a plain `FINISHED`.
- **The specific Trigger fires first, then `ENDED`.** A Plan for each runs, in that order, as for a Goal's `REACHED` and `ENDED` (chapter 05). Tidying shared by every ending goes in the plain `ENDED` Plan, once. A specific Trigger with no Plan doesn't stop `ENDED` from firing.
- They fire **once per Staging** that ends.
- They are heard like any Director Trigger: the current Phase's Plan, else the `DURING PLOT` Plan, with the precedence of chapter 13.
- **An ending the Subplot chose itself, that neither a `FINISHED` Plan nor `ENDED` has a Plan for, is ignored, and the Trace says so** (`T3802`, chapter 38). A `DROPPED` ending with no Plan is silent: the parent caused it.
- **A Subplot that ends because its parent is ending reports nothing**: the parent is going too.
- `WHEN P FINISHED`, `WHEN P DROPPED` or `WHEN P ENDED` in a Plot that never starts `P` is a compile-time error (`R1704`). `WHEN P DROPPED` in a Plot that starts `P` but never ends it from above, with no `DROP SUBPLOT P` and no `UNTIL EXITED` on a `START SUBPLOT P`, can never fire, and is an error (`R1712`).
- The retired spellings `WHEN P ENDED WITH e:` and `WHEN P ENDED WITHOUT OUTCOME:` are an error with a hint (`R1715`): `FINISHED WITH e`, and a plain `FINISHED` written after the `FINISHED WITH` Plans. `ENDED` with any complement is the same error.

Waiting for a Subplot in the Plan that started it (`START SUBPLOT …` and then the next line) is not in 2.0: a Director's Plan has nothing to wait on, as it has no Goals (chapter 20, *Handed off*). What follows a Subplot is written in these Plans, which know the Staging by its arguments.

### `DROP SUBPLOT`

```regia
DURING PLOT:
    WHEN guards_arrived:
        DROP SUBPLOT HonorDuel
```

- `DROP SUBPLOT <Plot>` ends **every** running Staging of that Plot started by this Staging, each with its own Subplots (as for `END PLOT`). It is the opposite of `START SUBPLOT`, and is worded like the Trigger it fires, as `DROP g` fires `DROPPED` (chapter 08).
- For a Plot with parameters, it ends every such Staging **whose arguments match**: `DROP SUBPLOT HonorDuel(?q)` with `?q` filled ends the duels over that quarrel, `DROP SUBPLOT HonorDuel(?)` ends them all. An unfilled Placeholder matches anything, as `?` does.
- **The parent hears it**: `WHEN HonorDuel DROPPED`, then `WHEN HonorDuel ENDED`, once per Staging ended, with its arguments (above). The Plans run **after** the Body that ran `DROP SUBPLOT`, like any Trigger's: a Statement written after `DROP SUBPLOT` runs before them.
- It doesn't stop the Body.
- With no such Staging running, it does nothing, without a warning, like the other no-ops (chapter 08).
- Naming a Plot this Plot never starts is a compile-time error (`R1704`).
- `SUBPLOT` is required: `DROP HonorDuel` is an error whose hint gives `DROP SUBPLOT HonorDuel` (`R0802`, chapter 08). The retired spelling `END SUBPLOT <Plot>` is an error with the same hint (`R1717`). `END` is left only in `END PLOT`, a Staging's own ending.

## Precedence

Spec 13 ranks a Subplot by its position under its parent. Nothing new is needed:

- Two Stagings of one Subplot under the same parent share that position and tie. They are one Plot with one set of Playbooks.
- A Plot started from two different parents has a position under each. An Agent holding Givings from both keeps the better rank, as spec 13 says of a Playbook given twice.
- The rank key's encoding: chapter 32 (`32-jason-precedence.md`). A Staging gets its place from its parent in `regia_start`.

## No cycles

A Plot may not start itself, directly or through other Plots (A starts B starts A). A cycle in the graph of `START SUBPLOT` Statements is a **compile-time error**: the Plot's Playbooks would rank both above and below themselves (chapter 13). Recursion may be allowed later; it is easier to add than to take away.

## Transpiler checks

**Errors**

- `R1701` A cycle among `START SUBPLOT` Statements (the message names the cycle).
- `R1702` A Statement after `END PLOT` in the same branch.
- `R1703` `END PLOT WITH` something other than one declared Cue, or with unfilled arguments.
- `R1704` `WHEN P FINISHED` (any form), `WHEN P DROPPED`, `WHEN P ENDED`, `DROP SUBPLOT P` or `P RUNNING` where this Plot never starts `P`. Absence check (chapter 23).
- `R1709` A Plot written with the wrong number of arguments: a Plot with parameters written bare, or one without written with arguments, in `START SUBPLOT`, `WHEN … FINISHED`, `WHEN … DROPPED`, `WHEN … ENDED`, `DROP SUBPLOT` or `RUNNING`; or a Plot written with arguments in `PRECEDENCE`.
- `R1710` A `START SUBPLOT` argument that isn't filled, or is a Role.
- `R1711` A Plan that fills a Plot parameter again (`LET ?quarrel BE …`), or two parameters of one Plot with the same name.
- `R1712` `WHEN P DROPPED` in a Plot that never ends `P` from above: no `DROP SUBPLOT P`, and no `UNTIL EXITED` on a `START SUBPLOT P`. Absence check (chapter 23).
- `R1714` `RUNNING` in a Playbook.
- `R1715` The retired `WHEN P ENDED WITH e:` or `WHEN P ENDED WITHOUT OUTCOME:`, or `ENDED` with any other complement (hint: `FINISHED WITH e`, or a plain `FINISHED` after the `FINISHED WITH` Plans).
- `R1717` The retired `END SUBPLOT P` (hint: `DROP SUBPLOT P`).

**Warnings**

- `R1705` `END PLOT WITH` in a Plot never started as a Subplot: `WITH` is ignored. Absence check (chapter 23).
- `R1706` `WHEN P FINISHED WITH e` where `P` never ends with `e`. Absence check (chapter 23).
- `R1707` Retired: with the specific Trigger firing before `ENDED`, a plain `ENDED` shadows nothing (ADR 0030).
- `R1708` An ending of `P`, with an Outcome or bare, that no Plan of the starting Plot hears in any Phase: no `FINISHED WITH` for that Outcome, no plain `FINISHED`, and no `ENDED`. Reported on the `START SUBPLOT`, once per unmatched ending. Endings from above are not checked. Absence check (chapter 23).
- `R1713` A `START SUBPLOT P …, UNTIL EXITED` in Phase `p`, where the Plot has a `DROPPED` or `ENDED` Plan for `P` in `p` and none in `DURING PLOT` or another Phase: the ending from above arrives after `p` is left, and nothing hears it. Absence check (chapter 23).
- `R1716` A plain `WHEN P FINISHED` Plan written above a `WHEN P FINISHED WITH …` Plan it also matches, which can then never run.

`START SUBPLOT` Mappings get chapter 15's checks.

## Reserved words

Every keyword is listed in chapter 01, *Reserved words* (`01-statements-and-blocks.md`).

## ASL mapping notes

For *The full ASL mapping* to pick up (for Jason, decided in chapter 31, `31-jason-stagings.md`: one Director agent per Staging, whose name is the Staging's identity):

- Each Staging needs a runtime identity (for example, a Director agent per Staging, with its parent's name as a belief). Givings, Signals and rank keys carry it.
- `START SUBPLOT` creates the child's Director (or a Staging inside an existing one), passes the cast (resolved whole Roles and counted picks) and the Plot's arguments, and returns at once.
- `END PLOT` walks the Subplot tree children first, takes away each Staging's Givings, then sends the parent an `ended(Plot, Outcome)` message unless the parent is ending too. `DROP SUBPLOT`, and `UNTIL EXITED` at an `ENTER`, do the same walk and post the parent a `dropped(Plot)` event of its own, handled after the current Body. The parent's handling runs the specific Plan, then the plain `ENDED` Plan.
- The parent keeps a record of its running Stagings, with their arguments, for `RUNNING`. A Staging leaves the record when it ends, before its ending is handled.
- The start-graph cycle check is a whole-Program pass over `START SUBPLOT` Statements.

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025). With no joiners, the `R1905` warning about `JOINED` in a Plot that is never the Root has nothing to warn about, and isn't reported.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- An Agent from an Outcome (`?w`) can be a recipient, an `ASSIGN` target or a `MAPPING`; `ENTER` ends its Body like `END PLOT` (chapter 20).
- A mid-run channel from child to parent (`SIGNAL PARENT e`) and recursive Subplots: *Richer Subplots* in the fog.

## Not in 2.0

- **A Staging's name**, and telling apart two Stagings with the same arguments.
- **Starting a Subplot and waiting for it** in the same Plan. It needs a Director Plan that waits, which comes with *Richer Directors*.
- **A Giving's identity inside the Agent**: a Plan that runs for one of two Givings of the same Playbook, so its Signals and its Playbook Roles reach only that Staging (chapter 15).
- **Pausing a Playbook while a Subplot runs** (`START SUBPLOT …, PAUSING Dining FOR Challenger`). It needs rules for running Plans, Pursuits, Quota counts and closing Plans.
- **Living casts below the Root**: a whole-Role Mapping on `START SUBPLOT` that keeps up with the parent's Role, so a joiner of `Guest` becomes a Spectator of a running duel (chapter 19).