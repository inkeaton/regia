# Plan bodies in Jason

How the Jason Target writes a Plan's Contexts and Statements in ASL: Placeholders as Jason variables, the variables the Transpiler makes up, `GIVEN` and `IF`, Random choice, Picks, `FOR EACH` and `COUNT`, the Basic Actions on Facts, `WAIT`, and Messages: how they are sent, how a Plan receives them, and how a told Fact is held. Decided in the ticket *A Plan's Statements in ASL* (`.scratch/showcase-1-5/issues/11-statements-in-asl.md`); *Messages* and the Facts' sources in the ticket *Messages and told Facts in ASL* (`.scratch/showcase-1-5/issues/12-messages-in-asl.md`). Both build on the research note *How Jason behaves where the translation waits* (branch `research/jason-facts`, `research/jason-facts.md`). It collects the ASL mapping notes of chapters 06, 07, 08, 09, 12 and 26, which now keep only what any AgentSpeak Target must respect and point here. It builds on chapter 28's names and on chapter 35's internal actions. Checked against Jason 3.3.4 (`references/jason-main/`) and 3.2.1, the version VEsNA-Pro pins (Regia runs on 3.3.2, chapter 28).

What this chapter doesn't hold: the plan around a Body (the Givings guard, chapter 29; precedence annotations, chapter 32), Actions sent to the game (`regia.act`, chapters 28 and 37), a Director's Signals and Messages (chapter 30), and how a Goal's endings are raised (chapter 40). The Goal Statements (`PURSUE`, `DROP`, `FAIL`, `PURSUING`) are here, under *Goals*, decided in the ticket *A Goal's life in ASL* (`.scratch/showcase-1-5/issues/13-goal-life-in-asl.md`).

## Placeholders and variables

- A **Placeholder** becomes a Jason variable with **its first letter uppercased** and nothing else changed: `?speaker` → `Speaker`, `?the_dish` → `The_dish`.
- A **blank**, `?` or `?_name` (chapter 03), becomes Jason's anonymous `_`. Two blanks never join, and neither do two `_`. A Jason variable such as `_who` is not used, because Jason would join two `_who` in one clause. Where a template needs to tell Matches apart by every blank (chapter 26), the blank becomes a fresh generated variable instead.
- A **generated variable**, which the Transpiler makes up for a weight, a total, a roll, a snapshot list and the like, is a Generated name (chapter 28) with its first letter uppercased: `Regia_weight__1`, `Regia_total`, `Regia_roll`, `Regia_each__1`. A Placeholder name can't start with `regia_` or contain `__` (`R1008`), so a generated variable never meets a Placeholder.
- The mapping is one-to-one because two Placeholders of one Plan can't differ only in case (`R1007`, chapter 10).
- A Placeholder is filled once per Plan run (chapter 03), and a Jason variable, once bound, stays bound for the rest of the plan. Nothing more is needed: no renaming, no copies.

## Contexts and `GIVEN`

- `AND`/`OR`/`NOT` map to `&`/`|`/`not`, which have the same precedence.
- **`?x PLAYS r`** is the conjunct `regia_plays(p, r, X)` (chapter 29), where `p` is the Playbook holding the Plan, with the Agent itself left in. `ME PLAYS r` is `.my_name(Me) & regia_plays(p, r, Me)`. Inside `COUNT`, a Pick or `FOR EACH` it is one more conjunct inside the `.setof`: `COUNT(grudge(?foe, ?) AND ?foe PLAYS peer)` (`noble_socializing.regia:9`) is `.setof(m(Foe, Regia_b__1), grudge(Foe, Regia_b__1) & regia_plays(nobleSocializing, peer, Foe), L) & .length(L, Grudges)`, so a foe reached through two Givings counts once. A Director's `PLAYS` is chapter 30's.
- Each `GIVEN` Block is its own plan with the shared trigger. Its context is its own Context **and the negation of every earlier sibling's Context** (`ctx3 & not ctx1 & not ctx2`), so "first match wins" doesn't hang on plan order. The `ELSE` plan's context negates them all. In the negated copies, every Placeholder **not filled by the Trigger** gets a fresh generated variable, so `GIVEN hates(?x)` then `GIVEN fears(?x)` gives `fears(X) & not hates(Regia_x__1)`. Placeholders filled by the Trigger stay shared on purpose. Why: chapter 06.

## `IF`

A Body `IF` chain maps to Jason's native `if (…) { … } elif (…) { … } else { … }`. Jason keeps a variable bound in an `if` condition bound for the rest of the plan. The Placeholder rules of chapter 06 mean this never changes what a later condition tests, so no renaming is needed. A failure inside a branch is the plan's own failure. Jason never emits the `regia_if__N` subgoal plans that chapter 06 describes for Targets without a native `if`.

## Random choice

Each weight is worked out into a generated variable, a negative one is clamped to 0 with a Trace entry, and then one roll is made from the seeded random source (chapter 35: a real number from 0 up to, but not including, the total). The pick is an `if`/`elif` chain on running sums. An Option holding only `PASS` is an empty branch (`true`):

```
+bored : … <-
    Regia_weight__1 = 3; Regia_weight__2 = 1; Regia_weight__3 = Anger;
    if (Regia_weight__3 < 0) { regia.trace(warning, warning, "T0902", [what(option(3))]) };
    Regia_weight__3c = math.max(0, Regia_weight__3);
    Regia_total = Regia_weight__1 + Regia_weight__2 + Regia_weight__3c;
    if (Regia_total > 0) {
        regia.random(Regia_total, Regia_roll);
        if (Regia_roll < Regia_weight__1) { wave }
        elif (Regia_roll < Regia_weight__1 + Regia_weight__2) { yawn }
        else { curse }
    } else {
        regia.trace(warning, warning, "T0903", [])
    }.
```

- Constant weights are folded by the Transpiler: there is no clamp and no Trace code when they are fixed and non-negative.
- A weight that isn't a Number makes the Jason arithmetic fail, which fails the Plan as required.
- Generated code never uses `math.random` or `.random`, only `regia.random`.
- A Placeholder filled in every Option stays bound after the chain, since Jason keeps it. One filled in only some Options is never seen by a later Statement (chapter 09). `LET ?x BE e` maps to `X = e`, and `?a != ?b` to `A \== B`.
- Jason never emits `regia_randomly__N`.

## Picks, `FOR EACH` and `COUNT`

Every `?` in these templates becomes a fresh generated variable, so that Matches are told apart by every blank.

- **Default**: the plain context, unchanged. Jason uses the first unifier.
- **`RANDOMLY`**: collect the distinct Matches with `.setof` over a tuple of the condition's blanks, then pick by index:

  ```
  +bored : .setof(m(G), guest(G), Regia_matches__1) & .length(Regia_matches__1, Regia_count__1) & Regia_count__1 > 0
           & regia.random(Regia_count__1, Regia_roll) & .nth(math.floor(Regia_roll), Regia_matches__1, m(G)) <- …
  ```

  `.setof` (not `.findall`) removes duplicates, such as the same Match from both branches of an `OR`. Jason accepts internal actions in contexts and in `if` conditions, so `IF …, RANDOMLY` uses the same formula.
- **`HIGHEST ?p` / `LOWEST ?p`**: `.setof` the Matches, keep those with `.number(P)`, take the `.max`/`.min` of the values, then take a Match with that value (`.member`). With `RANDOMLY`, `.setof` the tied Matches and pick by index as above.
- **`WEIGHT e`**: `.setof` the Matches with their Weight, `m(Blanks, W)`, then `regia.weighted_pick(L, m(Blanks, _))` (chapter 35). The internal action clamps negative Weights to 0. When the sum is 0 it writes `T2601` and fails, so the context doesn't hold. Otherwise it draws from the seeded source on running sums, as Random choice does. On a `GIVEN`, a Weight that isn't a Number is left out by a `.number(W)` test inside the `.setof`. On a Body `IF`, it is kept, so the internal action's arithmetic fails the Plan.
- **`FOR EACH`**: a `.setof` snapshot into a generated list, then Jason's `for` over it. From `dining.regia:30`:

  ```
  .setof(m(Dish), on_plate(Dish), Regia_each__1);
  for (.member(m(Dish), Regia_each__1)) {
      regia.act("eat", eat(Dish));
      -on_plate(Dish)
  }
  ```

  - **The snapshot is needed.** Jason's `for` works out its solutions lazily, so a `for` straight over `on_plate(Dish)` would see the Block's own `FORGET` and lose rounds. Chapter 26 requires the Matches to be collected once.
  - **Jason undoes every binding made in the body between rounds, and again after the loop** (`stdlib/foreach.java`; research note, question 3). That is Regia's rule: a Placeholder filled inside the Block lives for one round, and a later Statement can't see it.
  - A failure inside the Block fails the `for`, and with it the Plan.
  - A `WAIT`, a waiting `PURSUE` or a `DO` inside the Block suspends the intention in the middle of the loop, and the loop goes on when it resumes.
  - Jason never emits the recursive `regia_each__N` goal that chapter 26 describes for Targets without loops.
- **`COUNT`**: `.count(f, N)` when the condition is a single Fact, and `.setof(m(…), cond, L) & .length(L, N)` otherwise (an empty `.setof` gives `[]`, so 0). In a Body, the same, followed by the arithmetic.
- **Cost**: Picks, `FOR EACH` and `COUNT` build a list each time they are checked, linear in the matching Facts. The plain default doesn't.

## Basic Actions on Facts

- `LEARN f` maps to `+f`, guarded by `not f`, so that no event is raised for a known Fact and `LEARNED` Plans don't run. A Fact held only from a teller or the game is known too.
- `FORGET f` maps to `.abolish(f)`, guarded by `f`. A plain `-f` would remove only the `source(self)` annotation, and a Fact told by others or reported by the game would stay. `.abolish` removes the belief with every source, and raises one `-f` event, so `FORGOTTEN` fires once (*A told Fact*, below).
- `UPDATE f TO f2` maps to a test that `f` is known, which writes `T0801` and fails with `regia_because(Seq)` when it isn't (chapter 40, *The cause entry*), then `.abolish(f); +f2`. It is not `-+`, which matches any arguments. When `f` equals `f2`, it does nothing.
- `PRINT(a, b)` maps to `.print(a, " ", b)`.
- `PASS` maps to `true`, or to nothing when the Body has other Statements.

## `WAIT`

- **`WAIT d SECONDS`** maps to `regia.wait(D)` (chapter 35), where `D` is the Duration in milliseconds (`d * 1000`, or `d * 60000` for minutes). Like `.wait`, it suspends only its own intention. A constant Duration is folded by the Transpiler. Otherwise the Body works it out into a generated variable, clamps a negative value to 0 with `T1202`, and calls `regia.wait` on the result.
- **`WAIT d, UNTIL c`** maps to `regia.wait(Cond, D)`, and **`WAIT UNTIL c`** to `regia.wait(Cond)`. `Cond` is the condition compiled as a Jason logical formula, as for an `IF`. From `dining.regia:27`:

  ```
  regia.wait(on_plate(_), 60000);
  if (not on_plate(_)) { .fail(regia_fail, regia_reason(no_food)) }    // FAIL WITH no_food (Goals, below)
  ```

  - **When the condition is tested.** It is tested once at the call: if it already holds, the Body carries on at once. After that it is tested on **every new event** the agent gets, which is Jason's own `.wait` mechanism (`stdlib/wait.java`, `eventAdded`). Every belief added or removed raises an event, and Jason 3.3.4 adds events even with no relevant plan (`TransitionSystem.updateEvents`). So a change to a Fact, to `regia_phase` (`IN`) or to `regia_cast` (`PLAYS`) re-tests it, which is chapter 12's "whenever what it tests changes". It is not tested on every cycle.
  - **Running out of time never fails.** Jason's `.wait(Cond, T)` fails with `wait_timeout` when `T` runs out. `regia.wait` always succeeds, and the `IF` after it tells the two endings apart (chapter 12).
  - **Its variables stay as they were.** The condition fills no Placeholder (`R1204`), so the only unbound variables in `Cond` are `_`, and nothing is bound after the wait.
  - It is measured on the run's clock, which stops while the game is paused (chapter 37). Dropping the intention during the wait removes it (chapter 12).
  - It writes the **`time` entry** itself when the wait ends: `WAIT UNTIL <condition> MET` or `WAIT UNTIL <condition> TIMED OUT` (chapter 34), with `waited`, the milliseconds it waited. The condition is printed from `Cond`, as instantiated at the call, through the source map's names (chapter 35), with each `_` as `?`: `WAIT UNTIL on_plate(?) TIMED OUT`. Its `at` comes from the source map, like every entry's, so the call needs no extra argument.

## Messages

### Sending

| Statement | ASL |
| --- | --- |
| `TELL ?x f` (a Fact) | `regia.send(X, tell, f)` |
| `TELL ?x c` (a Cue, a local Cue included) | `regia.send(X, signal, c)` |
| `ASK ?x TO g` | `regia.send(X, achieve, g)` |
| `TELL Role …`, `ASK Role TO …` | the same, to each Agent of the Role's union (chapter 29) |
| `TELL 50% OF Role …`, `ASK 1 OF Role TO …` | the same, to each Agent `regia.pick` draws from that union (below) |
| `TELL EVERYONE …`, `ASK EVERYONE TO …` | `.broadcast(achieve, regia_everyone(Ilf, Content))`, with `Ilf` being `tell`, `signal` or `achieve` (chapter 30) |
| `SIGNAL c` | `regia.send(D, signal, c)` once for each distinct `D` in `regia_holds(p, D, …)` of the Playbook `p` holding the Statement: its Givings, or a closing's snapshot (chapter 29) |

- **A Cue travels as Jason's `signal` message.** The receiver gets the event `+c[source(S), signal]` and **no belief**, so every telling fires and nothing is left to test, as a Cue must be momentary (chapter 05). A plan written for `+c` is relevant to a `signal` event (`asSyntax/Trigger.java`), in Jason 3.2.1 and 3.3.4 alike, and VEsNA-Pro already sends its own game events this way.
- A game Cue arrives as the same kind of event, marked `source(percept)` (chapter 30). So `WHEN insulted:` hears both, and only `FROM` tells them apart.
- A local Cue is sent under its Generated name (`regia_local__courtesy__greeting`, chapter 28), like any local item.
- A `SIGNAL` is the same message as a told Cue. Only the recipients differ. How a Director receives it is chapter 30's.
- **A counted recipient** is drawn each time the Statement runs. From `dining.regia:26`:

  ```
  .my_name(Me);
  .setof(A, regia_plays(dining, waiter, A) & A \== Me, Regia_pool__1);
  regia.pick(count(1), Regia_pool__1, Regia_picked__1);
  for (.member(W, Regia_picked__1)) { regia.send(W, achieve, bring(Dish, Place)) }
  ```

  `regia.pick(count(N) | share(S), Pool, Picked)` draws from the run's one seeded source (chapter 35), uniformly and without replacement. A share **rounds up** against the pool, the sender already left out: `TELL 50% OF peer` with seven other peers tells four. It writes chapter 15's `T1502` when it asks for more than the pool holds (an empty pool included, so nothing is sent and the Plan goes on) and `T1503` for a negative count, and it fails only on a count that isn't a Number, which fails the Plan (chapter 15). A Director's counted picks call the same Java, except that a count that isn't a Number writes `T1501` there, since Director Statements never fail (chapter 20).
- Rejected forms for a Cue: a plain `tell`, which leaves a belief until a Plan removes it, so a Cue told again while the belief is there raises nothing (1.0's `untell` then `tell` works around this); and a generated achieve-goal per Cue, which a Cue with no applicable plan would turn into a Goal Failure.

### Who sent it

A Trigger's Sender is the trigger's `source(S)` annotation. A told Cue or Fact carries the sending Agent's or Director's name, a game item `percept`, and the Agent's own `LEARN` `self`.

| Trigger | Plan |
| --- | --- |
| no `FROM` | `+c[source(_)]`: no test, so it hears the game too |
| `FROM ?who` | `+c[source(Who)] : … & Who \== percept & Who \== self` |
| `FROM Role`, `FROM Role ?who` | the Sender is in the Role's union over the Playbook's Givings (chapter 29) |
| `FROM DIRECTOR` | `regia_holds(p, S, _, _, _, _)`: a Director giving this Playbook, or that gave it before a take still closing (chapters 05, 29) |

`FROM GAME` and `FROM ME`, which are later than 1.5, would be `S == percept` and `S == self`. The same tests serve `LEARNED, FROM …` on a told Fact (below) and a Goal's `TO …, FROM …`.

### A told Fact

**A Fact raises `+f` only when the Agent didn't know it**, from any source. Chapter 07 needs this for `LEARNED`, and Jason doesn't give it: a Fact told again by a new teller raises `+f[source(new)]` again (research note, question 1).

- **It is decided when the message arrives.** `regia.RegiaAgent` overrides `brf`. When the belief to add is already held, from a teller, from the game or from the Agent's own `LEARN`, it adds the new source to the belief and raises **no event**. Otherwise it adds the belief and raises `+f[source(S)]` as usual.
- Why not a Context test (`f[source(O)] & O \== S`): the belief base is updated before the plan's context is tested. When two Agents tell the same Fact before either plan runs, both contexts see two sources, and `LEARNED` would never fire.
- So the Sender of a `LEARNED` Trigger is the Fact's **first teller**, and `LEARNED, FROM ?who`, `FROM peer` and `FROM DIRECTOR` test that Sender like any other. A Fact already known fires nothing, whoever tells it. When the Director tells `on_duty` to a knight who already holds it (`royal_banquet.regia:128`), `WHEN on_duty LEARNED, FROM DIRECTOR:` doesn't run and the knight doesn't salute.
- **A Fact goes with all its sources.** `FORGET` and `UPDATE` use `.abolish` (*Basic Actions on Facts*, above). A game report removing a Fact removes it whatever its sources (chapter 30): a told Fact is the Agent's own Fact, and nothing remembers who told it (chapter 07). Messages only add (chapter 07), so these are the only ways a Fact goes, and each raises one `-f`. `FORGOTTEN` fires once.
- The sources stay underneath, which leaves room for `TOLD` (chapter 07).

### `ME`

The Role files are shared by every Agent of a kind (chapter 28), so an Agent's name isn't known at build.

- **As a Value**, `ME` is a generated variable bound once at the start of the Body, only when the Plan uses it: `.my_name(Regia_me); …; regia.send(…, tell, wronged(Regia_me, Speaker))`.
- **In a Trigger's pattern**, `ME` is a fresh generated variable in the trigger, tested right after the Givings guard. From `noble_socializing.regia:48`:

  ```
  +scandal(Regia_me__1)[source(Speaker)] : regia_given(nobleSocializing, _, _, _, _, _) & .my_name(Regia_me__1) & <Speaker in peer> <- …
  ```

  How this Plan and `WHEN scandal(?victim)` compete is chapter 13's.

### Nothing heard: `T0702`

A told Cue that no Plan of the Agent's given Playbooks runs for writes an `unheard` entry (chapter 34). Jason runs at most one plan per event, and drops an event no plan takes, so the Transpiler emits **one catch-all plan per Cue that some `TELL` in the Program sends**. They are in a generated file that every Role file includes, `asl/unheard.asl` (chapter 28):

```
@regia_unheard__scandal[regia_unheard]
+scandal(Regia_a__1)[source(S)] : S \== percept
   <- regia.trace(unheard, info, "T0702", [cue(scandal(Regia_a__1)), sender(S)]).
```

- **"No Plan ran", not "no Plan exists".** Gossip about a stranger, which falls through every `GIVEN` of `WHEN scandal(?victim)` with no `ELSE` (`noble_socializing.regia:54`), writes `T0702`. So does a Cue told to an Agent whose Playbooks never name it, such as `scandal` told to a Servant (`noble_socializing.regia:24`), and a Cue for a Playbook taken away.
- `selectOption` chooses a `regia_unheard` plan only when it is the only option (chapter 32), so it never competes with a Playbook's plan and never reaches `Temper`.
- A catch-all on a variable trigger (`+C[source(S)]`) wouldn't do. Jason tries such a plan only when **no** plan is relevant, so it would miss a Cue whose Plans are all inapplicable.
- A game Cue no Plan takes is dropped silently, as before.
- A Cue that a Quota Trigger watches has a dispatcher instead, and its catch-all is the dispatcher's failure plans (chapter 33).

## Goals

How a Goal Statement is written in ASL. What each internal action does, and how the endings are raised, is chapter 40.

| Statement | ASL |
| --- | --- |
| `PURSUE g` | `regia.pursue(g, Regia_pursuit__N); !g[regia_pursuit(Regia_pursuit__N)]` |
| `PURSUE g, WITHOUT WAITING` | `regia.pursue(g, Regia_pursuit__N); !!g[regia_pursuit(Regia_pursuit__N)]` |
| `DROP g` | `regia.drop(g)` |
| `FAIL` | `.fail(regia_fail)` |
| `FAIL WITH r` | `.fail(regia_fail, regia_reason(r))` |
| `PURSUING g`, in a `TO g` Plan | `regia.pursuing(g, Regia_pursuit)`, the trigger's own `Id` |
| `PURSUING g`, anywhere else | `regia.pursuing(g, none)` |

- **A recipe's trigger** binds the Sender and the Pursuit's `Id`, and its Body ends with `regia.reached` (chapter 40, *`REACHED`*). From `serving.regia:15`:

  ```
  @regia_plan__serving__4[regia_rank(serving, to(fetch), 0)]
  +!fetch(Dish)[source(Regia_sender), regia_pursuit(Regia_pursuit)] : regia_given(serving, _, _, _, _, _)
     <- regia.act("walk_to", walk_to(kitchen));
        if (not in_stock(Dish)) { .fail(regia_fail, regia_reason(sold_out(Dish))) };
        regia.act("pick_up", pick_up(Dish));
        regia.reached(fetch(Dish), Regia_sender, Regia_pursuit).
  ```

  A `TO g, FROM …` Plan writes its Sender variable or test in place of `Regia_sender` (*Who sent it*, above).
- `!g` adds `source(self)` itself. The `Id` is a generated variable, one per `PURSUE` Statement.
- The Statements write no Trace entry of their own. `FAIL`'s `T1103` is written by whoever catches it (chapter 40, *The cause entry*), so it is written once.
- `NOT PURSUING g` is `not regia.pursuing(…)`. A `PURSUING` with Placeholders fills them, one unifier per Pursuit, like a Fact.
- An ending Plan (`WHEN g REACHED`, `DROPPED`, `FAILED`, `ENDED`) is a plan for a generated goal, `+!regia_failed(G, Sender, Reason, Id, Closing)` and the like: chapter 40, *The ending goals*.

## `regia-jason` additions

- `regia.wait(Cond)` and `regia.wait(Cond, D)`, built on Jason's `wait` class and measured on the run's clock. They are listed with the other internal actions in chapter 35.
- `regia.RegiaAgent` overrides `brf`, so a Fact already known takes a new source without an event (*A told Fact*).
- The Goal internal actions (`regia.pursue`, `regia.drop`, `regia.pursuing`, `regia.reached`) are chapter 40's.

## Targets without a native `if` or loop

Chapters 06, 09 and 26 describe how a Target with no `if` or no loop lowers `IF`, `RANDOMLY` and `FOR EACH` to generated subgoals (`regia_if__N`, `regia_randomly__N`, `regia_each__N`). The Jason Target has both, so it emits none of them, and chapters 29 and 35 don't mention them.

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025).

## Not decided here

- A Director's Messages, how it receives a Signal, and its catch-all for `T3801`: chapter 30.
- Checking that a recipient Placeholder holds an Agent (`T0701`) and catching sends to Agents who have left: `regia.send`, chapter 33.
- How a Goal's endings are raised, the generated `-!g`, and the walker behind `DROP`: chapter 40.
- `SHIFT` and Moods: *Moods and Labels on VEsNA-Pro* (`.scratch/showcase-1-5/issues/20-moods-on-vesna.md`).
- Entering and leaving a Phase, `AFTER`: *Entering and leaving a Phase in ASL* (`.scratch/showcase-1-5/issues/18-phase-change.md`).
