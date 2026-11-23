# Write guide chapter 24, Jason: Directors and Stagings

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05

## Question

Write `docs/guide/24-jason-directors-and-stagings.md`, *Jason: Directors and Stagings*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 30, 31, 33.
- **Covers:** the Director's agent class, hearing the game, Phases (`!regia_enter`), the standing-Giving record, signals and messages from a Director, one Director agent per Staging, starting and ending a Staging, the parent's ending Plans, the starting cast, leaving, sends to agents that are gone.
- **Quotes most:** `royal_banquet.regia`, `honor_duel.regia`.
- **"In 2.0" notes:** joining, Quota counts.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-23 (AFK). [`docs/guide/24-jason-directors-and-stagings.md`](../../../docs/guide/24-jason-directors-and-stagings.md) written from the template, with the banquet starting a duel over an insult as the spine, from `START SUBPLOT` to `FINISHED WITH duel_settled(?winner)`.

- Sections: *The Director's agent class*, *One Director agent per Staging*, *Hearing the game* (*Attaching*, *Stopping hearing*), *Phases* (*A Plot with no Phases*, *`IN`*), *`AFTER`*, *`ENTER`* (*A `DO` in `EXITED`*), *Who plays a Role here* (*A Role with `EXCEPT`*), *Starting a Staging* (*The Root's start*, *A Subplot's start*, *Plot arguments*, *A Role that starts empty*), *Setups*, *The standing-Giving record* (*One Agent*), *Signals* (*Nothing heard*), *Messages and Actions from a Director*, *Ending a Staging* (*A child ended by its parent*, *`regia_ended`*, *`DROP SUBPLOT`*, *`RUNNING`*, *An ending Director hears nothing*, *`regia_end_staging`*, *The Root's `END PLOT`*), *The parent's ending Plans* (*`Heard` and `T3802`*), *Leaving* (*What the Agents do*, *Nobody joins*), *Sends to agents that are gone*, *Infrastructure state* (beliefs and messages), *How this combines with…*.
- Worked by hand: `arrival`'s `took_seat` plans and `IN`; `betting`'s two `AFTER`s; `regia_enter` in outline and the order of events leaving `feast` (sequence diagram); `RoyalBanquet`'s setups with a rolled purse and `T1601`; `reception`'s standing Giving and its record through `poisoner_caught` and `farewell`; the duel's `regia_start` message; a duel dropped at `farewell` (sequence diagram); `FINISHED WITH duel_settled` and `ENDED` plans; `WHEN Spectator ?who LEFT`.
- Throwaway variation: a Challenger setup reading `regia_args`.
- "In 2.0" notes: Quota counts cleared on `ENTER`, the standing record replayed for joiners, Quota counts in the leave walk, joining.
- Checks: `R2114`, `T2802`, `T2803`, `R2008`, `R2014`, `R2003`, `T2002`, `T1504`, `R1710`, `T1601`, `T2001`, `T3001`, `T1505`, `T1506`, `T3801`, `T1901`, `T1101`, `T3802`, `T3302`, `T1902`, `T3303`.
- No `Guide:` line: the showcase README's *Coverage* has no heading for chapter 30, 31 or 33.
- Re-read against chapters 30, 31, 33, 17, 19, 20, 29, 32; snippets checked verbatim by script; grep for retired spellings clean; humanizer pass done (nothing to change).

**Findings** (non-blocking, in `findings.md`): `fight` for `fighting` in 30 and 31; how a Director tells `T2001` from `T3001`; which join codes a 1.5 run writes; the Quota-clearing step (3 or 4); `regia_cast_copy` in no Messages table, and the setup-line subgoal unnamed.
