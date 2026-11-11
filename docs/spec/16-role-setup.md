# Role setup

What every Agent receives when it starts playing a Plot's Role: Playbooks, Facts and Goals, written once next to the Role. Decided in the ticket *Role setup* (`.scratch/regia-2/issues/17-role-setup.md`). It builds on chapters 05, 07, 08, 11, 13 and 15, and answers the "role instantiation" note in primer ch.5.

## The `STARTS WITH` Block

A Plot's Role may carry a Block saying what each of its Agents starts with:

```regia
PLOT RoyalBanquet:
    ROLE Host.
    ROLE Guest STARTS WITH:
        ASSIGN NobleSocializing, MAPPING Host TO host.
        LEARN invited.
        PURSUE find_seat.
    PHASE reception INITIAL.
    ...
```

- The header is `ROLE <name> STARTS WITH:`. It is the only way to give a Role a Block: `ROLE Guest:` with a Block is an error. `ROLE Guest.` with no setup stays as before.
- Only a **Plot's** Roles have a setup. A Playbook's Roles are addresses only (chapter 15); `STARTS WITH` on them is an error.
- The Block holds three kinds of Statement, in any number and any order:

| Statement | Gives the Agent |
|---|---|
| `ASSIGN <Playbook>[, MAPPING …]` | a Giving of the Playbook, with no `TO`: the target is the Agent starting the Role |
| `LEARN <fact>` | the Fact |
| `PURSUE <goal>` | the Goal, without waiting |

- Nothing else is allowed: no Context, no `IF`, no `EITHER`, no other Actions or Director Statements.
- Arguments are Values or Expressions (chapter 04), `RANDOM` included. There are no Placeholders: nothing is matched, so nothing can fill them.
- The setup is **the same for every Agent of the Role**. Values that differ per Agent (this Guest's gold, Trait values, chapter 14) come from Instancing.

## What it means

A setup is **sugar**. Everything in it could be written in the initial Phase's entry Plan, giving to the Role and telling it Facts and Goals. It adds no new kind of behaviour, only a place to write it and one rule a Plan can't easily follow: it applies to **each Agent when that Agent starts playing the Role**.

- **At Staging start**, every Role's setup runs for the starting cast, in Role declaration order, **before** the initial Phase's entry Plans.
- **When an Agent joins** a running Staging in the Role, the setup runs again for that Agent only, before the Role's standing Givings reach it and before the Director's `JOINED` Triggers (chapter 19). In 2.0 only an Agent entering the Program joins, and only the Root Plot.
- **Per Staging.** An Agent playing `Guest` in two Stagings of RoyalBanquet receives the setup twice, once from each. The two Givings of NobleSocializing add up (chapter 15); the Facts and Goals simply arrive twice.

### Sender

The setup speaks for the Director. A setup Fact arrives **told by the Director**, a setup Goal **asked by the Director**:

- `WHEN invited LEARNED FROM DIRECTOR:` fires, only if the Fact is new (chapter 07). A Plan with no `FROM` fires as usual.
- `TO find_seat FROM DIRECTOR:` matches the setup Goal.
- `LEARN` and `PURSUE` are borrowed for their readability ("a Guest starts by learning `invited`"). Inside a setup they don't mean the Agent's own Actions (chapter 08); they mean the Director's telling and asking. A Director's own Plans write the same thing as `TELL` and `ASK` (chapter 20).

### Order and trouble

- The Statements run **in the order written**, like a Body. Writing the `ASSIGN` first is the usual style: a `PURSUE` above the `ASSIGN` that gives its recipe may find no Plan (chapter 11, a Goal with no applicable Plan fails).
- `PURSUE` never waits: it is `PURSUE …, WITHOUT WAITING` (chapter 08) with nothing written. Writing `, WITHOUT WAITING` is allowed and changes nothing.
- A setup has no Plan to fail. A Statement that can't be carried out (a non-Number in arithmetic, chapter 04) is **skipped** with a Trace entry (chapter 11), and the rest still run.

## Mappings

A setup's `ASSIGN` takes `MAPPING` clauses exactly like a Director's (chapter 15): same names bind without writing them, an unfilled Playbook Role is a compile-time error, the giver's side is a Role of this Plot, and a whole-Role Mapping is live.

**Counted picks are an error in a setup.** `MAPPING 1 OF Host TO confidant` would mean one pick shared by the whole starting cast, and then a fresh pick for each Agent who joins: two behaviours for one line. A target count (`n OF`) has no meaning, since there is no `TO`. A pick per Agent belongs with the `EACH` form, not in 2.0 (chapter 15, *Not in 2.0*).

## When the Agent stops playing the Role

The setup is undone only where the things it gave are undone anyway:

| Given | When the Agent stops playing the Role, or the Staging ends |
|---|---|
| Playbook | The Giving is the Staging's like any other, and is taken away with the Agent's other Givings from it: running Plans stop, local Goals are dropped (chapters 10, 12). |
| Fact | Stays. Once told, it is the Agent's own, with no source (chapter 07). A Plan that wants it gone writes `FORGET`. |
| Goal | Nothing extra. If the Plan pursuing it belongs to a Playbook being taken away, that Plan stops as above. |

- **`UNASSIGN` reaches it.** `UNASSIGN NobleSocializing FROM Guest` in a Phase takes away the setup's Giving like an `ASSIGN`'s.
- **Precedence** treats a setup Playbook as a Playbook this Plot gives out (chapter 13): it is named in `PRECEDENCE:` by its Playbook name, and unordered ones fall back to name order with a warning.

## Transpiler checks

- A Role Block without `STARTS WITH`, or `STARTS WITH` on a Playbook's Role: error.
- A Statement other than `ASSIGN`, `LEARN`, `PURSUE` in a setup: error.
- `TO` on a setup `ASSIGN`, a counted target, or a counted `MAPPING`: error.
- A Placeholder in a setup: error.
- An unfilled Playbook Role, or another Mapping error from chapter 15: error.
- A `PURSUE` above the `ASSIGN` that gives the only Playbook with a Plan for it: warning.

## Reserved words

`STARTS`, `WITH`. Neither clashes with other uses: `START SUBPLOT` is a different word, and a later `WITH` in precedence (the fog item on running behaviours together) would sit in the `PRECEDENCE:` Block.

## ASL mapping notes

For *The full ASL mapping* to pick up:

- The Director runs each Role's setup when it starts the Staging, for each cast Agent, before posting the initial Phase's entry event; and again for each Agent joining the Role.
- A setup `ASSIGN` is the same `regia_give` message (chapter 29) the Director sends for a Phase `ASSIGN`, with the bindings attached; `LEARN` and `PURSUE` are `tell` and `achieve` sent by the Director, so the Agent's `[source(Director)]` makes `FROM DIRECTOR` match.
- A skipped Statement writes a Trace entry and moves on, inside the Director's setup code.

## Not decided here

- A Director tells Facts and asks Goals in its own Plans with `TELL` and `ASK` (chapter 20).
- A counted pick per joining Agent in a setup (`EACH`): with *Richer Mappings and Role tests*.
