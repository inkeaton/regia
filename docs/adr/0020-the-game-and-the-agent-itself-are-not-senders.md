# The game and the Agent itself are not Senders

A Trigger with no `FROM` matched anything, and a `FROM` clause matched only what an Agent or a Director had sent. Nothing could say "only what I saw" or "only my own Goal": in the showcase any Agent that told a Guard `saw_pouring(?rival)` got `?rival` seized, and `TO vent:` ran for anybody's `ASK`. Nor could a Plan say "unless it is about me", so one insult took two Messages. We add two words and keep one definition (spec 03, 05, 07, 38).

**A Sender stays an Agent or a Director.** The game and the Agent itself are named beside it: `FROM GAME` matches what the game sent or reported, and `FROM ME` what the Agent caused with its own `PURSUE`, `LEARN` or `CHANGE`. `FROM ?who` is never filled with either, and "the Sender of a Pursuit hears how it ended" has no exception. No `FROM` still matches everything.

**`ME` is a Value**, the Agent running the Plan, legal wherever a Value is in a Playbook and nowhere in a Plot. The same word is the source in `FROM ME`.

**An own `PURSUE` is from `ME`, wherever it is written.** A Pursuit started inside a recipe the Director asked for doesn't take that Plan's Sender. A recipe that serves several sources lists them: `TO take_seat FROM DIRECTOR OR ME:`.

## Considered Options

- **One word, `FROM NOBODY`, for anything without a Sender**: smaller, but `TO vent FROM NOBODY:` reads as its opposite, and a `LEARNED` Trigger could not tell what the game reported from the Agent's own `LEARN`. Jason already keeps the two apart.
- **No `FROM` means "from the game" or "my own"**: it would close the Guard's hole by default, but every Plan written so far would change meaning and the common case (`WHEN greeting:`) would become the long one.
- **Widen Sender to cover the game and the Agent**: one concept, but `FROM ?who` would have to be filled with something that is not an Agent, and the report of an ending would need an exception for a Sender that is oneself.
- **A `PURSUE` inherits the Sender of the Plan it is in**: `TO take_seat FROM DIRECTOR:` would then serve a `PURSUE` inside a Director's recipe, but the Director would hear the endings of Goals it never asked for, and `FAILED FROM DIRECTOR` would stop meaning "the Director asked".
- **No `OR`, write the recipe twice**: no new syntax, but eight of the showcase's twelve recipes carry a `FROM`, and every recipe that the Director starts and that repeats would need a copy.

## Consequences

- A Plan that must act only on what its Agent perceived writes `FROM GAME`. Nothing warns when it doesn't.
- A recipe with a `FROM` that doesn't list `ME` can't be pursued by its own Agent, and can't repeat. The Transpiler warns on a `PURSUE` no recipe admits, and on an `ASK` when every recipe is `FROM ME`.
- An `OR` list takes no Placeholder and no quantity; a Plan that needs the Sender is a Plan of its own.
- `FORGOTTEN` still takes no `FROM`, and a Director can't tell its own `LEARN` from the game's. `ME` in a Role setup is an error for now, though a setup is written in the Agent's words (ADR 0009).
- The chapter 05 note that left `FROM SELF` unspecified is closed; the word is `ME`.
