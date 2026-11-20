# A drop spreads as a drop

`DROP g` already stopped the Goals `g` was waiting on, and each fired `DROPPED`. Upward it went the other way: the Body waiting on `g` failed, its Goal fired `FAILED`, and the Trace recorded a Failure. We now make a drop **spread upward as a drop too**: the waiting Body stops, its Pursuit fires `DROPPED` and `ENDED`, and so on up the chain, with no Failure anywhere (spec 08).

A `FAILED` Plan can't read why its Goal failed, so it reacts as if something went wrong. In the showcase, dropping `fetch` made `WHEN bring FAILED` tell the Guest the pie was sold out, though nothing had gone wrong and we had chosen to stop. With this rule `FAILED` always means that something went wrong, and `DROPPED` that someone chose to stop. It is also what Jason does when a desire is dropped: the whole intention goes, with no failure event.

## Considered Options

- **A drop fails whoever waits (the first draft)**: "the Goal I waited on will never be reached" is one case, however it came about, and one `FAILED` Plan covers it. The Plan can't tell a choice from a fault.
- **Keep it, and let `FAILED` carry a reason of "dropped"**: every `FAILED` Plan would then start by testing for the one reason that isn't a failure.

## Consequences

- Dropping a small sub-Goal stops the Goal above it without a Failure in the Trace. The Trace links each stopped Pursuit to the `DROP` with `because`, at level `info`.
- A recipe that wants to give up one step and go on can't do it with `DROP`. It wasn't possible before either.
- Cleanup for "over, however it went" is written under `WHEN g ENDED`, which fires after `REACHED`, `DROPPED` or `FAILED`.
- `T1102` now covers only a waited-on Goal that fails.
