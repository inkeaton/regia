# Write: Subplots and Stagings

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Task

Write `docs/guide/12 - Subplots and Stagings.md`.

Covers: `START SUBPLOT` and `END SUBPLOT`, Mappings into a Subplot, several Stagings of one Plot, Outcomes and how the parent reacts.

Sources: 17.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-12: [`docs/guide/12 - Subplots and Stagings.md`](../../../docs/guide/12%20-%20Subplots%20and%20Stagings.md), about 4,000 words counting snippets, tables and the two diagrams, over eight sections (starting a Subplot, casting, in two Stagings at once, several Stagings of one Plot, ending with an Outcome, hearing a Subplot end, ending a Subplot from above, what a Plot may start). The `MAPPING` clause itself is left to *Playbooks and Roles*, counted Mappings to *Randomness*, and what `END PLOT` does step by step to *Plots and Directors*. Not yet read by the user.

Checked by hand against spec chapters 07, 13, 15, 16, 17, 18, 19, 20, 25, 30, 31 and 34, and primer chapters 1 and 5 (for *Since 1.0*).

Showcase: the Program is unchanged. The one snippet with no path line is the cycle (`HonorDuel` starting itself), which is an error and can't be in the showcase.

Sixteen `#revise`, three of them carried over from the README's notes (no "everyone else" beside Placeholder Mappings, an Agent in two duels at once, a Director that can't name its Cast, here as the reason `duel_abandoned` names nobody). New here:

- A Plot takes no arguments: what differs between two Stagings comes in through the Cast or through Facts the Agents already hold.
- A whole-Role `MAPPING` is looked up at each use on an `ASSIGN` and copied once on a `START SUBPLOT`, with the same spelling.
- A Placeholder Mapping takes whatever a Signal's argument holds; a wrong one leaves a duel with no `Defender`, waiting in `challenge`.
- Being cast in a Subplot adds behaviour and suspends none: a Challenger goes on dining.
- No condition asks whether, or how many, Stagings of a Plot are running.
- A Plot doesn't declare its Outcomes, and an Outcome is an Event like any other.
- A plain `ENDED` means "any ending" or "the endings not listed above" depending on its position; "no Outcome" can't be matched alone.
- An ending that no `ENDED` Block matches is ignored without a warning (`Poisoning`'s plain `END PLOT.`).
- `ENDED` doesn't say which Staging ended.
- What follows a Subplot is written in another Plan, tied to the `START SUBPLOT` only by the Plot's name; a Director can't start a Subplot and wait.
- `END SUBPLOT` ends every Staging of a Plot or none.
- A Subplot ended from above reports nothing, so tidying up is written twice.
- A Subplot meant to last one Phase is ended by hand.

Three *Spec wording* entries and one *Gaps in the showcase* entry were added to the showcase README.
