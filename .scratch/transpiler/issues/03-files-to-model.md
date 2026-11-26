# Review: files to Model

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 02

## Question

How do the files of a Program become one Model?

Work by hand: two files, an `IMPORT`, and `ASSIGN Brawling TO Guest`.

Decide: the order of Model build (collect declarations, then resolve); ids and origins; what an unresolved name leaves in the Model; how much of a broken construct is kept; what differs for a `.regia` Entry (no Root Plot).

Chapters 10, 21, 23; ADR 0012.

From *Review: tokens to tree to accessors*: a Plan or Statement with an `R0109` is left out of the Model. How does that not cause other Diagnostics (a Cue that then looks unused)? When is it left out, if only resolved names show it (a Goal's ending in a Plot)?

## Resolution

Agreed with Edoardo on 2026-11-25. The answer is in chapter 23, *From files to the Model*.

- **Steps.** Reach, collect, resolve, whole Program.
- **Ids.** One list per sort of item; one name table per Program, visibility checked per lookup; several origins per item.
- **References** are `Option`s; `None` means already reported.
- **Broken code.** Left out: a Statement without an essential part, a Plan without a Trigger, a declaration without a name.
- **Absence checks** are silent about unread names and missing imports. This answers the question from *Review: tokens to tree to accessors*.
- **The late `R0109`** moved from Validate to Model build, during resolve.
- **`.regia` Entry.** Same code, no Root Plot.
- **For *Review: diagnostics and where checks live*:** Model build reports Diagnostics too; which other checks are absence checks; the rules on silence need Conformance cases.
- **Teach-back.** Two examples worked. The unread-names rule slipped twice, then was confirmed; reach going downwards only was right the second time.
- No ADR: each choice is local to `model` and cheap to change.
