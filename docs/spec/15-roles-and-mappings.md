# Roles and Mappings

How a Playbook names other Agents through Roles of its own, how a Plot fills those Roles when it gives the Playbook, and how a Mapping picks a number or share of a Role's Agents at random. Decided in the ticket *Roles inside Playbooks* (`.scratch/regia-2/issues/16-roles-in-playbooks.md`). It builds on chapters 03, 05, 07 and 13, and answers the "roles inside playbooks" and "how many instances of a role get mapped" notes in primer ch.4 and ch.5.

## Playbook Roles

A Playbook declares the Roles it talks to, the same way a Plot declares its own, at the top of its Block:

```regia
PLAYBOOK NobleSocializing:
    ROLE host.
    ROLE Guest.

    WHEN insult_heard(?s) FROM Guest ?who:
        GIVEN hates(?s):
            TELL ?who hates(?s).
            TELL host scandal(?s).

    TO avenge(?s) FROM host:
        DO challenge(?s).
```

- A Playbook's Role names are **local to that Playbook**, like a Plot's Role names are local to the Plot (chapter 10). Two Playbooks may each have a `host`; a Playbook's `Guest` and a Plot's `Guest` are different Roles that a Mapping may join.
- `ROLE` lines come before the Playbook's Trigger Blocks.
- The Playbook stays **independent of any Plot**: it never names a Plot or a Plot's Role. Whoever gives it fills its Roles (*Mappings*, below).
- A Playbook with no `ROLE` lines can still use `FROM ?who`, `FROM DIRECTOR`, `?who` recipients and `EVERYONE`, as before.

### Roles are addresses

Inside a Playbook a Role is **only an address**: it says who a Message goes to, or who a Message came from. It may appear in exactly two places:

| Where | Example | Meaning |
|---|---|---|
| recipient of `TELL` / `ASK` | `TELL host scandal(?s).` | every Agent bound to `host`, except the sender (chapter 07) |
| `FROM` on a Trigger | `TO avenge(?s) FROM host:` | the Sender is bound to `host` |

Anywhere else a Role name is an error: as an argument (`hates(host)`, `DO toast(host)`), in a Context, or in an Expression. To talk about a particular Agent, fill a Placeholder (`FROM host ?h`) and use `?h`.

**A Playbook never directs another Agent.** It describes the behaviour of the Agent it is given to, and reaches others only by communicating: `TELL` informs, and `ASK … TO` is a request the receiver's own `TO … FROM` Plans decide on (and, after 2.0, may refuse: chapter 07, *Room for cooperation*). A Playbook can't make another Agent run an Action (the primer's `Host DO call_guards`), can't give or take away Playbooks, and can't change who plays a Role. Directing Agents, deciding what they do and when, is the job of Plots and their Directors.

Roles are also where cooperation will hang after 2.0 (replies, refusal, negotiation, chapter 07): those features address Roles and Agents the same way, so they add to this chapter rather than change it.

## Mappings

A **Mapping** fills a Role on the receiving side with a Role on the giving side. It is written as a trailing clause on the Director Statements that give: `ASSIGN` (a Playbook) and `START SUBPLOT` (a Plot).

```regia
PLOT RoyalBanquet:
    ROLE Host.
    ROLE Guest.
    ...
    DURING reception:
        WHEN food_served:
            ASSIGN NobleSocializing TO Guest, MAPPING Host TO host.
            START SUBPLOT HonorDuel, MAPPING 1 OF Guest TO Challenger, MAPPING 1 OF Guest TO Defender.
```

- The form is `, MAPPING <giver Role> TO <receiver Role>`, one clause per receiving Role, separated by `,` like other trailing clauses (`, WITHOUT WAITING`, chapter 08; Labels, chapter 14). The giver's Role always comes first.
- **Same names bind without writing them.** A receiving Role with no `MAPPING` is filled by the giver's Role of the same name, if there is one: above, the Playbook's `Guest` is the Plot's `Guest`. An explicit `MAPPING` overrides it.
- A receiving Role left unfilled (no `MAPPING`, no Role of the same name) is a **compile-time error** at that Statement.
- The giver's side must be a Role of the Plot the Statement is in. `MAPPING ?who TO opponent`, filling a Role with one Agent held by a Placeholder, is an error in 2.0 (see *Not decided here*).
- **Many to one is fine.** Several receiving Roles may be filled by the same giving Role (`MAPPING Host TO host, MAPPING Host TO speaker`). A receiving Role gets at most one `MAPPING` per Statement; two is an error.
- A `MAPPING` naming a Role the receiver doesn't declare is an error.

How a Subplot's Roles behave once started (who is told when it ends, how Stagings are told apart) is decided in *Subplots and Stagings*; the Mapping form and its counts are decided here and shared by both Statements.

### What a binding means

A whole-Role Mapping binds the receiving Role to the giving Role **in this Staging**, not to a list of Agents. Who is in it is checked **live**: `TELL host …` reaches whoever plays `Host` in that Staging when the Statement runs, and `FROM host` checks the Sender's Roles when the Message arrives.

### Givings

Each `ASSIGN` that runs is one **giving** of the Playbook, with its own bindings, applied to the Agents it gives the Playbook to.

```regia
ASSIGN Chatting TO Guest, MAPPING Host TO partner.
ASSIGN Chatting TO Host, MAPPING Guest TO partner.
```

A Guest's `partner` is the Hosts; a Host's `partner` is the Guests.

- An Agent's Playbook Role is the **union over every giving it currently holds**: from this Plot, from other Plots, and from other Stagings of the same Plot. An Agent playing both `Host` and `Guest` above has `partner` = every Host and every Guest (except itself, as always for recipients).
- `TELL partner …` reaches the union; `FROM partner` matches a Sender in any of them. This is the same rule `SIGNAL` and `FROM DIRECTOR` follow: every Plot currently giving the Playbook (chapters 05, 07).
- It is still **one Playbook** with one set of Trigger Blocks on the Agent; its Plans don't run once per giving (chapter 13).
- `UNASSIGN Chatting FROM Guest` takes away exactly that giving and its bindings. Other givings, and the Roles they bind, stay.

## Counts and fractions

A Mapping, or the target of an `ASSIGN`, can take a **part of a Role**, picked at random:

| Written | Picks |
|---|---|
| `Guest` | the whole Role (live, as above) |
| `<Expression> OF Guest` | that many of its Agents |
| `<Expression> PERCENT OF Guest` | that share of its Agents |

```regia
ASSIGN Brawling TO 30 PERCENT OF Guest.
ASSIGN Gossip TO Guest, MAPPING RANDOM(1, 3) OF Host TO confidant.
ASSIGN Brawling TO 2 OF Guest, MAPPING 1 OF Guest TO rival.
```

- Counts and fractions are allowed **only** in the target of `ASSIGN … TO` and on the giver's side of `MAPPING`. They are not recipients: `TELL 2 OF Guest …` is an error.
- `PERCENT` is a unit word, like `SECONDS` for a Duration (chapter 12). Regia has one Number kind (chapter 04), so `0.5 OF Guest` is a count, never "half".
- The Expression follows chapter 04: Values, filled Placeholders, `RANDOM`, arithmetic.

### How the pick works

- **Once, when the Statement runs.** The Agents are drawn uniformly at random from those playing the Role in this Staging at that moment. How the Target makes random numbers is its own, as for `EITHER`/`OR` (chapter 09).
- **The pick never grows.** Unlike a whole-Role binding, it is a fixed set: an Agent who starts playing the Role later never joins it. An Agent who stops playing the giving Role drops out of it.
- **No Agent twice in one Statement.** Counted picks from the same Role inside one Statement come from one pool, without replacement. Above, the two Guests in `HonorDuel` are different Guests, and each brawler's `rival` is a Guest who isn't one of the two brawlers. Picks in different Statements are independent. A whole-Role Mapping in the same Statement still means the whole Role.
- **One pick per Statement, shared.** In `ASSIGN Gossip TO Guest, MAPPING 1 OF Host TO confidant`, every Guest has the same `confidant`. A separate pick per receiving Agent is not in 2.0.

### Odd values

| Case | Result |
|---|---|
| fraction, or a count that isn't whole | rounds **down**: 50 PERCENT of 3 Guests is 1 |
| more than are left in the pool | takes everyone left; a runtime warning in the Trace |
| negative | counts as 0; a runtime warning in the Trace |
| 0 | an empty pick; the Role is empty, which is not an error (sending to it sends nothing, chapter 07) |
| not a Number | the Plan fails (chapter 11) |

These follow the rules for `WAIT` (chapter 12) and `WEIGHT` (chapter 09).

## Transpiler checks

- A Role name used in a Playbook outside a recipient or `FROM` position: error.
- A Role used but not declared by the Playbook or Plot: error.
- A receiving Role left unfilled by a giving Statement: error, naming the Role and suggesting a `MAPPING`.
- Two `MAPPING`s to one receiving Role in one Statement, or a `MAPPING` to a Role the receiver doesn't declare: error.
- `MAPPING ?who TO …`: error.
- A count or fraction outside an `ASSIGN` target or a `MAPPING`'s giver side: error.
- A Playbook Statement that directs another Agent (`Role DO …`, `ASSIGN`, …): error. Director Statements are only for Directors (glossary).

## Reserved words

`ROLE` (already a Plot keyword), `MAPPING`, `OF`, `PERCENT`.

## Not in 2.0

- **Filling a Role with one Agent** (`MAPPING ?challenger TO opponent`): what a Director can do with a Placeholder is *Director capabilities*' question.
- **One Role filled by several giving Roles** (`Host` and `Guest` both as `noble`).
- **A separate pick per receiving Agent** (`ASSIGN Chatting TO EACH Guest, MAPPING 1 OF Host TO partner`).
- **Counted recipients** (`TELL 2 OF Guest …`).
- **Testing whether an Agent plays a Role** (`GIVEN ?x PLAYS host`).

## ASL mapping notes

For *The full ASL mapping* to pick up:

- Each Agent needs, per giving it holds, the Playbook, the giving Director (and Staging), and each Playbook Role's binding: either a Plot Role in that Staging (resolved live against the infrastructure's record of who plays it) or a fixed set of Agents (a counted pick, from which leavers are removed).
- `TELL host f` expands to a send to every Agent in the union of the Agent's bindings for `host`, minus itself. `FROM host` in a Trigger becomes a Context test on the Sender against the same union, at arrival time.
- A counted pick runs in the Director: it reads the Role's current Agents, shuffles, takes the count, and removes them from the Statement's pool for that Role. The chosen set is sent along with the giving.
- 1.0's `signal_directors` already keeps "which Director gave this Playbook"; bindings extend that record.

## Not decided here

- How Subplots run once started, parent and child cooperation, and how Stagings of one Plot are told apart: *Subplots and Stagings*.
- What a Director can do with `?who`, and whether a Role can be filled with one Agent: *Director capabilities*.
- What happens to bindings and picks when Agents join or leave mid-Plot, beyond "a pick never grows": *Cast changes mid-Plot*.
- Starting state for a Role: *Role setup*.
