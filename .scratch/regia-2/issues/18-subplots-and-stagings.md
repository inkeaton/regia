# Subplots and Stagings

Type: grilling
Status: open

## Question

How do Subplots work (primer ch.5)? Decide how Roles are mapped (`START SUBPLOT HonorDuel MAPPING Guest TO Challenger`), including mapping a count or fraction of a Role's Agents. How do parent and child cooperate (the parent reacts to `SUBPLOT … ENDS`; does `END PLOT` end the children; can the child report outcomes or values to the parent)? How are Stagings identified when the same Plot runs several times at once?

## Comments
- From *Priority model* (14): a parent orders its direct Subplots against itself (`SELF`) and each other in its `PRECEDENCE:` Block, naming them by Plot name; a Subplot counts together with everything it starts, and refers to its parent only as `PARENT`. By default a Subplot beats its parent. Check how this works when the same Plot is started from two different parents, or twice as two Stagings (spec 13 assumes one Playbook given twice ranks at its best position). See `docs/spec/13-plan-selection.md`.
