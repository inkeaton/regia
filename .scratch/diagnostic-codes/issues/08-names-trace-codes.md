# Names: Trace codes

Type: grilling
Status: closed
Assignee: claude
Blocked by: 02, 03

## Question

What is the name of each code in every `T` code (chapters 04–38) (about 49 codes, retired ones included)? The rules are in *The shape of a code*.

Claude drafts a name for each code from `../inventory.txt` and the chapter's check list, starting from the case-file slug where a case exists, and checks the draft against `GLOSSARY.md`. The user reviews the batch and settles every name. The settled rows are appended to `../mapping.csv`, and `rename_codes.py check --partial` must pass on them.

A Trace code names a runtime event (a warning, a Failure cause, an `unheard` entry), so its name says what happened in the run (`negative-weight`, `spawn-refused`).

## Resolution

Settled with the user on 2026-11-27. The 46 rows for `T0401`–`T3802` are in [`mapping.csv`](../mapping.csv), and `rename_codes.py check --partial` passes on them. One code is left unmapped: `R0412`, chapter 23's fake example, which *Rewrite the spec text on codes* replaces. No name in this batch is over 30 characters.

**Patterns for runtime events.** Three of the obvious names were already taken by R codes (`negative-duration` is `R12_03`, and `unheard-signal` and `unheard-subplot-ending` are the R38 and R17 absence checks), so Trace codes use their own patterns:

- **`X-not-number`**: a value that isn't a Number at runtime (`T04_01-operand-not-number`, `T09_01-weight-not-number`, `T12_01-duration-not-number`, `T15_01-count-not-number`). It follows `R28_01-external-name-not-atom`, and `T07_01-recipient-not-agent` and `T15_04-except-placeholder-not-agent` read the same way.
- **`X-below-zero`**: a negative value counted as 0 (`T09_02-weight-below-zero`, `T12_02-duration-below-zero`, `T15_03-count-below-zero`). It is used over `negative-X` so the three stay parallel despite `R12_03-negative-duration`.
- **`X-found-no-plan`**: nothing ran for an event, whether no Plan names it or no Context holds (`T07_02-cue-found-no-plan`, `T11_04-goal-found-no-plan`, `T38_01-signal-found-no-plan`, `T38_02-ending-found-no-plan`). This covers the spec's `unheard` entries, whose `unheard-X` names went to the R absence checks.
- **Leaving and the Cast**, in glossary terms: `T19_01-message-after-leaving`, `T20_01-giving-after-leaving`, `T30_01-giving-outside-cast`. "Giving" covers Mappings too.
- **`stray-X`** for a game reply nothing waits for (`T37_01-stray-action-result`, `T37_03-stray-state-result`), as in *Names: chapters 01–05*.

**Other choices:**

- **`T19_02-join-refused`**, not the case slug's `spawn-refused`: the glossary avoids "Spawning" under *Joining*, and chapter 33 calls the message a join. The case file keeps its name (out of scope).
- **`T26_01-all-pick-weights-zero`** beside `T09_03-all-weights-zero`, as `R26_05` says `pick`.
- The retired **`T29_02-plan-stopped-by-take`** gets the plain name of what it reported.
- **Weakest names**, accepted as drafted: `T11_03-explicit-fail` (the alternative was `fail-statement`), `T08_01-update-of-unknown-fact` ("unknown" here is the spec's "isn't known"), `T15_01-count-not-number` (it covers fractions too), `T18_01-unusable-quota-quantity` and `T33_01-invalid-join` (each covers several faults). They can still change before the 1.5 release.
