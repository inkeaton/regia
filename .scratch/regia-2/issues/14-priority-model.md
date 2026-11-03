# Priority model

Type: grilling
Status: open
Blocked by: 13

## Question

How are conflicts between Plans resolved in Regia (primer ch.2, ch.4)? Several Playbooks, possibly given by different Plots, can react to the same Event. Decide the model (relative or absolute, hierarchical by Plot/Playbook/Plan, mutually exclusive Actions, utility, …), what it applies to (Plans only, or Playbooks and Plots too), and how a designer writes it. `PRIORITY` may become something entirely different.

## Comments

Starting point from the plan-conflict research (13): "priority" is really four decisions (event selection, plan selection, pre-emption between running intentions, actions that can't run together). Decide which of these Regia exposes, and whether each gets its own construct.

From *Parameters and variables* (03): when several matches satisfy a Context, which one is used is unspecified. Consider whether the priority model also orders matches, for example "the guest I hate most", or whether that's a separate construct. A Value in a Trigger restricts a Plan (`WHEN insult_heard(host)`), so a specific Plan and a general one (`WHEN insult_heard(?speaker)`) can both match the same Event.
