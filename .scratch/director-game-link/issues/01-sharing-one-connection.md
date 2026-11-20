# How Jason and VEsNA can share one game connection

Type: research
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by:

## Question

Find the facts that *The game link's shape* depends on:

1. **Jason's `Environment`.** How an `Environment` subclass delivers percepts to one agent and not another (`addPercept(agName, …)`, `getPercepts(agName)`), and when an agent reads them (each reasoning cycle? only on change?). Whether percepts are kept as state (beliefs added and removed by the BUF) or can be momentary, like a Cue: can an environment raise a `signal`-like event with no belief, or put a message in one agent's mailbox?
2. **Actions through an `Environment`.** How `executeAction` and `scheduleAction`/`actionExecuted` work, whether an action can stay pending for a long time without blocking the agent's other intentions or other agents, and what happens to a pending action when its intention is dropped or its agent is killed.
3. **Agents created at runtime.** Whether an agent made by `createAgent`/`.create_agent` (as `regia.start_staging` does, chapter 31) is attached to the MAS's environment like the `.jcm`'s agents, and what happens at `.kill_agent`.
4. **Mixing.** Whether a MAS can have an `Environment` while its Agents keep VEsNA-Pro WebSocket bodies, and whether a `regia.DirectorAgent` that isn't a `VesnaAgent` can use it. Whether JaCaMo/CArtAgO (VEsNA-Pro runs on JaCaMo) changes any answer: does a JaCaMo project use Jason's `Environment` at all, or artifacts?
5. **VEsNA-Pro's `WsClient`.** Whether one `WsClient` can be shared by several agents in one JVM: its threading, how it hands incoming messages to its owner (`myHandleMsg`), and whether a wrapper can sort them to several agents.
6. **Delivery from Java into an agent.** The supported ways for Java code outside an agent to put an event or a message in a given agent (by name) from another thread: `RuntimeServices`, `Agent.getTS().getC().addMsg`, `addExternalEv`, and how each keeps order relative to messages that agent receives from other agents.

Read the local sources first: Jason's source in `references/jason-main/` (the interpreter is `jason-interpreter/`), the Jason book in `references/`, and VEsNA-Pro in `references/vesna-pro-main/`. Go online (Jason and JaCaMo docs) only for what they don't settle, and note the version of each source. Cite file and line for each answer. Write the findings to a research note and link it here.

Done when each of the six questions has a sourced answer, or says plainly that the source doesn't settle it.

## Comments
Research ran on throwaway branch `research/game-link` (file `research/game-link.md`, commit `47835d0`), pushed and never merged. Sources: Jason 3.3.4 source (spot-checked against the 3.2.1 jar that JaCaMo 1.2 runs), the Jason book pp. 103–106, VEsNA-Pro `main`, and the JaCaMo 1.2 / JaCa 3.1 / Java-WebSocket 1.5.6 jars (read with `javap -l`).

## Resolution

1. **Percepts.** `addPercept(agName, …)` is per agent and read every reasoning cycle. Percepts are **state** (beliefs added and removed from a snapshot), so a percept added and removed between two reads is never seen. `Environment` has no momentary event and can't message an agent: only a message with the `signal` performative gives an event with no belief. `addPercept` doesn't wake a sleeping agent.
2. **Actions.** A pending action suspends only its own intention. The default `scheduleAction` blocks one of four threads shared by the whole MAS. An override can call `actionExecuted` later, from any thread. A dropped intention isn't reported to the environment (only a circumstance listener sees it), and a late result for a dropped intention or a killed agent is discarded.
3. **Runtime agents.** `.create_agent` agents get the same environment as `.jcm` agents (and, under JaCaMo, the CArtAgO arch chain). `.kill_agent` doesn't tell the `Environment`, whose percepts for that name stay behind for a later agent that reuses the name. `VesnaAgent` has no `stopAg`, so killing it doesn't close its WebSocket.
4. **Mixing.** In plain Jason the environment hangs off the architecture, so any agent class can use it. **JaCaMo 1.2 never creates a Jason `Environment`**, and its `CAgentArch.act` sends every action to CArtAgO. Under JaCaMo, a Jason `Environment` is a dead end. The `.jcm`'s `platform: <class>` is the one hook for code that runs for the whole MAS.
5. **`WsClient`.** One read thread, in-order delivery, a single replaceable handler, and a synchronized `send`. Nothing ties it to one agent, so **one client with a dispatcher on `receiver` works as the API stands**. `VesnaAgent` can't share its own (private field). An error on a shared client reaches its one handler, and VEsNA's own handler kills the agent.
6. **Delivering from Java.** `LocalAgArch.receiveMsg` (agent found by `BaseLocalMAS.getRunner().getAg(name)`) is the only entry point that shares the agent's mailbox with messages from other agents, so it keeps arrival order, and it wakes the agent. `C.addMsg` can overtake earlier messages and doesn't wake the agent. `addExternalEv` has no ordering with messages. `runAtBeginOfNextCycle` changes agent state on the agent's own thread. `receiveMsg` doesn't check `sender`, so the link can set it (for example to `percept`).

**Still open:** whether JaCaMo after 1.2 supports a Jason `Environment`; whether an injected message with sender `percept` is safe everywhere; whether `addBel` from another thread is safe (VEsNA does it, but the locking wasn't traced).
