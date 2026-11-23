# Write guide chapter 08, Randomness

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05

## Question

Write `docs/guide/08-randomness.md`, *Randomness*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 09; 21 (`RANDOM`, the seed).
- **Covers:** `RANDOMLY` / `OPTION`, weights, Placeholders in an Option, random Picks, random starting values, the seed.
- **Quotes most:** `wagering.regia`, `duelling.regia`, `banquet.regin`.
- **"In 2.0" notes:** none expected.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-20 (task). [`docs/guide/08-randomness.md`](../../../docs/guide/08-randomness.md), about 340 lines, written from the template:

- An opening table of every way to ask for chance (Random choice, `RANDOM`, random Picks, counted parts of a Role, starting values), with where each is explained; the seed covers them all.
- Sections, simple to full: One of several Options (`WHEN idle`); Weights (a chance table for 0, 2 and 5 grudges, the two spellings of "only sometimes" side by side, wrong Weights); Placeholders in an Option; Where a Random choice goes (a Director, never a setup); Rolls (`TO strike`, from the side of chance, pointing to *Placeholders and Expressions*); Random Picks (`HonorDuel`'s betting, and why a plain condition isn't random); A random part of a Role (`1 OF Guest AS Poisoner`, `50% OF peer`); Random starting values (the Guest setup's purse, `banquet.regin`'s nobles); The seed (where it comes from, first that applies).
- The outline didn't list counted parts of a Role; they are added because chapter 34 counts them among the seeded draws.
- Quotes `noble_socializing`, `duelling`, `honor_duel`, `royal_banquet` and `banquet.regin`. `wagering` appears only in a throwaway variant (a careful Spectator, for Placeholders in an Option). Throwaways: that variant, its `PASS` error case, a Director's Random choice, and a `replay.regin` with `SEED 42` (the showcase has no `SEED` yet; the runs will).
- No "In 2.0" note.
- Every showcase snippet checked against its file by script (7 snippets).
- Checks borrow `R0106`, `R1517`, `R1602`, `R1603`, `R2107`, `R2108`, `R2601`, `R2606`, `T0403`, `T1501`–`T1503` and `T2601`.
- `Guide: Randomness` added under *09 Random choice* and *21 Instancing* in the showcase README.
- Grep for retired spellings: only the deliberate `EITHER:`/`OR:` and `, AT RANDOM` in Checks. The humanizer pass rewrote two sentences.

Three non-blocking findings: chapter 34 lists `T0902`/`T0903` as warnings (chapter 09 says they aren't) and leaves out `T2601`; chapter 21's `bravery AT RANDOM(-1, 1)` gives a Trait a Mood's range; whether a free run with the same seed replays isn't said, only a case's.
