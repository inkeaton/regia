# Write guide chapter 25, Jason: the game and the Trace

Type: task
Status: open
Assignee:
Blocked by: 05

## Question

Write `docs/guide/25-jason-the-game-and-the-trace.md`, *Jason: the game and the Trace*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 37, 35.
- **Covers:** the envelope, Custom Actions, game messages in an Agent and on the game link, pausing, the end of the story, test mode; the Trace writer, the source map, the file, the console, starting a run.
- **Quotes most:** throwaway game messages and Trace lines.
- **"In 2.0" notes:** none expected.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.
