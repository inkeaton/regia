# The Visual Editor

Type: grilling
Status: open
Blocked by: 01

## Question

What does the editor draw, and what do its edits reach?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- N13 `DURING PLOT` is off the default drawing
- N14 The Trigger picker offers bare Events
- B13 The Trigger picker declares an Event nobody can send
- B14 Undo takes back half of a rename
- D18 The drawing is of a Plot
- D19 Edits that go further or less far than they look
- L9 The browser decides where a Project lives

Decide:

- Whether a Playbook gets a drawing or a Docs page in 2.0.
- `DURING PLOT` on the default map, and what deleting a Phase removes.
- What the picker writes (Sender, quantity) and where a new Event is declared.
- Undo across files; what a rename follows; whether moving an Extent is an operation.
- Which Program an open file's markers belong to (with *The command line, Programs and Diagnostics*).

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

Blocked by: [What passes between a Playbook and a Plot](01-playbook-plot-interface.md).
