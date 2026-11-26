# Goals and Triggers

What Goals are, how they are declared, and every kind of Trigger a Plan can start from. Decided in the ticket *Goals and Trigger kinds* (`.scratch/regia-2/issues/05-goals-and-trigger-kinds.md`). It builds on *Parameters and Placeholders* (`03-parameters-and-placeholders.md`) and replaces the Goal and trigger-type parts of primer ch.2–4. The choice to treat Fact changes and Goals as Trigger kinds, with Cues kept momentary, is recorded in `docs/adr/0003-events-are-momentary-fact-changes-are-trigger-kinds.md`. Pursuits, the `REACHED` and `ENDED` Trigger kinds and what a Director hears of a Goal were revised in the ticket *A Goal's life: reached, dropped, repeated* (`.scratch/regia-revision/issues/02-goal-lifecycle.md`), with ADR 0017. The `BY` clause, and `WITH` on `FAILED`, were added in the ticket *Failure a Plan can read, and answers to an `ASK`* (`.scratch/regia-revision/issues/03-failure-and-replies.md`), with ADR 0019. `EVENT` was renamed `CUE`, and **Event** became the general word for what starts a Plan, in the ticket *Words that do several jobs, and syntax nobody used* (`.scratch/regia-revision/issues/20-words-and-syntax.md`), with ADR 0039. `FROM` and `BY` became clauses written after a `,` in the ticket *The comma* (`.scratch/syntax-review/issues/02-the-comma.md`), which applies ADR 0041.

In the examples, the Context is written as the `IF` directly under the Trigger, as in chapter 03. Chapter 06 (`06-context-and-control-flow.md`) replaces this with `GIVEN`.

## Goals

A **Goal** is an objective an Agent pursues. Regia 2.0 has only one kind: a Goal the Agent tries to *reach*, and then stops pursuing (an *achievement* goal in BDI terms). There are no test goals; matching in a Context already does that job. Goals that must be *kept* true, or that are reached when a Fact holds, are not part of 2.0.

### Declaring Goals

Goals are declared like every other Vocabulary item, with untyped parameter names (chapter 03) and multi-definition:

```regia
GOAL find_food
GOAL avenge(person)
GOAL get_fed, find_shelter
```

### One name, one kind

A Vocabulary name belongs to exactly one kind. Declaring `FACT fed` and `GOAL fed` is an error. A Goal and the Fact that tells it is done get two names: `GOAL get_fed`, `FACT fed`. A name also has one parameter count, across the whole Program (chapter 10, ADR 0006).

### Who gives a Goal

An Agent can be given a Goal by:

- **itself**, with a Basic Action in a Body;
- **the Director** of a Plot, with a Director Statement;
- **another Agent**, with a message.

Another Agent writes `ASK ?who TO g` (chapter 07). The Agent itself writes `PURSUE g` (chapter 08); the Director writes `ASK ?who TO g` or `ASK Role TO g` (chapter 20).

### Reaching a Goal

A Goal is **reached when a Plan for it finishes its Body**. Nothing checks the world. `WHEN g REACHED` then fires (see *How a Pursuit ends*).

If no Plan for the Goal applies, or its Plan fails, the Goal **fails** and `WHEN g FAILED` fires (chapter 11, `11-failure.md`).

### Pursuits

Every request to pursue a Goal starts a **Pursuit**: one run of the Goal by one Agent, from the request to its ending, with its own Sender. A request is a `PURSUE`, an `ASK` from another Agent or from a Director, or a Role setup's `PURSUE`.

**Nothing is ignored and nothing is joined.** An Agent asked for `bring(roast)` by two Guests has two Pursuits of `bring(roast)`, each with its own Sender, each running a recipe, each ending by itself. Arguments say what is wanted; they are not what keeps two Pursuits apart (ADR 0017).

```regia
TO bring(?dish), FROM patron ?guest:      # runs once per order, also for two orders of one dish
    PURSUE fetch(?dish)
    DO walk_to(?guest)
    DO put_down(?dish)
```

A Goal that must not run twice at once says so in its Context:

```regia
TO have_dinner:
    GIVEN NOT PURSUING have_dinner:      # another Pursuit of it; this one doesn't count
        ...
```

With that `GIVEN` and no `ELSE`, a second request falls through (chapter 13), and if no other recipe takes it, it fails at once (chapter 11) and fires `FAILED` with its own Sender.

### Waiting for a Goal

A Body that pursues a Goal can either **wait** until it is reached and then continue, or **start it and carry on**. Both exist. `PURSUE g` waits and `PURSUE g, WITHOUT WAITING` carries on (chapter 08). A Goal given to another Agent never makes the giver wait.

### Testing Goals in a Context

A Context can ask whether the Agent is currently pursuing a Goal, with `PURSUING`. Matching and Placeholders work as for Facts:

```regia
WHEN food_smelled:
    IF is_hungry AND NOT PURSUING find_food:
        ...

WHEN insult_heard(?s):
    IF PURSUING avenge(?s):          # already after them
        ...
```

- `PURSUING g` holds while at least one Pursuit of `g` has a recipe running.
- In the Context and the Body of a `TO g` Plan, **the Plan's own Pursuit doesn't count**: `PURSUING g` there asks about another Pursuit of `g`. Everywhere else, including the recipe of a sub-Goal, every Pursuit counts.

## Cues are momentary

A **Cue** (`CUE food_served`) is something that happens and is over once noticed. It triggers Plans and leaves nothing behind:

- it can't be tested in a Context: `IF food_served` is an error;
- it can't be added with `LEARN` or removed with `FORGET`;
- a Plan that needs to remember it records a Fact.

A Fact lasts until it is forgotten, and a Context can test it at any time. Both can trigger Plans: a Cue when it happens, a Fact when it is learned or forgotten.

A Signal is a Cue that an Agent sends to a Director. The Director reacts to it like any other Cue.

`CUE` is the keyword that declares one. `EVENT`, its spelling before 2.0, is an error with the hint "renamed `CUE`" (`R0513`).

## Events

An **Event** is anything that happens to an Agent or a Director and can start a Plan: a Cue, a Fact learned or forgotten, a Goal pursued or over, a Phase entered or left, a Playbook given or taken away, a Role joined, left or emptied, a Phase's timeout. A Trigger names one Event, and each sort of Event is a Trigger kind (below). This is the meaning a *triggering event* has in Jason, so an Event and the Target's event are the same thing (chapter 28).

## Trigger kinds

Each sort of Event a Plan can start from is a **Trigger kind**. Each is written after `WHEN`, except a Goal recipe, written after `TO`, and a Plot's timeout, written after `AFTER`.

| Trigger kind | Written |
|---|---|
| A Cue happens (including a Signal, at a Director) | `WHEN insult_heard(?s):` |
| A Fact is learned | `WHEN hates(?h) LEARNED:` |
| A Fact is forgotten | `WHEN hates(?h) FORGOTTEN:` |
| A Goal is pursued (a recipe) | `TO find_food:` |
| A Goal is reached | `WHEN find_food REACHED:` |
| A Goal is dropped | `WHEN find_food DROPPED:` |
| A Goal fails | `WHEN find_food FAILED:` (chapter 11) |
| A Goal is over, however it went | `WHEN find_food ENDED:` |
| A Goal fails with a Reason | `WHEN find_food FAILED WITH nothing_left:` (chapter 11) |
| A Goal asked of someone else is over | `WHEN bring(?dish) REACHED, BY Servant ?s:` and the other three (below; for a Director, chapter 20) |
| A Phase is entered or left (Director Plans) | `WHEN ENTERED:`, `WHEN EXITED:` (chapter 20) |
| A Duration has passed since a Phase was entered or the Staging started (Director Plans) | `AFTER 30 SECONDS:` (chapter 12) |
| An Agent joins or leaves a Role, or a Role empties (Director Plans) | `WHEN Guest ?g JOINED:`, `WHEN Guest LEFT:`, `WHEN Guest EMPTIED:` (chapter 19) |
| A Playbook is given to the Agent or taken away (Playbook Plans) | `WHEN ASSIGNED:`, `WHEN REMOVED:` (chapter 15) |

```regia
WHEN hates(?h) LEARNED:
    DO glare_at(?h)

TO avenge(?who):
    IF is_armed:
        DO challenge(?who)

WHEN avenge(?who) DROPPED:
    PRINT("Let it go.")
```

- **Fact Triggers always have a kind word.** `WHEN hates(?h):` is an error; the Transpiler knows `hates` is a Fact and suggests `LEARNED` or `FORGOTTEN`. So a reader never has to look up whether a bare name is a Fact or a Cue.
- **The kind word follows the item**, using a participle: `LEARNED`, `FORGOTTEN`, `REACHED`, `DROPPED`, `FAILED`, `ENDED`. A Trigger with no written item (`WHEN ENTERED:`, `WHEN ASSIGNED:`) has the kind word alone, its subject being this Phase or this Playbook. Both follow chapter 01's rule for where condition words go.
- **`LEARNED` and `FORGOTTEN` fire whatever caused the change**: the game, a message, or the Agent's own `LEARN` and `FORGET`.
- **A kind word must suit the item.** `WHEN food_served LEARNED` (a Cue) or `WHEN find_food LEARNED` (a Goal) is an error.
- **A `TO` Plan is an ordinary Plan**: Placeholders in its Trigger, a Context, Labels and a Body follow the same rules as in a `WHEN` Plan.
- **`WHEN` reacts to an Event.** Plot Phases no longer use `ON ENTER` / `ON EXIT`; Phase entry and exit are `WHEN` Triggers, `WHEN ENTERED:` and `WHEN EXITED:` (chapter 20). The two Triggers without `WHEN` are `TO g:`, a Goal's recipe, and `AFTER d:`, a Phase's timeout (chapter 12), which reads as a time and is still an Event: the Phase's time running out.

## How a Pursuit ends

A Pursuit ends in exactly one of three ways, and each fires its Trigger:

| The Pursuit | Fires |
|---|---|
| is reached: its recipe finishes its Body | `REACHED` |
| is dropped: a `DROP`, or a drop of a Goal it waits on (chapter 08) | `DROPPED` |
| fails (chapter 11) | `FAILED` |

**`ENDED` then fires as well**, once per Pursuit, after whichever of the three fired. A Plan for the specific Trigger and a Plan for `ENDED` both run, in that order.

```regia
WHEN have_dinner FAILED:
    DO complain

WHEN have_dinner ENDED:              # reached, dropped or failed
    DO leave_table
```

- **All four are notifications.** By the time a `REACHED` Plan runs, the Bodies that waited on the Goal have already carried on; for `DROPPED` and `FAILED` they have already stopped. No ending Plan changes how the Pursuit ended (ADR 0007).
- **A Plan for an ending is not a recipe.** If it fails, it stops and leaves a Trace entry. Nothing else fires, so endings can't loop.
- **Along a chain of waiting Plans, innermost first**, each level complete before the next: `fetch DROPPED`, `fetch ENDED`, `bring DROPPED`, `bring ENDED`.
- **Each Pursuit fires its own.** Two Pursuits of `bring(roast)` that are reached fire `REACHED` twice, each with its own Sender.
- Which Plans run for an ending is chapter 13, as for any Trigger.
- `DROPPED` and `ENDED` are also the kind words of a Subplot's endings (`WHEN HonorDuel DROPPED`, `WHEN HonorDuel ENDED`, chapter 17), with the same meaning: `DROPPED` is "stopped on purpose by whoever started it", and `ENDED` is "over, however it went", fired after the specific Trigger (ADR 0030). A Subplot that ends by itself fires `FINISHED [WITH e]`, its counterpart of `REACHED` and `FAILED` (ADR 0047). `ENDED` never takes a complement. A name has one kind, so the item says which is meant.

## Where it came from: `FROM`

A Trigger can say where its item came from with `FROM`. Something that was **sent** (a Signal at a Director, a Goal given by the Director or by another Agent, a Fact or Cue told by another Agent) has a **Sender**. Everything else comes from the game or from the Agent itself, and has none.

| Written | Matches |
|---|---|
| no `FROM` | anything: any Sender, the game, the Agent itself |
| `FROM Guest` | a sender playing the Role `Guest`: in a Plot, in this Staging; in a Playbook, bound to the Playbook's Role `Guest` by any giving (chapter 15) |
| `FROM ?who` | any sender, and fills `?who` with the sending Agent |
| `FROM Guest ?who` | a sender playing `Guest`, and fills `?who` with it |
| `FROM DIRECTOR` | the Director of any Plot that currently gives this Playbook to the Agent |
| `FROM GAME` | what the game sent or reported, and nothing an Agent or a Director sent |
| `FROM ME` | what the Agent caused itself: its own `PURSUE`, `LEARN` or `UPDATE` |
| `FROM a OR b` | any of the alternatives (below) |

```regia
# In a Plot
WHEN insult_thrown(?target), FROM Guest ?who:
    ...

# In a Playbook
TO find_sword, FROM DIRECTOR:
    DO search_armory

WHEN saw_pouring(?rival), FROM GAME:      # seen, not heard from another Agent
    DO seize(?rival)

TO vent, FROM ME:                         # nobody can ask me to
    ...
```

- `?who` follows the Placeholder rules of chapter 03: filled once, by matching. A Director can send it Messages, `ASSIGN … TO ?who` and map it onto a Role (chapter 20).
- `FROM DIRECTOR` is worked out at runtime, so a Playbook never names a Plot and stays Plot-independent. A Goal from a Director whose Plot doesn't give this Playbook doesn't match.
- `FROM` is an error on `FORGOTTEN`. On `LEARNED`, a Sender form matches only a Fact told by another Agent or a Director, and only when the Fact was new (chapter 07).
- On `REACHED`, `DROPPED`, `FAILED` and `ENDED`, `FROM` means **where that Pursuit's request came from**, as on `TO g, FROM …`: `WHEN find_sword FAILED, FROM DIRECTOR:` (chapter 11). The Agent who pursued a Goal that was asked of it is named with `BY` (next section).
- Messages between Agents use these same forms (chapter 07, `07-messaging.md`).
- On a Cue Trigger, a quantity before the Role (`FROM ALL Guest`, `FROM 3 OF Guest`, `FROM 50% OF Guest`) makes a Quota Trigger, which waits until enough different Agents of the Role have sent the Cue (chapter 18, `18-quota-triggers.md`). The same quantities work after `BY`.

### The game and the Agent itself

The game and the Agent itself are **not Senders** (ADR 0020). A Sender form (`FROM Guest`, `FROM ?who`, `FROM Guest ?who`, `FROM DIRECTOR`) never matches what they caused, and `FROM ?who` is never filled with them. `FROM GAME` and `FROM ME` name them:

| Trigger | `FROM GAME` | `FROM ME` |
|---|---|---|
| a Cue, in a Playbook | a Cue from the game | error: an Agent never sends to itself (chapter 07) |
| a Cue, in a Plot | a Cue from the game, not a Signal | error: `ME` is not a word of a Plot (chapter 03) |
| `LEARNED`, in a Playbook | a Fact the game reported | a Fact from the Agent's own `LEARN` or `UPDATE` |
| `LEARNED`, in a Plot | a Fact the game reported | error |
| `TO g`, and a Goal's endings | error: no Goal comes from the game | the Agent's own `PURSUE` |
| `FORGOTTEN` | error, like any `FROM` | error |

- **No `FROM` still matches everything.** A Plan that must not run for what another Agent tells writes `FROM GAME`; a recipe nobody else may start writes `FROM ME`.
- **An own `PURSUE` is from `ME`, wherever it is written.** A Pursuit started inside a recipe the Director asked for is the Agent's own. It doesn't take the Sender of the Plan that started it, so `TO take_seat, FROM DIRECTOR:` doesn't apply to `PURSUE take_seat` and that Pursuit fails at once (chapter 11). A recipe that serves both is written with `OR`, below. The Transpiler warns about a `PURSUE` no recipe admits (chapter 38).
- A Role setup's `PURSUE` and `LEARN` are sent by the Director (chapter 16), so they are `FROM DIRECTOR`, not `FROM ME`.
- `GAME` and `ME` take no Placeholder and no quantity (`FROM GAME ?x`, `FROM 3 OF …`), and neither goes after `BY`.
- `ME` is also a Value, the Agent running the Plan (chapter 03).

### Alternatives: `OR`

`FROM` takes several alternatives joined by `OR`, and matches when any of them does:

```regia
TO take_seat, FROM DIRECTOR OR ME:           # asked by the Director, or pursued by myself
    ...

TO patrol, FROM DIRECTOR OR ME:              # the Director starts it, and it repeats (chapter 08)
    DO walk_to(gate)
    PURSUE patrol, WITHOUT WAITING

WHEN on_duty LEARNED, FROM DIRECTOR OR GAME:
    ...
```

- An alternative is `DIRECTOR`, `GAME`, `ME` or a bare Role. Each must be legal on the Trigger by itself.
- **No Placeholder and no quantity** in an `OR` list: `?who` would be unfilled on the `ME` or `GAME` branch. A Plan that needs the Sender is written as its own Plan.
- `OR` goes on a `TO` recipe, a Goal's endings, a Cue and `LEARNED`. `BY` takes no `OR`.
- This `OR` is the Context operator (chapter 06) applied to who sent it: the Trigger matches when any alternative does. The alternatives are never a `,` list, since a `,` never means OR (chapter 01). Kept in the ticket *`AND`, `OR` and `EITHER`*.

## Who pursued it: `BY`

Whoever asks for a Goal hears how it ended. The Trigger is the Goal's ending with a `BY` clause, which names **the Agent whose Pursuit it was**:

```regia
PLAYBOOK Dining:
    ROLE waiter

    WHEN hungry(?dish):
        ASK waiter TO bring(?dish)

    WHEN bring(?dish) REACHED, BY waiter ?s:     # the bring I asked for was reached; ?s did it
        DO thank(?s)

    WHEN bring(?dish) FAILED, BY waiter:         # the bring I asked for failed
        DO sulk
```

- **`BY` says whose Goal it is.** Without `BY`, an ending Trigger is about a Pursuit of the Agent's own, and `FROM` may say who asked for it. With `BY`, it is about a Pursuit this Agent **asked of someone else**. One Pursuit never fires both at the same Agent.
- `BY` takes the forms of `FROM`: `BY waiter`, `BY ?who`, `BY waiter ?who`, and the Quota forms `BY ALL waiter`, `BY 2 OF waiter`, `BY 50% OF waiter` (chapter 18). There is no `BY DIRECTOR`: a Director pursues nothing. In a Playbook the Role is the Playbook's, bound by any Giving the Agent holds (chapter 15).
- **Only Pursuits this Agent's own `ASK` started** are reported. A Goal the other Agent gave itself, or that someone else asked of it, is not, even under the same name.
- **One report per Pursuit.** A Goal asked twice is reported twice. A recipe that repeats (chapter 08) is reported for its first round only: later rounds are the Agent's own.
- The specific Trigger fires first, then `ENDED`, as at the Agent who pursued. That Agent's own ending Plans and the asker's are independent; neither waits for the other.
- **An ending with no Plan is silent.** Most asked Goals are not listened to.
- **Nothing waits.** `ASK` still carries on at once (ADR 0005); the report arrives later, as a Trigger.
- If the asker has left the Program, or no longer holds the Playbook with the `BY` Plan, the report reaches nobody.
- **An Agent that leaves the Program reports nothing** for the Pursuits it had: nothing was reached, dropped or failed. A Quota is checked again against the smaller Role (chapter 19).
- In a Plot, `BY` is how a Director hears of the Goals it asked, with the same rules (chapter 20).
- `BY` is an error on any Trigger that isn't a Goal's ending (except `WHEN EXITED, BY PARENT:`), together with `FROM`, and in a Playbook that never asks the Goal.
- **`BY` always names who did it**: here, whose Pursuit ended; on a Director's `EXITED`, the parent that ended the Staging (`WHEN EXITED, BY PARENT:`, chapter 20). The amount in `SHIFT m BY n` is the one closed exception (chapter 01).

## The shape of a Trigger

A Trigger has a core and clauses (chapter 01, *Clauses and the comma*). The **core** is, left to right:

1. `WHEN` (or `TO`);
2. the Vocabulary item, with its slots;
3. the kind word, if any;
4. `WITH <reason>`, after `FAILED` only (chapter 11).

The **clauses** follow, each after a `,`, in any order: `FROM …` (with its `OR` alternatives) or `BY …`, and the Labels (chapter 14, `14-labels.md`). Tools write `FROM` or `BY` first, then the Labels.

```regia
WHEN hates(?h) LEARNED, FROM ?teller, SUITS sympathy AT -0.5:
WHEN bring(?dish) FAILED WITH sold_out(?dish), BY waiter ?s:
```

The kind words, `WITH`, `FROM` and `BY` are reserved, so the parser always knows where the item ends. `DIRECTOR`, `GAME` and `ME` are reserved too. `FROM` or `BY` written without its `,` (`WHEN e FROM DIRECTOR:`) is `R0111` (chapter 01).

A Trigger has no Context clause: the Context is a `GIVEN` Block under the Trigger (chapter 06), and `WHEN e, GIVEN c:` is a parse error.


## Transpiler checks

**Errors**

- `R0501` One name declared as two kinds (`FACT fed` and `GOAL fed`).
- `R0502` A Cue tested in a Context or an `IF` (`IF food_served`).
- `R0503` A Fact Trigger without a kind word (`WHEN hates(?h):`, hint: `LEARNED` or `FORGOTTEN`).
- `R0504` A kind word that doesn't suit the item (`WHEN food_served LEARNED`, `WHEN find_food LEARNED`).
- `R0505` `FROM` on a `FORGOTTEN` Trigger.
- `R0506` `BY` on a Trigger that isn't a Goal's ending (a Cue, a Fact, a `TO` recipe, a Subplot's `ENDED`), except `, BY PARENT` on `EXITED` (chapter 20). `BY PARENT` on any other Trigger, and `BY` with anything but `PARENT` on `EXITED`, are this error too.
- `R0507` `FROM` and `BY` on the same Trigger.
- `R0508` `WHEN g … BY` in a Playbook that never asks `g`: no `ASK … TO g`. In a Plot it is `R2012` (chapter 20). Absence check (chapter 23).
- `R0509` `FROM GAME` on a `TO` recipe or a Goal's ending (no Goal comes from the game).
- `R0510` `FROM ME` on a Cue Trigger (an Agent never sends to itself).
- `R0511` A Placeholder or a quantity after `GAME` or `ME`, or anywhere in a `FROM … OR …` list.
- `R0512` `GAME`, `ME` or `OR` after `BY`.
- `R0513` The retired keyword `EVENT` (hint: renamed `CUE`).

`ME` in a Plot, `FROM ME` included, is `R0309` (chapter 03). A `PURSUE` or an `ASK` that no recipe's `FROM` admits is `R3805` or `R3806` (chapter 38).

## Regia 1.5

In 1.5 (ADR 0025): Goals, Cues and Events, every Trigger kind but `JOINED` (chapter 19), how a Pursuit ends with `REACHED`, `DROPPED`, `FAILED` and `ENDED` for the Agent's **own** Pursuits, and `FROM` with a Role, `?who`, `Role ?who` and `DIRECTOR`. A Trigger with no `FROM` still matches anything, and an Agent's own `PURSUE` still has no Sender.

Later, each `R0109` in a 1.5 build (chapter 01):

- `FROM GAME`, `FROM ME`, and `FROM` with `OR` alternatives.
- All of *Who pursued it: `BY`*: nobody hears how a Goal it asked ended. A recipe whose asker must know writes a `TELL` or a `SIGNAL` back.
- A quantity after `FROM` or `BY` (chapter 18).

`R0507`, `R0508`, `R0509`, `R0510`, `R0511` and `R0512` are about those words, and a 1.5 build never reports them. `R0506` stays: `BY` on a Trigger that isn't a Goal's ending is wrong in 2.0 too. `R3805` and `R3806` are later (chapter 38).

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- How a Body gives a Goal and drops one is decided in chapter 08 (`08-basic-actions.md`).
- The Director gives Goals with `ASK`; Phase entry and exit are `WHEN ENTERED:` / `WHEN EXITED:` (chapter 20).
- Goals that are kept or reached when a Fact holds: not yet specified.
- `FROM` on `FORGOTTEN` (a Fact the game took away, against the Agent's own `FORGET`), and a Director's own `LEARN` told from the game's: not in 2.0.
