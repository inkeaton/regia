# Write the 1.5 showcase Program

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 01, 02

## Question

Write the showcase Program in `docs/showcase/`, as the world and the coverage table decide: the Vocabulary, the Playbooks, the Plots and the `.regin` files.

Done when:

- every row of the coverage table has its place in the Program;
- each file has been checked by hand against the spec, chapter by chapter, for `R0109` and every other Diagnostic, and the expected warnings are listed;
- a short `docs/showcase/README.md` gives the world, the files and the coverage table, as the old README did.

Where writing finds a spec question, it is recorded in the resolution and becomes a ticket, not worked around silently.

## Resolution

Resolved on 2026-11-18. The Program is in `docs/showcase/`: [`vocabulary.regia`](../../../docs/showcase/vocabulary.regia), nine Playbooks in `playbooks/`, three Plots in `plots/`, and [`banquet.regin`](../../../docs/showcase/banquet.regin). The [README](../../../docs/showcase/README.md) gives the world, the files, the expected Diagnostics, the coverage table (now its only copy) and the interactions. The test casts are left to *The walkthrough's shape*, as *The banquet in 1.5* said.

**Checked.** Each file was read against chapters 01–21, 26 and 38 and their `## Regia 1.5` sections. No construct gets `R0109`: no `FROM GAME`/`FROM ME`/`OR`, no `BY`, no Goal ending in a Plot, no quantity after `FROM`, no `JOINED`. Expected Diagnostics: none, apart from `R0307` allowed on the laughing alternative. The checks that needed care:

- `R0807`: Agents change `grudge`, so it can't be a `GAME FACT`. It is a plain Fact, seeded by Instancing.
- `R3801`: `Keeping_watch` Signals `culprit_seized` to every Plot that gives it, `RoyalBanquet` included. The banquet now has a Plan for it (`DO ring_bell`).
- `R1404`/`R2107`: a Trait lies in [0, 1]. The old `bravery AT RANDOM(-0.6, 0.6)` and `SUITS bravery AT -0.5` would be errors, so the values were moved into range.
- `R1305`: every Trigger that two Playbooks of one Plot share on one Agent kind is ordered: `scandal` (`OVER`), `insulted` (`TIES`), `idle` across the Subplots (`HonorDuel OVER Poisoning`).
- `R1708`: every Outcome of both Subplots is matched. `Poisoning` no longer ends bare when its Poisoner leaves; it runs on until the feast ends.
- `R3807`: every Cue that isn't `GAME` has a `TELL`, `SIGNAL`, `END PLOT WITH` or `FAIL WITH`.
- `R0310`: the Names are declared (`wall`, `door`, `kitchen`, `roast`, `pie`, `bread`).
- Instancing: kinds are `KIND`, `AGENT` is an individual Agent, and `TARGET jason` is lowercase.

**Changed from the earlier tickets while writing.**

- *Names.* There are still five dotted names, but not the same five: `grudge` is gone (above), and the game Cue `poison_drunk` (`hall.table.poison_drunk`) is new. `in_stock(dish)` is a new `GAME FACT` with no External name.
- *Poisoning.* The `poison_poured` Signal and the Director's `WAIT 30 SECONDS` are gone. The game reports the cup drunk (`poison_drunk`), which also places "a game Cue reaching a Director". `pour_poison(person)` takes the cup's owner, and `Scheming` picks the Guest it resents least (`LOWEST`). Its `EXITED BY PARENT` does `DO discard_cup`.
- *HonorDuel* gets a third Phase, `betting`, between `challenge` and `fighting`. In `challenge`, an `AFTER 20 SECONDS` would have counted from the challenge and started a fight the Defender never accepted. A second `AFTER 1 MINUTE` covers a handkerchief that never falls.
- *Done-Signals* follow the `ENDED` rule everywhere: `toast_given` and `handkerchief_dropped` are sent from `WHEN open_feast ENDED` and `WHEN give_signal ENDED`.
- *Duelling* repeats with a local Goal `strike` (`PURSUE strike, WITHOUT WAITING`) instead of the `stamina LEARNED` loop. `strike` is the `GIVEN` against `IF` case, and the winner's `DROP strike.` stops it. Its Cues `challenged`, `hit`, `yielded` are local, and so is `Courtesy`'s `greeting`.
- *Serving* checks `IF NOT in_stock(?dish): FAIL WITH sold_out(?dish).` before `pick_up`, which can still be refused. A refusal has no Reason, so the Reason can only come from that check.
- *Spectators.* `Guest` without both duellists needs two `EXCEPT`s, and a Role takes one. `RoyalBanquet` maps `Guest EXCEPT ?offended`, and `HonorDuel` gives `Wagering TO Spectator EXCEPT ?offender`. This is ticketed below.
- *The caught Poisoner* is taken out with `UNASSIGN NobleSocializing FROM Guest ?culprit`. The coverage draft's `FROM ?culprit` would take nothing (`T1505`), because the Giving was made to `Guest`. Then `ASK ?culprit TO take_leave`.
- *Cast.* An individual `AGENT percival LIKE knight` is new, so that `hothead`'s `LEARN grudge(percival, 2)` has a Name from Instancing to use.
- *Small.* `TELL 50 PERCENT OF peer wronged(ME, ?speaker)` is the told Fact, with `LEARNED FROM peer`, `ME` and `PERCENT OF`. `Dining TIES NobleSocializing ON insulted` gives a mild Guest at dinner a way to ignore an insult. `took_seat FROM Host` starts the music, so the king's Signal isn't unheard.

**Rows moved.** These went to `snippet`, or stay gaps, because their places were forced:

- a relation `ON` a recipe or a Fact change (no two banquet Playbooks share one);
- a Random choice in a Director;
- a Phase with no `DURING` Block;
- an Expression in a Message argument, and a value named inside an Option.

`PRINT` moved from the Host's toast, where it would have been a game announcement, to `WHEN Poisoning DROPPED`, where it is a log line. The continuation lines are the two wrapped `START SUBPLOT`s. The README's coverage table and *Gaps that stay gaps* record all of this.

**Spec questions**, now tickets:

- [*Leaving two Agents out of one Role*](07-two-exceptions.md): the Spectators.
- [*What counts as using a Placeholder*](08-using-a-placeholder.md): whether a name used only in a Pick (`HIGHEST ?stake`, `LOWEST ?size`, `WEIGHT ?size`), or only by a sibling `GIVEN`, counts as used for `R0307`. The Program assumes it does. Also whether the allowed `R0307` should stay, since chapter 02 points to `?_who` for exactly this case.

**Noted, not ticketed.** These are spec wording, out of scope on this map. `R2005` reads as forbidding `ENDED` in a Playbook, but chapter 05 allows a Goal's `ENDED` there; it means a Subplot's. Chapter 17's *Plot parameters* example writes `Challenger STARTS WITH:` without `ROLE`, with a `TELL` in a setup.

Changed: `docs/showcase/` (new). Nothing in the spec, ADRs or glossary.
