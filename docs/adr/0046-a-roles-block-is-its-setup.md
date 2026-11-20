# A Role's Block is its setup

A Plot's Role setup was written `ROLE Guest STARTS WITH:`, and the Cast's `CAST STARTS WITH:`. The syntax review found that `WITH` there ("begins by doing") fails chapter 01's one-meaning rule, since everywhere else it introduces the Cue an ending carries. We dropped the phrase: a setup is the Role's own Block, `ROLE Guest:` and `CAST:`, at Plot level and inside `DURING <phase>`. The old header is the retired spelling `R1608`, and `STARTS` stays reserved for its hint.

This matches Instancing, where `KIND noble, PLAYS Guest:` carries the lines each of its Agents starts with. "Starts with" is what a Role's Block means, not a keyword.

Inside `DURING`, `ROLE Guest:` names a Role the Plot already declares and declares nothing, as `DURING PLOT` names the Plot. `ROLE` passes chapter 01's rule for nouns: every use refers to a Role. A Playbook keeps `ROLE` for its addresses for the same reason, and a Mapping reads well only because both sides are Roles. A Playbook's `ROLE` takes no Block (`R1601`).

`LEARN` and `PURSUE` stay in setups and on `KIND`/`AGENT`. Their gloss, read from the Agent's side ("comes to know", "takes on"), is the one they have in a Body. Only the source differs, and it follows from where the line is written.

## Considered options

- **A new head keyword, `SETUP Guest:` / `SETUP CAST:`.** `ROLE` would only declare, but at Plot level the Role's name is written twice (`ROLE Guest` then `SETUP Guest:`), and it adds a keyword.
- **`ROLE Guest STARTS:`.** The smallest change, but it keeps a keyword with one use and leaves `ROLE` inside `DURING` as it was.
- **`TELL` and `ASK` in a setup.** They name a recipient, and a setup has none to name. On a `KIND` no Director is written at all.

## Consequences

- `ROLE Guest:` with a Block, an error before, is now the only way to write a setup.
- A setup may use the Plot's parameters, which are filled when the Staging starts. Any other Placeholder is still `R1604`.
- The 1.5 showcase rewrites its setup headers when it is brought up to the reviewed syntax.
