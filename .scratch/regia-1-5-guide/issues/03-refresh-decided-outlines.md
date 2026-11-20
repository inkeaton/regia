# Refresh the two decided outlines

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 02

## Question

The showcase map's two decided outlines, `.scratch/showcase-1-5/prototypes/walkthrough-outline.md` and `jason-showcase-outline.md`, are the starting point for the hand-off work this map leaves out. Bring them in line so that work starts from a correct outline:

- the 1.5 syntax (`CAST STARTS WITH`, `ENDED`, … as the showcase now writes them) and the showcase's new line numbers;
- the *Directors and the game, without a gateway* map (`.scratch/director-game-link/map.md`): no Root Action relay, no percept forwarding, `director:` script steps become `link` steps, the game link in the Build;
- the ASL names renamed in *Rename generated ASL names built on retired words*.

Decisions stay as decided: only their wording and references change. If a change of the game-link map undoes an outline decision rather than rewording it, note it in `findings.md` and in the outline, without re-deciding it here.

## Resolution

Done on 2026-11-20 (AFK). Both outlines carry a *Refreshed* note under their opening paragraph. Only wording and references changed; every decision stands.

**`walkthrough-outline.md`**

- 1.5 syntax: `CAST:` and `ROLE Guest:`, `WHEN took_seat, FROM Host`, small talk as `RANDOMLY` with weighted `OPTION`s, `MAPPING Guest EXCEPT … AS Spectator`, `REMOVE … FROM Guest ?culprit`, `DROP SUBPLOT` (twice), `TELL 50% OF`, `LEARNED, FROM peer`, `EXITED, BY PARENT`, no trailing `.` in the done-Signal.
- Glossary words: "`TEMPER` lines" → the kinds' Propensity values (`bravery AT …`; *Temper* is an _Avoid_ word); "the dotted Action" → "the one Action whose External name has a dot"; the `unheard` insult named as a Signal (`T3801`).
- Game link: the *Scripting the game for one Agent* note says `*` also reaches `link`, and a Cue for the Directors is `> cue link …`; run 3's `poison_drunk` goes out on the link and only the `Poisoning` Director hears it; *Depends on* points at *ScriptedGame and the Trace on the game link*.
- Line numbers: the outline cites none.

**`jason-showcase-outline.md`**

- Build tree as chapter 28 now writes it: `asl/unheard.asl` (ch 39) and `asl/goals.asl` (ch 40) added; `banquet.jcm` opens with the `platform: regia.GameLink(…)` line and `cast.json` names `regia_game_link`; `regia.GameLink` listed as `regia-jason` Java, outside the Build; `sourcemap.json` noted as the generated file in `asl/regia/`. The layout decision ("exactly chapter 28's tree") is what asked for these.
- 1.5 syntax and renamed names: `RANDOMLY`/`OPTION`, `50% OF`, `LEARNED, FROM peer`, `REMOVED` (`+!regia_removed`), `CAST:`, `ASSIGN`/`REMOVE`, `ENTER` (`!regia_enter`), `DROP SUBPLOT`; "`Temper`" → Suits and Shifts Labels and the Selection function; "dotted Action" reworded.
- Game link in sections 6–11: `regia_hears` covers the own Plot only; each Director sends its own Actions; a Subplot Director attaches and asks `regia_state`; `regia_leave` reaches every attached Director; the `.jcm` gives no Director a port; section 9 opens with the game link, its failure (`no game link`, `T2802`/`T2803`), `regia_state` and `regia.end_story`; section 10 adds `link` steps; section 11 drops any relay or percept-forwarding cost. *Depends on* lists the game-link map.
- Line numbers: `dining.regia:30` (the `FOR EACH` with the `.setof` snapshot) and the `dining.regia:27` format example still point at the right lines.

**Checks**: a grep of both outlines for `EITHER`, `PERCENT`, `UNASSIGN`, `END SUBPLOT`, `TRANSITION`, `STARTS WITH`, `TEMPER`/`Temper`, "dotted Action", `relay`, `percept` and a clause `FROM` with no `,` finds only one deliberate mention (section 11's "relaying … forwarding percepts", saying they are gone). The generated names quoted (`regia_given`, `regia_phase`, `regia_hears`, `regia_start_cast`, `regia_kind`, `regia_playbook`, `regia_game`, `regia.send`, `regia.act`, `regia.wait`, `regia.trace`) all still appear in chapters 28–40.

**Findings**: none. No change of the game-link map undid an outline decision.

