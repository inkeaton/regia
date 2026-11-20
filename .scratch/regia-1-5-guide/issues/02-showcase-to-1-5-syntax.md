# Bring the showcase to the 1.5 syntax

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 01

## Question

Rewrite `docs/showcase/` (the fourteen `.regia`/`.regin` files and `README.md`) in the syntax the syntax review settled, so a 1.5 build would accept it with no `R0109` and no retired-spelling error:

- every spelling in chapter 01's *Retired spellings* table (about 50 in the Program, about 20 in the README);
- the changes that aren't errors, from the resolution of *The hand-off to the showcase* (`.scratch/syntax-review/issues/14-showcase-hand-off.md`): no trailing `.`, `PASS` in an empty Option, `!=`, every clause after its `,` (`R0111`), `%` only before `OF`; the README's *Flat blocks* and *Redundant terminators* rows go;
- the README's prose checked against `GLOSSARY.md` ("naming" → "fill", `CHANGE`, `UNASSIGNED`, …), and the coverage table's rows renamed where a construct was;
- new constructs only where a coverage-table row needs one.

Then **re-point the spec's line citations** into the showcase (about 53, in chapters 10, 20, 29–31, 34–36, 39 and 40, e.g. `royal_banquet.regia:100`), in the same change, keeping line numbers. Check by hand against the cited chapters, plus a grep for retired spellings. Anything the spec gets wrong goes to `findings.md`.

## Resolution

Done on 2026-11-20.

**The Program** (`docs/showcase/*.regia`, `banquet.regin`): every spelling of chapter 01's *Retired spellings* table, and every change from the hand-off that isn't an error.

- `?x = e` → `LET ?x BE e` (2), `CHANGE` → `UPDATE` (3), `EITHER`/`OR` → `RANDOMLY:` with `OPTION:` Blocks (1), `SUITS a AT x AND b AT y` → `,` (1), `MAPPING a TO b` → `MAPPING a AS b` (10), `UNASSIGN`/`UNASSIGNED` → `REMOVE`/`REMOVED` (4), `50 PERCENT OF` → `50% OF` (1), `ROLE r STARTS WITH:`/`CAST STARTS WITH:` → `ROLE r:`/`CAST:` (10), `ENDED WITH e` → `FINISHED WITH e` (3), `END SUBPLOT` → `DROP SUBPLOT` (1), `TRANSITION TO p` → `ENTER p` (10), `, AT RANDOM` → `, RANDOMLY` (1), `.regin`: `strategy = most_similar` → `strategy most_similar`, `PLAYS Guest AND Guard` → `PLAYS Guest, Guard`.
- `R0111`: every `FROM` after a Trigger's core now has its `,` (`WHEN e, FROM …`, `TO g, FROM DIRECTOR:`, `LEARNED, FROM …`, `FAILED WITH r, FROM …`), `WHEN EXITED, BY PARENT:`, and the `.regin` headers `KIND k, PLAYS …`, `KIND k, LIKE …`, `AGENT a, PLAYS …`, `AGENT a, LIKE …`.
- No trailing `.` anywhere (comment columns kept). `PASS` was already in the empty Option. No `NOT ?a = ?b` and no `%` outside `OF` were present.
- **One line added**: `RANDOMLY:` in `noble_socializing.regia`'s small talk, so its lines from 11 on moved down by one. Every other file keeps its line numbers. No new constructs were needed.
- `ENDED` stays where it is a Goal's ending (`WHEN take_seat ENDED`, …) and on `WHEN HonorDuel(?) ENDED` ("however the duel ended"), which chapter 17 keeps.

**README**: the Playbooks table (`REMOVED`; "Filling a Placeholder with `LET`, `UPDATE`"; "the one dotted Action" → "the one Action whose External name has a dot", per `GLOSSARY.md`) and the coverage rows renamed after their sections (04 *the Body fills*, 05 *The shape of a Trigger*, 08 *Updating a Fact*, 09 `RANDOMLY` / `OPTION`, 15 *Until the Phase is left*, *Given and taken*, 16 *A Role's Block*, 17 *The parent's Triggers: `FINISHED`, …*, `DROP SUBPLOT`, 20 `EXITED, BY PARENT`, *What `ENTER` does*), quoted code without trailing `.`. Chapter 01's rows: *Flat blocks* replaced by *No Block without indentation across lines* (`R0108`, snippet); *Redundant terminators* removed; rows added for *Clauses and the comma*, *Where condition words go*, *Retired spellings* (snippet) and the principles that are rules only (`—`).

**Spec citations**: 46 of the 53 point into the showcase (`brawl.regia` and `watch.regia` are the spec's own examples). All were checked by hand against their chapters; 42 already pointed at the right line and still do. Re-pointed: `noble_socializing.regia` `:23`→`:24`, `:47`→`:48`, `:53`→`:54` (chapter 39) and `:28`→`:29` (chapter 30). Chapter 35's source-map example named a Plan Dining doesn't have (`WHEN finished_eating` given `hungry`, at `dining.regia:56:5`); it now names `WHEN served(?dish), FROM waiter` given `sated` at `dining.regia:62:9`. Quotes of the cast in chapters 30 and 36 now read `AGENT percival, LIKE knight`.

**Checks**: a grep of `docs/showcase/` and `docs/spec/` for every retired spelling, and for `FROM` without its `,`, finds only the deliberate mentions (the table, the error codes, decision history). Two findings went to `findings.md` (chapter 21's stale "the header ends with `.`", and trailing `.` left in some spec quotes); neither blocks a chapter.
