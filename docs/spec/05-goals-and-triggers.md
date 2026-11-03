# Goals and Triggers

What Goals are, how they are declared, and every kind of Trigger a Plan can start from. Decided in the ticket *Goals and Trigger kinds* (`.scratch/regia-2/issues/05-goals-and-trigger-kinds.md`). It builds on *Parameters and Placeholders* (`03-parameters-and-placeholders.md`) and replaces the Goal and trigger-type parts of primer ch.2–4. The choice to treat Fact changes and Goals as Trigger kinds, with Events kept momentary, is recorded in `docs/adr/0003-events-are-momentary-fact-changes-are-trigger-kinds.md`.

In the examples, the Context is written as the `IF` directly under the Trigger, as in chapter 03. How a Context is written is decided in *Context vs control flow*. Labels are written `, PRIORITY 5` as a placeholder until *Label syntax* decides.

## Goals

A **Goal** is an objective an Agent pursues. Regia 2.0 has only one kind: a Goal the Agent tries to *reach*, and then stops pursuing (an *achievement* goal in BDI terms). There are no test goals; matching in a Context already does that job. Goals that must be *kept* true, or that are reached when a Fact holds, are not part of 2.0.

### Declaring Goals

Goals are declared like every other Vocabulary item, with untyped parameter names (chapter 03), multi-definition and Groups:

```regia
GOAL find_food
GOAL avenge(person)
GOAL get_fed, find_shelter
```

### One name, one kind

A Vocabulary name belongs to exactly one kind. Declaring `FACT fed` and `GOAL fed` is an error. A Goal and the Fact that tells it is done get two names: `GOAL get_fed`, `FACT fed`.

### Who gives a Goal

An Agent can be given a Goal by:

- **itself**, with a Basic Action in a Body;
- **the Director** of a Plot, with a Director Statement;
- **another Agent**, with a message.

How each is written is decided in *Basic action set*, *Director capabilities* and *Messaging*.

### Reaching a Goal

A Goal is **reached when a Plan for it finishes its Body**. Nothing checks the world. There is no "Goal reached" Trigger: if the Director or another Agent needs to know, the Plan tells them (a Signal, a message).

What happens when no Plan for the Goal applies, or the Plan fails, is decided in *Plan failure and fallback*.

### Pursuing a Goal twice

If an Agent is told to pursue a Goal it is already pursuing, with the same arguments, the second request is **ignored**. Different arguments are different Goals: `avenge(bob)` and `avenge(carl)` are pursued side by side.

### Waiting for a Goal

A Body that pursues a Goal can either **wait** until it is reached and then continue, or **start it and carry on**. Both exist. Their syntax, and which is the default, are decided in *Basic action set*. A Goal given to another Agent never makes the giver wait.

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
- it can't be `BELIEVE`d or `FORGET`ed;
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
| A Goal fails | reserved: *Plan failure and fallback* |
| A Phase is entered or left (Director Plans) | a `WHEN` Trigger: *Director capabilities* |

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
- **The kind word follows the item**, using a participle: `LEARNED`, `FORGOTTEN`, `DROPPED`.
- **`LEARNED` and `FORGOTTEN` fire whatever caused the change**: the game, a message, or the Agent's own `BELIEVE` and `FORGET`.
- **A kind word must suit the item.** `WHEN food_served LEARNED` (an Event) or `WHEN find_food LEARNED` (a Goal) is an error.
- **A `TO` Plan is an ordinary Plan**: Placeholders in its Trigger, a Context, Labels and a Body follow the same rules as in a `WHEN` Plan.
- **`WHEN` is the only reaction keyword.** Plot Phases no longer use `ON ENTER` / `ON EXIT`; Phase entry and exit are `WHEN` Triggers, worded by *Director capabilities*.

## Who sent it: `FROM`

A Trigger for something that was **sent** (a Signal at a Director, a Goal given by the Director or by another Agent, a message) can say who sent it with `FROM`:

| Written | Matches |
|---|---|
| no `FROM` | any sender, or none |
| `FROM Guest` | a sender playing the Role `Guest` in this Staging |
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

- `?who` follows the Placeholder rules of chapter 03: filled once, by matching. What a Director can do with it (`ASSIGN … TO ?who`) is decided in *Director capabilities* and *Role setup*.
- `FROM DIRECTOR` is worked out at runtime, so a Playbook never names a Plot and stays Plot-independent. A Goal from a Director whose Plot doesn't give this Playbook doesn't match.
- `FROM` is an error on Triggers that have no sender: Facts learned or forgotten, and Events from the game.
- A Goal the Agent gave itself has **no sender**, so no `FROM` clause matches it. Without `FROM`, it matches as usual.
- The sender forms for messages between Agents are decided in *Messaging*.

## Order of a Trigger

A Trigger reads, left to right:

1. `WHEN` (or `TO`);
2. the Vocabulary item, with its slots;
3. the kind word, if any;
4. `FROM …`, if any;
5. the Labels, if any (*Label syntax*).

```regia
WHEN hates(?h) LEARNED FROM ?teller, PRIORITY 5:
```

The kind words and `FROM` are reserved, so the parser always knows where the item ends.

## Not decided here

- How a Body gives a Goal (to itself, waiting or not) and drops one, and their names: *Basic action set*.
- How the Director gives Goals, and how Phase entry and exit Triggers are worded: *Director capabilities*.
- Message contents, and the sender forms for messages between Agents: *Messaging*.
- The "Goal fails" Trigger and what happens when no `TO` Plan applies: *Plan failure and fallback*.
- Renaming `EVENT` to `CUE`, Goals that are kept or reached when a Fact holds, and `FROM SELF`: not yet specified.
