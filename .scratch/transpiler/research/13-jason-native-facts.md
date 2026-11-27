# Research note: Jason's native forms for Regia's mechanics

For the ticket *Readable generated ASL* (`../issues/13-readable-generated-asl.md`), on 2026-11-27. Read from the Jason source in `references/jason-main` (Jason 3.3.x). Paths are under `jason-interpreter/src/main/java/jason/`. Everything here was read from the code. None of it was run, and the points marked *unsure* need a test when `regia-jason` is written.

## 1. Failure walk, and a shared `-!g` plan

- When a plan fails, `TransitionSystem.generateGoalDeletion` (`asSemantics/TransitionSystem.java:1427`) calls `Intention.findEventForFailure` (`asSemantics/Intention.java:224`). That walks the frames from the top down and skips each goal that has no relevant `-!` plan (`Intention.java:247-255`). Nothing is popped. The `-!g` plan is pushed on top of the whole stack (`TransitionSystem.java:744`).
- Only when the failing frame's own trigger is `-!g` does the walk skip the frames whose literal unifies with `g` and land on the caller (`Intention.java:228-242`).
- **A shared plan loops.** If `-!fetch(A) <- !regia_goal_failed(fetch(A)).` posted a shared plan that then called `.fail`, the walk would find no `-!regia_goal_failed`, reach the `-!fetch` frame, and post `-!fetch` again, with no end.
- The same holds for a failing `!regia_failed` or `!regia_ended` inside `-!g`. The `-!regia_<kind>` catchers of `agent.asl` are what stop it, because the walk finds them first.
- **A plain `.fail` at the end of `-!g` isn't enough.** When the frame below `+!g` is a `+event` plan, the result is `"No failure event was generated"`, a warning, and the intention dropped (`TransitionSystem.java:1465-1466`). When `+!g` is the bottom of the intention, `-!g` is probably posted again (*unsure*: the inner loop can't step past the last frame).
- Failure events keep the `+!g` trigger's annotations (`Intention.java:244`, `:253`). `setDefaultFailureAnnots` adds `error`, `code_src`, `code_line` and `code` (`TransitionSystem.java:1550-1567`), and `.fail` adds its arguments (`stdlib/fail.java:70-75`). A plan trigger's annotations must be a subset of the event's (`asSyntax/Plan.java:242-250`). A tail variable, `[source(S)|As]`, binds the rest (`asSyntax/Pred.java:434-435`).

## 2. Subgoals

- `!g` posts an event and leaves the intention. The plan is chosen in a later cycle's deliberation (one event per cycle, `TransitionSystem.java:1706-1720`), so a subgoal costs at least one reasoning cycle more than an internal action. This is an estimate from the code; it wasn't measured.
- **A subgoal hands its bindings back.** When it finishes, ClrInt unifies the finished goal with the body step that posted it (`TransitionSystem.java:1179` onward, "unifies the final event with the body that called it"). So `!regia_choose(Ws, N)` binds `N` in the caller.

## 3. `for` over a rule

- `stdlib/foreach.java` is lazy: it calls `logicalConsequence` once and takes one solution per round.
- For `for (regia_each(m(D), on_plate(D)))` with `regia_each(T, F) :- .setof(T, F, L) & .member(T, L)`, `.setof` runs once (`asSyntax/LogExpr.java:87`, `stdlib/setof.java:98-102`). Later rounds come from `.member` walking the built list (`stdlib/member.java:118-121`), so the loop body's belief changes don't change the set.
- A formula passed as a bound variable is evaluated by `VarTerm.logicalConsequence` (`asSyntax/VarTerm.java:205-213`), and `D` reaches the loop body.

## 4. Sending

- `.send` takes a list of receivers and sends to each (`stdlib/send.java:185-188`). `[]` sends nothing and succeeds.
- **A receiver that doesn't exist fails the sender's plan.** `LocalAgArch.sendMsg` throws `ReceiverNotFoundException` (`infra/local/LocalAgArch.java:357-363`), which becomes a goal deletion (`TransitionSystem.java:978-981`). With a list, the loop stops at the first missing receiver: the ones before it got the message, the ones after it didn't.
- `.kill_agent` returns at once and kills on a new thread (`infra/local/LocalRuntimeServices.java:126-147`). So for a while the agent still shows in `.all_names` and still takes messages.
- `signal` is a valid illocutionary force. The receiver gets `+c[source(B), signal]` and no belief (`TransitionSystem.java:358-361`).
- `.signal({+c[source(S)]}, type_signal)` puts that same event in the agent's own queue and keeps a given source (`stdlib/signal.java`, `execute`).

## 5. `.intend`

- `.intend(g[regia_pursuit(Id)])` unifies with the `+!g` trigger of every frame of every intention, annotations as a subset, and backtracks over every match (`stdlib/intend.java`, `find()`). It covers E, PE, PA, PI and the running intentions (`asSemantics/Circumstance.java:729-889`).
- **It skips intentions flagged suspended.** Only `.suspend` and `ConcurrentInternalAction` set that flag (`stdlib/suspend.java`, `asSemantics/ConcurrentInternalAction.java:94`). `.wait` doesn't set it.

## 6. Random

- Each agent has one `java.util.Random`, held by its `.random` instance (`stdlib/random.java:45`). `.set_random_seed` and `math.random` both reach it through `set_random_seed.getAgRandomIA(ts)` (`stdlib/set_random_seed.java`, `functions/Random.java:33`). Java in an agent class reaches it the same way.
- `.random(L, X)` picks a random member of the list `L`.
- **`.shuffle` doesn't use it.** It calls `Collections.shuffle` (`stdlib/shuffle.java:80`), so generated code never uses `.shuffle`.

## 7. Beliefs

- `.abolish(f)` removes every belief that unifies with `f`. When nothing matches, it removes nothing and raises no event (`asSemantics/Agent.java:1129`).

## 8. Agents

- `.create_agent(Name, Source, [agentClass(C)])` accepts an agent class. With `Name` a variable, it picks a unique name from the variable's (`bob`, `bob_1`, …) and binds it (`stdlib/create_agent.java`). In local mode, the agent starts synchronously (`infra/local/LocalRuntimeServices.java:43-108`).
- *Unsure*: JaCaMo plugs in its own runtime services, and its source isn't in `references/`.
