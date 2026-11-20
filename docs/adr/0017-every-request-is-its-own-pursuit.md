# Every request is its own Pursuit

In the first draft of 2.0 a Goal's arguments were its identity: a second request for a Goal already being pursued with the same arguments was ignored, and a waiting `PURSUE` joined the pursuit under way. We now make **every request start a Pursuit of its own**, with its own Sender, its own recipe and its own ending (spec 05). Nothing is ignored and nothing is joined. This replaces the consequence of ADR 0005 that a Goal already being pursued must be joined.

The old rule made arguments do a second job. In the showcase `bring` and `fetch` carried a seat only so that two Guests ordering roast would be two Goals, and the recipe matched the slot with a `?` and a Comment. A request that came second also lost its Sender, so `WHEN g FAILED FROM DIRECTOR` stayed silent when the Agent had started the Goal first. Which of two requests came first can't be read in the source.

## Considered Options

- **Arguments are the identity (the first draft)**: a Goal asked twice runs once without the designer doing anything. It costs the arguments added only to keep requests apart, the lost Sender, and generated code to join a running intention, since Jason starts a second one.
- **Arguments and Sender are the identity**: two Guests' orders become two Goals, but a Goal the Agent gives itself (`fetch`, under `bring`) still merges and still needs the extra argument.

## Consequences

- A Goal asked twice runs twice. One that must not says so: `GIVEN NOT PURSUING g`, where `PURSUING g` inside a recipe for `g` leaves out the recipe's own Pursuit.
- `DROP g` stops every Pursuit of `g`. There is no way to drop one of several.
- A recipe that ends with `PURSUE g, WITHOUT WAITING` for its own Goal repeats, each round a new Pursuit with no Sender. The waiting form never ends, and is a warning when unguarded (`R0806`).
- Each ending Trigger fires once per Pursuit.
- The Jason Target no longer joins intentions, and needs a way to tell Pursuits of one Goal apart for their Senders, their endings and the Trace.
