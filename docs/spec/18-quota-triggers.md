# Quota Triggers

How a Plan reacts when enough of a Role's Agents have sent the same Event: "when all Guests are ready", "when 3 Guests complain", "when half the Guests vote for the duel". Decided in the ticket *Conditions over a whole Role* (`.scratch/regia-2/issues/19-role-wide-conditions.md`). It builds on chapters 03, 05, 07, 13 and 15, and answers the Role-wide conditions question (Q4d) of the charting session.

## The form

A **Quota Trigger** is an Event Trigger whose `FROM` names a Role with a quantity in front:

```regia
DURING reception:
    WHEN ready FROM ALL Guest:
        TRANSITION TO feast.

    WHEN complaint FROM 3 OF Guest:
        ASK Host TO apologise.

DURING feast:
    WHEN voted(?choice) FROM 50 PERCENT OF Guest:
        ...
```

| Written | Fires when |
|---|---|
| `FROM ALL Guest` | every Agent playing `Guest` has sent the Event |
| `FROM 3 OF Guest` | at least 3 different `Guest`s have sent it |
| `FROM 50 PERCENT OF Guest` | at least that share of the `Guest`s have sent it |

- The quantities reuse the count forms of Mappings (chapter 15): `n OF`, `n PERCENT OF`, plus `ALL`.
- There is no `ANY`. "Any Guest" is plain `FROM Guest` (chapter 05), which reacts to each Event as it arrives.
- The quantity is a **Number Value**, checked at compile time: a whole number of at least 1 for `n OF`, and more than 0 and at most 100 for `PERCENT`. No Expressions and no `RANDOM`: nothing is filled before the Trigger matches, so an Expression could only be built from Values anyway.
- **`?who` is an error** after a quantity (`FROM ALL Guest ?who`). No single Agent fired the Trigger.

## Where it can be used

A Quota Trigger is allowed on any **Event Trigger** (`WHEN e …`) whose `FROM` names a Role:

- **In a Director**, over Signals from a Plot Role, in this Staging (chapter 05).
- **In a Playbook**, over Events told by Agents bound to a Playbook Role by any Giving the Agent holds (chapter 15). This covers spec 07's gossip case, "believe it once three people say it":

```regia
PLAYBOOK Gossip:
    ROLE neighbour.
    WHEN rumor(?about) FROM 3 OF neighbour:
        LEARN believes(?about).
```

It is an **error** on every other Trigger kind: `LEARNED` (it fires only when the Fact is new, so later tellers would never count), `FORGOTTEN`, `TO`, `DROPPED`, `FAILED` and `ENDED`.

Only Events are counted. A Director never reads its Agents' Facts. Agents send a Signal to have something counted: "when every Guest has eaten" means each Guest's Playbook signals `ate` and the Director waits on `WHEN ate FROM ALL Guest`.

## Counting

### Who counts

- **Each Agent counts once**, however many times it sends the Event.
- Only Agents playing the Role count. A sender outside it is ignored for the quota, though it can still trigger other Plans.
- `ALL` and `PERCENT` are measured against the Agents playing the Role **at the time of the check**, live, like a Role recipient (chapter 07).
- `PERCENT` means **at least that share**, with no rounding: 50 PERCENT of 3 Guests needs 2. This deliberately differs from picks, which round down (chapter 15), because a threshold that rounds down can be met too easily.
- In a Playbook, the Agent itself never counts and is left out of `ALL` and `PERCENT`: it never receives its own Events (chapter 07).
- `n OF` with more than n Agents in the Role is fine. With fewer, it can't be met and never fires.
- `ALL` of an **empty Role never fires**.
- Only **current** players count. An Agent that leaves the Program stops counting, and the quota is checked again when someone leaves, so a non-sender leaving can complete an `ALL`. A joiner raises the denominator of `ALL` and `PERCENT` (chapter 19).

### Arguments

The count is kept **per argument value**. `WHEN voted(?choice) FROM ALL Guest:` fires when every Guest has voted for the *same* choice, and fills `?choice` with it.

- An Agent that sends `voted(a)` and then `voted(b)` counts toward both.
- Values in the Trigger narrow it as usual: `voted(duel) FROM ALL Guest` counts only votes for `duel`.
- Placeholders follow chapter 03: the one that fired fills them.

### When counting starts and stops

The count belongs to the **Trigger**, not to a single Trigger Block:

- It starts when a Block with that Trigger becomes active: a Phase entered for `DURING <phase>`, Staging start for `DURING PLOT`, or a Giving for a Playbook.
- It is kept while **at least one** Block with that Trigger is active, and discarded when none is. Leaving `feast` discards the counts of `feast`'s Quota Triggers, unless `DURING PLOT` has the same Trigger.
- Senders counted before the count started don't count. A Guest that signalled `ready` during `reception` must signal again in `feast`.

### Firing

- When the quota is reached, the Trigger fires **once**, and that argument value's count **starts again from zero**. Other values' partial counts stay. The Trigger can fire again when the quota is reached anew.
- Reaching the quota is **momentary**, like an Event (chapter 05). If no Trigger Block is a candidate (every `GIVEN` fails and there is no `ELSE`), nothing runs and the count still resets. Keeping it would make the next stray Signal fire the Plan.

## Selection

A Quota Trigger is **its own Trigger**, separate from the plain Event and from other quantities:

```regia
DURING reception:
    WHEN ready FROM Guest ?g:
        TELL ?g welcome.                 # runs for every ready Guest
    WHEN ready FROM ALL Guest:
        TRANSITION TO feast.             # also runs, once, after the last one
```

- The Signal that completes the quota is handled by the plain Trigger as usual, **and** fires the Quota Trigger. One does not shadow the other.
- `FROM ALL Guest` and `FROM 3 OF Guest` on the same Event are two Triggers with two counts.
- Blocks with the **same** Quota Trigger (same Event, quantity and Role) compete as in chapter 13. For example, a Phase's Block beats `DURING PLOT`'s.

## Transpiler checks

**Errors**

- `R1801` A quantity on a Trigger kind other than an Event.
- `R1802` A quantity in front of something that isn't a Role (`FROM ALL ?x`, `FROM ALL DIRECTOR`).
- `R1803` `?who` after a quantity.
- `R1804` A quantity that isn't a Number Value, isn't whole for `n OF`, is below 1 for `n OF`, or is outside (0, 100] for `PERCENT`.

## Reserved words

`ALL`. `OF` and `PERCENT` come from chapter 15.

## ASL mapping notes

For *The full ASL mapping* to pick up. For Jason, these are implemented in chapter 33 (`33-jason-cast-changes-and-quotas.md`), in ASL (ADR 0013):

- **In a Director**, the mapping between Roles and Agents is already stored in the Director, so it keeps each count as generated Facts, for example `quota_seen(TriggerId, Args, Agent)`. A Signal adds the sender if it plays the Role. The Director then checks the quota against its own Role records, posts an internal event for the Quota Trigger and removes that trigger's Facts for those arguments.
- **In an Agent**, the same works against the per-Giving record of Role bindings (chapter 15's note), which the Agent needs for `FROM Role` anyway.
- Counts are cleared when the last Block with the Trigger becomes inactive: on Phase exit in the Director, on taking a Playbook away in an Agent.
- The plain Trigger's handling and the quota check both happen for the same arriving Signal. The quota check must not depend on the plain Plan being chosen.

## Not decided here

- Quantities over Subplot endings ("when every HonorDuel has ended"): *Richer Subplots*. `ENDED` takes no quantity in 2.0 (chapter 17).
- Counting an Agent's or Director's own Facts: `COUNT(condition)`, a Number Expression (chapter 26). `n OF` stays a Quota form.
