# `BY` keeps the amount of a shift, and `RANDOMLY` has two jobs

The syntax review's one-meaning rule (chapter 01, ADR 0041) allows a keyword one gloss and one structural job. Two words failed it, and we kept both on purpose, as closed exceptions next to ADR 0043's `TO`:

- **`BY` has two senses.** It names who did it (`WHEN EXITED, BY PARENT:`, and in 2.0 `WHEN g REACHED, BY waiter ?s:`), and it gives an amount in `SHIFT anger BY 0.1` and the Label `SHIFTS anger BY 0.1`. Who-did-it is the main sense: every `BY` but the shift's uses it. The shift keeps `BY` because "shift by 0.1" is the idiom, and every other spelling read worse.
- **`RANDOMLY` has two jobs.** It is the head of a Random choice (`RANDOMLY:` with `OPTION:` Blocks, chapter 09) and the Pick clause `, RANDOMLY` (chapter 26), which replaced `, AT RANDOM`. The sense is the same in both, "chosen by chance", among Options or among Matches. One word is easier to learn than two for the same idea.

## Considered options

- **The amount without a word**: `SHIFT anger 0.1, sympathy -0.2`. It keeps the rule whole, but a bare number after a name reads worse, and worse still next to `SUITS anger AT 0.5` in a Label.
- **Another word for the amount** (`PLUS`, `UP`/`DOWN`, `+=`): none read as well, and `UP`/`DOWN` can't take a signed Expression.
- **Another word for who did it**: "reached by the waiter" and "exited by the parent" are the English passive, and no other word reads as well.
- **`AT RANDOM` kept as a fixed phrase**: chapter 01 gives fixed phrases no exemption, and `AT` introduces a level elsewhere (`SUITS p AT n`, `bravery AT 0.3`).
- **`, ANY` for the random Pick**: it reads like the default, which already uses one Match and doesn't say which.

## Consequences

- Chapter 01's list of exceptions names `TO` (ADR 0043), `BY` as an amount and `RANDOMLY`. The list is closed: no other construct may cite them as a precedent.
- `EXITED BY PARENT` became the clause `WHEN EXITED, BY PARENT:`, like the `BY` of a Goal's ending. The old spelling is `R01_11-clause-without-comma`, and `R05_06-by-on-wrong-trigger` lost its exception: `BY PARENT` goes only on `EXITED`.
- `, AT RANDOM` is the retired spelling `R26_06-retired-at-random` (hint: `, RANDOMLY`). `RANDOM` is now only the function `RANDOM(a, b)`, which `bravery AT RANDOM(a, b)` in Instancing still uses.
- In Regia 1.5, and the same spellings in 2.0.
