# Decide: Trace entries and codes

Type: grilling
Status: open
Assignee:
Blocked by:

## Question

What kind of entry is each Trace code written as, and which codes stay?

- F18, F22, F48: `T0902`, `T0903` and `T2601` are not warnings (chapters 09, 26). Which kind are they written as (a new kind, or a `code` field on an existing one)? Does a negative Match Weight write `T0902`? Does `T2601` fire when Weights that aren't Numbers leave a `GIVEN` with no Match? Chapter 34's table also misses `T0403`. (Guide: entries a case need not list.)
- F25: is `T1102` retired, or does the failure chain say when it is written? (Guide: not listed.)
- F30: is `T1501` (a count that isn't a Number) meant for a Director's `ASSIGN … TO ?n OF`, where the failing Plan stops and the Phase stays?
- F81: how does a Director tell `T2001` (a leaver) from `T3001` (never in the Staging), when it keeps no record of leavers? Or do the two merge?
- F82: in 1.5, which code does a nonsensical join, a join before the state reply, and a join after the Root has ended write: `T1902` only, or `T3301`/`T3305`/`T3304`? (Guide: `T1902` only.)
- F86: which `agent` do the game link's own entries carry (`CLOCK PAUSED`/`RESUMED`, `T2802`/`T2803`)?
- F49: chapter 34's console texts: should the `plan` line's Trigger, `STAGING … STARTED` (no parameters, the cast list), `UNHEARD <code> <what>` and the `run` entry's `agent` be given as a form, not only by example? (Guide: `STAGING RoyalBanquet STARTED king AS Host, …`.)

Start each question from the guide's reading. Mark which answers need an ADR (a new kind, a retired code).

Applying the answers is *Apply: Trace entries and codes*.
