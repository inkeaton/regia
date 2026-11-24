# The Trace

The evening is over, and one Guest spent all of it standing by the wall. No error was reported, since nothing in the Program was wrong. To find out why, we read the Trace: the record of what the run did, in order. It holds the whole story of the run, every Failure and every runtime warning, all in one record, so the order between "this Action ran" and "this failed because of it" is never lost.

Every entry is written in three places, each in its own form:

| Form | Where | Used for |
|---|---|---|
| the entry, with every field | the Trace file, one entry per line | tools, and comparing two runs |
| the console line, one line of text | the console, as the run goes | reading a run as it happens |
| the expected line: the agent, a colon, the console line's text | a behaviour case's `.trace` file | testing a run against what the spec promises |

The entries, their fields, their codes and the `.trace` format are the same on every Target. How the Jason Target writes them is in *Jason: the game and the Trace*.

## Reading a run

The banquet starts. Here are its first moments, as entries (`…` marks entries left out; the run's own `RUN STARTED banquet.regin SEED 4127` comes first):

| `seq` | `agent` | Console line |
|---|---|---|
| 2 | `director:RoyalBanquet` | `STAGING RoyalBanquet STARTED king AS Host, noble_1 AS Guest, …` |
| 3 | `director:RoyalBanquet` | `PHASE -> arrival` |
| … | | |
| 5 | `director:RoyalBanquet` | `ASK king TO take_seat` |
| 6 | `director:RoyalBanquet` | `TELL noble_1 purse(12)` |
| … | | |
| 9 | `director:RoyalBanquet` | `ASK noble_1 TO take_seat` |
| … | | |
| 31 | `king` | `GIVE Hosting TO king AS Host IN director:RoyalBanquet` |
| 32 | `noble_1` | `FACT +seat(seat_3)` |
| 33 | `noble_1` | `FACT +purse(12) FROM director:RoyalBanquet` |
| … | | |
| 36 | `noble_1` | `GOAL take_seat PURSUED` |
| 37 | `noble_1` | `PLAN Courtesy: TO take_seat GIVEN seat(seat_3)` |
| 38 | `noble_1` | `DO walk_to(seat_3)` |
| 39 | `director:RoyalBanquet` | `PLAN arrival: WHEN ENTERED` |
| 40 | `director:RoyalBanquet` | `DO open_doors` |
| … | | |
| 57 | `noble_1` | `DO walk_to(seat_3) DONE` |
| 58 | `noble_1` | `DO sit_down` |
| 59 | `noble_1` | `DO sit_down DONE` |
| 60 | `noble_1` | `TELL king greeting` |
| 61 | `noble_1` | `GOAL take_seat REACHED` |
| 62 | `noble_1` | `PLAN Courtesy: WHEN take_seat ENDED` |
| 63 | `noble_1` | `SIGNAL took_seat TO director:RoyalBanquet` |
| 64 | `king` | `PLAN Courtesy: WHEN greeting` |
| 65 | `king` | `DO bow_to(noble_1)` |
| 66 | `director:RoyalBanquet` | `PLAN arrival: WHEN took_seat` |
| 67 | `director:RoyalBanquet` | `FACT +seated(noble_1)` |

- `seq` numbers the entries of the whole Program in one order, with no gaps. It is the only order between two Agents.
- A Staging's start comes first, in a fixed order: the `staging` entry, the `phase` entry of its initial Phase (none for a Plot without Phases), a `fact` entry for each game Fact its Director starts with, then the setups' entries. The setups' `LEARN` and `PURSUE` are a `TELL` and an `ASK` from the Director, so they are `message` entries under the Director's name.
- Receiving a Message has no kind of its own. A told Fact shows as the receiver's `fact` entry, with `FROM` (row 33). An `ASK` shows as the receiver's `goal` entry, then the recipe's `plan` entry (rows 36 and 37). A told Cue shows as the `plan` entry of the Plan it starts (row 64).
- What the game sends has no kind of its own either. A game Fact is a `fact` entry with no `FROM` (row 32), and a game Cue shows as the Plan it starts. A percept no Plan takes leaves no entry: the game sends far more than a Program listens to.
- A Giving is written by the Agent that holds it (row 31), one entry per Giving, even when the Agent already holds the Playbook through another. The Director that made it writes nothing, since it doesn't know who received it.
- A Director's Plan is named by its Phase, `PLAN arrival: WHEN took_seat`, or by `DURING PLOT`. The two `took_seat` Plans of `arrival` read alike here, and the entry's `at` field, the source location, tells them apart.

Spec: chapter 34, *What the Trace records*.

## Kinds of entry

Every entry has a kind. These are the kinds a 1.5 run writes:

| Kind | Written when | Console line |
|---|---|---|
| `run` | the run starts, with its Entry and seed, and when it ends | `RUN STARTED banquet.regin SEED 4127`, `RUN ENDED`, `RUN ENDED (STOPPED)` |
| `action` | a `DO` is sent, and again when its outcome comes back or it is called off | `DO walk_to(seat_3)`, then `… DONE`, `FAILED`, `REFUSED` or `CANCELLED` |
| `time` | a `WAIT … UNTIL` ends; the game pauses or resumes the clock | `WAIT UNTIL on_plate(?) MET`, `… TIMED OUT`, `CLOCK PAUSED`, `CLOCK RESUMED` |
| `message` | a `TELL`, `ASK` or `SIGNAL` is sent, a setup's `LEARN` and `PURSUE` included | `TELL king greeting`, `ASK noble_1 TO take_seat`, `SIGNAL took_seat TO director:RoyalBanquet` |
| `plan` | a Plan is chosen to run; a waiting Plan is stopped or fails in turn | `PLAN Courtesy: WHEN greeting` |
| `unheard` | something arrived and no Plan ran for it | `UNHEARD T0702 scandal(noble_2) FROM hothead_1` |
| `goal` | a Pursuit starts, and when it is reached, dropped or failed | `GOAL take_seat PURSUED`, `… REACHED` |
| `fact` | an Agent or a Director learns or forgets a Fact | `FACT +seated(noble_1)`, `FACT -on_duty` |
| `phase` | a Director enters its initial Phase, or changes Phase | `PHASE -> arrival`, `PHASE arrival -> reception ON WHEN took_seat` |
| `staging` | a Staging starts, with its Cast, or ends, with how it ended | `STAGING HonorDuel(hothead_1) FINISHED WITH duel_settled(noble_3)` |
| `giving` | an Agent receives or loses one Giving of a Playbook | `GIVE Hosting TO king AS Host IN director:RoyalBanquet` |
| `cast` | an Agent starts with its Propensity values, or leaves the Program | `TEMPER noble_1 bravery 0.53 sympathy 0.12 aggressiveness -0.2`, `LEFT noble_4` |
| `mood` | a Mood changes, by a `SHIFT` Statement or a `SHIFTS` Label | `MOOD sympathy 0.12 -> -0.08 BY SHIFT` |
| `failure` | the cause of a Failure | `FAILURE T1101 DO open_doors refused` |
| `warning` | a runtime warning: the Plan carries on | `WARNING T1901 …` |
| `script` | a behaviour case plays a `>` step | `> cue noble_2 idle` |

The console line of each kind, in full:

- `action`: `DO <action>` when sent; `DO <action> DONE`, `FAILED` or `REFUSED` when the outcome comes back, with the game's reason if it gave one; `DO <action> CANCELLED` when its Plan stopped first.
- `message`: `TELL <to> <fact or cue>`, `ASK <to> TO <goal>`, `SIGNAL <cue> TO <director>, …`, prefixed `DROPPED` when the recipient has left. A Director whose Staging had already ended when the Signal reached it is followed by ` ENDED`: `SIGNAL culprit_seized(noble_5) TO director:RoyalBanquet, director:Poisoning#1 ENDED`.
- `plan`: `PLAN <owner>: <trigger>`, then ` GIVEN <context>` or ` ELSE` when the Block has one, then ` OVER <block>, … BY <how>` when it had rivals (*Why a Plan ran*). The examples write the Trigger with its values filled in and its `FROM` left out. A waiting Plan stopped or failed in turn: `PLAN <block> STOPPED because #<seq>`, `PLAN <block> FAILED because #<seq>`.
- `goal`: `GOAL <goal> PURSUED`, `REACHED`, `DROPPED` or `FAILED`, with ` because #<seq>` when it ended in turn.
- `phase`: `PHASE <old> -> <new> ON <trigger>`, the Trigger of the Plan that ran the `ENTER` as its `plan` entry writes it: `ON WHEN handkerchief_dropped`, `ON AFTER 2 MINUTES`, `ON ENTERED`.
- `staging`: `STAGING <plot>(<args>) STARTED <cast>`; `… FINISHED WITH <outcome>`, `… FINISHED` for an ending with no Outcome, `… ENDED BY PARENT`. In a Cast, an Agent that already plays in another running Staging of the same Plot is followed by `ALSO IN #<n>`.
- `giving`: `GIVE <playbook> TO <agent> AS <role> IN <director>`, `TAKE <playbook> FROM <agent> IN <director>`. A Giving to one Agent has no ` AS <role>`; a Giving tied to a Phase adds ` UNTIL <phase> EXITED`.
- `mood`: `MOOD <mood> <old> -> <new> BY SHIFT` for the Statement, `MOOD <mood> <old> -> <new> BY <owner>: <trigger>` for a Label.
- `unheard`, `failure`, `warning`: `UNHEARD <code> <what>`, `FAILURE <code> <what>`, `WARNING <code> <what>`. The words after the code are for the reader; a behaviour case matches the code.

> **In 2.0** two systems add to the Trace. A Quota Trigger writes `count` entries as it counts Signals, and marks a firing completed by a departure on its `plan` entry. An Agent that joins writes a `cast` entry of its own. Spec chapter 34, *What the Trace records*, *Regia 1.5*; chapters 18 and 19. In 1.5 the banquet counts seated Guests by hand, so the count shows only as the Director's `fact` entries, `FACT +seated(noble_1)`.

Spec: chapter 34, *What the Trace records*, *The console line*.

## Fields

Every entry has these fields:

| Field | Holds |
|---|---|
| `seq` | its position in the run: 1, 2, 3 … with no gaps, one order for the whole Program |
| `t` | milliseconds since the run started, on the Target's clock |
| `agent` | who wrote it: an Agent's name or a Director's name |
| `kind` | one of the kinds above |
| `level` | `info`, `warning` or `error` |
| `at` | the `.regia` source location, `file:line:col`, of the Statement or Plan it comes from. The Program's own machinery (a `giving`, a `staging`, a `phase` at start) has none |
| `code` | its Trace code, on every `failure`, `warning` and `unheard` entry |

and the fields of its kind:

| Kind | Fields |
|---|---|
| `run` | `event: started`, `entry`, `seed`; `event: ended`, `how: story_ended` or `stopped` |
| `action` | when sent: `action`, `waiting` (`false` for `WITHOUT WAITING`). When it comes back or is called off: `of` (the `seq` of the send), `outcome: done`, `failed`, `refused` or `cancelled`, and `reason` when one was given |
| `time` | `condition`, `outcome: met` or `timed_out`, `waited` (milliseconds); or `clock: paused` or `resumed` |
| `message` | `form: tell`, `ask` or `signal`, `to` (a list of names), `content`; for a `SIGNAL`, `ended` (the Directors in `to` whose Staging had ended); `dropped: true` |
| `plan` | `block` (`owner`, `trigger`, and `given` or `else`), `values` (each Placeholder with its value), `by`, `over`, `fits`, `outcome: started`, `stopped` or `failed`, `because` |
| `unheard` | by code: `T0702` `cue`, `sender`; `T3801` `cue`, `sender`, `plot`, `phase`; `T3802` `plot`, `args`, `outcome` (absent for a bare ending), `phase` (the parent's) |
| `goal` | `goal`, `event: pursued`, `reached`, `dropped` or `failed`, `sender` (on `pursued`, when there is one), `of`, `because` |
| `fact` | `change: +` or `-`, `fact`, `from` when told |
| `phase` | `from` (absent for the initial Phase), `to`, `plan` (the `seq` of the `plan` entry that ran the `ENTER`) |
| `staging` | `event: started` or `ended`, `plot`, `args`, `cast` (a list of `agent`, `roles`, and `also_in`), `how: outcome`, `bare` or `by_parent`, `outcome` |
| `giving` | `event: give` or `take`, `playbook`, `agent`, `role` (the giving Plot's Role; absent for a Giving to one Agent), `staging` (the giving Director's name), `until` (the Phase, for a Giving tied to one) |
| `cast` | `event: temper` or `left`, `agent`, `roles`, `values` (each Propensity with its value) |
| `mood` | `mood`, `old`, `new`, and `by: shift` for the Statement or `plan: <seq>` for a Label |
| `failure` | `what` (the Statement or Goal, as written), `reason` when there is one |
| `warning` | `what`, and whatever its code's chapter names |
| `script` | `step`, as written, and `reached` for a `*` step |

- Values are written as Regia text: `"grudge(percival, 2)"`, `"?who"`. A field that doesn't apply is left out.
- `of` and `because` hold a `seq`. `of` links the end of something to its start: an Action's outcome to its send, a Goal's ending to the entry where that Pursuit started. Two Pursuits of the same Goal are told apart by `of`. `because` links an entry to the cause it happened for.
- Entries use the designer's names only: Agents, Plots, Phases, Playbooks, Plans, Goals and Statements as written in `.regia` files. A Target's Generated names never appear.

### Names

[`banquet.regin`](../showcase/banquet.regin)
```regia
AGENT king, PLAYS Host

KIND noble, PLAYS Guest:
    COUNT 6
```

- An individual Agent is named by its own name: `king`, `percival`.
- An Agent of a kind is `<kind>_<n>`, numbered from 1 within its kind, in the order Instancing lists the Agents: `noble_1` to `noble_6`, `hothead_1`, `hothead_2`, `knight_1`, `servant_1` to `servant_3`. Every Target uses these names, so a behaviour case names the same Agents on every Target.
- The Root Plot's Director is `director:<Plot>`: `director:RoyalBanquet`.
- A Subplot's Director is always numbered, `director:<Plot>#<n>`, by the order its Staging started among the Stagings of that Plot in this run. The first duel is `director:HonorDuel#1`, whether or not another is running, and `Poisoning`, which only ever has one Staging, is `director:Poisoning#1`. The number is the one `ALSO IN #<n>` gives. The Staging's arguments are on its `STAGING … STARTED` line.
- These numbers exist only in the Trace. Nothing in a run can read them.

Spec: chapter 34, *Entry fields*.

## Why a Plan ran

A Plan's `plan` entry is written when the Plan is chosen, before its first Statement runs. When more than one candidate was in play for the Trigger, it says how the Plan won and over whom. A knight on duty hears gossip about a Guest:

[`plots/royal_banquet.regia`](../showcase/plots/royal_banquet.regia)
```regia
PRECEDENCE:
    Keeping_watch OVER NobleSocializing ON scandal   # a knight on duty is a Guard first
```

```
PLAN Keeping_watch: WHEN scandal(?) GIVEN on_duty AND (NOT seat(?) OR NOT hungry) OVER NobleSocializing: WHEN scandal(noble_2) BY PRECEDENCE
DO watch(hothead_1)
```

| Field | Console | Holds |
|---|---|---|
| `by` | ` BY <how>` | what decided: `SUITS` (fit), `PRECEDENCE`, `NAME` (name order), or `DEFAULT` (a default gave way) |
| `over` | ` OVER <block>, …` | the candidates it beat, each named as a `plan` entry names its Block |
| `fits` | none | for a `SUITS` choice, the fit the Target reported for each alternative |

- A Plan with no rival has neither `by` nor `over`.
- A Plan that lost writes no entry of its own. It is read in the winner's `over`.
- `GIVEN` and `ELSE` siblings are not rivals. The first that holds runs, and the entry shows ` GIVEN <context>` or ` ELSE`. Whether a later sibling would also have held is never tested.
- A Block is named by its owner (the Playbook for an Agent; the Phase or `DURING PLOT` for a Director), its Trigger, and its `GIVEN` Context or `ELSE`. Blocks that still read alike are told apart by `at`.
- A `SHIFTS` Label's `mood` entries come right after the `plan` entry and point at it with `plan: <seq>`.

*Precedence and Labels* shows a `SUITS` choice among three ways to take an insult.

Spec: chapter 34, *Why a Plan ran*. For the mechanisms, chapters 13 and 14.

## What didn't run

"Why did nothing happen" is the question most often asked of a run. When something arrives with a Sender and no Plan runs for it, the Trace writes an `unheard` entry at level `info`, with its code.

[`playbooks/noble_socializing.regia`](../showcase/playbooks/noble_socializing.regia)
```regia
TO vent:
    GIVEN grudge(?foe, ?size) AND ?foe PLAYS peer, WEIGHT ?size:
        DO sneer_at(?foe)
        TELL ?foe insulted
        TELL EVERYONE scandal(?foe)
```

`TELL EVERYONE` reaches the Servants too. `Serving` has no Plan for `scandal`, so each Servant writes one entry and does nothing else:

```
UNHEARD T0702 scandal(noble_2) FROM hothead_1
```

A Director writes the same kind of entry for a Signal its current Phase doesn't hear. `insult_thrown` is Signalled from `NobleSocializing`, which the Guests hold from `reception` on, but `RoyalBanquet` has a Plan for it only in `feast`. An insult during the reception is written down and nothing follows:

```
UNHEARD T3801 insult_thrown(hothead_1) FROM noble_4 IN reception
```

The third case is a Subplot's own ending that no Plan of the parent hears. The banquet hears every duel's ending with `WHEN HonorDuel(?) ENDED`, so it never writes one. Without that Plan, a duel abandoned would be:

```
UNHEARD T3802 HonorDuel(hothead_1) FINISHED WITH duel_abandoned IN feast
```

- An `unheard` entry is not a warning. A Phase that ignores a Signal, or a Playbook taken away before its Cue arrives, is often what the writer meant. A behaviour case may list the entry, and need not.
- Three things write nothing when nobody hears them: a game percept, the ending of a Goal some Agent asked for, and a `DROPPED` Subplot. Most asked Goals aren't listened to, and a parent caused the drop it would hear.
- A told Fact is never unheard. It is a `fact` entry whether or not a Plan reacts to it.

**Checks**

- A told Cue for which no Plan of the receiver's given Playbooks runs → `T0702` (Trace, `unheard`)
- A Signal with no Plan in the Director's current Phase or `DURING PLOT` → `T3801` (Trace, `unheard`)
- A Subplot's own ending with no `FINISHED` or `ENDED` Plan in the parent's current Phase or `DURING PLOT` → `T3802` (Trace, `unheard`)

Spec: chapter 34, *What didn't run*. For each case, chapters 07 and 38.

## The failure chain

A Guest the game has laid no seat for:

[`playbooks/courtesy.regia`](../showcase/playbooks/courtesy.regia)
```regia
TO take_seat, FROM DIRECTOR:
    GIVEN seat(?place):
        DO walk_to(?place)               # waits until we have arrived
        DO sit_down
        TELL host greeting
    # no ELSE: with no seat laid for us, take_seat fails at once

WHEN take_seat FAILED:
    DO stand_by(wall)
```

```
#44 FAILURE T1104 GOAL take_seat: no applicable TO Plan
#45 GOAL take_seat FAILED because #44
#46 PLAN Courtesy: WHEN take_seat FAILED
#47 DO stand_by(wall)
```

A Failure spreads one level at a time, and the Trace writes it the same way: one cause, then one entry per level, each pointing at the cause.

- The cause is the Failure's one `failure` entry, written once. Its `at` is the Statement, and its `code` is the cause. A `FAIL WITH` adds the Reason with its arguments: `FAILURE T1103 FAIL WITH sold_out(pie)`.
- Each Pursuit that fails, the one where the cause happened included, writes `GOAL … FAILED` at level `error`, with `because` pointing at the cause. A failing recipe has no entry of its own: its Goal's is its entry.
- A waiting `WHEN` Plan that fails in turn has no Goal, so it writes `PLAN … FAILED` at level `error`, with the same `because`.
- The Reason is written once, on the cause, and read from there.
- Telling an asker how its Goal ended writes no entry. The asker's Plan for it, if it has one, is a `plan` entry.
- Each level is written as it happens, so the chain can be read while the run goes on.

The pie that runs out, three levels deep, is in *Goals and Failure*.

### When a Director's Plan fails

A Director Plan that fails stops there, and its Phase and Staging are untouched. The Trace writes the cause, then a warning naming the Plan. If the game refuses to open the doors:

```
#40 DO open_doors
#41 DO open_doors REFUSED
#42 FAILURE T1101 DO open_doors refused
#43 WARNING T2002 PLAN arrival: WHEN ENTERED
```

The banquet stays in `arrival` and goes on counting seats.

### A drop is not a Failure

[`playbooks/duelling.regia`](../showcase/playbooks/duelling.regia)
```regia
WHEN yielded, FROM opponent:
    DROP strike                          # no more lunges at a beaten opponent
    DO salute
    SIGNAL duel_won
```

```
#212 PLAN Duelling: WHEN yielded
#213 GOAL strike DROPPED
#214 DO salute
```

A `DROP` stops Pursuits below and above the dropped one, and none of them writes a `failure` entry:

- The dropped Pursuit writes `GOAL … DROPPED`, with the `at` of the `DROP`.
- Each Pursuit stopped in turn writes its own `GOAL … DROPPED`, with `because` pointing at the first.
- A waiting `WHEN` Plan stopped by the drop writes `PLAN … STOPPED`, with the same `because`.
- All of them are at level `info`.

**Checks**

- A Goal no recipe takes → `T1104` (Trace, Failure)
- `FAIL`, with its Reason → `T1103` (Trace, Failure)
- A `DO` the game refuses, or a waiting `DO` it reports as failed → `T1101` (Trace, Failure)
- A Director Plan that failed → `T2002` (Trace warning, after the entry of its cause)

Spec: chapter 34, *The failure chain*, *A drop is not a Failure*. For what fails and how it spreads, chapter 11; for Directors, chapter 20.

## Trace codes

Every runtime warning, every Failure cause and every kind of `unheard` entry has a stable Trace code: `T`, the spec chapter's two digits, then two digits numbering it within the chapter. `T0902` is chapter 09's second. Codes follow the rules of Diagnostic codes (*The Transpiler*): a code is never reused, and one that is dropped is marked retired.

- Each spec chapter that defines a runtime warning, a Failure cause or an `unheard` entry lists its codes in a `## Trace entries` section.
- A Target numbers its own entries in its own chapters: a lost game link, a Giving for a Playbook the Agent's files don't hold, and so on (*Jason: the game and the Trace*).
- A behaviour case matches codes, not wording, so a message can be improved without breaking a case.
- Three codes are entries that are neither Failures nor warnings, because what they mark can be meant: `T0902`, `T0903` and `T2601`. Like an `unheard` entry, they need not be listed in a case.

The codes a 1.5 run can write, from the language chapters:

**Checks**

- Body arithmetic on something that isn't a Number → `T0401` (Trace, Failure); a division by zero → `T0402` (Trace, Failure)
- A whole roll with no whole number between its bounds, in a Body → `T0403` (Trace, Failure)
- A recipient Placeholder that doesn't hold an Agent → `T0701` (Trace, Failure)
- A told Cue no Plan runs for → `T0702` (Trace, `unheard`)
- `UPDATE f TO f2` when `f` isn't known → `T0801` (Trace, Failure)
- A Weight that isn't a Number → `T0901` (Trace, Failure)
- A negative Weight, counted as 0 → `T0902` (Trace entry); every Weight 0 or less, no Option runs → `T0903` (Trace entry)
- A `DO` refused, or reported as failed while it waits → `T1101` (Trace, Failure)
- `FAIL` → `T1103` (Trace, Failure)
- A Goal no recipe takes → `T1104` (Trace, Failure)
- A Duration that isn't a Number → `T1201` (Trace, Failure); a negative one, counted as 0 → `T1202` (Trace warning)
- A count or share that isn't a Number → `T1501` (Trace, Failure)
- A count asking for more Agents than are left → `T1502` (Trace warning); a negative count → `T1503` (Trace warning)
- An `EXCEPT ?who` that doesn't hold an Agent → `T1504` (Trace warning)
- A `REMOVE` for one Agent that takes nothing → `T1505` (Trace warning); an `ASSIGN P TO <Role> ?who` with nothing to lift → `T1506` (Trace warning)
- A setup Statement that can't be carried out, skipped → `T1601` (Trace warning)
- A `TELL` or `ASK` to an Agent that has left, dropped → `T1901` (Trace warning)
- A spawn the game reports in a 1.5 run, refused → `T1902` (Trace warning)
- A Giving or Mapping that reaches an Agent who has left → `T2001` (Trace warning)
- A Director Plan that failed → `T2002` (Trace warning)
- Every Match of a weighted Pick weighs 0 or less → `T2601` (Trace entry)
- A Signal no Plan in the current Phase hears → `T3801` (Trace, `unheard`)
- A Subplot's own ending no Plan of the parent hears → `T3802` (Trace, `unheard`)

> **In 2.0** a Quota Trigger has two codes of its own: a warning for a quantity that works out unusable at runtime, and an `unheard` entry for a Quota met with no candidate Block. `T1902` is retired, since a 2.0 run lets the Agent join. Spec chapter 18, *Trace entries*; chapter 19, *Regia 1.5*.

Spec: chapter 34, *Trace codes*. Each code's chapter, in its `## Trace entries` section.

## The console

```
#57 DO walk_to(seat_3) DONE  playbooks/courtesy.regia:11:13
#58 DO sit_down  playbooks/courtesy.regia:12:13
```

The console line is written as the entry is. `seq` comes first, so a line leads to its entry in the file, and the source location last. Who wrote it is shown by the Target's console, which puts each Agent's and each Director's lines under its name.

`regia run --console` sets how much of the Trace the console shows, and never touches the file:

| `--console` | The console shows |
|---|---|
| `all` (the default) | every entry |
| `warnings` | `warning` and `failure` entries only |
| `off` | nothing |

The file always gets every entry. On Jason it is one JSON object per line, in a new file for each run, under the Build folder (*Jason: the game and the Trace*).

Spec: chapter 34, *The console line*. For `--console`, chapters 23 and 35.

## Behaviour cases

A behaviour case is a test of a run. It plays the game's side by a script and states the entries it expects. It is a Conformance case like a check case (*The Transpiler*), always a folder, with a `.regin` Entry naming its `ROOT` and one `.trace` file. Here is one for the Guest by the wall, with a throwaway cast of two:

```regia
# cases/no_seat/no_seat.regin
IMPORT "../../plots/royal_banquet"

ROOT RoyalBanquet

AGENT king, PLAYS Host

KIND noble, PLAYS Guest:
    COUNT 1
```

```
#! case: with no seat laid, a Guest stands by the wall and is counted all the same
#! rule: 11 When no Plan applies
> start
king: FAILURE T1104 GOAL take_seat: no applicable TO Plan
noble_1: FAILURE T1104 GOAL take_seat: no applicable TO Plan
noble_1: GOAL take_seat FAILED
noble_1: DO stand_by(wall)
> action done stand_by(*)
noble_1: DO stand_by(wall) DONE
director:RoyalBanquet: PLAN arrival: WHEN took_seat
director:RoyalBanquet: PHASE arrival -> reception ON WHEN took_seat
```

The `.trace` file holds both the script and the expected entries, interleaved, and reads top to bottom like the story of the run. Lines starting with `>` are script steps. Every other line is an expected entry: the agent, a colon, and the console line's text without `seq` and source location.

- The case gives no seats. A `fact` step to an Agent can only come after `> start`, and by the time the run has settled after it, every setup's `take_seat` has already been tried. In a case, every Guest starts without a seat.
- The king has no seat either, and its Failure must be listed. Every `failure` and `warning` entry has to be expected, or the case fails.
- `noble_1: GOAL take_seat FAILED` has no `because`. The order of the lines shows the chain.
- The Guest's `WHEN take_seat ENDED` Plan runs only once its `WHEN take_seat FAILED` Plan has finished, and that one waits on `stand_by`, which the stand-in holds. So the script finishes it, and only then can the Guest Signal `took_seat`. The case doesn't list the Signal itself: the Director's `PLAN arrival: WHEN took_seat` shows the Guest was counted.
- The case ends once the run settles after its last step. The reception's `AFTER 2 MINUTES` is still waiting, and never fires.

Spec: chapter 34, *Behaviour cases*. For case folders, chapter 27, *Case files*.

### The script

The game is played by a stand-in during a case, and each step tells it what to do:

| Step | Does |
|---|---|
| `> start` | starts the run; always the first step |
| `> cue noble_2 idle` | the game sends a Cue to one body |
| `> fact noble_1 +hungry`, `> fact noble_1 -hungry` | the game reports to one body a Fact holding, or no longer holding |
| `> cue link poison_drunk`, `> fact link +in_stock(pie)` | the same, sent once to the Directors |
| `> cue * idle`, `> fact * -in_stock(pie)` | the same, to every body that uses the item, and once to the Directors if any Director's Plot uses it |
| `> leave noble_4` | an Agent leaves the Program |
| `> join noble noble_7` | an Agent of this kind joins the Program |
| `> action fails walk_to(*)` | from now on, matching Actions are accepted, then fail |
| `> action refused pick_up(pie)` | from now on, matching Actions are refused |
| `> action holds eat(*)` | from now on, matching Actions are accepted and left unfinished |
| `> action succeeds walk_to(*)` | back to the default for the pattern: done at once |
| `> action done eat(*)`, `> action failed eat(*)` | finishes, or fails, every held Action matching the pattern |
| `> wait 30 seconds` | moves the clock forward |
| `> pause`, `> resume` | the game pauses or resumes the clock; a second `> pause` does nothing |
| `> lose link` | the game's connection to the Directors closes |

- A Cue or Fact step names who receives it: an Agent as the Trace names it, or `link` for the Directors. `<name>` is the item's Regia name.
- The game never names a Director. A `link` step reaches every running Director whose own Plot hears the item, and none that doesn't. `> cue link poison_drunk` reaches `director:Poisoning#1` while the poisoning runs; before it starts, nobody hears it, and it is dropped with no entry, as in a real run.
- `*` reaches every receiver that uses the item: each Agent whose files list it, and `link` if any Director's Plot does, all within the one step. Its `script` entry lists the receivers reached, with `link` last when it went out on the link: `> cue * idle -> noble_1, noble_2, …`.
- A step that names an Agent that is there but doesn't use the item is still sent, and the receiver writes the Target's warning for an unknown percept, as in a real run.
- The game remembers the Facts it reported on the link and the Agents that left, and answers from them when a Director starts. `> fact link +…` steps written before `> start` send nothing: they set the Facts true when the run starts, so the first Director starts with them, and `LEARNED` doesn't fire for them.
- Action rules match game Actions by name and arguments, never by who sent them, and each replaces the previous rule for its pattern. An Action with a dotted External name is the Target's own code. It runs for real, and no rule holds it or makes it fail.
- `> lose link` makes the Target write its lost-link entry. Every Director Action still in flight fails with the reason `no game link`, a paused clock starts again, and every later Director `DO` fails at once. `#! game link: none` in the header starts the run with no game on the link: the Target writes its entry at start, and every Director starts with no game Facts. Agents' bodies are never lost in a case.
- A step runs once the run has settled: every running Plan has finished, waits in a `WAIT`, or waits on a held Action, and nothing is on its way. Then the step is played and its `script` entry written.

> **In 2.0** a case can have an Agent join with `> join`. Such a case is marked `#! regia: 2.0`. Spec chapter 34, *Regia 1.5*; chapter 27, *Annotations*. In a 1.5 run, `> join` is refused with a warning, and a case that checks that refusal is marked `#! regia: 1.5`.

**Checks**

- A step that names an Agent the run never had, or one that has left → case error (nothing is sent, the run stops, nothing is matched)
- A step with no receiver, such as a `*` step for an item nobody uses → case error
- A step before `> start` other than `> fact link` → case error
- A `link` step, or a `*` step that would reach the link, after `> lose link` or under `#! game link: none` → case error
- `> join` in a 1.5 run → `T1902` (Trace warning)

Spec: chapter 34, *The script*. For the stand-in game and the Target's entries, chapter 35.

### Time, chance and order in a case

Three things a real run leaves to chance are fixed in a case:

- Time is virtual. The clock moves only when the run has settled and something is waiting, and then it jumps straight to the next wake-up. `> wait` moves it on by hand. A long `WAIT` costs nothing, and wake-ups always come in the same order. While the case has paused the clock it doesn't jump, and a run settled with only those waits goes on to the next step.
- Randomness is seeded: `#! seed: <n>` in the header, else the Build's `SEED`, else 1. The seed covers every draw the language makes: `RANDOM`, `RANDOMLY`, every Pick that draws, the Agents drawn by `n OF` and `n% OF`, and starting Propensity values. The same seed draws the same way every run.
- Agents step together, one reasoning step each at a time, so the order inside one Agent doesn't depend on thread timing.

Spec: chapter 34, *The script*. For the seed, chapter 21.

### Expected lines and matching

```
#! case: an insult during the reception starts no duel
#! rule: T3801
#! seed: 7
```

A case's header lines start with `#!`: `case:` (what it shows, in one line), `rule:` (the section or code it exercises; several lines allowed), `seed:`, `exactly`, `game link: none`, and `regia:`. Plain `#` comments are allowed anywhere.

An expected line matches an entry by its agent and its console text:

- `*` stands for any one argument: `noble_1: DO walk_to(*)`.
- A `failure`, `warning` or `unheard` line matches on its code. The words after it are for the reader.
- `because` links aren't written. The order of the lines shows the chain.
- A line may end with `at <file>:<line>` to check the source location as well.

A case passes when the run's Trace matches its expected lines:

- The `>` steps are barriers. The lines between two steps match entries written between those two steps' `script` entries. That is the only order between different Agents.
- For each Agent, the expected lines between two steps must appear among its entries in that order. Other entries may come in between, so a case states only what its rule is about.
- Every `failure` and `warning` entry must be expected. An unexpected Failure fails the case, since its cause is always a `failure` entry. The `error`-level `GOAL … FAILED` and `PLAN … FAILED` entries above it may go unlisted, like any other extra, and so may `unheard` entries.
- `#! exactly` turns extras off: every entry but `run` and `script` must be listed.

A case that doesn't match is a failing test, not a Diagnostic: the Trace has no Transpiler checks.

Spec: chapter 34, *Expected lines*, *Matching*, *Transpiler checks*. For the header, chapter 27, *Annotations*.

## How this combines with…

### Goals and Failure

A `FAILED` Plan reacts to a Failure without learning its cause. It reads only the Reason; which Statement failed and how is in the Trace alone, as the cause's code and `at`. (*Goals and Failure*)

### Precedence and Labels

`OVER` and `BY` are where the order of Plans shows at runtime, and `regia explain`'s conflict report is where it shows at build. A `SUITS` choice adds the fit of each alternative, so a surprising temper can be traced to the numbers. (*Precedence and Labels*)

### Randomness

The `run` entry records the seed, whichever way it came. Which Option ran isn't an entry of its own; the Trace shows it through what the Option did. (*Randomness*)

### Actions and time

Every `DO` writes two entries, the send and the outcome, linked by `of`. A `DO … , WITHOUT WAITING` whose outcome comes back after its Body has moved on still writes it. Each `WAIT … UNTIL` writes a `time` entry when it ends, met or timed out, and so does each pause and resume. (*Actions and time*)

### Messages

A Message is written once, by its sender, as a `message` entry. What the receiver did with it is in the receiver's own entries. (*Messages*)

### Subplots and Stagings

Each Staging's start and end is a `staging` entry, and each Subplot Director has its number from the moment its Staging starts. An Agent cast in two Stagings of one Plot is marked `ALSO IN` on the second. (*Subplots and Stagings*)

### When an Agent leaves

A leave is a `cast` entry, `LEFT noble_4`, whether or not a Plan hears it. A case plays it with `> leave noble_4`, and from then on naming `noble_4` in a step is a case error. (*When an Agent leaves*)

### The Transpiler

`regia test` runs behaviour cases, the spec's and our own, and runs only those whose `regia:` line fits its build. `regia run --seed` starts a run with a given seed, and `--console` sets how much the console shows. (*The Transpiler*)

### Jason: the game and the Trace

On Jason, one writer hands out `seq` and writes both the file and the console. A source map turns ASL locations and Generated names back into `.regia` ones, and a scripted stand-in game plays the case's steps. (*Jason: the game and the Trace*)
