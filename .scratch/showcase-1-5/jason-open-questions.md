# What the Jason chapters leave open

The inventory made for [*What the Jason chapters leave open*](issues/05-jason-open-questions.md). It walks spec chapters 28–37, and the *ASL mapping notes* of the language chapters they build on, against the 1.5 showcase in `docs/showcase/`. It lists every question that a hand-written Jason reference Build of the showcase would run into and that the spec doesn't answer.

Showcase lines are written `<file>:<line>`, relative to `docs/showcase/`. Chapters are spec chapters. Questions are grouped by subject. Each group is sized for one decision ticket, and the ticket it became is named in its heading.

Only what the showcase raises is listed here. A gap in the Jason chapters that the showcase never reaches (`ASSIGN P TO Guest ?who` lifting an exclusion, `CAST ?who LEFT`, `FROM GAME`, anything that only exists in 2.0) is left out, and marked "not raised" in the checklists at the end.

---

## A. Facts about Jason the decisions wait on: [*How Jason behaves where the translation waits*](issues/10-jason-facts.md)

These are questions about how Jason behaves, not decisions, so they make a research ticket. Several groups below can't be decided without them. Jason's source (`references/jason-main/`), the Jason book and VEsNA-Pro's source (`references/vesna-pro-main/`) are in the repo.

1. **A known belief with a new source.** Agent A believes `wronged(x, y)[source(b)]` and receives `tell wronged(x, y)` from `c`. Does Jason generate `+wronged(x, y)` again? Can a plan's context still see whether the belief was held before the event? (chapter 07 notes: `LEARNED` must fire only for a new Fact; `noble_socializing.regia:50`, `:62`.)
2. **An `[atomic]` intention that suspends.** If an `[atomic]` plan calls an internal action that suspends its intention (`regia.act` waiting for the game, `regia.wait`), do other intentions run while it waits, and does the mailbox keep being read? Can the intention resume at all? (chapter 30's `TRANSITION` and chapter 31's ending run `EXITED` "to completion" inside `[atomic]` plans; `royal_banquet.regia:103`, `honor_duel.regia:74`, `poisoning.regia:20`.)
3. **Variables in `for`.** Does Jason's `for (.member(m(X), L)) { … }` unbind variables bound inside the loop body between rounds? (chapter 26 says "check"; `dining.regia:25`, `:30`, `:39`, `honor_duel.regia:71`.)
4. **The `-!g` event.** What annotations does the `-!g` event carry: the original `[source(S)]` of an `achieve`, the `error(…)` terms, anything a plan can use to carry a Reason? What happens to an `-!g` with no applicable plan? (chapter 11 notes: "should be checked"; `serving.regia:21`, `:23`, `courtesy.regia:16`.)
5. **Telling a desire apart from the current intention.** Which internal actions (`.desire`, `.intend`, `.intention`) can test that a Goal is pursued **by another intention**, leaving out the current one? (chapter 08: `PURSUING g` in a `TO g` Plan leaves out the current intention; `dining.regia:17`, `:72`, `serving.regia:27`.)
6. **VEsNA-Pro's Temper and Moods.** In `references/vesna-pro-main/`: the range `Temper` accepts for a Mood's starting value and for a `temper([…])` annotation's target, what it does with a negative value, when it applies `effects`, and what public method a `regia.shift` could call. (chapter 14 says a Mood is in [-1, 1] and in its notes that "Regia follows the code", [0, 1]; `banquet.regin:12`, `:17`, `dining.regia:71`, `noble_socializing.regia:31`.)

## B. Plan Bodies in ASL: [*A Plan's Statements in ASL*](issues/11-statements-in-asl.md)

No chapter holds the translation of a Plan's Statements. The language chapters' notes were written "for *The full ASL mapping* to pick up", and chapters 28–37 build the Infrastructure around Plans.

1. **Where the translation lives.** Do the Statement translations stay as notes in chapters 06–26, or does a new Jason chapter collect them? The reference Build's guide needs one place to quote.
2. **Variable names.** How does a Placeholder become a Jason variable (`?speaker` → `Speaker`?), and what prefix do generated variables take so that they never meet one? Chapter 09 asks for "a prefix designers can't produce" and writes `W1`, `T`, `R`. A designer can write `?w1`. (`noble_socializing.regia:9`, `:10`, `wagering.regia:8`.)
3. **`FOR EACH`**: Jason's `for`, or the recursive `regia_each__N` goal. Hangs on A3. (`dining.regia:25`, `:30`, `:39`, `honor_duel.regia:71`.)
4. **`WAIT … UNTIL`**: the shape of `regia.wait(Cond, D)`. Is the condition passed as a term and re-tested on every belief change, or on every cycle? What `time` entry does it write? Chapter 12 names it; chapter 35 has only `regia.wait(D)`. (`dining.regia:27`.)
5. **Stale text.** Chapter 06 gives Jason the native `if`, while chapters 29 and 35 still list `regia_if__N` and `regia_either__N` plans among what a Jason Build guards and leaves out of the Trace.

## C. Messages and told Facts: [*Messages and told Facts in ASL*](issues/12-messages-in-asl.md)

1. **A told Cue.** What form does `TELL ?foe insulted` take so that nothing stays in the receiver's belief base and a repeated Cue fires again? Chapter 07 asks for one and gives two candidates (a generated achieve-goal per Cue, or removal in the handling plan); chapters 29 and 33 show a plain `+ready[source(S)]`. (`noble_socializing.regia:22`, `duelling.regia:13`, `:36`, `:45`, `serving.regia:13`, `:22`, `honor_duel.regia:32`, `courtesy.regia:13` for a local Cue.)
2. **A Signal.** Is `SIGNAL took_seat` the same message as a told Cue, sent to each Director in `regia_given`? How do the Director's `FROM Guest ?g`, `FROM Host`, `FROM Spectator ?who` and `FROM ?winner` test the Sender against `regia_cast(Me, Role, S)`? (`courtesy.regia:19`, `royal_banquet.regia:60`, `:65`, `honor_duel.regia:27`, `:34`, `:57`, `keeping_watch.regia:16`.)
3. **Nothing heard.** The catch-all for a Signal no Plan of the current Phase or `DURING PLOT` takes (`T3801`), and an Agent's catch-all for a told Cue with no Plan (`T0702`). Chapter 35 says "the catch-all plans" write the `unheard` entries, and no chapter writes them. The showcase hits both: `finished_eating` arrives in `farewell` from `Dining`'s closing Plans (`dining.regia:48`); `insult_thrown` outside `feast` (`noble_socializing.regia:28`); `scandal` told to a Servant (`noble_socializing.regia:23`).
4. **A told Fact, learned once.** How does the receiver run `LEARNED` only when the Fact is new from any source, and `FORGOTTEN` only when the last source goes? Hangs on A1. (`noble_socializing.regia:50`, `:62`, `royal_banquet.regia:128` telling a knight who is already `on_duty`.)
5. **`LEARNED FROM DIRECTOR` and `LEARNED FROM peer`** on a told Fact. Is the Sender the newest source annotation? What if the Fact was already held from another source? (`keeping_watch.regia:6`, `noble_socializing.regia:62`.)
6. **`ME`.** As a Value it is `.my_name` (chapter 07 notes). How is it written in a Trigger's pattern (`WHEN scandal(ME) FROM peer ?speaker`): a context test after the trigger, or a variable bound at start? (`noble_socializing.regia:48`, `:50`.)

## D. A Goal's life in ASL: [*A Goal's life in ASL*](issues/13-goal-life-in-asl.md)

Chapters 05, 08 and 11 decide what a Goal's life is. Their notes leave the Jason side to "the Jason chapters", and none of chapters 28–37 has it.

1. **A Pursuit's identity.** Each `!g` is its own Pursuit (chapter 08: nothing is joined). What does the generated code carry for it: the Sender (for `FROM patron ?guest` on its endings), a number for the Trace's `of`? (`serving.regia:9`, `:21`, `:23`.)
2. **The generated ending events.** `REACHED`, `DROPPED`, `FAILED` and `ENDED` aren't Jason events. What goals or events are posted, in what order (the specific Trigger, then `ENDED`), and on which intention, so that `WHEN have_dinner REACHED` runs before `WHEN have_dinner ENDED`? (`dining.regia:35`, `:38`, `:43`, `:45`, `:48`, `courtesy.regia:16`, `:19`, `hosting.regia:11`, `wagering.regia:18`.)
3. **A Reason along the chain.** How `FAIL WITH sold_out(?dish)` in `fetch` reaches `bring`'s `-!` plan, so that `WHEN bring(?dish, ?) FAILED WITH sold_out(?dish)` matches and the plain `FAILED` Plan doesn't run. Hangs on A4. (`serving.regia:18`, `:21`, `:23`, `dining.regia:29`, `:43`.)
4. **Two `FAILED` Plans.** How the generated `-!g` plan, the designer's `FAILED WITH` Plan and its plain `FAILED` Plan meet in `selectOption`: does the designer's Plan run inside the generated one, as a subgoal? (`dining.regia:43`, `:45`, `serving.regia:21`, `:23`.)
5. **No applicable `TO` Plan.** `take_seat` with no `seat` has no applicable recipe (`T1104`). Is the generated `-!take_seat` plan reached for a Goal that never started a recipe? (`courtesy.regia:10`, `:14`, `dining.regia:24`, `:33`.)
6. **`DROP`.** `.drop_desire` removes the intentions, and the generated code raises `DROPPED` and `ENDED` "for each level stopped". Who walks the stopped levels: generated ASL, or an internal action shared with `regia.stop_playbook`? (`dining.regia:21`, `duelling.regia:49`.)
7. **`PURSUING`.** Hangs on A5. (`dining.regia:17`, `:72`, `serving.regia:27`.)

## E. Roles read by an Agent, and which files hold a Playbook: [*Roles an Agent reads*](issues/14-roles-an-agent-reads.md)

1. **A counted recipient in a Playbook.** `TELL 50 PERCENT OF peer …` and `ASK 1 OF waiter TO …` are drawn by the Agent from its union of bindings (chapter 15 notes: "not in the Jason chapters yet"). How is it drawn: one internal action with the seeded source? How does `50 PERCENT` round? (`noble_socializing.regia:50`, `dining.regia:26`.)
2. **`PLAYS` in an Agent.** `?foe PLAYS peer` tests the union of bindings with the Agent itself left in. How is it compiled, inside `COUNT` and a `WEIGHT` Pick too? (`noble_socializing.regia:9`, `:20`.)
3. **`PLAYS` in a Director.** `COUNT(? PLAYS Guest)` reads `regia_cast(Me, guest, _)`. No chapter says so. (`royal_banquet.regia:62`, `:99`, `:115`, `:117`.)
4. **Which Role files hold a Subplot's Playbooks through `MAPPING ?who`.** Chapter 29's reach rule covers `ASSIGN … TO ?who`, not `MAPPING ?offender TO Defender`, which brings `Duelling` to whoever `?offender` holds. Which Root Roles' files include `Duelling`? Through chapter 14's emission rules, this decides whether `king` gets a `temper` because `Duelling` names `bravery`. (`royal_banquet.regia:93`–`:94`, `honor_duel.regia:9`–`:10`, `duelling.regia:16`, `:21`.)

## F. The Giving record: [*Exclusions, one Agent and a Phase in the Giving record*](issues/15-giving-record.md)

Chapter 29's `regia_given` and chapter 30's `regia_standing` have no place for these yet.

1. **`EXCEPT` on a standing Giving.** `ASSIGN Wagering TO Spectator EXCEPT ?offender`: what the Director records in `regia_standing` (an exclusion list) and what each Agent's `regia_given` target says. Chapter 30's 1.5 section says "the exclusion lists still read it", and no chapter defines them. (Was `honor_duel.regia:63`; since *Leaving two Agents out of one Role* the Program has no such Giving, so this is a snippet's question, still decided for the spec, with a list.)
2. **`EXCEPT` on a Director's recipient and on a Subplot's Mapping**: `TELL Spectator EXCEPT ?offender duel_on`, `MAPPING Guest EXCEPT ?offended TO Spectator`. Chapter 30's recipients and chapter 31's step 1 don't mention it. (`royal_banquet.regia:95`, now `Guest EXCEPT ?offended, ?offender`, a list. The recipient is a snippet's since *Leaving two Agents out of one Role*.)
3. **`UNASSIGN P FROM Guest ?culprit`.** Chapter 29 has `regia_take(p, role(guest))` and `regia_take(p, all)`, and not the Role-then-Agent form, which takes `?culprit` out of every Giving whose target includes `Guest` and narrows the standing one. What message goes to the Agent, and what changes in `regia_standing`? (`royal_banquet.regia:135`.)
4. **A Giving made for a Phase.** A Phase setup's `ASSIGN` lasts the Phase (chapter 16). How the record marks it, so that leaving the Phase takes it and nothing else. Chapter 29's banner says "Givings made for a Phase need a mark on the record". (`royal_banquet.regia:79`–`:82`.)
5. **`ASSIGN Keeping_watch TO ?winner`**, a Giving to one Agent added to the same Playbook held from a Role setup of the same Director (a knight wins). Is it a second `regia_given` with target `agent(w)` next to `role(guard)`, and does a later `UNASSIGN … FROM Guard` leave it? (`royal_banquet.regia:127`, `:32`–`:33`.)

## G. A Playbook given and taken away: [*A Playbook's opening and closing in ASL*](issues/16-opening-and-closing.md)

Chapter 29's *Taking a Playbook away* still says a Playbook's own `DROPPED`, `ENDED` and `UNASSIGNED` Plans don't run; its banner says chapter 15 (ADR 0021) reversed this and that the chapter is "not yet brought up to that".

1. **`ASSIGNED`.** Which plan posts it, on the first `regia_given` of P, and is it posted after the atomic `regia_give`? (`dining.regia:10`.)
2. **The closing state.** While P's closing Plans run, P has no Giving, yet its Plans for `DROPPED`, `ENDED` and `UNASSIGNED` must pass the guard and nothing else of P may. How is "closing" held, and when does it end? (`dining.regia:38`, `:48`, `duelling.regia:56`, `keeping_watch.regia:18`.)
3. **Speaking through the Givings as they were.** A closing Plan's `SIGNAL` reaches the Directors that gave P, and its `TELL waiter` the Role as bound just before. `regia_take` has already removed the records. Are they kept until the closing Plans end? (`dining.regia:48`: `finished_eating` after `farewell` takes `Dining`.)
4. **Rewriting step 1 of chapter 29.** `regia.stop_playbook` "generates the `DROPPED` events itself". With the closing Plans running wherever they sit, which events does it raise, in what order with `UNASSIGNED`, and does it share the walk of D6?

Blocked on *A Goal's life in ASL* (the ending events) and *The Giving record* (what a take-away removes).

## H. A Staging's start: [*What a Staging runs when it starts*](issues/17-staging-start.md)

1. **What `!regia_begin` reads.** It is fixed Infrastructure, and it needs the Plot's initial Phase and its Roles in declaration order. No belief in chapter 28's table carries them. (Every Plot of the showcase.)
2. **The `CAST` setup.** It runs before the Role setups (chapter 16). Chapter 30's `regia_begin` runs Role setups only. (`royal_banquet.regia:19`–`:20`.)
3. **The initial Phase's setups at start.** Chapter 16: the Plot's setups, then the initial Phase's. Chapter 30 doesn't run a Phase's setups. The showcase's initial Phase `arrival` has none, but `feast`'s setups are the same code (I2).
4. **`EMPTIED` for a Role that starts empty.** Chapters 17 and 19 fire it after the setups and before the entry Plans. Chapter 31 says only that the Role "starts empty". A duel whose `?offended` left before `START SUBPLOT` has no Challenger and must end at once. (`honor_duel.regia:65`–`:68`, `royal_banquet.regia:93`.)
5. **The setup lines of kinds and individual Agents** (chapter 21), run by the Root Director at start. Chapter 36 leaves them open ("with chapter 30's Role setups, still to be written"). Where are they carried (`regia_kind`, `regia_start_cast`, generated plans)? Do they run before or after the Role setups? Is `percival`, `LIKE knight`, given the kind's lines? (`banquet.regin:19`, `:27`.)

## I. Entering and leaving a Phase: [*Entering and leaving a Phase in ASL*](issues/18-phase-change.md)

1. **A Phase's setups on entry.** Chapter 30's `TRANSITION` has four steps and none runs the new Phase's setups, which come "after the Phase belief changes and before the `ENTERED` event". (`royal_banquet.regia:79`–`:82`.)
2. **Taking a Phase's Givings away** on leaving it, after `EXITED` (chapter 16), with F4's mark. Step 3 of the transition is the place. (`royal_banquet.regia:79`–`:82`, left at `:100`, `:118`, `:138`.)
3. **`UNTIL EXITED` on a `START SUBPLOT`.** Leaving `feast` ends `Poisoning` as `END SUBPLOT` does, and the parent hears `DROPPED`, then `ENDED`, from the new Phase or `DURING PLOT`. Where in the transition does the child get `regia_end`, and when is `dropped` posted? (`royal_banquet.regia:88`, `:139`.)
4. **`AFTER`.** Chapter 12: a plan for the Phase's entry event, posted with `ENTERED`'s, tagged with the Phase. Not in chapter 30. What does a Phase with two `AFTER`s and an `ENTERED` post, and in what order? What does `AFTER` in `DURING PLOT` count from? (`honor_duel.regia:37`, `:43`, `:54`, `royal_banquet.regia:72`.)
5. **`IN`** reads `regia_phase`. Not in chapter 30. (`royal_banquet.regia:115`, `:117`.)
6. **An `EXITED` Plan that waits on the game.** Chapter 20 forbids `WAIT` in `EXITED` and says nothing of `DO`. Chapter 30 runs `EXITED` "to completion" inside the `[atomic]` transition, and `DO clear_tables` suspends until the game replies. Is a waiting `DO` allowed there, and how does the transition wait for it? Hangs on A2. (`royal_banquet.regia:102`–`:103`.)

## J. Subplots after ADR 0030: [*Subplot arguments and endings in ASL*](issues/19-subplot-endings.md)

Chapter 31 predates ADR 0030 in places. It says a parent hears nothing when it ends a child itself, and that the `ENDED` Blocks of one Phase are exclusive, first match in written order. Chapter 17 now says the parent hears `DROPPED` then `ENDED`, and the specific Trigger's Plan then the plain `ENDED` Plan, both.

1. **Plot arguments.** `HonorDuel(?offender)`: how the child gets its arguments (`regia_start` carries `Cast` and `Prefix` only), how its Plans read `?offender`, and how the parent keeps them for matching. (`honor_duel.regia:6`, `:32`, `:63`, `royal_banquet.regia:92`.)
2. **`RUNNING`.** The parent's record of running Stagings with their arguments, which `regia_child(Director, Plot)` lacks. When is a child removed from it (chapter 17: before its ending is handled)? (`royal_banquet.regia:91`.)
3. **`END SUBPLOT` with a pattern.** `END SUBPLOT HonorDuel(?)` ends the Stagings whose arguments match. (`royal_banquet.regia:107`.)
4. **The parent's Triggers.** How `regia_subplot_ended` becomes the specific Trigger's Plan, then the plain `ENDED` Plan, each picked in its own Phase or in `DURING PLOT`, for `ENDED WITH`, `ENDED WITHOUT OUTCOME` and `DROPPED`. How the arguments are matched. Which ending writes `T3802` and which writes nothing. (`royal_banquet.regia:125`–`:140`.)
5. **`DROPPED` posted by the parent.** For `END SUBPLOT` and `UNTIL EXITED`, the parent posts `dropped` itself, once per Staging ended, "handled after the current Body". Its later `regia_ended` is then ignored, as now. (`royal_banquet.regia:107`, `:139`.)
6. **`EXITED BY PARENT`.** The child must know, while ending, that the ending came from its parent: does `regia_end` carry it? Its Plan runs before the plain `EXITED` Plan. (`honor_duel.regia:73`, `poisoning.regia:19`.)
7. **A Subplot's `DO` while its parent is ending.** When `RoyalBanquet` ends (`Guest EMPTIED`), each child gets `regia_end` and runs `EXITED BY PARENT`: `DO ring_bell`, `DO discard_cup`. A Subplot Director's Action goes to the Root, but chapter 31 guards "passing `DO` up" by `regia_phase(_)`, and the Root has removed its Phase before it waits for its children. Read as written, the Action is never answered, the child's ending never finishes, and the Root waits for its `regia_ended` forever. Hangs on A2 and I6. (`honor_duel.regia:74`, `poisoning.regia:20`, `royal_banquet.regia:120`–`:123`.)

Blocked on *Entering and leaving a Phase* (`UNTIL EXITED`, waiting `EXITED` Plans).

## K. Temper and Moods: [*Moods and Labels on VEsNA-Pro*](issues/20-moods-on-vesna.md)

1. **A Mood's range.** Chapter 14 says a Mood lies in [-1, 1], and its notes say VEsNA-Pro keeps values in [0, 1] and "Regia follows the code". The showcase starts Moods below zero and targets them in `SUITS`. What does the `.jcm`'s `temper` carry, and what does `most_similar` compute, for a negative Mood? Hangs on A6. (`banquet.regin:12`, `:17`, `dining.regia:71`, `noble_socializing.regia:31`.)
2. **A `SHIFTS` Label on a Plan that runs alone.** VEsNA-Pro applies `effects` only when temper selection picks among two or more intentions, so a lone Plan "never shifts a Mood through its Label". The showcase puts `SHIFTS` on uncontested Plans: a `FAILED` Plan, a `GIVEN` sibling, one Suits alternative. Does the Jason Target apply them when the Plan runs, and how? (`dining.regia:45`, `noble_socializing.regia:57`, `duelling.regia:21`, `:39`.)
3. **`regia.shift`** needs a public method on `Temper`, and the Trace needs a hook for an applied `SHIFTS` and for a temper choice's scores (`fits`). Is this a patch upstream, a subclass, or reflection? (`noble_socializing.regia:49`.)

## L. Actions and the Target's own code: [*The Target's own code in a Build*](issues/21-target-code.md)

1. **Where a dotted Action's Java lives.** `play_fanfare` is `hall.music.fanfare`, a Java internal action. Chapter 28 says a Build contains no Java, and chapter 35 that `regia run` never writes a class path. Where does the reference Build keep `hall/music/fanfare.java`, and how do `regia run` and `RunCase` find it? (`vocabulary.regia:83`, `hosting.regia:8`.)
2. **Its Trace entries.** Chapter 37: a dotted Action writes the same `DO` and `DO … DONE` entries, but they are written by `regia.act`, which a dotted Action doesn't go through. Is there a wrapper? (`hosting.regia:8`.)
3. **Stale text.** Chapter 37's *Not decided here* still lists "Cancelling an Action when its Plan stops: post-2.0", which ADR 0038 brought in. (Calling off: `dining.regia:21` dropping `have_dinner` during `DO eat`.)

## M. The Trace's pieces: [*The Trace's fields and entries*](issues/22-trace-pieces.md)

The walkthrough's runs (`docs/showcase/runs/`) state expected lines. Chapter 34 gives each kind's words and leaves these open. *Scripting the game for one Agent* already holds the script step that names no Agent.

1. **`regia.trace(Kind, Level, Code, Fields)`**: the fields of each kind, and the content of `sourcemap.json`, which chapter 35 gives only in words.
2. **`by`, `over` and `fits`.** How they reach a Plan's `regia.trace` call from `GIVEN` order, `selectOption`, Precedence and VEsNA-Pro (chapter 35: "not yet written"). (`dining.regia:56`/`:61`, `royal_banquet.regia:44`–`:47`, `noble_socializing.regia:26`–`:39`.)
3. **`giving` entries.** Who writes them (the Director or the Agent), one per Agent or one per Statement, and the form for a Giving to one Agent. (`royal_banquet.regia:70`, `:127`.)
4. **What writes an entry.** A Role setup's `LEARN` and `PURSUE` (a `message` entry, as the `tell` and `achieve` they are?); a Director's own Facts (a `fact` entry, which the table gives to "an Agent"); entering the initial Phase (a `phase` entry?); a `SIGNAL` (no kind covers it); a `T1104` Goal (one `failure` entry or two); a waiting Plan and the Goal it is a recipe for (one entry or two); `RUN ENDED` outside test mode. (`royal_banquet.regia:27`, `:61`, `courtesy.regia:19`, `courtesy.regia:14`.)
5. **The console line of a failure in turn** (`FAILURE <what> because #<seq>`) shows no `code`, while chapter 34 puts one on every `failure` entry.
6. **`ALSO IN #<n>`**, and the per-Plot Staging number of `director:HonorDuel#<n>`: which agent counts the Stagings of a Plot across parents, and how a Director learns its own number. (Two duels at once, `royal_banquet.regia:90`.)
7. **Agent names in a Target-neutral chapter.** Chapter 34's expected lines use names (`noble_1`) that only chapter 36 fixes, for Jason.

Blocked on *Temper and Moods with VEsNA-Pro* (`fits`).

---

## Checklist: the revision map's Jason fog

From *Not yet specified* in `.scratch/regia-revision/map.md`, item by item.

| Item | Where it went |
| --- | --- |
| The Director's catch-all for a Signal or an ending with no Plan | C3, J4 |
| Pursuits that are never joined | D1 |
| The generated `REACHED` and `ENDED` events | D2 |
| The report of a Goal's ending to whoever asked | not raised: later than 1.5 (chapters 07, 20) |
| A Reason along the failure chain | D3 |
| `FROM GAME`, `FROM ME` | not raised: later than 1.5 |
| The Value `ME` | C6 |
| A Playbook's closing state, `ASSIGNED`, `UNASSIGNED` | G |
| Givings and setups tied to a Phase | F4, H3, I1, I2 |
| A counted recipient drawn by an Agent | E1 |
| `PLAYS` against the cast copy | E2, E3 |
| Bindings with `EXCEPT` | F1, F2 |
| The `CAST` Role with its setup | H2 (the setup). `CAST` as a recipient, target or Mapping: not raised |
| Plot arguments in starting, ending and `END SUBPLOT` | J1, J3, J4 |
| The three `UNASSIGN … ?who` forms, with an exclusion list per Giving | F3 (`FROM Guest ?who`). `FROM CAST ?who` and plain `FROM ?who`: not raised |
| `EMPTIED` for a Role that starts empty | H4 |
| `ALSO IN` in the Trace | M6 |
| The `dropped` report, endings run specific-then-plain | J4, J5 |
| The record of running Stagings for `RUNNING` | J2 |
| `IN` against the current Phase | I5 |
| `EXITED BY PARENT` | J6 |
| Counted Signals with arguments for `SENT`, `?` slots out of a Quota's count key, a Quota quantity per check, `count` entries | not raised: Quotas are later than 1.5 |
| Picks that round up | E1 (`50 PERCENT OF peer`). A Director's `PERCENT` pick: not raised |
| `regia.shift` and the public method on `Temper` | K3 |
| Setup lines of kinds and individual Agents, run by the Root Director | H5 (at start). For a joiner: later than 1.5 |
| `regia-jason` reading `regia.seed` and `regia.trace_console` | covered: chapter 35 |
| An Agent's catch-all for a told Cue with no Plan | C3 |
| The console logger named with the designer name | covered: chapter 35 |
| `by`/`over`/`fits` from `selectOption`, Precedence and VEsNA-Pro | M2 |
| A `Temper` hook for an applied `SHIFTS` and a temper choice's scores | K3 |
| `AFTER` as a Phase-tagged plan started with `ENTERED` | I4 |
| `regia.wait(Cond, D)` with its `time` entry | B4 |
| The cancel sent when a waiting `regia.act` intention is dropped | covered: chapter 37 (ADR 0038); stale line, L3 |
| The run's clock paused by the Root Director's body | covered: chapter 37 |
| 1.5: the Root Director refusing a `regia_join` with `T1902` | covered: chapter 33's 1.5 section |

## Checklist: the old README's *Review notes* on chapters 30, 31, 34 and 35

From `docs/guide/showcase/README.md`, *Spec wording*. The `#revise` notes were design questions and were closed by the revision map.

| Note | Where it went |
| --- | --- |
| `EXITED` "to completion" and a `DO` that waits; a failing `EXITED` lets the transition carry on (chapters 20, 30) | I6, J7. The second half is chapter 30's, unchanged |
| `?who` never in the Staging, two Placeholder Mappings holding one Agent (chapters 20, 30) | covered for Jason: chapter 30's `T3001`. The rest is language, not this map |
| A Subplot Role that starts empty, and `EMPTIED` (chapters 17, 31) | H4 |
| `END SUBPLOT` runs `EXITED` (chapters 17, 20, 31) | covered: chapters 20 and 31. `BY PARENT`: J6 |
| Chapter 34: a code on a failure in turn; one entry or two for a waiting Plan and its Goal; no kind for `SIGNAL` | M4, M5 |
| Chapter 34's Director names against chapter 35's logger, and the numbering of concurrent Stagings | covered: chapters 34 and 35 now agree. Who counts: M6 |
| Agent names used by Target-neutral chapter 34, fixed only in chapter 36 | M7 |
| No chapter holds the translation of a Plan; a told Cue's form; a second `PURSUE`; the event `DROPPED` is raised as; `-!g` against `WHEN g FAILED`; Jason's `for`; `SIGNAL`, a Role recipient and `FROM` in words only | B1, C1, C2, D1 (a second `PURSUE` is now a second Pursuit, chapter 08), D2, D4, D6, B3 |
| `RANDOM(a, b)` in a Body has no ASL | covered: chapter 35's `regia.random(A, B, whole, R)` |
| Native `if` against `regia_if__N` | B5 |
| Placeholders as Jason variables; the item's name in `regia_rank` | B2. The item uses the Regia name: covered by chapter 28 (External names never reach ASL) |
| `Host` and `host` both lowercased to `host` | no question: they never share a slot |
| Which Role files get a Subplot Role's Playbooks through `MAPPING ?who` | E4 |
| `!regia_begin`'s initial Phase and Roles; `regia.trace`'s fields; `sourcemap.json`; two `ENDED` Blocks and `Pos` | H1, M1, J4 (ADR 0030 made the specific and plain Blocks both run) |
| Chapter 34's pieces: `PLAN` text for `FROM DIRECTOR` and `ENTERED`, the cast in `STAGING … STARTED`, `GIVE … TO … AS` for one Agent, who writes `giving` and `cast` entries | M3, M4. The `PLAN` text and the cast's form go with M1 |
| Setup `LEARN`/`PURSUE` and `message` entries; a Director's `fact` entries; the initial `phase` entry; `T1104` entries; `RUN ENDED` outside test mode | M4 |
| A script step that names no Agent | already a ticket: *Scripting the game for one Agent* |
