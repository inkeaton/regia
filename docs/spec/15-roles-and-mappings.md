# Roles and Mappings

How a Playbook names other Agents through Roles of its own, how a Plot fills those Roles when it gives the Playbook, how a Mapping picks a number or share of a Role's Agents at random, how a Role leaves Agents out with `EXCEPT`, and how a condition asks who plays a Role with `PLAYS`. Decided in the ticket *Roles inside Playbooks* (`.scratch/regia-2/issues/16-roles-in-playbooks.md`). It builds on chapters 03, 05, 07 and 13, and answers the "roles inside playbooks" and "how many instances of a role get mapped" notes in primer ch.4 and ch.5.

## Playbook Roles

A Playbook declares the Roles it talks to, the same way a Plot declares its own, at the top of its Block:

```regia
PLAYBOOK NobleSocializing:
    ROLE host
    ROLE Guest

    WHEN insult_heard(?s), FROM Guest ?who:
        GIVEN hates(?s):
            TELL ?who hates(?s)
            TELL host scandal(?s)

    TO avenge(?s), FROM host:
        DO challenge(?s)
```

- A Playbook's Role names are **local to that Playbook**, like a Plot's Role names are local to the Plot (chapter 10). Two Playbooks may each have a `host`; a Playbook's `Guest` and a Plot's `Guest` are different Roles that a Mapping may join.
- **The capital is a convention.** The showcase writes a Plot's Roles with a capital (`Host`) and a Playbook's in lowercase (`host`), so that a reader sees which side a line is on. The language doesn't read it: names are compared ignoring case (chapter 10), and a Plot's `Host` fills a Playbook's `host` with no `MAPPING` (*Mappings*, below).
- `ROLE` lines come before the Playbook's Trigger Blocks. A Playbook's `ROLE` takes no Block (`R1601`): only a Plot's Role has a setup (chapter 16).
- **`ROLE` is one word for both.** A Plot's Role is played and a Playbook's is an address, but both are Roles, classes of Agents, and a Mapping joins the two (`MAPPING Host AS host`), which reads well only because both sides are called Roles. The syntax review kept the word under chapter 01's rule for nouns.
- The Playbook stays **independent of any Plot**: it never names a Plot or a Plot's Role. Whoever gives it fills its Roles (*Mappings*, below).
- A Playbook with no `ROLE` lines can still use `FROM ?who`, `FROM DIRECTOR`, `?who` recipients and `EVERYONE`, as before.

### Roles are addresses

Inside a Playbook a Role is **an address**: it says who a Message goes to, or who a Message came from. It is **never a Value**. It may appear in three places:

| Where | Example | Meaning |
|---|---|---|
| recipient of `TELL` / `ASK` | `TELL host scandal(?s)` | every Agent bound to `host`, except the sender (chapter 07) |
| `FROM` on a Trigger, `BY` on a Goal's ending | `TO avenge(?s), FROM host:` | the Sender is bound to `host` |
| after `PLAYS` in a condition | `GIVEN ?h PLAYS host:` | `?h` is bound to `host` (*Who plays a Role*, below) |

Anywhere else a Role name is an error: as an argument (`hates(host)`, `DO toast(host)`) or in an Expression. To talk about a particular Agent, fill a Placeholder (`FROM host ?h`, `GIVEN ?h PLAYS host`) and use `?h`.

**A Playbook never directs another Agent.** It describes the behaviour of the Agent it is given to, and reaches others only by communicating: `TELL` informs, and `ASK … TO` is a request the receiver's own `TO … FROM` Plans decide on (and, after 2.0, may refuse: chapter 07, *Room for cooperation*). A Playbook can't make another Agent run an Action (the primer's `Host DO call_guards`), can't give or take away Playbooks, and can't change who plays a Role. Directing Agents, deciding what they do and when, is the job of Plots and their Directors, and even a Director does it only with Messages and Givings, never by making an Agent run an Action (chapter 20, ADR 0009).

Roles are also where cooperation will hang after 2.0 (replies, refusal, negotiation, chapter 07): those features address Roles and Agents the same way, so they add to this chapter rather than change it.

## Mappings

A **Mapping** fills a Role on the receiving side with a Role on the giving side. It is written as a trailing clause on the Director Statements that give: `ASSIGN` (a Playbook) and `START SUBPLOT` (a Plot).

```regia
PLOT RoyalBanquet:
    ROLE Host
    ROLE Guest
    ...
    DURING reception:
        WHEN food_served:
            ASSIGN NobleSocializing TO Guest, MAPPING Host AS host
            START SUBPLOT HonorDuel, MAPPING 1 OF Guest AS Challenger, MAPPING 1 OF Guest AS Defender
```

- The form is `, MAPPING <giver Role> AS <receiver Role>`, one clause per receiving Role, separated by `,` like other trailing clauses (`, WITHOUT WAITING`, chapter 08; Labels, chapter 14). The giver's Role always comes first.
- `AS` introduces the name the giver's Role goes by on the receiving side, as it does for an External name (`ext AS name`, chapter 10). The retired spelling `MAPPING a TO b` is an error (`R1514`): `TO` introduces a Goal (chapter 01).
- **Same names bind without writing them, ignoring case.** A receiving Role with no `MAPPING` is filled by the giver's Role of the same name, if there is one: above, the Playbook's `Guest` is the Plot's `Guest`, and its `host` would be the Plot's `Host` without the clause. A Plot can't declare both `Host` and `host` (chapter 10), so there is never a choice. An explicit `MAPPING` overrides it. `CAST` never binds by name (*The whole Cast*, below).
- A receiving Role left unfilled (no `MAPPING`, no Role of the same name) is a **compile-time error** at that Statement.
- The giver's side is a Role of the Plot the Statement is in, `CAST`, either of them with a count or an `EXCEPT` (below), or a Placeholder holding one Agent (`MAPPING ?who AS opponent`, chapter 20).
- Which Playbook has which Roles, and what a Plot fills them with, is part of the inferred Interface (chapter 38). A Plot that gives `Courtesy` with no `MAPPING` doesn't show on the line that `Courtesy` has a `host`; the Interface and the editor do.
- **Many to one is fine.** Several receiving Roles may be filled by the same giving Role (`MAPPING Host AS host, MAPPING Host AS speaker`). A receiving Role gets at most one `MAPPING` per Statement; two is an error.
- A `MAPPING` naming a Role the receiver doesn't declare is an error.

How a Subplot's Roles behave once started (cast at start, who is told when it ends, how Stagings are told apart) is decided in chapter 17 (`17-subplots.md`); the Mapping form and its counts are decided here and shared by both Statements.

### What a binding means

A whole-Role Mapping binds the receiving Role to the giving Role **in this Staging**, not to a list of Agents. Who is in it is checked **live**: `TELL host …` reaches whoever plays `Host` in that Staging when the Statement runs, and `FROM host` checks the Sender's Roles when the Message arrives.

### Givings

Each `ASSIGN` that runs is one **giving** of the Playbook, with its own bindings, applied to the Agents it gives the Playbook to.

```regia
ASSIGN Chatting TO Guest, MAPPING Host AS partner
ASSIGN Chatting TO Host, MAPPING Guest AS partner
```

A Guest's `partner` is the Hosts; a Host's `partner` is the Guests.

- An Agent's Playbook Role is the **union over every giving it currently holds**: from this Plot, from other Plots, and from other Stagings of the same Plot. An Agent playing both `Host` and `Guest` above has `partner` = every Host and every Guest (except itself, as always for recipients).
- `TELL partner …` reaches the union; `FROM partner` matches a Sender in any of them. This is the same rule `SIGNAL` and `FROM DIRECTOR` follow: every Plot currently giving the Playbook (chapters 05, 07).
- It is still **one Playbook** with one set of Trigger Blocks on the Agent; its Plans don't run once per giving (chapter 13).
- `REMOVE Chatting FROM Guest` takes `Chatting` away from the Guests through every giving this Staging made **whose target includes `Guest`**:
  - to `Guest` itself: the whole Role, a counted part of it (`2 OF Guest`), `Guest EXCEPT …`, or `Guest`'s Role setups (chapter 16). These givings end, and their bindings go with them.
  - to the whole Cast: `CAST`, a counted part of it, `CAST EXCEPT …`, or the `CAST` setups. These givings **narrow**: they no longer reach the Guests, and go on for everyone else. A standing one now reads `CAST EXCEPT Guest`, so a Guest who joins later doesn't get `Chatting` from it and a Servant who joins does. A counted one loses the picked Agents who play `Guest`.
  - Givings from other Stagings stay. So do this Staging's givings to another Role and to one Agent (`?who`), even for an Agent that also plays `Guest`: those givings were never made to the Guests.
- `REMOVE Chatting FROM CAST` takes away every giving of `Chatting` this Staging made, to any Role, to the Cast, or to one Agent.
- `FROM` introduces where the Playbook is taken from, in the same sense as a Sender's `FROM` (where a Message comes from, chapter 05), and with the same `<Role> ?who` shape (below). `REMOVE` and `REMOVED` replaced `UNASSIGN` and `UNASSIGNED`; the retired words are an error (`R1515`).
- **A giving belongs to the Staging that made it**, and only that Staging takes it away. An Agent holding `Keeping_watch` from the banquet and from `Poisoning` keeps the banquet's when `Poisoning` takes its own away or ends. The Agent knows which Director made each giving it holds.

#### Taking a giving from one Agent

What a `REMOVE` naming one Agent takes depends on **how the giving was made**, written with the `<Role> ?who` shape of `FROM` (chapter 07, ADR 0029):

| Written | Takes from `?who` |
|---|---|
| `REMOVE Keeping_watch FROM ?winner` | only this Staging's givings made **to `?winner`** (`ASSIGN Keeping_watch TO ?winner`). A Guard setup's giving stays. |
| `REMOVE Dining FROM Guest ?offended` | `?offended` out of this Staging's givings whose target includes `Guest`, as `FROM Guest` above. They go on for everyone else, now leaving `?offended` out: a standing one reads `Guest EXCEPT ?offended`. |
| `REMOVE Dining FROM CAST ?offended` | everything this Staging gave `?offended` of `Dining`: its givings to that Agent end, and it is taken out of every other one. |

- Standing givings stay standing: a later joiner still gets the Playbook, only `?who` is left out.
- `FROM Guest ?who` when `?who` doesn't play `Guest`, or a `FROM ?who` with no giving to that Agent, does nothing, with a Trace warning (`T1505`).
- `REMOVED` fires only if `?who` has lost its last giving of the Playbook, from any Staging.

#### Giving it back: `ASSIGN … TO <Role> ?who`

```regia
WHEN insult_thrown(?offender), FROM Guest ?offended:
    REMOVE Dining FROM Guest ?offended
    REMOVE Dining FROM Guest ?offender
    START SUBPLOT HonorDuel(?offended, ?offender),
        MAPPING ?offended AS Challenger, MAPPING ?offender AS Defender, MAPPING Guest AS Spectator
WHEN HonorDuel(?a, ?b) ENDED:                    # however it ended (chapter 17)
    ASSIGN Dining TO Guest ?a
    ASSIGN Dining TO Guest ?b
```

The Plot's arguments (chapter 17) carry the two duellists to the `ENDED` Plan. It runs for every ending, a Subplot ended from above (`DROP SUBPLOT`, `UNTIL EXITED`) included, which the parent hears as `DROPPED` and then `ENDED` (chapter 17, ADR 0030). The giving back is written once.

- `ASSIGN P TO Guest ?who` **lifts the exclusion** of `?who` from this Staging's givings of `P` whose target includes `Guest`, whether it was written (`Guest EXCEPT ?who`) or made by narrowing. `?who` holds those givings again, with their bindings, and later `REMOVE P FROM Guest` takes them as it takes everyone's.
- It makes no new giving. With no exclusion of `?who` to lift, or when `?who` doesn't play `Guest`, it does nothing, with a Trace warning (`T1506`).
- It takes no count, no `MAPPING` and no `UNTIL EXITED`: the giving it reopens already has its own (`R1513`).
- `ASSIGN P TO ?who` is still a new giving to that one Agent, which `REMOVE P FROM Guest` doesn't reach. To give a Guest back what the Guests have, write `TO Guest ?who`.
- A giving to a whole Role is **standing**: it also reaches Agents who join the Role later, until it is taken away. A giving to a counted target is not (chapter 19).
- A giving ends when a `REMOVE` takes it away, when its Staging ends, or, if it was made **for a Phase**, when that Phase is left. A giving is for a Phase when it comes from the Phase's Role setup (chapter 16) or carries `UNTIL EXITED` (below).

### Until the Phase is left: `UNTIL EXITED`

An `ASSIGN` or a `START SUBPLOT` in a Plan of a `DURING <phase>` Block may end with `, UNTIL EXITED`:

```regia
DURING feast:
    WHEN insult_thrown(?a, ?b):
        START SUBPLOT HonorDuel, MAPPING ?a AS Challenger, MAPPING ?b AS Defender, UNTIL EXITED
        ASSIGN Brawling TO 2 OF Guest, UNTIL EXITED
```

- The giving is taken away, or the Subplot ended, when the Plot leaves the Phase the Plan belongs to, after that Phase's `EXITED` Plan (chapter 20). No `REMOVE` or `DROP SUBPLOT` is written in another Block.
- A Subplot ended this way ends as with `DROP SUBPLOT` (chapter 17): the parent hears `DROPPED` and then `ENDED`, after the transition, in the new Phase's Plans or else in `DURING PLOT`.
- An earlier `REMOVE` or `DROP SUBPLOT` still works, and so does the Subplot ending itself.
- The clause comes last, after the `MAPPING` clauses. It fits any target: a whole Role (still standing while the Phase lasts), a counted target, or `?who`.
- In a `DURING PLOT` Plan it is an error: what such a Plan gives already ends with the Staging. So it is in a Role setup, where the Phase's setup already means it (chapter 16).

### Given and taken: `ASSIGNED` and `REMOVED`

A Playbook can react to being given and to being taken away. The two Trigger kinds have no item: their subject is the enclosing Playbook, as `ENTERED` and `EXITED` have the enclosing `DURING` Block (chapter 20).

```regia
PLAYBOOK Dining:
    WHEN ASSIGNED:
        IF hungry:
            PURSUE have_dinner, WITHOUT WAITING

    WHEN REMOVED:
        FORGET plate(?p)
```

- `ASSIGNED` fires when the Agent goes from holding **no** giving of the Playbook to holding one. `REMOVED` fires when its **last** giving goes. A second giving while one is held fires nothing, and neither does losing one of two: a giving has no identity a Plan could read (*Not in 2.0*).
- `REMOVED` fires whatever took the last giving: a `REMOVE`, a Phase left, a Staging ending. It does not fire when the Agent leaves the Program: its Plans stop with it (chapter 19).
- A Playbook taken and given again by one `ENTER` (both Phases give it, or the Phase is re-entered) fires `REMOVED`, then `ASSIGNED`.
- They are worded like the Statement that causes them, as `LEARN` and `LEARNED` are. `GIVEN` is the Context's word (chapter 06).
- They take no `FROM`, no `BY` and no Placeholder. They are **Playbook Trigger kinds only**: a Director does the giving and doesn't need to hear of it.
- One Plan each per Playbook is the usual case. Several follow chapter 13 like any Trigger.

### Taking a Playbook away

When an Agent's last giving of a Playbook goes:

1. **Its running Plans stop**, and the Pursuits they were carrying are dropped, as `DROP` would drop them (chapter 08): sub-Goals first, then the Goal, then whatever was waiting on it.
2. **The closing Plans run.** Each drop fires `DROPPED`, then `ENDED`, and those Plans run wherever they sit, **the Playbook being taken included**. Then its `REMOVED` Plan runs.
3. **Nothing else of the Playbook starts.** From step 1 on, no other Trigger of the Playbook is taken: a Cue, a Fact change or a new Goal finds no Plan in it.

- The closing Plans are ordinary Plans and run to their end. They may `WAIT`. A `PURSUE` in one of them for a Goal whose only recipe is in the Playbook fails for lack of a Plan (chapter 11), and the `FAILED` Plan for it, being the Playbook's, doesn't run.
- A closing Plan sees the Playbook's Local Facts and can forget them. What it doesn't forget stays (chapter 10).
- A closing Plan speaks through the givings **as they were just before the taking**: a `TELL` to a Playbook Role reaches the Role as those givings bound it, and a `SIGNAL` reaches the Directors that were giving the Playbook. A Director whose Staging has ended hears nothing (chapter 17), and a whole-Role binding through that Staging reaches nobody; a counted pick and a `MAPPING ?who` still reach their Agents.
- If the Playbook is given back while closing Plans still run, they finish, and `ASSIGNED` fires as for any first giving.
- A stopped Plan whose Trigger isn't a Goal just stops, with a Trace entry.

This is why a Director that takes `Dining` away doesn't leave a dirty plate: `WHEN have_dinner DROPPED` is `Dining`'s own Plan, and it still runs (ADR 0021).

## The whole Cast: `CAST`

`CAST` is the Role **every Agent of the Staging plays**. A Plot doesn't declare it, and it is written wherever one of the Plot's own Roles can be:

```regia
PLOT RoyalBanquet:
    ROLE Host
    ROLE Guest
    ROLE Guard

    DURING feast:
        WHEN toast_called, FROM CAST ?who:
            TELL CAST raise_glass(?who)                  # every Agent of this Staging, once
            ASSIGN Cheering TO CAST EXCEPT ?who
        WHEN duel_called:
            START SUBPLOT Wagering, MAPPING CAST EXCEPT Guard AS Spectator
        WHEN CAST ?late JOINED:
            TELL Host arrival(?late)
```

- **Each Agent is in it once**, however many Roles it plays. A knight who is `Guest` and `Guard` hears `TELL CAST …` once; `TELL Guest …` and `TELL Guard …` reach it twice.
- It is the Cast of **this Staging**: the Root Plot's living Cast, or a Subplot's Cast as it was fixed at its start (chapter 17). `EVERYONE` is still the whole game (chapter 07).
- It is a recipient, an `ASSIGN` and `REMOVE` target (standing, like a whole Role), the giver's side of a `MAPPING`, the Role of a `FROM`, a `BY` or a Quota (chapter 18), the subject of `JOINED`, `LEFT` and `EMPTIED` (chapter 19), the Role after `PLAYS`, and the header of a setup (`CAST:`, chapter 16). It takes counts and `EXCEPT` like any Role.
- `REMOVE P FROM CAST` takes away every Giving of `P` this Staging made. `REMOVE P FROM Guest` takes `P` from the Guests in a Giving made to `CAST` too, which goes on for everyone else as `CAST EXCEPT Guest` (*Givings*, above).
- **It never binds by name.** A Playbook Role is filled from the whole Cast only by writing `MAPPING CAST AS audience`.
- `CAST` is reserved. `ROLE Cast` is an error in a Plot and in a Playbook, in any case. A Playbook can't write `CAST`: it doesn't know a Plot, and its widest audience is a Role or `EVERYONE`.

It is a Role and not a second `EVERYONE` because everything a Director does to a Role it sometimes needs to do to everybody: give a Playbook, map, count, leave someone out (ADR 0024).

## Counts and fractions

A Mapping, the target of an `ASSIGN`, or the recipient of a `TELL` or an `ASK` can take a **part of a Role**, picked at random:

| Written | Picks |
|---|---|
| `Guest` | the whole Role (live, as above) |
| `<Expression> OF Guest` | that many of its Agents |
| `<Expression>% OF Guest` | that share of its Agents, in percent |

```regia
ASSIGN Brawling TO 30% OF Guest
ASSIGN Brawling TO ?share% OF Guest
ASSIGN Gossip TO Guest, MAPPING RANDOM(1, 3) OF Host AS confidant
ASSIGN Brawling TO 2 OF Guest, MAPPING 1 OF Guest AS rival
```

- Counts and fractions are allowed in the target of `ASSIGN … TO`, on the giver's side of `MAPPING`, and on a Role recipient (below). They are an error on `REMOVE`, after `PLAYS`, after `EXCEPT`, and on `EVERYONE`. A quantity on `FROM` or `BY` is a Quota, with its own rules (chapter 18).
- `%` follows the Expression it applies to, and is followed by `OF`: `50% OF Guest`, `?share% OF Guest`, `(?n * 10)% OF Guest`. A space before it is allowed, as around an operator; the spec and the tools write none. It is the share of a count and nothing else: Regia has one Number kind (chapter 04), so `50%` is never a Value (`LET ?x BE 50%.`, `WEIGHT 30%`), and `0.5 OF Guest` is a count, never "half". A `%` anywhere but before `OF` is `R1517`.
- `%` is a percentage, never a remainder, which Regia doesn't have (chapter 04, ADR 0045). It replaced the unit word `PERCENT`, which is `R1516`.
- The Expression follows chapter 04: Values, filled Placeholders, `RANDOM`, arithmetic.

### How the pick works

- **Once, when the Statement runs.** The Agents are drawn uniformly at random from those playing the Role in this Staging at that moment. How the Target makes random numbers is its own, as for `RANDOMLY` (chapter 09), but the draw is covered by the run's seed (chapter 34).
- **The pick never grows.** Unlike a whole-Role binding, it is a fixed set: an Agent who starts playing the Role later never joins it. An Agent who stops playing the giving Role drops out of it.
- **No Agent twice in one Statement.** Counted picks from the same Role inside one Statement come from one pool, without replacement. Above, the two Guests in `HonorDuel` are different Guests, and each brawler's `rival` is a Guest who isn't one of the two brawlers. Picks in different Statements are independent. A whole-Role Mapping in the same Statement still means the whole Role.
- **One pick per Statement, shared.** In `ASSIGN Gossip TO Guest, MAPPING 1 OF Host AS confidant`, every Guest has the same `confidant`. A separate pick per receiving Agent is not in 2.0.

### Odd values

| Case | Result |
|---|---|
| fraction, or a count that isn't whole | rounds **up**: 50% of 3 Guests is 2, 30% of 2 is 1. `%` means at least that share, here and in a Quota (chapter 18, ADR 0031) |
| more than are left in the pool | takes everyone left; a runtime warning in the Trace |
| negative | counts as 0; a runtime warning in the Trace |
| 0 | an empty pick; the Role is empty, which is not an error (sending to it sends nothing, chapter 07) |
| not a Number | the Plan fails (chapter 11) |

These follow the rules for `WAIT` (chapter 12) and `WEIGHT` (chapter 09).

### A counted recipient

`TELL` and `ASK` take a count or a share of a Role, in a Playbook and in a Plot:

```regia
PLAYBOOK Dining:
    ROLE waiter

    TO have_dinner:
        GIVEN wants(?dish):
            ASK 1 OF waiter TO bring(?dish)      # one Servant, not all of them

    WHEN bring(?dish) REACHED, BY waiter ?w:
        TELL ?w thanks
```

- **The pick is made each time the Statement runs**, from the Agents the Role reaches at that moment, the sender left out (chapter 07). Two requests may go to two different Servants. A Servant kept for the whole Giving is the pick per receiver, not in 2.0.
- The odd values are the table's. **A count that finds nobody sends nothing**, and the Plan goes on, as for an empty Role (chapter 07), with the `T1502` warning. It is not a Failure: `ASK 1 OF waiter` and `ASK waiter` behave alike in an empty hall. A Plan that must not wait in vain tests first: `GIVEN ? PLAYS waiter`.
- Who was picked is not handed back. An asker learns it from the ending (`BY waiter ?w`, chapter 05).
- A Quota over the endings is still measured against the whole Role (chapter 18): after `ASK 1 OF waiter TO bring(?dish)`, `WHEN bring(?dish) ENDED, BY ALL waiter` waits for Servants who were never asked. Write `BY 1 OF waiter`, or no quantity.
- In a Playbook the Role is the Playbook's, over the union of its Givings, as for a whole-Role recipient.

## Leaving Agents out: `EXCEPT`

In a **Plot**, a Role can leave out the Agents of other Roles, or single Agents:

```regia
START SUBPLOT Wagering, MAPPING Guest EXCEPT Duellist AS Spectator
ASSIGN Poisoning TO 1 OF Guest EXCEPT Guard
TELL Guest EXCEPT ?who scandal(?who)
START SUBPLOT HonorDuel(?offender), MAPPING Guest EXCEPT ?offended, ?offender AS Spectator
```

| Written | Means |
|---|---|
| `Guest EXCEPT Guard` | the Agents playing `Guest` and not `Guard`, in this Staging |
| `Guest EXCEPT ?who` | the Agents playing `Guest`, without the Agent `?who` holds |
| `2 OF Guest EXCEPT Guard` | two of the Agents playing `Guest` and not `Guard` |
| `Guest EXCEPT ?a, ?b` | the Agents playing `Guest`, without the Agents `?a` and `?b` hold |
| `Guest EXCEPT Guard, ?who` | the Agents playing `Guest` and not `Guard`, without the Agent `?who` holds |

- It is allowed where a Role is a **recipient**, an **`ASSIGN` target**, or the **giver's side of a `MAPPING`**. `CAST` takes it too: `CAST EXCEPT Duellist` is "everyone else".
- **It is as live as the Role it is on.** A whole-Role Mapping or a standing Giving with `EXCEPT` is checked when used, on both sides: an Agent who joins as `Guest` and not `Guard` gets `ASSIGN Poisoning TO Guest EXCEPT Guard`. With `EXCEPT ?who` the Agent left out is the one the Placeholder held when the Statement ran. A counted pick is drawn from what is left and is then fixed, as always. A Subplot's Cast is still fixed when it starts (chapter 17).
- **One `EXCEPT` per Role, followed by a list**: one or more items separated by commas, each one Role of this Plot or one filled Placeholder, in any mix. A comma followed by a keyword (`, MAPPING`, `, UNTIL EXITED`) ends the list and starts the Statement's next clause. Without a comma, the list ends at the first word that can't be an item: `TO` in `MAPPING Guest EXCEPT ?a, ?b AS Spectator`, or the Message in `TELL Guest EXCEPT ?a, ?b scandal(?b)`. `Guest EXCEPT Guard EXCEPT ?who` (write `Guest EXCEPT Guard, ?who`), `EXCEPT 2 OF Guard`, `EXCEPT CAST`, `EXCEPT EVERYONE`, and the same Role or Placeholder twice in one list are errors. Two Placeholders that hold the same Agent when the Statement runs are fine.
- An `EXCEPT ?who` whose Placeholder doesn't hold an Agent leaves nobody out for that item, with a Trace warning; the list's other items still apply. Director Statements never fail (chapter 20).
- It is **not** allowed:
  - on **`REMOVE`**, which takes a plain Role, `CAST`, `?who`, or a Role followed by `?who` (*Taking a giving from one Agent*). A Giving made to `Guest EXCEPT Guard` (or `Guest EXCEPT Guard, ?who`) counts as made to `Guest`, and `REMOVE Poisoning FROM Guest` takes it. Taking apart two Givings made to the same Role needs a Giving to have an identity (*Not in 2.0*).
  - Narrowing adds to a Giving's list: `ASSIGN P TO CAST EXCEPT Guard`, then `REMOVE P FROM Guest` and `REMOVE P FROM Host`, leaves `CAST EXCEPT Guard, Guest, Host`, the same as if it had been written so. `ASSIGN P TO Guest ?who` lifts `?who` from the list, whether it was written or narrowed.
  - on **`FROM`, `BY` and Quotas**. For one Sender a Context says it: `WHEN cheered, FROM Guest ?who:` with `GIVEN NOT ?who PLAYS Guard:` under it. A Quota over part of a Role is not in 2.0 (chapter 18).
  - after **`PLAYS`**: write `?x PLAYS Guest AND NOT ?x PLAYS Guard`.
  - in a **Playbook**. A recipient already leaves the sender out, and leaving out anyone else there is not in 2.0.

## Who plays a Role: `PLAYS`

A condition can ask who plays a Role. `<who> PLAYS <Role>` is written in a Context, an `IF` or a `COUNT(…)`, in a Plot and in a Playbook, and is matched like a Fact (chapter 03):

```regia
PLAYBOOK Duelling:
    ROLE opponent

    TO strike:
        GIVEN ?o PLAYS opponent AND ?o != ME:
            DO lunge(?o)

PLAYBOOK Serving:
    ROLE host

    WHEN guest_arrived(?g):
        GIVEN ME PLAYS host:
            DO greet(?g)

PLOT HonorDuel:
    ROLE Challenger
    ROLE Defender

    DURING fight:
        WHEN interrupted:
            GIVEN ?c PLAYS Challenger AND ?d PLAYS Defender:
                END PLOT WITH duel_abandoned(?c, ?d)
        WHEN yielded, FROM ?loser:
            GIVEN ?winner PLAYS CAST AND ?winner != ?loser:
                END PLOT WITH duel_won(?winner)
```

- **The left side** is a Placeholder, a blank `?`, or `ME`. An unfilled Placeholder is filled with an Agent playing the Role; a filled one is tested. A filled Placeholder that doesn't hold an Agent just doesn't match. `ME` is a Playbook's word (chapter 03).
- **The right side** is one Role: in a Plot, a Role of the Plot or `CAST`, checked in this Staging; in a Playbook, a Role of the Playbook, checked over the union of the Givings the Agent holds, as `FROM host` is. A Role bound to a counted pick or to one Agent is that fixed set.
- **It is checked live**, when the condition is: it sees the Cast as it is now, not as it was when the Playbook was given.
- **The Agent itself is not left out.** A recipient leaves the sender out because nobody tells themselves; a test says who plays the Role, and that may be the Agent running the Plan. `ME PLAYS host` depends on it. A Plan that wants someone else adds `AND ?o != ME`.
- **With several Matches** the condition follows chapter 26 like any other: one Match by default, a Pick (`, RANDOMLY`), every one with `FOR EACH`, their number with `COUNT(? PLAYS Guest)`.
- `NOT`, `AND` and `OR` treat it as they treat a Fact (chapters 03, 06): under `NOT` the Placeholder must already be filled.
- **It is a condition only.** There is no Trigger on it (`WHEN ?x PLAYS host LEARNED:` is an error). A Director hears of cast changes with `JOINED`, `LEFT` and `EMPTIED` (chapter 19); a Playbook doesn't hear of them in 2.0.
- It is not allowed in a Role setup, which has no conditions (chapter 16).
- `PLAYS` is the word Instancing already uses for the same relation (`KIND noble, PLAYS Guest`, chapter 21).

A Role is still not a Value: `hates(host)` stays an error, and `PLAYS` is the one way from a Role to an Agent besides a Message arriving (ADR 0023).

## Transpiler checks

**Errors**

- `R1501` A Role name used as a Value: as an argument or in an Expression.
- `R1502` A Role used but not declared by the Playbook or Plot.
- `R1503` A receiving Role left unfilled by a giving Statement (the message names the Role and suggests a `MAPPING`).
- `R1504` Two `MAPPING`s to one receiving Role in one Statement, or a `MAPPING` to a Role the receiver doesn't declare.
- `R1506` A count or fraction where none is allowed: on `REMOVE`, after `PLAYS`, after `EXCEPT`, or on `EVERYONE`.
- `R1507` A Playbook Statement that directs another Agent (`ASSIGN`, `MAPPING`, …). Director Statements are only for Directors.
- `R1508` `WHEN ASSIGNED:` or `WHEN REMOVED:` in a Plot, or with an item, a Placeholder, `FROM` or `BY`.
- `R1509` `UNTIL EXITED` outside a Plan of a `DURING <phase>` Block (in `DURING PLOT`, in a Role setup), not last in its Statement, or on a Statement other than `ASSIGN` and `START SUBPLOT`.

- `R1510` `EXCEPT` where it isn't allowed: in a Playbook, on `REMOVE`, on `FROM` or `BY`, after `PLAYS`, on `EVERYONE`; a second `EXCEPT` on one Role (the message suggests one list: `EXCEPT Guard, ?who`); an item of the list that isn't one Role of this Plot or one Placeholder; or the same Role or Placeholder twice in one list.
- `R1511` `PLAYS` misused: a left side that isn't a Placeholder, `?` or `ME`; a right side that isn't one Role declared here (or `CAST`, in a Plot); or `PLAYS` in a Trigger or a Role setup.
- `R1512` `CAST` declared as a Role, or written in a Playbook.
- `R1513` `ASSIGN P TO <Role> ?who` with a count, a `MAPPING` or `UNTIL EXITED`.
- `R1514` The retired `MAPPING a TO b` (hint: `MAPPING a AS b`).
- `R1515` The retired `UNASSIGN` or `UNASSIGNED` (hint: `REMOVE`, `REMOVED`).
- `R1516` The retired `n PERCENT OF Role` (hint: `n% OF Role`).
- `R1517` A `%` that isn't directly before `OF` (hint: a share is written `n% OF Role`; Regia has no remainder, and Weights are relative).

`R1505` (`MAPPING ?who AS …`) is no longer given: chapter 20 allows it.

## Trace entries

**Failures**

- `T1501` A count or fraction that isn't a Number.

**Warnings**

- `T1502` A count asking for more Agents than are left in the pool: it takes everyone left.
- `T1503` A negative count, counted as 0.
- `T1504` An `EXCEPT ?who` whose Placeholder doesn't hold an Agent: nobody is left out.
- `T1505` A `REMOVE` naming one Agent that takes nothing: `FROM <Role> ?who` when `?who` doesn't play the Role, or `FROM ?who` with no giving made to that Agent.
- `T1506` An `ASSIGN P TO <Role> ?who` with nothing to lift: `?who` doesn't play the Role, or no giving of `P` leaves it out.

## Reserved words

Every keyword is listed in chapter 01, *Reserved words* (`01-statements-and-blocks.md`).

## Not in 2.0

- **One Role filled by several giving Roles** (`Host` and `Guest` both as `noble`). `MAPPING CAST AS noble` covers the case of all of them.
- **A separate pick per receiving Agent** (`ASSIGN Chatting TO EACH Guest, MAPPING 1 OF Host AS partner`), a Servant of one's own. It needs a binding per Agent inside one Giving, and comes with a Giving's identity. Until then `ASK 1 OF waiter` picks afresh for each request.
- **A Giving's identity**: taking away one of two Givings to the same Role (`REMOVE` with `EXCEPT`, or naming the Giving), and a Plan that knows which Giving it runs for. A Playbook held twice runs one set of Plans over the union of its Givings, so a `SIGNAL` reaches every Director giving it and a Playbook Role reaches every binding (chapter 17, *An Agent in two Stagings of one Plot*).
- **`EXCEPT` in a Playbook**, and on `FROM` and `BY`.
- **A Trigger on `PLAYS`**: an Agent hearing that someone started or stopped playing one of its Playbook's Roles.
- **Recasting**: a Director moving an Agent into or out of a Role of a running Staging (chapter 19).

## ASL mapping notes

For *The full ASL mapping* to pick up:

- Each Agent needs, per giving it holds, the Playbook, the giving Director (and Staging), and each Playbook Role's binding: either a Plot Role in that Staging (resolved live against the infrastructure's record of who plays it) or a fixed set of Agents (a counted pick, from which leavers are removed).
- `TELL host f` expands to a send to every Agent in the union of the Agent's bindings for `host`, minus itself. `FROM host` in a Trigger becomes a Context test on the Sender against the same union, at arrival time.
- A counted pick runs in the Director: it reads the Role's current Agents, shuffles, takes the count, and removes them from the Statement's pool for that Role. The chosen set is sent along with the giving.
- A counted recipient in a Playbook is drawn by the Agent, from the same union `TELL host f` sends to. `?x PLAYS host` is a test against that union with the Agent itself left in. In Jason both read the rule `regia_plays` (chapter 29), the draw is `regia.pick` (chapter 39), and a Director's `PLAYS` is chapter 30's.
- A Subplot Role filled with `MAPPING ?who` brings its Playbooks to every Root Role that maps to any Role of the Plot starting it, as `ASSIGN … TO ?who` does (chapter 29).
- `EXCEPT` on a live binding has to travel with it: the Agent's record of a binding becomes "this Plot Role, minus those Roles and those Agents". `CAST` is the union of the Staging's Role records.
- The Director's standing record of a Giving to `CAST` keeps a list of excluded Roles, which `REMOVE … FROM <Role>` adds to. A joiner gets the Giving only if it plays none of them.
- 1.0's `signal_directors` already keeps "which Director gave this Playbook"; bindings extend that record.
- Decided in chapter 29 (`29-jason-givings.md`): the per-giving record `regia_given`, the cast copy each Agent keeps for live bindings, and how recipients and `FROM Role` are expanded against them.

## Regia 1.5

In 1.5 (ADR 0025): Playbook Roles, Mappings, Givings, `UNTIL EXITED`, `WHEN ASSIGNED` and `WHEN REMOVED`, `CAST`, counts and fractions, `EXCEPT` and `PLAYS`.

1.5 has no joiners, so a Staging's cast is fixed when it starts and only shrinks (chapter 19). What this chapter says about Agents who join later doesn't apply: a standing Giving reaches the Agents playing the Role when it is made, and lasts until it is taken away. `WHEN CAST ?late JOINED` is later (`R0109`, chapter 01), and so are `BY`, and Quotas over a Role or over the endings of a Goal.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`). `MAPPING … AS`, `REMOVE` and `REMOVED`, and `R1514` and `R1515` in the ticket *`TO` and `FROM` outside Triggers* (`.scratch/syntax-review/issues/05-to-and-from.md`), which also made `ASSIGN … TO` one of the two closed exceptions to the rule that `TO` introduces a Goal (chapter 01, ADR 0043).

## Not decided here

- How Subplots run once started, parent and child cooperation, and how Stagings of one Plot are told apart: chapter 17 (`17-subplots.md`).
- A Director can send `?who` Messages, `ASSIGN`/`REMOVE` a Playbook to it (not standing), and map it onto a Role (chapter 20).
- Whether an Agent hears of cast changes at all: with told Facts and news, not here.
- What happens to bindings and picks when Agents join or leave mid-Plot: decided in chapter 19 (`19-cast-changes.md`). Whole-Role givings are standing; picks never grow and leavers drop out.
- Starting state for a Role, and for the whole Cast: *Role setup*, decided in chapter 16 (a Block on `ROLE` or `CAST`; its `ASSIGN` takes the same Mappings, without counted picks).
