# Goals and Triggers

What Goals are, how they are declared, and every kind of Trigger a Plan can start from. Decided in the ticket *Goals and Trigger kinds* (`.scratch/regia-2/issues/05-goals-and-trigger-kinds.md`). It builds on *Parameters and Placeholders* (`03-parameters-and-placeholders.md`) and replaces the Goal and trigger-type parts of primer ch.2–4. The choice to treat Fact changes and Goals as Trigger kinds, with Events kept momentary, is recorded in `docs/adr/0003-events-are-momentary-fact-changes-are-trigger-kinds.md`.

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

Another Agent writes `ASK ?who TO g.` (chapter 07). The Agent itself writes `PURSUE g.` (chapter 08); the Director writes `ASK ?who TO g.` or `ASK Role TO g.` (chapter 20).

### Reaching a Goal

A Goal is **reached when a Plan for it finishes its Body**. Nothing checks the world. There is no "Goal reached" Trigger: if the Director or another Agent needs to know, the Plan tells them (a Signal, a message).

If no Plan for the Goal applies, or its Plan fails, the Goal **fails** and `WHEN g FAILED` fires (chapter 11, `11-failure.md`).

### Pursuing a Goal twice

If an Agent is told to pursue a Goal it is already pursuing, with the same arguments, the second request is **ignored**. Different arguments are different Goals: `avenge(bob)` and `avenge(carl)` are pursued side by side.

### Waiting for a Goal

A Body that pursues a Goal can either **wait** until it is reached and then continue, or **start it and carry on**. Both exist. `PURSUE g.` waits and `PURSUE g, WITHOUT WAITING.` carries on (chapter 08). A Goal given to another Agent never makes the giver wait.

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

## Events are momentary

An **Event** (`EVENT food_served`) is something that happens and is over once noticed. It triggers Plans and leaves nothing behind:

- it can't be tested in a Context: `IF food_served` is an error;
- it can't be added with `LEARN` or removed with `FORGET`;
- a Plan that needs to remember it records a Fact.

A Fact lasts until it is forgotten, and a Context can test it at any time. Both can trigger Plans: an Event when it happens, a Fact when it is learned or forgotten.

A Signal is an Event that an Agent sends to a Director. The Director reacts to it like any other Event.

## Trigger kinds

Everything a Plan can start from is a **Trigger kind**. Each is written after `WHEN`, except a Goal recipe, written after `TO`.

| Trigger kind | Written |
|---|---|
| An Event happens (including a Signal, at a Director) | `WHEN insult_heard(?s):` |
| A Fact is learned | `WHEN hates(?h) LEARNED:` |
| A Fact is forgotten | `WHEN hates(?h) FORGOTTEN:` |
| A Goal is pursued (a recipe) | `TO find_food:` |
| A Goal is dropped | `WHEN find_food DROPPED:` |
| A Goal fails | `WHEN find_food FAILED:` (chapter 11) |
| A Phase is entered or left (Director Plans) | `WHEN ENTERED:`, `WHEN EXITED:` (chapter 20) |
| An Agent joins or leaves a Role, or a Role empties (Director Plans) | `WHEN Guest ?g JOINED:`, `WHEN Guest LEFT:`, `WHEN Guest EMPTIED:` (chapter 19) |

```regia
WHEN hates(?h) LEARNED:
    DO glare_at(?h).

TO avenge(?who):
    IF is_armed:
        DO challenge(?who).

WHEN avenge(?who) DROPPED:
    PRINT("Let it go.").
```

- **Fact Triggers always have a kind word.** `WHEN hates(?h):` is an error; the Transpiler knows `hates` is a Fact and suggests `LEARNED` or `FORGOTTEN`. So a reader never has to look up whether a bare name is a Fact or an Event.
- **The kind word follows the item**, using a participle: `LEARNED`, `FORGOTTEN`, `DROPPED`, `FAILED`.
- **`LEARNED` and `FORGOTTEN` fire whatever caused the change**: the game, a message, or the Agent's own `LEARN` and `FORGET`.
- **A kind word must suit the item.** `WHEN food_served LEARNED` (an Event) or `WHEN find_food LEARNED` (a Goal) is an error.
- **A `TO` Plan is an ordinary Plan**: Placeholders in its Trigger, a Context, Labels and a Body follow the same rules as in a `WHEN` Plan.
- **`WHEN` is the only reaction keyword.** Plot Phases no longer use `ON ENTER` / `ON EXIT`; Phase entry and exit are `WHEN` Triggers, `WHEN ENTERED:` and `WHEN EXITED:` (chapter 20).

## Who sent it: `FROM`

A Trigger for something that was **sent** (a Signal at a Director, a Goal given by the Director or by another Agent, a Fact or Event told by another Agent) can say who sent it with `FROM`:

| Written | Matches |
|---|---|
| no `FROM` | any sender, or none |
| `FROM Guest` | a sender playing the Role `Guest`: in a Plot, in this Staging; in a Playbook, bound to the Playbook's Role `Guest` by any giving (chapter 15) |
| `FROM ?who` | any sender, and fills `?who` with the sending Agent |
| `FROM Guest ?who` | a sender playing `Guest`, and fills `?who` with it |
| `FROM DIRECTOR` | the Director of any Plot that currently gives this Playbook to the Agent |

```regia
# In a Plot
WHEN insult_thrown(?target) FROM Guest ?who:
    ...

# In a Playbook
TO find_sword FROM DIRECTOR:
    DO search_armory.
```

- `?who` follows the Placeholder rules of chapter 03: filled once, by matching. A Director can send it Messages, `ASSIGN … TO ?who` and map it onto a Role (chapter 20).
- `FROM DIRECTOR` is worked out at runtime, so a Playbook never names a Plot and stays Plot-independent. A Goal from a Director whose Plot doesn't give this Playbook doesn't match.
- `FROM` is an error on `FORGOTTEN`, which never has a Sender. On `LEARNED` it matches only a Fact told by another Agent, and only when the Fact was new (chapter 07); a Fact learned from the game or from the Agent's own `LEARN` has no Sender, so no `FROM` clause matches it. Likewise an Event from the game has no Sender.
- On `DROPPED` and `FAILED`, `FROM` means **the Goal's Sender**, as on `TO g FROM …`: `WHEN find_sword FAILED FROM DIRECTOR:` (chapter 11).
- A Goal the Agent gave itself has **no sender**, so no `FROM` clause matches it. Without `FROM`, it matches as usual.
- Messages between Agents use these same forms (chapter 07, `07-messaging.md`).
- On an Event Trigger, a quantity before the Role (`FROM ALL Guest`, `FROM 3 OF Guest`, `FROM 50 PERCENT OF Guest`) makes a Quota Trigger, which waits until enough different Agents of the Role have sent the Event (chapter 18, `18-quota-triggers.md`).

## Order of a Trigger

A Trigger reads, left to right:

1. `WHEN` (or `TO`);
2. the Vocabulary item, with its slots;
3. the kind word, if any;
4. `FROM …`, if any;
5. the Labels, if any (chapter 14, `14-labels.md`).

```regia
WHEN hates(?h) LEARNED FROM ?teller, SUITS sympathy AT -0.5:
```

The kind words and `FROM` are reserved, so the parser always knows where the item ends.


## Transpiler checks

**Errors**

- `R0501` One name declared as two kinds (`FACT fed` and `GOAL fed`).
- `R0502` An Event tested in a Context or an `IF` (`IF food_served`).
- `R0503` A Fact Trigger without a kind word (`WHEN hates(?h):`, hint: `LEARNED` or `FORGOTTEN`).
- `R0504` A kind word that doesn't suit the item (`WHEN food_served LEARNED`, `WHEN find_food LEARNED`).
- `R0505` `FROM` on a `FORGOTTEN` Trigger.

## Not decided here

- How a Body gives a Goal and drops one is decided in chapter 08 (`08-basic-actions.md`).
- The Director gives Goals with `ASK`; Phase entry and exit are `WHEN ENTERED:` / `WHEN EXITED:` (chapter 20).
- Renaming `EVENT` to `CUE`, Goals that are kept or reached when a Fact holds, and `FROM SELF`: not yet specified.
