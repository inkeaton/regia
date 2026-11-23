# Write guide chapter 25, Jason: the game and the Trace

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
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

## Resolution

`docs/guide/25-jason-the-game-and-the-trace.md` written (2026-11-23).

- Shape: the envelope; a game Action (`take_seat`'s `walk_to`) with its replies, calling off (`eat` under `DROP have_dinner`), the Target's own code (`play_fanfare`) and its two Trace entries; game messages in an Agent (`seat`, `saw_pouring`) and on the game link (`poison_drunk`), the starting state, a Director's Actions (`Poisoning`'s `discard_cup`); pausing; the end of the story (the banquet's bare `END PLOT`, `outcome: null`); the Trace writer with a who-writes-what table and Staging numbers; the source map for `TO take_seat`; file and console; starting a run and the one random source; test mode (`RunCase`, steps as messages, Action rules, the state in a case, settling).
- The banquet's own `regia_state` asks for no Facts (no Plot of the showcase names a game Fact), so a Fact in the reply is shown as a throwaway `in_stock(pie)`. The source map's ASL line numbers are made up and say so; its `.regia` locations are the showcase's.
- No "In 2.0" notes: `regia_join` in 1.5 is a bullet pointing at *Jason: the Build*.
- No `Guide:` line: the showcase README has no *Coverage* heading for chapter 35 or 37.
- Re-read against chapters 35, 37, 30, 34 and 23; no retired spellings; humanizer pass done.
- Two non-blocking findings: chapter 35's writer table has no `time` row and says `REMEMBER`; no `agent` is given for the game link's own entries (`CLOCK …`, `T2802`/`T2803`).
