A Guest with nothing to do gets `idle` from the game, again and again through the evening. If the Plan for it were fixed, ten Guests would chat at the same moments, and each would do the same thing all night. Regia has five places where we can ask for chance instead: a Random choice among written Options, a roll inside an Expression, a Pick `AT RANDOM` among Matches, a random part of a Role in a Mapping, and a random starting value in Instancing. A run can also be given a seed, so that all of this comes out the same way twice.

Rolls are introduced in *Placeholders and Expressions* and Picks in *Matching*; this chapter looks at both again from the side of chance. Starting values belong to *Instancing*, and the seed to *The Transpiler*.

## One of several Options

`showcase/playbooks/noble_socializing.regia`
```regia
# Small talk. The more grudges we hold, the likelier we are to vent one.
WHEN idle:
    ?grudges = COUNT(grudge(?, ?)).
    EITHER, WEIGHT 3: DO chat.
    OR: DO sip_wine.
    OR, WEIGHT ?grudges: PURSUE vent.
```

A Random choice is one Statement of a Body, made of an `EITHER` Block and one or more `OR` Blocks at the same indentation. Each Block is an Option. When the Body reaches the `EITHER`, exactly one Option runs, and the Body then carries on after the last `OR`. Leaving the Weights for the next section, this Guest chats, sips wine or vents a grudge.

An Option is an ordinary Block. The three above are Inline blocks of one Statement each, but an Option can be indented under its header and hold anything a Body can, another Random choice included:

```regia
WHEN idle:
    EITHER: DO chat.
    OR:
        DO sip_wine.
        IF hungry:
            DO complain.
```

- An `EITHER` with no `OR` is an error, since there is nothing to choose between.
- An Option has no condition of its own. To make one depend on a Fact we write an `IF` inside it, as above. The Option still takes its share of the choice, and does nothing when the `IF` doesn't hold.
- A Placeholder filled inside an Option, by a naming or by an `IF`, stays inside that Option. Sibling Options may use the same name, since only one of them runs. (*Placeholders and Expressions* has the example and a `#revise` on this rule.)
- A Random choice can go wherever a Statement can, a Director's Body included.

`#revise` `OR` is two things. Between conditions it is the operator of `GIVEN a OR b:`, and at the start of a line it opens an Option. The colon tells them apart for the Transpiler. A reader meets `OR:` three lines below an `EITHER`, possibly after a long indented Option, and has to look up to find what it belongs to.

Spec: chapter 09.

## Weights

A Weight is the clause `, WEIGHT <Expression>` on an Option's header. An Option without one has Weight 1. The chance of an Option is its Weight divided by the sum of all the Weights, so for the `idle` Plan above:

| Grudges held | `DO chat` | `DO sip_wine` | `PURSUE vent` |
|---|---|---|---|
| 0 | 3 in 4 | 1 in 4 | never |
| 2 | 3 in 6 | 1 in 6 | 2 in 6 |
| 4 | 3 in 8 | 1 in 8 | 4 in 8 |

Weights are relative. There are no percentages to keep adding up to 100, so a fourth Option can be added without touching the other three. The price is that no Weight can be read alone: `WEIGHT 3` says nothing until we have summed the others, and here one of the others is only known at runtime.

A Weight is any Expression: a Number, a filled Placeholder, arithmetic, a `COUNT`, even a roll. Its Placeholders have to be filled before the `EITHER`, which is why `?grudges` is named one line above. All the Weights are worked out together, once, when the Body reaches the `EITHER`. Nothing an Option does can change the choice that put it there.

| The Weight is | What happens |
|---|---|
| 0 | the Option is never chosen |
| negative | it counts as 0, and a warning is written to the Trace |
| not a Number | the Plan fails |
| 0 or negative on every Option | no Option runs, a warning is written, and the Body carries on |

The Weight of 0 is doing real work in the showcase. `TO vent` has a `GIVEN` and no `ELSE`, so pursued by a Guest with no grudge it would fail, and the `idle` Plan with it. `WEIGHT ?grudges` makes sure it is never pursued then.

`#revise` "Only sometimes" has no good spelling as a Random choice. A Guest who complains three times in ten and otherwise does nothing needs a second Option that is empty, and an empty Block gets a warning. So we write `IF RANDOM(1, 100) <= 30:` instead, which counts in hundredths, while Weights count in shares. The two ways of stating a chance don't look related.

`#revise` A wrong Weight is treated in three ways. A negative one is repaired with a warning, a set of Weights that are all 0 skips the whole choice with a warning, and one that isn't a Number fails the Plan. If `?grudges` were ever negative, the Guest would simply never vent, and we would learn it only from the Trace.

Spec: chapter 09. For the Trace, chapter 34.

## Rolls

`showcase/playbooks/wagering.regia`
```regia
WHEN duel_on FROM DIRECTOR:
    GIVEN purse(?gold) AND ?gold > 0:
        ?stake = RANDOM(1, ?gold).
        CHANGE purse(?gold) TO purse(?gold - ?stake).
        SIGNAL wagered(?stake).
```

`RANDOM(a, b)` is an Expression: a random Number from `a` to `b`, both included. With whole bounds it is a whole number, so a Spectator with 12 coins stakes anything from 1 to 12. If either bound is a decimal, the roll is a decimal too.

Every `RANDOM(…)` is a fresh roll. The Spectator names the stake because it is used twice. Written out twice, the gold taken from the purse and the stake announced to the Director would be two different numbers.

A roll goes wherever an Expression does. The showcase has one in a Duration:

`showcase/playbooks/duelling.regia`
```regia
WHEN stamina(?) LEARNED:
    WAIT RANDOM(1, 3) SECONDS.
    DO lunge.
    TELL opponent hit.
```

Both duellists hold this Plan and start with the same stamina. Each rolls its own wait before every lunge, and in the Program those rolls are the only thing that tells the two apart, so who wins is a matter of chance.

A roll in a comparison gives the "only sometimes" of the previous section. It works in an `IF` and in a Context:

```regia
WHEN idle:
    GIVEN hungry AND RANDOM(1, 100) <= 30:       # three times in ten
        DO complain.
```

In a Context the roll can't be named, since a Context only tests. It is rolled, compared, and gone.

`#revise` A roll is whole or decimal depending on how its bounds are written, and a bound can be a Placeholder. `WAIT RANDOM(1, 3) SECONDS.` waits one, two or three seconds and never 1.4. Whoever wanted any wait between one and three has to know to write `RANDOM(1, 3.0)`.

Spec: chapter 04. For Durations, chapter 12.

## Picks at random

`showcase/playbooks/noble_socializing.regia`
```regia
TO vent:
    GIVEN grudge(?foe, ?size), HIGHEST ?size, AT RANDOM:
        DO sneer_at(?foe).
```

A Random choice chooses among Options we wrote down. A Pick `AT RANDOM` chooses among the Matches of a condition, which only exist at runtime: here the foes a Guest happens to have. In the showcase it only breaks the tie between two grudges of the same size. Alone, as in `GIVEN grudge(?foe, ?), AT RANDOM:`, it would take any grudge, each one equally likely.

Without a Pick, a condition with several Matches uses one of them and the language doesn't say which. Unspecified is not random: on Jason it is the same Match every time, so a Guest with three grudges would sneer at one foe all evening. When we want variety we write `AT RANDOM`.

`#revise` Options have Weights and Matches don't. "The bigger the grudge, the likelier we vent it" can't be written: a Pick is `HIGHEST`, which always takes the biggest, or `AT RANDOM`, which ignores the size.

Spec: chapter 26.

## A random part of a Role

`showcase/plots/royal_banquet.regia`
```regia
START SUBPLOT Poisoning, MAPPING 1 OF Guest TO Poisoner, MAPPING Guard TO Watchman.
```

A Mapping can take a number of a Role's Agents, or a share of them with `PERCENT OF`, in place of the whole Role. The Agents are drawn at random, every one equally likely, from those playing the Role when the Statement runs. So nobody, the Director included, decides who the Poisoner is.

The draw is made once. The Poisoner stays the same Guest for the whole Staging, and a latecomer who becomes a Guest afterwards is never added. Within one Statement no Agent is drawn twice. The number is an Expression, so `MAPPING RANDOM(1, 3) OF Guest TO Poisoner` gives a banquet with one to three Poisoners. The same form works for the target of an `ASSIGN`.

Spec: chapter 15, chapter 17.

## Random starting values

`showcase/banquet.regin`
```regia
AGENT noble PLAYS Guest:
    COUNT 6.
    bravery AT RANDOM(-0.6, 0.6).
    sympathy AT RANDOM(0, 0.8).
    aggressiveness AT RANDOM(-0.4, 0.4).
```

In Instancing, a Propensity can start at a fixed value or at `RANDOM(a, b)`. The value is drawn once for each Agent, when that Agent is created, so the six nobles are six different temperaments, and each run draws them again. A `latecomer` who joins halfway through gets a draw of its own. In Instancing this is the only way two Agents of one kind can differ.

The bounds are written Numbers between -1 and 1, with no Placeholders and no arithmetic. Nothing else in Instancing is random: `COUNT` is a written number, and every Agent of a kind plays every Role the kind lists. The small cast in `showcase/test.regin` fixes every value, so that the walkthrough reads the same each time.

`#revise` By the rule for rolls, `bravery AT RANDOM(-1, 1)` has whole bounds and would give -1, 0 or 1. The spec's Instancing chapter only says "drawn from [a, b]". Either the same word rolls differently in a `.regin` file, or the most natural way to write "any bravery" gives three temperaments.

Spec: chapter 21. For Propensities, chapter 14.

## The seed

The draws of a run start from a number, the seed. The Trace of a run opens with it, `RUN STARTED … SEED <n>`.

We write a seed in one place only, the header of a behaviour case, as `#! seed: 7`. Left out, it is 1. A case runs with a scripted game and a virtual clock, so with a fixed seed it makes the same choices every time, and its Trace can be compared line by line with the one we expect.

| We write | What is drawn | When |
|---|---|---|
| `EITHER` / `OR` | one Option | each time the Body reaches the `EITHER` |
| `RANDOM(a, b)` | a Number | each time the Expression is worked out |
| `, AT RANDOM` | one Match | each time the condition is checked |
| `n OF Role` | that many Agents | once, when the `ASSIGN` or `START SUBPLOT` runs |
| `p AT RANDOM(a, b)` | a starting value | once per Agent, when it is created |

The Trace has no entry for a draw. We see which Option ran from the Actions that followed, and an Agent's starting values from its `TEMPER` line.

`#revise` The seed can only be set in a behaviour case. A real run has one, since the Trace records it, but nothing in Instancing or on the command line lets us choose it. A banquet that went wrong with the full cast can't be played again.

`#revise` The spec says what the seed covers by listing constructs: `EITHER`, `AT RANDOM` and `RANDOM` Propensity values. A `RANDOM(a, b)` in a Body and the Agents drawn by `n OF` are not in the list, so we can't tell whether a case whose Spectators roll their stakes repeats.

Spec: chapter 34. For the Jason Target, chapters 35 and 36.

## How this combines with…

### Goals and Failure

`PURSUE vent` in an Option waits, like any `PURSUE`. If venting fails, the `idle` Plan fails with it. An Option can also hold a `FAIL`, to fail on purpose some of the time. A Random choice that runs no Option because every Weight is 0 is not a Failure, while a Weight that isn't a Number is one. (*Goals and Failure*)

### Several Plans under one Trigger

A roll in a `GIVEN` is made when that Context is checked, and each `GIVEN` rolls for itself:

```regia
WHEN idle:
    GIVEN RANDOM(1, 100) <= 30:
        DO chat.
    GIVEN RANDOM(1, 100) <= 30:
        DO sip_wine.
```

The first Plan applies three times in ten. The second is only looked at when the first didn't apply, so it runs about two times in ten, and half the time nothing runs and `idle` falls through to the next Playbook. A three-way split is a Random choice in one Body. `#revise` The two Contexts read as the same chance and aren't. (*Plans*, *Precedence and Labels*)

### Matching

A `COUNT` can be a Weight, as in `OR, WEIGHT ?grudges: PURSUE vent.` The count in one Plan keeps the Pick in `TO vent` from ever finding no Match, and nothing in the source ties the two together. (*Matching*)

### Role setup

`showcase/plots/royal_banquet.regia`
```regia
ROLE Guest STARTS WITH:
    ASSIGN Courtesy, MAPPING Host TO host.
    LEARN purse(RANDOM(5, 20)).
```

A Role setup takes Expressions, rolls included, and runs for each Agent that starts playing the Role. `#revise` The spec also says a setup is the same for every Agent of the Role, and doesn't say whether this roll is made once or once per Guest. The showcase assumes once per Guest. If it were once, every purse would hold the same gold, and the only way to vary a starting Fact would be a Plan that rolls it. (*Plots and Directors*)

### Subplots and Stagings

The `1 OF Guest` drawn for `Poisoning` is drawn among all the Guests, the two knights included. A knight is also a Guard, so it can be cast as `Poisoner` and `Watchman` of the same Staging, and hold `Scheming` next to `Keeping_watch`. `#revise` A counted Mapping can't say "one of the Guests who isn't a Guard". (*Subplots and Stagings*, *Playbooks and Roles*)

### Suits alternatives

The three ways a Guest takes an insult are chosen by the Selection function, which takes the alternative that best fits the Guest's Propensities. We shouldn't count on it for variety: a Guest whose Moods don't move takes every insult the same way. The chance is one step earlier, in the `RANDOM` values that made one noble braver than another. The Jason Target's `strategy` setting does have a `random` value next to `most_similar`, which the language doesn't describe. (*Precedence and Labels*, *Instancing*)

## Since 1.0

1.0 had no chance in it at all. Its primer only proposed a `GROUP` of Vocabulary items, "for choosing from a set of options", and 2.0 dropped the idea: a Random choice does the choosing, and a Fact with a parameter covers "any of these".

`#changes` Random choice (`EITHER`, `OR`, `WEIGHT`) is new. `GROUP` was never added and is not a reserved word.

`#changes` `RANDOM(a, b)`, the Pick `AT RANDOM`, counted Mappings (`n OF`, `n PERCENT OF`) and `RANDOM` starting values in Instancing are new.

`#changes` A run has a seed, written in a behaviour case and recorded in the Trace.
