# Vocabulary and files

A Guest holds a grudge. Before any Plan can say so, the Program has to know that `grudge` exists, that it is something an Agent knows rather than something it does, and that it has two slots. That is one line of Vocabulary, `FACT grudge(person, size)`. The Vocabulary is every such line: the names Plans are built from. This chapter covers what those lines declare, what can fill their slots, where the names come from (the game, the Program or one Playbook), and how files reach each other's names.

| We write | It declares |
|---|---|
| `FACT`, `CUE`, `GOAL`, `ACTION` | an item of that kind |
| `TRAIT`, `MOOD` | a Propensity |
| `GAME FACT`, `GAME CUE` | an item the game produces |
| `<external> AS <name>` | the name the game or the Target uses for it |
| `NAME` | Names, the words a Plan may write as Values |
| `IMPORT "<path>"` | nothing: it makes another file's names visible |

How the lines are laid out is in *Syntax*. How Plans use the names is in *Plans* and the chapters after it.

## The kinds of item

[`vocabulary.regia`](../showcase/vocabulary.regia)
```regia
TRAIT bravery
MOOD sympathy, aggressiveness
```

```regia
FACT grudge(person, size)
FACT purse(gold), craves(dish), on_duty
```

```regia
CUE insulted, scandal(person)
```

```regia
GOAL vent, resent(person)
```

```regia
ACTION chat, sip_wine, sneer_at(person), scowl_at(person), laugh, snigger, roll_eyes
```

A declaration is a kind word followed by a name. The kind decides where a Plan may write the name:

| Kind | It is | A Plan writes it |
|---|---|---|
| `FACT` | something an Agent or a Director knows, until it is forgotten | in a Context; in `LEARN`, `FORGET`, `UPDATE`, `TELL`; in a Trigger with `LEARNED` or `FORGOTTEN` |
| `CUE` | something that happens and is over once noticed | in a `WHEN` Trigger, or after `FAILED WITH` and `FINISHED WITH`; in `TELL`, `SIGNAL`, `END PLOT WITH`, `FAIL WITH` |
| `GOAL` | an objective an Agent pursues | after `TO`; in `PURSUE`, `DROP`, `ASK … TO`, `PURSUING`; in a Trigger with `REACHED`, `FAILED`, `DROPPED` or `ENDED` |
| `ACTION` | a Custom Action, carried out outside the Program | after `DO` |
| `TRAIT`, `MOOD` | a Propensity of the Agent | in Labels (`SUITS`, `SHIFTS`) and, for a Mood, in `SHIFT` |

A Fact lasts and a Cue doesn't. `GIVEN on_duty` is a fair question at any moment, but nothing of an `insulted` is left to test once its Plans have started. A Plan that needs to remember a Cue records a Fact, as `TO resent` does with a `grudge`.

- A name has one kind in the whole Program. A Goal and the Fact that says it is done get two names: `take_seat` and `seat`, `have_dinner` and `sated`.
- Several items of one kind can share a line, separated by `,`. This is a Multi-definition. It is shorthand for one line per item, and the items have nothing to do with each other afterwards. Each carries its own parameters, as in `CUE served(dish), sold_out(dish)`.
- A Trait never changes during a run, and a Mood changes as the Agent runs Plans. Starting values come from Instancing: a Trait lies in [0, 1], a Mood in [-1, 1], and a Propensity an Agent is given no value for is neutral (0.5 for a Trait, 0 for a Mood).
- Propensities take no parameters, and they are not Facts: no Context can test one.
- Propensities and Actions are declared at the top level of a file only. A Propensity belongs to the whole Agent, and an Action is the Program's interface to what lies outside it, never one Playbook's.

The kind is the only thing a Cue's declaration says about it. The showcase sorts its Cues under comment banners (what Agents tell each other, Signals to the Directors, Outcomes of the Subplots, Reasons), but the banners are for the reader. Which job a Cue does is worked out from the Plans that send it (*Interfaces*).

**Checks**

- One name declared as two kinds → `R05_01-declared-as-two-kinds`
- `TRAIT` or `MOOD` declared inside a `PLAYBOOK` or `PLOT` → `R14_07-local-propensity`
- `ACTION` declared inside a `PLAYBOOK` or `PLOT` → `R10_12-misplaced-action-or-cue`
- A declared Propensity that no Label and no `SHIFT` names → `R14_09-unused-propensity` (warning)

Spec: chapter 05, *One name, one kind*; chapter 14, *Propensities*; chapter 10.

## Parameters

[`vocabulary.regia`](../showcase/vocabulary.regia)
```regia
#@desc: Seeded by Instancing. Guests add their own and make them bigger as the evening goes on.
FACT grudge(person, size)
```

The words in parentheses are Parameter names. They say that a grudge has two slots and what each slot is for, and the Visual Editor can show them as `grudge(person: …, size: …)`. They bind nothing: a Plan writes `grudge(?foe, ?size)`, `grudge(?mark, ?size)` or `grudge(?, ?)` as it likes. An item with no parentheses has no slots.

- What the Transpiler checks is the count. Every use of `grudge` has two arguments, and a name has one count in the whole Program, so there can't be a `grudge(person)` beside this one.
- Slots have no types. `person` is meant to hold an Agent and `size` a Number, and nothing stops a Plan from learning `grudge(roast, 3)`. The mistake shows later, at runtime: *Messages* follows a grudge against `roast` to the `TELL` it fails.
- A declaration holds Parameter names only. `?` in a declaration is an error, and `FACT purse(20)` doesn't give anyone twenty coins: a starting value comes from a `LEARN`.

**Checks**

- A use with more or fewer arguments than the declaration has parameters → `R03_01-wrong-argument-count`
- `?` in a declaration → `R03_02-placeholder-in-declaration`
- Two declarations of one name with different parameter counts → `R10_05-conflicting-redeclaration`

Spec: chapter 03, *Declaring parameters*.

## What the game produces: `GAME`

[`vocabulary.regia`](../showcase/vocabulary.regia)
```regia
#@desc: The seat the game has laid for this Agent. Servants and Guards have none.
GAME FACT hall.seating.seat AS seat(place)
#@desc: Kept up to date by the game: learned as the evening goes on, forgotten after enough food.
GAME FACT hall.needs.hungry AS hungry
#@desc: What the kitchen still has. The game forgets a dish when the last one is taken.
GAME FACT in_stock(dish)

#@desc: Sent by the game to an Agent with nothing to do.
GAME CUE hall.clock.idle AS idle
```

A `FACT` or `CUE` with `GAME` in front is a game item: the game produces it. Every other Fact and Cue is produced by the Program alone, through `LEARN`, `UPDATE`, `TELL`, `SIGNAL`, `END PLOT WITH` and `FAIL WITH`. The game tells a Guest it is `hungry` and forgets it again after dinner; it sends `idle` to an Agent with nothing to do; it keeps `in_stock` up to date as the kitchen empties.

`GAME` says where an item comes from and nothing else. Plans test it, react to it and tell it like any other item:

[`playbooks/serving.regia`](../showcase/playbooks/serving.regia)
```regia
TO fetch(?dish):
    DO walk_to(kitchen)
    IF NOT in_stock(?dish):
        FAIL WITH sold_out(?dish)
    DO pick_up(?dish)                    # still refused if the last one went while we walked
```

- Only a game item comes from the game. A game message for a Fact or Cue not declared `GAME` is dropped by the Target, with a Trace warning.
- `GAME` goes on `FACT` and `CUE` only. A Goal never comes from the game, and an Action is told apart by its External name instead (next section).
- In a Multi-definition, `GAME` covers every item of the line, like the kind word.
- A game Fact is the game's to keep. A Plan may `LEARN`, `FORGET` or `UPDATE` one, but the game may undo it at its next report, so the Transpiler warns. To remember what the game said, a Plan records a Fact of its own: `Dining` doesn't forget `hungry` after dinner, it learns `sated`.
- A Cue that isn't `GAME` must be sent by something in the Program. If nothing sends it, a Plan waiting for it can never run. Had `idle` been declared without `GAME`, every `WHEN idle:` in the showcase would be warned, with the hint to declare it `GAME CUE`.

**Checks**

- `GAME` on anything but a `FACT` or a `CUE` (`GAME TRAIT`, `GAME GOAL`, …), or on a local declaration → `R10_16-game-on-wrong-declaration`; on a `NAME` line it is `R03_11-misused-name-declaration`
- `LEARN`, `FORGET` or `UPDATE` on a game Fact → `R08_07-edit-of-game-fact` (warning)
- A Trigger waiting for a Cue that isn't `GAME` and that nothing in the Program sends → `R38_07-cue-never-sent` (warning; hint: `GAME CUE`)
- A game message for an item that isn't `GAME`, or that the receiver never uses → Trace warning (Jason: `T28_01-unknown-game-name`)

Spec: chapter 10, *What the game produces*. For `R08_07-edit-of-game-fact`, chapter 08; for `R38_07-cue-never-sent`, chapter 38.

## External names

[`vocabulary.regia`](../showcase/vocabulary.regia)
```regia
#@desc: Sent by the game to an Agent close enough to see a cup being tampered with.
GAME CUE hall.senses.saw_pouring AS saw_pouring(person)
```

```regia
#@desc: The Target's own code, not the game's: done when that code returns.
ACTION hall.music.fanfare AS play_fanfare
```

The game has names of its own, often dotted. `<external> AS <name>` gives a game item or an Action its External name. Plans always write the name after `AS`, so `Keeping_watch` reacts to `saw_pouring(?who)` and `Hosting` does `play_fanfare`. Only the Target ever sees `hall.senses.saw_pouring`. Without `AS`, the External name is the Regia name as written: `in_stock` and `walk_to` are the game's names as they stand.

For a game item, the External name is the game's name for it. The Target turns it into the Regia name as the game's message comes in, so nothing after that point holds the game's spelling.

For an Action, the External name also says who carries it out:

| The External name | Who runs the Action | In the showcase |
|---|---|---|
| has no dot | the game, asked by the Target under that name | `walk_to`, `seize`, `discard_cup` |
| has a dot | the Target's own code (a Java internal action in Jason) | `hall.music.fanfare AS play_fanfare` |

[`playbooks/hosting.regia`](../showcase/playbooks/hosting.regia)
```regia
TO open_feast, FROM DIRECTOR:
    DO stand_up
    DO play_fanfare                      # the Target's own code: Regia doesn't wait on the game
    DO raise_cup
```

A dotted Action is done when the code returns and fails if the code fails. The game never hears of it, so the game can't name an Action with a dot.

- An External name has no meaning in Regia. It may contain dots and any other character the game uses.
- A dotted name is only ever an External name. `ACTION hall.music.fanfare` without `AS` is an error, since every Plan would have to write the dots out.
- `AS` goes on game items, Actions and Propensities. A Fact or Cue that isn't `GAME` has no game name, a Goal never leaves the Program, and a local item is never seen outside it.
- The parameters are written once, after the Regia name.
- In a Multi-definition, `AS` belongs to the one item it follows: `GAME FACT world.time.is_night AS night, hungry` gives `hungry` no External name.
- One External name has one Regia name in the whole Program.

**Checks**

- A dotted name without `AS` → `R10_09-dotted-name-without-as`
- `AS` on a `GOAL`, on a local declaration, or on a `FACT` or `CUE` that isn't `GAME` → `R10_10-as-on-wrong-declaration`
- One External name given two Regia names → `R10_11-shared-external-name`
- Two declarations of one name with different External names → `R10_05-conflicting-redeclaration`

Spec: chapter 10, *External names*. For what a dotted Action does when it runs, chapter 08.

## Values

[`plots/royal_banquet.regia`](../showcase/plots/royal_banquet.regia)
```regia
#@desc: Everyone invited to the table. A knight is a Guest and a Guard at once.
ROLE Guest:
    LEARN purse(RANDOM(5, 20))           # rolled for each Guest
    LEARN craves(roast)
    LEARN craves(pie)
    PURSUE take_seat
```

[`vocabulary.regia`](../showcase/vocabulary.regia)
```regia
NAME wall, door, kitchen
NAME roast, pie, bread
```

A slot holds either a Placeholder (`?dish`, in *Placeholders and Expressions*) or a Value. A Value is fixed when the Plan is written:

| Value | Example | Declared |
|---|---|---|
| a Name | `roast`, `kitchen` | with `NAME` |
| a Number | `5`, `-0.4` | no |
| a String | `"The feast is over, and the poisoner was never found."` | no |
| `ME` | `scandal(ME)` | reserved: the Agent running the Plan |

`roast` and `kitchen` are Names. Every Name written in the source is declared with `NAME`, so `DO walk_to(kitchn)` is an error whose hint is the closest declared Name, `kitchen`. A `NAME` line declares Names and nothing else: no parameters, no `AS`, no `GAME`, and only at the top level of a file. Names are declared, but they are Values, not Vocabulary.

- Only the source is checked. A Name that arrives at runtime, from the game or in a Message, isn't checked against the declarations. The game lays a `seat(seat_3)` that no Plan ever writes, so `seat_3` needs no declaration.
- A declared Name can go in any slot. Which Names suit which slot would be a matter for types, which 1.5 doesn't have.
- Names share the namespace of items (*One namespace*, below): `NAME roast` and `FACT roast` can't both exist.
- A Plan never names an Agent. It reaches one through a Placeholder (*Messages*). Instancing names individual Agents, and its setup lines may write those names (`LEARN grudge(percival, 2)`) with no `NAME` declaration, but a `.regia` file can't: the story doesn't depend on the cast. A Plan meets `percival` at runtime, as a Name arriving in a Fact.
- A Role name is not a Value either. `toast(Host)` is an error; a Plan that needs the Host fills a Placeholder with `FROM Host ?h` and writes `?h`.
- `ME` is the Agent running the Plan, filled in where it is written. It is an error anywhere in a Plot, since a Director is not an Agent. It is never a recipient (*Messages*).

What Numbers can do, and Strings, is in *Placeholders and Expressions*.

**Checks**

- A Name not declared with `NAME` → `R03_10-undeclared-name` (hint: the closest declared Name)
- A `NAME` line with parameters, `AS` or `GAME`, or inside a `PLAYBOOK` or `PLOT` → `R03_11-misused-name-declaration`
- A Role name used as a Value → `R03_03-role-as-value` (hint: `FROM Role ?x`)
- `ME` in a Plot, a Role setup included → `R03_09-me-in-plot`

Spec: chapter 03, *Values and Placeholders*, *Names are declared*, *`ME`*. For Numbers and Strings, chapter 04.

## Durations

[`playbooks/duelling.regia`](../showcase/playbooks/duelling.regia)
```regia
WAIT RANDOM(1, 3) SECONDS
```

[`playbooks/dining.regia`](../showcase/playbooks/dining.regia)
```regia
WAIT 1 MINUTE, UNTIL on_plate(?)
```

[`plots/honor_duel.regia`](../showcase/plots/honor_duel.regia)
```regia
AFTER 20 SECONDS:                    # betting closes
```

A Duration is an Expression followed by a unit word, `SECONDS` or `MINUTES`. `SECOND` and `MINUTE` are accepted too, and singular and plural are interchangeable: `1 SECONDS` and `2 MINUTE` are both fine.

- The unit is always written. `WAIT 3` is an error.
- There are no shorthands like `3s` and no unit smaller than a second. Fractions cover the rest: `0.5 SECONDS`.
- The unit comes after the whole Expression: `WAIT ?delay * 2 SECONDS` waits `?delay * 2` seconds. Placeholders in it must be certainly filled before the `WAIT`.
- A Duration is written after `WAIT` and `AFTER`, and nowhere else. It is not a Value, so no slot holds one. A Guest's patience kept as a Fact is the Number in `patience(60)`, and the unit comes back when a Plan writes `WAIT ?p SECONDS`.
- The Duration says how long. The Target owns the clock that measures it, one clock for the whole run, stopped while the game is paused.

What waiting does, and what a Duration that isn't a Number does, are in *Actions and time*.

**Checks**

- A Duration without a unit word, or with another word → `R12_01-wrong-duration-unit`
- A Duration whose Placeholders aren't certainly filled before the `WAIT` → `R12_02-maybe-unfilled-duration`
- A negative Number written directly as the Duration (`WAIT -2 SECONDS`) → `R12_03-negative-duration` (warning)

Spec: chapter 12, *Durations*.

## Imports and the Program

[`plots/honor_duel.regia`](../showcase/plots/honor_duel.regia)
```regia
IMPORT "../vocabulary"
IMPORT "../playbooks/duelling"
IMPORT "../playbooks/wagering"
```

[`banquet.regin`](../showcase/banquet.regin)
```regia
# The full banquet. The test casts the walkthrough follows import this file.
IMPORT "plots/royal_banquet"
```

`IMPORT "<path>"` makes another file's declarations visible. Imports come first in a file, after its Doc comment and before any declaration.

- The path is a string, relative to the importing file. The `.regia` extension may be left out. There are no project roots, search paths or packages.
- Imports are transitive. A file sees what it declares, what it imports, and what those files import, all the way down. `banquet.regin` imports one file and reaches all thirteen through it.
- A file is loaded once, however many paths lead to it. `honor_duel.regia` reaches `vocabulary.regia` directly and again through `Duelling`, which is fine.
- An import cycle is an error that names every file in the loop.
- There is no export control. Everything at a file's top level is visible to every file that reaches it. The only private names are Local Vocabulary.

A Program starts from one Entry file and is every file reachable from it through imports. Visibility is per file: a file uses only the names it declares or reaches. Uniqueness is Program-wide: two files that never import each other, both reached from the Entry, still can't give one name two meanings, since their Playbooks may end up on one Agent.

- Any Entry can be checked and built. A `.regia` Entry has no Root Plot, so its Build is Target code only. Only a `.regin` Entry can be run.
- A `.regin` imports `.regia` files and other `.regin` files. A `.regia` file can't import a `.regin`: design files never depend on a build (*Instancing*).
- Builds are layered by importing, never by naming several Entry files. `regia check a.regin b.regin` checks two Programs, one after the other.

### A name that came through another file

Because imports are transitive, a file can use a name that reaches it only through another file. `honor_duel.regia` doesn't need its own `IMPORT "../vocabulary"`, since `Duelling` and `Wagering` both import `vocabulary.regia`. Suppose it left that line out, and both Playbook files were later changed to declare what they use themselves, dropping their import. The errors show up in `honor_duel.regia`, a file nobody edited, so the Transpiler says where each name used to come from:

```
error: `scandal` is not declared
  --> plots/honor_duel.regia:20
  hint: `scandal` is declared in `vocabulary.regia`, which this file no longer reaches.
        Add `IMPORT "../vocabulary"`.
```

The hint is there only while the declaring file is still in the Program, here through `royal_banquet.regia`. A file that imports what it uses directly, as `honor_duel.regia` does, is safe from such edits.

**Checks**

- An `IMPORT` that isn't at the top of the file → `R10_01-misplaced-import`
- An import path that leads to no file → `R10_02-missing-import-file`
- An import cycle → `R10_03-import-cycle` (the message names every file in the loop)
- A name the file neither declares nor reaches → `R10_04-name-out-of-scope` (hint: the file that declares it, and the `IMPORT`)
- A `.regia` file importing a `.regin` → `R21_01-import-of-instancing-file`

Spec: chapter 10, *Imports*, *The program*. For `.regin` files, chapter 21.

## One namespace

[`playbooks/serving.regia`](../showcase/playbooks/serving.regia)
```regia
IMPORT "../vocabulary"

#@desc: A Servant's work: fetching what the patrons ask for.
PLAYBOOK Serving:
```

Vocabulary items, Names, Playbooks and Plots share one flat namespace across the Program. A name is never qualified by its file (`vocabulary.served` means nothing), and a Fact can't be called `Serving`. Roles and Phases are not in it: they belong to their Plot, so two Plots may each have a `Host`. Nor are the kinds and Agents of Instancing, which share a namespace of their own (*Instancing*).

The showcase declares every shared item once, in `vocabulary.regia`, but nothing requires it. A Playbook file may declare what it uses, and a declaration that matches another declares the same item:

```regia
CUE served(plate)                        # in serving.regia: the same Cue as vocabulary.regia's served(dish)
```

- Two declarations of one name are one item when they agree on the kind, the parameter count, `GAME`, and the External name (or both have none). Parameter names may differ, since they only document. Any other difference is an error that names both declarations.
- A Playbook or a Plot can't be declared twice. Each has a body, so two of them are never the same.
- After the imports, declarations come in any order, and a name can be used above its declaration.

**Checks**

- Two declarations of one name that disagree on parameter count, `GAME` or External name → `R10_05-conflicting-redeclaration` (the message names both); on kind → `R05_01-declared-as-two-kinds`
- A Playbook or Plot declared twice → `R10_06-duplicate-playbook-or-plot`

Spec: chapter 10, *One namespace*, *Declaration order*.

## Name rules

```regia
FACT Grudge(person, size)                # error: `grudge` is already declared
GOAL regia_vent                          # error: `regia_` is kept for the Transpiler
FACT on__duty                            # error: so is `__`
```

- Names are unique ignoring case. `Grudge` and `grudge` can't both be declared, nor two Roles or two Phases of one Plot, nor two Placeholders of one Plan (`?who` and `?Who`). Targets that change case, and file systems that ignore it, would merge them. For the same reason a Plot's Role fills a Playbook's Role ignoring case: `Host` fills `host` (*Playbooks and Roles*).
- A name can't start with `regia_`, in any case, and can't contain `__`. Both are kept for the names the Transpiler makes up, so they never collide with ours. Placeholders are held to this too: `?regia_w` and `?a__b` are errors.
- External names are exempt. They are the game's names, not Regia's.
- A name spelled exactly like a keyword is an error (*Syntax*).

**Checks**

- Two names that differ only in case, in the namespace, among one Plot's Roles or Phases, or among one Plan's Placeholders → `R10_07-case-only-name-clash`
- A name, a Placeholder's included, that starts with `regia_` or contains `__` → `R10_08-reserved-name-spelling`
- A name spelled exactly like a keyword → `R01_10-keyword-as-name`

Spec: chapter 10, *Name rules*.

## Local Vocabulary

[`playbooks/dining.regia`](../showcase/playbooks/dining.regia)
```regia
PLAYBOOK Dining:
    ROLE waiter

    FACT on_plate(dish), sated
    GOAL make_do
```

[`plots/royal_banquet.regia`](../showcase/plots/royal_banquet.regia)
```regia
FACT seated(person), finished(person)
```

A declaration inside a Playbook or a Plot is Local Vocabulary. `on_plate`, `sated` and `make_do` exist for `Dining` alone. `seated` and `finished` are the Director's own, kept by `RoyalBanquet` to count the Guests by hand.

| Inside | May declare |
|---|---|
| a `PLAYBOOK` | `FACT`, `GOAL`, `CUE` |
| a `PLOT` | `FACT` |

A Plot has no local Goals, since its Director never pursues one or writes a recipe, and no local Cues, since a Cue a Plot hears is named by the Playbook or the Subplot that sends it.

- A local declaration goes anywhere in its Block and is visible everywhere inside it, every `DURING` of a Plot included. It is never visible outside: not in the rest of the file, and not through an import.
- A local Fact or Goal is private even on one Agent. A Guest holds `NobleSocializing` next to `Dining`, and none of its `NobleSocializing` Plans can test `on_plate`.
- Only the Playbook's own `LEARN`, `FORGET` and `UPDATE` touch a local Fact. The game never does, so a local item is never `GAME` and has no External name.
- A local Fact or Goal can't be sent. `TELL waiter on_plate(?dish)` is an error, since the receiver has no name for it.
- No shadowing: a local name that matches any name the file can see is an error. Two Playbooks may each declare the same local name, and those are two different items.
- When a Playbook is taken away, its local Facts stay, out of sight of every Plan, and are there again if it is given back. Local Goals being pursued are dropped. A Playbook that wants its Facts gone forgets them in `WHEN REMOVED:` (*Playbooks and Roles*).

**Checks**

- `ACTION` inside a `PLAYBOOK` or `PLOT`, `CUE` inside a `PLOT` → `R10_12-misplaced-action-or-cue`
- `GOAL` inside a `PLOT` → `R10_15-goal-in-plot` (hint: declare it at file level to `ASK` for it)
- A local name that shadows a name the file can see → `R10_13-shadowing-local-name`
- A local Fact or Goal sent with `TELL`, `ASK … TO` or `SIGNAL` → `R10_14-local-vocabulary-sent`
- `AS` on a local declaration → `R10_10-as-on-wrong-declaration`; `GAME` on one → `R10_16-game-on-wrong-declaration`

Spec: chapter 10, *Local Vocabulary*.

### Local Cues

[`playbooks/duelling.regia`](../showcase/playbooks/duelling.regia)
```regia
PLAYBOOK Duelling:
    ROLE opponent

    FACT stamina(points)
    GOAL strike
    CUE challenged, hit, yielded             # what two duellists say to each other

    TO issue_challenge, FROM DIRECTOR:
        DO throw_glove
        TELL opponent challenged
```

A Cue that one Playbook both sends and reacts to may be declared inside it. `challenged`, `hit` and `yielded` are what two holders of `Duelling` say to each other, and no other Playbook or Plot can name them. `greeting` in `Courtesy` is another.

- A local Cue is sent with `TELL`, to any recipient `TELL` accepts. A receiver holding the Playbook reacts with its Plans; any other receiver has no Plan for it, and nothing happens (*Messages*).
- It can't be Signalled and can't be an Outcome: a Director is outside the Playbook and couldn't name it. To a Plot, a local Cue isn't declared at all.
- It can be a Reason (`FAIL WITH`). Only Plans of the same Playbook can match it with `FAILED WITH`; anyone else sees a plain `FAILED`.
- The other rules of local items hold: no External name, no shadowing, no importing, and the same local name in two Playbooks is two Cues.

**Checks**

- A local Cue sent with `SIGNAL` → `R10_14-local-vocabulary-sent`
- A local Cue as an Outcome (`END PLOT WITH`, `FINISHED WITH`) → `R10_04-name-out-of-scope`: the Plot can't see it

Spec: chapter 10, *Local Cues*.

## How this combines with…

### Plans

The kind of a name decides how a Trigger is written. A Fact Trigger always says `LEARNED` or `FORGOTTEN`, so `WHEN hungry LEARNED:` and `WHEN idle:` tell a reader, without looking anything up, that `hungry` is a Fact and `idle` a Cue. A kind word that doesn't suit the item is an error. (*Plans*)

### Messages

The Vocabulary says what a Message carries, so the Statement doesn't: `TELL ?winner on_duty` tells a Fact and `TELL host greeting` a Cue only because of their declarations. A game Cue can be told like any other, and arrives as the same Cue. (*Messages*)

### Actions and time

An Action's declaration says nothing of what it does. Its Doc comment does, and the showcase writes one for each Action with something to say: when it is done (`walk_to`, when the Agent has arrived), when it is refused (`pick_up`, once the kitchen has run out), and what calling it off means (`eat`). (*Actions and time*)

### Playbooks and Roles

Roles and Phases are the two kinds of name outside the one namespace. A Playbook's Role is a local name the Plot fills through a Mapping, or by the same name ignoring case, so `Courtesy`'s `host` is `RoyalBanquet`'s `Host` with no Mapping written. (*Playbooks and Roles*)

### Precedence and Labels

`TRAIT` and `MOOD` declare the Propensities that `SUITS` and `SHIFTS` name. The declaration is all the Program says about them; their values live in the Agent, not in its Facts. (*Precedence and Labels*)

### Instancing

[`banquet.regin`](../showcase/banquet.regin)
```regia
KIND noble, PLAYS Guest:
    COUNT 6
    bravery AT RANDOM(0.2, 0.8)
    sympathy AT RANDOM(0, 0.8)
    aggressiveness AT RANDOM(-0.4, 0.4)
```

A `.regin` file declares no Vocabulary. It imports the `.regia` files and uses their names: the Propensities a kind starts with, and the Facts its setup lines learn. (*Instancing*)

### Interfaces

The Transpiler sorts the Cues by who sends them, using `GAME` for the ones the game sends and the Program's `TELL`, `SIGNAL`, `END PLOT WITH` and `FAIL WITH` lines for the rest. A Cue may land in several groups, as `sold_out` is both a Reason and a told Cue. (*Interfaces*)

### Jason: the Build

None of the External names reaches the ASL: beliefs and events use Regia names, and the Target translates the game's names as messages arrive. Local items get Generated names of the form `regia_local__<Playbook or Plot>__<name>`, which is why `regia_` and `__` are kept out of ours. (*Jason: the Build*)
