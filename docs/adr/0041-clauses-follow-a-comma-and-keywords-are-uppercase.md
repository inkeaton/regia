# Clauses follow a comma, and keywords are uppercase

Regia's `,` had at least six jobs (continuing a line, separating arguments, Multi-definition items and `EXCEPT` lists, starting a Label or Pick, opening an inline Context), and some optional parts of a header took one while others didn't (`WHEN e FROM DIRECTOR, SUITS …:`). We decided that `,` means one thing: **something more follows**, either the next item of a list or a **Clause**. A Clause is an optional part that applies to a whole header or Statement, and it is always written `, KEYWORD …` after the core. So the Sender becomes `WHEN e, FROM DIRECTOR:`. A complement that finishes a single word (`FAILED WITH r`, `SHIFT m BY n`) takes no comma. The parser tells a Clause from a list item by the token after the `,`, so no list item may start with a Clause keyword. Clauses may come in any order, and tools write them in the order their chapter lists them.

In the same ticket we fixed what a keyword is. Keywords are UPPERCASE and case-sensitive, and every keyword is reserved: a name spelled exactly like one is an error (`R0110`), while `count` or `Wait` stays an ordinary name. Without this rule, adding a keyword would silently take a name away from writers. The rule lets later renames add words freely.

## Considered options

- **No comma before the Sender** (`WHEN e FROM DIRECTOR:`, as before): it reads naturally, but a reader can't tell which parts of a header are optional, and the comma's meaning depends on which clause follows it.
- **A fixed Clause order**: easier to read in a diff, but every Clause already starts with its own keyword, so a fixed order only adds errors. Tools give a canonical order instead.
- **Case-insensitive keywords**: they would forbid common names such as `count`, `wait` and `random` in any case.

## Consequences

- Every chapter that writes a Clause without a comma (chapter 05's `FROM`, among others) is brought in line by the syntax review's ticket *The comma* (`.scratch/syntax-review/issues/02-the-comma.md`). Until then, chapter 01 decides.
- The per-chapter *Reserved words* lists become one list in chapter 01 once the review's renames are done.
- Amended by ADR 0043 (`0043-to-introduces-a-goal-with-two-closed-exceptions.md`): `ASSIGN P TO Role` and `UPDATE f TO f2` are the only exceptions to the one-meaning rule, kept for the English idiom. The list is closed.
- In Regia 1.5.
