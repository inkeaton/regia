# Subplots and Stagings

How a Plot starts another Plot as its Subplot, how the Subplot's Roles are cast, how parent and child end and hear about each other, and how several Stagings of one Plot live side by side. Decided in the ticket *Subplots and Stagings* (`.scratch/regia-2/issues/18-subplots-and-stagings.md`). It builds on chapters 05, 07, 08, 11, 13, 15 and 16, and answers the "how should parents and children cooperate" and "alert parent and children plots" notes in primer ch.5.

## Starting a Subplot

```regia
PLOT RoyalBanquet:
    ROLE Host.
    ROLE Guest.
    PHASE reception INITIAL.
    PHASE duel_interruption.
    ...
    DURING duel_interruption:
        WHEN insult_heard:
            START SUBPLOT HonorDuel, MAPPING 1 OF Guest TO Challenger, MAPPING 1 OF Guest TO Defender, MAPPING Guest TO Spectator.
```

- `START SUBPLOT <Plot>` followed by `MAPPING` clauses, with the form, implicit same-name Mappings, errors and counted picks of chapter 15.
- **It never waits.** The parent's Body carries on at once, like `ASK` (chapter 08). The Subplot starts in its own time: it casts its Roles, runs their Role setups (chapter 16), then the initial Phase's entry Plans. The parent learns how it went only through `WHEN … ENDED` (below).
- **Every `START SUBPLOT` makes a new Staging**, even if a Staging of the same Plot started by this parent is still running. Two insults, two duels.
- A Plot has no parameters in 2.0. What a Subplot needs to know reaches it through Facts its Agents already hold, or through its Role setups' Values.

### Casting

A Subplot's Roles are **played**, unlike a Playbook's Roles, which are only addresses (chapter 15). Its Agents get Role setups and Givings and are reached by its Director's Statements. So a Subplot's Roles are **cast when it starts**:

- A whole-Role Mapping (`MAPPING Guest TO Spectator`) casts everyone playing the parent's `Guest` in the parent's Staging **when `START SUBPLOT` runs**. An Agent who starts playing `Guest` later does not become a Spectator.
- A counted pick (`1 OF Guest`) works as in chapter 15: once, at random, no Agent twice in one Statement.
- Role setups run for this cast, per chapter 16.
- Agents joining the parent's Role **don't** carry through to a running Subplot. An Agent leaving the Program leaves every Staging, the Subplot's included, and its Director hears `LEFT`/`EMPTIED` (chapter 19).

### Being in both

An Agent cast into a Subplot **keeps** its Roles and Givings in the parent. It now plays Roles in two Stagings.

- A `SIGNAL` in a Playbook the Subplot gave reaches the Subplot's Director, since it is the one giving that Playbook (chapter 07). A Signal in a Playbook the parent gave reaches the parent's Director, as before.
- In the parent, `FROM Guest` still means the parent's own `Guest` in its own Staging. A parent never sees its Subplots' Roles.

## Stagings

A **Staging** is one running copy of a Plot (glossary). Stagings are **anonymous in the language**: nothing in Regia names one. Each Staging knows its parent (if it is a Subplot) and the Subplots it started. Everything a Director writes is about its own Staging: its Roles, its Phase, its Givings, its Subplots.

- Telling Stagings apart at runtime belongs to the Target. In Jason, a Staging is identified by its Director agent's name (chapter 31).
- Picking out **one** of several running Stagings of the same Subplot is not in 2.0.

## A Subplot outlives its Phase

A Subplot belongs to the parent's **Staging**, not to the Phase that started it. When RoyalBanquet moves from `duel_interruption` to `feast`, HonorDuel keeps running. It stops only when it ends itself, when the parent ends it with `END SUBPLOT`, or when the parent ends.

## Ending

### `END PLOT`

`END PLOT.` ends the Staging it runs in.

- **It stops its Body.** A Statement after it in the same branch is an unreachable-code error.
- **Its Subplots end too**, all the way down, children before parents. Each ending Staging's Givings are taken away (chapter 16's table: running Plans stop, local Goals are dropped, Facts stay).
- **It tells the parent**, if the Staging is a Subplot: the parent's `WHEN <Plot> ENDED` fires. A Subplot ended because its parent is ending tells nobody: the parent is going too.

### Outcomes: `END PLOT WITH`

A Subplot can end with an **Outcome**, one Event handed to the parent:

```regia
PLOT HonorDuel:
    ROLE Challenger.
    ROLE Defender.
    ...
    DURING fighting:
        WHEN yielded FROM Defender:
            END PLOT WITH duel_settled(?winner).   # ?winner filled earlier in the Plan
```

- `END PLOT WITH <event>` takes exactly one Event declared in the Vocabulary. Different endings use different Events (`duel_settled`, `duel_abandoned`).
- Its arguments must be filled: Values or filled Placeholders, as for any Action (chapter 08). An Agent is allowed (`?winner`); the parent's Director can send it Messages, give it Playbooks and map it onto Roles (chapter 20).
- The child declares no list of its endings. The Transpiler warns when a parent matches an Outcome the child never ends with.
- A plain `END PLOT.` ends with no Outcome. In a Plot that isn't a Subplot, `WITH` has no one to tell and is ignored with a warning.

### The parent's Trigger: `WHEN <Plot> ENDED`

```regia
DURING duel_interruption:
    WHEN HonorDuel ENDED WITH duel_settled(?w):
        TRANSITION TO feast.
    WHEN HonorDuel ENDED:
        END PLOT.
```

- `WHEN <Plot> ENDED:` is a Trigger kind for Directors, past tense like `LEARNED`, `FORGOTTEN`, `DROPPED`, `FAILED` (chapter 05). A name has one kind in the Program (ADR 0006), so no `SUBPLOT` word is needed.
- `, WITH <event>` after `ENDED` matches an Outcome, filling Placeholders as any Trigger does (chapter 03).
- **One Trigger, first match wins.** All `WHEN HonorDuel ENDED` blocks of one Phase (or of `DURING PLOT`) share a Trigger and are tried in written order, the first that matches runs, like several `GIVEN`s (chapter 06). A plain `ENDED` matches every ending; written above a `WITH` block, it shadows it, with a warning. A bare `END PLOT` matches only the plain form.
- It fires **once per Staging** that ends.
- It is heard like any Director Trigger: the current Phase's Plan, else the `DURING PLOT` Plan, with the precedence of chapter 13; with neither, the ending is ignored (an unhandled Event, chapter 11).
- `WHEN <Plot> ENDED` in a Plot that never starts that Plot is a compile-time error.

### `END SUBPLOT`

```regia
DURING PLOT:
    WHEN guards_arrived:
        END SUBPLOT HonorDuel.
```

- `END SUBPLOT <Plot>.` ends **every** running Staging of that Plot started by this Staging, each with its own Subplots (as for `END PLOT`).
- The parent's `WHEN HonorDuel ENDED` does **not** fire: the parent did it on purpose.
- It doesn't stop the Body.
- With no such Staging running, it does nothing, without a warning, like the other no-ops (chapter 08).
- Naming a Plot this Plot never starts is a compile-time error.

## Precedence

Spec 13 ranks a Subplot by its position under its parent. Nothing new is needed:

- Two Stagings of one Subplot under the same parent share that position and tie. They are one Plot with one set of Playbooks.
- A Plot started from two different parents has a position under each. An Agent holding Givings from both keeps the better rank, as spec 13 says of a Playbook given twice.
- The rank key's encoding stays with *The full ASL mapping*.

## No cycles

A Plot may not start itself, directly or through other Plots (A starts B starts A). A cycle in the graph of `START SUBPLOT` Statements is a **compile-time error**: the Plot's Playbooks would rank both above and below themselves (chapter 13). Recursion may be allowed later; it is easier to add than to take away.

## Transpiler checks

- `START SUBPLOT` Mappings: chapter 15's checks.
- A cycle among `START SUBPLOT` Statements: error, naming the cycle.
- A Statement after `END PLOT` in the same branch: error.
- `END PLOT WITH` something other than one declared Event, or with unfilled arguments: error.
- `END PLOT WITH` in a Plot never started as a Subplot: warning, `WITH` ignored.
- `WHEN P ENDED` or `END SUBPLOT P` where this Plot never starts `P`: error.
- `WHEN P ENDED WITH e` where `P` never ends with `e`: warning.
- A plain `WHEN P ENDED` above a `WITH` block for the same Trigger: warning (shadowed).

## Reserved words

`SUBPLOT` (already in `START SUBPLOT`), `END`, `ENDED`, `WITH` (shared with `STARTS WITH`, chapter 16). `ENDS` from the primer is not a word of the language.

## ASL mapping notes

For *The full ASL mapping* to pick up (for Jason, decided in chapter 31, `31-jason-stagings.md`: one Director agent per Staging, whose name is the Staging's identity):

- Each Staging needs a runtime identity (for example, a Director agent per Staging, with its parent's name as a belief). Givings, Signals and rank keys carry it.
- `START SUBPLOT` creates the child's Director (or a Staging inside an existing one), passes the cast (resolved whole Roles and counted picks), and returns at once.
- `END PLOT` walks the Subplot tree children first, takes away each Staging's Givings, then sends the parent an `ended(Plot, Outcome)` message unless the parent is ending too. `END SUBPLOT` does the same walk without the message.
- The start-graph cycle check is a whole-Program pass over `START SUBPLOT` Statements.

## Not decided here

- An Agent from an Outcome (`?w`) can be a recipient, an `ASSIGN` target or a `MAPPING`; `TRANSITION` ends its Body like `END PLOT` (chapter 20).
- Plot parameters, a mid-run channel from child to parent (`SIGNAL PARENT e`), naming or ending one particular Staging, and recursive Subplots: *Richer Subplots* in the fog.
