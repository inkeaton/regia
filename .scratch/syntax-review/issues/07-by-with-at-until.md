# `BY`, `WITH`, `WITHOUT`, `AT` and `UNTIL`

Type: grilling
Status: closed
Assignee: claude (with Edoardo)
Blocked by: 01, 02

## Question

These are the small clause words, each with several jobs (inventory §3):

- `BY`: the amount in `SHIFT m BY n` and `SHIFTS`, `EXITED BY PARENT`, and in 2.0 who pursued an asked Goal.
- `WITH`: a Reason (`FAIL WITH`, `FAILED WITH`), an Outcome (`END PLOT WITH`, `ENDED WITH`), a setup header (`STARTS WITH:`). `WITHOUT`: `WITHOUT OUTCOME`, `WITHOUT WAITING`.
- `AT`: the target of `SUITS p AT n`, the Pick `AT RANDOM`, a starting value in Instancing (`bravery AT 0.3`).
- `UNTIL`: `WAIT … UNTIL c` and the clause `UNTIL EXITED`.

For each word, decide which uses keep it and what the others become. The Reason/Outcome asymmetry (`WITH` on `FAILED` for Goals, on `ENDED` for Subplots) is in *Endings and kind words*. Here the question is only the word. Done when chapters 05, 08, 11, 12, 14, 15, 16, 17, 20, 21 and 26 are edited as each decision needs.

## Resolution

Grilled with the user on 2026-11-20. New ADR 0044 (`docs/adr/0044-by-keeps-the-amount-and-randomly-has-two-jobs.md`).

1. **`BY` names who did it**: `WHEN EXITED, BY PARENT:` and, in 2.0, `, BY waiter ?s` on a Goal's ending. `EXITED BY PARENT` became a clause, so its old spelling is `R0111` and `R0506` lost its exception (`BY PARENT` goes only on `EXITED`). **The amount in `SHIFT m BY n` / `SHIFTS m BY n` keeps `BY`** as a closed exception, because the user finds it more readable. Chapter 01 now lists the closed exceptions: `TO` (ADR 0043), `BY` as an amount, `RANDOMLY`.
2. **`WITH`** keeps the Reason and the Outcome, which share the gloss "the Cue an ending carries". `STARTS WITH:` fails the test, and its new spelling is left to *Setups and `ROLE`* so the header is renamed only once. Chapter 16 notes it.
3. **`WITHOUT`** stays in `WITHOUT OUTCOME` and `, WITHOUT WAITING` (both mean "lacking"; core or clause is allowed, as for `UNTIL`).
4. **`AT`** keeps only a level (`SUITS p AT n`, `bravery AT 0.3`). The Pick `, AT RANDOM` became **`, RANDOMLY`**, the same word as the Random choice, a closed exception to "one job" (head keyword vs clause keyword) that the user accepted. Retired spelling `R2606`. `RANDOM` is now only the function `RANDOM(a, b)`, reserved in chapter 04.
5. **`UNTIL`** stays in `WAIT … UNTIL c` and `, UNTIL EXITED` (both mean "lasting until").

Edited: chapters 01, 03, 04, 05, 09, 11, 14, 15, 16, 17, 18, 20, 25, 26, 30, 31, 34, 39; `GLOSSARY.md` (*Pick*); ADR 0044; cases `26-match-selection/pick-on-for-each.regia` and the new `26-match-selection/at-random-is-retired.regia`. Chapters 08, 12 and 21 needed no change. ADR 0030 still says `EXITED BY PARENT`, and is left as the historical record.
