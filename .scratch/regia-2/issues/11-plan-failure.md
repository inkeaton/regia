# Plan failure and fallback

Type: grilling
Status: open
Blocked by: 05

## Question

What happens when things go wrong (Q4b)? An Action fails, a Goal can't be reached, or no Plan applies to an Event. Does Regia expose failure handling (like ASL `-!` plans), and how would a designer write a fallback? What is the default behaviour when nothing handles a failure?

## Comments

- From *Numbers and arithmetic* (04): Body arithmetic on a non-Number, or division by zero, makes the Plan fail at runtime. This ticket decides what that failure does. See `docs/spec/04-numbers-and-expressions.md`.
- From *Goals and Trigger kinds* (05): a "Goal fails" Trigger kind is reserved (e.g. `WHEN g FAILED:`); decide whether it exists. Also what happens when a Goal is pursued and no `TO` Plan applies. A Goal is reached when its `TO` Plan finishes. See `docs/spec/05-goals-and-triggers.md`.
