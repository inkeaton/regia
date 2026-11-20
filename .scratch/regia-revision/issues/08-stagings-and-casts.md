# Telling Stagings and Givings apart, and what a Subplot is given

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 06

## Question

Can two Stagings of one Plot, or two Givings of one Playbook, be kept apart, and what does a Subplot get from its parent besides a copied Cast?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- F2 A Giving and a Staging have no identity
- D12 Being cast in a Subplot adds and never takes away
- D13 A Plot takes no arguments
- F9 Only the Root Plot has a living cast

Decide:

- Whether 2.0 gets identity, or forbids or warns about what it can't keep apart (a second Staging with an overlapping Cast, `UNASSIGN … FROM ?who` over a setup's Giving).
- Arguments to a Plot.
- Whether a Subplot can suspend a Playbook of its Cast.
- Live Casts below the Root, and a mark for the Root Plot.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

Blocked by: [What can be said about a Role](06-roles.md).

## Resolution

Resolved on 2026-11-17, with the user.

- **D13, fixed.** `PLOT HonorDuel(quarrel):` takes parameters, passed by `START SUBPLOT HonorDuel(?insult)`. Each is a Placeholder filled in every Block of the Plot, setups included, fixed for the Staging. Arguments must be filled and can't be Roles. One parameter count per Plot (ADR 0006); `PRECEDENCE` names the Plot bare. The Root Plot takes none.
- **F2, fixed as far as the parent goes; identity deferred.**
  - A parent tells its Subplots' Stagings apart by matching their arguments: `WHEN HonorDuel(?q) ENDED`, and `END SUBPLOT HonorDuel(?q)` / `HonorDuel(?)`. Stagings still have no names.
  - An Agent **may** play in two running Stagings of one Plot. The user first accepted leaving it out, then reopened it: Ada in two duels is a game-design matter, not something the language should forbid. Because a Plan doesn't know which Giving it runs for, Signals reach both Directors and Playbook Roles are the union. That is documented as a 2.0 limit, and the Trace marks the Staging start with `ALSO IN`, which is not a warning.
  - An `UNASSIGN` naming one Agent takes what was given the way it names: `FROM ?who` the Givings made to that Agent, `FROM Guest ?who` the Agent out of the Givings to `Guest`, `FROM CAST ?who` everything. `ASSIGN P TO Guest ?who` lifts the exclusion and makes no new Giving. The guard of honour ends without taking guard duty with it.
  - Across Stagings, already the rule and now stated: a Giving belongs to the Staging that made it, and only that Staging takes it away. The Agent knows who gave it what.
  - Deferred: Giving identity inside the Agent, a Staging's name, two Stagings with the same arguments.
- **D12, kept.** Being cast in a Subplot adds and never takes away. The parent takes `Dining` from the duellists with `UNASSIGN … FROM Guest ?a` and gives it back in the `ENDED` Plan with `ASSIGN … TO Guest ?a`, the duellists passed as arguments. Pausing a Playbook while a Subplot runs is deferred: it needs rules for running Plans, Pursuits, Quota counts and closing Plans.
- **F9, kept.** Casts below the Root stay a copy made at start. Living casts are deferred. The Root stays named or inferred in Instancing, since a Plot reads the same either way. Added: chapter 17 sets the copy on `START SUBPLOT` against the live Mapping on `ASSIGN`, and a `JOINED` Plan in a Plot that is never the Root is a warning.

Settled while asking:

- A Role that starts empty fires `EMPTIED` once, after the setups and before the initial Phase's entry Plans, `CAST` last. Before, an empty start was silent and a duel with no Defender waited for its timeout.

Standing preference from the user, added to the map's Notes: the language forbids or warns only about what can't be meant, or what the writer can't avoid. A game-design hazard is the writer's responsibility, and the Trace shows it.

Changed:

- Spec: chapter 17 (*Plot parameters*, *An Agent in two Stagings of one Plot*, arguments on `ENDED` and `END SUBPLOT`, `EMPTIED` on an empty start, *Not in 2.0*), chapter 15 (*Taking a giving from one Agent*, *Giving it back*, a Giving belongs to its Staging), and chapters 03, 19, 20, 21, 34 and 38. New codes: `R1709`, `R1710`, `R1711`, `R1513`, `R1905` (warning), `R2114`, `T1505`, `T1506`.
- ADRs: 0028 *A Plot takes arguments, and they tell its Stagings apart*; 0029 *`UNASSIGN` takes what was given the way it names*.
- Glossary: *Plot*, *Staging* and *Giving* reworded.

Handed on:

- A condition asking whether a Staging of a Plot is running, and with which arguments: [*What a Director knows about itself*](09-director-state-and-endings.md) (N7). A second insult between the same two Guests is guarded with it.
- The pick per receiver (from [*What can be said about a Role*](06-roles.md)) stays deferred with Giving identity.
- The Jason chapters 29, 30 and 31: Plot arguments in `regia_start` and in the `ended` message, matching in `END SUBPLOT`, the three `UNASSIGN … ?who` forms (`regia_take(p, all)` is now only `FROM CAST ?who`), an exclusion list per Agent on a standing Giving and lifting it, `EMPTIED` at start, and `ALSO IN` in the Trace.
- The guide's *Subplots and Stagings*, *Plots and Directors* and *Playbooks and Roles*, and the showcase, still have the argument-less `HonorDuel`, the duellists eating between lunges, and the guard of honour that never ends.
- The `<Role> ?who` shape on `ASSIGN` and `UNASSIGN` is open to [*Words and syntax*](20-words-and-syntax.md).

1.5, from [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md):

- D13 in. F2 in: argument matching, an Agent in two Stagings, the `UNASSIGN`/`ASSIGN` forms for one Agent. D12 in as kept. F9 in as kept; the `R1905` warning is later, since 1.5 has no `JOINED`. Nothing here needs a later part: without joiners, "standing" in the exclusion rules matters only for a Phase setup giving again on re-entry, and the exclusion holds there too.
