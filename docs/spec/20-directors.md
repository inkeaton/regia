# Directors

What a Plot's Director can know and do: what it perceives, how it directs its Agents, which Actions and Trigger kinds it has, how Phases are entered and left, and what failure means for it. Decided in the ticket *Director capabilities* (`.scratch/regia-2/issues/21-director-capabilities.md`). It builds on chapters 05, 07, 08, 11, 12, 13, 14, 15, 16, 17 and 19, and answers the primer's ch.5 `#discuss` points (the `WORLD` keyword, whether Directors should have Goals).

## What a Director is

The **Director** runs a Plot (glossary). There is one Director per Staging. It is a **reactive state machine**: its Plans live in `DURING <phase>` and `DURING PLOT` Blocks, react to Triggers, and move the Plot between Phases.

- It **has Facts** of its own: Facts the game reports to it, and Facts it changes itself with `LEARN`, `FORGET` and `CHANGE`, including its Plot's Local Vocabulary (chapter 10).
- It has **no Goals**: no `TO g:` Plans, no `PURSUE`, no `DROP`.
- It has **no Propensities**: no Traits, no Moods, and any Label on a Director's Plan is an error (chapter 14).
- It **never reads its Agents' Facts**. What an Agent knows reaches the Director only as a Signal (chapters 07, 18).

## What a Director perceives

A Director perceives the game the way an Agent does: game Events trigger its `WHEN e:` Plans, and game Facts become its own Facts, so `WHEN f LEARNED:` fires and a `GIVEN` can test them.

```regia
DURING PLOT:
    WHEN assassin_spotted:              # a game Event, straight to the Director
        DO lock_doors.
        ASK Host TO call_guards.
        END PLOT.
```

- **A Plot's `GIVEN` reads only its Director's own Facts.**
- **Facts belong to one Staging.** Two Stagings of `HonorDuel` share none, and a parent can't read a Subplot's Facts or the other way round. A parent and its Subplot talk only through `START SUBPLOT` Mappings and Outcomes (chapter 17).
- Which game Facts and Events reach which Director is the Target's business. For Jason, see chapter 30: game percepts are passed down the Staging tree, and a Subplot starts knowing the game Facts it hears.
- A Director that needs starting Facts learns them in `DURING PLOT: WHEN ENTERED:` (below). There is no `STARTS WITH` for the Director itself.

## How a Director directs Agents

A Director directs its Agents **only through Messages**, the same `ASK` and `TELL` Agents use (chapter 07), and through Director Statements (`ASSIGN`, `UNASSIGN`, `START SUBPLOT`, …). It never orders an Agent to perform an Action: 1.0's `Host DO call_guards.` is gone (ADR 0009).

```regia
DURING feast:
    WHEN insult_thrown FROM Guest ?who:
        TELL Guest scandal(?who).          # a Fact or Event to every Guest
        ASK Host TO calm_guests.           # a Goal; the Host's own Plan decides how
```

- The **Sender is `DIRECTOR`**, so `TO calm_guests FROM DIRECTOR:` and `WHEN scandal LEARNED FROM DIRECTOR:` match, exactly as for a Role setup's `PURSUE` and `LEARN` (chapter 16). What a Director's Messages mean is what a setup's Statements mean.
- **Recipients** are a Plot Role, a filled Placeholder holding an Agent, or `EVERYONE`.
  - A **Role** recipient reaches the Agents playing that Role **in this Staging when the Message is sent**. It is a one-off: an Agent who joins later doesn't get it. Starting state for every Agent of a Role belongs in its Role setup (chapters 16, 19).
  - `EVERYONE` keeps its chapter 07 meaning: every Agent in the game. There is no Director-only "whole Cast" recipient; every Role can be named.
  - A Message to an Agent that has left is dropped with a Trace entry (chapter 19).
- **The Director hears nothing back.** A Goal it asked being reached, failing or being dropped doesn't reach it. If it needs to know, the Agent's Plan sends a Signal (`SIGNAL seated.`). Replies are with *Agent cooperation*.

### Directing one Agent

An Agent held by a Placeholder (from `FROM Guest ?who`, `WHEN Guest ?who JOINED`, or an Outcome `WITH e(?w)`) can be:

- a **recipient**: `ASK ?who TO apologise.`
- **given a Playbook**: `ASSIGN Brawling TO ?who.` and `UNASSIGN Brawling FROM ?who.` The Giving is **not standing**: it goes to that Agent only (chapter 19). `UNASSIGN Brawling FROM ?who` takes away every Giving of `Brawling` this Staging made that the Agent holds, including one it got through a whole Role; the standing record stays (chapter 15).
- **mapped onto a Role** of a Playbook or a Subplot: `MAPPING ?who TO opponent` on `ASSIGN` and on `START SUBPLOT`. The Role is filled with exactly that Agent.

```regia
DURING feast:
    WHEN insult_thrown FROM Guest ?who:
        START SUBPLOT HonorDuel, MAPPING ?who TO challenger, MAPPING Host TO offended.
        TRANSITION TO duel_interruption.
```

- The Placeholder must be filled (chapter 03).
- An Agent that has left is dropped from a Giving or a Mapping with a Trace warning. It is not a Failure.

## Actions

A Director writes Custom Actions exactly as an Agent does: `DO play_music.` The `WORLD` keyword is gone from the language.

| Action | In a Director |
|--------|---------------|
| `DO <custom action>` | allowed |
| `LEARN`, `FORGET`, `CHANGE` | allowed, on the Director's own Facts |
| `TELL`, `ASK` | allowed, Sender `DIRECTOR` |
| `PRINT`, `FAIL` | allowed |
| `WAIT <Duration>` | allowed, except in an `EXITED` Plan (below) |
| `PURSUE`, `DROP` | error: a Director has no Goals |
| `SIGNAL` | error: Signals go from an Agent to a Director. A channel from child to parent (`SIGNAL PARENT`) is with *Richer Subplots* |

Director Statements (`ASSIGN`, `UNASSIGN`, `TRANSITION`, `START SUBPLOT`, `END SUBPLOT`, `END PLOT`) are for Directors only (chapter 15).

## Trigger kinds

| Trigger | In a Director |
|---------|---------------|
| `WHEN e:` | game Events and Signals; `FROM Role [?who]` and Quotas (chapters 05, 18) |
| `WHEN f LEARNED:` / `WHEN f FORGOTTEN:` | the Director's own Facts |
| `WHEN ENTERED:` / `WHEN EXITED:` | Phase entry and exit (below) |
| `WHEN Role [?who] JOINED:` / `WHEN Role [?who] LEFT:` / `WHEN Role EMPTIED:` | cast changes (chapter 19) |
| `WHEN P ENDED [WITH e]:` | a Subplot ending (chapter 17) |
| `TO g:`, `WHEN g DROPPED:`, `WHEN g FAILED:` | error: no Goals |
| `FROM DIRECTOR` | error: a Director is never its own Sender, and a parent reaches a Subplot only through Mappings and Outcomes |

## Entering and leaving Phases

`ON ENTER` and `ON EXIT` are retired (chapter 05). Inside a `DURING` Block, Phase entry and exit are `WHEN` Triggers whose subject is the enclosing Block:

```regia
DURING reception:
    WHEN ENTERED:
        DO play_music.
        ASSIGN NobleSocializing TO Guest.
        WAIT 30 SECONDS.
        TRANSITION TO feast.            # a rough timeout: never runs if the Phase was left first

    WHEN food_served:
        TRANSITION TO feast.

    WHEN EXITED:
        DO stop_music.
```

- In `DURING <phase>`, `ENTERED` fires when the Plot enters that Phase and `EXITED` when it leaves it.
- In `DURING PLOT`, `ENTERED` fires when the Staging starts, after the Role setups and **before** the initial Phase's `ENTERED`; `EXITED` fires when the Staging ends, after the current Phase's `EXITED`.
- `EXITED` was chosen over `LEFT`, which is the cast-change Trigger (chapter 19).

### Leaving a Phase stops its Plans

When the Plot leaves a Phase, every Plan of that Phase's Block still running (for example paused in `WAIT`) is **stopped silently**: no Failure, no Trace error, nothing undone. `DURING PLOT` Plans stop only when the Staging ends. So `WAIT` in a Phase Plan works as a rough Phase timeout until 2.0's successors add delayed Triggers (chapter 12).

### What a `TRANSITION` does

`TRANSITION TO feast.`:

1. stops the old Phase's running Plans silently;
2. runs the old Phase's `EXITED` Plan, **to completion**, before the new Phase becomes current;
3. changes the Phase and clears the old Phase's Quota counts (chapter 18);
4. runs the new Phase's `ENTERED` Plan as an ordinary Plan of that Phase: it may `WAIT`, and it is stopped if the Phase is left.

Because step 2 must finish, an `EXITED` Plan can't pause or move the Plot: `WAIT`, `TRANSITION` and `END PLOT` in an `EXITED` Plan are compile-time errors.

- **`TRANSITION` ends its Body.** Statements after it in the same branch are an error, as after `END PLOT` (chapter 17). This holds in `DURING PLOT` Plans too.
- **`TRANSITION` to the current Phase re-enters it**: its Plans stop, `EXITED` runs, its Quotas are cleared, and `ENTERED` runs. This is how a round restarts.
- **`END PLOT`** follows steps 1 and 2 for the current Phase, then runs `DURING PLOT`'s `EXITED` to completion, then walks the Subplots as in chapter 17.

## Failure

A Director's Plan can fail like an Agent's (chapter 11): a Custom Action the game reports as failed, Body arithmetic on a non-Number, or `FAIL`.

- **A failing Director Plan stops there and writes a Trace entry.** The Phase and the Staging are untouched and nothing is undone. There is no Director reaction to it: with no Goals, `FAILED` has nothing to react to.
- **Director Statements never fail.** `ASSIGN` to an empty Role does nothing. A Giving, Mapping or Message reaching an Agent that has left is dropped with a Trace warning.

## Errors and warnings

- `PURSUE`, `DROP` or `SIGNAL` in a Director: error.
- `TO g:`, `WHEN g DROPPED:`, `WHEN g FAILED:` or `FROM DIRECTOR` in a Director: error.
- Any Label on a Director's Plan: error (chapter 14).
- `WAIT`, `TRANSITION` or `END PLOT` in an `EXITED` Plan: error.
- A Statement after `TRANSITION` in the same branch: error.
- `ENTERED`, `EXITED`, `JOINED`, `LEFT`, `EMPTIED` or `ENDED` in a Playbook: error (Director Trigger kinds only).
- `Role DO …` or `WORLD DO …`: error (not part of the language).
- `ASSIGN`, `MAPPING` or a recipient with an unfilled Placeholder: error (chapter 03).

## Reserved words

`ENTERED`, `EXITED`. `WORLD` from the primer is not a word of the language.

## Notes for the ASL mapping

- One Director per Staging, as in 1.0; its beliefs are the Staging's Facts. Game percepts the Director should see are routed to it by the environment.
- `ASK`/`TELL` from a Director are `achieve`/`tell` sent by the Director, as for Role setup (chapter 16), so `[source(Director)]` matches `FROM DIRECTOR`.
- Leaving a Phase drops the intentions of that Phase's Plans before running `EXITED`. `EXITED` Plans run inside the atomic transition; `ENTERED` Plans are posted as ordinary, non-atomic events after it, so they may `WAIT`. The Jason mapping is chapter 30.
- A Giving to `?who` is a single `regia_give` message with no standing record (chapter 29). A `MAPPING ?who TO r` binds `r` to that Agent alone.

## Handed off

- Directors with Goals (multi-step Director recipes): fog, *Richer Directors*.
- Moods on a Plot (pacing, tension): *Richer Propensities*.
- Replies to a Director's `ASK`: *Agent cooperation*.
- Which percepts reach which Director, and how Phase-tagged intentions are dropped: chapter 30.
