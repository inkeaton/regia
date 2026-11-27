# Names: chapters 06–10

Type: grilling
Status: closed
Assignee: claude
Blocked by: 02, 03

## Question

What is the name of each code in chapters 06 to 10 (`R06`–`R10`) (about 41 codes, retired ones included)? The rules are in *The shape of a code*.

Claude drafts a name for each code from `../inventory.txt` and the chapter's check list, starting from the case-file slug where a case exists, and checks the draft against `GLOSSARY.md`. The user reviews the batch and settles every name. The settled rows are appended to `../mapping.csv`, and `rename_codes.py check --partial` must pass on them.


## Resolution

Settled with the user on 2026-11-27. The 41 rows for `R0601`–`R1016` are in [`mapping.csv`](../mapping.csv), and `rename_codes.py check --partial` passes on them (195 codes left unmapped).

**Choices past the patterns of *Names: chapters 01–05*:**

- **`R10_04-name-out-of-scope`**: `undeclared-name` was already `R0310` (a Name not declared with `NAME`). `R1004` covers a name declared nowhere and one declared in a file not reached.
- **`R0501` and `R1005` overlapped on kind.** The spec now gives kind to `R0501` alone: `R1005` (`R10_05-conflicting-redeclaration`) is about declarations of one kind that disagree on parameter count, External name or `GAME`. Edited in chapter 10's check list, chapter 23 (an `R0501` also marks the item *conflicted*) and the guide's *Vocabulary and files*.
- **Parallel pairs** are named in parallel: `as-on-wrong-declaration` and `game-on-wrong-declaration`, `if-placeholder-outside-branch` and `option-placeholder-outside-option`, `signal-with-non-cue` and `ask-with-non-goal`.
- **`R0807` is `edit-of-game-fact`**: `change` is avoided because `CHANGE` is a retired keyword (`R08_08-retired-change`).
- **`R1012` is `misplaced-action-or-cue`**, not `local-…`, because a local Cue in a Playbook is allowed.
- `ask-with-non-goal` replaced the agreed `ask-with-fact-or-cue`, which the script refused at five words.
