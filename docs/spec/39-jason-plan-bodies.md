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

A Random choice is one step to choose, then Jason's native `if`/`elif` chain on the chosen Option's number. The choosing is the Infrastructure plan **`regia_choose(Weights, N)`** of `regia/agent.asl`. It works out the list of weights, clamps a negative one to 0 with `T0902`, rolls with `.random` from the Agent's seeded generator (chapter 35), and binds `N` to the chosen Option's number, from 1. When the total is 0 it writes `T0903` and binds `N` to 0, so no branch runs. An Option holding only `PASS` is an empty branch (`true`):

```
+bored : … <-
    !regia_choose([3, 1, Anger], Regia_option__1);
    if (Regia_option__1 == 1) { wave }
    elif (Regia_option__1 == 2) { yawn }
    elif (Regia_option__1 == 3) { curse }.
```

- A subgoal hands its bindings back (chapter 28), so `Regia_option__1` is bound when the `if` runs.
- A weight that isn't a Number makes the plan's arithmetic fail, which fails `regia_choose` and with it the Plan, as required.
- Generated code draws only through Jason's `.random` and `math.random`, which share the Agent's one seeded generator, and never through `.shuffle`, which doesn't (chapter 35).
- A Placeholder filled in every Option stays bound after the chain, since Jason keeps it. One filled in only some Options is never seen by a later Statement (chapter 09). `LET ?x BE e` maps to `X = e`, and `?a != ?b` to `A \== B`.
- Jason never emits `regia_randomly__N`.

## Picks, `FOR EACH` and `COUNT`

Every `?` in these templates becomes a fresh generated variable, so that Matches are told apart by every blank.

- **Default**: the plain context, unchanged. Jason uses the first unifier.
- **`RANDOMLY`**: the rule **`regia_random_match(T, F)`** of `regia/agent.asl` collects the distinct Matches of `F` as tuples `T` of the condition's blanks, and picks one with `.random`:

  ```
  regia_random_match(T, F) :- .setof(T, F, L) & .random(L, T).

  +bored : regia_random_match(m(G), guest(G)) <- …
  ```

  `.setof` (not `.findall`) removes duplicates, such as the same Match from both branches of an `OR`. An empty `.setof` gives no Match for `.random` to pick, so the context doesn't hold. Jason accepts rules in contexts and in `if` conditions, so `IF …, RANDOMLY` uses the same formula.
- **`HIGHEST ?p` / `LOWEST ?p`**: the rules **`regia_highest(T, P, F)`** and **`regia_lowest(T, P, F)`** `.setof` the Matches with their value, keep those with `.number(P)`, take the `.max`/`.min` of the values, then a Match with that value (`.member`). With `RANDOMLY`, **`regia_highest_random`** and **`regia_lowest_random`** `.setof` the tied Matches and pick with `.random`, as above.
- **`WEIGHT e`**: `.setof` the Matches with their Weight, `m(Blanks, W)`, then `regia.weighted_pick(L, m(Blanks, _))` (chapter 35). It stays an internal action because it writes the Trace from inside a context, which a rule mustn't do (chapter 28, reason 1). It clamps negative Weights to 0. When the sum is 0 it writes `T2601` and fails, so the context doesn't hold. Otherwise it draws from the Agent's seeded generator on running sums. On a `GIVEN`, a Weight that isn't a Number is left out by a `.number(W)` test inside the `.setof`. On a Body `IF`, it is kept, so the internal action's arithmetic fails the Plan.
- **`FOR EACH`**: Jason's `for` over the rule **`regia_each(T, F)`** of `regia/agent.asl`, which snapshots the Matches. From `dining.regia:30`:

  ```
  regia_each(T, F) :- .setof(T, F, L) & .member(T, L).

  for (regia_each(m(Dish), on_plate(Dish))) {
      regia.act("eat", eat(Dish));
      .abolish(on_plate(Dish))
  }
  ```

  - **The snapshot is needed.** Jason's `for` works out its solutions lazily, so a `for` straight over `on_plate(Dish)` would see the Block's own `FORGET` and lose rounds. Chapter 26 requires the Matches to be collected once. In `regia_each`, `.setof` runs once, at the first round, and the later rounds come from `.member` walking the built list (research note of *Readable generated ASL*, *`for` over a rule*).
  - **Jason undoes every binding made in the body between rounds, and again after the loop** (`stdlib/foreach.java`; research note, question 3). That is Regia's rule: a Placeholder filled inside the Block lives for one round, and a later Statement can't see it.
  - A failure inside the Block fails the `for`, and with it the Plan.
  - A `WAIT`, a waiting `PURSUE` or a `DO` inside the Block suspends the intention in the middle of the loop, and the loop goes on when it resumes.
  - Jason never emits the recursive `regia_each__N` goal that chapter 26 describes for Targets without loops.
- **`COUNT`**: `.count(f, N)` when the condition is a single Fact, and `.setof(m(…), cond, L) & .length(L, N)` otherwise (an empty `.setof` gives `[]`, so 0). In a Body, the same, followed by the arithmetic.
- **Cost**: Picks, `FOR EACH` and `COUNT` build a list each time they are checked, linear in the matching Facts. The plain default doesn't.

## Basic Actions on Facts

- `LEARN f` maps to `+f`. `regia.RegiaAgent.brf` gives a Fact already known from any source no event (*A told Fact*, below), so `LEARNED` Plans don't run, and no guard is written.
- `FORGET f` maps to `.abolish(f)`. A plain `-f` would remove only the `source(self)` annotation, and a Fact told by others or reported by the game would stay. `.abolish` removes the belief with every source, and raises one `-f` event, so `FORGOTTEN` fires once (*A told Fact*, below). When `f` isn't known it removes nothing and raises nothing, so no guard is written.
- `UPDATE f TO f2` maps to `!regia_update(f, f2)`, an Infrastructure plan of `regia/agent.asl`. When `f` isn't known it writes `T0801` and fails with `regia_because(Seq)` (chapter 40, *The cause entry*). Otherwise it does `.abolish(f); +f2`. It is not `-+`, which matches any arguments. When `f` equals `f2`, it does nothing.
- `PRINT(a, b)` maps to `.print(a, " ", b)`.
- `PASS` maps to `true`, or to nothing when the Body has other Statements.

## `WAIT`

- **`WAIT d SECONDS`** maps to `regia.wait(D)` (chapter 35), where `D` is the Duration in milliseconds (`d * 1000`, or `d * 60000` for minutes). Like `.wait`, it suspends only its own intention. A constant Duration is folded by the Transpiler. Otherwise the Body works it out into a generated variable and calls `regia.wait` on it, and `regia.wait` clamps a negative value to 0 with `T1202`. It stays an internal action because it is measured on the run's clock (chapter 28, reason 2).
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
| `TELL Role …`, `ASK Role TO …` | `?regia_audience(p, role, L)`, then the same with `L`: each Agent of the Role's union, the Agent itself left out (chapter 29) |
| `TELL 50% OF Role …`, `ASK 1 OF Role TO …` | `!regia_draw(p, role, share(50), L)`, then the same with `L` (below) |
| `TELL EVERYONE …`, `ASK EVERYONE TO …` | `.broadcast(achieve, regia_everyone(Ilf, Content))`, with `Ilf` being `tell`, `signal` or `achieve` (chapter 30) |
| `SIGNAL c` | `?regia_directors(p, L); regia.send(L, signal, c)`, with `L` each distinct `D` in `regia_holds(p, D, …)` of the Playbook `p` holding the Statement: its Givings, or a closing's snapshot (chapter 29) |

- **A Cue travels as Jason's `signal` message.** The receiver gets the event `+c[source(S), signal]` and **no belief**, so every telling fires and nothing is left to test, as a Cue must be momentary (chapter 05). A plan written for `+c` is relevant to a `signal` event (`asSyntax/Trigger.java`), in Jason 3.2.1 and 3.3.4 alike, and VEsNA-Pro already sends its own game events this way.
- A game Cue arrives as the same kind of event, marked `source(percept)` (chapter 30). So `WHEN insulted:` hears both, and only `FROM` tells them apart.
- A local Cue is sent under its Generated name (`regia_local__courtesy__greeting`, chapter 28), like any local item.
- A `SIGNAL` is the same message as a told Cue. Only the recipients differ. How a Director receives it is chapter 30's.
- **`regia.send(To, Ilf, Content)`** takes one receiver or a list, and sends to each. It stays an internal action because Jason's `.send` fails the sender's plan on a receiver that has left, and stops a list there (chapter 28, reason 1; research note of *Readable generated ASL*, *Sending*). `regia.send` writes `T1901` for that receiver and goes on with the rest. It also writes `T0701` for a recipient Placeholder that doesn't hold an Agent (chapter 33).
- **The Role's union** is the rule **`regia_audience(P, R, L)`** of `regia/agent.asl`, read with a test goal when the Statement runs. `SIGNAL`'s Directors are **`regia_directors(P, L)`**:

  ```
  regia_audience(P, R, L)  :- .my_name(Me) & .setof(A, regia_plays(P, R, A) & A \== Me, L).
  regia_directors(P, L)    :- .setof(D, regia_holds(P, D, _, _, _, _), L).
  ```

  From `courtesy.regia:13`, `TELL host greeting` is:

  ```
  ?regia_audience(courtesy, host, Regia_to__1); regia.send(Regia_to__1, signal, regia_local__courtesy__greeting)
  ```

  An empty union gives `[]`, and nothing is sent.
- **A counted recipient** is drawn each time the Statement runs, by the Infrastructure plan **`regia_draw(P, R, count(N) | share(S), L)`** of `regia/agent.asl`. It reads `regia_audience` and draws from it with `.random`, uniformly and without replacement. From `dining.regia:26`:

  ```
  !regia_draw(dining, waiter, count(1), Regia_to__1); regia.send(Regia_to__1, achieve, bring(Dish, Place))
  ```

  A share **rounds up** against the pool, the sender already left out: `TELL 50% OF peer` with seven other peers tells four. `regia_draw` writes chapter 15's `T1502` when it asks for more than the pool holds (an empty pool included, so nothing is sent and the Plan goes on) and `T1503` for a negative count, and it fails only on a count that isn't a Number, which fails the Plan (chapter 15). A Director's counted picks use the same draw in `regia/director.asl`, except that a count that isn't a Number writes `T1501` there, since Director Statements never fail (chapter 20).
- Rejected forms for a Cue: a plain `tell`, which leaves a belief until a Plan removes it, so a Cue told again while the belief is there raises nothing (1.0's `untell` then `tell` works around this); and a generated achieve-goal per Cue, which a Cue with no applicable plan would turn into a Goal Failure.

### Who sent it

A Trigger's Sender is the trigger's `source(S)` annotation. A told Cue or Fact carries the sending Agent's or Director's name, a game item `percept`, and the Agent's own `LEARN` `self`.

| Trigger | Plan |
| --- | --- |
| no `FROM` | `+c[source(_)]`: no test, so it hears the game too |
| `FROM ?who` | `+c[source(Who)] : … & regia_from_agent(Who)` |
| `FROM Role`, `FROM Role ?who` | `regia_from_role(p, role, S)`: the Sender is in the Role's union over the Playbook's Givings (chapter 29) |
| `FROM DIRECTOR` | `regia_from_director(p, S)`: a Director giving this Playbook, or that gave it before a take still closing (chapters 05, 29) |

The three are rules of `regia/agent.asl`, one definition each:

```
regia_from_agent(S)       :- S \== percept & S \== self.
regia_from_role(P, R, S)  :- regia_plays(P, R, S).
regia_from_director(P, S) :- regia_holds(P, S, _, _, _, _).
```

`regia_from_role` needs no test for `percept` or `self`, since a cast lists only Agents' names. `FROM GAME` and `FROM ME`, which are later than 1.5, would be rules `regia_from_game(S)` and `regia_from_me(S)`, testing `S == percept` and `S == self`. The same tests serve `LEARNED, FROM …` on a told Fact (below) and a Goal's `TO …, FROM …`.

### A told Fact

**A Fact raises `+f` only when the Agent didn't know it**, from any source. Chapter 07 needs this for `LEARNED`, and Jason doesn't give it: a Fact told again by a new teller raises `+f[source(new)]` again (research note, question 1).

- **It is decided when the message arrives.** `regia.RegiaAgent` overrides `brf`. When the belief to add is already held, from a teller, from the game or from the Agent's own `LEARN`, it adds the new source to the belief and raises **no event**. Otherwise it adds the belief and raises `+f[source(S)]` as usual.
- Why not a Context test (`f[source(O)] & O \== S`): the belief base is updated before the plan's context is tested. When two Agents tell the same Fact before either plan runs, both contexts see two sources, and `LEARNED` would never fire.
- So the Sender of a `LEARNED` Trigger is the Fact's **first teller**, and `LEARNED, FROM ?who`, `FROM peer` and `FROM DIRECTOR` test that Sender like any other. A Fact already known fires nothing, whoever tells it. When the Director tells `on_duty` to a knight who already holds it (`royal_banquet.regia:128`), `WHEN on_duty LEARNED, FROM DIRECTOR:` doesn't run and the knight doesn't salute.
- **A Fact goes with all its sources.** `FORGET` and `UPDATE` use `.abolish` (*Basic Actions on Facts*, above). A game report removing a Fact removes it whatever its sources (chapter 30): a told Fact is the Agent's own Fact, and nothing remembers who told it (chapter 07). Messages only add (chapter 07), so these are the only ways a Fact goes, and each raises one `-f`. `FORGOTTEN` fires once.
- The sources stay underneath, which leaves room for `TOLD` (chapter 07).

### `ME`

The Role files are shared by every Agent of a kind (chapter 28), so an Agent's name isn't known at build.

- **As a Value**, `ME` is a generated variable bound once at the start of the Body, only when the Plan uses it: `.my_name(Regia_me); …; regia.send(…, tell, wronged(Regia_me, Speaker))`. A recipient list leaves the Agent out inside `regia_audience`, so no `ME` is bound for that.
- **In a Trigger's pattern**, `ME` is a fresh generated variable in the trigger, tested right after the Givings guard. From `noble_socializing.regia:48`:

  ```
  +scandal(Regia_me__1)[source(Speaker)] : regia_is_given(nobleSocializing) & .my_name(Regia_me__1) & regia_from_role(nobleSocializing, peer, Speaker) <- …
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
| `PURSUE g` | `regia.trace(goal, info, "", [goal(g), event(pursued)], Regia_pursuit__N); !g[regia_pursuit(Regia_pursuit__N)]` |
| `PURSUE g, WITHOUT WAITING` | `regia.trace(goal, info, "", [goal(g), event(pursued)], Regia_pursuit__N); !!g[regia_pursuit(Regia_pursuit__N)]` |
| `DROP g` | `regia.drop(g)` |
| `FAIL` | `.fail(regia_fail)` |
| `FAIL WITH r` | `.fail(regia_fail, regia_reason(r))` |
| `PURSUING g`, in a `TO g` Plan | `.intend(g[regia_pursuit(Regia_id__N)]) & Regia_id__N \== Regia_pursuit`, leaving out the trigger's own `Id` |
| `PURSUING g`, anywhere else | `.intend(g)` |

- **A recipe's trigger** binds the Sender and the Pursuit's `Id`, and its Body ends with `!regia_reach` (chapter 40, *`REACHED`*). From `serving.regia:15`:

  ```
  @regia_plan__serving__2[regia_rank(serving, to(fetch), 0)]
  +!fetch(Dish)[source(Regia_sender), regia_pursuit(Regia_pursuit)] : regia_is_given(serving)
     <- regia.act("walk_to", walk_to(kitchen));
        if (not in_stock(Dish)) { .fail(regia_fail, regia_reason(sold_out(Dish))) };
        regia.act("pick_up", pick_up(Dish));
        !regia_reach(fetch(Dish), Regia_sender, Regia_pursuit).
  ```

  A `TO g, FROM …` Plan writes its Sender variable or test in place of `Regia_sender` (*Who sent it*, above).
- `!g` adds `source(self)` itself. The `Id` is a generated variable, one per `PURSUE` Statement.
- The Statements write no Trace entry of their own. `FAIL`'s `T1103` is written by whoever catches it (chapter 40, *The cause entry*), so it is written once.
- `NOT PURSUING g` is `not .intend(…)`. A `PURSUING` with Placeholders fills them, one unifier per Pursuit, like a Fact: `.intend` backtracks over every frame of every intention (research note of *Readable generated ASL*, *`.intend`*). It finds a Pursuit waiting in `regia.wait` or `regia.act`, because neither flags its intention as suspended (chapter 37).
- The `PURSUED` entry is written by `regia.trace` with its optional last argument, which binds the entry's `seq` (chapter 35). That `seq` is the Pursuit's `Id`.
- An ending Plan (`WHEN g REACHED`, `DROPPED`, `FAILED`, `ENDED`) is a plan for a generated goal, `+!regia_failed(G, Sender, Reason, Id, Closing)` and the like: chapter 40, *The ending goals*.

## `regia-jason` additions

- `regia.wait(Cond)` and `regia.wait(Cond, D)`, built on Jason's `wait` class and measured on the run's clock (reason 2). `regia.wait(D)` clamps a negative `D` with `T1202`. They are listed with the other internal actions in chapter 35.
- `regia.send(To, Ilf, Content)`, with `To` one receiver or a list (reason 1).
- `regia.weighted_pick(L, M)` (reason 1: it writes `T2601` from a context).
- `regia.RegiaAgent` overrides `brf`, so a Fact already known takes a new source without an event (*A told Fact*; reason 4).

## Infrastructure

In `regia/agent.asl`, and in `regia/director.asl` where a Director uses the same Statement:

- Rules: `regia_is_given` and `regia_given_or_closing` (chapter 29), `regia_from_agent`, `regia_from_role`, `regia_from_director`, `regia_audience`, `regia_directors`, `regia_random_match`, `regia_highest`, `regia_lowest`, `regia_highest_random`, `regia_lowest_random`, `regia_each`.
- Infrastructure plans: `regia_choose`, `regia_draw`, `regia_update`, and `regia_reach` (chapter 40).

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
