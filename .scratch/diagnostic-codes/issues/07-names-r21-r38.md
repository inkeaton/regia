# Names: chapters 21–38

Type: grilling
Status: closed
Assignee: claude
Blocked by: 02, 03

## Question

What is the name of each code in chapters 21, 26 and the Target and interface chapters (`R21`–`R38`) (about 44 codes, retired ones included)? The rules are in *The shape of a code*.

Claude drafts a name for each code from `../inventory.txt` and the chapter's check list, starting from the case-file slug where a case exists, and checks the draft against `GLOSSARY.md`. The user reviews the batch and settles every name. The settled rows are appended to `../mapping.csv`, and `rename_codes.py check --partial` must pass on them.


## Resolution

Settled with the user on 2026-11-27. The 44 rows for `R2101`–`R3807` are in [`mapping.csv`](../mapping.csv), and `rename_codes.py check --partial` passes on them (47 codes left unmapped: the Trace codes and `R0412`). No name in this batch is over 30 characters.

**Choices past the patterns of the earlier batches:**

- **Glossary terms over file extensions**: `R21_01-import-of-instancing-file` and `R21_02-declaration-in-instancing-file` say "Instancing file", not `.regin`.
- **Mirrored names for mirrored checks**: `R21_03-conflicting-sibling-files` and `R21_20-conflicting-bases`, and `R38_05-pursue-without-me-recipe` and `R38_06-ask-only-me-recipes`.
- **Parallels with earlier batches**: `R21_07-wrong-propensity-value` (`wrong-label-value`), `R21_24-retired-equals-setting` (`retired-equals-statement`), `R21_25-retired-and-in-plays` (`retired-and-in-label`), `R21_23-kind-and-agent-clash` (`case-only-name-clash`), `R26_04-placeholder-outside-for-each` (`if-placeholder-outside-branch`).
- **`R26_05-maybe-unfilled-pick-weight`**: `maybe-unfilled-weight` is already chapter 09's, so chapter 26's Weight says `pick`.
- **`R26_07-quantity-in-condition`** uses chapter 18's "Quantity", and `condition` as in *Names: chapters 01–05*.
- **Absence checks** follow `X-never-Y` (`root-role-never-played`, `plot-never-reached`, `quota-never-met`, `cue-never-signalled`, `reason-never-given`, `cue-never-sent`) and `unheard-X` (`unheard-signal`, `unheard-message`). `R38_04` uses the glossary's "Reason", which "a Plan gives".
- **Retired codes** get the plain name of what they reported: `R21_11-missing-propensity-value`, `R28_01-external-name-not-atom`, `R35_01-console-level-setting`.
- **Case slugs not followed** because they are too long or name only part of the line: `R21_05-plays-non-root-role` (case `plays-a-role-the-root-plot-lacks`), `R26_03-misplaced-pick` (`pick-on-for-each`).
- **Weakest names**, accepted as drafted: `R21_17-agent-plays-nothing` (it covers kinds too, whose Agents play nothing), `R21_21-undeclared-name-after-no`, `R26_02-rank-on-unmatched-placeholder`, `R36_03-kind-numbered-agent-name`, `R38_06-ask-only-me-recipes`. They can still change before the 1.5 release.
