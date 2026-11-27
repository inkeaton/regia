# Rewrite the spec text on codes

Type: grilling
Status: closed
Assignee: claude
Blocked by: 01

## Question

How does the spec describe the new shape, and what ADR records the switch? The text is drafted with the user, and the examples use names already settled in the batches, or `R01_11-clause-without-comma`.

- Chapter 27, *Diagnostic codes*: the new shape and its rules (the number is the identity, names unique, names frozen at the 1.5 release). The paragraph "This shape is kept for 2.0… deferred past 2.0" goes. Also how a case's `#! error` and `#! rule:` lines write a code, and what the runner does with a wrong name.
- Chapter 34, *Trace codes*: the same shape for `T`.
- Chapter 23: the Diagnostic's `code` field. Does it carry the full code, or the number with the name in a field of its own? How does the Transpiler print it?
- `GLOSSARY.md`: *Diagnostic code* and *Trace code*, perhaps with a term for the name part.
- **Facts from *Write the migration script*** (see its resolution):
  - Chapter 23's example code `R0412` is not a real code. It changes to a settled one, or `check` keeps failing on it.
  - Five retired codes have no check-list line, only prose: `R1410`, `R1501`, `R1505`, `R2801`, `T2902`. Does every retired code get a line in its chapter's list (as `R0107` has), so the list is the single source of its name?
  - 12 places write a range between two codes (`` `R1801` to `R1806` ``, `` `T2801`–`T2803` ``), listed under *Check by hand* in `../inventory.txt`. How is a range written once codes carry names: the bare numbers, a list, or "chapter 18's checks"?
- An ADR: names on top of numbers. Options considered: names only, number as canonical with the name as an alias, an area segment, a global sequence.

Write only the text about codes here. The codes themselves are rewritten by *Run the migration*.

## Resolution

Decided with the user on 2026-11-27. The new text writes example codes in their new shape (`R01_11-clause-without-comma`), and every other code in the old shape, so *Run the migration* renames them with the rest.

**Decisions**

1. Chapter 23's example `R0412` becomes `R1301` (so `R13_01-precedence-cycle` after the migration).
2. A Diagnostic's `code` field carries the whole code, printed `error[R01_11-clause-without-comma]`. The spec says the enum gives each code's number, name and severity, and leaves its variant names to the Transpiler (no `Code::R0307` example).
3. Every retired code has a line in its chapter's list. Added: `R1410` (14), `R1501`, `R1505` (15), `R2801` (28, whose section now says its one check is retired), `T2902` (29). The prose sentences that mention them stay.
4. No ranges. A set that makes up a whole list is named in words; any other set is listed code by code. *Run the migration* rewords the 12 ranges under *Check by hand*.
5. Cases write the whole code in `#! error`, `#! warning`, `rule:` and `.trace` files. A missing or wrong name is a **case error**.
6. `#@allow` takes the whole code, matched on its number. A missing or wrong name is the new error **`R0206`** (mapped to `R02_06-allow-misnames-code`, following `R02_04-allow-names-error`), with a quick fix. An unknown number stays `R0205`.
7. New glossary term **Code name** (avoid: slug, alias, short name). *Diagnostic code* and *Trace code* redefined.

**Written**

- Chapter 27, *Diagnostic codes*: the three parts, the token regex, the number as identity, unique names, names frozen at the 1.5 release, no status in a name, the check list as the only source of names, no ranges. "Deferred past 2.0" is gone. *Annotations*: *Codes in annotations*.
- Chapter 34, *Trace codes*: the same shape with `T`, and the `.trace` case error.
- Chapter 23: the `code` comment, the enum, how a code is printed.
- Chapter 02: the `#@allow` rule and `R0206`, with the case `cases/02-comments/allow-with-a-misnamed-code.regia`.
- Guide: `02-syntax.md` (`#@allow`, the shape), `18-the-trace.md`, `19-the-transpiler.md` (*Diagnostic codes*, the `R0206` check).
- `GLOSSARY.md`, and [ADR 0051](../../../docs/adr/0051-codes-carry-a-name-after-their-number.md) *Codes carry a name after their number*. It writes no old-shape code apart from `R0206`, so the migration leaves its history alone.
- `mapping.csv`: the `R0206` row. `inventory.txt` regenerated: 288 codes, every one with a definition line, none unmapped. `check` is clean.
