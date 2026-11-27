# Directors

What a Plot's Director can know and do: what it perceives, how it directs its Agents, which Actions and Trigger kinds it has, how Phases are entered and left, and what failure means for it. Decided in the ticket *Director capabilities* (`.scratch/regia-2/issues/21-director-capabilities.md`). It builds on chapters 05, 07, 08, 11, 12, 13, 14, 15, 16, 17 and 19, and answers the primer's ch.5 `#discuss` points (the `WORLD` keyword, whether Directors should have Goals). That a Director hears how a Goal it asked ended was decided in the ticket *A Goal's life: reached, dropped, repeated* (`.scratch/regia-revision/issues/02-goal-lifecycle.md`). That it hears with `BY`, and hears a Failure's Reason, was decided in the ticket *Failure a Plan can read, and answers to an `ASK`* (`.scratch/regia-revision/issues/03-failure-and-replies.md`), with ADR 0019. What it can ask about its own Staging (`IN`, `RUNNING`) and `EXITED BY PARENT` were decided in the ticket *What a Director knows about itself, and how a Subplot's ending is heard* (`.scratch/regia-revision/issues/09-director-state-and-endings.md`), with ADR 0030.

## What a Director is

The **Director** runs a Plot (glossary). There is one Director per Staging. It is a **reactive state machine**: its Plans live in `DURING <phase>` and `DURING PLOT` Blocks, react to Triggers, and move the Plot between Phases.

- It **has Facts** of its own: Facts the game reports to it, and Facts it changes itself with `LEARN`, `FORGET` and `UPDATE`, including its Plot's Local Vocabulary (chapter 10).
- It has **no Goals**: no `TO g:` Plans, no `PURSUE`, no `DROP`.
- It has **no Propensities**: no Traits, no Moods. Any Label on a Director's Plan, and `SHIFT` in its Body, is an error (chapter 14).
- It **never reads its Agents' Facts**. What an Agent knows reaches the Director only as a Signal (chapters 07, 18). Of an Agent's Goals it hears one thing: how a Goal it asked itself ended (below).

## What a Director perceives

A Director perceives the game the way an Agent does: game Cues trigger its `WHEN e:` Plans, and game Facts become its own Facts, so `WHEN f LEARNED:` fires and a `GIVEN` can test them.

```regia
DURING PLOT:
    WHEN assassin_spotted:              # a game Cue, straight to the Director
        DO lock_doors
        ASK Host TO call_guards
        END PLOT
```

- **A Plot's `GIVEN` reads only its Director's own Facts.**
- **Facts belong to one Staging.** Two Stagings of `HonorDuel` share none, and a parent can't read a Subplot's Facts or the other way round. A parent and its Subplot talk only through `START SUBPLOT` Mappings and Outcomes (chapter 17).
- Which game Facts and Cues reach which Director is the Target's business. For Jason, see chapter 30: every Director hears the game for itself through one shared game link, and asks the game for the Facts it starts with.
- A Director that needs starting Facts learns them in `DURING PLOT: WHEN ENTERED:` (below). There is no setup for the Director itself.

### What a Director knows about its own Staging

Besides its Facts, a Director's conditions can ask about the Staging it runs:

| Condition | Holds when |
|---|---|
| `IN <phase>` | the Staging is in that Phase now |
| `<Plot>(args) RUNNING` | a Staging of that Plot that this Staging started is running (chapter 17) |
| `<who> PLAYS <Role>` | that Agent plays the Role in this Staging (chapter 15); `COUNT(? PLAYS Guest)` counts them |

```regia
DURING PLOT:
    WHEN poison_taken:
        GIVEN NOT IN farewell:           # don't re-enter farewell
            ENTER farewell
```

- `IN <phase>` is written wherever a condition goes: a Context, an `IF`, under `NOT`, joined with `AND` and `OR`. A Phase is not a Value, so there is no `IN ?p`, and it has no Matches to pick or count beyond 1 or 0.
- In a Phase's own Plans, `IN` of that Phase always holds: a Plan of a Phase is stopped when the Phase is left. It is meant for `DURING PLOT` Plans, which run in every Phase.
- `IN` naming a Phase the Plot doesn't declare is `R20_08-undeclared-phase`. `IN` in a Playbook, or in a Plot that declares no Phases, is an error (`R20_14-misplaced-in-clause`).
- `ENTER` naming the current Phase still re-enters it (below). Whether that is wanted is the writer's to say, with `IN`.
- **Where a transition goes, and where it came from, has no condition and no Trigger.** What belongs to "leaving `feast` for `farewell`" is written in the Plan that runs `ENTER farewell`, before it. That Plan is the transition, and the Phase map draws it as the edge (chapter 25). An `ENTERED` Plan that must know where the Plot came from reads a Fact that Plan learned.

## How a Director directs Agents

A Director directs its Agents **only through Messages**, the same `ASK` and `TELL` Agents use (chapter 07), and through Director Statements (`ASSIGN`, `REMOVE`, `START SUBPLOT`, …). It never orders an Agent to perform an Action: 1.0's `Host DO call_guards` is gone (ADR 0009).

```regia
DURING feast:
    WHEN insult_thrown, FROM Guest ?who:
        TELL Guest scandal(?who)           # a Fact or Cue to every Guest
        ASK Host TO calm_guests            # a Goal; the Host's own Plan decides how
```

- The **Sender is `DIRECTOR`**, so `TO calm_guests, FROM DIRECTOR:` and `WHEN scandal LEARNED, FROM DIRECTOR:` match, exactly as for a Role setup's `PURSUE` and `LEARN` (chapter 16). What a Director's Messages mean is what a setup's Statements mean.
- **Recipients** are a Plot Role, `CAST`, a filled Placeholder holding an Agent, or `EVERYONE`. A Role or `CAST` may carry a count and an `EXCEPT` (chapter 15): `ASK 1 OF Servant TO pour_wine`, `TELL Guest EXCEPT ?who scandal(?who)`.
  - A **Role** recipient reaches the Agents playing that Role **in this Staging when the Message is sent**. It is a one-off: an Agent who joins later doesn't get it. Starting state for every Agent of a Role belongs in its Role setup (chapters 16, 19).
  - **`CAST`** reaches every Agent of this Staging **once**, however many Roles it plays. It is the Role everybody in the Staging plays (chapter 15, ADR 0024), and a one-off like any Role recipient.
  - `EVERYONE` keeps its chapter 07 meaning: every Agent in the game, in this Staging or not.
  - A Message to an Agent that has left is dropped with a Trace entry (chapter 19).
- **The Director hears how a Goal it asked ended** (next section). It hears nothing back from a `TELL`.

### Hearing how an asked Goal ended

A Plot can write the four ending Triggers of chapter 05 on a Goal its own Director asked. The Playbook sends nothing: no Signal, and no `CUE` line for "done".

```regia
DURING seating:
    WHEN ENTERED:
        ASK Guest TO take_seat

    WHEN take_seat FAILED, BY Guest ?g:        # this Guest found no seat
        ASK Host TO find_place(?g)

    WHEN take_seat ENDED, BY ALL Guest:        # seated or not, the evening moves on
        ENTER feast
```

- **Only Pursuits whose Sender is this Staging's Director**: its `ASK … TO g`, and the `PURSUE g` of its Role setups (chapter 16). A Goal the Agent gave itself, or that another Agent or another Director asked, is not reported, even under the same name.
- **`BY` names the Agent whose Pursuit it was**: `BY Guest`, `BY ?who`, `BY Guest ?who`, and the Quota forms (chapter 18). The Role is checked when the ending arrives, in this Staging. It is the clause an asking Agent uses (chapter 05). `FROM` on a Goal's ending means who asked, which here is always this Director, so in a Plot it is an error with a hint to write `BY` (`R20_13-from-on-goal-ending`).
- **One report per Pursuit.** A Goal asked twice is reported twice. A recipe that repeats (chapter 08) is reported for its first round only: later rounds have no Sender.
- The specific Trigger fires first, then `ENDED`, as at the Agent. The Agent's own ending Plans and the Director's are independent; neither waits for the other.
- They are heard like any Director Trigger: the current Phase's Plan, else the `DURING PLOT` Plan (chapter 13).
- **An ending with no Plan is silent.** Most asked Goals are not listened to, so there is no `unheard` entry like a Signal's `T38_01-signal-found-no-plan`. The Agent's own `goal` entry is in the Trace either way (chapter 34).
- **A Failure's Reason is reported**: `WHEN take_seat FAILED WITH no_chair, BY Guest ?g:`, tried in written order with the plain `FAILED` Plans of the same Block (chapter 11). The cause of a Failure with no Reason is in the Trace only.
- **An Agent that leaves the Program reports nothing** for the Pursuits it had. `WHEN Guest LEFT` says it left (chapter 19), and a Quota is checked again against the smaller Role.
- An ending that arrives after the Staging has ended reaches nobody.
- A Goal-ending Trigger on a Goal this Plot never asks can never fire, and is an error (`R20_12-goal-never-asked`).
- The Agent still decides how: the Director hears that `take_seat` ended, never which recipe ran or what the Agent knows.

An asking **Agent** hears the same, with the same clause (chapters 05, 07).

### Directing one Agent

An Agent held by a Placeholder (from `FROM Guest ?who`, `WHEN Guest ?who JOINED`, `GIVEN ?who PLAYS Guest`, or an Outcome `WITH e(?w)`) can be:

- a **recipient**: `ASK ?who TO apologise`.
- **given a Playbook**: `ASSIGN Brawling TO ?who` and `REMOVE Brawling FROM ?who`. The Giving is **not standing**: it goes to that Agent only (chapter 19). `REMOVE Brawling FROM ?who` takes away only the Givings of `Brawling` this Staging made to that Agent. `REMOVE Brawling FROM Guest ?who` takes the Agent out of the Givings to `Guest`, `ASSIGN Brawling TO Guest ?who` puts it back, and `REMOVE Brawling FROM CAST ?who` takes everything this Staging gave it (chapter 15).
- **mapped onto a Role** of a Playbook or a Subplot: `MAPPING ?who AS opponent` on `ASSIGN` and on `START SUBPLOT`. The Role is filled with exactly that Agent.

```regia
DURING feast:
    WHEN insult_thrown, FROM Guest ?who:
        START SUBPLOT HonorDuel, MAPPING ?who AS challenger, MAPPING Host AS offended
        ENTER duel_interruption
```

- The Placeholder must be filled (chapter 03).
- **A Director gets an Agent from its Roles with `PLAYS`** (chapter 15), without waiting for a Message from it: `GIVEN ?c PLAYS Challenger`. A winner no longer has to Signal so that the Director learns a name it gave out itself, and an Outcome can say who was in the Subplot.
- An Agent that has left is dropped from a Giving or a Mapping with a Trace warning. It is not a Failure.

## Actions

A Director writes Custom Actions exactly as an Agent does: `DO play_music`. The `WORLD` keyword is gone from the language.

| Action | In a Director |
|--------|---------------|
| `DO <custom action>` | allowed |
| `LEARN`, `FORGET`, `UPDATE` | allowed, on the Director's own Facts |
| `TELL`, `ASK` | allowed, Sender `DIRECTOR` |
| `PRINT`, `FAIL` | allowed |
| `WAIT <Duration>` | allowed, except in an `EXITED` Plan (below) |
| `PURSUE`, `DROP g` | error: a Director has no Goals. `DROP SUBPLOT P` is a Director Statement (chapter 17) |
| `SIGNAL` | error: Signals go from an Agent to a Director. A channel from child to parent (`SIGNAL PARENT`) is with *Richer Subplots* |

Director Statements (`ASSIGN`, `REMOVE`, `ENTER`, `START SUBPLOT`, `DROP SUBPLOT`, `END PLOT`) are for Directors only (chapter 15).

## Trigger kinds

| Trigger | In a Director |
|---------|---------------|
| `WHEN e:` | game Cues and Signals; `FROM Role [?who]` and Quotas for Signals, `FROM GAME` for game Cues only (chapters 05, 18) |
| `WHEN f LEARNED:` / `WHEN f FORGOTTEN:` | the Director's own Facts; `LEARNED, FROM GAME` for a Fact the game reported |
| `WHEN ENTERED:` / `WHEN EXITED[, BY PARENT]:` | Phase entry and exit (below) |
| `AFTER <Duration>:` | a Phase timeout, counted from entering the Phase, or in `DURING PLOT` from the start of the Staging (chapter 12) |
| `WHEN Role [?who] JOINED:` / `WHEN Role [?who] LEFT:` / `WHEN Role EMPTIED:` | cast changes (chapter 19) |
| `WHEN P FINISHED [WITH e]:` / `WHEN P DROPPED:` / `WHEN P ENDED:` | a Subplot ending, by itself, by this Staging, or either (chapter 17) |
| `WHEN g REACHED:` / `WHEN g DROPPED:` / `WHEN g FAILED:` / `WHEN g ENDED:` | the endings of a Goal this Director asked; `BY Role [?who]`, Quotas, and `WITH` on `FAILED` (above) |
| `WHEN ASSIGNED:` / `WHEN REMOVED:` | error: Playbook Trigger kinds (chapter 15) |
| `TO g:` | error: no Goals |
| `FROM DIRECTOR` | error: a Director is never its own Sender, and a parent reaches a Subplot only through Mappings and Outcomes |
| `ME`, `FROM ME` | error: a Director is not an Agent (chapter 03) |

## Declaring Phases

```regia
PLOT RoyalBanquet:
    PHASE reception INITIAL
    PHASE feast
```

Decided in the ticket *Phase declaration checks* (`.scratch/regia-2/issues/44-phase-declaration-checks.md`).

- A Plot that declares Phases marks **exactly one** `INITIAL`, even when it has only one Phase. The Staging starts in it. Declaration order is free (chapter 10), so there is no default "first Phase".
- **A Plot may declare no Phases.** It has only Role setups and `DURING PLOT` Plans, which is enough for a small Subplot that gives a Playbook and ends on a Signal. It behaves as if it had one Phase that is never left: `DURING PLOT`'s `ENTERED` fires when the Staging starts, and `EXITED` when it ends. With no Phase to name, any `ENTER` in it is an error (`R20_08-undeclared-phase`).
- **One Block per Phase.** Each declared Phase has at most one `DURING` Block, and the Plot at most one `DURING PLOT`, so a Phase's Plans are all in one place.
- A Phase with no `DURING` Block is fine: a quiet Phase, moved on by `DURING PLOT` Plans. So is a Phase that nothing leaves: it can be the last act, ended by `END PLOT` or by the parent.
- `PHASE` and `DURING` belong to Plots only.

## Entering and leaving Phases

`ON ENTER` and `ON EXIT` are retired (chapter 05). Inside a `DURING` Block, Phase entry and exit are `WHEN` Triggers whose subject is the enclosing Block:

```regia
DURING reception:
    WHEN ENTERED:
        DO play_music
        ASSIGN NobleSocializing TO Guest

    AFTER 30 SECONDS:                   # never runs if the Phase was left first
        ENTER feast

    WHEN food_served:
        ENTER feast

    WHEN EXITED:
        DO stop_music
```

- In `DURING <phase>`, `ENTERED` fires when the Plot enters that Phase and `EXITED` when it leaves it.
- In `DURING PLOT`, `ENTERED` fires when the Staging starts, after the Role setups and **before** the initial Phase's `ENTERED`; `EXITED` fires when the Staging ends, after the current Phase's `EXITED`.

### `EXITED, BY PARENT`

A Subplot can tell an ending by its parent from one of its own:

```regia
DURING fighting:
    WHEN EXITED, BY PARENT:         # DROP SUBPLOT, UNTIL EXITED, or the parent ending
        DO sheathe_swords
    WHEN EXITED:                    # every exit, after the BY PARENT Plan when there is one
        DO bow
```

- `EXITED, BY PARENT` matches when the Staging is ending because of its parent: the parent's `DROP SUBPLOT`, an `UNTIL EXITED` when the parent leaves that Phase, or the parent itself ending. It is written in a Phase Block, where it matches when the Staging ends from above while in that Phase, and in `DURING PLOT`.
- **The specific Trigger fires first, then plain `EXITED`**, both to completion, as for a Subplot's endings (chapter 17) and a Goal's (chapter 05). What every exit does goes in plain `EXITED`, once.
- In a Plot never started as a Subplot it can't fire, and is a warning (`R20_15-ignored-exited-by-parent`), as `END PLOT WITH` is (chapter 17). It is a warning and not an error because a Plot doesn't say whether it is the Root (chapter 21).
- `BY PARENT` is a clause, written after a `,` like the `BY` of a Goal's ending (chapter 05), and with the same sense: who did it. It goes only on `EXITED` (`R05_06-by-on-wrong-trigger`). `WHEN EXITED BY PARENT:` without the `,` is `R01_11-clause-without-comma` (chapter 01), whose hint adds it. `PARENT` is chapter 13's word for the Plot that started this one.

### What starting a Staging does

1. `DURING PLOT` and the initial Phase become active, and their Quota counts start (chapter 18).
2. The `CAST:` setup runs, then the Plot's Role setups, then the initial Phase's Role setups, each in Role declaration order (chapter 16). In the Root Plot's Staging, each starting Agent's kind or individual-Agent lines run next (chapter 21, *Setup lines*).
3. `DURING PLOT`'s `ENTERED` Plan runs, then the initial Phase's; `DURING PLOT`'s and the initial Phase's `AFTER` counts start.

A Phase counts before anything is sent on its behalf. A setup's `PURSUE take_seat` that ends at once is heard by the initial Phase's `WHEN take_seat ENDED, BY ALL Guest`.
- `EXITED` was chosen over `LEFT`, which is the cast-change Trigger (chapter 19).

### Leaving a Phase stops its Plans

When the Plot leaves a Phase, every Plan of that Phase's Block still running (for example paused in `WAIT`) is **stopped silently**: no Failure, no Trace error, nothing undone. `DURING PLOT` Plans stop only when the Staging ends. An `AFTER` Plan still counting is stopped the same way, so a Phase timeout never fires once the Phase is left (chapter 12). The Agents' waiting Actions under Playbooks taken away are called off (chapter 08).

### What `ENTER` does

`ENTER p` makes `p` the current Phase. It names the Phase it enters and fires that Phase's `WHEN ENTERED`, as `LEARN` fires `LEARNED`. Moving from one Phase to another is still called a **transition**, and the Phase map draws each as an edge (chapter 25). `ENTER` replaced `TRANSITION TO`, which is an error (`R20_16-retired-transition-to`): `TO` introduces a Goal (chapter 01).

`ENTER feast`:

1. stops the old Phase's running Plans silently;
2. runs the old Phase's `EXITED` Plan, **to completion**, before the new Phase becomes current;
3. takes away what was given for the old Phase: its Role setups' Givings and its `UNTIL EXITED` Givings, and ends its `UNTIL EXITED` Subplots (chapters 15, 16). Their `DROPPED` and `ENDED` are heard after the transition, by the new Phase's Plans or else by `DURING PLOT` (chapter 17);
4. changes the Phase, clears the old Phase's Quota counts and starts the new Phase's (chapter 18);
5. runs the new Phase's Role setups, in Role declaration order (chapter 16);
6. runs the new Phase's `ENTERED` Plan as an ordinary Plan of that Phase, and starts its `AFTER` counts: they may `WAIT`, and they are stopped if the Phase is left.

Because step 2 must finish, an `EXITED` Plan can't pause or move the Plot: `WAIT`, `ENTER` and `END PLOT` in an `EXITED` Plan are compile-time errors. A `DO` is allowed, and the transition waits for the game's answer (`DO clear_tables`, `royal_banquet.regia:103`): what a Plot does on its way out may take the game's time, and whether the game answers is the game's affair, as for any Action.

- **`ENTER` ends its Body.** Statements after it in the same branch are an error, as after `END PLOT` (chapter 17). This holds in `DURING PLOT` Plans too.
- **`EXITED` runs before the taking**, so an `EXITED` Plan can still address Agents through the Phase's Playbooks. The Agents' own closing Plans (`DROPPED`, `ENDED`, `REMOVED`, chapter 15) run on their side and the transition doesn't wait for them.
- **A Playbook both Phases give is taken and given again.** Its Plans stop, `REMOVED` and then `ASSIGNED` fire, and its Local Facts survive. A Playbook meant to span Phases is given by the Plot's setup or by a plain `ASSIGN`.
- **`ENTER` naming the current Phase re-enters it**: its Plans stop, `EXITED` runs, what was given for it is taken away, its Quotas are cleared, its setups run again, and `ENTERED` runs. This is how a round restarts.
- **`END PLOT`** follows steps 1 and 2 for the current Phase, then runs `DURING PLOT`'s `EXITED` to completion, then walks the Subplots as in chapter 17.

## Failure

A Director's Plan can fail like an Agent's (chapter 11): a Custom Action the game reports as failed, Body arithmetic on a non-Number, or `FAIL`.

- **A failing Director Plan stops there and writes a Trace entry.** The Phase and the Staging are untouched and nothing is undone. There is no Director reaction to it: with no Goals, `FAILED` has nothing to react to.
- **Director Statements never fail.** `ASSIGN` to an empty Role does nothing. A Giving, Mapping or Message reaching an Agent that has left is dropped with a Trace warning.

## Transpiler checks

**Errors**

- `R20_01-playbook-statement-in-director` `PURSUE`, `DROP` or `SIGNAL` in a Director.
- `R20_02-playbook-trigger-in-director` `TO g:` or `FROM DIRECTOR` in a Director.
- `R20_03-wrong-statement-in-exited` `WAIT`, `ENTER` or `END PLOT` in an `EXITED` Plan.
- `R20_04-statement-after-enter` A Statement after `ENTER` in the same branch.
- `R20_05-director-trigger-in-playbook` `ENTERED` or `EXITED`, or a Subplot's `FINISHED`, `DROPPED` or `ENDED`, in a Playbook (Director Trigger kinds only; a Goal's `ENDED` is legal there).
- `R20_06-do-with-subject` `Role DO …` or `WORLD DO …` (not part of the language).
- `R20_07-missing-or-repeated-initial` A Plot that declares Phases with no `INITIAL` Phase, or with several (a quick fix marks one `INITIAL`).
- `R20_08-undeclared-phase` `DURING p:`, `ENTER p` or `IN p` naming a Phase the Plot doesn't declare, or any `ENTER` in a Plot that declares no Phases (with a "did you mean" hint when a declared name is close).
- `R20_09-repeated-during-block` Two `DURING` Blocks for one Phase, or two `DURING PLOT` Blocks.
- `R20_10-phase-in-playbook` `PHASE` or `DURING` inside a `PLAYBOOK`.
- `R20_12-goal-never-asked` `WHEN g REACHED`, `DROPPED`, `FAILED` or `ENDED` in a Plot that never asks `g`: no `ASK … TO g` and no setup `PURSUE g`. Absence check (chapter 23).
- `R20_13-from-on-goal-ending` `FROM` on a Goal's ending in a Plot (hint: `BY`).
- `R20_14-misplaced-in-clause` `IN <phase>` in a Playbook, or in a Plot that declares no Phases.
- `R20_16-retired-transition-to` The retired `TRANSITION TO p` (hint: `ENTER p`).

**Warnings**

- `R20_11-unreachable-phase` A Phase that can never be entered: it isn't `INITIAL`, and no `ENTER` in the Plot names it. Absence check (chapter 23).
- `R20_15-ignored-exited-by-parent` `WHEN EXITED, BY PARENT` in a Plot never started as a Subplot. Absence check (chapter 23).

A `GOAL` declared inside a Plot is `R10_15-goal-in-plot` (chapter 10). `ME` in a Plot is `R03_09-me-in-plot` (chapter 03). A Signal the Plot gives the Playbook for and never handles, and a `FROM <Role>` Plan no Signal can reach, are `R38_01-unheard-signal` and `R38_02-cue-never-signalled` (chapter 38). A Label on a Director's Plan is `R14_06-label-in-director`; `JOINED`, `LEFT` and `EMPTIED` in a Playbook are `R19_01-cast-change-in-playbook`; an unfilled Placeholder in `ASSIGN`, `MAPPING` or a recipient is `R03_04-unfilled-placeholder`/`R03_05-maybe-unfilled-placeholder`.

## Trace entries

**Warnings**

- `T20_01-giving-after-leaving` A Giving or a Mapping that reaches an Agent who has left, dropped.
- `T20_02-director-plan-failed` A Director Plan that failed: it stops, and the Phase and the Staging are untouched. It follows the failure entry of its cause.

A Message to an Agent who has left is `T19_01-message-after-leaving`. A Signal or a Subplot's ending that finds no Plan is an `unheard` entry, `T38_01-signal-found-no-plan`/`T38_02-ending-found-no-plan` (chapter 38).

## Reserved words

Every keyword is listed in chapter 01, *Reserved words* (`01-statements-and-blocks.md`).

## Notes for the ASL mapping

- One Director per Staging, as in 1.0; its beliefs are the Staging's Facts. Game percepts the Director should see are routed to it by the environment.
- `ASK`/`TELL` from a Director are `achieve`/`tell` sent by the Director, as for Role setup (chapter 16), so `[source(Director)]` matches `FROM DIRECTOR`.
- Leaving a Phase drops the intentions of that Phase's Plans before running `EXITED`. `EXITED` Plans run inside the atomic transition; `ENTERED` Plans are posted as ordinary, non-atomic events after it, so they may `WAIT`. **A `DO` in an `EXITED` Plan waits for the game**, and the Director runs nothing else meanwhile; what comes in is heard after the transition, by the new Phase. The Jason mapping is chapter 30.
- An Agent reports the ending of each Pursuit whose Sender is a Director to that Director, with the Reason of a Failure, as a message the designer never writes. The Director needs a catch-all that drops a report no Plan takes, with no Trace entry. The Jason chapters don't describe this yet.
- A Giving to `?who` is a single `regia_give` message with no standing record (chapter 29). A `MAPPING ?who AS r` binds `r` to that Agent alone.
- `IN p` reads the Director's current-Phase belief (chapter 30, *`IN`*). `EXITED, BY PARENT` needs the Staging to know, while it ends, whether the ending came from its parent: in Jason, receiving the parent's end message is what tells it (chapter 31, *A child ended by its parent*).

## Regia 1.5

In 1.5 (ADR 0025), except *Hearing how an asked Goal ended*: a Director hears no ending of a Goal it asked. `WHEN g REACHED`, `DROPPED`, `FAILED` or `ENDED` in a Plot, with or without `BY`, is `R01_09-later-regia-construct` in a 1.5 build (chapter 01), and `R20_12-goal-never-asked` and `R20_13-from-on-goal-ending` are never reported. A Subplot's endings are chapter 17's and stay. A Director that must know a Goal ended is told by a Signal the recipe sends.

Also later: `FROM GAME` in the Trigger table, `JOINED`, and the Quota counts that a Phase starts and clears.

`ENTER`, which replaced `TRANSITION TO`, and `R20_16-retired-transition-to` were decided in the ticket *`TO` and `FROM` outside Triggers* (`.scratch/syntax-review/issues/05-to-and-from.md`).
Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Handed off

- Directors with Goals (multi-step Director recipes): fog, *Richer Directors*. Starting a Subplot and waiting for it in the same Plan comes with them (chapter 17, *Not in 2.0*).
- Moods on a Plot (pacing, tension): *Richer Propensities*.
- Calling off a Goal the Director asked: not in 2.0, with replies and refusals (chapter 07, *Room for cooperation*). Until then a Goal that must stop with a Phase has its recipe in a Playbook given for that Phase, and the Playbook's `DROPPED` Plan cleans up (chapter 15).
- Which percepts reach which Director, and how Phase-tagged intentions are dropped: chapter 30.
