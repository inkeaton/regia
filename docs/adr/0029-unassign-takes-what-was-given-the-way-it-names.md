# `UNASSIGN` takes what was given the way it names

`UNASSIGN P FROM ?who` used to take every Giving of `P` the Staging had made that `?who` held, whatever its target. Ending a winner's guard of honour (`ASSIGN Keeping_watch TO ?winner`) then also took away its Guard setup's `Keeping_watch`. We now make an `UNASSIGN` that names one Agent take only the Givings made the way it says (spec 15):

- `FROM ?who`: the Givings made to that Agent.
- `FROM Guest ?who`: the Agent taken out of the Givings to `Guest`, which go on as `Guest EXCEPT ?who`.
- `FROM CAST ?who`: everything this Staging gave it.

`ASSIGN P TO Guest ?who` lifts the exclusion, so the Agent holds the same standing Giving again, with no new Giving made.

Across Stagings nothing changes: a Giving belongs to the Staging that made it, and only that Staging takes it away.

## Considered Options

- **Keep the old meaning**: it is simple, but the guard of honour can't end without taking guard duty with it. Giving a Playbook back with `ASSIGN P TO ?who` also made a Giving to one Agent, which a later `UNASSIGN P FROM Guest` doesn't reach, so the Agent kept `Dining` after the dinner ended.
- **Giving identity** (naming a Giving and taking it away by name): deferred with the rest of Giving identity (ADR 0028).

## Consequences

- The `<Role> ?who` shape already used by `FROM` now also follows `UNASSIGN` and `ASSIGN … TO`.
- An `UNASSIGN` or `ASSIGN` for one Agent that finds nothing does nothing, with a Trace warning (`T1505`, `T1506`). Director Statements never fail.
- Taking a Playbook from the duellists for the length of a duel is written by the parent, before `START SUBPLOT` and in the `ENDED` Plan. Pausing it is deferred.
- Respelled by ADR 0043 (`0043-to-introduces-a-goal-with-two-closed-exceptions.md`): `UNASSIGN` is now `REMOVE`, and `UNASSIGNED` is `REMOVED`. The decision and the `FROM` shapes stand.
