# When a Giving starts and ends, and what a joiner gets

Type: grilling
Status: open
Blocked by: none

## Question

What can react to a Playbook being given or taken, can a Giving or a Subplot be tied to a Phase, and how do a setup, a standing `ASSIGN` and a one-off Message treat an Agent that arrives late?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- N2 A Giving has no start and no end that anything can react to
- D7 A Giving is standing and a Message is sent once
- B3 The Role setups run before the first Phase starts counting

Decide:

- Triggers for a Playbook given and taken away, and what happens to its Goals and Local Facts when it goes.
- A Giving or a Subplot that lasts as long as a Phase.
- Whether a Director can call off a Goal it asked for.
- One rule for what a joiner receives, and whether a setup can depend on the Phase.
- The order of Role setups and the entry of the initial Phase.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.
