# Readable generated ASL

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

Which recurring patterns of the generated ASL become named Infrastructure, and in which form?

Chapter 28, *Generated ASL is readable*, sets the rule (a generated plan reads like the designer's Plan; each Statement one step) and the three forms (rule, internal action, Infrastructure plan). Apply it pattern by pattern across chapters 29–40.

Candidates found in *Review: Model to Target*: the Givings guard `regia_given(p, _, _, _, _, _)` (a rule such as `regia_active(p)`); the `FROM` tests (`regia_holds(p, S, …)`, `S \== percept & S \== self`); `TELL Role` and `TELL n OF Role` (`.setof` + `regia.pick` + `for` + `regia.send`); `SIGNAL`; the four-step `-!g` of `goals.asl` (check what `regia.goal_failed` reads if part of it becomes a subgoal). Also the Director side (chapters 30, 31, 33).

Decide as well: whether a plan label should name its Trigger, as 1.0's `pb__NobleSocializing__insult_heard__0` did (now `regia_plan__<owner>__<n>`, chapter 28).

Work by hand: `courtesy.regia` and `serving.regia`, rewritten. Then bring the guide's hand-written ASL (`docs/guide/22`–`25`) to the result, labels included.

Blocks the M7 emit tickets, once they are cut. Chapters 28–40; references `references/` (Jason source) for subgoal and internal action costs.

## Resolution

Agreed with Edoardo on 2026-11-27. Edoardo widened the question at the start of the grilling: generated ASL should stay **Jason ASL as much as possible**, with fewer calls into `regia-jason` and more of Jason's own stdlib. So the ticket also sorted every `regia.*` internal action. The answer is in chapter 28, *Generated ASL is readable*, and ADR 0050, *Generated ASL is Jason first*. The Jason facts it rests on, with file:line citations, are in the research note `../research/13-jason-native-facts.md`.

- **The rule.** Each Statement is one body step, or a test goal and the one action it feeds. Mechanics that recur are named in `agent.asl`/`director.asl`: a rule for a test or a collection, an Infrastructure plan for steps that wait, fail or write the Trace. A `regia.*` action exists only for one of four reasons:
  1. it leaves the agent with semantics the stdlib lacks;
  2. it needs the run's clock;
  3. it reshapes intentions beyond the stdlib;
  4. it hooks the reasoning cycle.
- **Rules** (chapters 29 and 39): `regia_is_given`, `regia_given_or_closing`, `regia_from_agent`, `regia_from_role`, `regia_from_director`, `regia_audience`, `regia_directors`, `regia_random_match`, `regia_highest`/`_lowest` (and `_random`), `regia_each`, `regia_roll`.
- **Infrastructure plans**: `regia_reach` (chapter 40), `regia_choose`, `regia_draw`, `regia_update` (chapter 39), and the three `regia_everyone` unwraps (chapter 30).
- **Retired.** Each goes to Jason's own form or to the rules and plans above:
  - `regia.pick` → `regia_draw`;
  - `regia.pursue` → `regia.trace` with an optional `Seq` out-argument;
  - `regia.reached` → `regia_reach`;
  - `regia.pursuing` → `.intend`;
  - `regia.random` → `.random`/`math.random` on a per-agent generator seeded from the run;
  - `regia.deliver` → `+F[source(S)]` and `.signal`;
  - `regia.start_staging` → `.create_agent` (to confirm on JaCaMo 1.3.1).
  
  `LEARN` and `FORGET` lose their guards (`brf`, and `.abolish` on nothing raises nothing).
- **Kept**, each with its reason written where it is defined:
  - `regia.act`, `regia.trace`, `regia.send` (now taking a list), `regia.weighted_pick`, `regia.goal_failed` and the link calls (reason 1);
  - `regia.wait`, which now also clamps (reason 2);
  - `regia.drop`, `regia.stop_playbook`, `regia.stop_phase`, `regia.end_body` and `regia.pass_failure` (reason 3);
  - `regia.shift` (reason 4).
- **`-!g`** keeps its four steps. A shared plan would loop, and plain `.fail` can't end an intention quietly. Chapter 40, *Why `-!g` is written out*, also records that the `-!regia_<kind>` catchers are load-bearing.
- **Plan labels** stay `regia_plan__<owner>__<n>`. The rank annotation already names the Item.
- **Consequences written into the spec:**
  - `regia.act` and `regia.wait` must suspend through Jason's pending intentions, never through `.suspend` or `ConcurrentInternalAction` (chapter 37), or `.intend` would miss a waiting Pursuit.
  - An entry written from an Infrastructure plan takes the `at` of the nearest mapped frame below (chapter 35). Without this, `T0801`, `T0902`, `T1502` and `REACHED` would lose their place.
- **Spec disagreements found and fixed:**
  - chapter 40's `serving.regia:21` example tested `\== percept & \== self` after `regia_plays`, which chapter 39 doesn't, and a cast can't hold either;
  - chapter 31 said `.create_agent` couldn't set the agent class, but it can;
  - chapter 39's `FOR EACH` example used `-on_plate(Dish)` where `FORGET` is `.abolish`;
  - the `serving` plan labels (`__4`, `__9`, `__10`) broke the per-owner source-order rule, and are now `__2`, `__3`, `__4`.
- **Edited:**
  - spec chapters 08, 09, 15, 26, 28, 29, 30, 31, 33, 35, 37, 39 and 40;
  - guide 06, 08, 21, 22, 23, 24 and 25;
  - ADR 0050.
  
  Label numbers in the guide other than `courtesy` and `serving` are illustrative, as the guide says.
- No glossary term was added: the new names are Generated names, not language terms.

### Worked result

What the M7 emit tickets are judged against. Includes, headers and the source map are left out.

`asl/playbooks/Courtesy.asl`:

```
@regia_plan__courtesy__1[regia_rank(courtesy, to(take_seat), 0)]
+!take_seat[source(Regia_sender), regia_pursuit(Regia_pursuit)]
    : regia_is_given(courtesy) & regia_from_director(courtesy, Regia_sender) & seat(Place)
   <- regia.act("walk_to", walk_to(Place));
      regia.act("sit_down", sit_down);
      ?regia_audience(courtesy, host, Regia_to__1); regia.send(Regia_to__1, signal, regia_local__courtesy__greeting);
      !regia_reach(take_seat, Regia_sender, Regia_pursuit).

@regia_plan__courtesy__2[regia_rank(courtesy, failed(take_seat), 0)]
+!regia_failed(take_seat, _, _, _, _)
    : regia_is_given(courtesy)
   <- regia.act("stand_by", stand_by(wall)).

@regia_plan__courtesy__3[regia_rank(courtesy, ended(take_seat), 0)]
+!regia_ended(take_seat, _, _, Regia_closing)
    : regia_given_or_closing(courtesy, Regia_closing)
   <- ?regia_directors(courtesy, Regia_to__1); regia.send(Regia_to__1, signal, took_seat).

@regia_plan__courtesy__4[regia_rank(courtesy, when(regia_local__courtesy__greeting), 0)]
+regia_local__courtesy__greeting[source(Who)]
    : regia_is_given(courtesy) & regia_from_agent(Who)
   <- regia.act("bow_to", bow_to(Who)).

@regia_plan__courtesy__5[regia_rank(courtesy, to(take_leave), 0)]
+!take_leave[source(Regia_sender), regia_pursuit(Regia_pursuit)]
    : regia_is_given(courtesy) & regia_from_director(courtesy, Regia_sender)
   <- ?regia_audience(courtesy, host, Regia_to__1); regia.send(Regia_to__1, signal, regia_local__courtesy__greeting);
      regia.act("walk_to", walk_to(door));
      regia.act("leave_hall", leave_hall);
      !regia_reach(take_leave, Regia_sender, Regia_pursuit).
```

`asl/playbooks/Serving.asl`:

```
@regia_plan__serving__1[regia_rank(serving, to(bring), 0)]
+!bring(Dish, Place)[source(Guest), regia_pursuit(Regia_pursuit)]
    : regia_is_given(serving) & regia_from_role(serving, patron, Guest)
   <- regia.trace(goal, info, "", [goal(fetch(Dish)), event(pursued)], Regia_pursuit__1); !fetch(Dish)[regia_pursuit(Regia_pursuit__1)];
      regia.act("walk_to", walk_to(Place));
      regia.act("put_down", put_down(Dish));
      regia.send(Guest, tell, served(Dish));
      !regia_reach(bring(Dish, Place), Guest, Regia_pursuit).

@regia_plan__serving__2[regia_rank(serving, to(fetch), 0)]
+!fetch(Dish)[source(Regia_sender), regia_pursuit(Regia_pursuit)]
    : regia_is_given(serving)
   <- regia.act("walk_to", walk_to(kitchen));
      if (not in_stock(Dish)) { .fail(regia_fail, regia_reason(sold_out(Dish))) };
      regia.act("pick_up", pick_up(Dish));
      !regia_reach(fetch(Dish), Regia_sender, Regia_pursuit).

@regia_plan__serving__3[regia_rank(serving, failed(bring), 0)]
+!regia_failed(bring(Dish, _), Guest, sold_out(Dish), _, _)
    : regia_is_given(serving) & regia_from_role(serving, patron, Guest)
   <- regia.send(Guest, signal, sold_out(Dish)).

@regia_plan__serving__4[regia_rank(serving, failed(bring), 1)]
+!regia_failed(bring(Dish, _), Guest, _, _, _)
    : regia_is_given(serving) & regia_from_role(serving, patron, Guest)
   <- regia.act("bow_to", bow_to(Guest)).

@regia_plan__serving__5[regia_rank(serving, when(idle), 0)]
+idle[source(_)]
    : regia_is_given(serving) & not .intend(bring(_, _))
   <- regia.act("walk_to", walk_to(kitchen)).
```

Their share of `asl/goals.asl`, one unguarded `-!g` per Goal:

```
-!take_seat
   <- regia.goal_failed(Regia_sender, Regia_pursuit, Regia_reason, Regia_because);
      !regia_failed(take_seat, Regia_sender, Regia_reason, Regia_pursuit, none);
      !regia_ended(take_seat, Regia_sender, Regia_pursuit, none);
      regia.pass_failure(Regia_reason, Regia_because).
```

The same goes for `take_leave`, `bring(Regia_arg__1, Regia_arg__2)` and `fetch(Regia_arg__1)`. Their share of `asl/unheard.asl` is one catch-all for `regia_local__courtesy__greeting`, the one Cue they `TELL`:

```
@regia_unheard__regia_local__courtesy__greeting[regia_unheard]
+regia_local__courtesy__greeting[source(S)] : S \== percept
   <- regia.trace(unheard, info, "T0702", [cue(regia_local__courtesy__greeting), sender(S)]).
```

### Teach-back

Not run: this ticket's grilling was on the spec, not on Rust. It is open for Edoardo: (a) why `regia.send` stays and `regia.pursue` went; (b) why `regia_reach` may be a subgoal and `regia.pass_failure` may not; (c) what would break if `regia.act` used `ConcurrentInternalAction`.
