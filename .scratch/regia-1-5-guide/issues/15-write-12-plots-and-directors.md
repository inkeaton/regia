# Write guide chapter 12, Plots and Directors

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05

## Question

Write `docs/guide/12-plots-and-directors.md`, *Plots and Directors*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 20, 16.
- **Covers:** a Plot, its Roles, a Role's Block as its setup, Phases, `ENTER`, `WHEN ENTERED`, `DURING PLOT`, what a Director perceives, Director Actions, failure in a Director, the Root Plot.
- **Quotes most:** `royal_banquet.regia`.
- **"In 2.0" notes:** `FROM GAME`, Quota Triggers in a Director.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-20 (task). [`docs/guide/12-plots-and-directors.md`](../../../docs/guide/12-plots-and-directors.md), about 600 lines, written from the template:

- An opening table of the chapter's words (`PLOT`, `ROLE` with a Block, `PHASE … INITIAL`, `DURING`, `ENTER`, `ENTERED`/`EXITED`/`AFTER`, `IN`, `END PLOT`, `ROOT`).
- Sections, simple to full: A Plot (`Poisoning` whole); Roles of a Plot (played vs address, who casts them, where a Plot Role stands); A Role's setup (the banquet's `CAST:` and Role setups, why `PURSUE take_seat` needs no `ASSIGN` above it, *A setup for a Phase*, *What a setup leaves behind*); Phases (a mermaid of the banquet's transitions); Entering and leaving a Phase (`reception`, the six steps of `ENTER`, `feast`'s `EXITED`, *A timeout: `AFTER`* on `HonorDuel`'s `betting`, *Starting a Staging*); `DURING PLOT` (the `LEFT` Plan, *`IN`*, *`EXITED, BY PARENT`*); What a Director perceives (`poison_drunk`, `wager`, *Counting by hand* on `arrival`); What a Director does (`farewell`, the Statement table, *Directing one Agent*); Failure in a Director; `END PLOT`; The Root Plot.
- Covers everything the ticket listed, plus `AFTER`, `IN` and `EXITED, BY PARENT` (spec 20/12 constructs the outline's list left implicit); `LEFT`/`EMPTIED`, Subplot endings and Givings are pointed at, not repeated.
- Three "In 2.0" notes: setups for joiners; `FROM GAME` (on `poison_drunk`); and one on the `took_seat` hand count covering both a Director hearing an asked Goal's ending and a Quota Trigger. The ticket's two (`FROM GAME`, Quotas) are among them.
- No throwaway snippets beyond inline ones (`GIVEN NOT IN farewell`).
- Every showcase snippet checked against its file by script (17 snippets). Codes appear in *Checks* only; they borrow `R0109`, `R0111`, `R0303`, `R0304`/`R0305`, `R0309`, `R0506`, `R1006`/`R1007`, `R1012`, `R1015`, `R1205`, `R1307`, `R1406`, `R1502`, `R1507`, `R1508`, `R1702`, `R1705`, `R2104`/`R2105`/`R2110`/`R2112`/`R2114`, `T1201`/`T1202`, `T1901`, `T3801`.
- `Guide: Plots and Directors` added under *16 Role setup* and *20 Directors* in the showcase README.
- Grep for retired spellings: only in *Checks* lines naming them. The humanizer pass fixed one count ("four `PHASE` lines") and found no other tells.

Three non-blocking findings: what a failing `EXITED` Plan does to its transition; chapter 17's "names or infers the Root" against chapter 21's "never inferred"; no code of its own for `ENTER` in a Plot with no Phases (the guide uses `R2008`).
