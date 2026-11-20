# Quantities: `%`, `OF`, `COUNT`, `RANDOM` and `WEIGHT`

Type: grilling
Status: closed
Assignee: claude (with Edoardo)
Blocked by: 01

## Question

- **Percentages.** `n PERCENT OF Role` uses a unit word. `%` is free now that `#%` is retired, and the user suggests `50% OF Guest`. Decide whether it replaces `PERCENT`, and how it reads next to a computed quantity (`?share% OF Guest`, `(?n * 10)% OF …`).
- **`COUNT`** is both the Expression `COUNT(cond)` and the Instancing line `COUNT 2.`
- **`RANDOM`**: since *`BY`, `WITH`, `WITHOUT`, `AT` and `UNTIL`*, the Pick is `, RANDOMLY` (`R2606` for `AT RANDOM`), so `RANDOM` is only the function `RANDOM(a, b)`. The overload is gone; only check that the function's name still sits well beside `RANDOMLY`.
- **`WEIGHT`** goes on a Random-choice Option and on a weighted Pick. It is probably one meaning, but confirm it. Since *`AND`, `OR` and `EITHER`*, the Option is written `OPTION, WEIGHT e:` under a `RANDOMLY:` Block; a rename of `RANDOM` should check it still sits well beside `RANDOMLY`.
- **`OF`** only appears in counts. Check that it stays one meaning once `%` comes in.

Done when chapters 04, 09, 15, 21 and 26 (and 18, for the 2.0 Quota spelling that follows) are edited.

## Resolution

Grilled with the user on 2026-11-20. New ADR 0045 (`docs/adr/0045-percent-is-a-share-never-a-remainder.md`).

1. **`%` replaces `PERCENT`.** It goes between any Number Expression and `OF` (`50% OF Guest`, `?share% OF Guest`, `(?n * 10)% OF Guest`). A space before it is allowed, but the spec and tools write none. Anywhere else it is `R1517`: `50%` is never a Value, and `WEIGHT 30%` is an error because Weights are relative. `PERCENT` is the retired spelling `R1516`, and stays reserved for its hint. The 2.0 Quota follows (`FROM 50% OF Guest`).
2. **`%` is never a remainder.** The user weighed keeping it for a future modulo. Modulo has few uses in story logic, designers read `%` as percent, and a remainder, if it ever comes, will be a word (`MOD` or a function). `MOD` is not reserved now. Chapter 01 says what `%` means and chapter 04 says it isn't a remainder.
3. **`COUNT`** keeps both uses. It is one noun, "how many", in `COUNT(cond)` and in the `.regin` line `COUNT 2.`. Chapters 21 and 26 cross-reference each other.
4. **`RANDOM(a, b)`** keeps its name. It shares a root and a sense with `RANDOMLY`, so it needs no new word.
5. **`WEIGHT`** has one meaning on Options and Picks. Chapter 09 says so.
6. **`OF`** keeps one meaning, "out of this Role". `ALL Guest` stays without `OF`, and chapter 25's `ALL OF` was fixed.

Edited: chapters 01, 04, 05, 07, 09, 15, 18, 19, 21, 25, 26, 29, 33, 34, 35, 39; `GLOSSARY.md` (*Quota Trigger*); ADR 0045; case `18-quota-triggers/percent-over-a-hundred.regia`; new cases `15-roles-and-mappings/percent-is-retired.regia` and `15-roles-and-mappings/percent-only-before-of.regia`. ADR 0031 still says `PERCENT` and is left as the historical record.
