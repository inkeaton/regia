# Decide: Trace entries and codes

Type: grilling
Status: open
Assignee:
Blocked by:

## Question

What kind of entry is each Trace code written as, and which codes stay?

- F18, F22, F48: `T09_02-weight-below-zero`, `T09_03-all-weights-zero` and `T26_01-all-pick-weights-zero` are not warnings (chapters 09, 26). Which kind are they written as (a new kind, or a `code` field on an existing one)? Does a negative Match Weight write `T09_02-weight-below-zero`? Does `T26_01-all-pick-weights-zero` fire when Weights that aren't Numbers leave a `GIVEN` with no Match? Chapter 34's table also misses `T04_03-empty-whole-roll`. (Guide: entries a case need not list.)
- F25: is `T11_02-pursued-goal-failed` retired, or does the failure chain say when it is written? (Guide: not listed.)
- F30: is `T15_01-count-not-number` (a count that isn't a Number) meant for a Director's `ASSIGN … TO ?n OF`, where the failing Plan stops and the Phase stays?
- F81: how does a Director tell `T20_01-giving-after-leaving` (a leaver) from `T30_01-giving-outside-cast` (never in the Staging), when it keeps no record of leavers? Or do the two merge?
- F82: in 1.5, which code does a nonsensical join, a join before the state reply, and a join after the Root has ended write: `T19_02-join-refused` only, or `T33_01-invalid-join`/`T33_05-join-before-root-state`/`T33_04-join-after-root-ended`? (Guide: `T19_02-join-refused` only.)
- F86: which `agent` do the game link's own entries carry (`CLOCK PAUSED`/`RESUMED`, `T28_02-game-link-connect-failed`/`T28_03-game-link-lost`)?
- F49: chapter 34's console texts: should the `plan` line's Trigger, `STAGING … STARTED` (no parameters, the cast list), `UNHEARD <code> <what>` and the `run` entry's `agent` be given as a form, not only by example? (Guide: `STAGING RoyalBanquet STARTED king AS Host, …`.)

Start each question from the guide's reading. Mark which answers need an ADR (a new kind, a retired code).

Applying the answers is *Apply: Trace entries and codes*.
