# The showcase world: a royal banquet

Every example in the guide comes from this one world. This file is its outline: what the world is, who is in it, and where each part of Regia 2.0 has its place. The Program itself sits beside this file:

| File | Holds |
|---|---|
| `vocabulary.regia` | every shared Fact, Event, Goal, Action and Propensity |
| `playbooks/*.regia` | one Playbook per file, each importing the Vocabulary |
| `plots/*.regia` | one Plot per file, importing the Playbooks it gives and the Subplots it starts |
| `banquet.regin` | the full cast |
| `test.regin` | the small cast, layered on `banquet.regin` |

The outline is derived from the spec, never the other way round. Where they disagree, the spec wins and this file is fixed.

## The world

One evening at a royal banquet, from the guests arriving to the last one taking leave. It extends the banquet of the 1.0 primer and keeps the names the spec's examples already use (`RoyalBanquet`, `HonorDuel`, `Guest`, `Host`, `NobleSocializing`).

The game behind it is a 3D hall. Walking to a seat takes time, animations finish when they finish, and the game can refuse an Action (a sword can't be drawn at the table, a dish has run out).

## Plots

### `RoyalBanquet` (the Root Plot)

Roles: `Host`, `Guest`, `Servant`, `Guard`.

| Phase | What happens | How it ends |
|---|---|---|
| `arrival` (initial) | Guests walk to their seats. | Quota Trigger: `ALL` Guests have signalled they are seated. |
| `reception` | Mingling and gossip. | The Host's toast. |
| `feast` | Servants serve, insults start duels, `Poisoning` starts. | Quota Trigger: `75 PERCENT OF Guest` signal they have finished eating. |
| `farewell` | Guests take leave of the Host and Leave the Program. | The Plot ends when the `Guest` Role has emptied. |

`DURING PLOT` reacts to `HonorDuel` and `Poisoning` ending (their Outcomes) and to a latecomer Joining, in whatever Phase that happens.

The banquet is the Root Plot, not a Subplot of a wider castle, because a joiner only ever enters the Root Plot.

### `HonorDuel` (Subplot, several Stagings at once)

Roles: `Challenger`, `Defender`, `Spectator`. Phases: `challenge`, `fighting`.

Every insult taken badly starts a new Staging. The insulted Guest and the one who insulted them, each held by a Placeholder, are mapped to `Challenger` and `Defender`; every Guest is a `Spectator` through a whole-Role Mapping. It ends with an Outcome: `duel_settled(?winner)` or `duel_abandoned`.

### `Poisoning` (Subplot, one Staging, no Phases)

Roles: `Poisoner`, `Watchman`.

Started once during the feast. `1 OF Guest` is cast as the hidden `Poisoner` and the Guards as `Watchman`. It has only `DURING PLOT` Plans and ends with `poisoner_caught(?who)` or `poison_taken`.

## Playbooks

| Playbook | Given to | What it carries |
|---|---|---|
| `Courtesy` | every Root Role, from Role setup | Baseline behaviour: greeting, walking to a seat, taking leave, Custom Actions that wait; the Host's toasts |
| `NobleSocializing` | Guests, by Phase | Suits alternatives, Shifts, gossip Messages, Match and Pick ("the Guest I hate most"), Random choice |
| `Dining` | Guests in `feast` | Goals with recipes, `LEARNED`/`FORGOTTEN`, `DROPPED` and `FAILED` Triggers, `FAIL`, `FOR EACH`, `COUNT`, Local Vocabulary |
| `Serving` | Servants in `feast` | A Playbook Role `patron` filled by a Mapping; a Guest's `ASK` answered with a waiting `PURSUE`; a refused Action |
| `Keeping_watch` | Guards, from Role setup; again by `Poisoning`; a duel's winner | Reacts to the same Events as `NobleSocializing`, so a `knight` needs Precedence; one Playbook given by two Plots; a Giving to one Agent held by a Placeholder |
| `Duelling` | `Challenger` and `Defender` in `HonorDuel` | A Playbook Role `opponent` mapped crosswise, Local Vocabulary, Durations, repetition through a Fact change |
| `Wagering` | `Spectator` in `HonorDuel` | Named values, `CHANGE`, Signals a Quota counts |
| `Scheming` | the Poisoner | `WITHOUT WAITING`; falling through to the parent's Playbook |

## Agent kinds

| Kind | Plays | Starts | Why it is here |
|---|---|---|---|
| `king` | `Host` | 1 | The single Host |
| `noble` | `Guest` | several | Random Propensity values |
| `hothead` | `Guest` | a few | Same Role as `noble`, different Propensity values |
| `knight` | `Guest` and `Guard` | a couple | One Agent in two Roles, where Precedence has to be declared |
| `servant` | `Servant` | a few | Work done through Custom Actions |
| `latecomer` | `Guest` | 0 | Enters only by Joining |

Two Instancing files: a full `banquet.regin`, and a small `test.regin` that imports it and overrides the kinds (one king, two nobles, one knight, one servant). The small build is the cast the walkthrough follows.

## Coverage

| System | Natural place |
|---|---|
| Placeholders and Expressions | `NobleSocializing` (who insulted whom); wagers and counts in `HonorDuel` |
| Goals and Trigger kinds | `Dining`: `TO` recipes, `LEARNED`/`FORGOTTEN` on hunger, `DROPPED` and `FAILED` |
| `GIVEN` versus `IF` | `Dining`: the Guest who was hungry when the Plan was chosen and no longer is when the Body gets to eating |
| Match, Pick, `FOR EACH` | `NobleSocializing` ("the Guest I resent most"); `FOR EACH` dish in `Dining`; the wager Pick in `HonorDuel` |
| Random choice | `NobleSocializing` small talk, with Weights |
| Failure | `Dining`, `Serving` and `Courtesy`: a refused Action, a Goal no Plan applies to, `FAIL` on purpose, `FAILED FROM` |
| Precedence | The `PRECEDENCE` Block in `RoyalBanquet` (the knight; `HonorDuel` over `Poisoning`), and `PARENT OVER SELF ON scandal` in `HonorDuel` |
| Suits and Shifts Labels | `NobleSocializing` reactions to an insult; accepting a challenge in `Duelling`; `noble` versus `hothead` values |
| Playbook Roles and Mappings | `Serving` (`patron`), `Dining` (`waiter`), `Duelling` (`opponent`); Placeholder Mappings for `HonorDuel`, a counted one for `Poisoning` |
| Role setup | `STARTS WITH` on every Root Role (`Courtesy`, starting Facts and Goals) and on every Subplot Role |
| Subplots | `HonorDuel` (several Stagings, Outcomes) and `Poisoning` (no Phases) |
| Quota Triggers | `ALL` in `arrival`, `75 PERCENT OF` in `feast`, `3 OF Spectator` in `HonorDuel` |
| Joining and Leaving | The `latecomer` kind and the two `JOINED` Plans; `farewell`; the Defender who walks out |
| Instancing | The kinds above, `ROOT`, Propensity values with `RANDOM`, Target settings, two layered `.regin` files |
| Custom Actions, with and without waiting | `walk_to(seat)` waits; `Scheming` pours poison `WITHOUT WAITING`; an External name on a Guard's Action |

## Interactions the world forces

1. **A Pick inside a Quota-triggered Plan in a Subplot.** In `HonorDuel`, once enough Spectators cheer, the Director picks the Spectator with the `HIGHEST` wager.
2. **Precedence across Playbooks, Phases and Subplots on one Agent.** A `knight`, Guest and Guard at once, is watching a duel and hears an insult.
3. **Failure climbing through a waiting Goal.** A Servant's `pick_up` is refused, `fetch` fails, `bring` fails with it, and its `FAILED` Plan tells the Guest. The Guest, who could not wait on the `ASK`, counts an empty plate after a minute and `FAIL`s, and its own `FAILED` Plan reacts.
4. **Leaving in the middle of a Subplot.** A Defender Leaves and the duel ends with `duel_abandoned`.
5. **Joining during a standing Giving and a running Subplot.** A latecomer gets `NobleSocializing` but is not a Spectator of the duel in progress. One who Joins during `farewell` is asked to leave by the Phase's `JOINED` Plan, which beats `DURING PLOT`'s.
6. **`GIVEN` versus `IF` on a Fact that changes mid-Plan.** The hungry Guest above.

## Review notes

Awkward spots found while writing the showcase are listed here, tagged `#revise`, and collected later in the Review List. None is fixed here: each is worked around in the Program, and the workaround is what the note points at.

**Agents and Messages**

- `#revise` A latecomer can be a Guest only because the banquet is the Root Plot. Had the banquet been a Subplot of a wider Plot, nobody could join it once it started.
- `#revise` An Agent can't tell that something is about itself: there is no "me". `NobleSocializing` sends two Messages for one insult, `insulted` to the victim and `scandal(?foe)` to everyone, and the victim also hears the gossip about itself.
- `#revise` A Body can't wait for an answer to an `ASK`. `Dining` waits a minute and counts what is on the plate. The Servant's `sold_out` arrives as an Event that the waiting recipe can't see.
- `#revise` A Role recipient reaches every Agent of the Role. `ASK waiter TO bring(…)` goes to every Servant, so with three Servants every dish is fetched three times. Nothing says "one of them".
- `#revise` A Goal's arguments double as its identity. Two Guests asking for `bring(roast)` would be one Goal, the second request ignored, so `bring` carries the seat. `fetch` carries it too for no other reason: without it, two orders of one dish would share one trip to the kitchen.
- `#revise` Chapter 06 lists "a Plan pursuing its Goal again" as a way to repeat, but a recipe that pursues its own Goal joins its own pursuit and waits on itself (chapter 08). `Duelling` repeats through `WHEN stamina(?) LEARNED` instead, which is harder to follow.
- `#revise` Leaving is something the game does after an Action. In the source it shows only in `leave_hall`'s doc comment.

**Playbooks and Givings**

- `#revise` Nothing fires when a Playbook is given or taken away. A Guest who was already hungry when `Dining` arrived never sees `hungry LEARNED`, so the Director also asks for `have_dinner`, and that Message isn't replayed for a latecomer. `Duelling` has to clear the `stamina` left over from an earlier duel, since Local Facts outlive the Giving.
- `#revise` `Host` and `host` differ only in case, which is enough to need a `MAPPING Host TO host` on all four Role setups, while the same case would have bound them silently.
- `#revise` The Host's own Plans sit in `Courtesy`, which every Role holds, because a Playbook can't tell which Role its Agent plays and one more Playbook felt heavy for three Plans.

**Plots and Directors**

- `#revise` A whole-Role Mapping next to Placeholder Mappings can't say "everyone else": both duellists are also Spectators, wager on their own duel and cheer it. The Quota `3 OF Spectator` is met in the small cast only because of this.
- `#revise` A Director can't name the Agent playing one of its Roles. To end with `duel_settled(?winner)` the winner has to Signal `duel_won`, so that `FROM ?winner` fills the Placeholder.
- `#revise` A Quota counts per argument value, so `wagered(?stake) FROM 3 OF Spectator` would wait for three equal stakes. Spectators send a second, bare Signal, `cheered`, only to be counted.
- `#revise` An Agent in two Stagings of `HonorDuel` at once has one `opponent` Role holding both opponents, and its `duel_won` reaches both Directors. Nothing in the source can keep the two duels apart.
- `#revise` Role setups run before the initial Phase is entered, and a Quota starts counting at entry. A Guest whose `take_seat` finished at once would Signal `took_seat` too early to count towards `FROM ALL Guest`.
- `#revise` `LEARN purse(RANDOM(5, 20))` in a Role setup: chapter 16 allows `RANDOM` and also says the setup is the same for every Agent. It doesn't say whether the roll is made once or per Agent. The showcase assumes per Agent.
- `#revise` An insult taken badly outside `feast` Signals `insult_thrown` to a Director with no Plan for it. The Guest has stood up and nothing follows, with no warning.

**Precedence**

- `#revise` `HonorDuel` says `PARENT OVER SELF ON scandal`, `RoyalBanquet` says `HonorDuel OVER Poisoning`, and the default puts `Poisoning` over `SELF`. On `scandal` that is a cycle, built from one line in each of two files and one line nobody wrote. `RoyalBanquet` adds `SELF OVER Poisoning ON scandal` to break it, which means knowing what its Subplot declared. Chapter 32's "unless a relation says otherwise" doesn't say whether a default gives way here.

**Instancing**

- `#revise` A layered `.regin` can't remove a kind. `test.regin` redeclares `hothead` with no `COUNT`; the kind still exists for Joining, and has lost its Propensity values because whole items are replaced.

**Spec wording** (not design)

- Chapter 17 writes the Trigger as `WHEN HonorDuel ENDED WITH duel_settled(?w):` in its examples and as "`, WITH <event>` after `ENDED`" in its rules. The showcase follows the examples.

## Gaps in the showcase

Things the example lacks. These are faults of the world, to be fixed by adding to the Program, and they don't go in the Review List.

- `LOWEST` is never used. Nothing at the banquet is yet "the least of" anything. (Found in *Matching*.)
