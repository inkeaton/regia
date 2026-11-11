# Choose the example world

Type: grilling
Status: closed
Assignee: Edoardo Vassallo

## Question

Which single world do all the guide's examples and the showcase Program come from? Decide:
- The scenario: the 1.0 royal banquet extended, or a new one.
- Its Roles, Plots (Root Plot plus at least one Subplot that can have several Stagings at once), Playbooks and Agent kinds, as a one-page outline.
- A coverage table showing where each newer system has a natural place: Placeholders and Expressions, Goals and Trigger kinds, `GIVEN` versus `IF`, Match / Pick / `FOR EACH`, Random choice, Failure, Precedence, Suits and Shifts Labels, Playbook Roles and Mappings, Role setup, Subplots, Quota Triggers, Joining and Leaving, Instancing, Custom Actions with and without waiting.
- Which interactions between systems the world should force (for example a Pick inside a Quota-triggered Plan in a Subplot).

The outline is recorded in `docs/guide/showcase/README.md`.

## Resolution

Settled by grilling on 2026-11-11. The outline is in [`docs/guide/showcase/README.md`](../../../docs/guide/showcase/README.md); the decisions behind it:

- **Scenario**: the 1.0 royal banquet, extended. The spec's examples already use it, so snippets check against the spec side by side and *Since 1.0* notes show the same scene before and after.
- **Shape**: one evening with a beginning and an end, not a sandbox. Joining, Leaving and several duels at once sit inside the arc.
- **The game**: a concrete imagined 3D hall, where Actions take time and can be refused.
- **Root Plot**: `RoyalBanquet` itself, with no wider Plot above it, because a joiner only enters the Root Plot. Recorded as the first `#revise`.
- **Root Roles**: `Host`, `Guest`, `Servant`, `Guard`. Kinds: `king`, `noble`, `hothead`, `knight` (Guest and Guard), `servant`, `latecomer` (no `COUNT`).
- **Subplots**: exactly two. `HonorDuel` (several Stagings, Outcomes, Phases `challenge` and `fighting`) and `Poisoning` (one Staging, no Phases).
- **Phases**: `arrival` → `reception` → `feast` → `farewell`, plus `DURING PLOT`.
- **Playbooks**: `Courtesy`, `NobleSocializing`, `Dining`, `Serving`, `Keeping_watch`, `Duelling`, `Scheming`.
- **Coverage table and six forced interactions**: as written in the README.
- **Builds**: a full `banquet.regin` and a small `test.regin` that imports and overrides it; the walkthrough follows the small cast.
- No glossary change and no ADR.

Exact syntax is left to *Write the showcase Program* (02).
