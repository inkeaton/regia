# A Playbook taken away still runs its closing Plans

When an Agent's last Giving of a Playbook went, every Plan of the Playbook was switched off at once. The Goals its Plans were pursuing fired `DROPPED`, and the Playbook's own `DROPPED` Plans didn't run, because they had just gone with it. We now let the Playbook **close**: its running Plans stop, the `DROPPED` and `ENDED` Plans those drops fire still run, then its `WHEN UNASSIGNED:` Plan, and no other Trigger of the Playbook is taken from the moment the taking starts (spec 15).

In the showcase the Director takes `Dining` away at the end of the feast. `WHEN have_dinner DROPPED`, which clears the plate, is `Dining`'s own Plan, so the plate kept its Facts. A Playbook is meant to be written without knowing its Plot, and it couldn't clean up after itself without asking the Plot to warn it first.

## Considered Options

- **The guard closes at once (the first draft, spec 29)**: the simplest rule, and the one Jason gives for free with a belief test on every plan. Cleanup then belongs to whoever takes the Playbook away, who can't see its Local Facts.
- **Forget the Playbook's Local Facts when it goes**: no cleanup Plan is needed for them. It breaks `already_greeted`, which is meant to survive the Playbook being given back (spec 10), and does nothing for Facts that aren't local or for an Action that must undo something in the game.
- **A Director's call-off, sent before the `UNASSIGN`**: the Director drops the Goal it asked, waits, then takes the Playbook. It puts the Playbook's cleanup in the Plot's hands, and waits on replies, which 2.0 doesn't have.
- **Closing Plans that must run to completion without pausing**, like an `EXITED` Plan: it would forbid `WAIT` in every `DROPPED` Plan, or only in those that happen to run during a taking, which can't be known at build.

## Consequences

- A Playbook is in one of three states on an Agent: given, closing, not given. The Target's guard has to tell them apart.
- A closing Plan can outlive the Giving by as long as it takes. If the Playbook is given back meanwhile, the closing Plans finish next to the new ones.
- `UNASSIGNED` and `ASSIGNED` fire on the last Giving going and the first arriving, never per Giving. A Giving has no identity a Plan can read.
- A Director still can't call off a Goal it asked. A Goal that must stop with a Phase has its recipe in a Playbook given for that Phase.
- Local Facts stay unless the Playbook forgets them in a closing Plan.
