# Messages and told Facts in ASL

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05, 10

## Question

Group C of the [inventory](../jason-open-questions.md#c-messages-and-told-facts-messages-and-told-facts-in-asl): how a told Cue, a Signal and a told Fact travel and are received in Jason.

Decide:

- the form of a told Cue that leaves nothing in the receiver, a local Cue included;
- the form of a Signal, and how a Director's `FROM Role [?who]` and `FROM ?who` test the Sender;
- the catch-all plans that write `T3801` and `T0702`;
- `LEARNED` and `FORGOTTEN` for a told Fact held from several sources (with the research on a belief told again), and `LEARNED FROM DIRECTOR` / `FROM peer`;
- `ME` as a Value and in a Trigger's pattern.

Closes when chapters 29, 30 (and chapter 07's notes) are edited.

## Comments

- From *A Plan's Statements in ASL*: the Statement translations this ticket decides go in chapter 39 (`docs/spec/39-jason-plan-bodies.md`), whose *Not decided here* points back here. Chapter 08's `LEARN`/`FORGET` note leaves how told Facts are forgotten to *Messages and told Facts in ASL*.

## Resolution

Grilled with the user on 2026-11-18. Recorded in a new *Messages* section of chapter 39, a *Signals* section of chapter 30, and edits to chapters 07, 28, 29, 32, 33, 34, 35 and 38.

1. **A told Cue** travels as Jason's `signal` message: the event `+c[source(S), signal]`, with no belief, so every telling fires. A local Cue goes under its Generated name, `EVERYONE` wraps it as `regia_everyone(signal, c)`, and a game Cue (`regia_cue`) is the same kind of event marked `source(percept)`. Rejected: a plain `tell` (a belief stays, and telling again raises nothing) and an achieve-goal per Cue (no applicable plan becomes a Goal Failure). Checked in Jason 3.2.1 and 3.3.4.
2. **A Signal** is the same message, sent once to each distinct Director in `regia_given(p, D, …)`. At the Director, `FROM Guest ?g` → `regia_cast(_, guest, G)` on the trigger's `source(G)`; `FROM ?winner` → `Winner \== percept`; no `FROM` matches the game too. A Signal to a Director that is ending is dropped silently.
3. **Catch-alls**: one generated plan per Cue, annotated `regia_unheard`, which `selectOption` takes only when it is the only option (chapter 32, new step 0). An Agent's are for each Cue some `TELL` sends, in a generated `asl/unheard.asl` (chapter 28), and write `T0702`. A Director's are for each Cue it can be Signalled, and write `T3801`. Both mean "no Plan ran", so a Cue whose `GIVEN`s all fail is unheard too (chapters 07 and 34 reworded). A variable-trigger catch-all was rejected: Jason tries it only when no plan is relevant. A dispatched Cue (2.0 Quotas) writes the entry from its dispatcher's failure plans (chapter 33).
4. **A told Fact**: `regia.RegiaAgent` overrides `brf`, so a Fact already known from any source takes the new source with no event. `+f` is raised only for a new Fact, and its Sender is the first teller. A Context test was rejected because two tellings can both arrive before either plan runs. `FORGET` and `CHANGE` use `.abolish`, and a game removal removes every source, so `FORGOTTEN` fires once. `LEARNED FROM DIRECTOR` / `FROM peer` test the trigger's source like any Sender form. The knight already `on_duty` (`royal_banquet.regia:128`) doesn't salute again.
5. **`ME`**: as a Value, `.my_name(Regia_me)` at the start of a Body that uses it. In a Trigger's pattern, a fresh generated variable tested with `.my_name` right after the Givings guard.
