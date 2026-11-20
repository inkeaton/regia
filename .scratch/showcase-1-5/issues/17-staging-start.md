# What a Staging runs when it starts

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05, 15

## Question

Group H of the [inventory](../jason-open-questions.md#h-a-stagings-start-what-a-staging-runs-when-it-starts): chapter 30's `!regia_begin` runs Role setups only, from data no belief carries.

Decide:

- the beliefs `!regia_begin` reads: the initial Phase, the Roles in order;
- the `CAST` setup, and the initial Phase's setups, at start;
- `EMPTIED` for a Role that starts empty;
- the setup lines of kinds and individual Agents (`LEARN grudge(percival, 2)`): where they are carried, when they run, and whether `LIKE` passes them on.

Closes when chapters 30, 31 and 36 are edited.

## Comments

- From [*Exclusions, one Agent and a Phase in the Giving record*](15-giving-record.md): `regia_give` now carries `Until` (`staging` or `phase(Ph)`), and a `CAST` Giving has target `role(cast)`. Setups send `Until` `staging` in the Plot's setup and `phase(Ph)` in a Phase's (chapter 30, *Role setups*).

## Resolution

Grilled with the user on 2026-11-18. Carried into chapters 30 (*Starting a Staging*, *Setups*, *Setup lines of kinds and individual Agents*, *An Agent joining*, the state table), 31 (*Starting a Subplot*), 33 (*The Root Director's starting cast*, *Joining*) and 36 (*Setup lines of kinds and individual Agents*), with notes in 16, 21 and 29.

1. **What `!regia_begin` reads.** Every Director file has the initial beliefs `regia_initial_phase(Ph)` (`regia_phase__plot` for a Plot with no Phases) and `regia_roles([…])`, the Roles in declaration order without `CAST`. `regia_begin` stays fixed Infrastructure.
2. **Setups are one generated Goal**, `regia_setup(Scope, Role, A)`, where `Scope` is `plot` or `phase(feast)` and `Role` is `cast` or a Role, with a catch-all no-op. The fixed `!regia_run_setups(Scope)` runs `CAST` and then each Role of `regia_roles`, each Agent through `.setof(regia_plays(…))`. Phase entry reuses it (ticket 18).
3. **`regia_begin`, atomic:** the Phase belief, the cast copy, `regia_run_setups(plot)`, `regia_run_setups(phase(Initial))`, the kind and individual lines (Root only), then posting `regia_role_emptied` for each empty Role (`CAST` last), then posting `regia_entered(plot)` and `regia_entered(phase(Initial))`.
4. **A setup's Givings are not standing**: no `regia_standing`. A Phase setup's are taken by `Until` through `regia_take_phase`. Chapter 16's ASL note is corrected.
5. **`EMPTIED` at start "starts first"**, like the two `ENTERED`s. An entry Plan already begun is stopped by an `EMPTIED` Plan's `END PLOT`. Running `EMPTIED` to completion first was rejected because a `WAIT` would hold up the start.
6. **Kind and individual lines** are generated plans `regia_instance_setup(kind(K) | agent(N), A)` on the Root Director, with `LIKE` resolved at compile time and a catch-all. `percival LIKE knight` has no lines and no grudge. `regia_start_cast` becomes `[agent(A, Source, Roles), …]` in port order. `regia_join` gains `Kind`, and a joiner runs its kind's plan after its setups.
7. **A line's `ASSIGN`** is `regia_give(p, agent(a), …, staging)`, which is not standing and is taken only by `FROM ?who`, `FROM CAST ?who` or the ending.
