# Names: chapters 01–05

Type: grilling
Status: closed
Assignee: claude
Blocked by: 02

## Question

What is the name of each code in chapters 01 to 05 (`R01`–`R05`) (about 53 codes, retired ones included)? The rules are in *The shape of a code*.

Claude drafts a name for each code from `../inventory.txt` and the chapter's check list, starting from the case-file slug where a case exists, and checks the draft against `GLOSSARY.md`. The user reviews the batch and settles every name. The settled rows are appended to `../mapping.csv`, and `rename_codes.py check --partial` must pass on them.

This batch comes first and sets the patterns the other batches follow: how a retired spelling is named (chapter 01's table), how a warning reads beside an error, and which recurring words are used (`without`, `unknown`, `twice`…). Record the patterns in the resolution.

## Resolution

Settled with the user on 2026-11-27. The 52 rows for `R0101`–`R0513` are in [`mapping.csv`](../mapping.csv), and `rename_codes.py check --partial` passes on them (236 codes left unmapped, `R0412` among them).

**Patterns for the other batches:**

- **Retired spellings** are `retired-<old spelling>`: `R05_13-retired-event`, `R04_07-retired-equals-statement`, and later `retired-change`, `retired-either`, `retired-at-random`. A retired spelling stays retired for ever (chapter 01), so this is not a status marker. A **retired code** (`R0107`) gets the plain name of what it used to report: `R01_07-unclosed-flat-block` (a Flat block still open at the end of the file, from *Words and syntax*).
- **Warnings** carry no marker: `unused-placeholder`, `stale-allow`, `block-without-body`. Severity is not identity.
- **Recurring words**:
  - `X-without-Y`: a required part is missing (`clause-without-comma`, `fact-trigger-without-kind`).
  - `X-as-Y`: used as the wrong kind of thing (`role-as-value`, `keyword-as-name`).
  - `X-in-Y`: in a place it can't go (`expression-in-trigger`, `me-in-plot`). `condition` means "a Context or an `IF` condition" (`let-in-condition`).
  - `X-on-Y`: a Clause on a Trigger that can't take it (`from-on-forgotten`, `from-me-on-cue`).
  - `stray-X`: a character or mark nothing uses (`stray-semicolon`, `stray-character`).
  - `undeclared-X`: should have been declared and wasn't (`undeclared-name`). `unknown-X` is kept for something outside a fixed set.
  - `wrong-X`: a choice that doesn't fit (`wrong-argument-count`, `wrong-trigger-kind`).
  - Adjective first: `unclosed-`, `unused-`, `unfilled-`.
- **A line that covers two mistakes** gets one name broad enough for both, with no spec split: `R01_13-malformed-string`, `R03_11-misused-name-declaration`, `R05_11-placeholder-without-sender`, `R05_12-from-word-after-by`. Splitting a code is only worth a ticket if no name can cover the line.
- **Version numbers stay out of names**: the script counts `1-5` as two words. `R0109` is `R01_09-later-regia-construct`, which stays true when 2.0 retires it.
- `R0412`, chapter 23's fake example, is **not mapped**. *Rewrite the spec text on codes* replaces the example.
- **Case file names are not renamed**, even when the slug no longer matches the name or breaks the glossary (`naming-a-filled-placeholder.regia`). Out of scope for this map.
