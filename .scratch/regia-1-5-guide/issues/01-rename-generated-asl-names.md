# Rename generated ASL names built on retired words

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by:

## Question

The syntax review renamed `UNASSIGN`/`UNASSIGNED` → `REMOVE`/`REMOVED`, `TRANSITION TO` → `ENTER`, `ENDED WITH` → `FINISHED WITH`, `END SUBPLOT` → `DROP SUBPLOT`, `EITHER` → `RANDOMLY`, `PERCENT` → `%`, `STARTS WITH` → the Role's Block, but the Jason chapters still generate names built on the old words (seen: `regia_unassigned` in chapter 29, `!regia_transition` in chapter 30, `percent(p)` in chapter 33). Rename every generated name, Trace field and `regia-jason` internal action built on a retired keyword so it follows the 1.5 keyword (`regia_removed`, `regia_enter`, …), in chapters 28–40 and `GLOSSARY.md` if any appears there. Closed tickets in `.scratch/` are history and stay as written.

Done when a grep of chapters 28–40 for the retired words (lowercase, as ASL names) finds only deliberate mentions, and the list of renames is recorded in the resolution. Names that are Jason's own (`.drop_desire`, …) or describe something that isn't a keyword stay.

## Resolution

Done by a claude session on 2026-11-20 (AFK). Four generated names were built on retired words, all in chapters 29, 30 and 33; `GLOSSARY.md` has none.

| Chapter | Was | Now | Why |
| --- | --- | --- | --- |
| 29 (lines 30, 210, 247) | `regia_unassigned(P)` | `regia_removed(P)` | the goal behind `WHEN REMOVED:`, pairing `regia_assigned(P)` (kept: `ASSIGNED` is a 1.5 Trigger word) |
| 30 (line 108) | `!regia_transition(x)` | `!regia_enter(x)` | the `[atomic]` plan `ENTER x.` calls; no clash with `regia_entered(phase(_))` |
| 33 (lines 144, 215) | `percent(50)`, `percent(p)` | `share(50)`, `share(p)` | the Quota's `n% OF` quantity; `share(S)` is already the name `regia.pick` uses for `n% OF` (chapters 35, 39), and the spec reads `%` as "at least that share" (ADR 0045) |

No `regia-jason` internal action or Trace field was built on a retired word: `regia.pick`, `regia.stop_phase`, `regia.end_body`, the Trace kinds and the Trace's `FINISHED WITH`/`ENDED BY PARENT` already follow 1.5.

Left as deliberate mentions: "transition" as prose for moving between Phases (it is the glossary's word, under *Phase*), and chapter 31's header history, which names `END SUBPLOT` and `ENDED WITH` as replaced spellings. Line numbers didn't move.

Check: `grep -rnE "regia_unassigned|regia_transition|percent\(" docs/spec GLOSSARY.md` finds nothing. The old guide (`docs/guide/`) still has 8 hits; it is deleted later by this map.

One finding: the Quota's `of(k)` and `regia.pick`'s `count(N)` name the same `n OF` differently (`findings.md`).
