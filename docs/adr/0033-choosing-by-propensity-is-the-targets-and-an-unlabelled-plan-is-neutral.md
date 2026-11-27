# Choosing by Propensity is the Target's, and an unlabelled Plan is neutral

When candidates of equal rank compete, the Selection function chooses by the Agent's Propensities. On Jason that is VEsNA-Pro's temper selection. It sums distances without normalising, so alternatives that name different sets of Propensities can't be compared by reading the source. It scores a plan without `temper` as a perfect fit, so a `TIES` pool labelled on one side only behaves as an `OVER` for the unlabelled side. It applies `SHIFTS` only when it chooses between several intentions, so a lone Plan never shifts a Mood. The language could define all three itself and have the Infrastructure do the scoring in its own Java.

We decided that 2.0 leaves the scoring and the moment a `SHIFTS` Label applies to the Target, as VEsNA-Pro does them today, and changes only what the Transpiler hands it:

- **An unlabelled candidate is neutral.** Where a competition (one Trigger's Blocks in a Playbook, or a `TIES` pool) has at least one `SUITS`, every unlabelled candidate in it gets a `temper` naming each Propensity the labelled ones name, at 0.5 for a Trait and 0 for a Mood. Labelled and unlabelled Blocks may then be mixed in one Playbook, and labelling one side of a tie is enough.
- **A missing starting value is neutral too**: 0.5 for a Trait, 0 for a Mood, written into the `.jcm`, with no warning. Trait values lie in [0, 1], as VEsNA-Pro keeps them.
- **A Mood can be changed from a Body** with `SHIFT m BY n`, applied when the Statement runs. This is the one place the Infrastructure reaches into VEsNA-Pro's Moods, through a small upstream method.
- **Propensity code is emitted only where something needs it**, since most Programs have no Propensities.

## Considered options

- **The language defines the fit** (mean distance over the named Propensities, an unlabelled candidate ranked after every labelled one, a Shift applied once when the Plan is chosen), implemented by the Infrastructure instead of VEsNA-Pro's temper path. It makes the outcome readable from the source and testable, but it replaces VEsNA-Pro's selection before VEsNA-Pro has been tried as it is. Deferred past 2.0.
- **Keep everything the Target's, including unlabelled candidates.** An unlabelled candidate would keep winning as a perfect fit under `most_similar`, and mixing would stay an error.
- **A neutral alternative ranked by the language** ("loses to any fitting alternative"). It needs a notion of "fitting", that is a threshold the language would have to invent.

## Consequences

- Which candidate wins, and when a `SHIFTS` Label applies, can still change with VEsNA-Pro. The spec records how it behaves today, and the Trace is where a run is checked.
- On VEsNA-Pro a `SHIFTS` Label has no effect for an Agent that never meets a `SUITS`. The Transpiler warns, and `SHIFT` in the Body is the reliable way.
- R13_04-mixed-suits-trigger-blocks (mixing in a Playbook), R13_09-unlabelled-ties-candidate (a mixed `TIES` pool) and R21_11-missing-propensity-value (a kind with no value) are retired.
- A Program with no Labels and no `SHIFT` emits no `temper`, `effects` or `strategy` at all.
- Testing a Propensity in a Context is still not in 2.0.
