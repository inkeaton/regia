# The command line, Programs and Diagnostics

Type: grilling
Status: open
Blocked by: none

## Question

What can the `regia` command do, what is one Program, and how is a Diagnostic named and answered?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- N9 The command line is two words
- N10 Only a whole story can be checked
- N11 A warning can't be answered
- B2 A Target's checks run only in the emit
- B11 Several Entry files: one Program or two
- B12 The Build folder
- D20 Diagnostic codes follow the spec's table of contents

Decide:

- The list of commands and options: running a Build, a behaviour case of our own, the conflict report, the seed, the Target, the console.
- Checking a Playbook or a Subplot alone.
- Marking a warning as seen.
- Target checks in `regia check`.
- One Entry file or several; the name and the content of the Build folder.
- Codes and the note severity.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.
