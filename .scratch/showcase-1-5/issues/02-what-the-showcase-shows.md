# What the showcase must show

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 01

## Question

Which constructs of Regia 1.5 does the showcase Program have to show, and where?

Decide:

- A coverage table from every section of the 1.5 spec (chapters 01–21, 26, 38, each read with its `## Regia 1.5` section) to its place in the world of [*The banquet in 1.5*](01-banquet-in-1-5.md), and the constructs left to throwaway snippets in the guides.
- Which of the old README's *Gaps in the showcase* are closed in the Program, and which stay gaps.
- The interactions the world forces, redone for 1.5: which of the old six survive, and what replaces the Quota and Joining ones.
- What the revision added that the old showcase never had: `CUE`, `PASS` and Flat blocks, `REACHED`/`ENDED`, `FAIL WITH`/`FAILED WITH`, `ME`, `WHEN ASSIGNED`/`UNASSIGNED`, Phase setups and `UNTIL EXITED`, `CAST`, `EXCEPT`, `PLAYS`, Plot arguments, `RUNNING`/`IN`/`EXITED BY PARENT`, `WAIT … UNTIL`, `AFTER`, `SEED`, `GAME FACT`/`GAME CUE`, and the rest.
- That the Program must build clean except for the warnings the guide wants to show, and which those are.
- Whether the Program has one dotted Action, the Target's own code that Regia doesn't wait on, now that `seize` is a plain game Action (from *The banquet in 1.5*).

## Resolution

Resolved on 2026-11-18, with the user. The coverage table was the asset `coverage.md`; *Write the 1.5 showcase Program* moved it into [`docs/showcase/README.md`](../../../docs/showcase/README.md), which holds the only copy.

**The table.** One row per `##`/`###` section of chapters 01–21, 26 and 38, with a *Construct* column where a section holds several. Place is a file and Plan, `snippet`, `—` (no construct) or `2.0` (an "In 2.0" note where the 1.5 Program has a stand-in). Chapter 38's rows: the Program is clean, each check is shown in a snippet.

**What goes in the Program.** A construct goes in when the banquet has a reason for it in a few lines; otherwise a snippet, which varies a banquet line and is never added to the files. Every error is a snippet. Writing may move a row to `snippet` when its place turns out forced, and says so in its resolution.

**Gaps.** Closed: `LOWEST`; a `#[ … ]#` comment; Doc comments on a Plan, a Role and a Phase; `PRINT` with a String; `OR` with parentheses; `ELSE IF`; `PURSUING`; a Trigger narrowed by a Value; a Placeholder joining two Facts; a Placeholder under `NOT`; an `IF` that fills a Placeholder; an Option of several Statements; a roll in a condition; a `PERCENT OF` count; a fallback Goal from `FAILED`; a `DROP` that stops a waiting recipe; `EVERYONE`; a Fact told by an Agent; `LEARNED FROM`; an `ASK` to one Agent held by a Placeholder; a Phase with no `DURING` Block; a game Cue reaching a Director; an `EXITED` Plan in a Subplot; `TIES`; a relation `ON` a recipe or Fact change. Staying gaps: a Subplot inside a Subplot, a Plot from two parents, a file with two Plots, two sibling `.regin` files, a Multi-definition with `AS`, an item declared in two files, a Goal with recipes in two Playbooks, a Playbook with two Roles, a Failure climbing three levels. Gone: the `#%` Instancing comment (chapter 02 retired it), the Quota and Joining gaps (2.0). Moved: Visual Editor gaps (chapters 22–25 aren't on this list), Conformance and Trace gaps (*The walkthrough's shape*).

**Interactions.** Seven, listed at the end of the table: the Pick in `challenge`'s timeout; the knight's Precedence; Failure climbing with `sold_out` and `no_food` (`WAIT … UNTIL`, fallback Goal); the Defender walking out; a Guest leaving during the `arrival` count; `GIVEN` versus `IF` on the lunge; leaving `feast` (`Dining` `UNASSIGNED`, `Poisoning` dropped) while a duel runs on to `farewell`.

**Warnings.** None in the default build. `R0307` (the Suits alternative that only laughs) stays in the source, silenced with `#@allow` and a reason. Others only if writing finds one that occurs naturally.

*Superseded by [What counts as using a Placeholder](08-using-a-placeholder.md):* the alternative that only laughs writes `?_who`, so the source has no warning at all and `#@allow` is a snippet.

**Dotted Action.** `ACTION hall.music.fanfare AS play_fanfare`, in `Hosting`'s toast.

**Revision additions placed here.**

- `PASS` in small talk; Flat blocks a snippet.
- `WHEN have_dinner REACHED: LEARN sated.`, with `sated` used in a Context.
- Reasons: `fetch` fails `WITH sold_out(?dish)`, `bring` reacts `FAILED WITH sold_out` above a plain `FAILED`; `Dining` waits `WAIT 1 MINUTE, UNTIL on_plate(?dish)` and fails `WITH no_food`.
- One `DURING PLOT` `WHEN Guest ?g LEFT` Plan with `IN` and `ELSE IF`.
- `Poisoning` started `UNTIL EXITED` from `feast`; `WHEN Poisoning DROPPED` in `DURING PLOT`; `Poisoning`'s `EXITED BY PARENT`.
- `farewell` ends running duels with `END SUBPLOT HonorDuel`.
- `UNASSIGN NobleSocializing FROM ?culprit` on `poisoner_caught`; `ASSIGN … TO <Role> ?who` a snippet.
- Instancing: the king as an individual `AGENT`, `hothead LIKE noble`; `NO KIND` and `SEED` in test casts.

Changed: nothing in the spec, ADRs or glossary. Handed on to *The walkthrough's shape*: which Interfaces the guide prints, and which test cast carries `NO KIND`, `SEED` and the other `.regin` constructs.
