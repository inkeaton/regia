# The walkthrough's outline (decided)

The decided outline of the guide that walks through the 1.5 showcase, from *The walkthrough's shape* (`issues/04-walkthrough-shape.md`). It started as a prototype to react to, and every proposal below was accepted on 2026-11-18. The **Alternative** lines record the shapes that were not chosen. Writing the guide and the four cases is hand-off work.

*Refreshed on 2026-11-20* by *Refresh the two decided outlines* (`.scratch/regia-1-5-guide/issues/03-refresh-decided-outlines.md`): the 1.5 syntax of the syntax review, the game link of *Directors and the game, without a gateway* (`.scratch/director-game-link/map.md`), and the glossary's words. No decision changed.

---

## Decisions at a glance

| Question | Decision |
|---|---|
| Order | The evening's story, told across **four runs**. The files aren't printed whole: each Plan is quoted when it first runs. |
| Runs and casts | Four test casts, each a `.regin` that imports `banquet.regin`: `evening`, `grudges`, `short_evening`, `two_duels`. |
| `.trace` files | Yes. Each run is a behaviour case in `docs/showcase/runs/<run>/`, written by hand until a build exists. |
| Spec Conformance | No. They are the writer's own cases (chapter 27, "a writer can keep cases for their own Program"), not `docs/spec/cases`. |
| "In 2.0" notes | A short boxed note where the stand-in first runs. It names the construct and its chapter, with no 2.0 code. Later appearances link back to it. |
| Snippets | Gathered in a closing **Variations** section, by spec chapter, and kept out of the runs. |
| `.regin` constructs | `SEED` and overrides in every cast; `NO KIND` in `grudges` and `two_duels`. |
| Interfaces | Two are printed: `Keeping_watch` (in *evening*, at the seizure) and `HonorDuel` (in *two_duels*, at the first challenge). |

**Blocker found:** a `.trace` script can't address one Agent. `> cue idle` and `> fact +hungry` name no Agent, but `regia_cue` and `regia_fact` go to one body (chapters 30 and 35), and every run here needs "`idle` to `noble_2` only". The old guide's *How this combines with… The Transpiler* hit the same wall. Ticketed as *Scripting the game for one Agent* (`issues/09-scripting-one-agent.md`), which must be decided before any run is written as a case. *Resolved:* steps name their receiver (`> cue noble_2 idle`), and `*` reaches every body that uses the item, plus the game link (`link`, last) when a Director's Plot uses it. A Cue for the Directors is scripted once, as `> cue link …` (chapter 34); the game never names a Director.

---

## The guide, section by section

### 0. Reading this chapter

- What the showcase is, with a link to `docs/showcase/README.md`, which stays the **coverage index**: a reader looking for a construct starts there.
- How to read a run: the cast, then the `.trace` file interleaved with prose. A `>` line is the game's half (the script), and every other line is what the Program wrote. A short key to the entry kinds, linking chapter 34.
- The game's half is now *printed*, as script steps. This answers the old `#revise` ("we had to invent seven behaviours of the game"): what the game does is visible in each run, line by line.
- Honest note: no Transpiler exists, so the Traces are written by hand from chapter 34, and the random draws are *assumed* to go the way stated. The development effort fixes each `#! seed:` once a build can run them.

### 1. The files

- The Import graph (mermaid) and the README's file table. No full listing.
- One line per Playbook and Plot: which run shows it first.

**Alternative (file by file):** print every file whole first, as the old *Showcase* did, then one run. That makes 600 lines of source before any story, and the old chapter's "What the run didn't reach" grew out of exactly this shape.
**Alternative (feature by feature):** one section per spec chapter, quoting banquet lines. The README's coverage table already does that job as an index, and the guide chapters 0–17 (rewritten later) will do it as prose.

### 2. The casts

The four test casts side by side, plus the full `banquet.regin` for reference. Each one fixes Propensity values, so the Selection function is predictable, and sets a `SEED`.

| Cast | Agents | `.regin` constructs it carries |
|---|---|---|
| `evening.regin` | `king`; `noble` ×2 (fixed values); `knight` ×1; `percival`; `servant` ×1 | `SEED`; overriding `COUNT` and values (layering); `NO KIND hothead` |
| `grudges.regin` | `king`; `noble` ×2 (one at sympathy −0.5, one at 0.7); `hothead` ×1; `percival`; `servant` ×1 | `SEED`; `NO KIND knight` while `percival LIKE knight` stays (a kind kept as a template only, chapter 21); `hothead`'s `LEARN grudge(percival, 2)` setup line |
| `short_evening.regin` | `king`; `noble` ×3; `servant` ×1 | `SEED`; no Guard at all: `NO KIND knight`, `NO AGENT percival`, and `NO KIND hothead` (else its `grudge(percival, 2)` is `R2122`) |
| `two_duels.regin` | `king`; `hothead` ×2; `noble` ×2; `knight`; `percival`; `servant` ×1 | `SEED`; an Agent in two Stagings of one Plot |

Exact values, seeds and beats are fixed when the cases are written.

### 3. Run 1: *The evening*, `evening.regin`

The main path, arrival to farewell. Sections follow the Phases.

1. **Before the doors open.** `CAST:`, Role setups (`ROLE Guest:`), `ASSIGN` before `PURSUE`, the kinds' Propensity values (`bravery AT …`). The knight has no seat: `take_seat` fails (`T1104`), then `stand_by(wall)`.
   > **In 2.0** (first done-Signal, `WHEN take_seat ENDED: SIGNAL took_seat`): the Director would hear the Goal's ending itself, `BY` (chapter 05).
2. **Arrival.** The hand count. `WHEN took_seat, FROM Host` starts the music.
   > **In 2.0** (the `#[ … ]#` block): a Quota Trigger (chapter 18).
3. **Reception.** `NobleSocializing` given; small talk (`RANDOMLY` with weighted `OPTION`s, `PASS`, the roll in a condition); `AFTER 2 MINUTES`; the toast with `play_fanfare` (the one Action whose External name has a dot); `WHEN open_feast ENDED` → `toast_given`.
4. **The feast.** Phase setups (`Dining`, `Serving`); `Poisoning` started `UNTIL EXITED` (`1 OF Guest`). Failure climbing: pie is out, so `fetch` fails `WITH sold_out(pie)`, `bring` fails with it, and the Guest is told `sold_out` (interaction 3, first half).
   > **In 2.0** (the Reason told back by hand in `Serving`): the asking Guest hears `bring FAILED WITH …` itself (chapters 07 and 11).
5. **An insult and a duel.** `vent` with a weighted Pick; the knight on duty watches the gossip (Precedence, interaction 2); `HonorDuel(noble_2)` starts with `MAPPING Guest EXCEPT ?offended, ?offender AS Spectator` (a Giving and a recipient with `EXCEPT` go to *Variations*); `betting` with a Pick in the timeout (interaction 1); `strike` repeating, `GIVEN` against `IF` (interaction 6); `duel_settled`.
6. **Honours and poison.** The winner is given `Keeping_watch`, a third Giving; `pour_poison` with `LOWEST`; `saw_pouring` → `seize`; `culprit_seized` reaches two Directors.
   - *Interface printed here:* `regia explain evening.regin interface Keeping_watch`, to show why `RoyalBanquet` needs its `ring_bell` Plan (`R3801`).
   - `REMOVE NobleSocializing FROM Guest ?culprit`, then `take_leave`.
7. **The feast ends.** The 75% hand count; `WHEN EXITED: DO clear_tables`; `Dining` taken away, so `have_dinner` is `DROPPED` (interaction 7, first half).
8. **Farewell.** `DROP SUBPLOT HonorDuel(?)` (nothing running here); `Guest EMPTIED`; bare `END PLOT`.

Reaches: interactions 1, 2, 3 (`sold_out`), 6, 7 (in part).

### 4. Run 2: *Old grudges*, `grudges.regin`

Short. It runs from `reception` into the first minute of `feast`, and the case simply stops there: a behaviour case needn't end the Program.

- A hothead `vent`s at `percival` (a Name from Instancing).
- Three ways to take an insult, one per Guest: stand up, **scowl** (`GIVEN grudge`, then `PURSUE resent`, the `IF` that fills `?size`), and **laugh** (`?_who`, a "don't care" named so the three ways read alike; *What counts as using a Placeholder* moved `#@allow` to *Variations*).
- Both gossip Plans: `scandal(ME)` (`SHIFT`, `TELL 50% OF peer wronged(…)`), and `scandal(?victim)` with snigger and eye-roll, plus the fall-through when neither `GIVEN` holds.
- `wronged … LEARNED, FROM peer` → `bow_to`.
- In `feast`: `Dining TIES NobleSocializing ON insulted`, so a mild Guest at dinner just sips wine.
- An insult thrown in `reception` shows as `unheard` at the Director (`T3801`: only `feast` takes the Signal `insult_thrown`).

### 5. Run 3: *A short evening*, `short_evening.regin`

The other endings of the Root Plot.

- A Guest leaves during `arrival` before sitting; the `LEFT` Plan forgets and recounts, and the count passes (interaction 5, `IN`, `ELSE IF`).
- A dinner eaten to the end: `WAIT … UNTIL` met, `eat`, `REACHED` → `sated`; a late `served(roast)` eaten anyway, any other dish pushed away.
- A Guest with no food: `WAIT` runs out → `FAIL WITH no_food` → `make_do` (interaction 3, second half). Also the refused `pick_up`: Failure with no Reason, and the Servant only bows.
- No Guard, so nobody sees the pouring: the game sends `poison_drunk` on the game link (`> cue link poison_drunk`), only the `Poisoning` Director hears it, and it ends with `poison_taken` → `farewell`.
- `Poisoning` *not* reached by `DROPPED` here; see run 1 vs run 4.

### 6. Run 4: *Two duels*, `two_duels.regin`

Subplots under strain.

- Two offenders, so two `HonorDuel` Stagings at once, with one Agent a Spectator in both.
- `GIVEN NOT HonorDuel(?offender) RUNNING` stops a second duel for the same offender.
   - *Interface printed here:* `regia explain two_duels.regin interface HonorDuel`, with its parameter, Phases, Signals by Phase, and Outcomes.
- Duel A: nobody bets, so the `ELSE` goes straight to `fighting`; the Defender walks out → `Defender EMPTIED` → `duel_abandoned` → `play_music` (interaction 4). A Spectator leaving forgets its wagers (`FOR EACH`).
- Duel B: the backer never drops the handkerchief (`> action holds drop_handkerchief(*)`), so `AFTER 1 MINUTE` fires; then it is still running when `feast` ends: `Poisoning` `DROPPED` (`PRINT`, `discard_cup`, `EXITED, BY PARENT`) while the duel outlives its Phase, until `farewell`'s `DROP SUBPLOT` calls it off (`ring_bell`) (interaction 7, second half).
- `Host EMPTIED`: the king leaves, and the Plot ends.

### 7. Variations

Every `snippet` row of the coverage table, ordered by spec chapter. Each is one banquet line, the varied line, and what changes (a Diagnostic, or a line of a Trace). `R0109` is shown here once, on one 2.0 line, and the "In 2.0" notes link to it.

**Alternative:** each snippet inline, beside the line it varies, inside the run. That makes it closer to the source, but it breaks the story every few lines.

### 8. What no run reached

It should be close to empty. It lists what is left out on purpose (the *Gaps that stay gaps*, `—` rows) and anything the four runs still miss.

---

## Where the files go

```
docs/showcase/
  README.md            # coverage index (exists)
  banquet.regin        # full cast (exists)
  runs/
    evening/      evening.regin       case.trace
    grudges/      grudges.regin       case.trace
    short_evening/short_evening.regin case.trace
    two_duels/    two_duels.regin     case.trace
```

Each `<run>.regin` imports `../../banquet.regin` and overrides it. Each `case.trace` has `#! case:`, `#! seed:`, and `#! rule:` naming the interactions it covers.

## Depends on

- *Scripting the game for one Agent* (`issues/09-scripting-one-agent.md`): the script syntax every case uses, with `link` steps for the Directors since *ScriptedGame and the Trace on the game link* (`.scratch/director-game-link/issues/06-scripted-game-and-the-trace.md`, chapter 34).
- *What counts as using a Placeholder* is decided: the laughing alternative that runs 1 and 2 quote writes `?_who`. (*Leaving two Agents out of one Role* is decided: the Spectators are mapped with one `EXCEPT` list.)
