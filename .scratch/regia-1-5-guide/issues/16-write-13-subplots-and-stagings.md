# Write guide chapter 13, Subplots and Stagings

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 05

## Question

Write `docs/guide/13-subplots-and-stagings.md`, *Subplots and Stagings*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 17.
- **Covers:** `START SUBPLOT`, casting, several Stagings of one Plot, a Subplot outliving its Phase, `FINISHED WITH`, `ENDED` as the catch-all, `DROP SUBPLOT`, no cycles.
- **Quotes most:** `honor_duel.regia`, `poisoning.regia`, `royal_banquet.regia`.
- **"In 2.0" notes:** a joiner reaching a Staging.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-20 (task). [`docs/guide/13-subplots-and-stagings.md`](../../../docs/guide/13-subplots-and-stagings.md), about 500 lines, written from the template:

- An opening table of the chapter's words (`START SUBPLOT`, `PLOT P(params)`, `RUNNING`, `END PLOT WITH`, `FINISHED`/`DROPPED`/`ENDED`, `DROP SUBPLOT`, `UNTIL EXITED`).
- Sections, simple to full: Starting a Subplot (`Poisoning` in `feast`, the four start steps); Plot parameters (`HonorDuel(offender)` and the insult Plan; a throwaway Role setup that reads `?offender`); Casting (the four Mapping forms, copy against `ASSIGN`'s live binding, *A Role that starts empty*); Being in both (what a Spectator holds, where its Signals go); Several Stagings of one Plot (a mermaid tree, arguments as the only way to tell Stagings apart, *An Agent in two Stagings of one Plot*); `RUNNING`; A Subplot outlives its Phase (`UNTIL EXITED`, `Poisoning DROPPED`); `END PLOT WITH`; Hearing a Subplot end (the banquet's handlers, a table of every ending and what runs, a throwaway plain `FINISHED`, a sequence diagram); `DROP SUBPLOT` (*When the parent ends*); No cycles (a throwaway rematch).
- One "In 2.0" note, as listed: a joiner never reaches a running Subplot.
- Throwaway snippets: the parameter in a Role setup, `COUNT(HonorDuel(?) RUNNING)`, a plain `FINISHED`, the rematch cycle.
- Every showcase snippet checked against its file by script (12 snippets). Codes appear in *Checks* only; they borrow `R0304`/`R0305`, `R0802`, `R1004`, `R1502`–`R1504`, `R1507`, `R1509`, `R1510`, `R1514`, `R2114`, `T1502`, `T2001`.
- `Guide: Subplots and Stagings` added under *17 Subplots* in the showcase README.
- Grep for retired spellings: only in *Checks* lines naming them. The humanizer pass rewrote four phrases ("Two insults, two duels", "One thing differs", "a mark, not a warning", "It belongs to Directors").

Three non-blocking findings: the README says `HonorDuel` reads `?offender` (it doesn't); where `EMPTIED` for a Role that starts empty falls against `DURING PLOT`'s `ENTERED` (chapter 20 leaves it out); no code for a Playbook's local Cue as an Outcome.
