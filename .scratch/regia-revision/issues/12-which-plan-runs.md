# Which Plan runs

Type: grilling
Status: open
Blocked by: none

## Question

Text order, falling through and Precedence each decide part of which Plan runs for a Trigger. Is each rule right, and do they fit together?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- L2 `GIVEN` is the Context and `IF` is control flow (ADR 0004)
- D2 A missing `ELSE` means two things
- D3 Name order is the default Precedence
- D4 A Subplot orders itself against a parent it can't see
- B8 A default order can close a cycle
- L6 Precedence is written where Playbooks are put together (ADR 0008)
- F6 One Plan per Trigger, and Plans that know nothing of each other

Decide:

- Whether Statements may stand before or after `GIVEN` branches. Confirm or reopen ADR 0004.
- What a missing `ELSE` means, and whether falling through is written out.
- The default order: name order, an error, or something a rename can't change.
- `PARENT`, `SELF`, and whether a default gives way in a cycle.
- From chapter 13's *Not in 2.0*: a Phase Plan that adds to `DURING PLOT`'s, and Actions that can't run together. 2.0 or later.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.
