# Write guide chapter 23, Jason: Givings and Precedence

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05

## Question

Write `docs/guide/23-jason-givings-and-precedence.md`, *Jason: Givings and Precedence*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 29, 32.
- **Covers:** Plans compiled in and switched on by Givings, the guard, the Giving record, `ASSIGNED`, taking a Playbook away (`regia_removed`), Levels, the Rank of a Giving, the plan annotation, `selectOption`.
- **Quotes most:** `noble_socializing.regia`, `royal_banquet.regia`.
- **"In 2.0" notes:** Givings that reach a joiner.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-23 (AFK). [`docs/guide/23-jason-givings-and-precedence.md`](../../../docs/guide/23-jason-givings-and-precedence.md) written from the template, with a knight holding `Keeping_watch` three times as the spine: its six `regia_given` beliefs late in the feast, then its `scandal` worked through `selectOption`.

- Sections: *Plans are compiled in*, *The guard* (with the closing guard on `Dining`'s `ENDED`), *The Giving record* (*Givings set aside*, *The cast copy*), *Messages between Director and Agent* (*What each Director Statement sends*), *Reading the record* (*Who plays a Playbook Role*, *`EXCEPT` in a binding*, *What reads it*), *Opening: `ASSIGNED`*, *Taking a Playbook away* (*The take step*, *Stopping the Plans*, *The closing*, *A Staging that has ended*), *Levels*, *The Rank of a Giving* (*Comparing two Ranks*, *A Playbook given several times*), *The plan annotation*, *`selectOption` in Agents*, *Directors*, *Infrastructure state*, *How this combines with…*.
- Worked by hand: the banquet's level tables (Staging table per item, Playbook table with the `insulted` merge; `Keeping_watch OVER NobleSocializing ON scandal` changes no level), every showcase Playbook's Rank resolved on `scandal` and `idle`, `regia_start`'s prefix for a duel; ASL for `Dining`'s `ASSIGNED` and `ENDED`, `Duelling`'s `REMOVED`, `Keeping_watch`'s guarded `scandal`, `NobleSocializing`'s three `insulted` labels; a sequence diagram of leaving `feast`; a Plot-tree diagram of prefixes.
- Throwaway variations: `MAPPING Guest EXCEPT Guard AS peer`; a `DURING feast` `culprit_seized` Plan for Director ranks.
- Three "In 2.0" notes: joiners (standing Givings replayed), Quota counts read through `regia_plays`, the take step clearing counts.
- Checks: `T2901`, `T1504`–`T1506`, `T2001`, `T1104`, `T3801`, `R1301`, `R1305`, `R1308`, `R1310`, `R1311`, `T3201`.
- No `Guide:` line: the showcase README's *Coverage* has no heading for chapter 29 or 32.
- Re-read against chapters 29, 32, 13, 14, 30, 31, 34, 39, 40; snippets checked verbatim; grep for retired spellings clean; humanizer pass done (nothing to change).

**Findings** (non-blocking, in `findings.md`): 32's step 2 and `T3201` read `regia_given` where `regia_holds` is meant (a closing's endings would be dropped); no Item for `REMOVED` plans; a merged `TIES` member's sort name, and whether `lv` lists unchanged items; stale `regia_give`/`regia_take` shapes in chapters 30 and 31.
