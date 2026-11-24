# Decide: Visual Editor

Type: grilling
Status: open
Assignee:
Blocked by:

## Question

Chapters 24 and 25 against the rest of the spec:

- F56: how does the Phase map draw an `AFTER <Duration>` Plan, and what do the Trigger picker and the graph view data offer for it? (Guide: a dotted edge labelled with its Trigger; "a timeout" in the picker.)
- F57: what is the label of an `ELSE` Plan's edge? (Guide: `AFTER 20 SECONDS · ELSE`.)
- F58: does the DURING PLOT layer read `IN p` in an `IF` condition?
- F59: should a layer draw Custom Actions outside `ENTERED`/`EXITED`, `PRINT` and a Phase's Role setups, or should "every Statement is drawn by some layer" be narrowed? (Guide: the Phase map leaves them out.)
- F60: what is the full list of Statements a card summarises (`IF`, a Pick, `RANDOMLY`, `FOR EACH`, `PRINT`)? (Guide: "`IF` and a Pick".)
- F63: does the picker write a Sender for a new Cue, and which warnings does the new Plan carry (`R3802`, `R3807`)?
- F64: how is a file name derived from a construct's name when it is renamed? (Guide: `honor_duel.regia` → `duel.regia`.)
- F65: is the list of semantic-token kinds closed, and should Actions, Names, Phases and Propensities be in it?
- F66: where does the editor show the conflict report and the Interfaces?

Start each question from the guide's reading. Mark which answers need an ADR.

Applying the answers is *Apply: Visual Editor*.
