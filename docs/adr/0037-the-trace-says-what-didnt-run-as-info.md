# The Trace says what didn't run, as info

The Trace recorded what a run did and nothing else. A Signal with no Plan, a Quota met with no candidate, a Plan that lost to another Playbook, and a Mood shifted by a Label left no entry, or a warning only for some of them. "Why did nothing happen" was the question most often asked of a run (the old guide's Review List, N12, at commit `c30d1d4`). Two Blocks with the same Trigger wrote the same `PLAN` line, and a Director had a different name depending on what else was running and on where you looked.

We decided that what arrives with a Sender, or a count that is reached, and finds no Plan writes an `unheard` entry at level **info**, with a Trace code. `T3801` and `T3802` (a Signal or a Subplot's ending with no Plan), which were warnings, become `unheard` entries. A `plan` entry with rivals says how it won and over whom. It names its owner (Playbook, Phase or `DURING PLOT`) and its `GIVEN` or `ELSE`. Mood changes and Quota counts get entries of their own. A Subplot's Director is always numbered.

## Considered options

- **Warnings for everything that didn't run**: a behaviour case must list every warning, and a Phase that ignores a Signal on purpose would fill every case with lines about nothing. The language warns only about what can't be meant or can't be avoided, and an ignored Signal is often meant.
- **An entry for each Plan that lost**: it doubles the Trace on every contested Trigger. The losers can be read from the winner's `over`.
- **Entries for game percepts nobody takes**: the game sends far more than a Program listens to.
- **Number a Director only when another Staging of its Plot runs**: the name of one Director changes with what else runs, so a behaviour case can't name it reliably.

## Consequences

- Trace codes now name `info` entries too. A behaviour case may list an `unheard` entry and doesn't have to.
- `--console warnings` hides `unheard` entries. The default, `all`, shows them.
- The Jason Target needs catch-all plans for told Events at Agents, a logger named with the designer name, a way for `selectOption` and VEsNA-Pro to pass `by`, `over` and `fits` to the `plan` entry, and a hook in VEsNA-Pro's `Temper` that reports when it applies a `SHIFTS` Label.
- In Regia 1.5 all of it is in, except the Quota entries (`count`, `T1802`, `ON DEPARTURE`), which come with Quota Triggers.
