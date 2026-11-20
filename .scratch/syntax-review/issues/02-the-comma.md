# The comma

Type: grilling
Status: closed
Assignee: claude (with Edoardo)
Blocked by: 01

## Question

Apply the comma rule from *The principles of the 1.5 syntax* to every place `,` appears (inventory §1, and the six or more jobs listed there):

- **Optional parts of a Trigger:** `FROM` (the user's example, `WHEN e, FROM DIRECTOR:`), the kind word's `WITH`, the Labels, the inline Context `WHEN x, GIVEN …:`, which is used at `03-parameters-and-placeholders.md:60` and `15-…:301,320,328,330` and specified nowhere. Specify it or remove it.
- **Optional parts of a Statement:** `, WITHOUT WAITING`, `, MAPPING`, `, UNTIL EXITED`, `WAIT d, UNTIL c`, and Picks on `GIVEN` and `IF`.
- **Lists:** arguments, Multi-definition, the `EXCEPT` list and how it ends when a clause follows (`, MAPPING`), `LIKE a, b`, `#@allow`.
- **The comma used as AND in a Context**, `GIVEN gold(?g), price(?item, ?p):` at `11-failure.md:61`. Fix the example, or make it a rule.
- **Continuation lines,** and the stale example in chapter 01.

For each one, say whether the comma stays, goes, or is added, and what the parser needs to tell a list from a clause. Done when chapters 01, 05, 06, 08, 14, 15 and 26 (and any others affected) are edited, along with the 2.0 forms that follow (`FROM … OR`, `BY`).

## Resolution

Grilled with the user on 2026-11-19. Applies ADR 0041; no new ADR.

1. **`FROM` and `BY` on a Trigger are clauses**: `TO find_sword, FROM DIRECTOR:`, `WHEN e LEARNED, FROM ?t, SUITS …:`, `WHEN g FAILED WITH r, BY waiter ?s:`, and the 2.0 forms `, FROM a OR b` and `, FROM 3 OF Guest`. The kind word and `FAILED WITH r` stay core. Chapter 05's *Order of a Trigger* became *The shape of a Trigger* (core, then clauses in any order; tools write `FROM`/`BY` before Labels). Every Trigger in the spec, the Jason chapters' tables and the Conformance cases was rewritten.
2. **The inline Context `WHEN x, GIVEN c:` is removed.** It would give `GIVEN` a second job, and it is a second spelling of the nested `GIVEN` Block. The five uses (chapters 03 and 15) became nested Blocks; chapter 05 says it's a parse error.
3. **`,` never means AND.** Chapter 11's `GIVEN gold(?g), price(…)` became `AND`; chapter 01 states the rule.
4. **`WAIT UNTIL c` and `WAIT d, UNTIL c` both stay**: the same word introduces the required item (core) or a limit (clause). Chapter 01 states it.
5. **`KIND` and `AGENT` in `.regin`**: `LIKE` and `PLAYS` are clauses, `KIND drunk_noble, LIKE noble, PLAYS Guest AND Drunkard:`. The `AND` between Roles is left to *`AND`, `OR` and `EITHER`*.
6. **Lists stay** (arguments, Multi-definition, `EXCEPT`, `LIKE`, `#@allow`). A list ends at a clause keyword after `,`, or at the first word that can't be an item (chapter 01 in general, chapter 15 for `EXCEPT`). Statement clauses already in shape (`, WITHOUT WAITING`, `, MAPPING`, `, UNTIL EXITED`, Picks on `GIVEN` and `IF`, `, WEIGHT`) are unchanged.
7. **`R0111`** (chapter 01, in 1.5): a clause keyword after the core with no `,`, hint adds it. One code for every clause, so later tickets reuse it. New case `docs/spec/cases/01-statements-and-blocks/clause-without-its-comma.regia`.

Edited: chapters 01, 03, 05, 06, 07, 08, 10, 11, 14, 15, 16, 17, 18, 20, 21, 25, 29, 30, 33, 38, 39, and the cases of 01, 07, 11, 15, 18, 19, 21.
