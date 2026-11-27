# A Goal's life in Jason

How the Jason Target runs a Pursuit from its request to its ending (chapters 05, 08 and 11): the identity each Pursuit carries, how `REACHED`, `DROPPED`, `FAILED` and `ENDED` are raised and in what order, the generated `-!g` plan that carries a Failure and its Reason up the chain, the walker that a `DROP` and a Playbook taken away share, `PURSUING`, and the Trace entries along the way. Decided in the ticket *A Goal's life in ASL* (`.scratch/showcase-1-5/issues/13-goal-life-in-asl.md`), with the `Closing` argument and the closing intention from *A Playbook's opening and closing in ASL* (`.scratch/showcase-1-5/issues/16-opening-and-closing.md`), on the research note *How Jason behaves where the translation waits* (branch `research/jason-facts`, `research/jason-facts.md`, question 4 on `-!g` and question 5 on `.intend`). The Statements (`PURSUE`, `DROP`, `FAIL`, `PURSUING`) are written out in chapter 39's *Goals*. It builds on chapter 28's names and layout, chapter 32's precedence and chapter 35's Trace writer. Checked against Jason 3.3.4 (`references/jason-main/`) and 3.2.1, the version VEsNA-Pro pins (Regia runs on 3.3.2, chapter 28).

## What Jason gives, and what it doesn't

- A Pursuit is an achievement goal: `!g` (waiting) or `!!g` (its own intention), or an `achieve` message. Jason never joins two, so each `!g` is its own Pursuit, as chapter 05 requires.
- Jason has no `REACHED`, `DROPPED` or `ENDED` event, and its `-!g` is a rescue, not a notification: when a `-!g` plan finishes, the Body waiting on `g` carries on as if `g` had been reached. So every ending is raised by generated code, and the generated `-!g` fails again at its end.
- When a plan fails, Jason looks down the intention for the first goal with a relevant `-!` plan and posts that event, with the failure's annotations (the `error` ones, the code location, and every argument of `.fail(…)`) added to it (`TransitionSystem.generateGoalDeletion`, `findEventForFailure`).
- When a `-!g` plan fails itself, Jason skips `g` and looks further down for the next `-!` plan (`Intention.findEventForFailure`, the "failure in a fail plan" case). This is what carries a Failure up the chain.
- **A `-!g` plan whose context is false drops the whole intention** (research note, question 4, against the book). So the generated `-!g` has the context `true` and no guard.
- A plan whose trigger isn't a goal (a `WHEN` Plan on a Cue or a Fact) has no `-!` event. When it fails with no goal under it, Jason drops the intention with a console warning and nothing else.

## A Pursuit's identity

Every Pursuit carries **`regia_pursuit(Id)`** on its `+!g` event, where `Id` is the `seq` of its **`GOAL … PURSUED`** entry (chapter 34). That entry is written when the request is made, so a Pursuit that never starts a recipe has one too. Its `Id` is the `of` of every later `goal` entry of the Pursuit.

The annotation is stamped where the request enters the Agent:

| Request | Stamped by |
| --- | --- |
| The Agent's own `PURSUE g` or `PURSUE g, WITHOUT WAITING` | `regia.trace(goal, info, "", [goal(G), event(pursued)], Id)`, which binds `Id` to the entry's `seq`, then `!g[regia_pursuit(Id)]` or `!!g[regia_pursuit(Id)]` (chapter 39) |
| An `ASK` from an Agent, a Director's `ASK`, a Role setup's `PURSUE` (an `achieve` message) | `regia.RegiaAgent.socAcc`, which adds the annotation to the message's content before Jason posts it |
| A Director's `ASK EVERYONE` (`regia_everyone(achieve, G)`, chapter 30) | the Infrastructure plan that unwraps it, with `regia.trace(goal, info, "", [goal(G), event(pursued), sender(S)], Id)` and `!!G[source(S), regia_pursuit(Id)]` |

- **The Sender is Jason's own `source(S)`**: the asking Agent's or Director's name, or `self` for the Agent's own `PURSUE`. Nothing else is stored. The `PURSUED` entry records it (no Sender for `self`).
- `-!g` keeps every annotation of `+!g` (research note, question 4), so the generated `-!g` plan reads the Sender and the `Id` from its own event.
- A recipe binds both in its trigger: `+!fetch(Dish)[source(Regia_sender), regia_pursuit(Regia_pursuit)]`. A Plan with `FROM` writes its own variable in place of `Regia_sender` (chapter 39, *Who sent it*).

## The ending goals

The designer's ending Plans compile to plans for four generated goals, one per kind:

| Trigger | Generated goal |
| --- | --- |
| `WHEN g REACHED` | `+!regia_reached(G, Sender, Id, Closing)` |
| `WHEN g DROPPED` | `+!regia_dropped(G, Sender, Id, Closing)` |
| `WHEN g FAILED`, `WHEN g FAILED WITH r` | `+!regia_failed(G, Sender, Reason, Id, Closing)` |
| `WHEN g ENDED` | `+!regia_ended(G, Sender, Id, Closing)` |

- `G` is the Goal with its arguments, as the Trigger's pattern writes it. `Reason` is the Reason Cue, or `none` when the Failure has none.
- `Closing` is `none`, except on the `DROPPED` and `ENDED` endings a Playbook's take hands to its closing, which carry the closing's id (chapter 29, *The closing*). It lets a closing Playbook's own `DROPPED` and `ENDED` plans pass their guard for those endings and no others. `regia_reach`, the generated `-!g` and `regia.drop` always pass `none`; `REACHED` and `FAILED` carry it only so that the four kinds have one shape.
- **`FROM`** is tested on the `Sender` argument, with the same tests as a Trigger's `source(S)` (chapter 39, *Who sent it*). A plain `FAILED` writes `_` for the Reason.
- Each plan carries chapter 32's annotation with the Items **`reached(g)`, `dropped(g)`, `failed(g)` and `ended(g)`**, and the Givings guard of chapter 29, like any Playbook plan. The `DROPPED` and `ENDED` plans' guard also admits a closing of their Playbook named by `Closing` (chapter 29, *The guard*).
- **First match wins** among a Playbook's `FAILED` Plans (chapter 11) with no extra code. `FAILED WITH r` and the plain `FAILED` below it share the Item `failed(g)`, at `Pos` 0 and 1, and chapter 32's step 3 keeps the lowest `Pos` among the applicable ones. When the Reason doesn't match, only the plain one is applicable.
- **An ending with no Plan.** `agent.asl` holds one no-op plan per kind, annotated `regia_noop`, which `selectOption` chooses only when it is the only option (chapter 32, step 0). So an ending nobody listens to is never a goal failure.
- **An ending Plan that fails just stops** (chapter 05). `agent.asl` holds one `-!regia_<kind>(…)` plan per kind, context `true`, which writes the Plan's `failure` entry (*The cause entry*, below) and succeeds. Nothing else fires, and the Statements after the ending (`ENDED` after `FAILED`, the next level up) still run.

From `serving.regia:21` and `:23`:

```
@regia_plan__serving__3[regia_rank(serving, failed(bring), 0)]
+!regia_failed(bring(Dish, _), Guest, sold_out(Dish), _, _)
    : regia_is_given(serving) & regia_from_role(serving, patron, Guest)
   <- regia.send(Guest, signal, sold_out(Dish)).

@regia_plan__serving__4[regia_rank(serving, failed(bring), 1)]
+!regia_failed(bring(Dish, _), Guest, _, _, _)
    : regia_is_given(serving) & regia_from_role(serving, patron, Guest)
   <- regia.act("bow_to", bow_to(Guest)).
```

## `REACHED`

Every recipe plan (every `TO g` Plan, each `GIVEN` and `ELSE` of it) ends with **`!regia_reach(G, Sender, Id)`**, an Infrastructure plan of `agent.asl`. It:

1. writes `GOAL … REACHED` (`of: Id`);
2. starts **a new intention**, `!!regia_endings([regia_reached(G, Sender, Id, none), regia_ended(G, Sender, Id, none)])`, which runs the two in order.

Then the recipe's plan finishes, and the waiting Body carries on **at once**, as chapter 05 says (one reasoning cycle later than an internal action would allow, which no reader can see): by the time a `REACHED` Plan runs, the Body has already carried on. Nothing spreads from a reach, so there is no order between levels to keep.

`regia_endings` is an Infrastructure plan of `agent.asl`, which runs each listed goal as a subgoal in turn.

## `FAILED`: the generated `-!g`

The Transpiler emits **one `-!g` plan for every Goal of the Program** that a recipe, a `PURSUE` or an `ASK` names, Local Goals included, in a generated file **`asl/goals.asl`** that every Role file includes once, like `unheard.asl` (chapter 28). Its context is `true` and it has **no Givings guard**: a guard that failed would drop the whole intention, waiting Bodies of still-given Playbooks included. The designer's `FAILED` Plans keep their guard.

From `serving.regia:15`:

```
-!fetch(Regia_arg__1)
   <- regia.goal_failed(Regia_sender, Regia_pursuit, Regia_reason, Regia_because);
      !regia_failed(fetch(Regia_arg__1), Regia_sender, Regia_reason, Regia_pursuit, none);
      !regia_ended(fetch(Regia_arg__1), Regia_sender, Regia_pursuit, none);
      regia.pass_failure(Regia_reason, Regia_because).
```

1. **`regia.goal_failed`** reads the plan's own event (the `-!g` frame on top of the current intention), binds the Sender, the `Id`, the Reason (`none` if there is no `regia_reason`) and the `seq` of the chain's first entry, and writes the Trace:
   - the **cause entry**, if the event carries no `regia_because` (*The cause entry*, below), whose `seq` is then the chain's first;
   - the Pursuit's `GOAL … FAILED` `goal` entry, at level `error`, `of: Id`, `because:` the first (chapter 34, *The failure chain*).
   If the event has no `regia_pursuit`, which only a bypassed stamp would cause, it writes the missing `PURSUED` entry first.
2. **The ending Plans run in the failing intention**, `FAILED` then `ENDED`. Every Body above is already stopped, since nothing below the `-!g` frame runs again, so chapter 11's "the waiting Body has already failed" holds. Running them here, before passing the failure on, is what makes the chain fire **innermost first, each level complete before the next** (chapter 05): `fetch FAILED`, `fetch ENDED`, `bring FAILED`, `bring ENDED`.
3. **`regia.pass_failure`** looks at the frame below the failed `+!g`:
   - **a goal** (a waiting recipe, or a waiting ending Plan): it fails, with `.fail(regia_reason(R), regia_because(B))`, or just `regia_because(B)` when the Reason is `none`. Jason then posts the next `-!` below (*What Jason gives*), with those annotations on it.
   - **a `WHEN` Plan or an Infrastructure plan**, which has no `-!`: it writes that Plan's `PLAN … FAILED` `plan` entry, at level `error`, `because:` the first, and removes the intention quietly, so Jason prints no "Could not finish intention".
   - **nothing**: the failed Pursuit was the bottom of its intention (`!!g`, an `achieve` message). It succeeds, and the intention ends. Nothing waits on it, so the rescue Jason makes of a finished `-!g` changes nothing.

### Why `-!g` is written out

The four steps stay in each `-!g` plan, not in one shared Infrastructure plan. Jason posts a failure for the first frame from the top that has a relevant `-!` plan, and only a failure inside the `-!g` plan's own frame skips the failed `+!g` (research note of *Readable generated ASL*, *Failure walk*). A shared plan that failed would reach the `-!g` frame again and post the same `-!g`, with no end. So the step that fails, `regia.pass_failure`, has to be in the `-!g` plan itself.

The same walk is why the four **`-!regia_<kind>` catchers** of `agent.asl` are load-bearing: a failing `FAILED` or `ENDED` plan, run as a subgoal of the `-!g`, would otherwise reach the `-!g` frame and post it again. The catchers are found first.

`regia.pass_failure` can't be a plain `.fail` either. Over a `WHEN` Plan, a `.fail` leaves Jason with no failure event to post: it logs a warning and drops the intention. With the `+!g` at the bottom of its intention, a `.fail` probably posts the `-!g` again (research note of *Readable generated ASL*, *Failure walk*).

### No applicable `TO` Plan

A Pursuit no recipe takes (`T1104`): Jason finds no applicable `+!g` plan, sees the relevant `-!g` plan and posts `-!g[error(no_applicable), …]` (`generateGoalDeletionFromEvent`). That is the same generated plan, so the Pursuit fires `FAILED` and `ENDED` and passes the failure on like any other. Its `PURSUED` entry was written when the request was stamped, before any recipe was tried. From `courtesy.regia:9`: a Guest with no `seat` asked to `take_seat` writes `T1104`, `GOAL take_seat FAILED`, runs `WHEN take_seat FAILED` and `WHEN take_seat ENDED`, and the `achieve` intention ends.

### Reasons along the chain

- **`FAIL`** maps to `.fail(regia_fail)`, and **`FAIL WITH r`** to `.fail(regia_fail, regia_reason(r))` (chapter 39).
- Jason adds every `.fail` argument to the `-!g` event it posts. `regia.goal_failed` reads `regia_reason(R)`, and `regia.pass_failure` passes it on unchanged, so every Goal of the chain fails with the same Reason (chapter 11). Only `FAIL WITH` sets it.
- From `serving.regia:18`: `fetch(roast)` fails with `sold_out(roast)`. `-!fetch` writes `T1103` with `reason: sold_out(roast)` and `GOAL fetch(roast) FAILED`, finds no `FAILED` Plan of `fetch` (the `regia_noop` runs), and fails again. Jason skips `fetch` and posts `-!bring(roast, …)[regia_reason(sold_out(roast)), regia_because(57), …]`. Its `regia_failed` matches `@regia_plan__serving__3` at `Pos` 0, so the Servant tells the Guest `sold_out(roast)` and doesn't bow. Then `regia_ended`, and `bring` was the bottom of the `achieve` intention, which ends.

### The cause entry

Every Failure has **exactly one cause entry** (chapter 34, *The failure chain*), written once:

- **by the Statement**, when it knows its own cause and writes it before failing. It then fails with `regia_because(Seq)`: `UPDATE` (`T0801`, chapter 39), the reply intake of `regia.act` (`T1101`, chapter 37), and the other Statements that already write their code;
- **otherwise by the catcher** (the generated `-!g`, a `-!regia_<kind>`, or the Java hook for a `WHEN` Plan, below), from the event's annotations: `regia_fail` is `T1103`, with `reason` when there is one; `error(no_applicable)` is `T1104`; Jason's own errors (arithmetic, a failed internal action) map to the code of chapter 11's table. The `at` comes from Jason's `code_src` and `code_line` through the source map (chapter 35).

A catcher that finds `regia_because` writes no cause entry.

### A `WHEN` Plan that fails on its own

A `WHEN` Plan that fails with no Goal under it (`T0401` in `WHEN insulted`, or a `FAIL` there) has no `-!` event, and Jason drops its intention with a console warning. **`regia.RegiaAgent` catches this on the Java side** and writes the Plan's cause entry (*The cause entry*), so chapter 11's "a failed `WHEN` Plan just stops" still leaves its trace, and the console shows the Trace line, not Jason's warning. Which Jason hook it uses (a `CircumstanceListener`, or an override of the failure path through the Agent's `TransitionSystem`) is chosen when `regia-jason` is written. A `WHEN` Plan *waiting* on a Goal that fails is handled by `regia.pass_failure` (above), not by this hook.

## `DROPPED`: the walker

`DROP g` maps to **`regia.drop(G)`** (chapter 39). It follows chapter 08's four steps in Java:

1. **Find** every intention of the Agent holding a `+!g` frame that unifies with `G`, running, suspended (waiting in `regia.act` or `regia.wait`) or waiting for an event, and every pending `+!g` event that already has a `regia_pursuit`.
2. **Take each intention whole.** Every frame above the `+!g` frame is what it waits on, and every frame below waits on it, down to the intention's bottom, where a `!!`, a message or an event started it. So a `DROP` stops the whole intention (chapter 08's steps 1, 2 and 4). A frame that is itself another `+!g` is the same Pursuit's recursion or another Pursuit of `g`, and is dropped as a level like the others.
3. **Call off** a `DO` the intention is waiting on (chapter 37).
4. **Write the Trace**: each Pursuit of `g` writes `GOAL … DROPPED` with the `at` of the `DROP`; every other goal frame of the intention writes `GOAL … DROPPED` with `because:` that entry; a `WHEN` Plan at the bottom writes `plan … stopped` with the same `because` (chapter 34). All at `info`.
5. **Remove** the intention, the current one included when the `DROP` runs in one of them: the rest of that Body doesn't run.
6. **Start one new intention per intention removed**, `!!regia_endings([…])`, listing for each goal frame `regia_dropped(G, Sender, Id, none)` then `regia_ended(G, Sender, Id, none)`, from the top of the stack down: innermost first, each level complete before the next (chapter 05). Senders and `Id`s are read from the frames' triggers.

- Goals started `WITHOUT WAITING` are on intentions of their own, and are stopped only if they hold `+!g` themselves (chapter 08).
- `DROP g` when no Pursuit of `g` exists finds nothing and does nothing. No entry is written.
- From `dining.regia:21`: `hungry FORGOTTEN` during `WAIT 1 MINUTE, UNTIL on_plate(?)` removes the `have_dinner` intention, which was started `WITHOUT WAITING` and so has `have_dinner` at its bottom, writes `GOAL have_dinner DROPPED`, and runs `WHEN have_dinner DROPPED` (pushing the plate away) and `WHEN have_dinner ENDED` on a fresh intention.
- From `duelling.regia:49`: `DROP strike` runs in `WHEN yielded`, which holds no `strike`, so its Body carries on to `DO salute`.

**`regia.stop_playbook` (chapter 29) shares this walker.** It finds every intention holding a frame of the Playbooks taken, instead of a `+!g` frame, and takes each whole as step 2 does. Its entries are `because:` the take's `TAKE` entry, and in step 6 it hands the endings, carrying the closing's id as `Closing`, to the one closing intention of the take instead of starting intentions of its own (chapter 29, *Stopping P's Plans*).

**A closing intention is never removed** (chapter 29, *The closing*): if it were, its `REMOVED` steps would never run and its snapshot would stay. A `DROP` or another take that finds a frame in one takes only the frames above its `regia_close` frame, which is the step running now. Their endings go where that walk's endings go, and the closing carries on with its next step. A take of P skips the steps of a closing of P altogether: those are P's closing Plans, and they run to their end.

## `PURSUING`

`PURSUING g` maps to Jason's **`.intend`** (chapter 39). It holds for each Pursuit of a Goal unifying with `G` that has a recipe running: a `+!g` frame on any intention, running, suspended or waiting. Like any condition it can fill Placeholders, one unifier per Pursuit found, since `.intend` backtracks over every frame of every intention (research note of *Readable generated ASL*, *`.intend`*).

- In the Context and the Body of a `TO g` Plan, the Plan's own Pursuit is left out by its `Id`: `.intend(g[regia_pursuit(Regia_id__1)]) & Regia_id__1 \== Regia_pursuit`, so it never counts (chapter 05). The `Id` is in the trigger, so this is exact in a Context and in a Body alike. Testing the current intention instead wouldn't be: in a Context, `.intention(Me, _, _, current)` names last cycle's intention (research note, question 5).
- Everywhere else it is `.intend(g)`.
- `.intend` skips intentions flagged suspended, which only `.suspend` and `ConcurrentInternalAction` set. So `regia.wait` and `regia.act` suspend their intention the way Jason's `.wait` does, never through either (chapter 37), and a Pursuit waiting on a `DO` is still found.

From `dining.regia:17`: `NOT PURSUING have_dinner` in `WHEN hungry LEARNED` is `not .intend(have_dinner)`.

## Order and intentions, in one table

| Ending | Raised by | Runs on | Then |
| --- | --- | --- | --- |
| reached | `!regia_reach` at the end of the recipe | a new intention: `REACHED`, `ENDED` | the waiting Body carries on at once |
| failed | the generated `-!g` | the failing intention: `FAILED`, `ENDED` | `regia.pass_failure` fails the level below, or ends the intention |
| dropped | `regia.drop` | one new intention per one removed: `DROPPED`, `ENDED` for each level, innermost first | nothing: the levels are already stopped |
| dropped by a take | `regia.stop_playbook` | the take's one closing intention: `DROPPED`, `ENDED` for each level, intention after intention, then `REMOVED` (chapter 29) | the closing ends |

## Infrastructure state

No beliefs are added. A Pursuit's identity and Sender live only in its trigger's annotations.

## `regia-jason` additions

- `regia.RegiaAgent.socAcc`: stamps `regia_pursuit(Id)` on an incoming `achieve`, after writing its `PURSUED` entry with the message's sender.
- `regia.goal_failed(S, Id, R, B)` (reason 1: it writes the cause entry and the `FAILED` entry, and covers a missing stamp) and `regia.pass_failure(R, B)` (reason 3: plain `.fail` can't end the intention quietly, *Why `-!g` is written out*).
- `regia.drop(G)`, with the walker shared with `regia.stop_playbook` (reason 3).
- The hook in `regia.RegiaAgent` that writes the cause entry of a `WHEN` Plan failing on its own.
- In `agent.asl`: `regia_reach`, `regia_endings`, the four `regia_noop` plans and the four `-!regia_<kind>` catchers.
- `selectOption`'s step 0 also leaves out a `regia_noop` option unless it is the only one (chapter 32).

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025). 1.5 has no `BY` (chapter 05), so nothing is reported to an asker, and a Reason goes only up the Agent's own chain (chapter 11).

## Not decided here

- Reporting an ending to whoever asked (`BY`), with its Reason: later than 1.5. The ending goals already carry the `Id` and the Sender it would need.
- A Subplot's endings (`WHEN HonorDuel ENDED`), which use the same words but are a Director's: *Subplot arguments and endings in ASL* (`.scratch/showcase-1-5/issues/19-subplot-endings.md`).
- The fields of each Trace entry: chapter 34. Who writes the `plan` entry (the agent class, when it chooses the option): chapter 35.
