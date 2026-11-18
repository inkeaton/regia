# How Jason behaves where the translation waits

Research for `.scratch/showcase-1-5/issues/10-jason-facts.md`, the six questions in group A of `.scratch/showcase-1-5/jason-open-questions.md`.

## Sources and versions

- **Jason source**: `references/jason-main/`, version **3.3.4** (`gradle.properties:1`, `jasonVersion=3.3.4`). Paths below are under `jason-interpreter/src/main/java/jason/` unless they say otherwise.
- **The Jason that VEsNA-Pro actually runs**: `references/vesna-pro-main/build.gradle:12` depends on `org.jacamo:jacamo:1.2`, whose POM (in the local Gradle cache) pins `io.github.jason-lang:jason-interpreter:3.2.1`. So the source is newer than the runtime. For each finding below I checked that 3.2.1 behaves the same way, either by reading its bytecode or by running it.
- **Experiments**: small `.mas2j` programs run on the 3.2.1 jar (`jason.infra.local.RunLocalMAS`). They were scratch files and aren't committed. Their key output lines are quoted under each answer.
- **The book**: Bordini, Hübner, Wooldridge, *Programming Multi-Agent Systems in AgentSpeak using Jason* (2007). Page numbers are the printed ones; add 21 to get the PDF page. The book describes Jason 0.9/1.0, and in places the current code works differently. Those places are pointed out.
- **VEsNA-Pro**: `references/vesna-pro-main/src/agt/vesna/`. It matches the copy in `vesna-pro-main/` at the repo root except for `.DS_Store` files.

No online source was needed.

---

## 1. A known belief told again from a new source

**Yes, Jason generates `+wronged(x,y)` again, but the event carries only the new source: `+wronged(x,y)[source(c)]`.** A second `tell` from a source the agent already has (`b` again) generates nothing.

- A received `tell` with a literal content goes straight to `Agent.addBel`, unless the agent has its own `kqml_received` plans (`asSemantics/TransitionSystem.java:341-353`). Otherwise the default plan `++NS::CA` does the same thing (`src/main/resources/asl/kqmlPlans.asl:12-18`). Either way it ends in `brf` → `BeliefBase.add`.
- `DefaultBeliefBase.add` (`bb/DefaultBeliefBase.java:144-166`): if the belief is already in the base (`contains`, which ignores annotations), only the annotations are merged in with `importAnnots`. It returns `true` only when at least one annotation is new.
- `Pred.importAnnots` (`asSyntax/Pred.java:274-289`) also **removes from the incoming literal every annotation that was already present** ("p will only contain the annots actually added (for Event)"). The literal that reaches the event therefore holds only `source(c)`.
- `brf` returns that literal as the addition (`asSemantics/Agent.java:1033-1038`), and `updateEvents` turns each addition into a `+b` event (`asSemantics/TransitionSystem.java:1381-1392`). If `add` returns `false` (same source again), `brf` returns `null` and no event is made (`Agent.java:1095-1106`).
- Book p. 156: `add` "returns true if the belief was added. If the belief is already there, it returns false. If the belief given as a parameter is in the BB except for (some of) the annotations, only those annotations are included." Book p. 61: "an event is generated only in the case where that message is not already in the belief base". The formal rule for Tell (book p. 216) always adds `+b[id]` to the events, so it is looser than the code.

**Can a plan's context see whether the belief was held before?** Not directly. The belief base is updated before the event is even queued, so by the time the context runs the belief is `wronged(x,y)[source(b),source(c)]`. Jason keeps no "before" state. What the context *can* see:

- the trigger's own annotation, which is only the new one(s): `+wronged(X,Y)[source(S)]` binds `S = c`;
- every source now held: `.findall(Src, wronged(X,Y)[source(Src)], L)` gives `[b,c]`.

So "was it held before" can be written as "is it held from a source other than the one in the trigger": `wronged(X,Y)[source(O)] & O \== S`. That holds only if each source is added once and nothing removes sources between the update and the plan running. Jason doesn't guarantee it, so the source doesn't settle this exactly. Note also that a first-time belief from a new source and a re-told belief raise the same event shape. Only the extra sources tell them apart.

Experiment (b tells, c tells, b tells again):

```
[a] Q1 event +wronged(x,y)[source(b)] sources now [b]
[a] Q1 event +wronged(x,y)[source(c)] sources now [b,c]
```

(no third line for b's repeated tell)

## 2. An `[atomic]` intention that suspends

**While the atomic intention is suspended, no other intention runs and no event is selected.** The mailbox is still read. When the suspension ends, the atomic intention resumes and keeps running atomically.

- An intention suspended in `.wait` (pending intention, `addPendingIntention`) or on an environment action (pending action, `addPendingAction`) stays registered as *the* atomic intention, with `atomicIntSuspended = true` (`asSemantics/Circumstance.java:470-474`, `:651-656`).
- **Events:** `applySelEv` selects nothing while any atomic intention exists, suspended or not (`asSemantics/TransitionSystem.java:396-401`).
- **Intentions:** `applySelInt` selects the atomic one if it isn't suspended. If it is suspended, the guard `!C.isAtomicIntentionSuspended()` stops any other intention from being selected (`TransitionSystem.java:836-853`; `Circumstance.java:418-437`). So other intentions don't run.
- **Mailbox:** `sense()` still calls `checkMail()` and `applyProcMsg()` every cycle (`TransitionSystem.java:1664-1698`), and the agent wakes up for messages even when the atomic intention is suspended (`canSleep`, `TransitionSystem.java:1619-1620`). Each cycle, a message is handled as follows:
  - a `tell` of a literal goes into the belief base **at once** (the `addBel` shortcut, `TransitionSystem.java:353-357`), and its `+b` event is queued;
  - an `achieve`, or any message when the agent has its own `kqml_received` plans, only becomes a queued event (`TransitionSystem.java:347-351`, `:368-376`). With the default `kqmlPlans.asl`, the `tell` shortcut applies;
  - a reply to a pending `askOne` resumes the waiting intention directly (`TransitionSystem.java:280-334`).

  Queued events are handled only after the atomic plan ends.
- **Resuming:** `.wait` registers a `CircumstanceListener` and checks its condition on `eventAdded`, i.e. when an event is *queued*, not when it is selected (`stdlib/wait.java:176`, `:254-266`; `Circumstance.addEvent` notifies listeners, `Circumstance.java:132-142`). Time-outs come from a scheduler (`wait.java:191-195`). On resume, `removePendingIntention` clears `atomicIntSuspended` (`Circumstance.java:484-490`), and `resumeIntention` puts the intention back as the atomic one (`Circumstance.java:354-357`, `:371-378`; `wait.java:223` lets atomic intentions through explicitly). So `.wait(ms)`, `.wait({+b})` and `.wait(cond)` all resume inside an atomic plan, as long as the awaited event is *queued* by something other than a plan.

**For a custom internal action that suspends until a message** (`regia.act`, `regia.wait`): it resumes only if Java code resumes it, such as a listener on `eventAdded`, the `ask` reply path, an action-feedback callback, or a scheduler. **If the resume depends on an ASL plan running (for example a `+done(...)` plan that calls `.resume`), it never comes while the atomic intention is suspended. The agent deadlocks until a time-out, if there is one.** VEsNA-Pro sends game events to the agent itself as `signal` messages (`VesnaAgent.java:99-106`, `:132-138`). `applyProcMsg` queues these as `+…` signal events at once (`TransitionSystem.java:358-363`), and that is enough to wake a `.wait`-style listener.

Book p. 98 (the `atomic` annotation): the intention "will be selected for execution in the subsequent reasoning cycles until that plan is finished … the interpreter does not even call the intention selection function". The book doesn't cover suspension.

Experiment: a ticker intention printing every 100 ms, and an `[atomic]` plan that does `.wait(250)`, `.wait(1000)`, then `.wait({+msg2}, 3000, T)`. Meanwhile `b` sends `tell msg1`, `achieve hello`, and later `tell msg2`:

```
[a] ATOMIC start (time wait 1000)
[b] b sends tell msg1 + achieve hello
[a] ATOMIC after time wait; msg1 believed? msg1
[a] ATOMIC now waiting for {+msg2}
[b] b sends tell msg2
[a] ATOMIC resumed after 549 ms; end
[a] tick 1
[a] plan for +msg1 ran
[a] plan for achieve hello ran
[a] plan for +msg2 ran
[a] tick 2 …
```

The ticker never ran during roughly 2 s of suspension. `+msg2` ended the wait. The plans for `+msg1`, `!hello` and `+msg2` ran only after the atomic plan finished.

## 3. Variables in `for`

**Yes, every binding made inside the loop body is undone between rounds, and again after the loop.** Only the bindings that existed before the `for` survive, plus each round's solution of the formula.

- `stdlib/foreach.java`: on the first call it saves a copy of the unifier (`:146`, "backup original unifier") and builds the solutions lazily from `un.clone()` (`:135`). Each round does `un.clear(); un.compose(iu.next())` (`:154-160`), and every solution extends the *pre-loop* unifier, so whatever the previous round bound is gone. After the last round it puts the saved pre-loop unifier back (`:166`). Javadoc, `:57`: "The unification resulted from the evaluation of the logical formula is used only inside the loop, i.e., the unification after the for is the same as before."
- The 3.2.1 bytecode has the same `clone`/`clear`/`compose` sequence.
- One consequence: a loop can't build a result in a variable. An accumulator has to go through beliefs, or be done with `.findall`, `.concat` and the like outside the loop. The solutions are lazy, so for a formula over beliefs, changes to the belief base during the loop can affect later rounds. `.member(m(X), L)` over a fixed list isn't affected.
- The book (2007) predates `for` and says nothing about it.

Experiment `for (.member(m(X),[m(1),m(2),m(3)])) { .print(Y); Y = X*10; .print(Y) }; .print(Y, X)`:

```
[a] Q3 X=1 Y-before=Y<no-value>
[a] Q3 Y-after=10
[a] Q3 X=2 Y-before=Y<no-value>
…
[a] Q3 after loop Y=Y<no-value> X=X<no-value>
```

## 4. The `-!g` event

**Annotations.** The `-!g` literal is built from the failed goal's `+!g` trigger as it was *received*, so it keeps the original annotations, including `source(S)` from an `achieve`. Jason then adds the error annotations:

- The intended means' trigger is the selected event's trigger with the unifier applied (`asSemantics/TransitionSystem.java:719`; `IntendedMeans.java` constructor, `trigger = te.capply(unif)`). The failure event copies it with the operator flipped to `-` (`Intention.java:244`, `:257`; `TransitionSystem.java:1431-1436`).
- `setDefaultFailureAnnots` (`TransitionSystem.java:1550-1568`) adds:
  - `error(Id)` and `error_msg("…")` (`JasonException.java:93-97`). Ids seen in the code: `ia_failed` (an IA returned false, `:955`), `internal_action` (an IA threw, e.g. `.fail(...)` with arguments, `JasonException.java:19-20`), `action_failed` plus the action's failure reason (`:820-823`), `no_relevant`/`no_applicable` (subgoal without a plan, `:554-563`), `wait_timeout` (`.wait` time-out, `stdlib/wait.java:231`), `ask_failed`, and `unknown` when none is given;
  - `code(Step)`: the body step that failed, with variables made anonymous;
  - `code_src("file")` and `code_line(N)` (`asSyntax/Literal.java:595-610`).
- **Carrying a Reason.** `.fail(T1, …, Tn)` turns each argument into an annotation of the `-!g` event, and `error_msg(M)` sets the message (`stdlib/fail.java:54-75`, then through `JasonException.getErrorTerms`). So `.fail(reason(R))` gives `-!g[…, reason(R)]`, which a plan matches with `-!g[reason(R)]`.
- **But `.fail_goal(g)` from another intention adds no annotations at all, not even `source`.** It builds the `-!g` from the goal literal it was given (`stdlib/fail_goal.java:113-117`; the hook `addAnnotsToFailEvent` is empty, `:134-135`). Experiment: `-!g(N)[source(S)|A]` was not applicable to the event `-!g(1)` raised by `.fail_goal(g(1))`, and `.fail_goal(h(2)[reason(r)])` didn't match the running goal `h(2)` at all, so nothing was dropped. A Reason can't travel on `.fail_goal`. It has to go some other way, such as a belief.

Experiment (`b` sends `achieve g4`, and `+!g4` runs `.fail(reason(boom), error_msg("my msg"))`):

```
[a] Q4a -!g4 from b annots [code(.fail(reason(boom),error_msg("my msg"))),code_line(9),code_src("file:a.asl"),error(internal_action),error_msg("my msg"),reason(boom)]
```

**Which `-!g` is raised, and what happens without an applicable plan.** Three cases:

1. **No relevant `-!g` plan at all.** When `g` fails, Jason walks down the intention stack, looking for the nearest goal that has *some* candidate `-!` plan with the same functor and arity (`Intention.java:244-261`; `PlanLibrary.hasCandidatePlan`, `pl/PlanLibrary.java:391-396`). The failure annotations go on *that* event. If no goal on the stack qualifies, the whole intention is dropped with the warning "No failure event was generated" (`TransitionSystem.java:1462-1466`; `Intention.fail` does nothing, `Intention.java:221-222`, so the intention simply isn't put back).
2. **A candidate `-!g` plan exists but none is applicable** (its context is false, or its annotations don't unify). The `-!g` event has already been queued. When it is selected, `applyRelApplPlRule2` → `generateGoalDeletionFromEvent` finds that it is not a goal *addition*. It logs "Could not finish intention" and drops the intention. **The failure does not propagate to goals further down**, even if they have applicable `-!` plans (`TransitionSystem.java:554-563`, `:1483-1531`). Experiment: `!q4 → !g4b`, where `+!g4b <- .fail`, `-!g4b : .my_name(nobody)` (not applicable), and an applicable `-!q4` exists. Result: "Could not finish intention" and "Found a goal for which there is no applicable plan: -!g4b[code(.fail),code_line(14),code_src(…),error(ia_failed),error_msg(""),source(self)]". The `-!q4` plan never ran. The book (p. 90) says the failure "propagates to the goals below" when the `-!g1` plan isn't applicable. In 3.2.1 and 3.3.4 that is true only when no `-!g1` plan is relevant (case 1), not when one is relevant but inapplicable.
3. **An applicable `-!g` plan exists.** It runs on top of the failed `+!g` intended means. When it finishes, both are popped and the parent plan **carries on after `!g` as if `g` had succeeded** (book p. 89; `TransitionSystem.java:1220-1240`). Experiment: "Q4c reason r(1)", then "Q4c parent continues after -!g4c handled".

A failure *inside* a `-!g` plan does not raise `-!g` again. The search starts below that goal (`Intention.java:228-242`; book p. 89, footnote 3).

## 5. Telling a desire apart from the current intention

**`.intend(G, I)` and `.desire(G, I)` can each bind the id of the intention that holds the goal, and `.intention(Me, _, _, current)` binds the current intention's id. In a plan *body*, `.intend(g, I) & I \== Me` therefore tests "pursued by another intention".** In a plan *context* this is not reliable. Details:

- `.intend(G[, I])` (`stdlib/intend.java:98-157`) succeeds for each intention with a `+!G` intended means in its stack, and binds `I` to that intention's id. It looks at every intention: running, in events, pending (waiting in `.wait` or on an action), and the selected one (`Circumstance.getAllIntentions`, `Circumstance.java:729-…`). It skips only intentions suspended by `.suspend` (`intend.java:148`, `considerSuspended = false`).
- `.desire(G[, I])` (`stdlib/desire.java:81-185`) is `.intend` (with `.suspend`ed intentions included) **plus** any `+!G` event not yet intended: the selected event, the event queue, and pending events. For an event from `!!g`, or from an `achieve` from another agent, the event has no intention, and `I` is **left unbound** (`desire.java` `testEvent`: `if (i == null || intID == null) return solution`). So an `I \== Me` test passes trivially there.
- `.intention(Id, State, Stack, current)` (`stdlib/intention.java:91-113`) uses the *selected intention* `C.SI`. If that is null, it uses the selected event's intention. In a body `C.SI` is the right one. **In a context, `C.SI` still holds the intention selected in the previous reasoning cycle**: it is cleared only at the start of `act()` (`Circumstance.java:114-118`), and the context is evaluated earlier, in `deliberate()`. So in a context "current" is whichever intention ran last, not necessarily the one that posted the event. The javadoc (`intention.java:61-62`) says otherwise.
- **The goal being handled isn't on any stack yet while its context is evaluated.** The intended means is pushed only after selection (`TransitionSystem.java:719`). So in the context of a `+!g` plan, `.intend(g)` doesn't see this Pursuit, while `.desire(g)` *does* see it (the selected event is checked first, `desire.java:114-122`).

Experiment (two `!!p5(_)` intentions, plus the posting intention 7):

```
[a] Q5 p5(1) me=8 others pursuing p5: [9]          <- body: .intention(Me,_,_,current) & .intend(p5(_),I) & I \== Me
[a] Q5 p5(2) me=9 others pursuing p5: [8]
[a] Q5 me=7 intend p5 in [9,8]                     <- intentions waiting in .wait are included
[a] Q5ctx(no intend in ctx) in-context current=7 body current=10 desire(q5ctx) id=DI<no-value>
[a] Q5ctx(no intend in ctx) in-context current=7 body current=7 desire(q5ctx) id=7
```

On the fourth line, `!!q5ctx` was posted by intention 7 and runs as intention 10. In the context, "current" was 7 (stale), `.desire` matched the event itself with `DI` unbound, and `.intend(q5ctx)` was false (the plan variant with it in the context never ran). The fifth line is the same plan reached as a subgoal of intention 7, where the stale value happens to be right.

**Recommendation from the facts:** do the "pursued by another intention" test in the body, or have the context compare against something stable. For `PURSUING g` inside a `TO g` Plan, the current Pursuit's own `+!g` is either not on a stack yet (in a context) or is the current intention (in a body). The body test `.intention(Me,_,_,current) & .intend(g, I) & I \== Me` is the exact one. `.intend` leaves out goals that are only queued as events (`!!g` not yet picked up). `.desire` includes them, but can't give their intention id. The source doesn't settle how Regia should count a queued, not-yet-started Pursuit.

## 6. VEsNA-Pro's `Temper` and Moods

All references are to `references/vesna-pro-main/src/agt/vesna/Temper.java` unless they say otherwise.

**Ranges.**
- A trait marked `[mood]` in the agent's `temper(...)` setting must start in **[-1, 1]**. A trait without `[mood]` is a personality trait and must be in **[0, 1]**. Anything else throws `IllegalArgumentException` (`:61-70`). So a negative starting Mood is accepted, and the code allows [-1, 1] for Moods. The readme's example has `prop3(-0.5)[mood]` (`readme.md:23`). Chapter 14's note that "Regia follows the code, [0, 1]" is right for personality traits, not for Moods.
- A `temper([...])` annotation's target value must be in **[-1, 1]** for every trait (`:107-109`). The error message there says "[0, 1]", which is wrong. A trait in the annotation that the agent doesn't have is skipped (`:99-100`).
- An `effects([...])` value must be in **[-1, 1]** (`:249-251`). The message says "[-100,100]", also wrong.

**What a negative value does.**
- `most_similar`: each plan's score is `Σ |agentValue − targetValue|` over the traits it names, and the lowest score wins (`:112-113`, `:227-237`). Negative values are just points on the scale, and the distance works as expected.
- `random`: the weight is `Σ agentValue × targetValue` (`:110-111`). A negative product *lowers* the weight. But `getWeightedRandomIdx` (`:207-225`) is broken for negative and fractional weights. It accumulates in an `int currentMin`, so fractions are truncated. A negative weight can never satisfy `roll > currentMin && roll < w + currentMin`. When no interval matches, it falls back to index 0. And if all weights are 0 (min bound = max bound = 0), `Random.nextDouble(0.0, 0.0)` throws `IllegalArgumentException`. In short, `random` doesn't work as designed when weights are fractional or negative. That's a VEsNA-Pro bug, not a semantics to translate to.
- Clamping when an effect is applied (`:252-257`): above 1 it is set to 1.0, but **below -1 it is set to 0.0, not -1.0**. That is a bug, so a Mood driven past -1 jumps to neutral.

**When `effects` are applied.** Only inside `Temper.selectIntention` (`:173-175`), and only for the label of the **top** intended means of the intention selected (`selected.peek().getPlan()`; `IntentionWrapper.java:15-17`). `VesnaAgent.selectIntention` calls it only when the agent has a temper, more than one intention is runnable, and at least one of them has a `temper(...)` annotation on its top plan (`VesnaAgent.java:228-236`). As a result:
- the effects are **not** applied when a plan is chosen (`selectOption`, `VesnaAgent.java:217-225`, never touches the Mood);
- they are applied **every time** that intention is selected through this path, i.e. once per body step that runs while other intentions compete. A long plan applies its effects many times, and a plan that runs alone applies them **never**;
- an `[atomic]` intention never goes through `selectIntention` (`TransitionSystem.java:837-841`), so its effects are never applied;
- the effects belong to whatever plan is on top of the stack. During a subgoal they are the subplan's effects, not the parent's.

An effect on a trait that is personality and not marked `[mood]` throws (`:243-244`). An effect on an unknown trait is ignored (`:245-246`).

**A public method for `regia.shift`.** **There is none.** `mood` is a `private Map<String, Double>` (`:39`), and the only code that writes to it, `updateDynTemper`, is `private` (`:239`). Nothing else is exposed: `Temper`'s public methods are the constructor, `computeWeight`, `hasOptionsAnnotation`, `hasIntentionsAnnotation`, `selectOption`, `selectIntention` and `select`. `VesnaAgent.temper` is also `private`, with no getter (`VesnaAgent.java:40`, `:238-240`). A `regia.shift` would need a change to VEsNA-Pro: a public getter on `VesnaAgent`, and a public `shift(String mood, double delta)` on `Temper` (that could reuse and fix `updateDynTemper`'s clamping). Without that change, the only way in would be reflection.

**Other things the translation will hit:**
- `strategy` must be given. If it is missing, the constructor sets the default and then calls `strategy.equals(...)` on null (`:79-81`), which throws a `NullPointerException`. The only accepted values are `most_similar` and `random` (`:81-86`). The readme's `nearest` (`readme.md:13`, `:32`) throws "Decision Strategy Unknown".
- In `selectOption`, a `NoValueException` makes it return `null` (`:153-157`). Jason treats that as no option, i.e. `no_option` failure (`TransitionSystem.java:629-632`).

---

## Short answers

1. **Re-told belief:** a `tell` from a new source raises `+wronged(x,y)[source(c)]`, with only the new annotation. The same source again raises nothing. The context sees the belief after the merge (`[source(b),source(c)]`), so "held before" is only approximated by "has a source other than the trigger's".
2. **Atomic plus suspend:** no other intention runs and no event is selected, but messages are still read (`tell` updates the belief base at once, and its plan waits). The intention resumes if Java code (a `.wait` listener, scheduler, `ask` reply, or action feedback) resumes it. A resume that depends on an ASL plan deadlocks.
3. **`for`:** every round starts from the pre-loop unifier plus that round's solution. Bindings made in the body are lost between rounds and after the loop.
4. **`-!g`:** keeps the original `+!g` annotations (`source(S)`), plus `error`, `error_msg`, `code`, `code_src` and `code_line`, plus every argument of `.fail(...)`. That is how a Reason can travel. `.fail_goal` adds none, not even `source`. A relevant but inapplicable `-!g` drops the whole intention without propagating. With no relevant `-!g`, the failure goes to the nearest goal below that has one.
5. **Another intention:** in a body, `.intention(Me,_,_,current) & .intend(g,I) & I \== Me`. `.desire` also counts queued `+!g` events but can't give their intention id. In a context, `current` is stale and the goal being handled isn't intended yet.
6. **Temper:** Mood starting values, annotation targets and effects are all in [-1, 1] (personality traits in [0, 1]). A negative value works for `most_similar` but breaks `random`'s weighted pick. Clamping below -1 sets the Mood to 0 (a bug). Effects are applied on *intention* selection, only when several intentions compete, once per selected step. There is no public method to shift a Mood.
