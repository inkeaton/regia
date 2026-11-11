# The Trace in Jason

How the Jason Target writes the Trace of chapter 34: the writer, the source map that turns ASL back into designer names, the file and the console, and the test mode that runs behaviour cases. Decided in the ticket *Trace and logging* (`.scratch/regia-2/issues/40-trace-and-logging.md`). It builds on chapter 28's layout and on the Trace sources of chapters 29–33. Running behaviour cases against a scripted game is recorded in `docs/adr/0014-behaviour-cases-run-against-a-scripted-game.md`.

## The writer

Every Trace entry goes through **one writer** in `regia-jason`. The Jason Target runs every agent in one JVM (centralised infrastructure), so the writer is a single shared object. It hands out `seq` numbers in one order for the whole Program, and writes each entry to **both**:

- **the Trace file**, as one JSON object per line (JSON Lines), and
- **Jason's console**, as the console line of chapter 34, through **the writing agent's own logger** (`ts.getLogger()`), the channel `.print` uses. Lines show up under `[guard_1]` or `[regia_director__watch]` in the MAS console, mixed in with any `.print` a developer adds while debugging.

ASL code reaches it through the internal action **`regia.trace(Kind, Level, Code, Fields)`**. The `regia-jason` internal actions that already write Trace entries (`regia.stop_playbook`, `regia.send`, `selectOption`'s bypassed guard, and so on, chapters 29–33) call the writer directly.

| Kind | Written by |
| --- | --- |
| `run` | the writer itself, at start-up and shutdown |
| `action` | `regia.act` when it sends, and the reply intake of `regia.RegiaAgent` and `regia.DirectorAgent` when the outcome comes back (chapter 37) |
| `message` | `regia.send` (chapter 33), which every generated and Infrastructure send goes through |
| `plan` | a `regia.trace` call first in every generated plan Body for a designer's Plan |
| `goal` | `regia.trace` calls in the generated `+!`/`-!` plans and `DROPPED` events (chapter 11) |
| `fact` | `regia.trace` after each `REMEMBER`/`FORGET`/`CHANGE`, and in the Infrastructure plan that takes in a told Fact |
| `phase`, `staging`, `giving`, `cast` | the Infrastructure plans of chapters 29–33 that do these things |
| `failure` | the generated `-!g` plans (chapter 11), with `because` from the failure's root |
| `warning` | wherever chapters 09–33 say "a trace warning" |

- Generated control-flow plans (`regia_if__N`, `regia_either__N`) write no entries of their own; their failure is the designer's Plan's failure (chapter 11).
- `regia.trace` never fails. A writer error (a full disk, say) is reported once on the console and the run carries on.

## The source map

Jason's failure events carry the **ASL** location (`code_src`, `code_line`). To name designer items and `.regia` locations, every Build includes a **source map**, `asl/regia/sourcemap.json`, written by the Transpiler:

- ASL file and line → the `.regia` file, line and column of the Statement or Plan it came from;
- every Generated name (`regia_if__3`, `regia_director__watch`, `regia_when__insult`) → the designer item it stands for, or "fold away" for frames that never appear in the Trace.

The writer reads it once at start-up. Every entry's `at` and names go through it, so chapter 11's rule (Trace entries never show Generated names) is kept in one place, and the ASL stays free of location annotations.

## The file

- Each run writes **`traces/<YYYYMMDD-HHMMSS>.jsonl`** under the Build folder (`build/<entry>/traces/`). Runs are kept, so two runs of the same Build can be compared.
- The path is printed on the console when the run starts.
- The file always gets **every** entry. Nothing turns it off in 2.0.

## The console setting

A `TARGET JASON:` setting in Instancing (chapter 21) filters the console, never the file:

```regia
TARGET JASON:
    trace_console = warnings.
```

| Value | The console shows |
| --- | --- |
| `all` (default) | every entry |
| `warnings` | `warning` and `failure` entries only |
| `off` | nothing |

## Time

`WAIT d SECONDS.` compiles to **`regia.wait(D)`**, not `.wait(D)` (chapter 12). In a normal run it waits on the wall clock, exactly like `.wait`. In test mode it waits on the virtual clock. Dropping the intention during the wait removes it, as before.

## Test mode

Behaviour cases (chapter 34) run in **test mode**, launched by `regia.testing.RunCase`:

```
java -cp regia-jason.jar:… regia.testing.RunCase build/<entry> case.trace
```

1. `RunCase` starts **`ScriptedGame`**: a WebSocket server (Java-WebSocket's `WebSocketServer`) on every address and port the `.jcm` gives. It speaks the same JSON envelope `{sender, receiver, type, data}` and message types as the game (`regia_event`, `regia_fact`, `regia_join`, `regia_leave`, chapters 30 and 33, and `regia_action`, `regia_action_result` and `regia_story_ended`, chapter 37).
2. It starts the MAS from the Build's `.jcm`, in the same JVM, with **Jason's synchronous execution control**, so agents step in lockstep reasoning cycles, and with the case's **seed** given to every random source `regia-jason` controls: `EITHER`, Picks `AT RANDOM`, and `RANDOM` Propensity values (drawn by `regia.RegiaAgent`, chapter 36). Starting Agents are named `<kind>_<n>` (chapter 36). The Root Director and the Agents connect their bodies to `ScriptedGame` exactly as they would to Godot.
3. For each `>` step of the `.trace` file, it waits for the run to **settle**, plays the step through `ScriptedGame`, and writes a `script` entry.
4. **Settled** means: for every agent, no intention is running except ones paused in `regia.wait` or waiting in `regia.act` on an Action `ScriptedGame` holds, the mailbox and event queue are empty, and `ScriptedGame` has nothing left to send, for one whole cycle. If the run has settled and something is paused in `regia.wait`, the virtual clock jumps to the earliest wake-up instead of the next step.
5. `ScriptedGame` answers each Action with a single **`done`**, unless a standing rule (`> action fails`, `refused`, `holds`) matches it (chapter 37).
6. After the last step, and once the run has settled, `RunCase` writes `RUN ENDED`, stops the MAS and exits. The Trace file is the only output.

**Matching is done in Rust**, in the Transpiler's Conformance suite, which builds the case, runs `RunCase`, reads the `.jsonl` and applies chapter 34's matching. `RunCase` itself never reads the expected lines.

- Starting Agents have bodies, as in a real run, so `ScriptedGame` serves the ports the `.jcm` assigns them as well.
- Random sources inside Jason or VEsNA-Pro that `regia-jason` can't seed (such as `.random`) are not used by generated code. If one turns out to matter, it's a gap for the development effort to close.

## `regia-jason` additions

- The Trace writer, and the internal actions `regia.trace(Kind, Level, Code, Fields)` and `regia.wait(D)`.
- The `regia.testing` package: `RunCase` and `ScriptedGame`.
- Reading `asl/regia/sourcemap.json`.

## Transpiler checks

**Warnings**

- An unknown value for `trace_console` (as for any unknown key in a known Target's group, chapter 21).

## Not decided here

- Numbering the Jason Target's Trace codes in chapters 28–37: *Number the checks and add exemplar cases*.
