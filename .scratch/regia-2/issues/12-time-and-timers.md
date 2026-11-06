# Time and timers

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo

## Question

How does Regia deal with time (Q4c)? `WAIT` exists, but there is no way to schedule things: timers, repeating Events (`digestion_check` reads like polling), timeouts on a Phase ("if no one signals within 30s"). What is in scope, and how is it written? Is time a property of the Target or of the language?

## Answer

Spec chapter: `docs/spec/12-time.md`. Glossary: *Duration* added, *Basic Action* updated. Specs 07, 08 and 11 updated to match.

- **The clock belongs to the Target.** The language fixes Durations; the Target decides whether they are wall-clock or game time (pausing, time scale). One Program uses one clock. Time-of-day Facts are ordinary External Facts.
- **Durations** are `<Expression> SECONDS` / `MINUTES` (singular accepted, interchangeable). The unit is always written; no `3s`, no milliseconds (use fractions).
- **2.0 has only `WAIT <Duration>.`** It pauses only its own Body; the Agent keeps reacting, and a waiting recipe's Goal is still being pursued. `WAIT 0` carries on at once.
- **Failure:** a non-Number Duration fails the Plan (added to spec 11's causes table). A negative one counts as 0 with a runtime warning in the trace (like Weights), plus a Transpiler warning for a negative literal. A Plan stopped during a `WAIT` just stops; the wait isn't a failure of its own.
- **Out of scope for 2.0:** repeating Triggers (`EVERY`), delayed Triggers (`AFTER`, Phase timeouts) and timeout clauses (`WITHIN`). Repeating Events like `digestion_check` stay External Events the game sends.
- **Handed off:** whether Director Plans can use `WAIT` to *Director capabilities*; how a Target picks its clock to *Supporting multiple Targets*.

## Comments

- From *Basic Action set* (07): `WAIT` is a Basic Action, written without `DO`. Its argument, its units, and whether it takes a trailing `,` clause are this ticket's. See `docs/spec/08-basic-actions.md`.
- From *Plan failure and fallback* (11): decide whether `WAIT`, a timer or a timeout can fail a Plan, and if so add it to the causes table in `docs/spec/11-failure.md`. Every failure must leave a trace entry.
