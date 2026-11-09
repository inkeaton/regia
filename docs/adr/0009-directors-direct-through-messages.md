# Directors direct through Messages, not orders

A Director never orders an Agent to perform an Action. 1.0's `Host DO call_guards.` is retired. A Director reaches its Agents with the same `ASK … TO` and `TELL` that Agents use with one another, sent with Sender `DIRECTOR`, and with Director Statements that hand out Playbooks and Subplots (`docs/spec/20-directors.md`). The Agent's own `TO call_guards:` Plan decides how the request is carried out, or whether it fails.

A Playbook is written in isolation and describes how its Agent behaves (primer ch.2). A Director that could make an Agent perform any Custom Action would bypass every Playbook, Context and Precedence the Agent has, so the Agent's behaviour could no longer be read from its Playbooks. Using `ASK`/`TELL` also gives "the Director asks" a single meaning: a Role setup's `PURSUE`/`LEARN`, a Director Plan's `ASK`/`TELL`, and `TO g FROM DIRECTOR` all describe the same thing.

## Considered Options

- **Keep `Role DO action`** (1.0): direct and familiar to designers, but it overrides the Agent's own Plans, needs a `WORLD` keyword to tell the Director's own Actions apart, and in 1.0 already compiled to an `achieve` anyway.
- **Both**: `ASK` for requests, `Role DO` for "just do it". Two ways to say nearly the same thing, and the stronger one wins every time a designer is in a hurry.

## Consequences

- `WORLD` is removed; a Director writes `DO play_music.` like an Agent.
- Every Director request needs a matching `TO g:` Plan in some Playbook the Agent holds, otherwise the Goal fails at once (spec 11). A Playbook can provide a one-line `TO call_guards: DO call_guards.` when nothing more is needed.
- The Director gets no reply in 2.0. Agents send a Signal when the Director needs to know.
