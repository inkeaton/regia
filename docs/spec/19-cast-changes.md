# Cast changes

How the Cast of a running Staging changes when Agents join or leave the Program: a new guest arrives mid-feast, the host is killed and removed from the game. Decided in the ticket *Cast changes mid-Plot* (`.scratch/regia-2/issues/20-cast-changes.md`). It builds on chapters 07, 13, 15, 16, 17 and 18, and answers the cast-changes question (Q4f) of the charting session.

## Who changes the Cast

The **Cast** of a Staging is the Agents playing its Roles (glossary). In 2.0, only the **game** changes it, by adding Agents to the Program or removing them:

- **Joining**: an Agent enters the Program while it runs (the game spawns it). It joins the **Root Plot's** Staging in the Roles its Agent kind plays (an Agent declaration, chapter 21), exactly as a starting Agent is cast. The game reports the kind and a name for the new Agent.
- **Leaving**: an Agent leaves the Program (the game removes it). It stops playing **every Role in every Staging** at once.

Nothing else changes a Cast in 2.0:

- A Director can't move an Agent into or out of a Role of a running Staging. Recasting (`CAST ?who AS Host`) is with *Richer Mappings and Role tests*.
- A Subplot's Cast is fixed when it starts (chapter 17), apart from Agents leaving the Program.
- A "dead" NPC that is still in the world has not left. Being dead is the game's business, told to Regia as a Fact or Event. Only removal from the Program is leaving.

## Joining

### Standing Givings

A Giving whose target is a **whole Role** is **standing**: it gives the Playbook to every Agent playing the Role, including Agents who join later, until it is taken away.

```regia
DURING feast:
    WHEN ENTERED:
        ASSIGN NobleSocializing TO Guest, MAPPING Host TO host.
```

A Guest who arrives mid-feast gets `NobleSocializing` with the same Mapping as every other Guest, so a latecomer behaves like the rest.

- `UNASSIGN NobleSocializing FROM Guest` takes the standing Giving away from everyone holding it, and later joiners no longer get it.
- A Giving to a **counted target** (`ASSIGN Brawling TO 2 OF Guest`) is **not** standing. It is a fixed set, like every pick (chapter 15): a joiner never gets it.
- A standing Giving keeps its own Mappings. A whole-Role Mapping in it is live anyway (chapter 15). A counted pick in it (`MAPPING 1 OF Host TO confidant`) was made once, when the `ASSIGN` ran, and the joiner shares that pick.
- **Messages are not replayed.** Facts told and Goals asked earlier (`TELL Guest …`, `ASK Guest TO …`) were Messages and reached only the Agents playing the Role when they were sent. Starting state for every Agent of a Role belongs in its Role setup (chapter 16).

### Order

When an Agent joins a Staging:

1. Its **Role setup** runs for each Role it joins, in Role declaration order (chapter 16).
2. The **standing Givings** of those Roles reach it, in the order they were made.
3. The Director's **`JOINED`** Triggers fire, one per Role it joins, in Role declaration order (below).

This mirrors Staging start, where Role setups run before the initial Phase's entry Plans.

### Subplots

A joiner joins only the Root Plot. It **never** joins a Subplot that is already running, even one whose Role was cast with a whole-Role Mapping from a Role the joiner now plays. The Subplot's Cast was fixed when it started (chapter 17). A Subplot started **after** the Agent joined casts it like any other Agent.

## Leaving

When an Agent leaves the Program:

- **Its Roles and Givings vanish in every Staging.** Its Plans stop with it. Nothing is undone in other Agents.
- **Live bindings stop reaching it** without anything extra: a whole-Role Mapping or recipient is checked when used (chapters 07, 15).
- **It drops out of every counted pick**, which is not refilled (chapter 15).
- **A Message sent to it is dropped.** A `TELL` or `ASK` whose recipient is a Placeholder holding an Agent that has left does not fail the sender's Plan. It leaves a trace entry (chapter 11), since it is likely a mistake worth finding. Sending never waits for the receiver (chapter 07), so a sender can't tell anyway.
- An Outcome or Placeholder still **holding** the Agent (`END PLOT WITH duel_settled(?w)`) is just a Value. Using it as a recipient is the case above.

### Quota Triggers

Quota Triggers (chapter 18) count only **current** players of the Role:

- An Agent that **leaves** after it was counted stops counting. Its Signal is removed from every count.
- The quota is **checked again when someone leaves**, against the smaller Role. A non-sender leaving can complete an `ALL` or a `PERCENT` without any new Signal, and the Trigger then fires as usual.
- An Agent that **joins** raises the denominator of `ALL` and `PERCENT`: an `ALL` that was one Signal short now also waits for the joiner. Joining can never complete a quota, so it doesn't trigger a check.
- `n OF` doesn't depend on the Role's size. A leaver who was counted lowers its count.

## The Director hears about it

Directors get three Trigger kinds about their own Roles in their own Staging:

```regia
DURING PLOT:
    WHEN Guest ?g JOINED:
        TELL Host guest_arrived(?g).

    WHEN Host LEFT:
        TELL Guest host_gone.

    WHEN Host EMPTIED:
        END PLOT WITH host_gone.
```

| Written | Fires when |
|---|---|
| `WHEN Guest JOINED:` / `WHEN Guest ?who JOINED:` | an Agent joins `Guest` in this Staging |
| `WHEN Guest LEFT:` / `WHEN Guest ?who LEFT:` | an Agent playing `Guest` in this Staging leaves |
| `WHEN Guest EMPTIED:` | the last Agent playing `Guest` in this Staging leaves |

- The Role comes first and the Placeholder after it, as in `FROM Guest ?who` (chapter 05). `?who` follows chapter 03. Besides Messages, a Director can give it a Playbook or map it onto a Role (chapter 20).
- `EMPTIED` takes no Placeholder. It exists because no condition can count a Role's Agents in 2.0 (`COUNT` counts only the Director's own Facts, chapter 26), so after a `LEFT` a Director can't tell whether anyone is left.
- They are **Director Trigger kinds only**. A Playbook doesn't know Plot Roles, and its own Roles are addresses (chapter 15). In a Playbook they are an error.
- They are **not** heard for a Staging's starting Cast. Starting is not joining: the starting Cast gets its Role setups and the initial Phase's entry Plans (chapter 16).
- They follow chapter 13 like any Trigger: blocks in a Phase and in `DURING PLOT` compete, with the Phase winning by default.

### Order when leaving

When an Agent leaves a Staging:

1. Every Quota Trigger of the Staging is checked again (above), and those that are now met fire.
2. For each Role the Agent played there, in Role declaration order: `LEFT` fires, then `EMPTIED` if that Role is now empty.

An Agent playing both `Host` and `Guest` fires `WHEN Host LEFT`, `WHEN Host EMPTIED` (if it was the only Host), then `WHEN Guest LEFT`, and so on.

### An empty Role

Nothing happens on its own when a Role empties:

- The Staging doesn't end. Ending is the Director's call, usually in `WHEN … EMPTIED`.
- Statements aimed at the empty Role send nothing and give to nobody, as with any empty recipient (chapter 07). Standing Givings stay and reach the next joiner.
- `ALL` of an empty Role never fires (chapter 18).

## Transpiler checks

- `JOINED`, `LEFT` or `EMPTIED` in a Playbook: error.
- `JOINED`, `LEFT` or `EMPTIED` after something that isn't a Role of this Plot: error.
- `?who` after `EMPTIED`: error.
- A quantity on them (`WHEN ALL Guest LEFT`): error.

## Reserved words

`JOINED`, `LEFT`, `EMPTIED`.

## ASL mapping notes

For *The full ASL mapping* to pick up:

- The game reports joining and leaving to the infrastructure. Joining reaches the Root Plot's Director with the Agent's Roles from Instancing. Leaving reaches every Director whose Staging the Agent plays in.
- Each Director keeps a record of its standing Givings, in order, next to its Role records, and replays them for a joiner after running its Role setups.
- On leaving, a Director removes the Agent from its Role records and counted picks, removes it from its Quota counts (`quota_seen`, chapter 18) and checks them again, then posts the internal `LEFT`/`EMPTIED` events. Agents holding a counted pick that included the leaver remove it from their per-Giving record.
- A `.send` to an Agent that no longer exists must be caught and turned into a trace entry, not a failure.

## Not decided here

- A Director moving Agents between Roles of a running Staging (`CAST`, `UNCAST`): *Richer Mappings and Role tests*.
- Joiners carrying through to running Subplots: not in 2.0 (cast fixed at start).
- `?who` from `JOINED` can be given a Playbook or mapped onto a Role; from `LEFT` it is only a dropped recipient (chapter 20).
