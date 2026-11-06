# Time and timers

Type: grilling
Status: open

## Question

How does Regia deal with time (Q4c)? `WAIT` exists, but there is no way to schedule things: timers, repeating Events (`digestion_check` reads like polling), timeouts on a Phase ("if no one signals within 30s"). What is in scope, and how is it written? Is time a property of the Target or of the language?

## Comments

- From *Basic Action set* (07): `WAIT` is a Basic Action, written without `DO`. Its argument, its units, and whether it takes a trailing `,` clause are this ticket's. See `docs/spec/08-basic-actions.md`.
- From *Plan failure and fallback* (11): decide whether `WAIT`, a timer or a timeout can fail a Plan, and if so add it to the causes table in `docs/spec/11-failure.md`. Every failure must leave a trace entry.
