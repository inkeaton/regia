# The Jason showcase's outline (decided)

The decided outline of the Jason reference Build in `docs/showcase/jason/` and the guide that goes with it, from *The Jason showcase's shape* (`issues/06-jason-showcase-shape.md`). It started as a prototype to react to, and every proposal below was accepted on 2026-11-18. The **Alternative** lines record the shapes that were not chosen. Writing the guide and the Build's files is hand-off work.

*Refreshed on 2026-11-20* by *Refresh the two decided outlines* (`.scratch/regia-1-5-guide/issues/03-refresh-decided-outlines.md`): the 1.5 syntax of the syntax review, the generated names renamed in *Rename generated ASL names built on retired words*, the game link of *Directors and the game, without a gateway* (`.scratch/director-game-link/map.md`, ADR 0040), and chapter 28's Build tree as it now stands. No decision changed.

---

## Decisions at a glance

| Question | Decision |
|---|---|
| Which Build | **One** Build, of `banquet.regin`, the full cast. The four runs' casts are shown as what changes from it: the Root Director's start beliefs, the `.jcm` and `cast.json`. |
| Layout | The Build folder exactly as chapter 28 writes it, under `docs/showcase/jason/banquet/`, so that a real build can be diffed against it file by file. |
| Generated vs Infrastructure | Told apart the way chapter 28 already does it: by folder (`asl/regia/`) and by header comment. Plus a file table in the guide that gives each file's kind and source. Nothing extra is written in the files. |
| Hand-written mark | The header carries `<version>` = `reference`. The files claim to be nothing more than what the Transpiler must write. |
| Guide order | **Feature by feature**, in parts that follow the language (Plans, Goals, Messages, Givings, Directors, Subplots, Cast, Instancing), quoting the Regia line and the ASL it becomes, each with `file:line`. |
| Found by name | The README's coverage table gets a fourth column, **Jason**, that links every row to its guide section. A row with no ASL says why (`—`, comment, `2.0`). |
| Old *Translation to ASL* | Keep its opening, its names table, its game-protocol tables and its sequence diagram. Drop the small `evening` Build and *Since 1.0*. Turn the `#revise` notes that are still open into a closing *Costs you can see in the ASL*. |
| Traces | Yes, as short excerpts: a few `.trace` lines from a walkthrough run, quoted beside the `regia.trace` call that writes them, with a link to `runs/<run>/case.trace`. One section shows a single entry through all three forms: the call, the JSONL line, and the `.trace` line. |

---

## The reference Build

### Where the files go

```
docs/showcase/jason/
  README.md                         the guide (see below)
  banquet/                          = build/banquet/ for Entry banquet.regin (ch 23, 28)
    banquet.jcm                     ch 36; its first line is the game link's `platform: regia.GameLink(…)`
    cast.json                       ch 36; names the game link (`regia_game_link`) beside the bodies
    asl/regia/agent.asl             Infrastructure: fixed, the same in every Build
    asl/regia/director.asl          Infrastructure
    asl/regia/sourcemap.json        generated (ch 35)
    asl/unheard.asl                 generated: the Agents' catch-alls for told Cues no Plan takes (ch 39)
    asl/goals.asl                   generated: the `-!g` plan of every Goal (ch 40)
    asl/playbooks/                  generated, one per Playbook (9)
      Courtesy.asl  Dining.asl  Duelling.asl  Hosting.asl  Keeping_watch.asl
      NobleSocializing.asl  Scheming.asl  Serving.asl  Wagering.asl
    asl/directors/                  generated, one per Plot (3)
      RoyalBanquet.asl  HonorDuel.asl  Poisoning.asl
    asl/roles/                      generated, one per Root Plot Role, plus combinations
      Host.asl  Guest.asl  Servant.asl  Guard.asl
      Guest__Guard.asl              knight and percival play both (ch 36)

docs/showcase/java/
  hall/music/fanfare.java           the Target's own code for play_fanfare (ticket 21)
```

`fanfare.java` is the project's code, not Build output, so it sits beside the showcase's sources, not in `banquet/`. It is a few lines that log the fanfare and return `true`, and its comment says that a real one runs on the agents' side and can't play a sound in Godot. Source only, with no jar committed. The guide says how it is built into a jar in the Project's `lib/`, where `regia run` and `regia test` find it (chapter 28).

Not in the folder: `traces/` (written at run time; the runs' `.trace` cases stand in for it), and `regia-jason`'s Java (a library, never part of a Build, ch 28), the game link `regia.GameLink` included. The guide lists the internal actions the Build calls, with their chapters. It doesn't write them.

Notes for whoever writes it:
- `Guard.asl` is written although no kind plays `Guard` alone. Chapter 28 says one file per Root Plot Role, and a joiner could use it. Keep it, so the reference shows the rule as written.
- Size. About 640 lines of Regia. I'd guess 2,000–3,000 lines of ASL with the Infrastructure. That is hand-off work, and the ordering below lets it be written and reviewed one part at a time.

**Alternative (one Build per run):** four near-identical copies, with only three beliefs, the `.jcm` and `cast.json` differing. Every fix would have to be made four times.
**Alternative (Build of `evening.regin`):** its names would match the main run's Trace, but `NO KIND hothead` leaves `grudge(percival, 2)` out, and a reference should hold the whole cast.

### The four runs' casts

In the guide, not as files: for each run, a short diff against `banquet/` showing `regia_start_cast`, `regia_kind`, the setup lines run at start, the `.jcm` entries and `cast.json`. `grudges` and `short_evening` also lose `Guest__Guard.asl` from the `.jcm` (no knight kind starts, or `percival` only), and the diff shows that.

### Generated or Infrastructure

Chapter 28 already separates them: `asl/regia/` holds the Infrastructure (bar the generated `sourcemap.json`), and every other ASL file starts with `/* Generated by the Regia Transpiler <version> from <file>. Do not edit. */`. The reference writes that header with `reference` as the version. A file table in the guide (section 1) adds the column a reader wants: **kind** (Infrastructure, generated from a source file, generated from the cast, Target's own code) and **source**.

**Alternative (two folders, `generated/` and `infrastructure/`):** clearer at a glance, but the tree would stop being chapter 28's, and a real build could no longer be diffed against it.

---

## The guide, section by section

`docs/showcase/jason/README.md`, so that it opens when someone browses the folder. Every section quotes a Regia line as `playbooks/dining.regia:27` and its ASL as `banquet/asl/playbooks/Dining.asl:41`, with links.

### 0. Reading this chapter

- From the old chapter: we aren't meant to read a Build, and the Trace speaks in our names. We read it anyway, because some costs of the design only show in the ASL.
- Every file was written by hand from chapters 28–37 and 39. When a Transpiler exists, its build of `banquet.regin` is diffed against `banquet/`, and each difference is either a Transpiler bug or a spec change.
- How to find a construct: through the README's coverage table, using its **Jason** column.

### 1. The Build

- The file tree above, and the file table (file, kind, source, chapters).
- The names table from the old chapter, updated: External names no longer reach the ASL (ADR 0026, `regia_game` beliefs); `play_fanfare` is the one Action whose External name has a dot; the generated names follow the 1.5 keywords (`regia_removed`, `!regia_enter`).
- Two small files printed whole: `Keeping_watch.asl` (a Playbook file: guards, annotations, a told Fact) and `roles/Guest__Guard.asl` (a top-level file: includes, `regia_playbook` beliefs). This takes over the job the old small `evening` Build did, showing what complete files look like.

### 2. A Plan's Statements (chapters 01–04, 06, 09, 26; Jason in 39)

The guard and the rank annotation; one plan per `GIVEN` with the denials; `IF`/`ELSE IF`; Placeholders as variables and the prefix for Generated variables; `RANDOM` in three places; `RANDOMLY` with weighted `OPTION`s, the weighted Pick, `LOWEST`, `FOR EACH` (the `.setof` snapshot, and why it is needed: `dining.regia:30`); `PASS`. Quoted from chapter 39.

### 3. Goals, Actions and Failure (chapters 05, 08, 11, 12)

`TO`/`PURSUE`, waiting and `WITHOUT WAITING`; the four endings on `Dining`; `PURSUING`; the repeating `strike`; `regia.act` and a refused Action; `FAIL WITH` climbing from `fetch` to `bring` to the Guest; `WAIT … UNTIL`; the done-Signals on `ENDED`. `WAIT … UNTIL` is quoted from chapter 39 (`regia.wait(Cond, D)` and its `time` entry). Interactions 3 and 6.

### 4. Messages (chapter 07)

`TELL`/`ASK`/`SIGNAL` through `regia.send`; `EVERYONE`, `1 OF`, `50% OF`; a told Fact and `LEARNED, FROM peer`; `FORGET` on `REMOVED` (`+!regia_removed`); the Reason told back by hand in `Serving`.

### 5. Givings, Roles and Precedence (chapters 13–16)

`regia_given`; the `CAST:` and Role setups; `ASSIGN`/`REMOVE`; the crosswise Mapping in `Duelling`; `EXCEPT`; ranks across Playbooks, Phases and Subplots on the knight (interaction 2); `TIES`, Suits and Shifts Labels, `SHIFT`, and the Selection function.

### 6. The Director and its Phases (chapter 20)

`regia_phase`, `ENTER` (`!regia_enter`), `ENTERED`/`EXITED`; the hand counts (with the "In 2.0" note linking to the walkthrough's); `AFTER`; `regia_hears`, which lists only the Director's own Plot's game items, and the Signal catch-all that writes the `unheard` insult in `reception`; each Director sending its own Actions on the game link; `PRINT`. Interaction 5. A sequence diagram, as in the old chapter, of the `evening` run's `arrival`, with the game link between the game and the Directors.

### 7. Subplots and Stagings (chapter 17)

`START SUBPLOT` with an argument and a Mapping; two `HonorDuel` Stagings at once; `UNTIL EXITED`; `DROP SUBPLOT`; a Subplot Director attaching to the game link and asking the game for its starting Facts (`regia_state`); `Defender EMPTIED`; endings heard by the parent; `DROPPED` from above. Interactions 1, 4 and 7.

### 8. The cast (chapters 19, 21)

`LEFT` and `EMPTIED`, with `regia_leave` delivered by the game link to every attached Director; `banquet.jcm` (the game link's `platform:` line first, no port for any Director), `cast.json`, `regia_kind`, the `RANDOM` draws; then the four runs' casts as diffs.

### 9. The game and the Infrastructure (chapter 37)

The game link (chapter 28): one connection for every Director, named `regia_game_link` in the envelope, and what happens when it fails (`no game link`, `T2802`/`T2803`). The protocol tables from the old chapter, updated, with the state request (`regia_state`) and the Root ending the story with `regia.end_story`; the internal actions of `regia-jason` the Build calls; `play_fanfare` as `regia.act("hall.music.fanfare", play_fanfare)`, run by `regia.act` with no message, and `fanfare.java` built into `lib/` (chapters 28, 37).

### 10. The Trace (chapters 34–35)

One entry traced end to end: the `regia.trace` call in `Serving.asl`, its JSONL line, and its `.trace` line in `runs/evening/case.trace`. The source map. How a case scripts the game link: `link` steps, `*` reaching `link` last, `> fact link` before `> start`. Elsewhere, sections 3–8 quote short excerpts from the runs where the ASL writes the entry.

### 11. Costs you can see in the ASL

The old chapter's `#revise` notes that are still true, plus any that the Jason tickets find. Resolved ones (dotted Fact names, `Host`/`host`) are dropped, and so is anything about the Root relaying other Directors' Actions or forwarding percepts down the Staging tree, which the game link replaced.

### 12. What has no ASL

Coverage rows with `—`, comments, `#@allow`, and the `2.0` rows: one line each, so that the Jason column never comes up empty without a reason.

**Alternative (file by file through the Build):** follows the folder, but a feature such as a Giving is spread across the Director file, the Infrastructure and a Playbook file. The reader's question is "what does *this* become?", so the answer should sit in one place.
**Alternative (follow the walkthrough's runs):** reuses the story, but the Jason guide is a reference that people look things up in, and the runs don't reach some rows (`—` rows, snippets).
**Alternative (strict spec-chapter order, 01 to 38):** matches the coverage table one to one, but chapters 01–04 have almost no ASL of their own, and a Giving (15, 16) would come long before the Director (20) that makes it.

---

## Depends on

- Tickets 11–22 decide the ASL that sections 2–10 quote. The guide's shape doesn't wait on them, but no file of the Build can be written before they close.
- *Scripting the game for one Agent* (ticket 09) and *The Trace's fields and entries* (ticket 22): the `.trace` excerpts.
- *Directors and the game, without a gateway* (`.scratch/director-game-link/map.md`, all closed): the game link, which sections 1, 6–10 quote.
- *The Target's own code in a Build* (ticket 21, closed): `docs/showcase/java/hall/music/fanfare.java`, built into `lib/`.
