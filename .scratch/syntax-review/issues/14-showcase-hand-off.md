# The hand-off to the showcase

Type: grilling
Status: closed
Assignee: claude (with Edoardo)
Blocked by: 12

## Question

Updating the 1.5 showcase (`docs/showcase/`) and its reference Build is a later effort, out of this map's scope. Decide what this map hands it: whether it needs a written list of old and new spellings, and where that list lives (a *Since the 1.5 syntax review* section in the spec, a file next to the showcase, the map itself, or nothing beyond the ADRs). Done when the chosen list exists, or the map records that none is needed.

## Known items

Carried over from the map's *Not yet specified* note: the showcase relies on new lines rather than trailing dots (its "house style writes it" note goes), the *Flat blocks* row of `docs/showcase/README.md` goes, an Option that does nothing holds `PASS`, `?x = e.` becomes `LET ?x BE e.`, `NOT ?a = ?b` becomes `?a != ?b`, and `TARGET` settings drop their `=`. From *`TO` and `FROM` outside Triggers*: `CHANGE f TO f2` → `UPDATE f TO f2`, `TRANSITION TO p` → `ENTER p`, `MAPPING a TO b` → `MAPPING a AS b`, `UNASSIGN`/`UNASSIGNED` → `REMOVE`/`REMOVED`. From *`AND`, `OR` and `EITHER`*: `EITHER:` / `OR:` → `RANDOMLY:` with `OPTION:` Blocks (one more indent), and `AND` in `SUITS`/`SHIFTS`/`SHIFT`/`PLAYS` lists → `,`. From *`BY`, `WITH`, `WITHOUT`, `AT` and `UNTIL`*: `, AT RANDOM` → `, RANDOMLY`, `WHEN EXITED BY PARENT:` → `WHEN EXITED, BY PARENT:`. From *Quantities*: `n PERCENT OF Role` → `n% OF Role`. From *Setups and `ROLE`*: `ROLE X STARTS WITH:` → `ROLE X:`, `CAST STARTS WITH:` → `CAST:`. From *Endings and kind words*: `WHEN P ENDED WITH e` → `WHEN P FINISHED WITH e`, `WHEN P ENDED WITHOUT OUTCOME` → a plain `WHEN P FINISHED` after the `WITH` Plans, `END SUBPLOT P` → `DROP SUBPLOT P`.

Since *Retired spellings and their codes*: chapter 01 has a *Retired spellings* table (old spelling, replacement, code) covering every rename above that is an error. Not in it, because they aren't errors: trailing `.`, `PASS` in an empty Option, `NOT ?a = ?b` → `?a != ?b`, and `WHEN EXITED BY PARENT:` (which is `R0111`, a missing comma).

## Resolution

Agreed with Edoardo on 2026-11-20.

- **The renames: chapter 01's *Retired spellings* table, and nothing else.** It is normative, stays in the spec for ever, and lists every rename above that is an error, with the code that names the new spelling. No copy goes into a separate file or a *Since the 1.5 syntax review* section: two lists would drift. There is no 1.5 Transpiler in the repo yet, so the showcase effort reads its files against the table instead of building them.
- **The changes that aren't errors live here**, in this resolution, which the map's *Out of scope* line on the showcase links to. Neither the spec (no migration notes for one body of text) nor `docs/showcase/` (it is derived from the spec, and a migration file would be stale content there) holds them. They are:
  - trailing `.` is silent: the showcase relies on new lines, and the README's *Redundant terminators* row ("house style writes it") goes;
  - the *Flat blocks* row of the README goes (Flat blocks are removed; `R0107` retired, a stray `;` is `R0108`);
  - an Option of a Random choice that does nothing holds `PASS`;
  - `NOT ?a = ?b` becomes `?a != ?b`;
  - a clause keyword written without its `,` (`WHEN EXITED BY PARENT:`, `WHEN e FROM DIRECTOR:`) is `R0111`, a missing comma, not a retired spelling;
  - `%` is allowed only before `OF` (`R1517`).
- **The showcase's own prose** (the README's "Naming a value", "the one dotted Action", `CHANGE`, `UNASSIGNED` in the Playbooks table, and the like) is checked against `GLOSSARY.md`, which records the retired terms ("naming" → "fill"). The rewording is the showcase effort's work, so it is not listed term by term here.
- No ADR: a hand-off note, easy to reverse, with no real trade-off behind it.
- **Files changed:** none beyond the map.
