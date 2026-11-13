# What passes between a Playbook and a Plot

Type: grilling
Status: open
Blocked by: none

## Question

Should a Playbook declare the Goals it expects to be asked and the Signals it sends, and a Plot its Outcomes, so that the Transpiler can check one side against the other and report a Signal, an ending or an `ASK` that nobody handles?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- N3 A Playbook and a Plot don't declare what passes between them
- B16 A `GOAL` declared in a Plot
- L8 Events are global (the part on local Events; the Role files are in *The Vocabulary and the game*)

Decide:

- Declared, inferred and shown by the tools, or left as it is.
- If declared: where (the Playbook, the Vocabulary, the `EVENT` line), and which mismatches become errors or warnings.
- Whether an Event may be local to a Playbook or to a pair of Roles.
- What a Signal with no Plan in the current Phase does: nothing, a warning at build, an entry in the Trace.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.
