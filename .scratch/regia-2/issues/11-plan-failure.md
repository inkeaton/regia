# Plan failure and fallback

Type: grilling
Status: open
Blocked by: 05

## Question

What happens when things go wrong (Q4b)? An Action fails, a Goal can't be reached, or no Plan applies to an Event. Does Regia expose failure handling (like ASL `-!` plans), and how would a designer write a fallback? What is the default behaviour when nothing handles a failure?

## Comments

- From *Numbers and arithmetic* (04): Body arithmetic on a non-Number, or division by zero, makes the Plan fail at runtime. This ticket decides what that failure does. See `docs/spec/04-numbers-and-expressions.md`.
- From *Goals and Trigger kinds* (05): a "Goal fails" Trigger kind is reserved (e.g. `WHEN g FAILED:`); decide whether it exists. Also what happens when a Goal is pursued and no `TO` Plan applies. A Goal is reached when its `TO` Plan finishes. See `docs/spec/05-goals-and-triggers.md`.
- From *Context vs control flow* (06): a Trigger with `GIVEN` Blocks and no `ELSE`, where no Context holds, is a "no Plan applies" case. See `docs/spec/06-context-and-control-flow.md`.
- From *Context vs control flow* (06): on Targets without a native `if`, an `IF` becomes an internal subgoal (`regia_if_N`). A failure inside a branch must behave exactly like a failure of the Plan itself, and designers must never see or handle the internal goal.
