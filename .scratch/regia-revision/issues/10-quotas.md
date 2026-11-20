# Quotas

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

What does a Quota Plan know, when does it fire, and what happens when the cast is smaller than the count?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- D8 A Quota counts, and that is all it does
- D9 The size of a Quota is in the Plot and the size of the hall in Instancing
- B5 `PERCENT` rounds up in a Trigger and down in a Mapping
- D1 rows `FROM Guest` / `FROM ALL Guest` and quantity

Decide:

- Who sent the counted Signals, and counting a Signal that carries data.
- Once or every time, and a Quota met while no `GIVEN` holds.
- A Quota that can't be met, `ALL` of an empty Role, firing on a departure.
- One rounding rule, and whether a quantity is an Expression everywhere.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

## Resolution

Resolved on 2026-11-17, with the user.

- **D8** fixed. A Quota Plan reads the Signals counted in its firing with `?x SENT e(args)`, one Match per Signal, from the Agents still counted, and with a named Placeholder only the value that fired. It is an error outside the Plans of a Quota Trigger Block. The anonymous `?` doesn't split the count, so `wagered(?) FROM 3 OF Spectator` counts any stake and `cheered` is no longer needed. Firing every time the count fills is kept: it is meant, and "once" is a Phase change or a Fact. A quota met while no `GIVEN` holds still resets; the Trace records it.
- **D9** fixed in part, kept in part. An `n OF` larger than the Role stays legal: the Plot doesn't know the hall, and the hall can grow. Where the build makes it certain (the Root Plot, a Role the `.regin` caps below n with no joining kind) it is warning `R2115`, and the Trace notes an active count whose Role is too small. `ALL` of an empty Role still never fires, and `EMPTIED`, now heard for a Role that starts empty, is the Plan for it. Firing on a departure is kept, with the Placeholders filled from the completed count and the Trace saying so.
- **B5** fixed. One rule: a share or a count that isn't whole rounds up, in a Quota and in a pick. The Quota quantity is a Number Expression over Values and Plot parameters, worked out at each check; `RANDOM` is an error; a runtime value of 0 or less is a Trace warning and the Quota doesn't fire.
- **D1** row `FROM Guest` / `FROM ALL Guest` kept. `FROM 1 OF Guest` stays legal with no warning: it can be meant, as a second Plan that doesn't compete with the plain one.

Changed:

- Spec:
  - Chapter 18: the quantity as an Expression, rounding, *What the Plan knows* (`SENT`), `?` in a count, firing every time, firing on a departure, the empty Role, an unmeetable `n OF`, the checks, ASL notes.
  - Chapter 15: the *Odd values* table rounds up.
  - Chapter 21: warning `R2115`.
  - New codes: `R1806` (error), `R2115` (warning). `R1804` reworded.
  - Reserved word: `SENT`.
- ADR: 0031 *A Quota Plan reads what it counted, and a share rounds up everywhere*.
- Glossary: *Quota Trigger*.

Handed on:

- To [*The Trace*](17-trace.md) (N12): a quota met with no Plan to run, a firing completed by a departure, a count active while its Role is smaller than its quantity, and a quantity that works out below 1.
- The Jason chapter 33: the counted Signals kept with their arguments for `SENT`, `?` slots left out of the count key, the quantity worked out per check from parameters, and picks rounding up.
- `SENT` and the second job of `?` are open to [*Words that do several jobs*](20-words-and-syntax.md).
- Counted Goal endings have no `SENT` in 2.0.

1.5, from [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md):

- D8, D9, D1 row: later. Quota Triggers are not in 1.5.
- B5: in for picks (they round up in 1.5 too); the Quota half is later.
