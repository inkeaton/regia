# PURSUE waits; ASK does not

`PURSUE g.` gives the Agent a Goal and waits until it is reached before the Body goes on. Carrying on at once is written with a trailing clause: `PURSUE g, WITHOUT WAITING.` `ASK <recipient> TO g.`, which gives a Goal to another Agent, never waits.

Designers read a Body as a list of steps, each one finished before the next starts, as `DO` already behaves. A recipe like `PURSUE find_food. DO eat_food.` only reads correctly if the first line finishes first. 1.0's `ACHIEVE` already compiled to Jason's waiting `!g`. Sending is a different act from doing something yourself, so `ASK` stays non-waiting, as messaging decided. Both use the same `,` trailing-clause shape for options.

## Considered Options

- **`PURSUE` carries on by default, `, AND WAIT` to wait**: a symmetric pair with `ASK` and its reserved `, AND WAIT` clause, but the common recipe case reads wrong, and the rare case becomes the short one.
- **Two verbs** (for example `PURSUE` and `START`): no clause needed, but one more keyword, and the two words don't say which one waits.

## Consequences

- `PURSUE` and `ASK … TO` look alike but differ on waiting. The Visual Editor should show the difference.
- A waiting Body depends on its Goal: it fails if the Goal is dropped or can't be reached (*Plan failure and fallback*).
- A Goal already being pursued must be joined, not restarted, which needs generated ASL beyond a plain `!g`.
