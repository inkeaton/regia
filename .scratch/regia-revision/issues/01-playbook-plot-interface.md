# What passes between a Playbook and a Plot

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
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

## Resolution

Resolved on 2026-11-16, with the user.

- **N3, fixed.** Nothing is declared. The Transpiler works out the **Interface** of each Playbook and Plot from the whole Program and checks one side against the other. New warnings: a Signal the giving Plot never handles (`R3801`, on the `ASSIGN`), a `FROM <Role>` Director Plan no Signal can reach (`R3802`), Mappings that leave an `ASK` or `TELL` with no `FROM` that admits the sender (`R3803`), an ending the parent never matches (`R1708`, on the `START SUBPLOT`). A Signal handled in some Phases only gets no build check. At runtime a Signal or an ending that finds no Plan writes a Trace entry and nothing else (`T3801`, `T3802`). No marker on `EVENT` lines: the Interface gives each Event its inferred senders.
- **B16, fixed.** `GOAL` inside a `PLOT` is an error (`R1015`).
- **L8, the Events half, fixed.** `EVENT` may be declared inside a `PLAYBOOK`: never from the game, no External name, told to any recipient, never Signalled and never an Outcome. Not allowed in a `PLOT`. The Role-files half is in [*The Vocabulary and the game*](07-vocabulary-and-the-game.md).

Changed:

- Spec: new chapter 38 (`38-interfaces.md`); chapters 07, 10, 17, 20 and 34.
- ADRs: 0015 *The Interface is inferred, not declared*; 0016 *An Event may be local to a Playbook*.
- Glossary: *Interface* added; *Local Vocabulary* and *Signal* reworded.

Handed on:

- The command that prints an Interface: [*The command line, Programs and Diagnostics*](16-command-line-and-diagnostics.md).
- How an Interface is drawn: [*The Visual Editor*](18-visual-editor.md).
- The Jason chapters (28 to 31) don't yet describe the Director's catch-all for `T3801`/`T3802`; chapter 38 only notes it.

1.5, from [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md):

- N3 in, without the checks added later by [*The Sender, the game and "me"*](04-sender-and-self.md) (`R3805`, `R3806`). B16 in. L8, the Events half, in.
