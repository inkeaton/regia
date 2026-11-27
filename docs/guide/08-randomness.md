# Randomness

A Guest with nothing to do gets `idle` from the game, again and again through the evening. If its Plan for `idle` were fixed, a whole table of nobles would chat at the same moments and do the same thing all night. Wherever we want variety, we ask for chance. Regia has these ways of asking:

| We write | Chance chooses | Where it is explained |
|---|---|---|
| `RANDOMLY:` with `OPTION:` Blocks | one of several written Blocks | here |
| `RANDOM(a, b)` | a Number | *Placeholders and Expressions*, and here |
| `, RANDOMLY` or `, WEIGHT …` on a condition | one of its Matches | *Matching*, and here |
| `1 OF Guest`, `50% OF peer` | which Agents of a Role | *Playbooks and Roles*, and here |
| `RANDOM(…)` in a Role setup, `AT RANDOM(…)` in Instancing | each Agent's starting values | here |

A run has one seed, and the seed covers all of them, so that a run can be played again (*The seed*, below).

## One of several Options

[`playbooks/noble_socializing.regia`](../showcase/playbooks/noble_socializing.regia)
```regia
# Small talk. The more grudges we hold against those at the table, the likelier we vent one.
WHEN idle:
    LET ?grudges BE COUNT(grudge(?foe, ?) AND ?foe PLAYS peer)
    RANDOMLY:
        OPTION, WEIGHT 3: DO chat
        OPTION, WEIGHT 2:
            DO sip_wine
            IF RANDOM(1, 100) <= 30:     # one cup too many
                DO laugh
        OPTION, WEIGHT ?grudges: PURSUE vent
        OPTION, WEIGHT 5: PASS           # nothing, this time
```

A Random choice is a Statement of a Body: a `RANDOMLY:` Block whose children are `OPTION:` Blocks. When the Body reaches it, exactly one Option runs, picked at random, and the Body carries on after the `RANDOMLY` Block. This Guest chats, sips wine, vents a grudge, or does nothing. Leaving the Weights for the next section, those are its four Options.

- An Option is an ordinary Block, indented under its header or inline on the header's line. The whole choice fits on one line too: `RANDOMLY: OPTION: DO wave; OPTION: DO yawn`, with `;` closing each Option (*Syntax*).
- Only `OPTION` Blocks stand directly under `RANDOMLY:`, and an `OPTION:` stands nowhere else.
- An Option holds any Statements, mixed freely: Actions, `PURSUE`, `IF`, `FOR EACH`, another Random choice.
- An Option has no condition of its own. To make one depend on a Fact, we write an `IF` inside it, as the sip of wine does with its roll. The Option keeps its share of the choice and does nothing when the `IF` doesn't hold. A Weight that comes to 0 is the other way (next section).
- An Option that does nothing holds `PASS`. That is how "only sometimes" is written, in shares like any other Option. An Option with no body at all is an empty Block, and warned about like one.
- A `RANDOMLY` with a single Option always runs it. That is allowed, with a warning: a generator building Options from a list may well produce one. One with no Option is an error.
- `RANDOMLY` chooses among Blocks we wrote. Choosing among the Matches of a condition is a Pick, which shares the word: `, RANDOMLY` means "chosen by chance" in both places (*Random Picks*, below).

**Checks**

- A `RANDOMLY` with no `OPTION` → `R09_01-randomly-without-options`
- A Statement other than `OPTION` directly under `RANDOMLY:`, or an `OPTION:` anywhere else → `R09_02-wrong-randomly-nesting`
- A `RANDOMLY` with a single `OPTION` → `R09_05-randomly-with-one-option` (warning)
- An Option with no body → `R01_06-block-without-body` (warning)
- The retired headers `EITHER:` and `OR:` → `R09_06-retired-either` (hint: `RANDOMLY:` with one `OPTION:` per Option)

Spec: chapter 09, *`RANDOMLY` / `OPTION`*.

## Weights

A Weight is the clause `, WEIGHT <Expression>` on an `OPTION` header, before the `:`. An Option without one weighs 1. The chance of an Option is its Weight divided by the sum of all the Weights, so in the `idle` Plan above:

| Grudges at the table | `chat` | `sip_wine` | `vent` | nothing |
|---|---|---|---|---|
| 0 | 3 in 10 | 2 in 10 | never | 5 in 10 |
| 2 | 3 in 12 | 2 in 12 | 2 in 12 | 5 in 12 |
| 5 | 3 in 15 | 2 in 15 | 5 in 15 | 5 in 15 |

- Weights are relative. There are no percentages to keep at 100, so adding an Option never breaks the others. The price is that no Weight reads alone: `WEIGHT 3` means nothing until we have summed the rest, and here one of the rest is known only at runtime.
- A Weight is any Expression: a Number, a filled Placeholder, arithmetic, a `COUNT`, a roll. Its Placeholders must be certainly filled before the `RANDOMLY`, which is why `?grudges` is named one line above it.
- All the Weights are worked out together, once, when the Body reaches the `RANDOMLY`, and then the roll is made. Nothing an Option does changes the roll that chose it.
- A Weight of 0 means the Option is never picked. In `WHEN idle` that keeps a Plan from failing: `TO vent` has no `ELSE`, so a Guest with no grudge at the table would fail to vent. `WEIGHT ?grudges` keeps it from trying.
- A Weight is a plain Number, never a share: `WEIGHT 30%` is an error.

"Only sometimes" has two spellings, and the showcase uses both. The `PASS` Option counts in shares, against the other Weights: with no grudges, the Guest does nothing half the time. `IF RANDOM(1, 100) <= 30:` counts in hundredths, against nothing else: the Guest who sips laughs three times in ten. Use `PASS` when the chance sits among other Options, and a roll when it stands alone.

Wrong Weights are treated in three ways:

| The Weights are | What happens |
|---|---|
| one negative | it counts as 0, and the Trace writes an entry |
| all 0 or less | no Option runs, the Trace writes an entry, and the Body carries on |
| one not a Number | the Plan fails |

Neither entry is a warning, since both can be meant. "None of these, this time" is a fair thing to write, and a computed Weight such as `?anger - 2` that drops below 0 means "never". The writer has nothing to clamp it with, so nothing warns.

**Checks**

- A Weight whose Placeholders aren't certainly filled before the `RANDOMLY` → `R09_03-maybe-unfilled-weight`
- `WEIGHT 30%` → `R15_17-misplaced-percent-sign`
- A Weight that isn't a Number → `T09_01-weight-not-number` (Trace, Failure)
- A negative Weight, counted as 0 → `T09_02-weight-below-zero` (Trace entry)
- Every Weight is 0 or less, and no Option runs → `T09_03-all-weights-zero` (Trace entry)

Spec: chapter 09, *Weights*. For Expressions, chapter 04; for `%`, chapter 15.

## Placeholders in an Option

```regia
WHEN duel_on, FROM DIRECTOR:
    GIVEN purse(?gold) AND ?gold >= 2:
        RANDOMLY:
            OPTION, WEIGHT 3: LET ?stake BE 1               # a careful coin
            OPTION: LET ?stake BE RANDOM(1, ?gold / 2)
        UPDATE purse(?gold) TO purse(?gold - ?stake)        # every Option filled ?stake
        SIGNAL wagered(?stake)
```

A careful Spectator, unlike the one in `Wagering`, bets a single coin three times in four. Both Options name `?stake`, so it is filled whichever runs, and the Body uses it after the choice.

The rules are those of the branches of an `IF`, with Options in the place of branches:

- A Placeholder filled inside an Option, by `LET` or by an `IF` condition, can be used inside that Option.
- Sibling Options may fill the same Placeholder, since only one of them runs.
- A Placeholder filled in every Option outlives the choice: it is certainly filled after it.
- One filled in some Options but not all can't be used after the choice, nor anywhere in the Plan but a sibling Option. An Option holding only `PASS` fills nothing, so a choice with a `PASS` Option fills nothing that outlives it:

```regia
RANDOMLY:
    OPTION: LET ?stake BE 1
    OPTION: PASS                         # no bet this time
SIGNAL wagered(?stake)                   # error: the PASS Option leaves ?stake empty
```

- Placeholders filled before the choice can be used in every Option and in every Weight: `?gold` above.

**Checks**

- A Placeholder filled in some Options but not all, used after the choice or outside a sibling Option → `R09_04-option-placeholder-outside-option`

Spec: chapter 09, *Placeholders in an Option*. For `IF` branches, chapters 04 and 06.

## Where a Random choice goes

```regia
DURING PLOT:
    WHEN HonorDuel(?) ENDED:
        RANDOMLY:
            OPTION: DO play_music
            OPTION, WEIGHT 2: PASS              # the musicians tire of duels
```

A Random choice goes wherever a Statement goes. Here the banquet's Director has music played after one duel in three. The showcase's Director plays it after every duel.

- It goes in any Body: a Playbook's Plans, a Director's Plans, inside an Option, an `IF` branch or a round of `FOR EACH`.
- It never goes in a Role setup. A setup holds only `ASSIGN`, `LEARN` and `PURSUE`, the same Statements for every Agent of the Role. Its Expressions can roll, once per Agent (*Random starting values*, below).
- It is a Statement, so it never stands in a Context or a condition. A roll does (next section).

**Checks**

- `RANDOMLY` in a Role setup → `R16_02-wrong-statement-in-setup`

Spec: chapter 09. For setups, chapter 16.

## Rolls

[`playbooks/duelling.regia`](../showcase/playbooks/duelling.regia)
```regia
TO strike:
    GIVEN stamina(?):                    # chosen while we can still fight …
        WAIT RANDOM(1, 3) SECONDS
        IF stamina(?):                   # … and still able, now that the wait is over?
            DO lunge
            TELL opponent hit
            PURSUE strike, WITHOUT WAITING
```

Both duellists hold this recipe and start with the same stamina. Each rolls its own wait before every lunge, and the rolls decide who lands three hits first.

`RANDOM(a, b)` is an Expression, and *Placeholders and Expressions* has its rules. From the side of chance, three of them matter:

- It is whole or decimal by how its bounds are written, never by what they work out to. `WAIT RANDOM(1, 3) SECONDS` waits one, two or three seconds, never 1.4. A wait anywhere between them is `RANDOM(1, 3.0)`.
- Every `RANDOM(…)` is a fresh roll, each time the Statement or the condition holding it is reached. A roll used twice is named once, with `LET`, as `Wagering` names its stake.
- In a Context or an `IF`, a roll is compared and gone, for a Plan that applies only some of the time: `IF RANDOM(1, 100) <= 30:`.

**Checks**

- A whole roll with no whole number between its bounds, in a Body → `T04_03-empty-whole-roll` (Trace, Failure)

Spec: chapter 04, *Random numbers*. For Durations, chapter 12.

## Random Picks

[`plots/honor_duel.regia`](../showcase/plots/honor_duel.regia)
```regia
AFTER 20 SECONDS:                    # betting closes
    GIVEN wager(?backer, ?stake), HIGHEST ?stake, RANDOMLY:
        ASK ?backer TO give_signal
    ELSE:
        ENTER fighting               # nobody bet: no handkerchief to wait for
```

A Random choice picks among Blocks we wrote down. A Pick picks among the Matches of a condition, which exist only at runtime: here the wagers the Spectators happened to make. `HIGHEST ?stake` keeps the biggest, and `RANDOMLY` breaks a tie between two Spectators who bet the same.

| We write | Chance chooses |
|---|---|
| `, RANDOMLY` | one Match, each equally likely |
| `, HIGHEST ?p, RANDOMLY`, `, LOWEST ?p, RANDOMLY` | between the Matches tied on `?p` |
| `, WEIGHT <Expression>` | one Match, each as likely as its Weight |

`TO vent` in `NobleSocializing` uses the last: `GIVEN grudge(?foe, ?size) AND ?foe PLAYS peer, WEIGHT ?size:`, the bigger grudge the likelier insult. A weighted Pick has the Weights of a Random choice, with Matches in the place of Options, and the same rules for wrong ones, except that when every Weight is 0 the condition has no Match and its `ELSE` runs.

A condition with several Matches and no Pick uses one, and the language doesn't say which. Unsaid doesn't mean random: a Target may give the same Match every time, so a Guest whose `vent` had no Pick could sneer at the same foe all evening.

**Checks**

- `WEIGHT` with `HIGHEST`, `LOWEST` or `RANDOMLY` → `R26_01-conflicting-pick-clauses`
- The retired `, AT RANDOM` → `R26_06-retired-at-random` (hint: `, RANDOMLY`)
- Every Match weighs 0 or less → `T26_01-all-pick-weights-zero` (Trace entry)

Spec: chapter 26. For Weights, chapter 09.

## A random part of a Role

[`plots/royal_banquet.regia`](../showcase/plots/royal_banquet.regia)
```regia
WHEN ENTERED:
    START SUBPLOT Poisoning,
        MAPPING 1 OF Guest AS Poisoner,
        MAPPING Guard AS Watchman,
        UNTIL EXITED
```

Nobody decides who the Poisoner is, the Director included. `1 OF Guest` draws one Guest at random when the Statement runs. The same draw works in the target of an `ASSIGN` and in a recipient:

[`playbooks/noble_socializing.regia`](../showcase/playbooks/noble_socializing.regia)
```regia
WHEN scandal(ME), FROM peer ?speaker:
    SHIFT sympathy BY -0.2
    TELL 50% OF peer wronged(ME, ?speaker)
    PURSUE resent(?speaker)
```

- The Agents are drawn uniformly, from those playing the Role at that moment. A recipient's draw leaves out the sender.
- The draw is made each time the Statement runs. The Poisoner, drawn once when the Staging starts, stays the same Guest for the whole Staging. `ASK 1 OF waiter TO bring(…)` in `Dining` draws again for every dish, so two dishes may go to two Servants.
- No Agent is drawn twice in one Statement. Counted picks from one Role in one Statement share a pool. Draws in different Statements are independent.
- A share, or a count that isn't whole, rounds up: `50% OF peer` with seven other peers draws four.
- The count is an Expression, so it can roll too: `MAPPING RANDOM(1, 3) OF Host AS confidant`.
- A count that asks for more Agents than are left takes everyone left, and a negative one takes nobody, each with a Trace warning. A count that isn't a Number fails the Plan.

**Checks**

- A counted `ASSIGN` target or `MAPPING` in a Role setup → `R16_03-misused-to-in-setup`
- A count or share that isn't a Number → `T15_01-count-not-number` (Trace, Failure)
- A count asking for more Agents than are left → `T15_02-count-exceeds-pool` (Trace warning); a negative count → `T15_03-count-below-zero` (Trace warning)

Spec: chapter 15, *Counts and fractions*. For a Subplot's casting, chapter 17.

## Random starting values

[`plots/royal_banquet.regia`](../showcase/plots/royal_banquet.regia)
```regia
ROLE Guest:
    LEARN purse(RANDOM(5, 20))           # rolled for each Guest
    LEARN craves(roast)
    LEARN craves(pie)
    PURSUE take_seat
```

[`banquet.regin`](../showcase/banquet.regin)
```regia
KIND noble, PLAYS Guest:
    COUNT 6
    bravery AT RANDOM(0.2, 0.8)
    sympathy AT RANDOM(0, 0.8)
    aggressiveness AT RANDOM(-0.4, 0.4)
```

A Role setup is the same Statements for every Agent of the Role, and its Expressions are worked out for each Agent. Each Guest rolls its own purse, from 5 to 20 coins. In Instancing, each noble draws its own temperament.

- A setup's roll is made once per Agent, each time the setup runs for one. It follows the usual rule for a roll's kind: `RANDOM(5, 20)` is whole.
- A starting Propensity value is always a decimal, however its bounds are written. `sympathy AT RANDOM(0, 0.8)` is any sympathy from 0 to 0.8, and `aggressiveness AT RANDOM(-1, 1)` would be any aggressiveness from -1 to 1, not one of three.
- Its bounds are literals, within [0, 1] for a Trait and [-1, 1] for a Mood.
- Instancing draws values and never Roles. Every Agent of a kind plays every Role of the kind. Five Guests of whom two are drunk are two kinds; a random part of a Role is drawn by a Plot (above).

**Checks**

- `RANDOMLY`, `IF` or any Statement other than `ASSIGN`, `LEARN` or `PURSUE` in a setup → `R16_02-wrong-statement-in-setup`
- A Propensity's value or `RANDOM` bound that isn't a literal, or lies outside its range → `R21_07-wrong-propensity-value`

Spec: chapter 16. For Propensity values, chapter 21, *Agent kinds*; for Traits and Moods, chapter 14.

## The seed

```regia
# replay.regin
IMPORT "banquet.regin"

SEED 42
```

Every draw the language makes comes from one source, seeded once per run: rolls in a Body, a Context, a setup, a Weight, a `WAIT` or a count; Random choices; Picks that draw; counted parts of a Role; starting Propensity values. This `.regin` layers on the full banquet and changes only the seed.

Where the seed comes from, first that applies:

| Started as | The seed is |
|---|---|
| `regia run --seed <n>`, or a behaviour case with `#! seed: <n>` | `n` |
| a run or a case that gives none, in a Build with `SEED` | the Build's |
| a behaviour case with neither | 1 |
| a run with neither | one the run picks |

- `SEED` is a whole, non-negative literal. It is one item for overriding, so a `.regin` that imports another may set its own.
- The Trace's `run` entry records the seed, whichever way it came: `RUN STARTED <entry> SEED <n>`. A run that went interestingly is started again with that number.
- A behaviour case runs its Agents in lockstep with a fixed seed, so it draws the same way every time and its expected lines can rely on the draws.
- The seed covers what the language draws. A random source inside the Target that the language's choices rely on, and that the Target can't seed, is a gap in the Target.

**Checks**

- A `SEED` that isn't a whole, non-negative literal → `R21_08-wrong-count-or-seed`

Spec: chapter 21, *The seed*. For what the seed covers and behaviour cases, chapter 34; for `--seed`, chapter 23.

## How this combines with…

### Placeholders and Expressions

A roll and a Weight are Expressions, and follow their rules: a Weight's Placeholders must be certainly filled, and a roll used twice is named with `LET`. A Placeholder filled in every Option of a Random choice is certainly filled after it, as after an `IF` with an `ELSE`. (*Placeholders and Expressions*)

### Matching

`COUNT` and a weighted Pick meet in `NobleSocializing`. `WEIGHT ?grudges` in `WHEN idle` decides whether to vent, from a `COUNT` of the same condition `TO vent` matches, and `WEIGHT ?size` decides whom at. Because both count only grudges against peers at the table, `vent` is never pursued with nothing to match. (*Matching*)

### Goals and Failure

A Random choice never fails a Plan by itself. Every Weight at 0 runs nothing and goes on. A Weight that isn't a Number fails the Plan, as does a whole roll with nothing to give, and an Option that pursues a Goal fails the Plan if the Goal fails: `PURSUE vent` waits for `vent`. (*Goals and Failure*)

### Actions and time

`WAIT RANDOM(1, 3) SECONDS` is a fresh wait each time. In a behaviour case the clock is virtual and the seed fixed, so even a random wait wakes at the same moment every run. (*Actions and time*)

### Precedence and Labels

The Selection function, which picks among Suits alternatives by an Agent's Propensities, is not one of the language's draws. It is the Target's, and a run that uses it plays again only given the same Mood history. `TIES` between Plans with no `SUITS` falls back to name order, never to chance. Variety by temperament is a `SUITS` Label; variety by chance is `RANDOMLY`. (*Precedence and Labels*)

### Playbooks and Roles

A counted Mapping is drawn once and fixed: the Agents bound to the Role don't change while the Giving lasts. A counted recipient is drawn every time it sends. (*Playbooks and Roles*)

### Instancing

Starting Propensity values are the one draw Instancing makes, and the one place a roll is always a decimal. `SEED` sits in a `.regin` beside the cast it seeds. (*Instancing*)

### The Trace

The `run` entry holds the seed. Which Option ran isn't written as an entry of its own: the Trace shows it through what the Option did. Negative and all-zero Weights write entries, never warnings. (*The Trace*)

### Jason: Plans and Goals

A Random choice stays inside the Plan's body: one step, `!regia_choose`, rolls once with Jason's `.random` and hands back the chosen Option, then an `if`/`elif` chain runs it. `regia-jason` seeds each Agent's generator from the run's seed, so every draw can be repeated. (*Jason: Plans and Goals*)
