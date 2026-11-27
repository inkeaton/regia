# Names: chapters 16–20

Type: grilling
Status: closed
Assignee: claude
Blocked by: 02, 03

## Question

What is the name of each code in chapters 16 to 20 (`R16`–`R20`) (about 52 codes, retired ones included)? The rules are in *The shape of a code*.

Claude drafts a name for each code from `../inventory.txt` and the chapter's check list, starting from the case-file slug where a case exists, and checks the draft against `GLOSSARY.md`. The user reviews the batch and settles every name. The settled rows are appended to `../mapping.csv`, and `rename_codes.py check --partial` must pass on them.


## Resolution

Settled with the user on 2026-11-27. The 52 rows for `R1601`–`R2016` are in [`mapping.csv`](../mapping.csv), and `rename_codes.py check --partial` passes on them (91 codes left unmapped). No name in this batch is over 30 characters.

**Choices past the patterns of the earlier batches:**

- **`X-never-Y`** names an absence check on something the Plot never does: `R17_04-subplot-never-started`, `R17_12-subplot-never-dropped`, `R20_12-goal-never-asked`.
- **`ignored-X`** names a warning for a construct that can't take effect: `R17_05-ignored-end-plot-with` and `R20_15-ignored-exited-by-parent`, both in a Plot never started as a Subplot.
- **`unheard-X`** names an ending nothing hears: `R17_08-unheard-subplot-ending`, `R17_13-unheard-until-exited-ending`.
- **Mirrored names for mirrored checks**: `R20_01-playbook-statement-in-director` and `R20_02-playbook-trigger-in-director`, opposite chapter 15's `director-statement-in-playbook` and `R20_05-director-trigger-in-playbook`. `R17_16-shadowed-finished-with` and the retired `R17_07-shadowed-ended-with` follow `shadowed-failed-with`.
- **`wrong-statement-in-X`** names a Block that takes only some Statements: `R16_02-wrong-statement-in-setup`, `R20_03-wrong-statement-in-exited`.
- **"Cast change"** got a `GLOSSARY.md` entry (`JOINED`, `LEFT`, `EMPTIED`) for `R19_01-cast-change-in-playbook`, `R19_02-wrong-cast-change-subject` and `R19_04-quantity-on-cast-change`. **"Quantity"** (chapter 18's `ALL` / `n OF` / `n% OF`) is used without a glossary entry: it is part of the Quota Trigger entry, not a term of its own.
- **`R20_06-do-with-subject`** (`Role DO`, `WORLD DO`) avoids clashing with chapter 08's `misused-do`. **`R20_14-misplaced-in-clause`** treats `IN <phase>` as a Clause.
- **Case slugs not followed** because they name only part of the line: `R16_02` (case `custom-action-in-a-setup`), `R16_04` (`plot-parameter-in-a-setup`, which is the exception), `R18_04-wrong-quantity` (`percent-over-a-hundred`), `R19_01` (`joined-in-a-playbook`), `R20_01` (`pursue-in-a-director`).
- **The 4-word limit counts `non-role` as two words**: `cast-change-of-non-role` failed it and became `wrong-cast-change-subject`.
