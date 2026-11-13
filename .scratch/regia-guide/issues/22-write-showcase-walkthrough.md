# Write: Showcase

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21

## Task

Write `docs/guide/19 - Showcase.md`: the full Program in `docs/guide/showcase/`, walked through file by file, then one run narrated from start to end with the Trace it would leave. Each part points back to the chapter that explains it. Fold in every addition chapters made to the showcase.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-13: [`docs/guide/19 - Showcase.md`](../../../docs/guide/19%20-%20Showcase.md), about 9,500 words, of which roughly half is the fourteen files printed whole and the Trace. Not yet read by the user.

The first half is the Program file by file (the Vocabulary, the eight Playbooks in five sections, `RoyalBanquet`, the two Subplots, the two casts), each with two to four paragraphs that point back to the chapters. The files are inlined from `docs/guide/showcase/` by a script, so they are verbatim; if the showcase changes, the chapter has to be regenerated or edited by hand. It adds two things no chapter had: a table of every Signal and Outcome with its sender and its listener, and a table of what `noble_1` holds over the evening.

The second half is one run of `test.regin`, about 150 Trace lines in eight excerpts numbered #1 to #546, put together by hand. It contains the excerpt of *The Transpiler* (#311 to #349) unchanged. The run: the knight has no seat and `take_seat` fails; three dinners take the three paths of `Dining`; `noble_2` insults `noble_1`; a duel, won by `noble_1`; the Host's honours; `noble_1`, drawn as the Poisoner, pours and is seized by the knight; the game leads it out and the departure fires the `75 PERCENT` Quota; a latecomer Joins in `farewell`. The showcase Program is unchanged.

The run needed seven behaviours of the game that no `.regia` file states, and it ends its feast with nobody having eaten. A closing section lists the parts of the Program the run never reached.

Three `#revise`:
- The Vocabulary declares what the game supplies and nothing of what the game does with it; telling one run took seven invented behaviours.
- Plans on one Agent run side by side, and nothing says that two Actions need the same body (a handkerchief and a sword, two trips to the kitchen, a seat and a door).
- `PLAN WHEN ENTERED` reads the same for six Blocks of a Trace, since the Trigger has no name in it.

Three entries were added to the README's *Spec wording* (the open pieces of chapter 34's entry texts, and script steps that name no Agent) and three to *Gaps in the showcase* (the Defender is never got up from the table; a yielded duellist can still land a lunge; the small cast can't reach most of `NobleSocializing`).
