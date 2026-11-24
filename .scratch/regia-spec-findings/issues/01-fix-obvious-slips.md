# Fix the obvious slips

Type: task
Status: closed
Assignee: claude
Blocked by:

## Question

Fix the findings that need no decision, because one side of the contradiction is plainly a slip. In each case the guide already took the right side, so the spec moves to it.

- F7: chapter 21, *Agent kinds*, drop "With no Body, the header ends with `.`".
- F8: drop the trailing `.` from the spec's examples and inline quotes (chapters 30, 38 lines 12–16 and 94, 40, and the rest a grep finds).
- F11: chapter 03, *Names are declared*, reword "Agent names are never Names" to match chapter 21 (*Individual Agents*).
- F12 (second half only): `GLOSSARY.md`, *Mood*, remove the stray `_Avoid_: Notification, message` line. The *Vocabulary* question is in *Decide: Diagnostic codes and the Vocabulary*.
- F21: chapter 37, *The game's replies*, `## …` lines become `#@desc:`.
- F23: chapter 21, *Agent kinds*, `bravery AT RANDOM(-1, 1)` becomes `aggressiveness`.
- F26 and F85 (the `REMEMBER` half): chapters 34 and 35, `REMEMBER` becomes `LEARN`.
- F27: chapter 15, *Leaving Agents out*, `TO` becomes `AS`.
- F32: chapter 17, *Casting*, the Root is named, never inferred (ADR 0036).
- F61: chapter 25, *Edit operations*, drop "'Undo all' …" to match chapter 24.
- F62: chapter 25, move the `Import marks` row into its table; move the last two *Regia 1.5* bullets to *Handed off*.
- F67: chapter 29, `temper` lists `bravery`, `sympathy` and `aggressiveness`.
- F69: chapters 36 and 28, rebuild the examples on the banquet (the guide's *Jason: the Build* has them worked out); `sympathy(0)[mood]`.
- F76: chapter 32, step 2 and `T3201`, read `regia_holds`.
- F79: chapter 30, *One Agent*, and chapter 31, *What an Agent does*, use chapter 29's message shapes.
- F80: chapters 30 and 31, `fight` becomes `fighting`.
- F85 (the missing row): chapter 35, *The writer*, add the `time` row.
- F87: chapter 20, *What starting a Staging does*, step 2, adds the `CAST:` setup first and the Root's kind and individual-Agent lines after the setups.
- F88: chapter 20, *Transpiler checks*, move `R2016` to errors.

If a fix turns out to need a decision after all, leave it and add a line to this map's `findings.md`.

Then fix any guide passage that still says the spec is otherwise, grep the edited chapters for retired spellings, and check that the README paragraph on open details doesn't mention a point fixed here.

Done when every item is fixed in the spec or moved to `findings.md`.

## Resolution

Every item is fixed in the spec; none needed a decision, so nothing went to `findings.md` as open.

- F7: chapter 21, *Agent kinds*, the "With no Body…" sentence is dropped.
- F8: trailing `.` dropped from 36 inline quotes (chapters 15, 25, 30, 31, 34, 35, 37, 39, 40) and from the Regia code in chapters 27 (*Expected Diagnostics*) and 38. Chapter 02's `DO eat_food.` / `DO eat_food.#` example is kept on purpose: it shows how the silent `.` meets a comment. `PHASE name.`, which the editor's `addPhase` writes (chapter 25), is now `PHASE name`.
- F11: chapter 03 now says an Agent's name is a Name only inside Instancing, never written in a `.regia` file, and met by a Plan at runtime as an ordinary Name (chapters 07 and 21 agree).
- F12 (second half): the stray `_Avoid_` line under *Mood* in `GLOSSARY.md` is removed.
- F21: chapter 37's `walk_to` doc comment is the showcase's `#@desc:` line.
- F23: chapter 21's roll example is `aggressiveness AT RANDOM(-1, 1)`.
- F26, F85 (`REMEMBER` half): chapters 34 and 35 write `LEARN`.
- F27: chapter 15 names `AS`.
- F32: chapter 17 says Instancing names the Root and never infers it (ADR 0036).
- F61: chapter 25 now says "one undo step, across files too (chapter 24)", with no "Undo all".
- F62: chapter 25's `Import marks` row is back in its table; the two bullets moved to *Handed off*.
- F67: chapter 29's `temper` lists `bravery`, `sympathy` and `aggressiveness`.
- F69: chapter 36's `.jcm`, combination file, `cast.json`, `regia_kind` and RANDOM example, and chapter 28's Build tree, are rebuilt on the banquet (`king`, `percival`, `Guard__Guest.asl`, the noble's rolls with `[mood]`), matching the guide's *Jason: the Build*.
- F76: chapter 32 step 2 and `T3201` read `regia_holds`.
- F79: chapter 30, *One Agent*, gives `regia_give` its `Until`; chapter 31 writes `regia_take(p, all)`.
- F80: chapters 30 and 31 write `fighting`, including the hypothetical `conceded` plan in 31.
- F85 (missing row): chapter 35's writer table has a `time` row (`regia.wait`, and the game link for `CLOCK PAUSED`/`CLOCK RESUMED`).
- F87: chapter 20 step 2 runs `CAST:` first, and in the Root's Staging the kind and individual-Agent lines after the setups.
- F88: chapter 20 lists `R2016` under errors.

Two slips found on the way are fixed too and logged in `findings.md`.

Guide: no passage disagreed with the new text (the guide had already taken each side), so no guide prose changed. The README paragraph on open details mentions none of these points. The retired-spellings grep over the edited chapters is clean.
