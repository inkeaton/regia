# Messaging

How Agents send Facts, Cues and Goals to one another, how they Signal their Directors, and what the receiver sees. Decided in the ticket *Messaging between Agents* (`.scratch/regia-2/issues/08-messaging.md`). It builds on chapters 03, 05 and 06, and replaces the `TELL`, `BROADCAST` and `SIGNAL` parts of primer ch.4. Their names are confirmed in chapter 08 (`08-basic-actions.md`). That an asking Agent hears how its `ASK` ended was decided in the ticket *Failure a Plan can read, and answers to an `ASK`* (`.scratch/regia-revision/issues/03-failure-and-replies.md`), with ADR 0019. That a told Fact is taken back by the receiver's own Plans, that its first teller is the only one heard, and that `TELL` doesn't show the kind (ADR 0003 confirmed) were decided in the ticket *Facts that are told, and news in general* (`.scratch/regia-revision/issues/11-told-facts.md`).

## Three ways to send

| Statement | Sends | To |
|---|---|---|
| `TELL <recipient> <fact or event>.` | a Fact or a Cue | an Agent, a Role, or `EVERYONE` |
| `ASK <recipient> TO <goal>.` | a request to pursue a Goal | an Agent, a Role, or `EVERYONE` |
| `SIGNAL <event>.` | a Cue | the Directors giving this Playbook |

```regia
WHEN insult_heard(?s), FROM Guest ?who:
    GIVEN hates(?s):
        TELL ?who hates(?s)                # share a Fact
        TELL EVERYONE scandal(?s)          # share a Cue with everyone
        ASK ?who TO avenge(?s)             # request a Goal
        SIGNAL insult_thrown(?s)           # tell the Directors
```

- Every name has exactly one kind (chapter 05), so the Transpiler knows what is being sent. `TELL` with a Goal is an error that suggests `ASK … TO`; `ASK … TO` with a Fact or Cue is an error that suggests `TELL`.
- `TELL` *informs*; `ASK` *requests*. `ASK … TO` reads like the `TO` Trigger the request starts on the other side.
- Arguments follow chapter 03: Values, or Placeholders that are certainly filled. Expressions are allowed (chapter 04).
- Messages only **add** things. There is no way to make another Agent forget a Fact or drop a Goal; the receiver's own Plans decide that (*Taking a told Fact back*, below).
- `TELL` doesn't say whether it sends a Fact or a Cue. The name's one kind says it (ADR 0003), so the Vocabulary, and the editor, show which. The difference is in the receiver: a Fact lasts there and a Cue doesn't.
- There is no `BROADCAST`: it became the recipient `EVERYONE`.

## Recipients

A recipient is one of:

| Written | Reaches |
|---|---|
| `?who` | the Agent held by a certainly-filled Placeholder |
| a Role, e.g. `Guest` | every Agent playing that Role, except the sender |
| `<n> OF <Role>`, `<n>% OF <Role>` | that many of them, or that share, picked at random each time the Statement runs (chapter 15) |
| `EVERYONE` | every Agent in the game, except the sender |

A Director has two more: `CAST`, every Agent of its Staging reached once, and a Role with `EXCEPT` (chapters 15, 20).

- **Regia never names an Agent.** Agent names belong to instancing, not to the language. An Agent is reached only through a Placeholder filled at runtime, from `FROM ?who`, or from a Fact whose slot holds an Agent (`hates(?h)`). A Value in the recipient position is an error.
- One recipient per Statement. To reach two, write two Statements.
- A Playbook names Roles it declares itself (`ROLE host`), filled by the Plot that gives it. A Role there reaches the Agents bound to it by every giving the Agent holds, across Plots and Stagings (chapter 15, `15-roles-and-mappings.md`).
- `EVERYONE` is the only audience that doesn't depend on a Plot, which is why it is the whole game. Narrower audiences are Roles.
- If the recipient Placeholder holds something that is not an Agent at runtime (`?h` filled with `sword`), the **Plan fails**, like arithmetic on a non-Number (chapter 04). What failing does is in chapter 11 (`11-failure.md`).
- An empty Role, or `EVERYONE` when nobody else exists, sends nothing. That is not an error. A counted recipient that finds nobody sends nothing either, with a Trace warning (`T1502`, chapter 15): an `ASK` sent to nobody has no ending to hear.
- An Agent that plays two Roles hears a `TELL` to each of them twice. A Director that means everybody once writes `TELL CAST …`.

## Signals

`SIGNAL e` sends the Cue `e` to the Director of **every Plot that currently gives the Playbook containing the `SIGNAL` Statement**. If two Plots give it, both Directors receive the Signal. This is the same set of Directors that `FROM DIRECTOR` matches (chapter 05), so a Playbook stays Plot-independent.

- A Signal carries a Cue only, and never a local Cue (chapter 10).
- A Signal the giving Plot has no Plan for in any Phase is a warning at build; one that finds no Plan in the current Phase is a Trace entry, and nothing else happens (chapter 38).
- It has no recipient.
- `SIGNAL` is an Agent's **only** way to reach a Director. A Director is not an Agent, isn't held by a Placeholder and doesn't play a Role, so it can never be a `TELL` or `ASK` recipient.

## Delivery

- **Sending never waits**, whatever is sent. A Goal given to another Agent never makes the giver wait (chapter 05, ADR 0005). How the Goal ended comes back later, as a Trigger (*An asked Goal*, below).
- Messages from one sender to one receiver arrive **in the order they were sent**. Nothing is promised about the order across different senders.
- A message is never lost while its receiver is in the Program. When it arrives is up to the Target. A Message to an Agent that has left the Program is dropped, with a trace entry, and doesn't fail the sender (chapter 19).

## What the receiver sees

### A told Fact

A told Fact becomes the receiver's **own Fact**. Nothing remembers who told it.

- `WHEN f LEARNED, FROM ?who` fires only if the Agent **didn't already know** `f`; `?who` is the teller. Being told a Fact you already know does nothing.
- A Fact learned from the game, or from the Agent's own `LEARN`, has no Sender, so no Sender form matches it. `LEARNED, FROM GAME` and `LEARNED, FROM ME` do (chapter 05). Without `FROM`, `LEARNED` matches it as usual.
- `FORGET f` removes the Fact completely, however many Agents told it.
- `FORGOTTEN` never has a Sender; `FROM` on it is an error.

```regia
WHEN hates(?h) LEARNED, FROM ?teller:
    DO glance_at(?teller)
```

**Scenario.** Bob tells Alice `hates(host)`; `LEARNED, FROM ?who` fires with `?who` = bob. Carl tells her the same; nothing fires, she already knows it. Alice runs `FORGET hates(host)`; she no longer knows it.

A designer who needs to know *who* said what, for trust or gossip ("believe it once three people say it"), models it in the open: tell a Cue and record the teller in a Fact. Counting tellers is a Quota Trigger, `WHEN rumor(?about), FROM 3 OF neighbour:` (chapter 18).

```regia
WHEN rumor(?about), FROM ?who:
    LEARN heard_from(?who, ?about)
```

The reserved Trigger kind `TOLD` (below) is where built-in provenance may go later.

#### A Fact or a Cue

Which one to tell is chosen by what the receiver should do with it. A **Fact** is for what lasts: the receiver can test it, and telling it again changes nothing, so only its first teller is heard. A **Cue** is for each telling: every one fires, with its own Sender, and leaves nothing to test. A happening that must both be counted and remembered is told as a Cue, and the receiver records the Fact it needs (`rumor` and `heard_from`, above).

#### Taking a told Fact back

No Message takes a Fact back. The receiver forgets it in its own Plans, and the usual place is the Playbook the Fact belongs with. A Fact that goes with a duty is forgotten when the duty is taken away:

```regia
PLAYBOOK Keeping_watch:
    WHEN REMOVED:
        FORGET on_duty
```

`REMOVED` fires when the Agent's last giving of `Keeping_watch` goes (chapter 15), so a Guard who also won a duel stays `on_duty` while it still holds the Playbook as a Guard. A Fact the Director wants gone at a moment of its own choosing is a Goal it asks for, such as `ASK ?winner TO stand_down`, whose recipe forgets it.

### A told Cue

A Cue told by another Agent is **the same Cue** as one coming from the game, which only a `GAME CUE` can (chapter 10). `WHEN insult_heard(?s):` matches both; `FROM` tells them apart: a game Cue has no Sender, and `FROM GAME` matches only it (chapter 05). A Plan that acts on what the Agent saw, and must not be set off by another Agent's `TELL`, is written `FROM GAME`. If no Plan handles a told Cue, it is dropped, exactly like a game Cue.

### An asked Goal

A Goal given with `ASK` becomes the receiver's Goal, exactly like one it gave itself. In 2.0 there is no Statement for refusing it; its `TO` Plans and their Contexts decide what happens, and a recipe that won't do it fails with a Reason (below). A `TO … FROM` Plan can treat requests differently from the Agent's own pursuit:

```regia
TO avenge(?s), FROM Guest ?who:
    GIVEN friend_of(?who):
        DO challenge(?s)
    ELSE:
        DO shrug
```

- Every `ASK` starts a Pursuit of its own at the receiver, also for a Goal the receiver already pursues with the same arguments (chapter 05).
- If no `TO` Plan applies, the asked Goal fails at the receiver and fires its `WHEN … FAILED` there (chapter 11).

### Hearing how an asked Goal ended

**Whoever asked hears how the Goal ended**: an Agent as below, a Director in the same way (chapter 20). The receiver's Playbook sends nothing for it: no "done" Cue and no hand-written answer.

```regia
# The Servant's Playbook
TO bring(?dish), FROM patron ?g:              # FROM: who asked me
    GIVEN in_kitchen(?dish):
        DO carry(?dish, ?g)
    ELSE:
        FAIL WITH sold_out(?dish)            # a refusal, with its Reason

# The Guest's Playbook
WHEN hungry(?dish):
    ASK waiter TO bring(?dish)

WHEN bring(?dish) REACHED, BY waiter ?s:      # BY: who pursued what I asked
    DO thank(?s)

WHEN bring(?dish) FAILED WITH sold_out(?dish), BY waiter:
    LEARN off_the_menu(?dish)

WHEN bring(?dish) FAILED, BY waiter:          # any other Failure
    DO sulk
```

- The four endings of chapter 05 (`REACHED`, `DROPPED`, `FAILED`, `ENDED`) are heard with a `BY` clause, which names the Agent who pursued the Goal. The rules are in chapter 05, *Who pursued it: `BY`*.
- A Failure's **Reason** reaches the asker, also when it was given further down, in a Goal the asked one was waiting on (chapter 11).
- **A Body can't wait for it.** There is no `, AND WAIT` in 2.0. A Plan that must go on only when the Goal is over is split in two: the `ASK`, and a `WHEN g ENDED, BY …` Plan.
- A Role recipient starts one Pursuit per Agent reached, and each is reported. "When all of them are done" is a Quota: `WHEN bring(?dish) ENDED, BY ALL waiter:` (chapter 18).

### Sender forms

Messages between Agents use the `FROM` forms of chapter 05 and add none: `FROM Role`, `FROM ?who`, `FROM Role ?who`. `FROM DIRECTOR` matches only what a Director sent. No Message is ever `FROM GAME` or `FROM ME`: those are for what nobody sent. A recipe that takes both a request and the Agent's own `PURSUE` is `TO g, FROM Role OR ME:`. Inside a Playbook, `FROM Role` matches a Sender bound to that Playbook Role by any giving the Agent holds (chapter 15).

## Room for cooperation

Agent cooperation (accepting and refusing requests, hearing back, negotiating) is not part of 2.0. These choices keep it an addition, not a redesign:

- **`ASK` is a request, not a command.** In 2.0 the receiver always takes the Goal on, but that is 2.0's behaviour, not the meaning of `ASK`. Declining is written `FAIL WITH <reason>.` in a `TO …, FROM ?who` Plan, and the asker hears `FAILED WITH <reason>`. A later version may add a `REFUSE` Statement that declines before the Goal is taken on, without changing any `ASK` already written.
- **Replies are Trigger kinds on the Goal, with `BY` for the replier.** The four endings are heard in 2.0 (above). `AGREED` and `REFUSED` would be two more, in the same shape: `WHEN find_sword REFUSED, BY ?who`. These two kind words are **reserved** now and do nothing in 2.0.
- **Message Statements may later take trailing clauses**, `,`-separated like Labels on a Trigger: `ASK ?g TO find_sword, AND WAIT`, `…, WITHIN 30 SECONDS` (timeouts are not in 2.0, chapter 12). 2.0 defines none, and any clause is an error. Waiting on an `ASK` is put off because it ties two Agents together: the asker would fail when the other fails, a drop would spread from one Agent to another, a Role recipient would mean waiting on many, and the asked Agent may leave.
- **No conversation ids.** A request is identified by its Goal *with its arguments* plus `FROM`, which tells `find_sword` asked of Bob from the same Goal asked of Carl. If cooperation later needs more ("this auction, not that one"), a Goal argument carries it.
- **`TOLD` is reserved** as a Trigger kind for Facts, for provenance: a later `WHEN f TOLD, FROM ?who` could fire on *every* tell, even of a known Fact, alongside a Context test of who told it. It would add meaning, never change `LEARNED`.

## Reserved words

`TELL`, `ASK`, `SIGNAL`, `EVERYONE`; the kind words `TOLD`, `AGREED`, `REFUSED`; `REFUSE`. `REACHED` and `FAILED` are Trigger kinds (chapters 05, 11), and `BY` is chapter 05's.


## Transpiler checks

**Errors**

- `R0701` `TELL` with a Goal (hint: `ASK … TO`).
- `R0702` `ASK … TO` with a Fact or a Cue (hint: `TELL`).
- `R0703` `SIGNAL` with something that isn't a Cue.
- `R0704` A Value in the recipient position, `ME` included (Regia never names an Agent).
- `R0705` A trailing clause on a message Statement (none exist in 2.0).
- `R0706` A reserved word used: the kind words `TOLD`, `AGREED`, `REFUSED`, or `REFUSE`.

## Trace entries

**Failures**

- `T0701` A recipient Placeholder that doesn't hold an Agent at runtime.

**Unheard** (`info`, chapter 34)

- `T0702` A Cue told to an Agent, for which no Plan of the Agent's given Playbooks runs: none names it, or every one that does has a Context that doesn't hold. The entry names the Cue and its Sender. A Fact told is a `fact` entry whether or not a Plan reacts to it.

## ASL mapping notes

The Jason forms are in chapter 39 (*Messages*) and, for a Director, chapter 30 (*Signals*). What any AgentSpeak Target must respect:

- **A told Fact is new only once.** Whether the receiver already knows it, from any source, is decided when the message arrives, not in a Plan's Context: two tellings can arrive before either Plan runs. A Target that keeps the sources underneath, as Jason does, leaves room for `TOLD`. `FORGET f` removes the Fact with every source, so `FORGOTTEN` fires once.
- **A told Cue leaves nothing behind** in the receiver, so that a repeated Cue fires again and Cues stay momentary (chapter 05). It reaches the same Plans as a game Cue.
- `T0702` and chapter 38's `T3801` need a catch-all that runs only when no Plan does, also when a Plan for the Cue exists and its Context doesn't hold.
- **Role recipients and `EVERYONE`** need the infrastructure to know which Agents play a Role (chapter 29's cast copy). `EVERYONE` is a wrapped `.broadcast` that Directors ignore, so nobody needs to know every Agent (chapter 30). The sender is excluded.
- **`SIGNAL`** keeps 1.0's shape: each Agent knows which Directors gave it which Playbook, and sends to each of them (`signal_directors` in the primer's ASL examples). The Signal reaches the Director with the Sender's Role available for `FROM Role`.
- **A non-Agent recipient** must fail the Plan, so the generated send checks that `?x` names a known Agent first.
- Jason's per-sender message order matches the ordering promise above.
- `FROM GAME` and `FROM ME` are Jason's `source(percept)` and `source(self)`. `ME` is the Agent's own name, which a Role file shared by many Agents can't know at build: in Jason it is `.my_name`, as a Value and in a Trigger's pattern (chapter 39).
- An Agent reports the ending of each Pursuit whose Sender is another Agent to that Agent, with the Reason of a Failure, as a message the designer never writes; the asker needs a catch-all that drops a report no Plan takes. This is the same report a Director gets (chapter 20). The Jason chapters don't describe it yet.

## Regia 1.5

In 1.5 (ADR 0025), except *Hearing how an asked Goal ended*: the asker hears no ending and no Reason. A Plot or an Agent that must know writes it in the recipe, with a `TELL` or a `SIGNAL` back. `LEARNED, FROM GAME` and `LEARNED, FROM ME` are later (`R0109`, chapter 01), and so is counting tellers with a Quota Trigger.

For the ASL mapping, an Agent sends no ending reports in 1.5, and the asker needs no catch-all for them.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- The names of `TELL`, `ASK` and `SIGNAL` were confirmed, and `PURSUE g, WITHOUT WAITING` uses the trailing-clause shape: chapter 08.
- How a Playbook names Roles, and which Staging a Role recipient or `FROM Role` means there: chapter 15 (`15-roles-and-mappings.md`).
- A Director uses `ASK`/`TELL` too, with Sender `DIRECTOR`; it can never use `SIGNAL` (chapter 20).
- Messages that undo (forget a Fact, drop a Goal, call off a Goal that was asked), waiting on an `ASK`, `REFUSE` and `AGREED`, and provenance (`TOLD`): after 2.0.
