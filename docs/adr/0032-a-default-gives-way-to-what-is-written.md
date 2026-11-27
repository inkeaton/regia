# A default gives way to what is written

With nothing declared, a Subplot ranks above its parent (ADR 0008). In the showcase, `HonorDuel`'s `PARENT OVER SELF ON scandal` and `RoyalBanquet`'s `HonorDuel OVER Poisoning` together with the default `Poisoning OVER SELF` made a cycle on `scandal`. That cycle was built from one line in each of two files and a line nobody wrote. `RoyalBanquet` could break it only with `SELF OVER Poisoning ON scandal`, which it could write only by knowing what its Subplot had declared.

We decided that a Plot's written relations, its Subplots' `PARENT` relations included, are placed first. Each default is added afterwards, and only if the written relations don't already imply the opposite, directly or through a chain. A default left out is reported as a note (`R13_12-default-left-out`) and in the conflict report. A cycle made only of written relations is still an error (`R13_01-precedence-cycle`).

## Considered options

- **Defaults as relations like any other, cycles an error** (the old rule): the writer must find and break a cycle that contains a line nobody wrote, often by knowing what a Subplot declared.
- **Drop the default for that Subplot entirely, for every item**: simpler to state, but one `PARENT` line on one item would undo "the story beats everyday behaviour" for all the others.
- **No default between a Subplot and its parent, name order instead**: removes the cycle but trades a meaningful default for an arbitrary one with a warning on every story.

## Consequences

- No written line is ever overruled by a default, and no default is ever named in a cycle.
- The order is worked out per item, so a default can be left out on `scandal` and still hold on `idle`.
- Chapter 32's sort places written relations, then defaults, then breaks free choices by name.
