# Write guide chapter 09, Goals and Failure

Type: task
Status: open
Assignee:
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
