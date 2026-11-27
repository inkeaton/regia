# Run the migration

Type: task
Status: closed
Assignee: claude
Blocked by: 02, 03, 04, 05, 06, 07, 08, 09

## Question

Apply `../mapping.csv` to every live file, and confirm that nothing was invented or missed.

1. `rename_codes.py check` passes: every code is mapped, no entry is unused, and the names are unique.
2. `rename_codes.py apply`, then read the `git diff` by sampling every directory, plus every line under *Check by hand*. Reword each reported range as *Rewrite the spec text on codes* decided.
3. Grep the live files for `\b[RT]\d{4}\b`: there are no hits.
4. From `transpiler/`, run the four checks in `CLAUDE.md`, all clean (the case runner reads the case files).
5. Re-read chapter 27's code section and one chapter's check list as rendered Markdown.

The user reviews the diff and decides when to commit.

## Resolution

Done on 2026-11-27.

1. `check` was clean: 288 codes, all mapped, no unused entry, names unique. 1790 replacements in 151 files.
2. `apply` rewrote those 151 files (spec 38, cases 43, guide 26, ADRs 24, showcase 1, open tickets 19). A word diff against a pre-migration copy was sampled in every directory: only codes changed. The 12 ranges under *Check by hand* were reworded by decision 4 of *Rewrite the spec text on codes*:
   - Whole lists, in words: guide 21 (*the three under* Ports), the showcase's chapter 38 row, chapter 18's 1.5 note (*this chapter's checks and Trace codes*), and chapter 34's table (chapter 11's Trace codes; chapters 28, 33 and 37's).
   - Partial sets, listed code by code: ADR 0015, chapters 01, 11, 16 (the nine live codes; the retired `R15_05` left out, as the user chose) and 38.
3. No `\b[RT]\d{4}\b` or `R..xx` left in the live files. Every new-shape code there is in `mapping.csv`, apart from the deliberate wrong name `R03_07-ignored-placeholder` in `cases/02-comments/allow-with-a-misnamed-code.regia`.
4. `cargo fmt --check`, `clippy`, `test` and `doc` are clean. There is no case runner yet, so no test reads the case files.
5. Chapter 27's *Diagnostic codes* and chapter 12's check list read correctly.

`mapping.csv` is now the frozen record for reading old codes. `inventory.txt` is the pre-migration inventory and is no longer current. The pre-migration copy of the live files is a scratchpad tarball (not kept in the repo). The user reviews the diff and decides when to commit.
