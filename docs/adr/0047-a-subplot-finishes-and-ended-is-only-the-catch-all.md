# A Subplot finishes, and `ENDED` is only the catch-all

ADR 0030 made a Subplot's endings heard like a Goal's: a specific Trigger first, then plain `ENDED`. It spelled the specific Triggers `ENDED WITH e` and `ENDED WITHOUT OUTCOME`, so `ENDED` had two jobs. With a complement it meant "ended by itself", and plain it meant "ended any way, after the specific Trigger". Adding `WITH e` changed who caused the ending as well as which Outcome matched. `ENDED WITHOUT OUTCOME`, read as English, also covered a drop, which carries no Outcome but never fired it. A plain `ENDED` also fired after `ENDED WITH`, while a plain `FAILED` competes with `FAILED WITH` in written order, so a reader who knew one couldn't predict the other. Under chapter 01's one-meaning rule, `ENDED` failed.

A Subplot that ends by itself now fires **`FINISHED`**. It is the Subplot's counterpart of a Goal's `REACHED` and `FAILED`: a Subplot has no success or failure, and its Outcome says how it went. `FINISHED WITH e` and a plain `FINISHED` share a Trigger and are tried in written order, first match wins, exactly as `FAILED WITH r` and plain `FAILED` are. `ENDED` is only "over, however it went". It never takes a complement and always fires after the specific Trigger, for a Goal and a Subplot alike. `DROPPED` keeps its one meaning for both: stopped on purpose by whoever started it.

`WITHOUT OUTCOME` is retired. A plain `FINISHED`, written after the `FINISHED WITH` Plans, hears a bare `END PLOT` and any Outcome they didn't match, as a plain `FAILED` hears a Failure with no Reason.

`END SUBPLOT P` became **`DROP SUBPLOT P`**. It fires `DROPPED`, as `DROP g` does, and is the opposite of `START SUBPLOT`. `END` is left only in `END PLOT`, a Staging's own ending.

## Considered options

- **Keep `ENDED` for "ended by itself" and rename the catch-all** (`WHEN g OVER:`). `END PLOT` and `ENDED` would stay paired, but every Goal's `ENDED` would change, and the new word isn't a participle like the other kind words.
- **Leave both jobs to `ENDED`** as a closed exception in chapter 01. Nothing is renamed, but the overlap of `WITHOUT OUTCOME` with a drop stays, and so do the two orders.
- **`CONCLUDED`** instead of `FINISHED`. Same shape, heavier word.
- **Keep `FINISHED WITHOUT OUTCOME`** to match exactly a bare ending. It means more syntax, and has no counterpart on Goals: nobody has asked to single out a Failure with no Reason.
- **A bare `DROP P` for a Plot.** It parses, and the name's kind tells a Plot from a Goal, but a Director's `DROP` would then take either kind. `SUBPLOT` mirrors `START SUBPLOT`.

## Consequences

- `END PLOT` fires `FINISHED`, not a word of its own: the Action and its Trigger no longer share a word, unlike `DROP`/`DROPPED`.
- The retired `ENDED WITH e`, `ENDED WITHOUT OUTCOME` and `ENDED` with any complement are `R17_15-retired-ended-with`. The retired `END SUBPLOT` is `R17_17-retired-end-subplot`. A bare `DROP P` on a Plot is `R08_02-wrong-kind-for-action`, with the hint `DROP SUBPLOT P`. `OUTCOME` stays reserved for `R17_15-retired-ended-with`'s hint.
- A plain `FINISHED` above a `FINISHED WITH` it shadows is a warning (`R17_16-shadowed-finished-with`), as `R11_06-shadowed-failed-with` is for `FAILED`. `R17_06-unknown-subplot-outcome` keeps only the unknown Outcome, and `R17_08-unheard-subplot-ending` counts a plain `FINISHED` as hearing every ending the Subplot chose itself.
- In Jason, `ENDED WITH` and `ENDED WITHOUT OUTCOME` become one generated goal, `regia_subplot_finished(p, Args, O, Heard)`, with `O` being `none` for a bare ending (chapter 31). The Trace writes `FINISHED WITH o` and `FINISHED` (chapter 34).
- ADR 0030 still says `ENDED WITH`, `ENDED WITHOUT OUTCOME` and `END SUBPLOT`, and is left as the historical record. Its decision, a specific Trigger first and then `ENDED`, stands.
