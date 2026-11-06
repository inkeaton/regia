# FAILED notifies; it does not rescue

`WHEN g FAILED:` runs when the Goal `g` fails. By the time it runs, every Body that was waiting on `g` with `PURSUE g.` has already failed. Finishing a `FAILED` Plan doesn't count as reaching `g`, and the waiting Body doesn't carry on. Failure also never retries another `TO g` Plan by itself.

Jason works the other way: if an `-!g` plan finishes, the intention carries on after `!g` as if `g` had succeeded. For designers, that breaks the reading of a recipe as a list of steps. In `TO dinner: PURSUE find_food. DO eat_food.`, a rescue would run `eat_food` even though no food was found. Notification keeps one rule true: a Goal is reached only when its `TO` Plan finishes (chapter 05). It also mirrors `DROPPED`. Fallbacks are written explicitly, as another recipe chosen up front or a fallback Goal started from `FAILED`.

## Considered Options

- **Rescue (Jason's `-!g`)**: fallbacks that let a waiting Body continue are shorter to write, but a reader of the waiting Body can't tell whether the next line runs after success or after a handled failure.
- **Automatic retry of the next applicable `TO` Plan (JACK-style)**: this clashes with "first `GIVEN` in the text wins" (chapter 06), and it can re-run side effects that a failed attempt already caused.

## Consequences

- The ASL Target generates an `-!g` plan for every Goal. It runs the designer's `FAILED` Plans, then re-fails with `.fail`, so every level of a waiting chain fires `FAILED`.
- The reason for a failure is never visible in the language, only in the trace (`docs/spec/11-failure.md`).
