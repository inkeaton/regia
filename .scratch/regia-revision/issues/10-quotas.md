# Quotas

Type: grilling
Status: open
Blocked by: none

## Question

What does a Quota Plan know, when does it fire, and what happens when the cast is smaller than the count?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- D8 A Quota counts, and that is all it does
- D9 The size of a Quota is in the Plot and the size of the hall in Instancing
- B5 `PERCENT` rounds up in a Trigger and down in a Mapping
- D1 rows `FROM Guest` / `FROM ALL Guest` and quantity

Decide:

- Who sent the counted Signals, and counting a Signal that carries data.
- Once or every time, and a Quota met while no `GIVEN` holds.
- A Quota that can't be met, `ALL` of an empty Role, firing on a departure.
- One rounding rule, and whether a quantity is an Expression everywhere.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.
