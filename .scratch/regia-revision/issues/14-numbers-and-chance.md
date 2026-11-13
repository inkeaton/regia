# Numbers, rolls and repetition

Type: grilling
Status: open
Blocked by: none

## Question

Fix the rules for rolls and names that disagree, and settle the ones the spec doesn't give.

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- B4 A roll is whole or decimal by how its bounds are written
- B6 A name made in every branch outlives an `IF` and not an `EITHER`
- D15 Rules the spec doesn't give (the roll in a setup, the seed's coverage, wrong Weights)
- F5 No loop, and no weighted Pick
- F10 the short spellings (`CHANGE`, "only sometimes", `COUNT … = 0`, bare `HIGHEST`)

Decide:

- When a roll is whole, in a Body and in a `.regin` file, and whether anything rounds.
- One rule for names made in every branch.
- A setup's roll: once, or per Agent.
- What the seed covers.
- Loops, weighted Picks and the short spellings: 2.0, later, or a warning.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.
