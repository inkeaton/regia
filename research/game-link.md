# How Jason and VEsNA-Pro can share one game connection

Research for `.scratch/director-game-link/issues/01-sharing-one-connection.md`. It collects facts and decides nothing.

## Sources and versions

| Source | Version | Where |
| --- | --- | --- |
| Jason interpreter, source | 3.3.4 (`gradle.properties`) | `references/jason-main/jason-interpreter/src/main/java/jason/`, shortened to `jason/` below |
| Jason interpreter, bytecode | 3.2.1, the version JaCaMo 1.2 depends on | `~/.gradle/caches/.../jason-interpreter-3.2.1.jar` |
| *Programming Multi-Agent Systems in AgentSpeak using Jason* (Bordini, Hübner, Wooldridge, 2007) | 1st ed. | `references/*.pdf`, cited by printed page |
| VEsNA-Pro | `main` snapshot | `references/vesna-pro-main/`, shortened to `vesna/` below (`src/agt/vesna/`) |
| JaCaMo | 1.2 (VEsNA-Pro's `build.gradle`: `org.jacamo:jacamo:1.2`) | jar in the Gradle cache, read with `javap -c -l` |
| JaCa (CArtAgO bridge) | 3.1 (JaCaMo 1.2's pom) | jar in the Gradle cache, read with `javap -c -l` |
| Java-WebSocket | 1.5.6 (VEsNA-Pro's `build.gradle`) | jar in the Gradle cache, read with `javap -c -l` |

- Line numbers in `jason/` are from the 3.3.4 source. JaCaMo 1.2 runs Jason 3.2.1. The release notes from 3.2 to 3.3.3 (`references/jason-main/doc/release-notes.adoc:1-30`) list no change to environments, messages, actions or agent creation. I spot-checked the 3.2.1 jar for the methods this note relies on: `LocalAgArch.receiveMsg` (`offer` then `wakeUpSense`), `LocalEnvironment.actionExecuted` (the `getAg` null check), `LocalRuntimeServices.createAgent` (`setEnvInfraTier`), the `signal` case in `applyProcMsg`, and the fixed thread pool in `Environment`. They match.
- JaCaMo, JaCa and Java-WebSocket have no source on disk. Their citations give the **source line from the class's `LineNumberTable`** (`File.java:N`, as `javap -l` prints it), checked against the bytecode.
- I didn't go online. The local source and bytecode were enough for all six questions.

---

## 1. Jason's `Environment`: percepts

**Per agent.** `Environment` keeps one global list (`percepts`) and one list per agent name (`agPercepts: Map<String, List<Literal>>`) (`jason/environment/Environment.java:37-38`). `addPercept(String agName, Literal...)` adds to that agent's list only (`:252-266`). `getPercepts(agName)` returns the global list plus that agent's own list (`:127-157`). The book describes the same mechanism (pp. 103-106, Figs. 5.1-5.2, and the `addPercept(A,L)` list on p. 106: "only A will be able to perceive L").

**When an agent reads them.** On every reasoning cycle, in *sense*:

- `TransitionSystem.sense()` calls `ag.buf(getAgArch().perceive())` once every `nrcbp` cycles (`jason/asSemantics/TransitionSystem.java:1664-1679`). The default for `nrcbp` is 1 (`jason/runtime/Settings.java:21,29`), so every cycle.
- `LocalAgArch.perceive()` calls `infraEnv.getUserEnvironment().getPercepts(getAgName())`, and returns `null` when the agent has no environment (`jason/infra/local/LocalAgArch.java:343-350`).
- `getPercepts` returns **`null` when nothing changed** for that agent since its last call. It tracks this with `uptodateAgs` (`Environment.java:46,129-134`), and every `add/removePercept` takes the name out of that set (`:196,203,261,274`). `buf(null)` does nothing (`jason/asSemantics/Agent.java:836-838`).
- `addPercept` doesn't wake a sleeping agent. Only `informAgsEnvironmentChanged(agents...)` does that (`Environment.java:111-115`, then `jason/infra/local/LocalEnvironment.java:74-94` calls `wakeUpSense`). An idle agent sleeps 50 ms, and the wait grows by 100 ms per idle cycle up to `MAX_SLEEP` = 1000 ms (`LocalAgArch.java:293-314`). So a percept added without that call can wait up to about 1 s.

**Percepts are state.**

- The BUF, `Agent.buf`, compares the whole list it receives with the `source(percept)` beliefs. It **removes** every belief that is no longer in the list, which raises `-b[source(percept)]`, and **adds** every new one, which raises `+b[source(percept)]` (`Agent.java:821-938`; deletions at `:857-873`, additions at `:920-931`).
- A percept that is added and removed between two of an agent's perceive calls is **never seen** by that agent. The BUF only sees snapshots. The book says the same of global percepts: agents perceive L "if they sense the environment before L is removed" (p. 106).
- **`Environment` has no momentary event.** Its whole public API is percept lists, `scheduleAction` and `executeAction`, `informAgsEnvironmentChanged`, and the infra tier (`Environment.java:67-359`). Nothing in it raises an event without a belief, and nothing sends a message. `EnvironmentInfraTier` offers only `informAgsEnvironmentChanged`, `getRuntimeServices`, `isRunning` and `actionExecuted` (`jason/environment/EnvironmentInfraTier.java:9-25`). `RuntimeServices` has no send method (see §6).

**What Jason does have for momentary events**, outside `Environment`:

- A **message with performative `signal`** becomes a `TEType.signal` event, `+content[source(Sender), signal]`, and **no belief is added** (`TransitionSystem.java:358-362`). That fast path runs only when the agent is not in sync mode and has no user `kqml_received` plans (`:346`). Otherwise the default plan `@kqmlReceivedSignal` does the same thing through `.signal({+CA}, type_signal)` (`references/jason-main/jason-interpreter/src/main/resources/asl/kqmlPlans.asl:141-146`, `jason/stdlib/signal.java`). The source annotation is the **sender's name**, never `percept`.
- The internal action `.signal` adds an event directly (`jason/stdlib/signal.java`).
- An environment class can call any public Java API it can reach, for example `BaseLocalMAS.getRunner().getAg(name)` (`jason/infra/local/BaseLocalMAS.java:104`). That is the Local infrastructure, not part of the `Environment` contract. See §6 for what can be done with an agent's arch from outside.

## 2. Actions through an `Environment`

**The path.**

1. In *act*, the TS puts the action in the pending-actions map, `C.addPendingAction(action)`, keyed by intention id. This **suspends that intention only** (`TransitionSystem.java:1740`, `jason/asSemantics/Circumstance.java:651-663`).
2. The TS calls `getAgArch().act(action)` (`TransitionSystem.java:1742`). `LocalAgArch.act` passes it to `LocalEnvironment.act` (`LocalAgArch.java:404-417`), which calls `userEnv.scheduleAction(agName, actionTerm, action)` (`LocalEnvironment.java:59-63`).
3. The default `scheduleAction` submits a task to the environment's executor. The task calls `executeAction(agName, action)` and then `environmentInfraTier.actionExecuted(agName, action, success, infraData)` (`Environment.java:338-351`).
4. `LocalEnvironment.actionExecuted` sets the result on the `ActionExec` and calls `ag.actionExecuted(action)` (`LocalEnvironment.java:65-71`), which puts it in the feedback queue `FA` and wakes the agent (`jason/architecture/AgArch.java:183-186`, `Circumstance.java:632-641`).
5. In the agent's next `applyProcAct`, the intention goes back to running on success. On failure it gets a goal-deletion event with `action_failed` (`TransitionSystem.java:790-831`).

**A long-pending action.**

- **The agent isn't blocked.** Only the intention in `PA` waits. `canSleepAct` ignores `PA` (the `//&& !C.hasPendingAction()` comment, `TransitionSystem.java:1636-1639`), and other intentions keep running. The book says the same: "the reasoning cycle goes ahead … as if the executeAction method was invoked asynchronously" (p. 104).
- **The default executor is shared and small.** `new Environment()` makes a fixed pool of **4 threads** (`Environment.java:51-65`), shared by every agent of the MAS. If `executeAction` blocks while waiting, it holds a pool thread. A fifth concurrent blocking action, from any agent, then waits in the queue.
- **`scheduleAction` is public and can be overridden.** `infraData` is the `ActionExec` (`LocalEnvironment.java:61,66`), and `getEnvironmentInfraTier().actionExecuted(...)` is public on the interface (`EnvironmentInfraTier.java:25`). An environment can therefore store the request and answer it later from any thread, without holding a pool thread. Jason ships no class that does this. It is what the API allows.

**An intention dropped while its action is pending.**

- `Circumstance.dropIntention` calls `dropPendingAction`, which removes the entry from `PA` and calls `intentionDropped(i)` on every `CircumstanceListener` (`Circumstance.java:689-700, 895-915`).
- **The environment isn't told.** `executeAction` keeps running, and its result still reaches `FA`. When `applyProcAct` takes that feedback, `removePendingAction` returns `null` and the feedback is **silently discarded** (the comment says "it means that the intention was dropped and should not return to I", `TransitionSystem.java:804-830`).
- A listener on `intentionDropped` is the only hook that sees the drop. It is the same hook chapter 37 already plans to use for `regia_action_cancel`.

**The agent killed while its action is pending.**

- `.kill_agent` → `LocalRuntimeServices.killAgent` → `ag.stopAg()` and then `masRunner.delAg(agName)` (`jason/infra/local/LocalRuntimeServices.java:126-147`). Nothing touches `PA`, and nothing tells the environment.
- When the action ends, `LocalEnvironment.actionExecuted` looks the agent up by name and **drops the result if the agent is gone**, per the comment "the agent may was killed" (`LocalEnvironment.java:68-70`).
- **Names are reused.** `getNewAgentName` picks the first free `base`, `base_1`, `base_2`, … (`jason/infra/local/BaseRuntimeServices.java:29-35`), and a killed agent's name is free again after `delAg` (`BaseLocalMAS.java:92-102`). A late `actionExecuted` for a killed agent therefore reaches a new agent that has the same name. Intention ids are global (`static AtomicInteger idCount`, `jason/asSemantics/Intention.java:40,62`), so the new agent's `removePendingAction` finds no match and drops the result (`TransitionSystem.java:808`).

## 3. Agents created at runtime

**Same environment as the `.jcm` agents.**

- `.create_agent` calls `RuntimeServices.createAgent(name, source, agClass, archClasses, bbPars, settings, ts.getAg())`, passing **the creating agent as `father`**, and then `startAgent` (`jason/stdlib/create_agent.java:148-149`).
- `LocalRuntimeServices.createAgent` gives the new arch `agArch.setEnvInfraTier(masRunner.getEnvironmentInfraTier())` (`LocalRuntimeServices.java:80`). That is the **same `LocalEnvironment` object** the startup agents get (`jason/infra/local/RunLocalMAS.java:620`). So in plain Jason a runtime agent perceives and acts in the same `Environment`, under its own name.
- **Arch classes**:
  - The ones you pass, if any.
  - If you pass none and there is a `father`, the father's whole arch chain (`getAgArchClassesChain`).
  - Otherwise the registered default archs (`LocalRuntimeServices.java:53-62`, `AgArch.java:71-79`).
  - `createCustomArchs` skips `AgArch` and `LocalAgArch` in the list (`AgArch.java:96-116`).
- Under JaCaMo 1.2 the default archs are `jaca.CAgentArch` and `jacamo.infra.JaCaMoAgArch` (`JaCaMoRuntimeServices.java:13-18`, `registerDefaultAgArch` in the constructor). A runtime Director made by a `.jcm` agent through `createAgent(..., father)` gets the father's chain, which is the same JaCaMo chain.
- The new agent's name is the one `getNewAgentName` gives (`LocalRuntimeServices.java:75`, `BaseRuntimeServices.java:29-35`). A clash gets `_1`, `_2`, … Chapter 31's "adding a number" is accurate; the exact form is `<base>_<n>`.

**`.kill_agent`.**

1. `killAgent(agName, byAg, deadline)` asks the victim's `Agent.killAcc(byAg)` (`LocalRuntimeServices.java:129`).
2. With a deadline, it adds `+jag_shutting_down(D)` and sleeps D ms (`:131-139`).
3. `LocalAgArch.stopAg()`: `running = false`, wake, interrupt the agent's thread, `Agent.stopAg()` (BB `stop`, then **`destroy()` on every internal action the agent loaded**), and `stop()` on every arch in the chain (`LocalAgArch.java:137-150`, `Agent.java:229-253`). Under JaCaMo, `CAgentArch.stop()` closes the CArtAgO session (`CAgentArch.java:152-157`).
4. `masRunner.delAg(agName)` (`LocalRuntimeServices.java:142`).

**What a kill leaves behind.**

- **The `Environment` isn't told.** `agPercepts[agName]` and `uptodateAgs` keep the dead agent's entries. A later agent with the **same name** inherits its personal percepts. If the name is still in `uptodateAgs`, the new agent also gets `null` from `getPercepts` until something changes for that name (`Environment.java:127-134`). Calling `clearPercepts(agName)` clears both (`:317-325`).
- **`VesnaAgent` doesn't override `stopAg`**, so `.kill_agent` **doesn't close its `WsClient`**. Only VEsNA's own error path closes it (`vesna/VesnaAgent.java:187-208`, with no `stopAg` anywhere in the class).

## 4. Mixing an `Environment` with VEsNA bodies, and JaCaMo

**In plain Jason, they don't interfere.**

- The environment link lives in the **arch** (`LocalAgArch.perceive/act`, `LocalAgArch.java:343-350, 404-417`). It has nothing to do with the `Agent` subclass. `Agent.buf` only consumes what the arch returns.
- A VEsNA body is a private `WsClient` field opened in `VesnaAgent.initAg` (`vesna/VesnaAgent.java:39,45-96`). Its messages enter as `signal` messages to self through `ts.getAgArch().sendMsg` (`:99-106`), or as direct `addBel` calls (`:146-185`). They never touch the environment.
- So under a plain-Jason `.mas2j` with `environment:`, a `VesnaAgent` keeps its socket and also perceives the environment. A `regia.DirectorAgent` that extends `Agent` has the same arch and can use the environment just the same.

**JaCaMo 1.2 doesn't use Jason's `Environment` at all.**

- `JaCaMoLauncher.createEnvironment()` **overrides** `RunLocalMAS.createEnvironment()` without calling `super`. It only builds the CArtAgO platform (`new jacamo.platform.Cartago()`, `setJcmProject`, `init`) (`JaCaMoLauncher.java:354-362`). Jason's version, the only code that builds a `LocalEnvironment` from `project.getEnvClass()`, never runs (`RunLocalMAS.java:538-543`).
- So `BaseLocalMAS.env` stays `null` (`BaseLocalMAS.java:43,77-79`). Every agent gets `setEnvInfraTier(null)`, and `LocalAgArch.perceive` returns `null` (`LocalAgArch.java:346`).
- The `.jcm` grammar has **no environment keyword**. Its whole token list is `mas agent instances ag-arch ag-class ag-bb-class beliefs goals node host focus join roles in uses class-path asl-path java-path org-path platform debug package running workspace artifact focused-by agents organisation group responsible-for scheme players situated institution workspaces` (constant pool of `jacamo.project.parser.JaCaMoProjectParserConstants`).
- The environment in a JaCaMo project is **CArtAgO artifacts**. `jaca.CartagoEnvironment` extends Jason's `Environment`, but `Cartago.init` calls only its `init` (`jacamo/platform/Cartago.java:29-31`) and doesn't install it as a Jason user environment.
- **Percepts under JaCaMo.** `CAgentArch.perceive()` drains CArtAgO events (`fetchNextPercept`), turns them into beliefs and events itself, and then returns `super.perceive()` (`CAgentArch.java:474-501`). Further down the chain that is `LocalAgArch.perceive`, which is `null` under JaCaMo.
- **Actions under JaCaMo.** `CAgentArch.act()` routes every action to CArtAgO: a focused artifact's operation, or `doActionWithImplicitCtx`. On failure it calls `notifyActionFailure` with `env_failure`. It **never calls the next arch's `act`** (`CAgentArch.java:195-427`; the method has no call to `AgArch.act`). Chapter 37's rejected option says the same: such an action "finds no artifact".
- **What the JaCaMo API does offer**, without changing the launcher:
  - `platform: <class>` in the `.jcm`. `JaCaMoLauncher.createCustomPlatforms` instantiates any `jacamo.platform.Platform` (`init(String[])`, `start()`, `stop()`) by class name (`JaCaMoLauncher.java`, the `createCustomPlatforms` method; `jacamo/platform/Platform.java`). It is a hook for one-per-MAS Java code that starts with the MAS.
  - `LocalAgArch.setEnvInfraTier(LocalEnvironment)`, `new LocalEnvironment(ClassParameters, BaseLocalMAS)` and `LocalEnvironment.setUserEnvironment(Environment)` are all public (`LocalAgArch.java:184-186`, `LocalEnvironment.java:27-56`).
  - Even with an environment installed, though, actions under JaCaMo never reach it, because of `CAgentArch.act` above. Only perception would work.
  - Whether a supported JaCaMo configuration enables Jason's `Environment`: the 1.2 bytecode shows no such path. I didn't check later JaCaMo versions (the cache also holds `jacamo-1.3.1.jar`).

## 5. VEsNA-Pro's `WsClient`

**What it is.**

- `public class WsClient extends org.java_websocket.client.WebSocketClient` with a public constructor (`vesna/WsClient.java:12-22`).
- It holds **one** `WsClientMsgHandler`, and `setMsgHandler` replaces it (`:14,24-26`).
- `onMessage(String)` calls `msgHandler.handleMsg(message)`, and `onError` calls `handleError` (`:38-54`).
- `WsClientMsgHandler` is a public interface with `handleMsg(String)` and `handleError(Exception)` (`vesna/WsClientMsgHandler.java`).

**Threading** (Java-WebSocket 1.5.6):

- `connect()` starts **one read thread** named `WebSocketConnectReadThread-<id>` (`WebSocketClient.java:372-379`).
- `run()` reads the socket in a loop and decodes each frame on that thread (`WebSocketClient.run`, calling `WebSocketImpl.decode`). So **`onMessage`, and with it the handler, runs on that single thread, one message at a time, in arrival order.**
- `send` builds frames and calls `write(List)`, which is `synchronized` on `synchronizeWriteObject` (`WebSocketImpl.java:673-685, 755-760`). Concurrent `send` calls from several threads are therefore safe, and each message's frames are written together.

**How VEsNA hands messages to its owner.**

- `VesnaAgent.initBody` creates its own `WsClient` per agent from the `address`/`port` user parameters, and installs an anonymous handler that calls `myHandleMsg(msg)` and `myHandleError(e)` (`vesna/VesnaAgent.java:80-96`).
- **`myHandleMsg` runs on the WebSocket read thread.** It parses the envelope and reads `receiver`, then **ignores it** (`:108-113`). It then calls `sense()`, which sends a `signal` message to itself through `ts.getAgArch().sendMsg` (`:99-106, 132-144`), or calls `addBel`/`abolish` **directly from that thread** (`:146-185`).
- The `body` field is **private and has no getter**. `perform(String)` is public and calls `body.send` (`:39, 210-212`).
- `handleError` kills the agent, closing the body and stopping the `LocalAgArch` (`:187-208`).

**Can one `WsClient` serve several agents?**

- **Nothing in `WsClient` ties it to one agent.** One instance plus a handler that reads the envelope's `receiver` (or anything else) and calls into the right agent would work with the API as it stands. `send` is thread-safe, and delivery is serial on one thread.
- `VesnaAgent` can't *share* its own client, because the field is private and `initBody` always opens a fresh one per agent. A shared client would be a separate `WsClient` instance created by other code.
- **Error handling.** An `onError` on a shared client reaches its one handler. VEsNA's own handler would kill one agent (`:187-193`). A shared wrapper would have to choose what an error means for each agent.
- **Lifetime.** `.kill_agent` doesn't close a VEsNA body (§3). A shared client outlives every agent unless something closes it.

## 6. Delivering into a named agent from Java, on another thread

**Finding the agent.** `BaseLocalMAS.getRunner().getAg(name)` returns its `LocalAgArch`, or `null` (`BaseLocalMAS.java:104-106`). Under JaCaMo the runner is `JaCaMoLauncher`, a `RunLocalMAS` subclass.

| Way in | What it does | Thread-safety and waking | Order |
| --- | --- | --- | --- |
| `LocalAgArch.receiveMsg(Message)` | `mbox.offer(m)` and `wakeUpSense()` (`LocalAgArch.java:373-376`). It is exactly what `sendMsg` does for the receiver (`:353-371`), minus the clone and `MsgListener`s. | `mbox` is a `ConcurrentLinkedQueue` (`:66`). Wakes the agent. | **One FIFO per receiver** for every sender, whether agents (`.send` → `sendMsg` → `rec.receiveMsg`) or Java. Messages are taken in arrival order. Order from one sender is kept when that sender calls from one thread. |
| `AgArch.sendMsg(Message)` on some agent's arch | Sets `sender` if missing, looks up the receiver, calls `receiveMsg(clone)`, and notifies `MsgListener`s (`LocalAgArch.java:353-371`). Under JaCaMo, `CAgentArch.sendMsg` adds a Java-object fix-up and then calls `super` (`CAgentArch.java:756-762`). | As above. VEsNA uses it from the WS thread (`VesnaAgent.java:101-102`). | Same queue as above. |
| `Circumstance.addMsg(Message)` (`ts.getC().addMsg`) | `MB.offer(m)` (`Circumstance.java:314-316`). | `MB` is a `ConcurrentLinkedQueue` (`:86-96`). **Doesn't wake the agent**, which may sleep up to 1 s (§1). | It **skips the arch mailbox.** `checkMail` moves `mbox` into `C.MB` only during *sense* (`LocalAgArch.java:389-397`, `TransitionSystem.java:1678`). A message put straight into `C.MB` can **jump ahead** of earlier messages still waiting in `mbox`. |
| `Circumstance.addExternalEv(Trigger)` / `addEvent` | Puts an event in `E` (`Circumstance.java:126-140`). | `E` is a `ConcurrentLinkedQueue` (`:86-96`). **Doesn't wake.** | **No order relative to messages.** A message becomes an event only when `applyProcMsg` handles it. That handles **one message per sense step** (`TransitionSystem.java:177-185, 260-263`; `cyclesSense` defaults to 1, `LocalAgArch.java:485`). An event added directly can be selected before messages that arrived earlier. |
| `TransitionSystem.runAtBeginOfNextCycle(Runnable)` | Queues a task that **the agent's own thread** runs at the start of *deliberate*, then wakes the agent (`TransitionSystem.java:1641-1648, 1706-1715`). The comment says it is "used mostly to change the C only by the TS thread (e.g. by .wait)". | Concurrent queue, with a wake. The only way in documented as "change C from the TS thread". | Tasks run in FIFO order among themselves, at the start of *deliberate*. That is **after** that cycle's *sense*, which handles at most one message. Not ordered against messages. |
| `RuntimeServices` | No send or deliver method (`jason/runtime/RuntimeServices.java`). `runAsAgent(agName, code)` parses ASL and calls `C.addRunningIntention` **from the caller's thread**, then wakes the agent (`LocalRuntimeServices.java:211-245`). `loadASL` adds plans and beliefs. | `runAsAgent` changes `I` from a foreign thread. | A new intention. Not ordered against messages. |
| `Agent.addBel` from another thread | `brf` plus `ts.updateEvents` (`Agent.java:1096-1107`). VEsNA does this from the WS thread (`VesnaAgent.java:151, 181`). | No lock taken in `addBel`. Doesn't wake. | Not ordered against messages. |

**What a delivered message looks like to the agent.**

- `achieve`, `tell` and `signal` messages become `+!c[source(S)]`, `+c[source(S)]` and `+c[source(S), signal]`, where `S` is the message's `sender` (`TransitionSystem.java:346-366`). A sender equal to the receiver's name becomes `self` (`:341-343`).
- **`receiveMsg` doesn't check the `sender` field.** Code that builds the `Message` sets whatever sender it likes.
- `percept` is a forbidden agent name (`LocalAgArch.java:166-167`), but nothing stops a message from carrying `sender = "percept"`. Chapter 30's `source(percept)` annotation currently comes from `regia.perceive`, not from Jason. Whether a message with sender `percept` behaves well everywhere, for example in `.send` replies, is **not settled** by what I read.

**Ordering across ways in.** Only `receiveMsg`/`sendMsg` share a queue with agent-to-agent messages. Everything else (`C.addMsg`, `addExternalEv`, `runAtBeginOfNextCycle`, `runAsAgent`, `addBel`) is **unordered** with respect to messages from other agents. Within the Local infrastructure, Jason guarantees no order across different senders beyond "arrival into the receiver's `mbox`".

---

## Not settled by these sources

- Whether any JaCaMo version after 1.2 supports Jason's `Environment` (only the 1.2 bytecode was read).
- Whether `sender = "percept"` on an injected message is safe everywhere (§6).
- Whether `Agent.addBel` from a foreign thread is safe against the agent's own reasoning thread in every case. VEsNA does it. I didn't trace the BB's locking.
