# Write the migration script

Type: task
Status: closed
Assignee: claude
Blocked by: 01

## Question

Write the one-off script that renames every code from a mapping file, with the guarantees in *The shape of a code*. No real mapping exists yet, so it is tested on a small mapping and a copy of a few files.

- **Input**: `../mapping.csv`, with columns `old,new` (`R0111,R01_11-clause-without-comma`). It is filled by the *Names* tickets.
- **Files**: the live set in *The shape of a code*. `.scratch` tickets count only when their `Status:` line says `open`, and the script prints the list so it can be checked.
- **`inventory` mode**: lists every distinct code in the live files, with each file and line where it appears, marking the line in a chapter's check list that defines it. The *Names* tickets draft from this list.
- **`check` mode** (dry run): validates the mapping (every `new` matches `[RT]\d{2}_\d{2}-[a-z0-9-]+`, its number equals `old`'s, names are unique, names are at most 4 words), then reports codes found but not mapped, entries never used, and a count of replacements per file. Any problem fails the run.
- **`apply` mode**: runs `check`, then rewrites in place. Matching is whole-token (`\b[RT]\d{4}\b`), and the script reports anything that looks like a code but may not be one (inside a URL or a hash, for example).

Lives at `.scratch/diagnostic-codes/rename_codes.py` (Python 3, standard library only). Done when the three modes work on the test mapping and `inventory` has been run on the real files, with its output saved as `../inventory.txt`.

## Resolution

Done on 2026-11-27. [`rename_codes.py`](../rename_codes.py) works as asked, and [`inventory.txt`](../inventory.txt) holds the real inventory: **288 codes** (242 `R`, 46 `T`) in **220 live files**.

**How it works, beyond the question:**

- **Live set**: `docs/spec`, `docs/guide`, `docs/showcase`, `docs/adr`, `GLOSSARY.md`, and `.scratch/*/issues/*.md` whose `Status:` is exactly `open`. Two tickets say `Status: draft`, and they are left out like closed ones. This effort's own tickets are left out too, since they quote old codes on purpose. A file type it doesn't expect in the live set stops the run.
- **Definition line**: the first `` - `R1301` `` bullet in the code's own chapter (`docs/spec/13-…`). Chapter 27 quotes check lists and chapter 34 summarises them in a table, so those lines are ordinary uses.
- **Check by hand**: a code inside a URL is reported and left as is (this is skipped by position, so the same code elsewhere on the line is still renamed). A code that isn't a whole token (`xR0111`) and a wildcard (`R01xx`) are reported and left as is. A range (`` `R0112` to `R0115` ``, `` `T2801`–`T2803` ``) is reported, and both ends are renamed.
- **`check --partial`**: counts codes found but not mapped instead of failing, so a *Names* batch can be checked alone. `apply` refuses it.
- The mapping must start with the header `old,new`. A name over 30 characters prints a warning, and over 4 words is an error.
- Line endings are kept, and a second run finds no old code, so it can't rename anything twice.

**Tested** on a git-tracked copy of chapter 01, one case, a planted `GLOSSARY.md`, an open, a closed and an own-effort ticket, and a `docs/primer` file. A bad mapping (wrong number, a name used twice, 5 words, an uppercase name, an unused entry, a missing code) fails both `check` and `apply`, and nothing is written. A good one rewrites exactly the live files, and leaves the URL, the near-misses, the closed ticket, the own-effort ticket and the primer alone.

**Facts the inventory surfaced** (handed to later tickets):

- `R0412` is no code: it is the example in chapter 23's `Diagnostic` struct (line 181), and chapter 04's list stops at `R0408`. Until the example changes, `check` reports it as unmapped. → *Rewrite the spec text on codes*.
- Five retired codes are written only in prose, with no check-list line: `R1410` (14), `R1501`, `R1505` (15), `R2801` (28), `T2902` (29). They still need names (*The shape of a code*), and the inventory marks them `! defined in no check list`. If check lists are to be the single source of names, they need a line. → *Rewrite the spec text on codes*.
- 12 ranges are written between two codes, in the spec, the guide, the showcase and ADR 0015, listed under *Check by hand* in the inventory. With full codes they read badly. → *Rewrite the spec text on codes* decides how, *Run the migration* rewords them.
