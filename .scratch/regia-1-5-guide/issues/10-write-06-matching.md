# Write guide chapter 06, Matching

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05

## Question

Write `docs/guide/06-matching.md`, *Matching*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 26.
- **Covers:** one Match left unspecified, Picks, `FOR EACH`, `COUNT`.
- **Quotes most:** `hosting.regia`, `royal_banquet.regia`.
- **"In 2.0" notes:** none expected.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-20 (task). [`docs/guide/06-matching.md`](../../../docs/guide/06-matching.md), about 330 lines, written from the template:

- Sections, simple to full: One Match, and we don't say which (with `Duelling`'s single `stamina` Fact as the case where the default is safe); Picks (with *The ranked Placeholder*); A weighted Pick (a table for wrong Weights); Where Picks are allowed (throwaway error lines); `FOR EACH` (snapshot shown in a mermaid sequence: the pie served mid-loop stays on the plate; with *Forgetting everything that matches*); `COUNT` (with *Counting who plays a Role*).
- Quotes `honor_duel`, `scheming`, `noble_socializing`, `dining`, `duelling` and `royal_banquet`. The outline's `hosting.regia` has no Pick, `FOR EACH` or `COUNT`, so it isn't quoted.
- One "In 2.0" note, though none was expected: `RoyalBanquet`'s hand count with `COUNT` is the 1.5 stand-in for a Quota Trigger (spec chapter 18), and the showcase says so in a comment.
- Every showcase snippet checked line by line against its file by script. Throwaways: the four misplaced Picks for `R2603`.
- Checks borrow `R0801`, `R1517`, `R0304`, `T0901` and `R0109` where the misuse is in this chapter's constructs. No `T0902` for a negative Match Weight: chapter 26 doesn't say (finding).
- `Guide: Matching` added under *26 Match selection* in the showcase README.
- Grep for retired spellings: only the deliberate `, AT RANDOM` in Checks. The humanizer pass rewrote three sentences.

Two non-blocking findings: `T0902`/`T2601` left open for weighted Picks; no code for `GIVEN 3 OF …`.
