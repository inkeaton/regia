# Decide: Interfaces and Precedence

Type: grilling
Status: open
Assignee:
Blocked by:

## Question

- F39: is a `WHEN` Trigger with no `FROM` listed in a Playbook's Interface? (Guide: a recipe with no `FROM` is open to anyone; `WHEN` Triggers with no `FROM` are left out.)
- F40: is a Plot's Signals row limited to Cues some `SIGNAL` sends, or are game Cues listed too?
- F42: how does `regia explain <entry> interface` print an Interface, and how is a local Cue shown beside its Playbook? (Guide: tables of parts, no printed form.) The README's coverage claim is in *Decide: Showcase README coverage*.
- F43: does `R13_07-unreachable-trigger-block` warn when one Phase always catches a Trigger while `DURING PLOT` still runs in the others?
- F44: in the conflict report, is a Block whose Trigger has a Value or a narrower `FROM` a full stop? Which Plot's Roles does "per Role" mean when a Playbook goes to a Subplot's Role?
- F78: what name does a merged `TIES` pair sort under for the alphabetical tie-break? Does an `lv` step list only items whose level differs from `N`? (Guide: the first of its names.)

Start each question from the guide's reading. Mark which answers need an ADR.

Applying the answers is *Apply: Interfaces and Precedence*.
