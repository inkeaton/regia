# The Trace in Jason

How the Jason Target writes the Trace of chapter 34: the writer, the source map that turns ASL back into designer names, the file and the console, and the test mode that runs behaviour cases. Decided in the ticket *Trace and logging* (`.scratch/regia-2/issues/40-trace-and-logging.md`). It builds on chapter 28's layout and on the Trace sources of chapters 29–33. Running behaviour cases against a scripted game is recorded in `docs/adr/0014-behaviour-cases-run-against-a-scripted-game.md`. How `ScriptedGame` plays the game's side of the game link, its state replies and `> lose link`, in the ticket *ScriptedGame and the Trace on the game link* (`.scratch/director-game-link/issues/06-scripted-game-and-the-trace.md`). The `regia.trace` call's fields, the `plan` entry written at selection, the Staging numbers and `sourcemap.json`, in *The Trace's fields and entries* (`.scratch/showcase-1-5/issues/22-trace-pieces.md`).

## The writer

Every Trace entry goes through **one writer** in `regia-jason`. The Jason Target runs every agent in one JVM (centralised infrastructure), so the writer is a single shared object. It hands out `seq` numbers in one order for the whole Program, and writes each entry to **both**:

- **the Trace file**, as one JSON object per line (JSON Lines), and
- **Jason's console**, as the console line of chapter 34, through a logger named with the entry's `agent`, so lines show up under `[guard_1]`, `[director:Watch]` or `[director:HonorDuel#2]`, the one name chapter 34 gives each Director, never under a Generated name such as `regia_director__watch`. They are mixed in with any `.print` a developer adds while debugging, which still shows under the Jason agent's own name.

ASL code reaches it through the internal action **`regia.trace(Kind, Level, Code, Fields)`**, or **`regia.trace(Kind, Level, Code, Fields, Seq)`**, which also binds `Seq` to the entry's `seq` (a `PURSUE` takes its Pursuit's `Id` this way, chapter 39). The `regia-jason` internal actions that already write Trace entries (`regia.stop_playbook`, `regia.send`, `selectOption`'s bypassed guard, and so on, chapters 29–33) call the writer directly.

- `Code` is a string, `""` when the entry has none. `Fields` is a list of `key(Value)` terms, with chapter 34's field names for the kind: `regia.trace(unheard, info, "T3801", [cue(ready), sender(S), plot(royalBanquet), phase(Ph)])`. Java callers pass the same keys.
- The writer adds `seq`, `t`, `agent`, `kind`, `level` and `code`. It turns atoms and structures into their Regia text, lists into arrays and numbers into numbers, and every Generated name into its designer name through the source map.
- **`at` comes from the caller's frame**: the ASL file and line of the instruction running on the current intention, through the source map's `lines`. A frame the source map doesn't map (an Infrastructure plan) gives the `at` of the nearest mapped frame below it, which is the Statement that posted it: `T0801` from `regia_update`, `T1502` from `regia_draw` and `REACHED` from `regia_reach` point at the `UPDATE`, the `TELL` and the recipe. An intention with no mapped frame gives no `at`.
- **`agent`** is the source map's name for the Jason agent. A Subplot Director's `#<n>` is added by the writer (*Staging numbers*, below).

| Kind | Written by |
| --- | --- |
| `run` | the writer itself: `RUN STARTED` at start-up; `RUN ENDED` when the Root ends the story (`regia.end_story`, chapter 37), or from a JVM shutdown hook, `how: stopped`, if the run stops first (Ctrl-C, or the MAS is closed). In test mode, `RunCase` (below) |
| `action` | `regia.act` when it sends, and the reply intake of `regia.RegiaAgent` and `regia.DirectorAgent` when the outcome comes back; the game link for a detached Director's call-offs and late outcomes, and for Actions failed when it is lost (chapter 37) |
| `time` | `regia.wait` when a `WAIT … UNTIL` ends, met or timed out (chapter 39); the game link for `CLOCK PAUSED` and `CLOCK RESUMED` (chapter 37) |
| `message` | `regia.send` (chapter 33), which every generated and Infrastructure send goes through: a `TELL`, an `ASK`, a `SIGNAL` (one entry for the Statement, listing every Director it went to, and in `ended` those whose Staging had ended, which `regia.send` finds when the delivery fails: `info`, not `T3303`), and a setup's `LEARN` and `PURSUE` sent by the Director (chapter 30) |
| `plan` | `RegiaAgent.selectOption` and `DirectorAgent.selectOption`, when they choose the option (*The `plan` entry*, below); a stopped one by the walker and `regia.stop_playbook` (chapters 29 and 40), a failed one by `regia.pass_failure` (chapter 40) |
| `goal` | `regia.trace` for a `PURSUE` and `RegiaAgent.socAcc` (`PURSUED`), `regia_reach`, `regia.goal_failed` in the generated `-!g` (`FAILED`, at `error`), and the drop walker (chapter 40) |
| `fact` | `regia.trace` after each `LEARN`/`FORGET`/`UPDATE`, in the Infrastructure plan that takes in a told Fact, in the Java intake of a game Fact, Agents' and Directors' alike, and, for a Director's starting game Facts, in `regia_begin` (chapter 30) |
| `phase`, `staging`, `cast` | the Infrastructure plans of chapters 30–33 that do these things. `regia_begin` writes `STAGING … STARTED`, then the initial `phase` entry, then the starting game Facts, before the setups (chapter 30) |
| `giving` | the receiving Agent: `regia_give` and `regia_restore` write `GIVE`, each take step and `regia_set_aside` write `TAKE`, one entry per Giving (chapter 29) |
| `failure` | the cause entry only: the Statement that knows its cause, else the catcher (the generated `-!g`, the `-!regia_<kind>` catchers of ending Plans, and `RegiaAgent`'s hook for a `WHEN` Plan failing on its own), chapter 40 |
| `warning` | wherever chapters 09–33 say "a trace warning" |
| `unheard` | the `regia_unheard` catch-all plans of a Director (chapter 30) and of an Agent for a told Cue (chapter 39), the dispatchers' failure plans and the Quota check (chapter 33) |
| `mood` | `regia.shift` for the Statement, and `RegiaAgent.selectOption` when it applies a `SHIFTS` Label (chapters 14 and 32) |
| `count` | the Quota check (chapter 33) |

- Generated helper plans write no entries of their own, and their failure is the designer's Plan's failure (chapter 11). A Failure's cause entry is written exactly once (chapter 40, *The cause entry*). Jason emits no control-flow plans: `IF`, `RANDOMLY` and `FOR EACH` stay inside the Plan's body (chapter 39).
- `regia.trace` never fails. A writer error (a full disk, say) is reported once on the console and the run carries on.

### The `plan` entry

A designer's Plan writes its `plan` entry **when it is chosen**, not from its Body. Only the agent class sees the rivals, so `by`, `over` and `fits` are known there and nowhere else, and a `SHIFTS` Label's `mood` entries, written in the same call, come after the entry they belong to.

- `RegiaAgent.selectOption` writes it at step 6 of chapter 32, and `DirectorAgent.selectOption` after its `[Level, Pos]` comparison. Each does so for any chosen option whose plan label is in the source map's `plans`, contested or not, since Jason calls `selectOption` for every event once it is overridden.
- `block` and `at` come from `plans`. `values` comes from the option's unifier, after the trigger and the Context are unified, read through that plan's `vars`.
- Generated plan Bodies hold no `regia.trace(plan, …)` call (chapters 39 and 40).

### Staging numbers

A Subplot Director's Jason name is only unique (chapter 31), and no agent reads `#<n>` or `ALSO IN`. They exist only in the Trace, so **the writer** works them out from the entries it has already written, and from nothing else:

- When it writes a Director's first entry, its `STAGING … STARTED`, it gives that Director the next number for its Plot in this run, and from then on names it `director:<Plot>#<n>` in every entry, on the console too.
- For each Agent of that cast, `also_in` lists the numbers of the Stagings of the same Plot that have a `STARTED` entry naming it and no `ENDED` entry yet, and of which it hasn't `LEFT`.

These are names for the output, worked out from the output. The writer holds no Program state (chapter 28, *the game link*).

## The source map

Jason's failure events carry the **ASL** location (`code_src`, `code_line`). To name designer items and `.regia` locations, every Build includes a **source map**, `asl/regia/sourcemap.json`, written by the Transpiler. It is one JSON object with three maps:

```json
{
  "lines": { "agents/noble.asl": { "41": "playbooks/dining.regia:62:9" } },
  "names": { "regia_director__royalBanquet": "director:RoyalBanquet",
             "regia_director__honorDuel": "director:HonorDuel",
             "regia_when__insult": null },
  "plans": { "regia_plan__dining__6": { "owner": "Dining", "trigger": "WHEN served(?dish), FROM waiter",
                                 "given": "sated", "at": "playbooks/dining.regia:62:9",
                                 "vars": { "Dish": "?dish" } } }
}
```

- **`lines`**: each ASL file, and each of its lines that comes from a Statement or a Plan → the `.regia` file, line and column: 1-based lines and character columns, as the CLI shows them (chapter 23, *Positions*). Every map is sorted by key, so a Build is the same bytes every time.
- **`names`**: every Generated name → the designer name it stands for, or `null` to fold it away (frames that never appear in the Trace). A Subplot Director's name has no number here: the writer adds it.
- **`plans`**: every plan label of a designer's Block → the Block as a `plan` entry names it (`owner`, `trigger`, `given` or `else`), its `at`, and the map from the plan's ASL variables to its Placeholders.

The writer reads it once at start-up. Nothing in it changes at run time. Every entry's `at` and names go through it, so chapter 11's rule (Trace entries never show Generated names) is kept in one place, and the ASL stays free of location annotations.

## The file

- Each run writes **`traces/<YYYYMMDD-HHMMSS>.jsonl`** under the Build folder (`build/<Entry path>/traces/`). Runs are kept, so two runs of the same Build can be compared.
- The path is printed on the console when the run starts.
- The file always gets **every** entry. Nothing turns it off in 2.0.

## The console

`regia run --console <level>` (chapter 23) filters the console, never the file. How much the console shows changes nothing in the run, so it is not a Target setting and isn't in the Build: `regia run` passes it to the JVM as the system property `regia.trace_console`, which the Trace writer reads at start-up.

| Value | The console shows |
| --- | --- |
| `all` (default) | every entry |
| `warnings` | `warning` and `failure` entries only |
| `off` | nothing |

## Starting a run

`regia run <entry>` (chapter 23) builds, then starts the MAS from the Build's `.jcm` with the `regia-jason` jar the CLI carries and, after it, every jar in the Project's `lib/` folder (chapter 28), so the writer never writes a class path. It gives the run's seed (`--seed`, else the Build's `SEED`, else one it picks) to `regia-jason` as the system property `regia.seed`, from which every agent seeds its own generator (*Random draws*, below), and the console level as `regia.trace_console`. The `run` entry records the seed (chapter 34). The game connects as it always does.

`regia test` (chapter 23) runs behaviour cases through `RunCase`, below, and matches their Traces.

## Time

`WAIT d SECONDS` compiles to **`regia.wait(D)`**, not `.wait(D)`, and `WAIT … UNTIL` to `regia.wait(Cond[, D])` (chapters 12 and 39). In a normal run it waits on the wall clock, exactly like `.wait`. In test mode it waits on the virtual clock. Dropping the intention during the wait removes it, as before.

## Test mode

Behaviour cases (chapter 34) run in **test mode**, launched by `regia.testing.RunCase`:

```
java -cp regia-jason.jar:lib/*:… regia.testing.RunCase build/<Entry path> case.trace
```

`regia test` puts the Project's `lib/` jars on the class path as `regia run` does, so a case runs the project's own Java (dotted Actions) for real (chapter 37, *Test mode*).

1. `RunCase` starts **`ScriptedGame`**: a WebSocket server (Java-WebSocket's `WebSocketServer`) on every address and port the `.jcm` gives. It speaks the same JSON envelope `{sender, receiver, type, data}` and message types as the game (chapter 37's table). It tells the connections apart **by port**: the port of the `.jcm`'s `platform: regia.GameLink(address, base_port)` line is the game link's (chapter 28), and every other port is the body of the Agent the `.jcm` gives it. It never looks at `sender` to tell them apart. With `#! game link: none` (chapter 34), it doesn't serve the link's port, so the link writes `T2802` at start.
2. It starts the MAS from the Build's `.jcm`, in the same JVM, with **Jason's synchronous execution control**, so agents step in lockstep reasoning cycles, and with the case's **seed** given to `regia-jason`, from which every agent seeds its own generator. Every draw chapter 34 lists comes from the drawing agent's generator (*Random draws*, below). Agents have chapter 34's names, which chapter 36 gives the Jason agents. The game link and the Agents' bodies connect to `ScriptedGame` exactly as they would to Godot.
3. For each `>` step of the `.trace` file, it waits for the run to **settle**, plays the step through `ScriptedGame`, and writes a `script` entry.
   - A `cue` or `fact` step to an Agent goes out as one `regia_cue` or `regia_fact`, on the WebSocket of the body the step names, with `receiver` set to that body. Its `name` is the item's External name, which `ScriptedGame` reads from that receiver's `regia_game` beliefs (chapter 28). If the receiver has no entry for the item, the Regia name is sent as it is, and the receiver writes `T2801`.
   - A `link` step goes out once on the link's connection, with `receiver: "regia_game_link"`. Its External name comes from the `regia_game` beliefs of the Build's Director files (`asl/directors/`, Subplots' included); if none lists the item, the Regia name is sent. The link delivers it to every attached Director that hears it, and drops it with no entry if none does (chapter 30).
   - A `*` step sends one message to each body whose `regia_game` beliefs list the item, in Trace order, then one on the link if any Director file lists it, all before the run is next checked for settling. The `script` entry lists the receivers reached, `link` last.
   - A receiver with no connected body (an Agent the run never had, or one that has left), and a `link` step (or a `*` step that would reach the link) after `> lose link` or under `#! game link: none`, is a case error. `RunCase` sends nothing, writes `RUN ENDED`, stops the MAS, and exits with a non-zero status naming the step. The Conformance suite fails the case without matching it.
   - `> lose link` closes the link's connection from `ScriptedGame`'s side. The link writes `T2803` and fails what it has in flight (chapter 37).
4. **Settled** means: for every agent, no intention is running except ones paused in `regia.wait` or waiting in `regia.act` on an Action `ScriptedGame` holds, the mailbox and event queue are empty, `ScriptedGame` has nothing left to send, and nothing it sent is still on its way on any connection, the link's included, for one whole cycle. A Director waiting for its state reply needs no rule of its own: `ScriptedGame` answers every `regia_state` at once (*The game's state*, below), so it is never settled while one is unanswered. If the run has settled and something is paused in `regia.wait`, the virtual clock jumps to the earliest wake-up instead of the next step.
5. `ScriptedGame` answers each Action with a single **`done`**, unless a standing rule (`> action fails`, `refused`, `holds`) matches it (chapter 37).
6. After the last step, and once the run has settled, `RunCase` writes `RUN ENDED`, stops the MAS and exits. The Trace file is the only output.

### The game's state

`ScriptedGame` answers each `regia_state` (chapter 37) at once, in order with everything else it sends, from the smallest record a game would keep:

- **Facts**: the instances that `link` steps (and `*` steps that reached the link) have made true and not since made false. `fact` steps to Agents' bodies don't count: they say what one body perceives. `> fact link +…` steps written before `> start` set the record without sending anything, so the Root's reply carries them.
- **Left**: every Agent named by a `> leave` step.

A case can't hold a state reply or send a second one, so `T3305` and `T3703`, which only a misbehaving game causes, aren't scriptable.

**Matching is done in Rust**, in the Transpiler's Conformance suite, which builds the case, runs `RunCase`, reads the `.jsonl` and applies chapter 34's matching. `RunCase` itself never reads the expected lines.

- Starting Agents have bodies, as in a real run, so `ScriptedGame` serves the ports the `.jcm` assigns them, as well as the link's.

### Random draws

- **One generator per agent** (ADR 0050). Jason gives every agent one `java.util.Random`, shared by `.random` and `math.random` (research note, *Random*). `regia.RegiaAgent` and `regia.DirectorAgent` seed it when the agent starts, from the run's seed and the agent's name. Outside a case the run's seed is the one given when the run starts, else the Build's `SEED` (chapter 21), else one the run picks. The `run` entry records it.
- So a case is reproducible: under synchronous execution each agent's draws come in the same order, and one agent's draws don't depend on how the others are scheduled.
- Every draw goes through it: generated code uses `.random` and `math.random`, the Infrastructure plans `regia_choose` and `regia_draw` and the rules of Picks use `.random` (chapter 39), and `regia.weighted_pick` and `RegiaAgent`'s `RANDOM` Propensity values (chapter 36) take the same generator from Java.
- Generated code never uses `.shuffle`, which draws from an unseeded source. VEsNA-Pro's own `new Random()` (chapter 14) is a gap for the development effort to close.
- **`RANDOM a TO b`** is the rule **`regia_roll(A, B, whole | decimal, R)`** of `regia/agent.asl`, read with a test goal, built on `math.random`. The `whole` roll is from `A` to `B` (bounds in either order, rounded inward), and fails when there is no whole number between them, which the cause entry maps to `T0403` (chapter 04). The Transpiler picks `whole` or `decimal` from how the bounds are written.

## `regia-jason` additions

- The Trace writer, and the internal actions `regia.trace(Kind, Level, Code, Fields[, Seq])` (reason 1, chapter 28), `regia.wait(D)` and `regia.wait(Cond[, D])` (reason 2, chapter 39), and `regia.weighted_pick(L, M)` (reason 1, chapter 39).
- Seeding each agent's generator at start, in `regia.RegiaAgent` and `regia.DirectorAgent` (reason 4).
- In `regia/agent.asl`: the rule `regia_roll`.
- The `regia.testing` package: `RunCase` and `ScriptedGame`.
- Reading `asl/regia/sourcemap.json`.

## Transpiler checks

**Warnings**

- `R3501` Retired: the console level is an option of `regia run`, not a Target setting.

## Regia 1.5

In 1.5 (ADR 0025), except the `count` entries and the Quota check's `unheard` entries, which are later.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

