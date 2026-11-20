# The Visual Editor

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
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
- What a rename says when it flips a competition ordered only by name ([*Which Plan runs*](12-which-plan-runs.md) kept name order, D3, and left this here).
- Which Program an open file's markers belong to, when a `.regia` file is reached by several `.regin` Entries. From [*The command line, Programs and Diagnostics*](16-command-line-and-diagnostics.md): a Program has one Entry, each `.regin` is its own Program, an unreached `.regia` is checked alone with no Root Plot, and allowed warnings are shown faded with an *Allow here* quick fix (spec 24).

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

Blocked by: [What passes between a Playbook and a Plot](01-playbook-plot-interface.md).

## Resolution

Resolved on 2026-11-17, with the user.

- **N13, fixed.** The `DURING PLOT` layer is on by default. The Givings, Messages, Entry and exit, Knowledge and Plain comments layers also write on the "any phase" node, and the Docs page gives `DURING PLOT` Plans a section of their own. Deleting a Phase still removes only its `PHASE` line and `DURING` Block, but only after a confirmation that lists the Plans removed (with how many the drawing doesn't show) and every reference left broken: `TRANSITION TO`, `IN p`, `UNTIL EXITED`, and Plans that take back what only that Phase gave.
- **N14, fixed.** The Trigger picker writes whole Triggers: a Signal with its possible senders (or "anyone"), and a quantity for what a Quota can count. A new declaration goes at the end of a comment section the designer picks, by default the one holding the most Events the Plot already uses.
- **B13, fixed.** The picker is built from the Interface and from `GAME EVENT`, and offers only Events someone sends. A new Event is declared in a file that both the Plot and the sending Playbook reach, and the picker asks which Playbook sends it. The "this file" and "Local Vocabulary" choices are gone. The `SIGNAL` is written by hand, and `R3802` stays on the Plan until it is.
- **B14, fixed.** The web app keeps its own undo stack across Monaco models. An edit that touched several files is undone whole from any of them while it is the latest edit in each; otherwise only that file's part is undone, with a notice. The "Undo all" toast is gone.
- **D18, fixed.** Only Plots are drawn. Every `.regia` file has a Docs page: Plots, Playbooks (Local Vocabulary, Goals and recipes, Plans by Trigger) and Vocabulary, with each one's Interface. The Inspector's Names used table shows each name's `#@desc`. Every Statement is drawn somewhere: a Knowledge layer for `LEARN`/`FORGET`/`CHANGE`, `END SUBPLOT` on the Subplots layer, Plan cards summarising every Statement, a Roles layer in Nested Plans, and an edge's Message lines when another edge shares its endpoints and Trigger. A Playbook drawing is deferred past 2.0.
- **D19, fixed (rename), kept (moving).** A rename shows a preview: references, whole-word matches in doc comments, and the file when it is named after the construct (through `moveFile`). Each of the last two can be unticked; plain comments are left alone. No 2.0 operation moves an Extent. The Extent rules stay, since they serve `delete` and a later move, and chapter 22 says so.
- **L9, kept.** Only Chromium lets a web page open a disk folder. The editor's note names the command line and the desktop wrapper (Tauri) planned past 2.0.
- **From [*Which plan runs*](12-which-plan-runs.md):** the rename preview lists every pair of Plans decided only by name order whose winner the new name changes.
- **From [*The command line, Programs and Diagnostics*](16-command-line-and-diagnostics.md):** the status bar holds an **Active Entry**, which by default is the last `.regin` opened or built that reaches the file. Markers, semantic tokens, name origins, Docs and Interfaces come from its Program, and the status bar offers a switch when other Entries reach the file.
- **From [*What passes between a Playbook and a Plot*](01-playbook-plot-interface.md):** an Interface is shown on the Docs page of a Plot and of a Playbook, and in the Inspector for a selected `ASSIGN` or `START SUBPLOT`, with the Interface Diagnostics in place. It is never drawn on the canvas.

Changed:

- Spec: chapters 22, 23 (`setActiveEntry`, `entriesReaching`, `docs`, `preview`), 24 and 25.
- ADRs: none. These are editor behaviour, changeable in a release; ADR 0011 stands.
- Glossary: *Active Entry* added.

Handed on:

- Guide chapter 17 and the showcase: under *Not yet specified* (the guide isn't kept in step).

1.5: N13 in. N14 in, without the quantity field (Quota Triggers are later). B13 in, without the `FROM GAME` and `OR` sender choices. B14 in. D18 in. D19 in. L9 kept as it is. None of these needs a later part to work: the 1.5 picker is the 2.0 picker with fewer choices.
