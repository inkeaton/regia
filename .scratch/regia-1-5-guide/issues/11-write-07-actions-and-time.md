# Write guide chapter 07, Actions and time

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05

## Question

Write `docs/guide/07-actions-and-time.md`, *Actions and time*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 08, 12.
- **Covers:** Basic Actions on Facts and Goals, `PRINT`, Custom Actions, `WAIT`, `WAIT … UNTIL`, `AFTER` (Phases themselves are *Plots and Directors*), the Target's clock and pausing.
- **Quotes most:** `serving.regia`, `keeping_watch.regia`, `royal_banquet.regia`.
- **"In 2.0" notes:** none expected.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-20 (task). [`docs/guide/07-actions-and-time.md`](../../../docs/guide/07-actions-and-time.md), about 500 lines, written from the template:

- An opening table of every Statement a Body can run, saying which chapter covers each (Messages, `FAIL`, `SHIFT` and `PASS` are pointers).
- Sections, simple to full: Learning and forgetting (with *Forgetting everything that matches*); Updating a Fact (the `IF`-update-else-learn pattern from `resent`); Starting and stopping a Goal (only which form waits; the rest is left to *Goals and Failure*, as *Plans* already says); Custom Actions (a mermaid state diagram of the game's replies, the `ACTION` doc comments as the "done" agreement, `leave_hall`), with *Not waiting*, *Calling an Action off* and *The Target's own code*; `PRINT`; `WAIT` (`TO strike`, and why it tests stamina twice); `WAIT … UNTIL` (`have_dinner`, a mermaid sequence of another Plan of the same Guest ending the wait); `AFTER` (`HonorDuel`'s `betting`, two counts and a Cue); The clock.
- Quotes `dining`, `duelling`, `wagering`, `noble_socializing`, `serving`, `courtesy`, `scheming`, `hosting`, `vocabulary`, `royal_banquet` and `honor_duel`. `keeping_watch` has no Action this chapter needs beyond what *Messages* quotes, so it isn't quoted. One throwaway: the set-loose Action wrapped in a Goal (`poison_cup`).
- No "In 2.0" note: the repeating recipe's note (`FROM DIRECTOR OR ME`) is already in *Plans*, *Loops*, and this chapter points there.
- Every showcase snippet checked line by line against its file by script (15 snippets).
- Checks borrow `R0304`/`R0305`, `R1009`, `R2001`, `R2003` and `T1101` where the misuse is in this chapter's constructs. The Duration's own codes are repeated under `WAIT`, `WAIT … UNTIL` and `AFTER`, as *Vocabulary and files* lists them under *Durations*.
- `Guide: Actions and time` added under *08 Basic actions* and *12 Time* in the showcase README.
- Grep for retired spellings: only the deliberate `CHANGE` in Checks. The humanizer pass rewrote two sentences.

Two non-blocking findings: `R0805` doesn't except `WAIT d, UNTIL c`; chapter 37's `walk_to` example still writes doc comments as `##`.
