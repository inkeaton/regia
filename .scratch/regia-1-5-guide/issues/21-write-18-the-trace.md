# Write guide chapter 18, The Trace

Type: task
Status: open
Assignee:
Blocked by: 05

## Question

Write `docs/guide/18-the-trace.md`, *The Trace*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 34.
- **Covers:** what it records, entry fields, the failure chain, Trace codes, the console line, behaviour cases and their scripts (`link` steps, `> lose link`).
- **Quotes most:** throwaway traces of a banquet run.
- **"In 2.0" notes:** `count` entries, `T1801`, `T1802`, departures, `JOINED` in `cast` entries.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.
