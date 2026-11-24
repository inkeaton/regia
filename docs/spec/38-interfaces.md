# Interfaces

What passes between a Playbook and the Plots that give it, and between a Subplot and its parent: how the Transpiler works it out, what it checks, and what the Trace says when something sent finds no Plan. Decided in the ticket *What passes between a Playbook and a Plot* (`.scratch/regia-revision/issues/01-playbook-plot-interface.md`), recorded in ADR 0015. It builds on chapters 05, 07, 10, 15, 17 and 20. Reasons and the endings an asking Agent hears were added by the ticket *Failure a Plan can read, and answers to an `ASK`* (`.scratch/regia-revision/issues/03-failure-and-replies.md`).

## Nothing is declared

A Playbook declares its Roles and a Plot its Roles and Phases. Neither declares what it sends or answers. The **Interface** of a Playbook or a Plot is worked out by the Transpiler from the whole Program, and checked one side against the other.

```regia
PLAYBOOK Keeping_watch:
    WHEN saw_pouring(?who):
        DO seize(?who)
        SIGNAL culprit_seized(?who)        # part of the Interface: a Signal

PLOT RoyalBanquet:
    ROLE Guard
    DURING PLOT:
        WHEN ENTERED:
            ASSIGN Keeping_watch TO Guard      # warning R3801: `culprit_seized` has no Plan here
```

- There is no `SIGNALS`, `ANSWERS` or `OUTCOMES` line, and no marker on a `CUE` declaration that says which part of the Program sends it. The one marker is `GAME` (chapter 10), which says the game produces it: the Transpiler can't see the game, so that can't be inferred.
- The Interface is not source. It can't be written, imported or edited; it changes when the Bodies change.
- It is printed by `regia explain <entry> interface <Playbook or Plot>` (chapter 23). From a `.regia` Entry, it shows what that file and its imports say, with no Root Plot.

## The Interface of a Playbook

| Part | Read from |
|---|---|
| Its Roles | the `ROLE` lines (chapter 15) |
| The Goals it answers, and from whom | every `TO g:` Trigger with its `FROM`, local Goals left out |
| The Cues and Facts it reacts to when told, and from whom | every `WHEN` Trigger with a `FROM` |
| The Reasons each Goal it answers can fail with | every `FAIL WITH` in a recipe of the Goal, and in the recipes of the Goals it waits on |
| What it tells and asks, and to which recipient | every `TELL` and `ASK … TO` |
| The asked Goals whose endings it hears, and with which Reasons | every `WHEN g REACHED`, `DROPPED`, `FAILED` or `ENDED` Plan with `BY` (chapter 05) |
| The Signals it sends | every `SIGNAL` |

A Trigger with no `FROM` is listed as open to anyone (chapter 05). A local Cue (chapter 10) is listed with the Playbook's own name beside it, since no other Playbook can use it.

## The Interface of a Plot

| Part | Read from |
|---|---|
| Its Roles | the `ROLE` lines |
| Its parameters | the `PLOT` header (chapter 17): declared, the one part of a Plot's Interface that is |
| The Playbooks it gives, to which Role, with which Mappings | every `ASSIGN` and Role setup |
| The Signals it handles, and in which Phases | every `WHEN e` Plan, by `DURING` Block |
| What its Director tells and asks | every `TELL` and `ASK … TO` |
| The asked Goals whose endings it hears, with which Reasons, and in which Phases | every `WHEN g REACHED`, `DROPPED`, `FAILED` or `ENDED` Plan, by `DURING` Block (chapter 20) |
| Its endings | every `END PLOT`, with its Outcome or plain |
| The Subplots it starts, and the endings it matches | every `START SUBPLOT`, and `WHEN P FINISHED`, `DROPPED` and `ENDED` |

## Who sends a Cue

For each Cue the Program declares, the Interface gives its **senders**, worked out from use:

- **told**, when some `TELL` sends it;
- **Signal**, when some `SIGNAL` sends it;
- **Outcome**, when some `END PLOT WITH` ends with it;
- **Reason**, when some `FAIL WITH` gives it;
- **from the game**, when it is declared `GAME CUE` (chapter 10).

A Cue can be in several groups, the game included: a game Cue that Agents also tell is listed as both. A Cue in no group can never fire, and a Trigger on it is a warning (`R3807`, below).

## Checks

All six are warnings. Each has a correct Program it would wrongly reject as an error: a Playbook given by two Plots, an Agent that plays two Roles, a recipe held from another Plot.

### A Signal the giving Plot never handles

When a Plot gives a Playbook, and the Playbook sends a Signal for which the Plot has no `WHEN` Plan in any Phase or in `DURING PLOT`, the Transpiler warns on the giving Statement. The message names the Signal and the Playbook.

The check is exact, because a Signal reaches only the Directors of the Plots that give the Playbook (chapter 07).

### A Signal handled in some Phases only

There is **no build check**. Telling which Givings stand in which Phase would need every `ASSIGN`, `REMOVE` and `ENTER` followed, and the answer often depends on the run. The Interface lists the Phases that handle each Signal, and the Trace reports a Signal that finds no Plan (below).

### A Director Plan no Signal can reach

`WHEN e, FROM <Role>:` or `WHEN e, FROM ?who:` in a Plot, where no Playbook the Plot gives sends `e` as a Signal, can never run: nothing from the game has a Sender (chapter 05). The Transpiler warns on the Trigger.

A Trigger with no `FROM` is not checked here, since the Cue may come from the game. A Cue that nothing sends at all, the game included, is the next check.

### A Cue nothing sends

`WHEN challanged:` waits for a Cue that isn't `GAME` and that no `TELL`, `SIGNAL`, `END PLOT WITH` or `FAIL WITH` of the Program sends. It can never fire, and the Transpiler warns on the Trigger (`R3807`), with the hint to declare it `GAME CUE` if the game is meant to send it.

### An `ASK` or `TELL` that no `FROM` admits

```regia
DURING feast:
    WHEN ENTERED:
        ASSIGN Dining TO Guest, MAPPING Servant AS waiter
        ASSIGN Serving TO Servant, MAPPING Host AS patron      # warning R3803
```

`Dining` writes `ASK waiter TO bring(…)`, and `Serving` answers `TO bring(…), FROM patron`. With `patron` mapped to `Host`, no Guest's request is ever admitted.

Within one Plot, the Transpiler follows each `ASK` and `TELL` of a given Playbook, and each of the Director's own, by Role name: which Plot Role sends, which Plot Role receives, which Plans for that Goal, Cue or Fact the receiving Role is given by this Plot, and which Plot Roles their `FROM` admits. It warns when the receiving Role is given at least one such Plan and none admits the sender.

- Only the Playbooks this Plot gives are counted. A Plan from another Plot, or from the Agent's kind (chapter 21), is not seen.
- When the receiving Role is given no Plan at all for the item, nothing is reported here. For a Goal, that is chapter 11's failure at runtime.
- A recipient held in a Placeholder, and `EVERYONE`, are not followed. `CAST` is followed as every Role of the Plot, and a Role with a count or an `EXCEPT` as the Role itself.

### A Reason the Goal never fails with

`WHEN g FAILED WITH r` is checked against the Reasons `g` can fail with: every `FAIL WITH` in a recipe of `g`, and in the recipes of the Goals those recipes wait on, followed through the Program. When no recipe the Transpiler can see fails `g` with `r`, it warns on the Trigger.

- For a Trigger without `BY`, the recipes are those the Program holds for `g`. For one with `BY`, in a Playbook or a Plot, they are the same: which Agent holds which recipe is not followed.
- Nothing is reported the other way. A Reason that no Plan reads is normal: plain `FAILED` covers it.

### A request no recipe's `FROM` admits

```regia
PLAYBOOK Seating:
    TO take_seat, FROM DIRECTOR:
        ...

PLAYBOOK Mingling:
    WHEN tired:
        PURSUE take_seat           # warning R3805
```

An Agent's own `PURSUE` is `FROM ME` and never takes the Sender of the Plan it is written in (chapter 05). When the Program holds recipes for `g` and **none admits `ME`** (each has a `FROM`, and `ME` is not among its alternatives), a `PURSUE g` can only fail at once, and the Transpiler warns on it. The hint is `FROM … OR ME`.

- This is how a recipe that repeats under `TO g, FROM DIRECTOR:` is reported (chapter 08).
- The other way round, an `ASK … TO g`, from an Agent or a Director, when every recipe of `g` in the Program is `FROM ME` alone, is a warning on the `ASK`.
- Both look at the whole Program, not at which Playbooks an Agent holds. A Goal with no recipe at all is not reported here.
- A setup's `PURSUE` is the Director's (chapter 16) and is checked as an `ASK`.

## Transpiler checks

**Warnings**

- `R3801` A Plot gives a Playbook that sends a Signal the Plot has no Plan for, in any Phase.
- `R3802` `WHEN e` with any `FROM` (a Role or `?who`) in a Plot where no Playbook the Plot gives Signals `e`.
- `R3803` A Plot's Mappings leave an `ASK` or `TELL` with no receiving Plan whose `FROM` admits the sender's Role.
- `R3804` `WHEN g FAILED WITH r` where no recipe of `g`, or of a Goal it waits on, fails with `r`.
- `R3805` A `PURSUE g` where no recipe of `g` in the Program admits `ME` (hint: `FROM … OR ME`).
- `R3806` An `ASK … TO g`, or a setup's `PURSUE g`, where every recipe of `g` in the Program is `FROM ME`.
- `R3807` A Cue that isn't `GAME` (chapter 10) and that no `TELL`, `SIGNAL`, `END PLOT WITH` or `FAIL WITH` in the Program sends, while some Trigger waits for it. Reported on each such Trigger (hint: declare it `GAME CUE` if the game sends it). A local Cue is checked within its Playbook.

An ending the parent never matches is `R1708` (chapter 17). A Goal-ending Trigger in a Plot that never asks the Goal is `R2012` (chapter 20); with `BY` in a Playbook that never asks it, `R0508` (chapter 05).

## Trace entries

**Unheard** (`info`, chapter 34). They were warnings until the ticket *What the Trace records* (ADR 0037): a Phase that ignores a Signal is often what the writer meant.

- `T3801` A Signal that reached a Director with no Plan for it in the current Phase or in `DURING PLOT`. The entry names the Cue, the sending Agent, the Plot and the Phase.
- `T3802` A Subplot's own ending that no Plan of the parent heard (no `FINISHED WITH` Plan for its Outcome, no plain `FINISHED` and no `ENDED`), in the current Phase or in `DURING PLOT`. The entry names the Subplot, the Outcome (or says the ending was bare) and the parent's Phase. A `DROPPED` ending with no Plan writes no entry: the parent caused it (chapter 17).

Neither is a Failure. The sender is not told, its Plan goes on, and the Director does nothing. The ending of an asked Goal that finds no Plan writes no entry, at a Director or at an asking Agent (chapters 05, 20).

## Notes for the ASL mapping

- Each Director needs a catch-all for a Signal and for an `ended(Plot, Outcome)` message that no Plan of the current Phase takes, which writes the Trace entry and nothing else, and one for a `dropped(Plot)` that writes nothing. The Signal's catch-all in Jason is in chapter 30 (*Signals*).
- A game Cue with no Plan writes no entry: only what arrives with a Sender as a Signal, and endings, are reported.

## Regia 1.5

In 1.5 (ADR 0025), except the rows of the asked Goals whose endings a Playbook or a Plot hears. They are always empty in 1.5, since `BY` and a Plot's Goal endings are later. `R3805` and `R3806` are later too, and never reported. `R3801` to `R3804` and `R3807` are in.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- How the Visual Editor draws an Interface: *The Visual Editor* (`.scratch/regia-revision/issues/18-visual-editor.md`).
- Telling the Givings of one Playbook apart, so that a Signal reaches one Director: *Givings and joiners* (`.scratch/regia-revision/issues/05-givings-and-joiners.md`).
- Conformance cases for the codes above.
