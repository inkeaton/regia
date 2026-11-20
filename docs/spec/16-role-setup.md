# Role setup

What every Agent receives when it starts playing a Plot's Role: Playbooks, Facts and Goals, written once next to the Role. Decided in the ticket *Role setup* (`.scratch/regia-2/issues/17-role-setup.md`); the header, the shared gloss of `LEARN` and `PURSUE`, and Plot parameters in a setup were revised in the syntax review's *Setups and `ROLE`* (`.scratch/syntax-review/issues/09-setups-and-roles.md`), with ADR 0046. It builds on chapters 05, 07, 08, 11, 13 and 15, and answers the "role instantiation" note in primer ch.5.

## A Role's Block

A Plot's Role may carry a Block saying what each of its Agents starts with. That Block is the Role's **setup**:

```regia
PLOT RoyalBanquet:
    ROLE Host
    ROLE Guest:
        ASSIGN NobleSocializing, MAPPING Host AS host
        LEARN invited
        PURSUE find_seat
    PHASE reception INITIAL
    ...
```

- The header is `ROLE <name>:`, the Role's declaration with a Block, as an Instancing `KIND` or `AGENT` carries the lines its Agents start with (chapter 21). `ROLE Guest` with no setup stays as before. What the Block means, "each Agent starts with this", is the meaning of a Role's Block, not a keyword.
- The retired spelling `ROLE <name> STARTS WITH:` (and `CAST STARTS WITH:`) is an error with a hint (`R1608`): `WITH` introduces the Cue an ending carries (chapter 01).
- The same Block inside a `DURING <phase>` Block is the Role's setup **for that Phase** (below, *A setup for a Phase*).
- `CAST:` with a Block is the setup of **every Agent of the Staging**, whatever its Roles (below, *A setup for the whole Cast*).
- Only a **Plot's** Roles have a setup. A Playbook's Roles are addresses only (chapter 15); a Block on one is an error.
- The Block holds three kinds of Statement, in any number and any order:

| Statement | Gives the Agent |
|---|---|
| `ASSIGN <Playbook>[, MAPPING …]` | a Giving of the Playbook, with no `TO`: the target is the Agent starting the Role |
| `LEARN <fact>` | the Fact |
| `PURSUE <goal>` | the Goal, without waiting |

- Nothing else is allowed: no Context, no `IF`, no `RANDOMLY`, no other Actions or Director Statements.
- Arguments are Values or Expressions (chapter 04), `RANDOM` included. The only Placeholders are the **Plot's parameters** (chapter 17), which are filled when the Staging starts. Any other Placeholder is an error: nothing is matched, so nothing can fill it. `ME` is an error too (`R0309`, chapter 03): 2.0 keeps the setup's Statements the same for every Agent.
- The setup is **the same Statements for every Agent of the Role**, and its **Expressions are worked out for each Agent**, each time the setup runs for one. A roll is made **once per Agent**: `LEARN purse(RANDOM(5, 20))` gives every Guest its own purse. What differs between kinds of Agent, or between particular Agents, in one cast (starting Propensity values, a seat, a grudge) is written in Instancing, on a `KIND` or an `AGENT`, with the same three Statements (chapter 21).

## What it means

A setup is **sugar**. Everything in it could be written in the initial Phase's entry Plan, giving to the Role and telling it Facts and Goals. It adds no new kind of behaviour, only a place to write it and one rule a Plan can't easily follow: it applies to **each Agent when that Agent starts playing the Role**.

- **At Staging start**, the `CAST` setup runs for the starting cast, then every Role's setup, in Role declaration order. The initial Phase is already current and its Quota counts have started (chapter 18), so an ending or a Signal that comes back at once is counted. Its setups run next, and only then the entry Plans: `DURING PLOT`'s `ENTERED`, then the initial Phase's (chapter 20).
- **When an Agent joins** a running Staging in the Role, the `CAST` setup and then the Role's setup run for that Agent only, then the current Phase's setups in the same order, before the Role's standing Givings reach it and before the Director's `JOINED` Triggers (chapter 19). In 2.0 only an Agent entering the Program joins, and only the Root Plot.
- **Per Staging.** An Agent playing `Guest` in two Stagings of RoyalBanquet receives the setup twice, once from each. The two Givings of NobleSocializing add up (chapter 15); the Facts and Goals simply arrive twice.

### Sender

The setup speaks for the Director. A setup Fact arrives **told by the Director**, a setup Goal **asked by the Director**:

- `WHEN invited LEARNED, FROM DIRECTOR:` fires, only if the Fact is new (chapter 07). A Plan with no `FROM` fires as usual.
- `TO find_seat, FROM DIRECTOR:` matches the setup Goal.
- `LEARN` and `PURSUE` keep the gloss they have in a Body (chapter 08), read from the Agent's side: `LEARN f` is "the Agent comes to know `f`", `PURSUE g` is "the Agent takes on `g`". What differs is the **source**, and it follows from where the line is written: in a Body the Agent itself, in a setup the Director, on an Instancing `KIND` or `AGENT` the Root Plot's Director (chapter 21). A Director's own Plans write the same thing as `TELL` and `ASK` (chapter 20), which name a recipient; a setup has none to name, and on a `KIND` no Director is written at all. The Agent's `TO` recipe still decides what to do with a setup Goal. The words were kept in the ticket *Words that do several jobs, and syntax nobody used* (`.scratch/regia-revision/issues/20-words-and-syntax.md`) and passed chapter 01's one-meaning test in the syntax review.

### Order and trouble

- The Statements run **in the order written**, like a Body. Writing the `ASSIGN` first is the usual style: a `PURSUE` above the `ASSIGN` that gives its recipe may find no Plan (chapter 11, a Goal with no applicable Plan fails).
- `PURSUE` never waits: it is `PURSUE …, WITHOUT WAITING` (chapter 08) with nothing written. Writing `, WITHOUT WAITING` is allowed and changes nothing.
- A setup has no Plan to fail. A Statement that can't be carried out (a non-Number in arithmetic, chapter 04) is **skipped** with a Trace entry (chapter 11), and the rest still run.

## A setup for a Phase

A `DURING <phase>` Block may hold setups too. They say what each Agent of the Role gets **while that Phase lasts**:

```regia
PLOT RoyalBanquet:
    ROLE Guest:
        ASSIGN Courtesy, MAPPING Host AS host
        LEARN invited

    DURING arrival:
        ROLE Guest:
            PURSUE take_seat

    DURING feast:
        ROLE Guest:
            ASSIGN Dining, MAPPING Servant AS waiter
            PURSUE have_dinner
```

- **It runs for every Agent of the Role when the Phase is entered**, and for an Agent who **joins while the Phase is current**. A Guest arriving in `feast` gets `Dining` and is asked to dine. A Guest arriving in `farewell` is not asked to take a seat.
- **Its Givings last as long as the Phase.** They are standing while it lasts and are taken away when it is left, after the Phase's `EXITED` Plan (chapter 20). No `REMOVE` is written.
- **Facts and Goals stay**, as with the Plot's setup: a Fact told is the Agent's own, and a Goal asked goes on unless its recipe is in a Playbook that is taken away (chapter 15).
- Same header, same three Statements, same limits, same Sender as the Plot's setup. The Role is one the Plot declares: the `ROLE` line here declares nothing, it names the Role the setup is for, as `DURING PLOT` names the Plot without declaring it. `ROLE Guest` with no Block inside a `DURING` is an error.
- **One setup per Role per Phase.** In `DURING PLOT` it is an error: a setup for the whole Plot is written on the Role's own `ROLE` line.
- **It runs on every entry**, `ENTER` naming the current Phase included (chapter 20). A Fact the Agent already knows fires no `LEARNED` (chapter 07). A Goal is a new Pursuit (chapter 05).
- **Order.** On entering a Phase its setups run after the Phase has become current and before its `ENTERED` Plan: its `CAST` setup, then its Role setups in Role declaration order. At Staging start the Plot's setups run first, `CAST` and then every Role, then the initial Phase's.
- `REMOVE Dining FROM Guest` reaches a Phase setup's Giving as it reaches the Plot's (below). Agents who join later in this stay in the Phase get the setup's Facts and Goals without that Playbook. The next entry of the Phase gives it again.
- In a Subplot it runs on entry only, since a Subplot's Cast doesn't grow (chapter 19).

A setup is still sugar: a Phase's setup is what its `ENTERED` Plan and a `JOINED` Plan would do with a whole-Role `ASSIGN … UNTIL EXITED` (chapter 15), a `TELL` and an `ASK`. It is the place for what a Role should get **whenever it arrives**. A Message in a Plan reaches the Agents that are there when it is sent (ADR 0022).

## A setup for the whole Cast

What every Agent of the Plot gets, whatever it plays, is written once:

```regia
PLOT RoyalBanquet:
    ROLE Host
    ROLE Guest
    ROLE Servant
    ROLE Guard

    CAST:
        ASSIGN Courtesy             # its `host` is the Plot's Host, by name
        LEARN banquet_tonight

    DURING feast:
        CAST:
            ASSIGN Toasting
```

- It is the setup of the Role `CAST` (chapter 15), written `CAST:` with its Block, since `CAST` is never declared, with the same three Statements, the same limits and the same Sender as a Role's setup.
- **An Agent gets it once per Staging**, not once per Role it plays. A knight who is `Guest` and `Guard` holds one Giving of `Courtesy` from it.
- **It runs before the Role setups**: the Plot's `CAST` setup, the Plot's Role setups in declaration order, then the Phase's `CAST` setup and the Phase's Role setups. The same order holds for a joiner (chapter 19).
- **One per Plot and one per Phase.** At Plot level it is written among the `ROLE` lines; in a `DURING <phase>` Block it lasts the Phase, as a Role's does. In `DURING PLOT` it is an error.
- Its Givings are made to `CAST`: `REMOVE Courtesy FROM CAST` takes them away, and `REMOVE Courtesy FROM Guest` takes `Courtesy` from the Guests only. The setup goes on giving it to everyone else, joiners included, and no longer to a Guest who joins (chapter 15).
- It is sugar like the others: `ASSIGN Courtesy TO CAST` in the entry Plan and a `WHEN CAST ?who JOINED:` Plan for the Facts and Goals.

## Mappings

A setup's `ASSIGN` takes `MAPPING` clauses exactly like a Director's (chapter 15): same names bind without writing them, ignoring case, an unfilled Playbook Role is a compile-time error, the giver's side is a Role of this Plot or `CAST`, with or without `EXCEPT` and its list of Roles, and a whole-Role Mapping is live.

**Counted picks are an error in a setup.** `MAPPING 1 OF Host AS confidant` would mean one pick shared by the whole starting cast, and then a fresh pick for each Agent who joins: two behaviours for one line. A target count (`n OF`) has no meaning, since there is no `TO`. A pick per Agent belongs with the `EACH` form, not in 2.0 (chapter 15, *Not in 2.0*).

## When the Agent stops playing the Role

The setup is undone only where the things it gave are undone anyway:

| Given | When the Agent stops playing the Role, or the Staging ends |
|---|---|
| Playbook | The Giving is the Staging's like any other, and is taken away with the Agent's other Givings from it: running Plans stop, their Goals are dropped, and the Playbook's closing Plans run (chapter 15). A Phase setup's Giving goes earlier, when the Phase is left. |
| Fact | Stays. Once told, it is the Agent's own, with no source (chapter 07). A Plan that wants it gone writes `FORGET`. |
| Goal | Nothing extra. If the Plan pursuing it belongs to a Playbook being taken away, that Plan stops as above. |

- **`REMOVE` reaches it.** `REMOVE NobleSocializing FROM Guest` in a Phase takes away the setup's Giving like an `ASSIGN`'s.
- **Precedence** treats a setup Playbook as a Playbook this Plot gives out (chapter 13): it is named in `PRECEDENCE:` by its Playbook name, and unordered ones fall back to name order with a warning.

## Transpiler checks

**Errors**

- `R1601` A Block on a Playbook's Role.
- `R1602` A Statement other than `ASSIGN`, `LEARN` or `PURSUE` in a setup.
- `R1603` `TO` on a setup `ASSIGN`, a counted target, or a counted `MAPPING`.
- `R1604` A Placeholder in a setup, other than the Plot's parameters.
- `R1606` A setup in `DURING PLOT`, a second setup for one Role (or for `CAST`) in one Phase or at Plot level, or `ROLE <name>` with no Block inside a `DURING`.
- `R1607` A Phase setup for a Role the Plot doesn't declare.
- `R1608` The retired header `ROLE <name> STARTS WITH:` or `CAST STARTS WITH:`. The hint gives `ROLE <name>:` or `CAST:`.

**Warnings**

- `R1605` A `PURSUE` above the `ASSIGN` that gives the only Playbook with a Plan for it.

An unfilled Playbook Role, and the other Mapping errors, are chapter 15's (`R1503`–`R1512`).

## Trace entries

**Warnings**

- `T1601` A setup Statement that can't be carried out, skipped.

## Reserved words

Every keyword is listed in chapter 01, *Reserved words* (`01-statements-and-blocks.md`).

## ASL mapping notes

For *The full ASL mapping* to pick up (for Jason, done in chapter 30):

- The Director runs each Role's setup when it starts the Staging, for each cast Agent, before posting the initial Phase's entry event; and again for each Agent joining the Role. The setup's Expressions are worked out inside that per-Agent step, so each Agent gets its own rolls, from the seeded source (chapter 35).
- A Phase's setups run inside the transition, after the Phase belief changes and before the `ENTERED` event is posted. Their Givings are marked with the Phase, so that leaving it takes them away. They aren't recorded as standing: the setup itself runs again for a joiner. For Jason, chapter 30 (*Starting a Staging*, *Setups*).
- A setup `ASSIGN` is the same `regia_give` message (chapter 29) the Director sends for a Phase `ASSIGN`, with the bindings attached; `LEARN` and `PURSUE` are `tell` and `achieve` sent by the Director, so the Agent's `[source(Director)]` makes `FROM DIRECTOR` match.
- A skipped Statement writes a Trace entry and moves on, inside the Director's setup code.

## Regia 1.5

In 1.5 (ADR 0025), for the starting cast and for Phase entry. What runs **when an Agent joins** is later, with joining (chapter 19), and so are the Quota counts that start with the initial Phase.

A setup is still sugar, without `JOINED`:

- a Role setup, and the `CAST` setup, are what the initial Phase's entry Plan would do for each starting Agent: an `ASSIGN`, a `TELL` and an `ASK`;
- a Phase's setup is what its `ENTERED` Plan would do with a whole-Role `ASSIGN … UNTIL EXITED`, a `TELL` and an `ASK`. It runs again when the Phase is entered again, and that is the only time "standing" matters for it.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- A Director tells Facts and asks Goals in its own Plans with `TELL` and `ASK` (chapter 20).
- A counted pick per joining Agent in a setup (`EACH`): not in 2.0, with a Giving's identity (chapter 15, *Not in 2.0*).
