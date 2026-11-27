# Codes carry a name after their number

A Diagnostic code used to be `R` and four digits: the spec chapter, then the check's place in it. It said where its check is defined and nothing else. `R13` means Plan selection only to someone who knows the spec's table of contents, so a writer reading the first error of chapter 13 had to look the code up to learn what kind of mistake it was. Chapter 27 had kept that shape for 2.0 and put off a better one, warning that a later change would have to map every code already given. With 288 codes and the Transpiler not yet printing any, this was the cheapest time to change.

We decided that every Diagnostic and Trace code is **its number followed by a Code name**: `R01_11-clause-without-comma`, `T09_02-weight-below-zero`. The number is today's, with `_` between chapter and check, and it stays the **identity**: the Conformance runner, `#@allow` and the docs pages match on it. The name, at most four words in glossary terms, says what the mistake or event is. Names are unique across all codes and are frozen at the Regia 1.5 release, as numbers are. A code is always written whole, and a right number with a wrong name is an error: a case error in a Conformance case, and `R02_06-allow-misnames-code` in an `#@allow`.

A reviewed mapping file (`.scratch/diagnostic-codes/mapping.csv`) rewrote every code in the live docs. Closed tickets, finished maps, `docs/primer` and the `1.0` branch keep the old codes, and the mapping file is how to read them.

## Considered options

- **Names only** (`clause-without-comma`). The most readable form, but a name is harder to keep stable than a number: fixing its wording would break every reference to it. It also loses the chapter, which is how a code is found in the spec.
- **The number as the code, with the name as an alias** that tools also accept. This creates two spellings of one code, and every tool and document has to choose between them. A single whole token, matched on its number, gives the reader the name and gives tools the number.
- **An area segment instead of the chapter** (`R-SEL-01`). Readable at a glance, but areas are a second taxonomy beside the spec's chapters, and would need a mapping and a home of their own.
- **One global sequence**, numbering every check in the order it was added. Stable and short, but it says neither where a check is defined nor what it is.
- **`.` or `-` as the number's separator.** `.` breaks double-click selection and must be escaped in a regex. `-` can't be told apart from the hyphens in the name.

## Consequences

- Codes are longer. A table column headed "code" may print the number alone if the whole code proves too cramped.
- Each chapter's check list (or Trace entry list) is the only place a code is named, so every retired code has a line there.
- Ranges between two codes are no longer written: a whole list is named in words, and any other set is listed code by code.
- The Transpiler's code enum gives each code's number, name and severity. How its variants are named is the Transpiler's choice.
- Decided in the tickets *The shape of a code* and *Rewrite the spec text on codes* (`.scratch/diagnostic-codes/`).
