# Telling Stagings and Givings apart, and what a Subplot is given

Type: grilling
Status: open
Blocked by: 06

## Question

Can two Stagings of one Plot, or two Givings of one Playbook, be kept apart, and what does a Subplot get from its parent besides a copied Cast?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- F2 A Giving and a Staging have no identity
- D12 Being cast in a Subplot adds and never takes away
- D13 A Plot takes no arguments
- F9 Only the Root Plot has a living cast

Decide:

- Whether 2.0 gets identity, or forbids or warns about what it can't keep apart (a second Staging with an overlapping Cast, `UNASSIGN … FROM ?who` over a setup's Giving).
- Arguments to a Plot.
- Whether a Subplot can suspend a Playbook of its Cast.
- Live Casts below the Root, and a mark for the Root Plot.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

Blocked by: [What can be said about a Role](06-roles.md).
