# Generated ASL is Jason first

The Jason Target's generated plans had drifted from the Plans they come from. The Givings guard and the `FROM` tests were written out in every plan, and `TELL Role` took four steps. They had also come to lean on `regia-jason`: 29 internal actions, several of which only repeated what Jason's own stdlib already does. Generated ASL should read like the designer's Plan, and should stay plain Jason that a Jason programmer can follow without `regia-jason`'s documentation open.

We decided that generated and Infrastructure ASL use **Jason's language and stdlib first**. A recurring mechanic gets a name in `agent.asl` or `director.asl`: a **rule** for a test, an **Infrastructure plan** for steps that wait, fail or write the Trace. A `regia.*` internal action exists only when ASL can't do the job, for one of four reasons, which chapter 28 lists:

1. it leaves the agent with semantics the stdlib form lacks: the game link, a VEsNA body, the Trace file, a send that never fails its sender;
2. it needs the run-wide clock;
3. it reshapes intentions in ways the stdlib can't;
4. it hooks the reasoning cycle, in the agent class.

Applying the test retired `regia.pick`, `regia.pursue`, `regia.reached`, `regia.pursuing`, `regia.random`, `regia.deliver` and `regia.start_staging`, and the guards around `LEARN` and `FORGET`. The ticket's research note (`.scratch/transpiler/research/13-jason-native-facts.md`) holds the Jason facts behind each case. Those facts are also why `regia.send`, `regia.goal_failed` and `regia.pass_failure` stay.

## Considered options

- **Named internal actions for every pattern** (`regia.tell`, `regia.signal`): the shortest plans, but it means more Java, and a reader has to know `regia-jason` to follow a plan.
- **Everything written out in each plan**: no names to learn, but plans no longer read like the Plan, and a fix has to be made in every one.

## Consequences

- Infrastructure plans (`regia_reach`, `regia_choose`, `regia_draw`, `regia_update`) cost a reasoning cycle each where an internal action cost none. None of them is on a path that waits for it.
- Random draws come from **one generator per agent**, seeded from the run's seed and the agent's name, in place of one source per run. A case stays reproducible, and one agent's draws don't depend on how the others are scheduled.
- `regia.act` must suspend its intention the way `.wait` does, because `.intend` skips intentions that `.suspend` or `ConcurrentInternalAction` flag.
- `.create_agent` for Subplot Directors is to be confirmed on JaCaMo 1.3.1. If it fails there, `regia.start_staging` comes back under reason 4.
