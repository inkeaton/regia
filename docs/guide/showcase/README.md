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
