# The Vocabulary and the game

Type: grilling
Status: open
Blocked by: none

## Question

What does a declaration say about the game's side, and what is checked about the Values that fill it?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- B1 Dotted External names are refused by the only Target
- D14 The Vocabulary names what the game supplies and not what the game does
- F8 Values are neither declared nor typed
- L8 The Role files are fixed at build time (the *Translation to ASL* note)

Decide:

- What an External name may look like for each kind, and what `hall.guards.seize` should be. The showcase is fixed to match.
- Whether a declaration can say who sends an Event, who keeps a Fact, whether an Action can be refused or ends the Agent.
- Declared Names, typed Parameters, or a Placeholder known to hold an Agent of a Role: which of these, and when.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.
