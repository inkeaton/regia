# Write guide chapter 09, Goals and Failure

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05

## Question

Write `docs/guide/09-goals-and-failure.md`, *Goals and Failure*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 05 (Goals, how a Pursuit ends), 11.
- **Covers:** `PURSUE`, the same Goal twice, `DROP`, `REACHED`/`FAILED`/`DROPPED`, what fails a Plan, how Failure spreads, `FAIL`, Reasons, `WHEN g FAILED`, fallbacks; the failure chain as a pointer to *The Trace*.
- **Quotes most:** `scheming.regia`, `duelling.regia`, `poisoning.regia`.
- **"In 2.0" notes:** `BY`; hearing how an asked Goal ended.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-20 (task). [`docs/guide/09-goals-and-failure.md`](../../../docs/guide/09-goals-and-failure.md), about 530 lines, written from the template:

- An opening table of the words around a Goal (`GOAL`, `TO`, `PURSUE`, `PURSUING`, `DROP`, `FAIL`, the ending Triggers).
- Sections, simple to full: A Goal and its recipe (three ways to take a Goal on, the setup `PURSUE` as the Director asking, an own `PURSUE` that a `FROM DIRECTOR` recipe turns away); Waiting on a Goal; The same Goal twice (Pursuits, `PURSUING`, the own Pursuit left out); Dropping a Goal (the four steps, a throwaway `DROP fetch(pie)` for the upward half, `DROP strike`); How a Pursuit ends; What fails a Plan (cause table with banquet examples, what isn't a Failure); How Failure spreads (mermaid of the pie, `take_seat` with no seat, a waiting `WHEN` Plan); `FAIL` and Reasons; Reacting: `WHEN g FAILED`; Writing a fallback (the three places as a table; *Trying again* with a throwaway); What the Trace keeps (console lines of the pie chain, a pointer to *The Trace*).
- The outline's "quotes most" didn't fit: `scheming.regia` and `poisoning.regia` have no Goals. The chapter quotes `serving`, `dining`, `courtesy`, `duelling`, `hosting`, `noble_socializing` and `royal_banquet` instead.
- Two "In 2.0" notes: `BY` (a Director hearing an asked Goal's ending; 1.5 signals `took_seat`/`toast_given` from `ENDED` Plans), and the Reason reaching the asker (1.5 tells `sold_out` back by hand).
- Every showcase snippet checked against its file by script (18 snippets). Throwaways: `WHEN kitchen_closed: DROP fetch(pie)` and the counted retry.
- Checks borrow `R0109`, `R0501`, `R0504`, `R0802`, `R0805`, `R0806`, `R1101`–`R1106`, `R1605`, `R2001`, and the Failure causes `T0401`, `T0402`, `T0701`, `T0801`, `T0901`, `T1101`, `T1103`, `T1104`, `T1201`, `T1501`.
- `Guide: Goals and Failure` added under *05 Goals and triggers* and *11 Failure* in the showcase README.
- Grep for retired spellings: none. The humanizer pass rewrote one sentence (an unsupported "commonest Failure").

Two non-blocking findings: `T1102` is never written under chapter 34's failure chain; chapter 34's `fact` row says `REMEMBER`.
