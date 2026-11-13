This chapter collects every `#revise` of the guide and of the showcase's README, about 225 notes. They are not listed one by one. Many notes are the same miss seen from three chapters, so the list is by cause: what the language lacks or says twice, then the notes that follow from it. A revision discusses the cause once.

The causes are sorted by what kind of answer they call for. The sorting is a proposal, and the first thing the revision should do is disagree with it. Nothing here changes the design.

## How to read the list

| Part | What is in it | Causes |
|---|---|---|
| Bugs | Two rules that disagree, or a result nobody chose. To be fixed whatever else is decided. | B1 to B16 |
| Deliberate limits | A decision with an ADR or a spec section behind it. The guide shows what it costs. | L1 to L9 |
| Features for 2.0 | Something missing that the showcase had to work around in many places, and that looks small enough for this version. | N1 to N15 |
| Features for a later version | Something the spec already lists as not in 2.0, or too large to add now. | F1 to F10 |
| To discuss | No decision exists, or the guide can't tell whether the behaviour was meant. | D1 to D20 |

Each cause has a name, a few lines on what is missing, the notes it explains (chapter in italics, the reason after it), and the spec chapters a change would touch. "README" is `showcase/README.md`. A note that the README and a chapter both carry is listed once, under the chapter.

A cause in *Features for a later version* is not a small one. F1 and F2 explain more notes than any cause in the 2.0 part, and several of their notes are places where the showcase does the wrong thing. They are there because the spec has already said "not in 2.0", and the revision may want to say otherwise.

Three kinds of finding are not here, because they are not `#revise` notes: the contradictions of the spec (*Spec wording* in the README), the constructs the banquet never uses (*Gaps in the showcase*), and the glossary's missing or wrong entries (the map of this effort).

## Bugs

### B1. Dotted External names are refused by the only Target

The language chapter calls External names "often dotted" for Facts, Events and Actions. Jason can't hold a dot in a belief, and reads a dot in an Action's name as a Java class.

- *Translation to ASL*: the five dotted Facts and Events of the showcase are errors, so the showcase doesn't build.
- *Translation to ASL*: `hall.guards.seize` asks for a Java class no Build contains, and the declaration doesn't say so.

Spec: chapters 10, 28, 37.

### B2. A Target's checks run only in the emit

- *The Transpiler*: `R2801` and the warning for a `SUITS` without a Selection function come out of `regia build`, so a Program passes `regia check` and then fails to build with an error that was there all along.

Spec: chapters 23, 28.

### B3. The Role setups run before the first Phase starts counting

A setup's `PURSUE` is sent before the initial Phase is entered, and a Quota counts from entry.

- *Plots and Directors*, README: a Guest whose `take_seat` ends at once Signals `took_seat` too early, and `FROM ALL Guest` waits for good.
- *Quotas and Cast Changes*: the same, from the Quota's side.

Spec: chapters 16, 18, 20.

### B4. A roll is whole or decimal by how its bounds are written

A bound can be a Placeholder or an Expression, so the kind of roll is only known at runtime.

- *Placeholders and Expressions*: `RANDOM(1, ?gold / 2)` is whole with 12 coins and gives 3.71 coins with 13. Nothing rounds.
- *Randomness*: any wait between one and three seconds has to be written `RANDOM(1, 3.0)`.
- *Randomness*: `bravery AT RANDOM(-1, 1)` reads as three temperaments, unless a `.regin` file rolls differently, which chapter 21 doesn't say.

Spec: chapters 04, 09, 21.

### B5. `PERCENT` rounds up in a Trigger and down in a Mapping

- *Quotas and Cast Changes*: of ten Guests, `75 PERCENT OF Guest` is eight in a Quota and seven in a Mapping.

Spec: chapters 15, 18.

### B6. A name made in every branch outlives an `IF` and not an `EITHER`

- *Placeholders and Expressions* (and a pointer in *Randomness*): chapter 04 has the exception for `IF`/`ELSE`, chapter 09 has none for Options.

Spec: chapters 04, 09.

### B7. "Pursuing its Goal again" doesn't repeat

- README: chapter 06 lists it as a way to repeat, and by chapter 08 a recipe that pursues its own Goal joins its own pursuit and waits on itself. `Duelling` repeats through `WHEN stamina(?) LEARNED`.
- *Goals and Failure*: the one place where pursuing again does work is a `FAILED` Plan, where it retries without end and nothing checks it.

Spec: chapters 06, 08, 11. See also F5.

### B8. A default order can close a cycle

- *Precedence and Labels*, README: on `scandal`, one line in `HonorDuel`, one in `RoyalBanquet` and the default for `Poisoning` make a cycle. The banquet breaks it with a line it can write only by knowing what its Subplot declared. Chapter 32 doesn't say whether a default gives way.

Spec: chapters 13, 32. See also D4.

### B9. A Shift is promised by the language and applied by chance

- *Precedence and Labels*: VEsNA-Pro shifts only when the Agent chooses between several running Plans, so one scowl with nothing else going on shifts nothing and a busy Guest is shifted at every step. Whether a Plan that fails halfway has shifted is not said.

Spec: chapters 14, 32.

### B10. A tie only works by editing both Playbooks

`TIES` is written by the Plot and decided by Labels inside the Playbooks, which is what ADR 0008 set out to avoid.

- *Precedence and Labels*: with Labels on one side only, the unlabelled Plan counts as a perfect fit, and the tie behaves as an `OVER`.

Spec: chapters 13, 14, 32. See also F7.

### B11. Several Entry files: one Program or two

- *The Transpiler*: chapter 10 makes everything the Entry files reach one Program, and a Build is made from one Entry file. `regia build banquet.regin test.regin` can't be read.
- *The Visual Editor*: `royal_banquet.regia` is in two Programs, and nothing says which one its markers and its graph come from.

Spec: chapters 10, 23, 24.

### B12. The Build folder

- *The Transpiler*: it is named after the Entry file's name alone, so two `test.regin` share one. It holds files made again at every build next to the Traces we want to keep, and the Visual Editor clears it.

Spec: chapters 23, 24, 35.

### B13. The Trigger picker declares an Event nobody can send

- *The Visual Editor*: the default puts the new `EVENT` in the Plot's file, which no Playbook can import. The second choice, the Plot's Local Vocabulary, is refused by the language.

Spec: chapters 10, 25.

### B14. Undo takes back half of a rename

- *The Visual Editor*: once the "Undo all" notice is gone, undo in one tab reverts that file and leaves the others.

Spec: chapters 22, 24.

### B15. An unknown Target is skipped without a word

- *Instancing*: `TARGET JASN:` is read as settings for another Target. An unknown key gets a warning and an unknown Target doesn't.

Spec: chapter 21.

### B16. A `GOAL` declared in a Plot

- *Plots and Directors*: the Director can't pursue it and a local item can't be sent, so nothing can use it, and nothing says so.

Spec: chapters 10, 20.

## Deliberate limits

### L1. Placeholders are filled by matching (ADR 0001, ADR 0002)

- *Placeholders and Expressions*: in `grudge(?who, ?size)` one Placeholder is tested and one filled, and they look the same. A misspelt `?woh` is a new blank that matches anything.
- *Placeholders and Expressions*: `IF ?stake = ?gold:` compares and `?stake = ?gold.` names, both in a Body.

Spec: chapters 03, 04.

### L2. `GIVEN` is the Context and `IF` is control flow (ADR 0004)

Two constructs choose among alternatives. The showcase kept using the one that makes it repeat lines.

- *Plans*: with an `ELSE`, a `GIVEN` chain and an `IF` chain that fills the Body do the same job.
- *Plans*: no Statement can stand before or after the branches, so `Wagering` and `HonorDuel` write their last lines twice.
- *Plans*: "which Plan runs" has two shapes, siblings under one header and headers side by side, with two rules.
- *Placeholders and Expressions*: sibling `GIVEN`s may share names and two `IF`s in a row can't.
- *Randomness*: two `GIVEN`s that each roll read as the same chance and aren't.

Spec: chapters 06, 13.

### L3. `PURSUE` waits and `ASK` does not (ADR 0005)

- *Goals and Failure* (and a pointer in *Messages*): the two lines look alike, and `Serving` and `Dining` each carry a Comment to say which waits.

Spec: chapters 07, 08. See also F3.

### L4. A Director asks; a setup is written in the Agent's words (ADR 0009)

- *Goals and Failure*: `PURSUE` in a Body is the Agent's own and waits. In a setup it is an `ASK` from the Director and doesn't.
- *Plots and Directors*: `LEARN on_duty.` in a setup, `TELL ?winner on_duty.` in a Plan, and `LEARN` in a Director's Plan are three meanings in two spellings.

Spec: chapters 16, 20.

### L5. A kind word follows the item, except for Goals and Messages (ADR 0003)

- *Plans*: ten kind words, and a Goal being pursued has `TO` in place of `WHEN`.
- *Messages*: `TELL ?winner on_duty.` and `TELL Host guest_arrived(?late).` read the same, and only the Vocabulary says which one lasts.

Spec: chapters 05, 07.

### L6. Precedence is written where Playbooks are put together (ADR 0008)

- *Precedence and Labels*: the order for `scandal` is spread over two Plots, a default and two missing `ELSE`s. The conflict report is the only place to read it whole.

Spec: chapter 13. See also N9.

### L7. Phases are a set, and the `PHASE` lines look like a sequence

- *Plots and Directors*: which Phase follows which is found by reading every Body of the Plot.

Spec: chapter 20.

### L8. Events are global, and the Role files are fixed at build time

- *Vocabulary*: `challenged`, `hit` and `yielded` are used by `Duelling` alone and sit in the shared file, since an Event can't be local.
- *Translation to ASL*: a Guest holds the plans of `Scheming` from the first second, and every `idle` tests its guard.

Spec: chapters 10, 29.

### L9. The browser decides where a Project lives

- *The Visual Editor*: in Firefox or Safari the banquet is zipped in and zipped out, so the copy in git and the copy we edit are two.

Spec: chapter 24.

## Features for 2.0

### N1. No Trigger for a Goal that is reached, or that is over

A Goal has `DROPPED` and `FAILED`. Being reached is written at the end of every recipe, as a Signal with a name of its own.

- *Goals and Failure*: every recipe a Director depends on ends with `took_seat`, `toast_given` or `finished_eating`, each with its `EVENT` line.
- *Goals and Failure*: `Dining` writes `SIGNAL finished_eating.` four times, because "dinner is over, however it went" has no Trigger.
- *Vocabulary*: families of near twins, `take_seat`, `took_seat` and `seat`, told apart by a letter.

Spec: chapters 05, 11.

### N2. A Giving has no start and no end that anything can react to

Nothing fires when a Playbook is given or taken, and a Giving or a Subplot can't be tied to the Phase it is meant for.

- *Playbooks and Roles*, README: a Playbook can't set itself up or clean up. `Duelling` clears an old `stamina`, and `Dining` needs the Director's `ASK` because a Guest already hungry never sees `hungry LEARNED`.
- *Playbooks and Roles*: a Phase can't give a Playbook for as long as it lasts. Three `UNASSIGN`s in `farewell` are kept in step with three `ASSIGN`s elsewhere.
- *Goals and Failure*: a Director can't call off a Goal it asked for. It takes `Dining` away, the `DROPPED` Plan goes with the Playbook, and the plate keeps its Facts.
- *Subplots and Stagings*: a Subplot that should last a Phase is ended by hand in the next Phase's entry Plan.

Spec: chapters 15, 17, 20, 29.

### N3. A Playbook and a Plot don't declare what passes between them

A Playbook declares its Roles. The Goals it expects to be asked, the Signals it sends, and the Outcomes of a Plot are found by reading every Body. Since nothing is declared, nothing is checked, and what doesn't fit is lost in silence.

- *The Logic of Regia*, *Playbooks and Roles*: `Courtesy` is independent of its Plot only on paper.
- *Subplots and Stagings*: a Plot doesn't declare its Outcomes. `HonorDuel` has four `END PLOT` lines to find.
- *Showcase*: the table of every Signal and Outcome is the contract, and we made it by hand. Two Events already sit under the wrong banner.
- *Vocabulary*: every `EVENT` looks the same, whether the game, an Agent, a Playbook or a Subplot sends it.
- *Messages*: the pair `waiter` and `patron` is one relation written three times, and `MAPPING Host TO patron` compiles.
- *Messages*: where a Signal goes is not on its line.
- *Playbooks and Roles*: whether a Signal has a listener depends on the Givings the sender holds. A duel's winner seizes the Poisoner and tells the one Director that does nothing about it.
- *Plots and Directors*, README: a Signal with no Plan in the current Phase is lost. A Guest insulted during `reception` stands up, and no duel follows.
- *Subplots and Stagings*: an ending that no `ENDED` Block matches is ignored, and only the opposite mistake is warned about.
- *Goals and Failure*: an `ASK` to a Role that doesn't hold the recipe fails on the receiver, and the asker hears nothing.

Spec: chapters 05, 07, 10, 15, 17, 20.

### N4. The Sender can't be "the game" or "myself"

- *Messages*: no `FROM` means anyone or nobody. Any Agent that tells a Guard `saw_pouring(?rival)` gets `?rival` seized. `TO vent:` runs for anybody's `ASK`.
- *Goals and Failure*: `FROM` on a recipe makes the Agent's own `PURSUE` of that Goal fail at once, and eight of twelve recipes have one.
- *Goals and Failure*: a request that arrives second is ignored and its Sender lost, so `FAILED FROM DIRECTOR` depends on who asked first.

Spec: chapters 05, 07, 11.

### N5. No word for "me"

- *Messages*, README: the victim of an insult receives the gossip about itself, and `WHEN scandal(?victim)` can't say "unless it is me". The showcase sends two Messages for one insult.

Spec: chapters 03, 07.

### N6. A Failure has no reason a Plan can read, and only a Goal can fail in a way a Plan hears

- *Goals and Failure*: `WHEN bring(?dish, ?) FAILED` tells the Guest `sold_out` whatever went wrong. The reason is in the Trace.
- *Goals and Failure*: a `WHEN` Plan that fails can't be reacted to. Making `seize` recoverable means wrapping it in a Goal.
- *Plans*: after `, WITHOUT WAITING` the Agent never learns how the Action ended. `LEARN poured` is true whether or not the poison dissolves.

Spec: chapters 08, 11, 37.

### N7. A Director can't ask about its own state

- *Plots and Directors*: no condition on the current Phase. A `TRANSITION TO farewell` in `DURING PLOT` could enter it twice.
- *Plots and Directors*: an `EXITED` Plan can't tell where the Plot is going, nor an `ENTERED` Plan where it came from. It takes a Fact learned just before the `TRANSITION`.
- *Subplots and Stagings*: no condition on whether a Staging is running. One duel at a time is a counter kept in four places.
- *Subplots and Stagings*: a Subplot's `EXITED` Plan can't tell an ending by its parent from its own.
- *Quotas and Cast Changes*: a Director can't count the Agents of its Roles. (Chapter 26 keeps this for after 2.0.)

Spec: chapters 17, 19, 20, 26.

### N8. An Agent kind gives Propensity values and nothing else

Chapter 16 sends starting values that differ per Agent to Instancing, and chapter 21 doesn't take them.

- *Plots and Directors*: every Guest craves roast and pie. The purses differ only because of a roll.
- *Instancing*: a hothead can't start with a grudge or a heavier purse.
- *Instancing*: the Facts that most set one Guest apart, its seat and its grudges, are the ones the Program can't state.

Spec: chapters 16, 21. See also D14 and D15.

### N9. The command line is two words

`check` and `build`. Everything else the chapters describe has no command.

- *The Transpiler*: no command starts a Build. After the Diagnostics comes a Java class path.
- *The Transpiler*: no way to run a behaviour case of our own, though the `.trace` format would hold one.
- *The Transpiler*, *The Visual Editor*: the conflict report is printed "on request", and neither tool has the request.
- *The Transpiler*: the Target is "chosen on the command line", with no spelling for it.
- *The Transpiler*: how much the console shows is a Target setting, so quieting it means a new build.
- *Randomness*, *Instancing*: the seed can only be set in a behaviour case. A banquet that went wrong can't be played again.

Spec: chapters 13, 21, 23, 27, 34.

### N10. Only a whole story can be checked

- *The Transpiler*: a Playbook file gets "no Root Plot", and a Subplot's file is taken for the Root Plot.

Spec: chapters 10, 23.

### N11. A warning can't be answered

- *The Transpiler*: nothing marks a warning as seen, and the spec itself says some name-order warnings are false.
- *Placeholders and Expressions*: the laughing Plan keeps `?who` so that the three ways to take an insult look alike, and is warned for it.
- *Placeholders and Expressions*: `scandal(?victim)` written for the reader earns the warning, and `?` doesn't say what is ignored.
- *Precedence and Labels*: two of three `PRECEDENCE` lines exist only to silence a warning. The third case is D3.

Spec: chapters 03, 13, 23.

### N12. The Trace records what happened, not what didn't or why

- *The Transpiler*: a Signal nobody handles, a Quota two Guests short, a Plan that lost to another Playbook each leave nothing.
- *Precedence and Labels*: the three ways to take an insult write the same `PLAN` line, and nothing says why one was chosen.
- *Quotas and Cast Changes*: a Quota met while no `GIVEN` holds is lost without a trace, and it is the whole count.
- *Showcase*: six `PLAN WHEN ENTERED` entries read alike.
- *The Transpiler*: a Director is `director:HonorDuel` or `director:HonorDuel#1` depending on what else runs, and has a third name on the console.

Spec: chapters 34, 35.

### N13. `DURING PLOT` is off the default drawing

- *The Visual Editor*: the Phase map leaves out the poison's way into `farewell` and the Host's exit. We see the evening on which nothing goes wrong.
- *The Visual Editor*: the Docs tab lists what Phases do, and doesn't say whether `DURING PLOT` is on it.
- *The Visual Editor*: the Layers write on Phase nodes, so `ASSIGN Keeping_watch TO ?winner.` has no node.
- *The Visual Editor*: deleting a Phase deletes Plans the drawing didn't show, and leaves `farewell` taking away a Playbook nobody is given.

Spec: chapter 25.

### N14. The Trigger picker offers bare Events

- *The Visual Editor*: none of the banquet's three arrows could be drawn. They have a Sender and a quantity, and the picker gives `WHEN feast_cancelled:`, which anyone sets off.
- *The Visual Editor*: the new `EVENT` line goes after the last one, under the wrong Comment banner.

Spec: chapter 25. See also B13.

### N15. A kind is written whole every time

- *Instancing*: `latecomer` repeats `noble`, and four kinds of Guest would become six with one more trait.
- *Instancing*: going from two knights to one rewrites the knight in full, and the copies drift.
- *Instancing*, README: a later file can't remove a kind. `hothead` is emptied, still exists, and is warned about for values we dropped on purpose.
- *Instancing*: a `TARGET` Block is overridden line by line and an `AGENT` Block whole.
- *Instancing*: `king PLAYS Host` says one thing twice.

Spec: chapter 21.

## Features for a later version

### F1. Roles can be mapped and addressed, and little else

Chapters 15 and 26 list this as *Richer Mappings and Role tests*: counted recipients, a pick per receiver, testing whether an Agent plays a Role, counting a Role. The showcase is wrong in two places because of it (the roasts and the duellists who cheer).

- *Messages*, README: `ASK waiter TO bring(…)` reaches every Servant. Three Servants put three roasts on one plate.
- *Playbooks and Roles*: `1 OF` on a Mapping is the same one for all. "A Servant of their own" can't be written.
- *Subplots and Stagings*, README: a whole-Role Mapping can't say "everyone else". The duellists wager on their own duel, and the small cast meets `3 OF Spectator` only because of it.
- *Randomness*: `1 OF Guest` can't leave out the Guards, so a knight can be Poisoner and Watchman at once.
- *Playbooks and Roles*, README: a Playbook can't ask which Roles an Agent plays. The Host's Plans sit in a Playbook every Servant holds.
- *Playbooks and Roles*: a Role gives up an Agent only when a Message arrives from it. `DO lunge.` has no target.
- *Plots and Directors*, README: a Director can't name the one Agent of `Challenger`. The winner has to Signal so that `FROM ?winner` fills a Placeholder.
- *Subplots and Stagings*: an Outcome carries only what the Director was handed, so `duel_abandoned` can't say who was duelling.
- *Messages*: between one Role and `EVERYONE` there is no recipient, and a knight hears a `TELL` per Role twice.
- *Plots and Directors*: `ASSIGN Courtesy, MAPPING Host TO host.` four times. A Plot can't say "everyone in it".

Spec: chapters 07, 15, 16, 20, 26.

### F2. A Giving and a Staging have no identity

Chapter 17 keeps "picking out one of several running Stagings" for later. Until then two duels at once are one duel.

- *Subplots and Stagings*, README: an Agent in two duels has one `opponent` holding both, and its `duel_won` ends every duel in `fighting`.
- *Playbooks and Roles*: a Plan can't tell its Givings apart, to Signal one Director or keep a Fact per Giving.
- *Playbooks and Roles*: `UNASSIGN Keeping_watch FROM ?winner` also takes the Giving of the Guard setup, so the guard of honour never ends.
- *Subplots and Stagings*: `WHEN HonorDuel ENDED` doesn't say which Staging ended.
- *Subplots and Stagings*: `END SUBPLOT` ends all the Stagings of a Plot or none.
- *Subplots and Stagings*: a second insult between Ada and Bruno starts a second duel between Ada and Bruno.

Spec: chapters 15, 17, 20, 29, 31. See also N7.

### F3. A request has no reply

Chapter 07 keeps room for replies, refusal and waiting on an `ASK`. Today every answer is a Message with a name of its own.

- README: a Body can't wait for the answer to an `ASK`. `Dining` waits a minute and counts the plate.
- *Goals and Failure*: `SIGNAL took_seat.` and `TELL ?guest sold_out(?dish).` are replies written by hand.
- *Goals and Failure*: `WHEN take_seat FAILED` sends `took_seat` from a Guest standing by the wall, since the Director never hears of a Failure.
- *Messages*: nothing shows the duel as one exchange. Five Plans and three shared Events are put in order in our heads.

Spec: chapters 07, 15.

### F4. Time is one `WAIT` on the wall clock

- *Plans*: `WAIT` can't end early. The Guest waits the whole minute with both dishes on the plate, and fails when the roast was two seconds away.
- *Plots and Directors*: a Phase's timeout is the tail of its entry Plan, one per Phase, found by noticing a `WAIT`.
- *Translation to ASL*: `WAIT 2 MINUTES` runs out while the game is paused.

Spec: chapters 12, 28.

### F5. No loop, and no weighted Pick

- *Matching*: a dish served after the second `FOR EACH` has started is never eaten.
- *Randomness*: Options have Weights and Matches don't. "The bigger the grudge, the likelier" can't be written.

Spec: chapters 06, 09, 26. See also B7.

### F6. One Plan per Trigger, and Plans that know nothing of each other

Chapter 13 lists all of these as not in 2.0.

- *Precedence and Labels*: the knight can't both watch the speaker and snigger.
- *Plots and Directors*: a Phase's Plan replaces `DURING PLOT`'s and can't add to it.
- *Quotas and Cast Changes*: a `JOINED` Plan in `feast` would replace the one that has the Host bow.
- *Showcase*: one Agent drops a handkerchief and draws a sword at once, and a Servant goes to the kitchen twice. Nothing says two Actions need the same body.
- *Plans*: `IF hungry` in `Dining` races the Playbook's own `DROP`, and the source doesn't show who wins.
- *Plots and Directors*: `WAIT` is an error in an `EXITED` Plan, and `DO clear_tables.` holds the Plot between two Phases all the same.
- *Precedence and Labels*: a relation can't name one Trigger Block, and takes one item per line.
- *Precedence and Labels*: a tie can't cross a Plot.
- *Instancing*: a `PRECEDENCE` line of the Plot is needed only because of an `AND` in a `.regin` file, and neither file shows the link.

Spec: chapters 13, 21, 32.

### F7. What the Selection function does is the Target's business

Chapter 14 keeps a neutral ranking, a `SHIFT` Statement and Propensity tests for later.

- *Precedence and Labels*: three alternatives name three sets of Propensities, and the source doesn't say which one a knight runs.
- *Precedence and Labels*: with no neutral alternative a fallback is one more point in the space, and one `SUITS` forces a Label on every sibling.
- *Precedence and Labels*: no condition tests a Mood and no Statement changes it.
- *Precedence and Labels*: a Shift is all or nothing for the Plan.
- *Instancing*: a `SUITS` on a Propensity the Agent has no value for is left to the Target.

Spec: chapters 14, 21, 32. See also B9 and B10.

### F8. Values are neither declared nor typed

Chapter 03 keeps `name: type` free for later.

- *Vocabulary*: `DO walk_to(kitchn)` is a correct Program.
- *Vocabulary*: `person` sixteen times, `dish` ten. The Parameter names do the work of types and nothing holds them to it.
- *Subplots and Stagings*: `MAPPING ?offender TO Defender` reads the same whether or not `?offender` is a Guest. If not, the duel waits for nobody.
- *Quotas and Cast Changes*: `ASK ?gone TO take_leave.` compiles and is dropped at run time.
- *Translation to ASL*: `ASSIGN Keeping_watch TO ?winner` puts the Playbook in every Role file, since the source can't say that `?winner` is a Guest.

Spec: chapters 03, 15, 19, 29.

### F9. Only the Root Plot has a living cast

Chapters 19 and 21 keep joiners in Subplots and Roles outside the Root Plot for later.

- *Subplots and Stagings*: a whole-Role `MAPPING` is live on an `ASSIGN` and a copy on a `START SUBPLOT`.
- *Plots and Directors*, README: nothing in `royal_banquet.regia` says it is the Root Plot. As a Subplot of `Castle` it would read the same and no latecomer could join it.

Spec: chapters 17, 19, 21.

### F10. An Action can't be called off, and some things have no short spelling

- *Translation to ASL*: when `have_dinner` is dropped during `eat(roast)`, the Guest goes on eating.
- *Plans*: every `CHANGE` repeats its Fact three times to add or take away one.
- *Randomness*: "three times in ten, otherwise nothing" needs an empty Option, which is warned about, or `IF RANDOM(1, 100) <= 30:`.
- *Matching*: `IF COUNT(on_plate(?)) = 0:` for `IF NOT on_plate(?):`.
- *Matching*: a bare `HIGHEST` leaves ties open and nothing reminds us.

Spec: chapters 08, 09, 26, 37.

## To discuss

### D1. A few words do many jobs

The largest group of "constructs that read alike". Some are harmless, and the question is which are worth a second word.

| Word | Jobs | Found in |
|---|---|---|
| `TO` | receiver of an `ASSIGN`, Role of a `MAPPING`, Goal of an `ASK`, `TRANSITION TO`, `CHANGE … TO`, the opening of a recipe | *Playbooks and Roles* |
| `AT` | `, AT RANDOM`, `SUITS bravery AT 0.8`, `bravery AT RANDOM(…)` | *Matching* |
| `OR` | operator in a condition, opening of an Option | *Randomness* |
| `=` | comparison, naming, Target setting | *Placeholders and Expressions*, *Instancing* |
| `COUNT` | Matches of a condition, Agents of a kind | *Matching* |
| `,` after a condition | a Pick, which chooses a Match, or a Label, which describes the Plan | *Matching* |
| `FROM Guest`, `FROM ALL Guest` | a Plan per Signal, or one after many. `FROM 1 OF Guest` is the first under the rules of the second | *Quotas and Cast Changes* |
| `SELF` | a Plot's own Playbooks, or the Plot with all it starts | *Precedence and Labels* |
| `.` | ends a Statement, marks a decimal, joins an External name | *Syntax* |
| `#` | `#`, `#[`, `#@`, `#%`, and `#!`, which the grammar doesn't know | *The Transpiler* |
| quantity | an Expression in a Mapping, a written Number in a Quota, a `RANDOM` with written bounds in Instancing | *Placeholders and Expressions*, *Quotas and Cast Changes* |

Spec: chapters 01, 02, 04, 09, 13, 15, 18, 21, 26. `LEARN` and `PURSUE` in a setup are L4.

### D2. A missing `ELSE` means two things, and one of them is a decision about other Playbooks

- *Plans* (and a pointer in *Goals and Failure*): under a Goal it fails at once, under an Event it falls through. Four Blocks carry a Comment to say which.
- *Precedence and Labels*: adding `ELSE: DO sip_wine.` to one Playbook ends the hushing in every duel, with no warning anywhere.

Spec: chapters 06, 11, 13.

### D3. Name order is the default Precedence

- *Precedence and Labels*: had `Keeping_watch` been called `Watch`, the knights would snigger. A rename changes behaviour and a warning is the only sign.

Spec: chapter 13.

### D4. A Subplot orders itself against a parent it can't see

- *Precedence and Labels*: `PARENT OVER SELF ON scandal` is written blind. From another parent it orders nothing, or Plans its author never saw.
- *Precedence and Labels*: `SELF` is a Plot's own Playbooks in one file and its whole subtree in the other, and a Subplot can't place itself against its siblings.

Spec: chapters 13, 32. See also B8.

### D5. A Goal's arguments are its identity

- *Goals and Failure*, README: `bring` carries the seat so that two orders of roast are two Goals, and `fetch` carries it for nothing else.

Spec: chapters 05, 08. See also N4.

### D6. A `DROP` goes down as a drop and up as a Failure

- *Goals and Failure*: `DROP fetch(…)` fires `FAILED` on the `bring` above it, though we chose to stop.

Spec: chapters 08, 11.

### D7. A Giving is standing and a Message is sent once

What a Role gets "whenever it arrives" has three homes with three behaviours.

- *Quotas and Cast Changes*: the setup, a whole-Role `ASSIGN` and an entry Plan's `ASK` differ for a joiner. `feast` uses two of them two lines apart.
- *Messages*: a latecomer gets `Dining` and not the request to dine.
- *Quotas and Cast Changes*: so a joiner raises the bar of the feast's Quota for a Signal nobody asked it to send.
- *Quotas and Cast Changes*: a setup can't depend on the Phase. A latecomer in `farewell` walks to its seat and to the door at once.

Spec: chapters 16, 18, 19, 20.

### D8. A Quota counts, and that is all it does

- *Quotas and Cast Changes*: the Plan knows that enough Agents sent the Event and never which. `HonorDuel` keeps `wager` Facts from a plain Trigger beside it.
- *Quotas and Cast Changes*, README, *Vocabulary*: an argument splits the count, so `cheered` exists only to be counted, next to `wagered` and `wager`.
- *Quotas and Cast Changes*: it fires every time the count fills again. "Once" is a Phase change or a Fact and a `GIVEN`.

Spec: chapter 18. See also N12.

### D9. The size of a Quota is in the Plot and the size of the hall in Instancing

- *Quotas and Cast Changes*: with two Guests, `3 OF Spectator` waits for a cheer that can't come, and nothing warns.
- *Quotas and Cast Changes*: `ALL` of an empty Role is never met, and no `EMPTIED` fires.
- *Quotas and Cast Changes*: a Quota can fire on a departure, under a Trigger that names an Event nobody sent.

Spec: chapters 18, 19, 21.

### D10. What an Agent or a Director has been told stays as it was

- *Messages*: the Director can take a Playbook back and not a Fact. The winner is on duty for good.
- *Messages*: only the first teller of a Fact counts. To count tellers we tell an Event, so `FACT` or `EVENT` is decided by how we want it received.
- *Plots and Directors*: the `wager` Facts are a copy kept by hand. A Spectator who walks out leaves one behind, and the Pick can choose it.
- *Quotas and Cast Changes*: an Agent never hears of a cast change. A Challenger goes on telling `hit` to a Role nobody plays.

Spec: chapters 07, 19, 20.

### D11. How a Subplot's ending reaches its parent

- *Subplots and Stagings*: `WHEN HonorDuel ENDED:` means "abandoned" because of the Block above it. "Ended with no Outcome" can't be written alone.
- *Subplots and Stagings*: what follows a Subplot is in another Plan, tied to the `START SUBPLOT` by a name. A Director can't start one and wait.
- *Subplots and Stagings*: a Subplot ended from above reports nothing, so the tidying is written twice.

Spec: chapters 17, 20, 31.

### D12. Being cast in a Subplot adds and never takes away

- *Subplots and Stagings*: a Challenger still holds `Dining` and eats between lunges. Taking it away leaves nobody who knows to give it back.

Spec: chapters 13, 17.

### D13. A Plot takes no arguments

- *Subplots and Stagings*: `HonorDuel` can't be told what the quarrel was about. What differs between two Stagings comes in through the Cast.

Spec: chapter 17.

### D14. The Vocabulary names what the game supplies and not what the game does

- *Vocabulary*: that the game can refuse an Action is in a Doc comment, where no tool can use it.
- *Vocabulary*: only the External name shows that `hungry` is the game's and `on_duty` the Agents'.
- *Showcase*: telling one run took seven behaviours of the game that no file states.
- *Quotas and Cast Changes*, README: leaving is the game's answer to `DO leave_hall`, and a Statement after it reads as reachable.
- *Instancing*: to know a noble we read a `.regin` file, a Plot and the game's own data.

Spec: chapters 10, 19, 37.

### D15. Rules the spec doesn't give

- *Randomness*, README (and a pointer in *Plots and Directors*): a roll in a Role setup is made once, or once per Agent. The showcase assumes the second.
- *Randomness*: what the seed covers is a list of constructs that leaves out `RANDOM` in a Body and the Agents drawn by `n OF`.
- *Syntax*: a Doc comment above `FACT purse(gold), craves(dish), on_duty` describes the first item, or all three.
- *Randomness*: a wrong Weight is repaired, skips the choice or fails the Plan, depending on how it is wrong.

Spec: chapters 02, 09, 16, 34.

### D16. Parts of the syntax the showcase never needed, or used without choosing

- *Syntax*: the `.` is optional. The showcase writes it on Statements and not on Vocabulary lines, and the Visual Editor writes none.
- *Syntax*: 700 lines never used a `;`. The one-line style brings a rule, the `;;` and an error with it.
- *Syntax*: a blank line means something only under a Doc comment.
- *Syntax*: `#@desc` and `#` differ by a character, and the showcase documents its Plans with the one tools skip.
- *Syntax*: importing what we use is a habit nothing checks.
- *The Visual Editor*: with one Vocabulary file every label carries `↗`, so the mark says nothing.
- *Instancing*: Instancing comments are a second home for a cast, and two files can then disagree about a kind.
- *Instancing*: Target settings have their own rules: `JASON` in capitals, `most_similar` declared nowhere.

Spec: chapters 01, 02, 10, 21, 25.

### D17. A Plot's Role and a Playbook's Role are told apart by a capital

- *The Logic of Regia*, *Playbooks and Roles*, README: `Host` and `host` need a `MAPPING` on all four setups. Spelled alike they would bind without a line, and the Plot wouldn't show that `Courtesy` has a Role.
- *Translation to ASL*: both are `host` in the Build.

Spec: chapters 15, 16.

### D18. The drawing is of a Plot

- *The Visual Editor*: eleven of fourteen files have no drawing. The eight Playbooks are 244 lines against the Plots' 183.
- *The Visual Editor*: so they have no Docs tab, and a Doc comment of the Vocabulary is read in its file or not at all.
- *The Visual Editor*: the Nested Plans view has no place for Roles.
- *The Visual Editor*: `END SUBPLOT` and a Director's `LEARN` are on no Layer, and the card of a Plan whose Body is one `LEARN` is empty.
- *The Visual Editor*: two Plans that differ by an `ASK` are two arrows with the longest label on the map, and the `ASK` isn't drawn.

Spec: chapter 25. See also N13.

### D19. Edits that go further or less far than they look

- *The Visual Editor*: a rename follows references. The Doc comment that names the Plot and the file `honor_duel.regia` keep the old name.
- *The Visual Editor*: the rules for moving an Extent are given in detail, and no operation moves one.

Spec: chapters 22, 25.

### D20. Diagnostic codes follow the spec's table of contents

- *The Transpiler*: `R13` means Plan selection only to someone who knows the spec. The digits don't give the severity.
- *The Transpiler*: the note is a severity with one member, `R1311`.

Spec: chapters 23, 27.

## What the whole guide shows

No single chapter shows these. Each is a pattern across the causes above.

### The seam between a Playbook and a Plot carries most of the notes

N1, N2, N3, N4, F1, F2 and F3 are all about what passes between an Agent's Playbook and whoever gave it: what is asked, what is answered, who is meant, and which Giving it belongs to. A Playbook is meant to be written without knowing its Plot, and the showcase's Playbooks know their Plots well. They send the Signal a Quota counts, carry an argument that a Mapping needs, and end with the Event a Phase waits for.

### Silence

The commonest runtime result of a mistake is nothing. A Signal with no listener (N3), an ending no Block matches (N3), a Quota met with no `GIVEN` (N12), a Mapping of an Agent outside the Cast (F8), an `ASK` to someone who has left (F8), a Quota that can't be met (D9), a Target name misspelt (B15), a Shift not applied (B9). Most of them leave no entry in the Trace either. "Why did nothing happen" was the question we asked most often while telling the run.

### Four mechanisms answer "which Plan runs"

Text order among `GIVEN`s (L2), fit among `SUITS` alternatives (F7), Precedence between Playbooks (L6, D3, D4), and falling through a missing `ELSE` (D2). Each is reasonable alone. For `scandal` or `insulted` a reader needs all four, in three files, and the conflict report that puts them together has no command (N9).

### Three places say what an Agent starts with

Instancing gives Propensity values, a Role setup gives Facts, Goals and Playbooks, and the game gives the rest (N8, D14, D7). The seat and the grudges, which decide most of the evening, are in the third.

### Three ways to carry a piece of news

A told Fact, an Event with a Fact kept by the receiver, and a Signal counted by a Quota (D8, D10, L5). The choice between `FACT` and `EVENT` ends up made by how the receiver should treat it, and one happening often needs two names (`wagered` and `wager`, `poured` and `poison_poured`).

### Ceremony that repeats

- A done-Signal with its own `EVENT` line for every Goal a Director waits on (N1).
- `MAPPING Host TO host` on every setup (D17), and `ASSIGN Courtesy` once per Role (F1).
- An `UNASSIGN` or an `END SUBPLOT` in another Block for every `ASSIGN` or `START SUBPLOT` (N2).
- A counter or a copy kept as a Director's Fact: wagers, duels running, who is left (N7, D10).
- A second kind in Instancing for every variation of a first (N15).
- The last lines of a Body, written under each `GIVEN` (L2).

### Comments that do the language's work

The showcase explains in a Comment what the source can't say: what a missing `ELSE` does (four times), which of `PURSUE` and `ASK` waits, why `fetch` carries a seat, which Events are Signals, which Actions the game can refuse, that `leave_hall` ends the Agent. Each of these Comments marks a cause in this list (D2, L3, D5, N3, D14).

### Workarounds that say the opposite of what they mean

`took_seat` sent by a Guest who has no seat (F3). `sold_out` told for a dish in the Servant's hands (N6). `cheered` sent beside `wagered` so that something can be counted (D8). `duel_won` Signalled so that the Director learns a name it gave out itself (F1). These are the places where a reader of the showcase is most likely to be misled, since the Program is correct and its words aren't.
