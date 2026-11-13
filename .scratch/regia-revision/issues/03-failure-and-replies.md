# Failure a Plan can read, and answers to an `ASK`

Type: grilling
Status: open
Blocked by: none

## Question

How does an Agent learn why something failed, and how does whoever asked learn how it went?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- N6 A Failure has no reason a Plan can read
- F3 A request has no reply
- L3 `PURSUE` waits and `ASK` does not (ADR 0005)

Decide:

- Whether `FAILED` carries a reason, and what the reasons are.
- Whether a `WHEN` Plan's Failure or a non-waited Action's result can be reacted to.
- Whether any part of replies (chapter 07's reserved clauses) comes into 2.0, since the showcase reports a Failure by sending the Signal for success.
- Confirm or reopen ADR 0005.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.
