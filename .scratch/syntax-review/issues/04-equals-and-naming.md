# `=` and naming a value

Type: grilling
Status: closed
Assignee: claude (with Edoardo)
Blocked by: 01

## Question

`=` means equality in a condition, naming a value in a Body (`?dmg = RANDOM(1, 6).`), and a Target setting in `.regin` (`strategy = random.`). The user wants `=` to mean equality only, with a keyword for naming.

- Which keyword names a value (for instance `LET ?dmg BE …`, `?dmg IS …`, `SET …`), and does it read well in an Option on one line (`EITHER: <name> ?stake …`) and in a Body?
- Does the same keyword, or a different one, write `.regin` Target settings, which aren't Placeholders?
- Does "not equal" stay `NOT a = b`, now that `=` has one meaning?
- What happens to the "already filled is an error" rule (`R0405`) and its message?

Done when chapters 04, 09, 21 and 26 and the examples that name values are edited, and `GLOSSARY.md` has the new word if it names a concept.

## Resolution

Grilled with the user on 2026-11-20. ADR 0042 (`docs/adr/0042-let-fills-a-placeholder-and-equals-only-compares.md`), amending ADR 0002's spelling.

1. **Filling a Placeholder in a Body:** `LET ?dmg BE RANDOM(1, 6).` (the user chose it over `LET ?x = e.` so that `=` never appears in a Body). `LET` and `BE` are reserved. One line in an Option: `EITHER: LET ?stake BE ?gold / 2.`
2. **The concept:** "naming a value" is dropped, because it clashes with **Name**/`NAME`. A **`LET` Statement fills** a Placeholder. `GLOSSARY.md` *Placeholder* now lists naming under *Avoid*; no new term.
3. **`.regin` Target settings:** `key value.` (`strategy most_similar.`), the shape of `SEED 42.`. `:` was ruled out because it is the one-line spelling of an indent, and `LET` because a setting is overridable. The retired `key = value.` is `R2124`.
4. **Not equal:** `?a != ?b` (the user chose it over `?a NOT = ?b`, `<>`, `≠` and a keyword), so the negation sits in the operator's position. It works on any Value, at the precedence of `=`, and doesn't chain (`R0403`) or fill (`R0404`). `NOT ?a = ?b` stays legal (`NOT` applies to any condition) with no diagnostic; the spec and the tools write `!=`.
5. **Checks:** `R0405` reworded for `LET`; `R0407` for the retired `?x = e.` (hint `LET ?x BE e.`); `R0408` for `LET` in a Context or an `IF` condition; `R1711`'s example respelled.

Edited: chapters 03, 04 (with a *Reserved words* section), 09, 15 (the `NOT ?x = …` examples now use `!=`), 17, 21, 26 and 39 (the Jason mapping of `LET` and `!=`); the case `cases/04-numbers-and-expressions/naming-a-filled-placeholder.regia`; `GLOSSARY.md`; ADRs 0001 and 0002 (pointers to 0042).
