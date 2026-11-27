# A Plot takes arguments, and they tell its Stagings apart

Chapter 17 gave a Plot no parameters and kept "picking out one of several running Stagings" for later. We now let a Plot declare parameters (`PLOT HonorDuel(quarrel):`), passed by `START SUBPLOT` and read in every Block of the Plot as filled Placeholders. A parent matches them as it matches a Goal's arguments: `WHEN HonorDuel(?q) ENDED` says which duel ended, and `END SUBPLOT HonorDuel(?q)` ends only the duels that match. Stagings still have no names (spec 17).

An Agent may also play in two running Stagings of the same Plot. Ada fighting two duels at once is a choice for whoever designs the game, not something the language should prevent.

## Considered Options

- **Name Stagings** (`START SUBPLOT HonorDuel AS ?d`, then `END SUBPLOT ?d`): it gives an identity, but a Staging becomes a Value that can be stored, told and outlive its Staging. Arguments give the parent what it needs from Values it already has.
- **Leave out an Agent already cast in a running Staging of the same Plot**, with a Trace warning: each duel stays correct, but the language forbids a story the designer may want, and a whole-Role Mapping silently casts fewer Agents than it names.
- **No arguments**, with the old workaround: what differs between two Stagings comes in through the Cast or through Facts the Agents already hold. That workaround is what led to cause D13.

## Consequences

- The Root Plot takes no parameters (`R21_14-root-plot-with-parameters`). A Plot with parameters is always written with them, except in `PRECEDENCE`, which ranks the Plot and not a Staging.
- Two Stagings with the same arguments can't be told apart, and a Statement that matches one matches both.
- The parameters are the one part of a Plot's Interface that is declared (ADR 0015 infers the rest).
- An Agent in two Stagings of one Plot runs one set of Plans for a Playbook it holds twice. Its Signals reach both Directors and its Playbook Roles reach both bindings, because a Plan doesn't know which Giving it runs for. Giving identity inside the Agent is deferred. The Trace marks the Staging start (`ALSO IN`), and it is not a warning.
- Being cast in a Subplot still adds and never takes away. Arguments let a parent hand the duellists back what it took from them, in the `ENDED` Plan (ADR 0029).
