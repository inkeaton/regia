# Map: Readable Diagnostic and Trace codes

Label: wayfinder:map

## Destination

Every Diagnostic code and Trace code has the shape `R01_11-clause-without-comma`: today's number with a separator, plus a short name. Chapters 27, 34 and 23, the glossary and an ADR say so. A script driven by one reviewed mapping file has rewritten every code in the live docs and open tickets.

Charted with the user on 2026-11-27.

## Notes

- **This map carries execution.** The *Names* tickets fill `mapping.csv`, and *Run the migration* applies it. Nothing is renamed by hand: every substitution goes through `rename_codes.py`, so no name is invented and no code is missed.
- **Names are drafted by Claude and settled by the user**, one batch per ticket, following the rules in *The shape of a code* and the patterns *Names: chapters 01–05* sets.
- Files here: `mapping.csv` (old to new, the frozen record after the migration), `inventory.txt` (every code in the live files and where it appears), and `rename_codes.py`.
- Tickets: `.scratch/diagnostic-codes/issues/NN-<slug>.md`, with `Type:`, `Status:`, `Assignee:` and `Blocked by:` lines. The frontier is the open, unblocked, unclaimed tickets, lowest number first. The *Names* tickets after the first one can run in parallel.
- Skills: `grilling` and `domain-modeling` for the *Names* tickets and *Rewrite the spec text on codes*. Prose follows `docs/standards/docs.md`, with `humanizer:humanizer` on new spec prose.

## Decisions so far

<!-- one line per resolved ticket: [title](issues/NN-slug.md): gist -->

- [The shape of a code](issues/01-the-shape-of-a-code.md): `<R|T><chapter>_<index>-<kebab-name>`. Numbers are unchanged and stay the identity. The name says what the mistake is, is unique and at most 4 words, and freezes at the 1.5 release. The full code is written everywhere in live docs. A failing-safe script applies one reviewed mapping to the spec, guide, showcase, glossary, ADRs and open tickets.
- [Write the migration script](issues/02-write-the-migration-script.md): `rename_codes.py` works (`inventory`, `check`, `check --partial` for one batch, `apply`). There are 288 codes in 220 live files. It found a fake example code in chapter 23, five retired codes with no check-list line, and 12 code ranges, all handed to *Rewrite the spec text on codes*.
- [Names: chapters 01–05](issues/03-names-r01-r05.md): 52 rows in `mapping.csv`. Sets the patterns: `retired-<spelling>`, no warning marker, the recurring words (`without`, `as`, `in`, `on`, `stray`, `undeclared`, `wrong`), broad names over splitting a code, no version numbers in names. `R0412` stays unmapped.
- [Names: chapters 06–10](issues/04-names-r06-r10.md): 41 rows in `mapping.csv`. `R1004` is `name-out-of-scope` (beside `R0310`'s `undeclared-name`), parallel checks get parallel names, and `R0501`/`R1005` no longer overlap: the spec gives kind to `R0501` alone.
- [Names: chapters 11–15](issues/05-names-r11-r15.md): 52 rows in `mapping.csv`. Adds `misused-<construct>` and `-or-` names for lines with several mistakes, and `R15_01-role-name-as-value` next to `R0303`. Case slugs give way when they name an outcome. The 4-word limit is hard: `out-of-range` counts as 3 words.
- [Names: chapters 16–20](issues/06-names-r16-r20.md): 52 rows in `mapping.csv`. Adds `X-never-Y` for absence checks, `ignored-X` and `unheard-X` for warnings, and mirrored names for mirrored checks. Adds a *Cast change* glossary entry. `non-role` counts as 2 words.
- [Names: chapters 21–38](issues/07-names-r21-r38.md): 44 rows in `mapping.csv`. Uses "Instancing file" over `.regin`, mirrored names for mirrored checks (`conflicting-sibling-files` / `conflicting-bases`), `X-never-Y` and `unheard-X` for chapter 38's absence checks, and `R26_05-maybe-unfilled-pick-weight` beside chapter 09's `maybe-unfilled-weight`. 47 codes left: the Trace codes and `R0412`.
- [Names: Trace codes](issues/08-names-trace-codes.md): 46 rows in `mapping.csv`. Runtime patterns `X-not-number`, `X-below-zero` (since `negative-duration` is `R12_03`'s) and `X-found-no-plan` for the `unheard` entries. Leaving names come from the glossary (`message-after-leaving`, `giving-outside-cast`), and T1902 is `join-refused` (the glossary avoids "spawn"). Only `R0412` is left unmapped.

- [Rewrite the spec text on codes](issues/09-rewrite-the-spec-text-on-codes.md): chapters 27, 34, 23, 02, the guide, the glossary (*Code name*) and ADR 0051 describe the shape. Every retired code has a check-list line, ranges are written as words or lists, a wrong name is a case error in a case and the new `R0206` in an `#@allow`. `R0412` is gone; 288 codes, all mapped.
- [Run the migration](issues/10-run-the-migration.md): 1790 codes rewritten in 151 live files, none left in the old shape. The 12 ranges are reworded (whole lists in words, the rest listed code by code). Transpiler checks clean. `mapping.csv` is the frozen record.

## Not yet specified

Nothing. The destination is reached.

## Out of scope

- **Codes in the Transpiler** (a `Code` type, the registry, printing): this map ends with the spec. The Transpiler implements whatever the spec says, through its own map (see `.scratch/transpiler/issues/04-diagnostics.md`).
- **Docs pages per code** (chapter 27, "each code has a docs page"): the shape makes them possible, but writing them is separate work.
- **Renaming Conformance case files** to match the new names (for example `naming-a-filled-placeholder.regia`, whose slug breaks the glossary): the migration rewrites codes inside files only. Ruled out in [Names: chapters 01–05](issues/03-names-r01-r05.md).
- **Rewriting history**: closed and resolved tickets, finished maps, `docs/primer` and the `1.0` branch keep the old codes. `mapping.csv` is how to read them.
