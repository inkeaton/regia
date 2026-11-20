# A Quota Plan reads what it counted, and a share rounds up everywhere

A Quota Trigger's Plan used to know only that enough Agents had sent the Event. To know who, the Director kept Facts by hand from a plain Trigger written beside the Quota (`HonorDuel`'s `wager`). Each argument also split the count, so a Signal couldn't be counted and carry data at once: `HonorDuel` sent a bare `cheered` only to be counted, next to `wagered(?stake)`.

We decided:

- Inside the Plans of a Quota Trigger Block, the condition `?x SENT e(args)` matches the Signals counted in this firing, one Match per Signal, from the Agents still counted. It is an error anywhere else.
- The anonymous `?` in a Quota Trigger matches any value without splitting the count. Named Placeholders still split it, so a vote still fires for the choice the hall agrees on.
- `PERCENT`, and any count that isn't whole, rounds **up** in a Quota and in a pick alike: a share means at least that share.

## Considered options

- **`?who` after a quantity, filled with the Agent that completed the count.** It gives one Agent of many, and none when a departure completes an `ALL`.
- **Generated Facts the Director can read anywhere.** That is the hand-kept copy again, made by the Transpiler: it outlives the firing and has to be cleaned up. `SENT` exists only while the Plan that fired runs.
- **Letting every Placeholder pool into one count.** Then `voted(?choice) FROM ALL Guest` can't say which choice won. `?` already means "any value, not kept" in `COUNT(? PLAYS Guest)` and `HonorDuel(?)`.
- **Keeping two roundings** (up for a threshold, down for a pick). The same `75 PERCENT OF Guest` meant 8 in one place and 7 in the other. Rounding down everywhere would let half of three Guests fire a vote with one. Rounding up makes a pick never empty a Role by rounding alone: 30 PERCENT of 2 Guests picks one.

## Consequences

- `SENT` is reserved. A Target keeps every counted Signal with its arguments until the Plan has run, not only the sender.
- Counted Goal endings (`BY ALL Guest`) have no `SENT` in 2.0.
- Quotas are not in Regia 1.5 (ADR 0025), so none of this is.
