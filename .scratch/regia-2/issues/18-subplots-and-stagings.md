# Subplots and Stagings

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo

## Question

How do Subplots work (primer ch.5)? Decide how Roles are mapped (`START SUBPLOT HonorDuel MAPPING Guest TO Challenger`), including mapping a count or fraction of a Role's Agents. How do parent and child cooperate (the parent reacts to `SUBPLOT … ENDS`; does `END PLOT` end the children; can the child report outcomes or values to the parent)? How are Stagings identified when the same Plot runs several times at once?

## Answer

Spec chapter: `docs/spec/17-subplots.md`. Glossary: *Outcome* added; *Subplot*, *Staging* and *Director Statement* updated. No ADR: each choice is cheap to reverse.

- **Starting:** `START SUBPLOT P, MAPPING …` (spec 15's form) never waits, and every run makes a new Staging. No Plot parameters in 2.0.
- **Casting:** a Subplot's Roles are cast when it starts. A whole-Role Mapping takes everyone playing the parent Role at that moment, counted picks work as in spec 15, and Role setups run for that cast. Agents keep their parent Roles and Givings. Signals go to the Director that gave the Playbook, and a parent never sees its child's Roles.
- **Stagings:** anonymous in the language; each knows its parent and its Subplots. Runtime identity is left to the ASL mapping.
- **Lifetime:** a Subplot belongs to the parent's Staging, not to a Phase, so it survives `TRANSITION`.
- **`END PLOT`:** stops its Body (anything after it in the branch is an error), ends every Subplot below it children first and takes away their Givings, and tells the parent unless the parent is ending too.
- **Outcomes:** `END PLOT WITH <event>` takes one declared Event with filled arguments (an Agent is allowed). The parent writes `WHEN HonorDuel ENDED[, WITH e(?x)]:`, which is one Trigger whose blocks are tried first match in written order. A plain `ENDED` matches any ending and gets a warning when it shadows a `WITH` block. It is heard by the current Phase, else `DURING PLOT`, else ignored, and fires once per Staging.
- **`END SUBPLOT P`:** ends every Staging of P that this Staging started, with no `ENDED`. It doesn't stop the Body, and it is a silent no-op when none is running.
- **Precedence:** no change. Stagings under one parent tie, and a Plot under two parents keeps the best rank (spec 13).
- **Cycles** in the `START SUBPLOT` graph are a compile-time error.
- **Handed off:** joiners and leavers carrying through to a Subplot go to *Cast changes mid-Plot*; what a Director does with an Outcome's Agent goes to *Director capabilities*; top-level Plots go to *Instancing comments*; Plot parameters, `SIGNAL PARENT`, ending a single Staging and recursion go to the fog (*Richer Subplots*).

## Comments
- From *Priority model* (14): a parent orders its direct Subplots against itself (`SELF`) and each other in its `PRECEDENCE:` Block, naming them by Plot name; a Subplot counts together with everything it starts, and refers to its parent only as `PARENT`. By default a Subplot beats its parent. Check how this works when the same Plot is started from two different parents, or twice as two Stagings (spec 13 assumes one Playbook given twice ranks at its best position). See `docs/spec/13-plan-selection.md`.
- From *Roles inside Playbooks* (16): the Mapping form and counts are decided in `docs/spec/15-roles-and-mappings.md`: `START SUBPLOT HonorDuel, MAPPING 1 OF Guest TO Challenger, MAPPING 1 OF Guest TO Defender.` Same-name Roles map implicitly, unfilled Roles are errors, `n OF` / `n PERCENT OF` picks are random, made once, never grow, and don't overlap within one Statement. This ticket keeps how a running Subplot uses its Roles, parent/child cooperation, and how Stagings are told apart.
