# `LET` fills a Placeholder, and `=` only compares

`=` had three jobs: comparing in a condition, filling a Placeholder in a Body (`?dmg = RANDOM(1, 6)`), and giving a `.regin` Target setting (`strategy = random`). ADR 0002 accepted the Body use because the place told the two readings apart. The syntax review's principles (chapter 01, ADR 0041) give each symbol one meaning, so we decided that `=` means **equal** and nothing else. A Body fills a Placeholder with **`LET ?dmg BE RANDOM(1, 6)`**, so `=` never appears in a Body Statement, and like every other Statement, this one now starts with a keyword. Target settings are written `strategy random`, the key-then-value shape of `SEED 42` and `COUNT 2` "Not equal" gets its own operator, **`?a != ?b`**, so the negation sits where the operator goes. `NOT ?a = ?b` stays legal, since `NOT` applies to any condition, but the spec and the tools write `!=`.

## Considered options

- **`LET ?x = e`**: one new word, and `=` reads "equals" as in "let x = 3". Rejected because `=` would still appear where a value is filled.
- **`?x IS e`**: no head keyword, and `IS` reads like a condition, so the overload just moves to another word.
- **ADR 0002's objection to `LET … BE`** ("reads like programming") was outweighed by `=` having two meanings, and by the Body Statement being the only one with no head keyword.
- **Target settings with `:`** (`strategy: random`): `:` is the one-line spelling of an indent (chapter 01), so this would read as a Block. With `LET strategy BE random`, `LET` would mean both "fill once" and "an overridable setting".
- **Not equal as `?a NOT = ?b`**: `NOT` would need a second position, and only for `=`. **`<>`** is obscure, **`≠`** can't be typed, and a keyword (`ISNT`) adds a word. Keeping only `NOT ?a = ?b` puts the negation away from the operator, where a reader may take it as `(NOT ?a) = ?b`.

## Consequences

- This amends ADR 0002's spelling. Its decision stands: Placeholders are filled by computed values only in the Body.
- `LET` and `BE` are reserved (chapter 04). The retired spellings are errors with a hint: `?x = e` (`R04_07-retired-equals-statement`), and `key = value` in a `TARGET` group (`R21_24-retired-equals-setting`). `LET` in a condition is `R04_08-let-in-condition`.
- "Naming a value" is no longer the name of the concept, because a **Name** is a declared word. The spec says a `LET` Statement **fills** a Placeholder.
- In Regia 1.5.
