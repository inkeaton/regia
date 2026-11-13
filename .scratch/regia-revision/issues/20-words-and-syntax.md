# Words that do several jobs, and syntax nobody used

Type: grilling
Status: open
Blocked by: 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15

## Question

After the language tickets have settled what stays, which words get a second spelling and which unused syntax goes?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- D1 A few words do many jobs
- D16 Parts of the syntax the showcase never needed (the language notes)
- D15 the Doc comment above a Multi-definition
- L1 Placeholders are filled by matching (ADR 0001, ADR 0002)
- L4 A Director asks; a setup is written in the Agent's words (ADR 0009)
- L7 Phases are a set, and the `PHASE` lines look like a sequence

Decide:

- Go through the table of D1 row by row: rename, keep, or already changed by an earlier ticket.
- The optional `.`, the `;`, the blank line under a Doc comment, `#@` against `#`, unchecked Imports.
- Confirm or reopen ADRs 0001, 0002 and 0009 as far as the notes touch them.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

Blocked by every language ticket (01 to 15), since a word is only worth renaming once its construct is known to stay.
