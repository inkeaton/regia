# The walkthrough's shape

Type: prototype
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 02

## Question

What does the guide that walks through the 1.5 showcase look like? Make a rough outline to react to.

Decide:

- Its order: file by file (as the old guide's *Showcase*), the evening's story, or feature by feature.
- Which runs it follows, and with which casts. The old small cast couldn't reach several Plans, so there may be several runs.
- Whether those runs are written as `.trace` behaviour cases (chapter 34), so that the showcase is also tested, and whether they become spec Conformance cases.
- How the "In 2.0" notes are written, and where.
- The casts must between them reach `resent`, both gossip Plans, the scowl and a dinner eaten to the end (from *The banquet in 1.5*).
- Which test cast carries `NO KIND`, `SEED` and the other `.regin` constructs the coverage table places in the test casts (from *What the showcase must show*).
- Which Interfaces (chapter 38) the guide prints, and where.

## Resolution

Resolved on 2026-11-18, with the user, by reacting to a prototype outline. The decided outline is [`prototypes/walkthrough-outline.md`](../prototypes/walkthrough-outline.md), and it holds the detail.

**Order.** The evening is told as a story across four runs. The files aren't printed whole: each Plan is quoted where it first runs. The [README](../../../docs/showcase/README.md)'s coverage table stays the index for finding a construct. The guide's sections: reading a run, the files (Import graph only), the casts, the four runs, **Variations**, and what no run reached.

**Runs and casts.** Four test casts in `docs/showcase/runs/<run>/`, each importing `../../banquet.regin`:

- *The evening* (`evening`): arrival to farewell, with interactions 1, 2, 3 (`sold_out`), 6 and part of 7.
- *Old grudges* (`grudges`): `resent`, the scowl, the laugh, both gossip Plans, `wronged`, `TIES`, and an `unheard` insult in `reception`.
- *A short evening* (`short_evening`): a Guest leaving during the `arrival` count, a dinner eaten to the end, `no_food` → `make_do`, a refused `pick_up`, and `poison_drunk` → `poison_taken`.
- *Two duels* (`two_duels`): two Stagings, the no-wager `ELSE`, the Defender walking out, the handkerchief that never falls, `Poisoning DROPPED` while a duel outlives `feast`, `END SUBPLOT`, and `Host EMPTIED`.

Every cast sets `SEED` and overrides values. `NO KIND` is in *The evening* (`hothead`), *Old grudges* (`knight`, with `percival LIKE knight` kept as a template) and *A short evening* (`knight` and `hothead`, with `NO AGENT percival`: a removed `percival` with hotheads still present is `R2122`).

**Cases.** Each run is a `.trace` behaviour case, written by hand until a build exists. They are the writer's own cases (chapter 27), run by `regia test`, and **not** spec Conformance cases. The script steps print the game's half of each run, which answers the old guide's `#revise` about the invented game behaviours.

**"In 2.0" notes.** A short boxed note where the stand-in first runs (the done-Signal, the hand count, the Reason told back), naming the construct and its chapter, with **no 2.0 code**. Later appearances link back to it. `R0109` is shown once, among the Variations. The map's Notes win over the coverage row for chapter 01, which is now fixed.

**Snippets.** Gathered in a closing *Variations* section, ordered by spec chapter.

**Interfaces.** Two are printed: `Keeping_watch` in *The evening*, at the seizure (why `RoyalBanquet` needs `ring_bell`, `R3801`), and `HonorDuel` in *Two duels*, at the first challenge.

**New ticket.** A `.trace` script step can't address one Agent (`> cue idle`, `> fact +hungry`), while `regia_cue` and `regia_fact` go to one body: [*Scripting the game for one Agent*](09-scripting-one-agent.md).

Changed: [`docs/showcase/README.md`](../../../docs/showcase/README.md) (the test casts' place, and the coverage rows for chapters 01, 11, 21 and 38). Nothing in the spec, ADRs or glossary.
