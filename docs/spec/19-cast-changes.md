# Cast changes

How the Cast of a running Staging changes when Agents join or leave the Program: a new guest arrives mid-feast, the host is killed and removed from the game. Decided in the ticket *Cast changes mid-Plot* (`.scratch/regia-2/issues/20-cast-changes.md`). It builds on chapters 07, 13, 15, 16, 17 and 18, and answers the cast-changes question (Q4f) of the charting session. That only Directors hear cast changes, and that a Director tidies its own Facts about a leaver, were confirmed in the ticket *Facts that are told, and news in general* (`.scratch/regia-revision/issues/11-told-facts.md`).

## Who changes the Cast

The **Cast** of a Staging is the Agents playing its Roles (glossary). In 2.0, only the **game** changes it, by adding Agents to the Program or removing them:

- **Joining**: an Agent enters the Program while it runs (the game spawns it). It joins the **Root Plot's** Staging in the Roles its Agent kind plays (a `KIND`, chapter 21), exactly as a starting Agent is cast. The game reports the kind and a name for the new Agent. Only a kind joins: an individual Agent (`AGENT`, chapter 21) is in the starting cast and is never spawned.
- **Leaving**: an Agent leaves the Program (the game removes it). It stops playing **every Role in every Staging** at once.

Nothing else changes a Cast in 2.0:

- A Director can't move an Agent into or out of a Role of a running Staging. Recasting is not in 2.0. `CAST` is now the Role of the whole Cast (chapter 15), so the Statement will need another word than the `CAST ?who AS Host` once sketched.
- A Subplot's Cast is fixed when it starts (chapter 17), apart from Agents leaving the Program.
- A "dead" NPC that is still in the world has not left. Being dead is the game's business, told to Regia as a Fact or Cue. Only removal from the Program is leaving.

## Joining

### Standing Givings

A Giving whose target is a **whole Role** is **standing**: it gives the Playbook to every Agent playing the Role, including Agents who join later, until it is taken away.

```regia
DURING feast:
    WHEN ENTERED:
        ASSIGN NobleSocializing TO Guest, MAPPING Host AS host
```

A Guest who arrives mid-feast gets `NobleSocializing` with the same Mapping as every other Guest, so a latecomer behaves like the rest.

- `REMOVE NobleSocializing FROM Guest` takes the standing Giving away from everyone holding it, and later joiners no longer get it. It also takes away this Staging's counted Givings to `Guest`, and takes the Guests out of its Givings to the whole Cast, which go on as `CAST EXCEPT Guest`: a joining Guest doesn't get the Playbook from them (chapter 15).
- `REMOVE NobleSocializing FROM Guest ?who` takes it away from that Agent only. The standing Giving stays, now leaving `?who` out, and later joiners still get it. `ASSIGN NobleSocializing TO Guest ?who` gives it back. `REMOVE … FROM ?who` alone takes only a Giving made to that Agent (chapter 15).
- A Giving to a **counted target** (`ASSIGN Brawling TO 2 OF Guest`) is **not** standing. It is a fixed set, like every pick (chapter 15): a joiner never gets it.
- A standing Giving keeps its own Mappings. A whole-Role Mapping in it is live anyway (chapter 15). A counted pick in it (`MAPPING 1 OF Host AS confidant`) was made once, when the `ASSIGN` ran, and the joiner shares that pick.
- **Messages are not replayed.** Facts told and Goals asked earlier (`TELL Guest …`, `ASK Guest TO …`) were Messages and reached only the Agents playing the Role when they were sent. Starting state for every Agent of a Role belongs in its Role setup, for the whole Plot or for one Phase (chapter 16).
- **A Giving is a state and a Message is something that happened.** That is why a whole-Role `ASSIGN` in a Plan reaches a joiner and an `ASK` next to it doesn't. What a Role should get whenever it arrives is written in a setup (ADR 0022).

### Order

When an Agent joins a Staging:

1. The Plot's **`CAST` setup** runs for it, then its **Role setup** for each Role it joins, in Role declaration order (chapter 16).
2. The **current Phase's setups** run the same way: `CAST`, then each of those Roles. Then its **kind's setup lines** from Instancing (chapter 21).
3. The **standing Givings** of those Roles and of `CAST` reach it, in the order they were made. A standing Giving with `EXCEPT` skips it if it is left out (chapter 15).
4. The Director's **`JOINED`** Triggers fire: `WHEN CAST … JOINED` once, then one per Role it joins, in Role declaration order (below).

This mirrors Staging start, where Role setups run before the initial Phase's entry Plans. Step 3 covers the standing Givings made by Plans, with or without `UNTIL EXITED`; a Phase setup's Givings reached the joiner in step 2.

### Subplots

A joiner joins only the Root Plot. It **never** joins a Subplot that is already running, even one whose Role was cast with a whole-Role Mapping from a Role the joiner now plays. The Subplot's Cast was fixed when it started (chapter 17). A Subplot started **after** the Agent joined casts it like any other Agent.

## Leaving

When an Agent leaves the Program:

- **Its Roles and Givings vanish in every Staging.** Its Plans stop with it. Nothing is undone in other Agents.
- **Live bindings stop reaching it** without anything extra: a whole-Role Mapping or recipient is checked when used (chapters 07, 15).
- **It drops out of every counted pick**, which is not refilled (chapter 15).
- **A Message sent to it is dropped.** A `TELL` or `ASK` whose recipient is a Placeholder holding an Agent that has left does not fail the sender's Plan. It leaves a trace entry (chapter 11), since it is likely a mistake worth finding. Sending never waits for the receiver (chapter 07), so a sender can't tell anyway.
- An Outcome or Placeholder still **holding** the Agent (`END PLOT WITH duel_settled(?w)`) is just a Value. Using it as a recipient is the case above.
- **Facts that name it stay.** A Fact holding the Agent, the Director's or another Agent's, is not forgotten: it may be meant to outlive the leaver (`beaten_by(?who)`). A Director that keeps a record of its Agents tidies it on `LEFT` (below).

```regia
DURING PLOT:
    WHEN Spectator ?who LEFT:
        FOR EACH wager(?who, ?stake):
            FORGET wager(?who, ?stake)
```

Without it, a Pick over `wager` can choose the leaver, and the `ASK` to it is dropped with `T1901`.

### Quota Triggers

Quota Triggers (chapter 18) count only **current** players of the Role:

- An Agent that **leaves** after it was counted stops counting. Its Signal is removed from every count.
- The quota is **checked again when someone leaves**, against the smaller Role. A non-sender leaving can complete an `ALL` or an `n% OF` without any new Signal, and the Trigger then fires as usual.
- An Agent that **joins** raises the denominator of `ALL` and `n% OF`: an `ALL` that was one Signal short now also waits for the joiner. Joining can never complete a quota, so it doesn't trigger a check. A joiner should be asked for what the Quota waits on: a Goal asked in the Phase's setup reaches it, an `ASK` in the `ENTERED` Plan doesn't (chapter 16).
- `n OF` doesn't depend on the Role's size. A leaver who was counted lowers its count.

## The Director hears about it

Directors get three Trigger kinds about their own Roles in their own Staging:

```regia
DURING PLOT:
    WHEN Guest ?g JOINED:
        TELL Host guest_arrived(?g)

    WHEN Host LEFT:
        TELL Guest host_gone

    WHEN Host EMPTIED:
        END PLOT WITH host_gone
```

| Written | Fires when |
|---|---|
| `WHEN Guest JOINED:` / `WHEN Guest ?who JOINED:` | an Agent joins `Guest` in this Staging |
| `WHEN Guest LEFT:` / `WHEN Guest ?who LEFT:` | an Agent playing `Guest` in this Staging leaves |
| `WHEN Guest EMPTIED:` | the last Agent playing `Guest` in this Staging leaves |

- The Role comes first and the Placeholder after it, as in `FROM Guest ?who` (chapter 05). `?who` follows chapter 03. Besides Messages, a Director can give it a Playbook or map it onto a Role (chapter 20).
- `EMPTIED` takes no Placeholder. A condition can count a Role too (`COUNT(? PLAYS Guest)`, chapters 15 and 26); `EMPTIED` is the Trigger for the moment the count reaches nothing.
- The Role may be `CAST`: `WHEN CAST ?who JOINED:` fires once for a joiner whatever its Roles, `WHEN CAST ?who LEFT:` once for a leaver, and `WHEN CAST EMPTIED:` when nobody is left in the Staging.
- They are **Director Trigger kinds only**. A Playbook doesn't know Plot Roles, and can only test its own (`PLAYS`, chapter 15). In a Playbook they are an error.
- `JOINED` and `LEFT` are **not** heard for a Staging's starting Cast. Starting is not joining: the starting Cast gets its Role setups and the initial Phase's entry Plans (chapter 16).
- `EMPTIED` **is** heard for a Role that starts empty, once, after the Role setups and before the initial Phase's entry Plans, in Role declaration order and `CAST` last (chapter 17). A Plan written for "nobody is left" then also covers "nobody came".
- Only the Root Plot has joiners, so `JOINED` in a Plot that is never the Root never fires (`R1905`).
- They follow chapter 13 like any Trigger: blocks in a Phase and in `DURING PLOT` compete, with the Phase winning by default.

### Order when leaving

When an Agent leaves a Staging:

1. Every Quota Trigger of the Staging is checked again (above), and those that are now met fire.
2. For each Role the Agent played there, in Role declaration order: `LEFT` fires, then `EMPTIED` if that Role is now empty. `CAST` comes last: `WHEN CAST … LEFT`, then `WHEN CAST EMPTIED` if the Staging has nobody left.

An Agent playing both `Host` and `Guest` fires `WHEN Host LEFT`, `WHEN Host EMPTIED` (if it was the only Host), then `WHEN Guest LEFT`, and so on.

### An empty Role

Nothing happens on its own when a Role empties:

- The Staging doesn't end. Ending is the Director's call, usually in `WHEN … EMPTIED`.
- Statements aimed at the empty Role send nothing and give to nobody, as with any empty recipient (chapter 07). Standing Givings stay and reach the next joiner.
- `ALL` of an empty Role never fires (chapter 18).

### What the Agents hear

Agents hear nothing of a cast change. Only the Director does, and it passes on what matters, or ends the Staging, which takes its Playbooks away:

```regia
DURING PLOT:
    WHEN Defender EMPTIED:
        END PLOT WITH fled
```

A Challenger left alone stops telling `hit` because `Duelling` is taken from it, not because it noticed. A Director that wants the Staging to go on tells its Agents with a Message (`TELL Challenger opponent_fled`). A Playbook's own Roles are bound per giving, so a Playbook hearing that one of them emptied is not in 2.0.

## Transpiler checks

**Errors**

- `R1901` `JOINED`, `LEFT` or `EMPTIED` in a Playbook.
- `R1902` `JOINED`, `LEFT` or `EMPTIED` after something that isn't a Role of this Plot or `CAST`.
- `R1903` `?who` after `EMPTIED`.
- `R1904` A quantity on them (`WHEN ALL Guest LEFT`).

**Warnings**

- `R1905` `JOINED` in a Plot that is never the Root Plot: it can't fire. Absence check (chapter 23).

## Trace entries

**Warnings**

- `T1901` A `TELL` or `ASK` to an Agent that has left the Program, dropped.
- `T1902` A spawn the game reported in a 1.5 run, refused: joining is Regia 2.0 (*Regia 1.5*, below). Reported by a 1.5 run only; retired in 2.0.

## Reserved words

Every keyword is listed in chapter 01, *Reserved words* (`01-statements-and-blocks.md`).

## ASL mapping notes

For *The full ASL mapping* to pick up (for Jason, the Director's side of joining and the standing record are chapter 30; the rest is chapter 33, `33-jason-cast-changes-and-quotas.md`):

- The game reports joining and leaving to the infrastructure. Joining reaches the Root Plot's Director with the Agent's Roles and its kind's setup lines from Instancing. Leaving reaches every Director whose Staging the Agent plays in.
- Each Director keeps a record of its standing Givings, in order, next to its Role records, and replays them for a joiner after running its Role setups.
- On leaving, a Director removes the Agent from its Role records and counted picks, removes it from its Quota counts (`quota_seen`, chapter 18) and checks them again, then posts the internal `LEFT`/`EMPTIED` events. Agents holding a counted pick that included the leaver remove it from their per-Giving record.
- A `.send` to an Agent that no longer exists must be caught and turned into a trace entry, not a failure.

## Regia 1.5

In 1.5 (ADR 0025): **leaving**, `LEFT` and `EMPTIED`, a leaver's Givings taken away, its picks and bindings dropped, and `T1901`.

**Joining is later.** In 1.5 the game can't spawn an Agent while the run goes on. A spawn is refused: the Agent joins nothing, and the Trace writes `T1902`. Every Agent comes from the starting Instancing, so a Staging's cast is fixed when it starts and only shrinks. Where the text says "later joiners", it doesn't apply.

- `JOINED` is `R0109` in a 1.5 build (chapter 01). `R1901` and `R1902` still cover `LEFT` and `EMPTIED`. `R1905` is never reported.
- What Quota Triggers do on a leave is later, with chapter 18.
- `T1902` is reported by a 1.5 run only, and is retired in 2.0, where the same spawn joins.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- A Director moving Agents between Roles of a running Staging: not in 2.0, and not yet worded.
- A Playbook hearing a cast change of its own Roles (`WHEN opponent EMPTIED:`): after 2.0. In 2.0 the Director passes it on (*What the Agents hear*).
- Joiners carrying through to running Subplots: not in 2.0 (cast fixed at start).
- `?who` from `JOINED` can be given a Playbook or mapped onto a Role; from `LEFT` it is only a dropped recipient (chapter 20).
