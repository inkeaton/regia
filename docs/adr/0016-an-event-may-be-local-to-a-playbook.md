# An Event may be local to a Playbook

Spec 10 let a Playbook declare local Facts and Goals and kept every `EVENT` at file level, for two reasons: Events are the game's interface, and a local item can't be sent because nobody outside can name it. Neither holds for an Event that one Playbook both sends and reacts to. `challenged`, `hit` and `yielded` are told only between two holders of `Duelling`, and still sat in the shared Vocabulary. We now allow **`EVENT` inside a `PLAYBOOK`**: it never comes from the game, has no External name, and is sent with `TELL` to any recipient. Local Facts and Goals still can't be sent.

The difference is that the receiver of a told local Event can hold the same Playbook, and then it can name the Event. A local Fact or Goal is private even from other Playbooks on the same Agent, so telling one would have nowhere to land.

## Considered Options

- **Keep Events global**: one rule for all Events, but the words of a single Playbook's exchange are in everyone's namespace.
- **Local Events in Plots too**, for Outcomes: the parent has to name an Outcome in `ENDED WITH`, so it can't be local to the child.
- **Recipients limited to the Playbook's Roles**: stricter, but `TELL ?foe hit` after `WHEN challenged FROM opponent ?foe` is the natural way to answer one Agent.

## Consequences

- A local Event can't be Signalled or be an Outcome (`R10_14-local-vocabulary-sent`): a Director is outside the Playbook.
- A receiver that doesn't hold the Playbook has no Plan for the Event and nothing happens. This is not reported, as for any told Event nobody reacts to.
- On Jason the Event travels under its Generated name, `regia_local__<Playbook>__<name>`, which is the same on every holder.
- A Plot now has local Facts only: a local `GOAL` there was never usable and is an error (`R10_15-goal-in-plot`).
