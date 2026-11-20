# Quota Triggers

How a Plan reacts when enough of a Role's Agents have sent the same Cue: "when all Guests are ready", "when 3 Guests complain", "when half the Guests vote for the duel". Decided in the ticket *Conditions over a whole Role* (`.scratch/regia-2/issues/19-role-wide-conditions.md`). It builds on chapters 03, 05, 07, 13 and 15, and answers the Role-wide conditions question (Q4d) of the charting session.

## The form

A **Quota Trigger** is a Cue Trigger whose `FROM` names a Role with a quantity in front:

```regia
DURING reception:
    WHEN ready, FROM ALL Guest:
        ENTER feast

    WHEN complaint, FROM 3 OF Guest:
        ASK Host TO apologise

DURING feast:
    WHEN voted(?choice), FROM 50% OF Guest:
        ...
```

| Written | Fires when |
|---|---|
| `FROM ALL Guest` | every Agent playing `Guest` has sent the Cue |
| `FROM 3 OF Guest` | at least 3 different `Guest`s have sent it |
| `FROM 50% OF Guest` | at least that share of the `Guest`s have sent it |

- The quantities reuse the count forms of Mappings (chapter 15): `n OF`, `n% OF`, plus `ALL`.
- There is no `ANY`. "Any Guest" is plain `FROM Guest` (chapter 05), which reacts to each Cue as it arrives.
- The quantity is a **Number Expression** (chapter 04) over Values and the Placeholders filled in every Block: a Plot's parameters (chapter 17). `WHEN cheered, FROM ?needed OF Spectator:` in `PLOT HonorDuel(quarrel, needed)`. `RANDOM` is an error: the quantity is worked out again at every check, and a draw per check means nothing. A quantity made of Values only is checked at compile time: more than 0 for `n OF`, and more than 0 and at most 100 for `n% OF`.
- A quantity that isn't whole **rounds up**, as everywhere a count is taken (chapter 15): `2.5 OF Guest` needs 3.
- A quantity worked out at runtime to 0 or less, a share above 100%, or something that isn't a Number is a runtime warning in the Trace (`T1801`), and the Quota doesn't fire at that check.
- **`?who` is an error** after a quantity (`FROM ALL Guest ?who`). No single Agent fired the Trigger. Which Agents were counted is read with `SENT` (*What the Plan knows*, below).

## Where it can be used

A Quota Trigger is allowed on any **Cue Trigger** (`WHEN e …`) whose `FROM` names a Role:

- **In a Director**, over Signals from a Plot Role, in this Staging (chapter 05).
- **In a Playbook**, over Cues told by Agents bound to a Playbook Role by any Giving the Agent holds (chapter 15). This covers spec 07's gossip case, "believe it once three people say it":

```regia
PLAYBOOK Gossip:
    ROLE neighbour
    WHEN rumor(?about), FROM 3 OF neighbour:
        LEARN believes(?about)
```

- **Over the endings of a Goal that was asked**, in a Director (chapter 20) and in a Playbook (chapter 05): `REACHED`, `DROPPED`, `FAILED` and `ENDED` after a Goal's name, with the quantity after `BY`. Each ending counts like a Signal from the Agent whose Pursuit it was, with the same rules below: once per Agent, per argument value, from when the Block becomes active. In a Playbook the Role is the Playbook's, as for told Cues.

```regia
DURING seating:
    WHEN ENTERED:
        ASK Guest TO take_seat
    WHEN take_seat ENDED, BY ALL Guest:       # seated or not
        ENTER feast
```

```regia
PLAYBOOK Dining:
    ROLE waiter
    WHEN bring(?dish) FAILED, BY 2 OF waiter:     # two waiters couldn't bring it
        LEARN off_the_menu(?dish)
```

A quantity can't be combined with `WITH` (chapter 11): `FAILED WITH sold_out(?d), BY 2 OF waiter` is an error in 2.0. Plain `FAILED, BY 2 OF waiter` counts every Failure, whatever its Reason.

It is an **error** on every other Trigger kind: `LEARNED` (it fires only when the Fact is new, so later tellers would never count), `FORGOTTEN`, `TO`, a Goal's ending without `BY` (one Agent's own Goals), and a Subplot's `ENDED`.

Cues and the endings of asked Goals are all that is counted. A Director never reads its Agents' Facts. For anything else, Agents send a Signal: "when every Guest has tasted the wine" means each Guest's Playbook signals `tasted` and the Director waits on `WHEN tasted, FROM ALL Guest`.

## Counting

### Who counts

- **Each Agent counts once**, however many times it sends the Cue.
- Only Agents playing the Role count. A sender outside it is ignored for the quota, though it can still trigger other Plans.
- `ALL` and `n% OF` are measured against the Agents playing the Role **at the time of the check**, live, like a Role recipient (chapter 07).
- `%` means **at least that share**: 50% of 3 Guests needs 2, and 75% of 10 needs 8. Picks round up the same way (chapter 15, ADR 0031), so a share is one number wherever it is written.
- In a Playbook, the Agent itself never counts and is left out of `ALL` and `n% OF`: it never receives its own Cues (chapter 07).
- `n OF` with more than n Agents in the Role is fine. With fewer, it can't be met and never fires until enough join. The language doesn't forbid it: the Plot doesn't know the size of the hall, and in 2.0 the hall can grow. Where the build makes it certain, the Root Plot whose Role the `.regin` caps below n with no kind that joins, it is a warning (`R2115`, chapter 21). The Trace notes a count that is active while its Role is smaller than its quantity (`COUNT … SHORT`, chapter 34).
- `ALL` of an **empty Role never fires**: nobody has sent anything. "Nobody came" and "nobody is left" are `EMPTIED`, which is heard for a Role that starts empty too (chapter 19).
- In a Director the Role may be `CAST`: `WHEN ready, FROM ALL CAST:` waits for every Agent of the Staging, each counted once (chapter 15). `EXCEPT` is not allowed on a Quota.
- A Quota doesn't know who was asked. After a counted `ASK 1 OF waiter TO g`, `BY ALL waiter` still means every `waiter` (chapter 15).
- Only **current** players count. An Agent that leaves the Program stops counting, and the quota is checked again when someone leaves, so a non-sender leaving can complete an `ALL`. A joiner raises the denominator of `ALL` and `n% OF` (chapter 19).
- A Quota completed by a departure fires like any other, though no Signal is arriving: "every Guest still here has sent it" has become true. Its Placeholders are filled from the argument value of the count that was completed, not from a Signal, and `SENT` reads the counted Signals as usual. Its `plan` entry says the firing was completed by a departure (`ON DEPARTURE`, chapter 34).

### Arguments

The count is kept **per argument value**. `WHEN voted(?choice), FROM ALL Guest:` fires when every Guest has voted for the *same* choice, and fills `?choice` with it.

- An Agent that sends `voted(a)` and then `voted(b)` counts toward both.
- Values in the Trigger narrow it as usual: `voted(duel), FROM ALL Guest` counts only votes for `duel`.
- Placeholders follow chapter 03: the one that fired fills them.
- **The anonymous `?` doesn't split the count.** It matches any value, and every Signal of the Cue counts in one count. `WHEN wagered(?), FROM 3 OF Spectator:` fires at the third Spectator to wager, whatever the stakes. The stakes are read with `SENT`. A Signal can then be counted and carry data at once, with no second Signal sent only to be counted.

## What the Plan knows

A Quota Plan can read which Agents were counted, and what they sent, with the condition **`?x SENT e(args)`** (ADR 0031):

```regia
WHEN wagered(?), FROM 3 OF Spectator:
    GIVEN ?backer SENT wagered(?stake), HIGHEST ?stake, RANDOMLY:
        ASK ?backer TO give_signal
        ENTER fighting
```

- Its Matches are the Signals **counted in this firing**: one per Signal, so a Spectator who sent `wagered(4)` and then `wagered(7)` gives two Matches. A writer who wants one per sender ranks or Picks.
- Only Agents still counted: a sender who has left since is out of `SENT`, as it is out of the count.
- With a named Placeholder, only the value that fired: in `WHEN voted(?choice), FROM ALL Guest:`, `?g SENT voted(?choice)` gives the Guests who voted for the choice that won, each with `?choice` already filled.
- It is written wherever a condition goes inside the Block's Plans: a Context, an `IF`, under `NOT`, inside `COUNT(…)`, with Picks and `FOR EACH` (chapter 26). `COUNT(? SENT wagered(?))` is how many wagers were counted.
- It is an **error** anywhere else: outside the Plans of a Quota Trigger Block, or naming a Cue other than the one the Trigger counts (`R1806`).
- The count's reset after firing (below) happens once the Plan has been chosen and run, so the whole Plan reads the same Signals.
- Counted Goal endings (`take_seat ENDED, BY ALL Guest`) have no `SENT` in 2.0: which Agents' Pursuits ended is not readable.

### When counting starts and stops

The count belongs to the **Trigger**, not to a single Trigger Block:

- It starts when a Block with that Trigger becomes active: a Phase entered for `DURING <phase>`, Staging start for `DURING PLOT`, or a Giving for a Playbook.
- A Block is active **before anything is sent on its behalf**: at Staging start and on a Phase entry the counts start first, then the Role setups run, then the `ENTERED` Plans (chapters 16, 20). A Guest whose `take_seat` ends at once is counted by `WHEN take_seat ENDED, BY ALL Guest`.
- It is kept while **at least one** Block with that Trigger is active, and discarded when none is. Leaving `feast` discards the counts of `feast`'s Quota Triggers, unless `DURING PLOT` has the same Trigger.
- Senders counted before the count started don't count. A Guest that signalled `ready` during `reception` must signal again in `feast`.

### Firing

- When the quota is reached, the Trigger fires **once**, and that argument value's count **starts again from zero**. Other values' partial counts stay. The Trigger can fire again when the quota is reached anew.
- Reaching the quota is **momentary**, like a Cue (chapter 05). If no Trigger Block is a candidate (every `GIVEN` fails and there is no `ELSE`), nothing runs and the count still resets. Keeping it would make the next stray Signal fire the Plan. The Trace records a quota met with no Plan to run (`T1802`). Every counted Signal writes a `count` entry, so a Quota two short can be read in the Trace (chapter 34).
- It fires **every time** the count fills again, for as long as a Block with the Trigger is active: `WHEN complaint, FROM 3 OF Guest` at the 3rd, 6th and 9th complaint. There is no "once": a Plan that should run once leaves the Phase, or records a Fact and tests it with a `GIVEN`. This is meant, and kept.

## Selection

A Quota Trigger is **its own Trigger**, separate from the plain Cue and from other quantities:

```regia
DURING reception:
    WHEN ready, FROM Guest ?g:
        TELL ?g welcome                  # runs for every ready Guest
    WHEN ready, FROM ALL Guest:
        ENTER feast              # also runs, once, after the last one
```

- The Signal that completes the quota is handled by the plain Trigger as usual, **and** fires the Quota Trigger. One does not shadow the other.
- `FROM ALL Guest` and `FROM 3 OF Guest` on the same Cue are two Triggers with two counts.
- Blocks with the **same** Quota Trigger (same Cue, quantity and Role) compete as in chapter 13. For example, a Phase's Block beats `DURING PLOT`'s.

## Transpiler checks

**Errors**

- `R1801` A quantity on a Trigger kind other than a Cue or a Goal's ending with `BY`.
- `R1802` A quantity in front of something that isn't a Role or, in a Plot, `CAST` (`FROM ALL ?x`, `FROM ALL DIRECTOR`, `BY ALL ?x`).
- `R1803` `?who` after a quantity.
- `R1805` A quantity on a `FAILED WITH` Trigger.
- `R1804` A quantity that isn't a Number Expression, uses `RANDOM`, or reads a Placeholder that isn't filled in every Block; or, made of Values only, is 0 or less for `n OF`, or outside (0, 100] for `n% OF`.
- `R1806` `SENT` outside the Plans of a Quota Trigger Block, or naming a Cue other than the one its Trigger counts.

A Role that the build caps below an `n OF` is `R2115`, in chapter 21.

## Trace entries

**Warnings**

- `T1801` A quantity worked out at runtime to 0 or less, a share above 100%, or something that isn't a Number. The Quota doesn't fire at that check.

**Unheard** (`info`, chapter 34)

- `T1802` A quota met with no candidate Block: every `GIVEN` failed and there is no `ELSE`. The entry names the Quota and the argument value; the count has reset.

A Quota also writes `count` entries, as each Signal is counted and when it becomes active while its Role is smaller than its quantity, and marks a firing completed by a departure on its `plan` entry (chapter 34).

## Reserved words

Every keyword is listed in chapter 01, *Reserved words* (`01-statements-and-blocks.md`).

## ASL mapping notes

For *The full ASL mapping* to pick up. For Jason, these are implemented in chapter 33 (`33-jason-cast-changes-and-quotas.md`), in ASL (ADR 0013):

- **In a Director**, the mapping between Roles and Agents is already stored in the Director, so it keeps each count as generated Facts, for example `quota_seen(TriggerId, Args, Agent)`. A Signal adds the sender if it plays the Role. The Director then checks the quota against its own Role records, posts an internal event for the Quota Trigger and removes that trigger's Facts for those arguments.
- **In an Agent**, the same works against the per-Giving record of Role bindings (chapter 15's note), which the Agent needs for `FROM Role` anyway.
- Counts are cleared when the last Block with the Trigger becomes inactive: on Phase exit in the Director, on taking a Playbook away in an Agent.
- The plain Trigger's handling and the quota check both happen for the same arriving Signal. The quota check must not depend on the plain Plan being chosen.
- `SENT` needs every counted Signal kept with its arguments, not only the sender: `quota_seen(TriggerId, Args, Agent, Signal)`, the `?` slots left out of `Args`. The Plan reads them before they are removed.
- A quantity over parameters is worked out at each check from the Director's parameter beliefs.

## Regia 1.5

**None of this chapter is in 1.5** (ADR 0025). A quantity after `FROM` or `BY`, and `SENT`, are `R0109` in a 1.5 build (chapter 01). `R1801` to `R1806`, `T1801` and `T1802` are never reported.

"Every Guest has done it" is written by hand in 1.5: the Director records each Signal in a Fact of its own and compares `COUNT` over it with `COUNT(? PLAYS Guest)` (chapter 26).

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- Quantities over Subplot endings ("when every HonorDuel has ended"): *Richer Subplots*. A Subplot's `ENDED` takes no quantity in 2.0 (chapter 17).
- Counting an Agent's or Director's own Facts: `COUNT(condition)`, a Number Expression (chapter 26). `n OF` stays a Quota form.
