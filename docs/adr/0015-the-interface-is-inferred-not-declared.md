# The Interface is inferred, not declared

A Playbook declares its Roles and nothing else about what it exchanges: the Goals it answers, the Events it tells and the Signals it sends are found only in its Bodies, and so are a Plot's endings. In the first draft of 2.0 nothing checked one side against the other, and a Signal, an `ASK` or an ending that nobody handled was lost in silence. We keep the source as it is and have the **Transpiler work the Interface out from the whole Program** (spec 38): it checks each Playbook against the Plots that give it and each Subplot against its parents, reports mismatches as warnings, and the tools show the result.

The Transpiler always compiles a whole Program, so every mismatch we wanted caught is between two things already written: a `SIGNAL` and the Plans of the Plot that gives its Playbook, an `ASK` and the `FROM` of a recipe, an `END PLOT WITH` and an `ENDED WITH`. A declaration would state them a third time and need its own checks against the Bodies.

## Considered Options

- **Declared**: a Playbook lists its Signals and the Goals it answers, a Plot lists its Outcomes, and an `EVENT` line says who sends it. This lets a Playbook be checked with no Plot in sight and gives a reader one place to look. It costs new syntax in every Playbook and Plot, and a second source of truth to keep in step with the Bodies. Nothing in the review asked for checking a Playbook alone.
- **Left as it was**: no checks. The showcase's hand-made table of Signals and Outcomes already had two Events under the wrong heading.

## Consequences

- The checks are warnings, not errors (`R38_01-unheard-signal`, `R38_02-cue-never-signalled`, `R38_03-unheard-message`, `R17_08-unheard-subplot-ending`): a Playbook given by two Plots, an Agent in two Roles or a recipe held from another Plot make each of them wrong in some correct Program.
- A Signal handled in some Phases only is not caught at build. The Trace reports a Signal or an ending that finds no Plan (`T38_01-signal-found-no-plan`, `T38_02-ending-found-no-plan`).
- A Playbook can't be checked against a Plot that isn't in the Program. If libraries of Playbooks are ever shipped alone, declarations may come back, and they could then be generated from the inferred Interface.
- The Interface is shown by the tools (the command line and the Visual Editor), since it is nowhere in the source.
