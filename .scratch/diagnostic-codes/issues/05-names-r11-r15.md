# Names: chapters 11–15

Type: grilling
Status: closed
Assignee: claude
Blocked by: 02, 03

## Question

What is the name of each code in chapters 11 to 15 (`R11`–`R15`) (about 52 codes, retired ones included)? The rules are in *The shape of a code*.

Claude drafts a name for each code from `../inventory.txt` and the chapter's check list, starting from the case-file slug where a case exists, and checks the draft against `GLOSSARY.md`. The user reviews the batch and settles every name. The settled rows are appended to `../mapping.csv`, and `rename_codes.py check --partial` must pass on them.


## Resolution

Settled with the user on 2026-11-27. The 52 rows for `R1101`–`R1517` are in [`mapping.csv`](../mapping.csv), and `rename_codes.py check --partial` passes on them (143 codes left unmapped).

**Choices past the patterns of the earlier batches:**

- **`R15_01-role-name-as-value`**: `R1501` was retired into `R0303` (`role-as-value`), and names are unique, so the retired code needs its own wording for the same mistake.
- **`misused-<construct>`** names a line that covers several mistakes with one construct: `misused-fail-with`, `misused-ties`, `misused-mapping`, `misused-assigned-or-removed`, `misused-until-exited`, `misused-except`, `misused-plays`, `misused-cast`.
- **`-or-` names** join two mistakes when no broad word covers both: `unknown-or-repeated-label`, `misplaced-count-or-share`, `misused-assigned-or-removed`.
- **The case slug is not followed** when it names an outcome or covers only part of the line: `R12_01-wrong-duration-unit` (case `wait-without-a-unit`), `R14_04-wrong-label-value` (case `suits-value-out-of-range`), `R15_08-misused-assigned-or-removed` (case `misplaced-plan-is-left-out`).
- **`R14_07-local-propensity`** uses `local-` because a `TRAIT` or `MOOD` inside a `PLAYBOOK` or `PLOT` is never allowed. `R1012` avoided `local-` because a local Cue is allowed.
- **`R14_05-misplaced-suits`**: "Branch" is kept for `IF`, and `ELSE` has no Context, so neither word could name the place.
- **The 4-word limit is hard.** The script counts every hyphenated part (`out-of-range` is 3 words). Three agreed names failed it and were replaced: `label-value-out-of-range` became `wrong-label-value`, `suits-on-given-or-else` became `misplaced-suits`, and `clause-on-assign-to-placeholder` became `clause-on-placeholder-assign`.
- Over the 30-character soft limit, kept: `relation-without-shared-trigger`, `suits-without-selection-function`.
