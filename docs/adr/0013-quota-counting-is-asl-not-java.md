# Quota counting is ASL, through a generated dispatcher, not Java

A Quota Trigger (spec 18) must see every Signal of its Event, and the plain `WHEN e` Plan must still run for the same Signal. Jason handles one plan per event, so one incoming event has to become two effects. We do this in generated ASL. For every Event name that some Quota Trigger watches, the Transpiler emits an atomic **dispatcher**: the only plan for the incoming event. It posts the plain Trigger as a generated Goal, `regia_when__<e>(…, Sender)`, then counts with an Infrastructure plan. The designer's plain Blocks for that Event become plans for the generated Goal. Silence when nothing applies comes from empty `-!…[error(no_applicable)]` and `[error(no_relevant)]` plans (spec 33).

`regia-jason`'s job is the connection between Jason and the game (VEsNA-Pro's body), VEsNA's Propensities, and precedence in `selectOption`, which only Java can reach. Quota counting is language logic. Keeping it in ASL keeps the Java small and shows the counts in the mind inspector like every other piece of Infrastructure state (spec 28).

## Considered Options

- **A hook in `regia-jason`'s message intake** (`socAcc`, or where a message becomes an event) that posts a second, counting event. Every Event keeps its trigger, but quota logic would live in Java, in both agent classes.
- **The sender sends a second counting message.** Twice the traffic, and the sender would have to know which receivers count what.
- **A dispatcher for every Event from another Agent**, watched or not. One uniform shape, but every Signal pays an extra reasoning cycle.

## Consequences

- A watched Event costs one extra reasoning cycle, and its plain Plans run as a fresh intention posted by the dispatcher. Events that no Quota Trigger watches are unchanged.
- Whether an Event is watched is a whole-Program fact: adding a Quota Trigger in one Playbook changes how other files compile that Event. This is fine because the Transpiler always rebuilds the whole Program (spec 23).
- The Sender is passed as an argument, since Jason replaces it with `source(self)` on Goals it posts itself. `FROM` tests on watched Events compile against that argument.
- An Agent kind combining several Role files must not duplicate a dispatcher (*.jcm generation*).
