# Behaviour cases run against a scripted game over the real WebSocket

A behaviour case (spec 27) runs a Program without Godot and checks the Trace it leaves (spec 34). Something has to stand in for the game. We use **`ScriptedGame`**, a Java class in `regia-jason`'s `regia.testing` package. It is a real WebSocket server on the ports the `.jcm` gives, and speaks the same JSON envelopes `{sender, receiver, type, data}` that the game speaks to VEsNA bodies (spec 30, 33). The Root Director and every Agent run unchanged, with the same `.jcm`, the same `WsClient` bodies and the same message parsing, so a behaviour case tests the real API end to end.

`ScriptedGame` runs **in the same JVM** as the MAS, started by `regia.testing.RunCase` in test mode. A case's `>` steps must wait until the run has **settled**, and `WAIT` runs on a virtual clock. Both mean looking inside Jason (intentions, mailboxes, pending events, cycle boundaries under synchronous execution control), which only in-process code can do. It reuses Java-WebSocket's `WebSocketServer`, from the library VEsNA's `WsClient` already depends on.

`RunCase` only plays the `>` steps and writes the Trace. **Matching the Trace against the expected lines is done in Rust**, in the Transpiler's Conformance suite, after the run: it is pure logic over JSON Lines, and the Java side stays small.

## Considered Options

- **An in-memory fake in place of `WsClient`**, inside the JVM. Simpler, with no sockets or ports, but it skips the WebSocket and the JSON envelope, so it doesn't test the API the game will use.
- **A fake game in another process, in Python or Rust.** Just as real a protocol test, but it can't see inside Jason, so it can't detect settling or drive the virtual clock without a second control channel into the JVM.
- **Real wall time and sleeps between steps.** No test mode at all, but cases get slow and flaky, and a 30-second `WAIT` costs 30 seconds.

## Consequences

- `WAIT` compiles to `regia.wait(D)` instead of `.wait(D)` (spec 12, 35). It uses the wall clock in a normal run and the virtual clock in test mode. An intention paused in it counts as settled.
- Test mode writes a `script` Trace entry at every `>` step, so the Rust matcher can split the Trace into the stretches between steps.
- `ScriptedGame` fakes whatever answers the game gives, so it follows *Custom Actions through VEsNA*: whatever message carries an Action's result there is what it sends, success unless the case says otherwise.
- The Conformance suite needs a JVM and the `regia-jason` jar to run behaviour cases. Check cases don't.
