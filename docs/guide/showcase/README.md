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
- Chapter 21 says an Agent declaration with no Body "ends with `.`", while chapter 01 says a `.` at the end of a line does nothing. Either `AGENT hothead PLAYS Guest` with no `.` is a valid line, or this is the one place where the `.` is required. The showcase writes the `.`. (Found in *Syntax*.)
- Chapter 03 says a Role name can't be a Value and gives `host` as its example of a Name. It doesn't say whether a Role of a Playbook counts (`Courtesy` has `ROLE host.`), nor whether a Value may be a word that is also declared as an item, such as `craves(hungry)`. The showcase avoids both. (Found in *Vocabulary*.)
- Chapter 04 says both sides of a comparison in a Context "must be filled already", and chapter 03 that a Match must satisfy the whole Context. Neither says whether `GIVEN ?now > 1 AND stamina(?now):`, with the comparison written before the Fact that fills it, is an error. The showcase always writes the Fact first. (Found in *Placeholders and Expressions*.)
- Chapters 13 and 14 call Trigger Blocks "with the same Trigger" Suits alternatives, without saying whether `WHEN insulted FROM peer ?who` and `WHEN insulted FROM peer` are the same Trigger. The showcase keeps `?who` on all three, and the one that only laughs gets the unused-Placeholder warning. (Found in *Placeholders and Expressions*.)
- Chapter 26 says the Placeholders a `FOR EACH` fills are used "only inside the Block, as for `IF` branches", and its checks cover use after the Block. It doesn't say whether a second `FOR EACH` in the same Body may fill the same name, which chapter 06 forbids for a second `IF`. (Found in *Placeholders and Expressions*.)
- Chapter 34 says a seeded case draws `EITHER`, `AT RANDOM` and `RANDOM` Propensity values the same way every run, and chapter 35 repeats the list. Neither names a `RANDOM(a, b)` in a Body or a Role setup, nor the Agents drawn by a counted Mapping (chapter 15). (Found in *Randomness*.)
- Chapter 04 makes a roll whole when both bounds are whole. Chapter 21 says a Propensity's `RANDOM(a, b)` is "drawn from [a, b]" without saying whether `RANDOM(-1, 1)` follows that rule and gives -1, 0 or 1. The showcase always writes one bound as a decimal. (Found in *Randomness*.)
- Chapter 05 says `FROM ?who` matches "any sender, and fills `?who` with the sending Agent". It doesn't say whether a Message from a Director matches, nor what `?who` would then hold. In `Courtesy`, `WHEN greeting FROM ?who: DO bow_to(?who).` would bow to a Director if one ever told `greeting`. No Director in the showcase tells an Event that a `FROM ?who` Plan handles. (Found in *Messages*.)
- Chapter 02 lists the declarations that take a Doc comment (Plot, Playbook, Role, Phase, Plan, Vocabulary item) and leaves out Agent declarations, and doesn't say whether a `.regin` file can have a file Doc comment. The showcase uses plain Comments in both `.regin` files.
- Chapter 15 lists `MAPPING ?who TO …` among its errors (`R1505`) and says under *Mappings* that it "is an error in 2.0", while its *Not in 2.0* list and chapter 20 say it is allowed on `ASSIGN` and `START SUBPLOT`. The showcase follows chapter 20 (`MAPPING ?offended TO Challenger`). (Found in *Playbooks and Roles*.)
- That a Playbook's own `DROPPED` Plans don't run when the Playbook is taken away is said only in chapter 29, for Jason. Chapters 15 and 16 say "running Plans stop, local Goals are dropped" and no more. (Found in *Playbooks and Roles*.)
- Chapter 15 says `ROLE` lines come before a Playbook's Trigger Blocks, and chapter 10 that local declarations go anywhere in the Block. Neither says whether a `FACT` line may stand above a `ROLE` line. Chapter 10's rule on names that differ only in case names a Plot's Roles and Phases, and not a Playbook's Roles. The showcase writes `ROLE` lines first and one Role per Playbook. (Found in *Playbooks and Roles*.)
- Chapter 16 says that values differing per Agent, "this Guest's gold" among them, come from Instancing. Chapter 21 lets an Agent declaration give Propensity values and nothing else, so no starting Fact can differ per Agent except through a roll. (Found in *Plots and Directors*.)
- No chapter says what a run is once its Root Plot has ended. Chapter 17 takes the Givings away and chapter 19 makes Leaving the game's doing, so the Agents are still there, holding no Playbook. The guide says so; the spec doesn't. (Found in *Plots and Directors*.)
- Chapter 20 says an `EXITED` Plan runs "to completion" and forbids `WAIT` in it, and says nothing of a `DO` that waits for the game. That a failing `EXITED` Plan lets the `TRANSITION` carry on is said only in chapter 30, for Jason. (Found in *Plots and Directors*.)
- Chapter 20 says an Agent that has left is dropped from a `MAPPING ?who TO …`. What happens when `?who` holds an Agent that was never in the Staging's Cast, or a Value that is no Agent, is said only in chapter 30, for Jason (dropped, with a Trace warning). No chapter says whether two Placeholder Mappings in one `START SUBPLOT` may hold the same Agent. (Found in *Subplots and Stagings*.)
- That a Subplot's Role may start empty, when the parent's Role is empty or a Mapping is dropped, is said only in chapter 31, for Jason. Chapter 17 doesn't say it, nor that `EMPTIED` doesn't fire for a Role that starts empty, which follows from chapter 19's wording alone. (Found in *Subplots and Stagings*.)
- Chapter 17 says of `END SUBPLOT` that each Staging ends "as for `END PLOT`" and takes its Givings away. That its `EXITED` Plans run when the parent ends it is in chapter 20's general wording and, explicitly, only in chapter 31. (Found in *Subplots and Stagings*.)

- Chapter 19 fixes the order of a leave inside one Staging (Quota checks, then `LEFT` and `EMPTIED` per Role) and says nothing of the order between a parent and its Subplots, nor of what the rest of that sequence does once one of its Plans has ended the Plot. Chapter 33 has the first, for Jason. (Found in *Quotas and Cast Changes*.)
- That `ON <event>` in a `PRECEDENCE` line covers the Quota Triggers on that Event is said only in chapter 32, for Jason. What happens to an Agent that Joins after the Root Plot has ended is said only in chapter 33 (it is created and joins no Cast). (Found in *Quotas and Cast Changes*.)
- Chapter 18 says a departure can complete a Quota and the Trigger "then fires as usual", without saying which argument value fills its Placeholders when no Event arrived. Chapter 25's Trigger picker lists Events and cast changes and no quantity, so it doesn't say how a Quota transition is drawn in the Visual Editor. (Found in *Quotas and Cast Changes*.)
- Chapter 13 says `ON` takes "a Trigger's item, with its kind word if it has one", and its examples are an Event, a Fact change and a Goal. It doesn't say how `ON` is written for a Director's cast Triggers (`Guest JOINED`), a Subplot ending (`HonorDuel ENDED`) or `ENTERED`. The showcase's one competition between a Phase and `DURING PLOT` is on `Guest ?late JOINED`, so the relation that would turn it around can't be written with confidence. Nor does the chapter say whether an `OVER` on one item and a `TIES` on another may join the same two Playbooks. (Found in *Precedence and Labels*.)
- Chapter 13's table of defaults gives a Phase's Plan beating `DURING PLOT`'s "a warning only if the Phase's Trigger Block always catches the Trigger", while its check list words it as a `DURING PLOT` Plan "fully shadowed by a Phase's". `farewell`'s `JOINED` Plan has no Context and always catches, yet `DURING PLOT`'s still runs in the other three Phases. By the first wording the showcase compiles with a warning, by the second without. (Found in *Precedence and Labels*.)
- Chapter 13 lists the conflict report "per Role and Trigger". The banquet's one relation between Playbooks, `Keeping_watch OVER NobleSocializing ON scandal`, orders a Playbook of `Guard` against one of `Guest`, which meet only on an Agent of a kind that plays both, or on an Agent given a Playbook through a Placeholder. The chapter doesn't say under which Role such a competition is listed. (Found in *Precedence and Labels*.)
- Chapter 14 says "running the Plan shifts those Moods" and leaves the moment to the Target. It doesn't say whether a Plan that fails, or is stopped when its Playbook is taken away, has shifted. (Found in *Precedence and Labels*.)
- That `SELF` in a Subplot's `PARENT OVER SELF` stands for the Subplot with everything it starts, and `PARENT` for the parent's own Playbooks without its other Subplots, follows only from chapter 32's rewriting of the line as `SELF OVER HonorDuel`. Chapter 13 doesn't say it. (Found in *Precedence and Labels*.)
- Chapter 23 says "The Target is chosen by Instancing (chapter 21)", while chapter 21 says the Target is chosen outside Instancing, on the command line or in the Visual Editor, and that a `TARGET` Block only configures. The guide follows chapter 21. (Found in *Instancing*.)
- Chapter 21 says a build ignores the `TARGET` groups of other Targets and warns about an unknown key in the group of a known one. It doesn't say what happens to a group whose Target the Transpiler doesn't know, such as a misspelt `TARGET JASN:`. (Found in *Instancing*.)
- Chapter 21 says a `COUNT` left out "means 0" and that a `COUNT` is a non-negative literal, so `COUNT 0.` and no line are two spellings of one thing; it doesn't say whether a redeclaration differing only in that is "identical" for the sibling rule. (Found in *Instancing*.)
- Chapter 23 names the commands `regia check` and `regia build` and says nothing else of the command line: where the output folder is (chapter 28 gives `build/<entry>/` and cites chapter 24, which is the Visual Editor's), how the Target that chapter 21 says is chosen there is written, how the conflict report of chapter 13 is asked for "on request", or how a Build is started outside test mode. (Found in *The Transpiler*.)
- Chapter 10 makes one Program of everything reachable from the Entry files, in the plural, while the glossary's Build is made from one Entry file and chapter 23 has the Visual Editor treat each `.regin` as its own Program. What several Entry files on one command line give is not said. (Found in *The Transpiler*.)
- Chapter 21 makes a Program with no Plot an error (`R2104`) "even with no other Instancing", and chapter 23 has the Visual Editor check a `.regia` file that no Entry reaches "as if it were its own Entry". Read together, every Playbook or Vocabulary file not yet imported by a Plot carries that error, and a Subplot's file is checked as a Root Plot. (Found in *The Transpiler*.)
- Chapter 24 clears `build/<entry name>/` before writing a Build, and chapter 35 keeps every run's Trace under `build/<entry>/traces/` so that runs can be compared. (Found in *The Transpiler*.)
- Chapter 27 gives Diagnostic codes to the checks of the language chapters (01 to 21, 26) and says the others have no Conformance cases, while chapters 28 and 35 define `R2801` and `R3501`. Chapter 23 has a Target return Diagnostics from the emit, which runs only with no errors, and doesn't say whether `regia check` reports them. (Found in *The Transpiler*.)
- Chapter 34 puts a `code` on every `failure` entry, while its console text for an entry that fails in turn (`FAILURE <what> because #<seq>`) shows none. It doesn't say whether a waiting Plan and the Goal it was a recipe for write one entry or two, and no kind covers a `SIGNAL`. (Found in *The Transpiler*.)
- Chapter 34 says entries never show Generated names and calls a Director `director:<Plot>`, and chapter 35 prints console lines under the agent's Jason logger, `[regia_director__watch]`. Chapter 34 also numbers the Directors of concurrent Stagings `#1`, `#2` and gives no number to a Plot with one Staging running, without saying what the first is called once a second starts. (Found in *The Transpiler*.)
- Chapter 34 is Target-neutral, yet the Agent names its expected lines use (`guard_1`) are fixed only in chapter 36, for Jason. (Found in *The Transpiler*.)
- Chapter 25 lets a new Event made from the Trigger picker be declared in "the Plot's Local Vocabulary", while chapter 10 keeps `EVENT` out of `PLAYBOOK` and `PLOT` Blocks (`R1012`). (Found in *The Visual Editor*.)
- Chapter 22 says new constructs are written "without redundant terminators", and chapter 25's table has `addPhase` write "a `PHASE name.` line". Neither says whether a blank line is put before a Plan added at the end of a `DURING` Block. The guide follows chapter 22. (Found in *The Visual Editor*.)
- Chapter 25 draws a Plot with no Phases as one node "with the start dot and its endings", while every Plan of such a Plot is in `DURING PLOT`, whose transitions and endings are a Layer that is off by default. It doesn't say what that Layer adds for `Poisoning`, on which node the Givings and Messages of `DURING PLOT` Plans are written, whether the Docs tab lists `DURING PLOT`'s transitions, or whether `addPlan` and `addTransition` can target `DURING PLOT`. (Found in *The Visual Editor*.)
- Chapter 25 draws dotted, as a timeout, "a `WHEN ENTERED` Plan that transitions". `HonorDuel`'s `fighting` waits and then runs `END PLOT WITH duel_abandoned`, which is an ending and not a transition. Nor does it say how the `ELSE` of a `GIVEN` is labelled, whether a Pick is part of the Context on a label, or whether an ending's node shows the Outcome's arguments. (Found in *The Visual Editor*.)
- Chapter 25's graph view data sums a Body up as transitions, endings, a `WAIT` before a transition, Givings, Messages, Custom Actions and `START SUBPLOT`. `END SUBPLOT`, and `LEARN`, `FORGET` and `CHANGE` of the Director's own Facts, are in no list. (Found in *The Visual Editor*.)
- Chapter 25's Trigger picker gives an Event by name. How the slots of an Event with parameters are written (`insult_thrown(?)`), and whether "`WHEN ENTERED` with a `WAIT`" appends to an `ENTERED` Plan that already waits, are not said. (Found in *The Visual Editor*.)
- Chapter 22 lists "moving a construct under another parent" among the edit operations and gives rules for re-indenting a moved Extent, and chapter 25's list of operations has no move. (Found in *The Visual Editor*.)
- Chapter 23 has every `.regin` checked as its own Program. It doesn't say which Program's Diagnostics, semantic colours and graph view a `.regia` file gets when two `.regin` files reach it. Chapter 24's list of semantic kinds (Event, Fact, Goal, Playbook, Role, Plot) leaves out Action, Phase and Propensity without saying whether it is complete. (Found in *The Visual Editor*.)
- Chapter 21 says the Target is chosen "on the command line or in the Visual Editor", and chapter 24 describes no such choice. Chapter 25's Docs tab shows `desc` and `version` and doesn't name `author`, the third key chapter 02 says tools understand. (Found in *The Visual Editor*.)

- No chapter holds the translation of a Plan. Chapters 28 to 37 decide the code around Plans, and the Statements themselves have only the *ASL mapping notes* of chapters 06 to 26, written "for *The full ASL mapping* to pick up". Left open there: how an Event that is told or Signalled is sent so that nothing stays with the receiver (chapter 07 gives two ways, while chapters 29 and 33 show a plain `+ready[source(S)]`); what a second `PURSUE` of a running Goal waits on (chapter 08); the event `DROPPED` is raised as (chapters 08 and 11); how the generated `-!g` plan and our `WHEN g FAILED` Plans meet in `selectOption` (chapter 11, "should be checked"); whether Jason's `for` keeps variables between rounds (chapter 26). Chapter 29 describes `SIGNAL`, a Role recipient and `FROM <Playbook Role>` in words and gives no ASL for them. (Found in *Translation to ASL*.)
- Chapters 09 and 26 roll with `math.random`, and chapter 35 says generated code uses no random source that `regia-jason` can't seed. No chapter gives the ASL of a `RANDOM(a, b)` in a Body. (Found in *Translation to ASL*.)
- Chapter 06 gives Jason the native `if`, while chapters 29 and 35 list `regia_if__N` and `regia_either__N` plans among what a Jason Build guards and leaves out of the Trace. (Found in *Translation to ASL*.)
- How a Placeholder becomes a Jason variable is shown only by examples (`?speaker` as `Speaker`). Generated variables are to use "a prefix designers can't produce", and the notes write `W1`, `T` and `R`. Chapter 32 says the item in `regia_rank` is written with "Jason names" and doesn't say whether that is the External name the trigger itself uses. (Found in *Translation to ASL*.)
- Chapter 28 calls the lowercasing of names one-to-one "because names are unique ignoring case (chapter 10)". A Plot's Role `Host` and a Playbook's Role `host` are both allowed and both become `host`. They never share a slot, so nothing breaks. (Found in *Translation to ASL*.)
- Chapter 29 says which Role files get a Playbook given by `ASSIGN … TO ?who`. It doesn't say which get the Playbooks of a Subplot Role filled by `MAPPING ?who TO …`, such as `Duelling` through `?offender`, which an Event's argument fills. (Found in *Translation to ASL*.)
- Chapter 30's `!regia_begin` is fixed Infrastructure and needs the Plot's initial Phase and its Roles in declaration order. No belief in chapter 28's table carries them. Chapter 35 gives `regia.trace(Kind, Level, Code, Fields)` without the fields of any kind, and the content of `sourcemap.json` only in words. Chapter 31 doesn't say whether two `ENDED` Blocks for one Plot with different Outcomes are "the same Trigger" for the position in `regia_rank`. (Found in *Translation to ASL*.)

- Chapter 34 gives each kind of entry its words and leaves the pieces open. For a `plan` entry, `PLAN <trigger>`: whether `FROM DIRECTOR` is printed as written or as the Director's name, and whether a Quota Trigger keeps its quantity. `PLAN WHEN ENTERED` and `PLAN WHEN EXITED` name no Phase and no Plot. For `STAGING <plot> STARTED <cast>`, the form of the cast. `GIVE <playbook> TO <agent> AS <role>` has no form for a Giving to one Agent held by a Placeholder, and the chapter doesn't say whether a Giving to a whole Role is one entry or one per Agent, nor which agent writes `giving` and `cast` entries. (Found in *Showcase*.)
- Chapter 34 doesn't say whether a Role setup's `LEARN` and `PURSUE` write `message` entries, as the `TELL` and `ASK` they arrive as would; whether a Director's own Facts write `fact` entries, which the table gives to "an Agent"; whether entering the initial Phase writes a `phase` entry; whether a Goal with no applicable recipe (`T1104`) is one `failure` entry or two; nor whether a run outside test mode ever writes `RUN ENDED`. (Found in *Showcase*.)
- Chapter 34's script steps `> event <name>(<args>)` and `> fact +<name>(<args>)` name no Agent. Its exemplars have one Agent each. In a case with several, the step doesn't say who gets the `idle`. (Found in *Showcase*.)

## Gaps in the showcase

Things the example lacks. These are faults of the world, to be fixed by adding to the Program, and they don't go in the Review List.

- `LOWEST` is never used. Nothing at the banquet is yet "the least of" anything. (Found in *Matching*.)
- No Comment over several lines (`#[ … ]#`), and no Doc comment on a Plan, a Role or a Phase. *Syntax* added a `#@version` and a `#@desc[ … ]#` to `RoyalBanquet`. (Found in *Syntax*.)
- No Instancing comment (`#%`): all Instancing is in the two `.regin` files. (Found in *Syntax*.)
- No String and no `PRINT`: nothing at the banquet is printed. (Found in *Vocabulary*.)
- No Multi-definition with an `AS` inside it, and no item declared in two files: the showcase gives every External name a line of its own and keeps all shared Vocabulary in one file. (Found in *Vocabulary*.)
- No `OR` and no parentheses in a condition, no `PURSUING`, and no `ELSE IF`: every condition in the showcase is a Fact, a `NOT`, or an `AND` with a comparison. (Found in *Plans*.)
- No Trigger narrowed by a Value in a slot (`WHEN served(roast)`), no Context that ties two Facts together through one Placeholder, no Placeholder under a `NOT`, no `IF` that fills a Placeholder, and no value named inside a branch or an Option. Every Placeholder in the showcase is filled by a Trigger, by a single Fact of a Context or a `FOR EACH`, or by a naming at the top of a Body. (Found in *Placeholders and Expressions*.)
- The `GIVEN` versus `IF` case the coverage table promises, `IF hungry` in `Dining`, is undercut by `WHEN hungry FORGOTTEN: DROP have_dinner.` in the same Playbook: the recipe is dropped before its `ELSE` can run. *Plans* explains the difference on `IF COUNT(on_plate(?)) = 0:` instead; a cleaner case is wanted. (Found in *Plans*.)
- No Option of more than one Statement, no Random choice inside another or in a Director, no Placeholder filled in an Option, and no roll in a condition (`IF RANDOM(1, 100) <= 30:`). `AT RANDOM` only ever follows a `HIGHEST`, and the one counted Mapping is `1 OF Guest`, with no `PERCENT OF` and no Expression. (Found in *Randomness*.)
- No `PURSUING` in a condition, no fallback Goal pursued from a `FAILED` Plan, no `DROP` that stops a Goal the recipe was waiting on (`have_dinner` waits on none), and no Failure that climbs more than two levels. No Goal has recipes in two Playbooks, and no recipe without a `FROM` is ever asked by another Agent. (Found in *Goals and Failure*.)
- No `EVERYONE`, no Fact told by an Agent (only the Director's `TELL ?winner on_duty.`) and no `LEARNED FROM`. No recipe that treats its requesters differently, no `ASK` from an Agent to a single Agent held by a Placeholder, no Expression in a Message's argument, and no Quota Trigger in a Playbook. (Found in *Messages*.)
- No `ASSIGN` to a part of a Role, and no counted or Placeholder Mapping onto a Playbook's Role: the three in the showcase all fill Roles of a Subplot. No Role bound by its name alone, no Plot Role filling two Roles of one Playbook, and no Playbook with more than one Role. No `UNASSIGN … FROM ?who`, and no Playbook taken away while a Plan of another Playbook waits on one of its Goals. (Found in *Playbooks and Roles*.)
- No Phase without a `DURING` Block, no `ENTERED` or `EXITED` in `DURING PLOT`, no `TRANSITION` to the current Phase, and no game Event or Fact that reaches a Director: every Director Trigger in the showcase is a Signal, a cast change or a Subplot ending. No Director Plan keeps a Fact to remember how a Phase was left. *Plots and Directors* added `WHEN EXITED: DO clear_tables.` to `feast`, and the Action to the Vocabulary. (Found in *Plots and Directors*.)
- No Subplot that starts a Subplot of its own, no Plot started from two parents, and no Role of a Subplot filled by a parent's Role of the same name. Every `ENDED` Plan is in `DURING PLOT`, so none competes with a Phase's. No `EXITED` Plan in a Subplot, so nothing shows what a duel does when it is ended from above. (Found in *Subplots and Stagings*.)
- No `LEFT` Plan: every departure the banquet cares about is an `EMPTIED`. No Event heard by both a plain Trigger and a Quota, no Quota in `DURING PLOT`, none whose Event carries an argument, and none that fires twice. No Agent kind that Joins in two Roles, and no `JOINED` Plan that gives the joiner a Playbook. (Found in *Quotas and Cast Changes*.)
- No `TIES`, no two Trigger Blocks of one Playbook that match the same Trigger without being Suits alternatives, and no relation between a Phase and `DURING PLOT`. No relation names a recipe or a Fact change (`ON have_dinner`, `ON hungry LEARNED`): all three `ON`s are `ON scandal`. Two of `RoyalBanquet`'s three relations say what name order would decide anyway, so nothing shows a relation going against it. No Subplot with a Subplot of its own, so `SELF` is never more than one Plot's Playbooks. No Suits alternative has a Context, and no Mood is shifted upwards except aggressiveness. (Found in *Precedence and Labels*.)
- No Target setting other than a default (`strategy = most_similar` is what Jason does anyway), no second `TARGET` Block, and none overridden by `test.regin`. No two `.regin` files side by side, so no conflict between siblings to settle. No `COUNT 0`, no kind whose Roles change from one build to the next, and no kind that only the game ever spawns apart from `latecomer`, a copy of `noble`. The Instancing comment is still missing: *Instancing* shows one in a throwaway snippet. (Found in *Instancing*.)
- No Conformance case over the banquet: no `.trace` file and no annotated file, so the cases in *The Transpiler* are the spec's exemplars. The Program compiles with one known warning, so every error shown there comes from breaking a file in a throwaway snippet. (Found in *The Transpiler*.)
- No file with two Plots, so the graph pane never has two tabs. No name reached only through another file's Imports (every file imports `vocabulary.regia` itself), so no `↗↗` mark. No Event declared in a Plot's own file. No `IF` whose branches go to two Phases, and no `WHEN ENTERED` Plan that waits and then transitions: the one timeout, in `HonorDuel`, ends the Plot. No Doc comment on a Role, a Phase or a Plan for the Docs tab to show, and no Inline block in a Plot for a graph edit to open. (Found in *The Visual Editor*.)
- The showcase doesn't build on Jason. The five External names of Facts and Events in `vocabulary.regia` (`hall.seating.seat`, `hall.needs.hungry`, `hall.social.grudge`, `hall.clock.idle`, `hall.senses.saw_pouring`) are dotted, which chapter 28 makes an error (`R2801`), and `hall.guards.seize` is read as a Java class and not as the game's Action. *Translation to ASL* reads the five with `_` for each dot. *The Logic of Regia*, *Syntax* and *Vocabulary* quote the dotted lines, and *The Transpiler* shows the Program building with one warning. (Found in *Translation to ASL*.)
- Nothing gets the Defender up from the table. The insulted Guest does `DO stand_up`, the offender never does, and `draw_sword` is "refused at the table". Whether the Defender's `fight` fails at once is left to the game. `seize` has no Doc comment, so what happens to a seized culprit is left to it too. (Found in *Showcase*.)
- A duellist who has yielded still owes a lunge for its last lost point. If it lands before the winner's `salute` is done, the winner yields as well and both Signal `duel_won`. `ASK ?backer TO give_signal` is followed at once by `TRANSITION TO fighting`, so the fight never waits for the handkerchief. (Found in *Showcase*.)
- The small cast can't reach two of the three ways to take an insult, `TO resent`, or either gossip Plan of `NobleSocializing`: all three Guests stand up or stand guard, and only one grudge is seeded. The run in *Showcase* also ends its feast before anyone eats, so the `IF hungry` and the `DROPPED` Plan of `Dining` are never seen running. A second walkthrough cast, or a second run, is wanted. (Found in *Showcase*.)
