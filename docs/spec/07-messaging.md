# Messaging

How Agents send Facts, Events and Goals to one another, how they Signal their Directors, and what the receiver sees. Decided in the ticket *Messaging between Agents* (`.scratch/regia-2/issues/08-messaging.md`). It builds on chapters 03, 05 and 06, and replaces the `TELL`, `BROADCAST` and `SIGNAL` parts of primer ch.4. Their names are confirmed in chapter 08 (`08-basic-actions.md`).

## Three ways to send

| Statement | Sends | To |
|---|---|---|
| `TELL <recipient> <fact or event>.` | a Fact or an Event | an Agent, a Role, or `EVERYONE` |
| `ASK <recipient> TO <goal>.` | a request to pursue a Goal | an Agent, a Role, or `EVERYONE` |
| `SIGNAL <event>.` | an Event | the Directors giving this Playbook |

```regia
WHEN insult_heard(?s) FROM Guest ?who:
    GIVEN hates(?s):
        TELL ?who hates(?s).               # share a Fact
        TELL EVERYONE scandal(?s).         # share an Event with everyone
        ASK ?who TO avenge(?s).            # request a Goal
        SIGNAL insult_thrown(?s).          # tell the Directors
```

- Every name has exactly one kind (chapter 05), so the Transpiler knows what is being sent. `TELL` with a Goal is an error that suggests `ASK … TO`; `ASK … TO` with a Fact or Event is an error that suggests `TELL`.
- `TELL` *informs*; `ASK` *requests*. `ASK … TO` reads like the `TO` Trigger the request starts on the other side.
- Arguments follow chapter 03: Values, or Placeholders that are certainly filled. Expressions are allowed (chapter 04).
- Messages only **add** things. There is no way to make another Agent forget a Fact or drop a Goal; the receiver's own Plans decide that.
- There is no `BROADCAST`: it became the recipient `EVERYONE`.

## Recipients

A recipient is one of:

| Written | Reaches |
|---|---|
| `?who` | the Agent held by a certainly-filled Placeholder |
| a Role, e.g. `Guest` | every Agent playing that Role, except the sender |
| `EVERYONE` | every Agent in the game, except the sender |

- **Regia never names an Agent.** Agent names belong to instancing, not to the language. An Agent is reached only through a Placeholder filled at runtime, from `FROM ?who`, or from a Fact whose slot holds an Agent (`hates(?h)`). A Value in the recipient position is an error.
- One recipient per Statement. To reach two, write two Statements.
- How a Playbook can name a Role at all, and which Staging's Agents a Role means there, is decided in *Roles inside Playbooks*.
- `EVERYONE` is the only audience that doesn't depend on a Plot, which is why it is the whole game. Narrower audiences are Roles.
- If the recipient Placeholder holds something that is not an Agent at runtime (`?h` filled with `sword`), the **Plan fails**, like arithmetic on a non-Number (chapter 04). What failing does is in chapter 11 (`11-failure.md`).
- An empty Role, or `EVERYONE` when nobody else exists, sends nothing. That is not an error.

## Signals

`SIGNAL e.` sends the Event `e` to the Director of **every Plot that currently gives the Playbook containing the `SIGNAL` Statement**. If two Plots give it, both Directors receive the Signal. This is the same set of Directors that `FROM DIRECTOR` matches (chapter 05), so a Playbook stays Plot-independent.

- A Signal carries an Event only.
- It has no recipient.
- `SIGNAL` is an Agent's **only** way to reach a Director. A Director is not an Agent, isn't held by a Placeholder and doesn't play a Role, so it can never be a `TELL` or `ASK` recipient.

## Delivery

- **Sending never waits**, whatever is sent. A Goal given to another Agent never makes the giver wait (chapter 05).
- Messages from one sender to one receiver arrive **in the order they were sent**. Nothing is promised about the order across different senders.
- A message is never lost. When it arrives is up to the Target.

## What the receiver sees

### A told Fact

A told Fact becomes the receiver's **own Fact**. Nothing remembers who told it.

- `WHEN f LEARNED FROM ?who` fires only if the Agent **didn't already know** `f`; `?who` is the teller. Being told a Fact you already know does nothing.
- A Fact learned from the game, or from the Agent's own `LEARN`, has no Sender, so no `FROM` clause matches it. Without `FROM`, `LEARNED` matches it as usual.
- `FORGET f` removes the Fact completely, however many Agents told it.
- `FORGOTTEN` never has a Sender; `FROM` on it is an error.

```regia
WHEN hates(?h) LEARNED FROM ?teller:
    DO glance_at(?teller).
```

**Scenario.** Bob tells Alice `hates(host)`; `LEARNED FROM ?who` fires with `?who` = bob. Carl tells her the same; nothing fires, she already knows it. Alice runs `FORGET hates(host)`; she no longer knows it.

A designer who needs to know *who* said what, for trust or gossip ("believe it once three people say it"), models it in the open: tell an Event and record the teller in a Fact.

```regia
WHEN rumor(?about) FROM ?who:
    LEARN heard_from(?who, ?about).
```

The reserved Trigger kind `TOLD` (below) is where built-in provenance may go later.

### A told Event

An Event told by another Agent is **the same Event** as one coming from the game. `WHEN insult_heard(?s):` matches both; `FROM` tells them apart, since game Events have no Sender. If no Plan handles a told Event, it is dropped, exactly like a game Event.

### An asked Goal

A Goal given with `ASK` becomes the receiver's Goal, exactly like one it gave itself. In 2.0 the receiver can't refuse it outright; its `TO` Plans and their Contexts decide what happens. A `TO … FROM` Plan can treat requests differently from the Agent's own pursuit:

```regia
TO avenge(?s) FROM Guest ?who:
    GIVEN friend_of(?who):
        DO challenge(?s).
    ELSE:
        DO shrug.
```

- Asking for a Goal the receiver already pursues, with the same arguments, is ignored (chapter 05).
- If no `TO` Plan applies, the asked Goal fails at the receiver and fires its `WHEN … FAILED` there (chapter 11). The asker hears nothing in 2.0.

### Sender forms

Messages between Agents use the `FROM` forms of chapter 05 and add none: `FROM Role`, `FROM ?who`, `FROM Role ?who`. `FROM DIRECTOR` matches only what a Director sent. Inside a Playbook, which Staging `FROM Role` refers to is decided in *Roles inside Playbooks*.

## Room for cooperation

Agent cooperation (accepting and refusing requests, hearing back, negotiating) is not part of 2.0. These choices keep it an addition, not a redesign:

- **`ASK` is a request, not a command.** In 2.0 the receiver always takes the Goal on, but that is 2.0's behaviour, not the meaning of `ASK`. A later version may let the receiver decline, for example with a `REFUSE` Statement in a `TO … FROM ?who` Plan, without changing any `ASK` already written.
- **Replies will be Trigger kinds on the Goal**, shaped like `DROPPED`: `WHEN find_sword AGREED FROM ?who`, `REFUSED`, `REACHED`, `FAILED`. These kind words are **reserved** now and do nothing in 2.0. (`FAILED` is now a real local Trigger kind, chapter 11, where `FROM` names the Goal's *Sender*. A reply `WHEN find_sword FAILED FROM ?who` would use `FROM` for the *replier*, which clashes, so the reply wording must be redesigned with cooperation. There is still no local "Goal reached" Trigger: chapter 05.)
- **Message Statements may later take trailing clauses**, `,`-separated like Labels on a Trigger: `ASK ?g TO find_sword, AND WAIT`, `…, WITHIN 30 SECONDS` (timeouts are not in 2.0, chapter 12). 2.0 defines none, and any clause is an error.
- **No conversation ids.** A request is identified by its Goal *with its arguments* plus `FROM`, which tells `find_sword` asked of Bob from the same Goal asked of Carl. If cooperation later needs more ("this auction, not that one"), a Goal argument carries it.
- **`TOLD` is reserved** as a Trigger kind for Facts, for provenance: a later `WHEN f TOLD FROM ?who` could fire on *every* tell, even of a known Fact, alongside a Context test of who told it. It would add meaning, never change `LEARNED`.

## Reserved words

`TELL`, `ASK`, `SIGNAL`, `EVERYONE`; the kind words `TOLD`, `AGREED`, `REFUSED`, `REACHED`, `FAILED`; `REFUSE`.

## ASL mapping notes

For *The full ASL mapping* to pick up:

- `TELL ?x f` (a Fact) maps to `.send(X, tell, f)`. `ASK ?x TO g` maps to `.send(X, achieve, g)`.
- **Told Facts keep their Jason sources underneath.** The language hides them: `LEARNED` must fire only when the belief is new, so the receiving side checks whether `f` was already believed from any source before running a `LEARNED` Plan. `FORGET f` removes every source (e.g. `.abolish` or one removal per source), and `FORGOTTEN` fires only when the last one goes. Keeping the sources leaves room for `TOLD`.
- **A told Event** isn't a belief. 1.0 sends `untell` then `tell` so that a repeated Event fires again; 2.0 should use a form that leaves nothing behind in the receiver's belief base (for example a generated achieve-goal per Event, or an immediate removal in the handling plan), so that Events stay momentary (chapter 05).
- **Role recipients and `EVERYONE`** need the infrastructure to know which Agents play a Role and which Agents exist; part of *The full ASL mapping*. The sender is excluded.
- **`SIGNAL`** keeps 1.0's shape: each Agent knows which Directors gave it which Playbook, and sends to each of them (`signal_directors` in the primer's ASL examples). The Signal reaches the Director with the Sender's Role available for `FROM Role`.
- **A non-Agent recipient** must fail the Plan, so the generated send checks that `?x` names a known Agent first.
- Jason's per-sender message order matches the ordering promise above.

## Not decided here

- The names of `TELL`, `ASK` and `SIGNAL` were confirmed, and `PURSUE g, WITHOUT WAITING` uses the trailing-clause shape: chapter 08.
- How a Playbook names Roles, and which Staging a Role recipient or `FROM Role` means there: *Roles inside Playbooks*.
- How a Director gives Goals, Facts and Events to Roles or Agents: *Director capabilities*.
- Messages that undo (forget a Fact, drop a Goal), agent cooperation, and provenance (`TOLD`): not yet specified.
