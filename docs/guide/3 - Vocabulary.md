Before a Guest can hold a grudge, somebody has to say that `grudge` exists, that it is something an Agent knows, and that it has two slots. That is a line of Vocabulary: `FACT hall.social.grudge AS grudge(person, size)`. The Vocabulary is every such line of a Program, the names that Plans are built from. This chapter goes through the kinds of item, what can be written in their slots, the names the game uses for them, and the items a Playbook keeps to itself.

It follows *Syntax*, which covers how the lines are laid out, and comes before *Plans*, where the names are put to use. Most snippets are cut from `showcase/vocabulary.regia`.

## The kinds of item

`showcase/vocabulary.regia`
```regia
TRAIT bravery
MOOD sympathy, aggressiveness

FACT purse(gold), craves(dish), on_duty

EVENT insulted, scandal(person)

GOAL vent, resent(person)

ACTION chat, sip_wine, sneer_at(person), scowl_at(person), laugh, snigger, roll_eyes
```

A declaration is a keyword and a name. The keyword gives the item its kind, and the kind decides where a Plan may write the name.

| Keyword | What it declares | Where a Plan writes it |
|---|---|---|
| `FACT` | something an Agent or a Director knows, until it is forgotten | conditions; `LEARN`, `FORGET`, `CHANGE`; the Triggers `… LEARNED` and `… FORGOTTEN` |
| `EVENT` | something that happens and is over once noticed | a `WHEN` Trigger; `TELL`, `SIGNAL`, `END PLOT WITH` |
| `GOAL` | an objective an Agent pursues until a Plan for it finishes | `PURSUE`, `DROP`, `ASK … TO`; a `TO` recipe; the Triggers `… DROPPED` and `… FAILED` |
| `ACTION` | a Custom Action, carried out by the game | after `DO` |
| `TRAIT`, `MOOD` | a Propensity of an Agent | Labels only |

A Fact stays, and an Event doesn't. `GIVEN on_duty:` is a fair question at any moment, while `GIVEN insulted:` is an error, because nothing of the insult is left to test. A Plan that wants to remember an Event records a Fact, as `TO resent` does with a `grudge`.

A name has one kind in the whole Program. `FACT hungry` and `GOAL hungry` can't both exist, in one file or in two files that never import each other, since both could end up on the same Agent.

`#revise` One name per kind gives families of near twins. The showcase has `wagered(stake)`, the Event a Spectator Signals, and `wager(person, stake)`, the Fact the Director keeps of it; `take_seat`, `took_seat` and `seat`; `poured` and `poison_poured`. Nothing in the source ties the members of a family together, and one letter tells them apart.

`#revise` Every `EVENT` looks the same. The showcase file sorts its Events under four comment banners: sent by the game, told between Agents, Signals to a Director, Outcomes of a Subplot. Take the banners away and `EVENT cheered` could be any of the four. The same goes for Facts: only the External name shows that `hungry` is kept by the game and `on_duty` by the Agents.

Spec: chapter 05. For the one set of names, chapter 10.

## Parameter names

`showcase/vocabulary.regia`
```regia
#@desc: The game seeds a few old grudges; Guests add their own.
FACT hall.social.grudge AS grudge(person, size)
```

The words in parentheses are Parameter names. They say that a `grudge` has two slots and what each is for. They bind nothing: a Plan writes `grudge(?foe, ?size)` or `grudge(?victim, ?)` as it likes. An item with no parentheses has no slots.

What the Transpiler checks is the count. Every use of `grudge` has two arguments, and a name has one count in the whole Program, so there is no `grudge(person)` next to this one. `bring` in the showcase is `bring(dish, place)` everywhere, even where a Plan doesn't care about the place and writes `bring(?dish, ?)`.

Slots have no types. `size` is meant to be a Number and `person` an Agent, and nothing stops a Plan from learning `grudge(3, roast)`. The mistake shows later, when some other Plan compares the roast with a number: in a condition the comparison is simply false, and in a Body the arithmetic fails the Plan.

`#revise` The showcase uses Parameter names as if they were types: `person` sixteen times, `dish` ten, `place` five. The convention does the work of the types the language doesn't have yet, and no tool holds anyone to it.

Spec: chapter 03. For a Number that isn't one, chapter 04.

## Values

A slot holds a Placeholder (`?foe`) or a Value. Placeholders have their own chapter. A Value is fixed when the Plan is written, and there are three sorts: a Name, a Number, a String.

`showcase/plots/royal_banquet.regia`
```regia
    ROLE Guest STARTS WITH:
        ASSIGN Courtesy, MAPPING Host TO host.
        LEARN purse(RANDOM(5, 20)).
        LEARN craves(roast).
        LEARN craves(pie).
        PURSUE take_seat.
```

`roast` and `pie` are Names: bare words that stand for themselves. They are not declared anywhere. The same holds for `door`, `kitchen` and `wall` in `DO walk_to(door)`, which mean something only because the game knows a place by each of those words.

`5` and `20` are Numbers. There is one kind of Number, whole or decimal, so `5 = 5.0` holds. A decimal has a digit before the point (`0.5`, never `.5`), and a `-` in front of a digit belongs to the number, as in `sympathy AT -0.4`. Exponents, digit separators and other bases don't exist.

A String is text in double quotes, `"Patrol started"`. It is a Value like the others, mostly seen in `PRINT`.

Two things are not Values. A Role name can't be written in a slot, so a Plan reaches the Host through a Placeholder filled by `FROM`, as in `WHEN greeting FROM ?who: DO bow_to(?who).` And a declaration holds Parameter names only: `FACT purse(20)` doesn't give anybody twenty coins. The starting value comes from the `LEARN` above.

`#revise` A Name is whatever word we type. `DO walk_to(kitchn)` is a correct Program that sends the Servant to a place the game has never heard of, and `craves(roast)` matches the kitchen's `roast` only if both sides spell it alike. Items are declared and checked; the Values that fill them are not.

Spec: chapter 03, chapter 04.

## Durations

`showcase/playbooks/duelling.regia`
```regia
    WHEN stamina(?) LEARNED:
        WAIT RANDOM(1, 3) SECONDS.
        DO lunge.
        TELL opponent hit.
```

A Duration is an Expression followed by a unit word: `SECONDS` or `MINUTES`, with `SECOND` and `MINUTE` accepted as well. `Dining` waits `1 MINUTE` for the Servants and the Director of `HonorDuel` gives a duel `2 MINUTES`. The unit is always written, there is nothing smaller than a second, and fractions cover the rest (`0.5 SECONDS`).

A Duration is written after `WAIT` and nowhere else. It is not a Value, so no slot holds one: a Guest's patience kept as a Fact is the Number in `patience(60)`, and the unit comes back when a Plan writes `WAIT ?p SECONDS.` Which clock counts the seconds, the wall's or the game's, is up to the Target. (*Plans*)

Spec: chapter 12.

## Multi-definition

`showcase/vocabulary.regia`
```regia
EVENT challenged, hit, yielded, duel_on
```

Several items of one kind can share a line, separated by commas. This is a Multi-definition, and it is shorthand for four lines. The items have nothing to do with each other afterwards. Each carries its own parameters, as in `EVENT served(dish), sold_out(dish)`.

Spec: chapter 03, chapter 05.

## External names

`showcase/vocabulary.regia`
```regia
#@desc: The seat the game has laid for this Agent. Servants and Guards have none.
FACT hall.seating.seat AS seat(place)

#@desc: Sent by the game to an Agent with nothing to do.
EVENT hall.clock.idle AS idle

ACTION hall.guards.seize AS seize(person)
```

The game has its own names for what it supplies and what it carries out, often dotted. `<the game's name> AS <our name>` gives an item its External name. Plans write `seat`, `idle` and `seize`, and only the Target ever sees `hall.seating.seat`.

- `FACT`, `EVENT` and `ACTION` can take an External name. `GOAL` can't, since no Goal comes from the game.
- The parameters are written once, after our name.
- A dotted name is only ever an External name. `ACTION hall.guards.seize` with no `AS` is an error.
- One External name has one name in Regia, in the whole Program.
- In a Multi-definition, `AS` belongs to the one item it follows: `FACT world.time.is_night AS night, hungry` gives `hungry` no External name.

An External name is needed only when the two names differ. `ACTION walk_to(place)` has none, and it is the game's all the same.

Spec: chapter 10.

## Propensities

`showcase/vocabulary.regia`
```regia
TRAIT bravery
MOOD sympathy, aggressiveness
```

A Propensity is a disposition of an Agent. A Trait stays as it is for the whole run, and a Mood moves as the Agent runs Plans. They take no parameters, and they are declared at the top level of a file, never inside a Playbook, because a Propensity belongs to the whole Agent.

The declaration gives a name and nothing else. Values, from -1 to 1, come from Instancing (`bravery AT 0.9.` for a `hothead`). Plans mention Propensities only in Labels: `SUITS bravery AT 0.7` picks the Plan that fits the Agent best, and `SHIFTS sympathy BY -0.3` moves a Mood, never a Trait.

Propensities are not Facts. No condition can test one, so there is no `GIVEN bravery > 0.5:`, and no Action sets one. The Transpiler warns about a Propensity that no Label names. (*Precedence and Labels*, *Instancing*)

Spec: chapter 14.

## Local Vocabulary

`showcase/playbooks/dining.regia`
```regia
PLAYBOOK Dining:
    ROLE waiter.

    FACT on_plate(dish)

    WHEN served(?dish) FROM waiter:
        LEARN on_plate(?dish).
```

A `FACT` or a `GOAL` declared inside a Playbook or a Plot is Local Vocabulary. `on_plate` exists for `Dining` alone. The line can stand anywhere in the Block and is seen in all of it. The showcase has four more: `stamina(points)` in `Duelling`, `poured` in `Scheming`, the Goal `fetch(dish, place)` in `Serving`, and `wager(person, stake)` in the Plot `HonorDuel`, which is the Director's.

- Nothing outside the Block sees a local item, not the rest of the file, and not another Playbook on the same Agent. A Guest's `NobleSocializing` can't test `on_plate`.
- The game never touches a local Fact. Only the Playbook's own `LEARN`, `FORGET` and `CHANGE` do, and a local item has no External name.
- A local item can't be sent. `TELL waiter on_plate(?dish)` is an error, since the receiver would have no name for it.
- A local name can't repeat a name the file can see. Two Playbooks may each have a local `poured`, and those are two different Facts.
- Events, Actions and Propensities can't be local.

`#revise` `challenged`, `hit` and `yielded` are used by `Duelling` and by nothing else, yet they sit in the shared file. An Event can't be local, and a local item couldn't be sent anyway, so the words two holders of one Playbook say to each other are everybody's.

Spec: chapter 10.

## One item, declared twice

The showcase declares every shared item once, in one file. That is a habit. A Program can do without the shared file, and let each Playbook declare what it uses:

```regia
# playbooks/dining.regia
EVENT served(dish)

# playbooks/serving.regia
EVENT served(plate)
```

These two lines declare the same Event. Declaring a name again is allowed when the kind, the number of parameters and the External name all agree. Parameter names may differ, since they only document. Any other difference is an error that points at both lines. A Playbook or a Plot can't be declared twice.

A few rules hold for every name we choose:

- Names are unique ignoring case. `Scandal` next to `scandal` is an error.
- A name can't start with `regia_` or contain `__`. Both are kept for the names the Transpiler makes up.
- Vocabulary items, Playbooks and Plots share one set of names, so a Fact can't be called `Dining`. Roles and Phases belong to their Plot.

Spec: chapter 10.

## How this combines with…

### Plans

The kind of a name is checked wherever a Plan writes it. `LEARN insulted` and `PURSUE hungry` are errors, and the message suggests the right Action. A Trigger on a Fact always says which change it means:

`showcase/playbooks/dining.regia`
```regia
    WHEN hungry LEARNED:
        PURSUE have_dinner, WITHOUT WAITING.

    WHEN hungry FORGOTTEN:
        DROP have_dinner.
```

A bare `WHEN hungry:` is an error, so a reader never has to look in the Vocabulary to know whether `hungry` is a Fact or an Event. (*Plans*, *Goals and Failure*)

### Custom Actions and the game

`showcase/vocabulary.regia`
```regia
#@desc: Refused once the kitchen has run out of the dish.
ACTION pick_up(dish)
#@desc: Accepted at once; done only when the poison has dissolved.
ACTION pour_poison
```

When an Action is done, and whether the game can refuse it, decides how a Plan should call it: `Scheming` writes `DO pour_poison, WITHOUT WAITING.` because of the second line. `#revise` That knowledge is in Doc comments, where we chose to write it. The declaration has no place for it, and neither the Transpiler nor the Visual Editor can use it. (*Plans*, *Goals and Failure*)

### Messages

The Vocabulary says what can be sent and never who sends it. `scandal(person)` is told by Guests to their peers, `took_seat` is Signalled to a Director, `duel_settled(winner)` is the Outcome a Subplot ends with, and all three are an `EVENT` line. A Fact can be told as well: the Director of `RoyalBanquet` writes `TELL ?winner on_duty.` to the Guest who won a duel. (*Messages*, *Subplots and Stagings*)

### Givings

Local Facts outlive the Giving of their Playbook. When `Duelling` is taken away after a duel, the loser's `stamina` stays where no Plan can see it, and it is there again in the next duel. That is why `TO fight` starts by forgetting every `stamina` it finds. Local Goals being pursued are dropped with the Playbook. (*Playbooks and Roles*, *Matching*)

### Stagings

`wager(person, stake)` is local to the Plot `HonorDuel`, so it is a Fact of its Director. Two duels running at once are two Stagings with a Director each, and the wagers of one are not counted in the other. (*Subplots and Stagings*)

## Since 1.0

1.0 had Facts, Events and Actions, declared at the top of the file before anything else. Facts and Actions took parameters, Events took none, and Actions could have an alias with `AS`.

`#changes` `GOAL`, `TRAIT` and `MOOD` are new kinds.

`#changes` Every item with slots declares them the same way, Events included, and a slot can hold a Placeholder.

`#changes` Multi-definition is new. The `GROUP` the primer thought of was not taken up.

`#changes` `AS` now works on Facts and Events too, and the name before it is called the External name.

`#changes` Facts and Goals can be declared inside a Playbook or a Plot, and one item can be declared in several files.
