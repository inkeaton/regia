# Trace

What a running Program records, in what form, and how a behaviour case scripts a run and states the Trace it expects. Decided in the ticket *Trace and logging* (`.scratch/regia-2/issues/40-trace-and-logging.md`); who receives a scripted Cue or Fact, in *Scripting the game for one Agent* (`.scratch/showcase-1-5/issues/09-scripting-one-agent.md`); `link` steps, the game's state, `> lose link` and `#! game link: none`, in *ScriptedGame and the Trace on the game link* (`.scratch/director-game-link/issues/06-scripted-game-and-the-trace.md`); each kind's fields, the failure chain's entries, Agent names and what writes an entry, in *The Trace's fields and entries* (`.scratch/showcase-1-5/issues/22-trace-pieces.md`). It widens chapter 11's trace of Failures into the record of the whole run, and fills in the behaviour cases that chapter 27 left open. This chapter is Target-neutral: the entries, their fields, their codes and the `.trace` format are the same on every Target. How the Jason Target writes them is chapter 35.

## What the Trace records

The **Trace** is the record of what a run did, in order. It holds the story of the run and every Failure and runtime warning in **one** record, so the order between "this Action ran" and "this failed because of it" is never lost.

Every entry has a **kind**:

| Kind | Written when |
| --- | --- |
| `run` | the run starts (with its Entry and random seed) and ends |
| `action` | a Custom Action (`DO`) is sent, and again when its outcome comes back or it is called off (linked by `of`) |
| `time` | a `WAIT … UNTIL` ends, met or timed out, with `waited`, the milliseconds it waited; the game pauses or resumes the clock (chapter 12) |
| `message` | a `TELL`, `ASK` or `SIGNAL` is **sent**, a setup's `LEARN` and `PURSUE` included (they are a `TELL` and an `ASK` from the Director, chapter 16). A send that is dropped (the recipient left, chapter 19) is a `message` entry at warning level |
| `plan` | a Plan is chosen to run: the Block, the values of its Placeholders, and, when it had rivals, how it won and over whom (*Why a Plan ran*, below). Also when a waiting Plan is stopped by a drop or fails in turn (below) |
| `unheard` | something arrived or was reached and no Plan ran for it (*What didn't run*, below) |
| `goal` | a Pursuit starts (with its Sender, if any), and again when it is reached, dropped or failed (linked by `of`) |
| `fact` | an Agent or a Director learns or forgets a Fact: its own `LEARN`/`FORGET`/`UPDATE`, a Fact told to it, a game Fact, and, for a Director, each Fact it starts with from the game |
| `phase` | a Director enters its initial Phase, or changes Phase with the Trigger that caused it |
| `staging` | a Staging starts (with its cast) or ends (with how it ended) |
| `giving` | an Agent receives or loses one Giving of a Playbook |
| `cast` | an Agent joins or leaves the Program, or starts with its Propensity values |
| `mood` | a Mood changes: by a `SHIFT` Statement, or by a `SHIFTS` Label when its Plan is chosen (chapter 14) |
| `count` | a Quota counts a Signal, or its count becomes active while its Role is smaller than its quantity (chapter 18) |
| `failure` | the cause of a Failure (below) |
| `warning` | a runtime warning: the Plan carries on |
| `script` | a behaviour case's `>` step is played (test mode only) |

- **Receiving a Message has no kind of its own.** It shows as the receiver's `plan` entry (an `ASK`, or a `TELL` with a `WHEN` Plan) or `fact` entry (a told Fact).
- **Game percepts** (Facts and Cues from the game) have no kind of their own either. They show as the Plans they trigger and, for Facts, as `fact` entries. A percept no Plan takes leaves no entry: the game sends far more than a Program listens to.
- **Givings are written by the Agent that holds them**, one entry per Giving: a setup Giving, one set aside by `REMOVE … FROM Role ?who` (a `TAKE`) and one given back (a `GIVE`) included. An Agent that already held the Playbook through another Giving still writes it. The Director that made a Giving doesn't write it: it doesn't know who received it.
- **A Staging's start** writes, in order: the `staging` entry, the `phase` entry for its initial Phase (none for a Plot without Phases), a `fact` entry for each game Fact its Director starts with (`LEARNED` doesn't fire for them, chapter 19), then the setups' entries.

### What didn't run

"Why did nothing happen" is the question a run is most often asked. When something arrives with a Sender, or a count is reached, and no Plan runs for it, the Trace writes an `unheard` entry at level `info`, with its Trace code:

| Code | Nothing ran for |
| --- | --- |
| `T0702` | a Cue told to an Agent, for which no Plan of the Agent's given Playbooks runs (chapter 07) |
| `T1802` | a Quota met with no candidate: every `GIVEN` failed and there is no `ELSE` (chapter 18) |
| `T3801` | a Signal at a Director, with no Plan in the current Phase or in `DURING PLOT` (chapter 38) |
| `T3802` | a Subplot's own ending that no Plan of the parent hears (chapter 38) |

- **It is not a warning.** A Phase that ignores a Signal, or a Playbook taken away before its Cue arrives, is often what the writer meant. A behaviour case may list an `unheard` entry and need not.
- **Game percepts, the ending of an asked Goal, and a `DROPPED` Subplot write none.** Most asked Goals are not listened to, and a parent caused the drop it hears.

### Why a Plan ran

A Plan's `plan` entry is written **when the Plan is chosen**, before its first Statement runs. When more than one candidate was in play for a Trigger, it adds two fields:

| Field | Meaning |
| --- | --- |
| `by` | what decided: `SUITS` (fit, chapter 14), `PRECEDENCE` (chapter 13), `NAME` (name order, chapter 13), or `DEFAULT` (a default gave way, chapter 13) |
| `over` | the candidates it beat, each named as a `plan` entry names its Block (below) |

- A Plan with no rival has neither field.
- A Plan that lost writes no entry of its own. It is read in the winner's `over`.
- **`GIVEN` and `ELSE` are not rivals.** `GIVEN` siblings never compete (chapter 13): the first that holds runs, and the entry shows ` GIVEN <context>` or ` ELSE`. Whether a later sibling would also have held is never tested.
- A `SUITS` choice also carries `fits`: the fit the Target reported for each alternative.
- A `SHIFTS` Label's `mood` entries come right after the `plan` entry, `plan:` that entry.
- The Block is named by its **owner** (the Playbook for an Agent, the Phase or `DURING PLOT` for a Director), its Trigger, and its `GIVEN` Context or `ELSE`. Two Blocks that still read alike are told apart by `at`.
- A firing of a Quota completed by a departure adds `departure: true` (chapter 18).

## Entry fields

Every entry has these fields:

| Field | Meaning |
| --- | --- |
| `seq` | its position in the run: 1, 2, 3 … with no gaps, one order for the whole Program |
| `t` | milliseconds since the run started, on the clock the Target uses (chapter 12) |
| `agent` | who wrote it: an Agent's name, or a Director's name (below) |
| `kind` | one of the kinds above |
| `level` | `info`, `warning` or `error` |
| `at` | the `.regia` source location (`file:line:col`) of the Statement or Plan the entry comes from, when there is one. Entries of the Program's own machinery (a `giving`, a `staging`, a `phase` at start) have none |
| `code` | the entry's Trace code (below), on every `failure`, `warning` and `unheard` entry |

plus the fields of its kind:

| Kind | Fields |
| --- | --- |
| `run` | `event: started`, `entry`, `seed` · `event: ended`, `how: story_ended \| stopped` |
| `action` | when sent: `action`, `waiting: true \| false` (`false` for `WITHOUT WAITING`) · when its outcome comes back or it is called off: `of`, `outcome: done \| failed \| refused \| cancelled`, `reason` when the game or the Target gave one. No id: the outcome links by `of` |
| `time` | `condition`, `outcome: met \| timed_out`, `waited` · or `clock: paused \| resumed` |
| `message` | `form: tell \| ask \| signal`, `to` (a list of names), `content`; for a `SIGNAL`, `ended` (the Directors in `to` whose Staging had already ended); `dropped: true` with `T1901` |
| `plan` | `block` (`owner`, `trigger`, and `given` or `else` when the Block has one), `values` (each Placeholder, `?name`, with its value), `by`, `over` (a list of blocks), `fits` (a list of `block` and `fit`), `outcome: started \| stopped \| failed`, `because` |
| `unheard` | by code: `T0702` `cue`, `sender` · `T3801` `cue`, `sender`, `plot`, `phase` · `T3802` `plot`, `args`, `outcome` (absent for a bare ending), `phase` (the parent's) · `T1802` `quota` |
| `goal` | `goal`, `event: pursued \| reached \| dropped \| failed`, `sender` (on `pursued`, when there is one), `of`, `because` |
| `fact` | `change: + \| -`, `fact`, `from` when told |
| `phase` | `from` (absent for the initial Phase), `to`, `plan` (the `seq` of the `plan` entry of the Plan that ran the `ENTER`) |
| `staging` | `event: started \| ended`, `plot`, `args`, `cast` (a list of `agent`, `roles`, and `also_in` when there is one), `how: outcome \| bare \| by_parent`, `outcome` |
| `giving` | `event: give \| take`, `playbook`, `agent`, `role` (the giving Plot's Role; absent for a Giving to one Agent), `staging` (the giving Director's name), `until` (the Phase, for a Giving tied to one) |
| `cast` | `event: joined \| left \| temper`, `agent`, `roles`, `values` (each Propensity with its value) |
| `mood` | `mood`, `old`, `new`, and `by: shift` for the Statement or `plan: <seq>` for a Label |
| `count` | `quota`, `have`, `need`, `short: true` when its Role is smaller than its quantity |
| `failure` | `what` (the Statement or Goal, as written), `reason` when there is one |
| `warning` | `what`, and whatever its code's chapter names |
| `script` | `step`, as written, and `reached` for a `*` step |

- Values are written as Regia text: `"grudge(gawain)"`, `"?who"`. A field that doesn't apply is left out.
- **Designer names only.** Entries name the designer's Agents, Plots, Phases, Playbooks, Plans, Goals and Statements, never Generated names (chapter 11, chapter 28).
- **Agent names.** An individual Agent is named by its own name (chapter 21). An Agent of a kind is `<kind>_<n>`, numbered from 1 within its kind in the order Instancing lists the Agents (`noble_1`, `noble_2`). A joiner keeps the name the game reports. Every Target uses these names, so behaviour cases name Agents the same way on every Target.
- **A Director has one name**, in the file, on the console and in behaviour cases. The Root Plot's Director is `director:<Plot>`. A Subplot's Director is always numbered, `director:<Plot>#<n>`, by the order its Staging started among the Stagings of that Plot in this run, whether or not another is running. The number is the one `ALSO IN #<n>` gives, and the Staging's arguments are on its `STAGING … STARTED` line. The numbers exist only in the Trace: nothing in a run can read them.

## The failure chain

Chapter 11 requires the Trace to say what failed, why, and what failed in turn because of it. Failure spreads one level at a time, so the Trace writes **one cause, then one entry per level, linked**, the same way a drop is written (below):

- The **cause** is the Failure's one `failure` entry, written once: the Statement by `at`, and the cause from chapter 11's table (or "no applicable `TO` Plan") by its `code`. A `FAIL WITH r` adds the field `reason`, the Reason with its arguments. `FAILURE T1103 FAIL WITH sold_out(pie)`, `FAILURE T1104 GOAL take_seat: no applicable TO Plan`.
- **Each Pursuit that fails**, the one where the cause happened included, writes its `goal` entry, `GOAL … FAILED`, at level `error`, with `because: <seq of the cause>`. A failing `TO` Plan is its Goal's recipe, so it has no entry of its own: the Goal's is its entry.
- **A waiting `WHEN` Plan that fails in turn** has no Goal: it writes a `plan` entry, `PLAN … FAILED`, at level `error`, with the same `because`.
- The Reason is not repeated: it is read from the cause.
- The report of an ending to whoever asked writes no entry of its own. The asker's Plan for it, if any, shows as a `plan` entry.
- The chain is every entry pointing at the same cause. Each level is written as it happens, so the chain can be read live.

### A drop is not a Failure

A `DROP` stops Pursuits below and above the dropped one (chapter 08). None of them writes a `failure` entry:

- The dropped Pursuit writes a `goal` entry, "dropped", with the `at` of the `DROP`.
- **Each Pursuit stopped in turn** writes its own `goal` entry, "dropped", with `because: <seq of the first>`.
- A waiting `WHEN` Plan stopped by the drop has no Goal: it writes a `plan` entry, "stopped", with the same `because`.

All are at level `info`. Two Pursuits of one Goal are told apart by `of`, which points at the entry where each started.

## Trace codes

Every runtime warning, every Failure cause and every kind of `unheard` entry has a stable **Trace code**: `T`, the chapter's two digits, then two digits numbering it within the chapter (`T0902` is a negative Weight). It follows the same rules as the Diagnostic codes of chapter 27: codes are never reused, and a dropped one is marked retired.

- Every chapter that defines a runtime warning, a Failure cause or an `unheard` entry lists its codes in a `## Trace entries` section.
- Target chapters (28–37) number their own Target-only entries: a Giving for a Playbook the Agent's files don't hold, a guard bypassed in `selectOption`, a send caught by `regia.send`, and so on.
- Behaviour cases match on codes, not on message wording, so wording can improve without breaking cases.

Where the codes are:

| Chapters | Codes |
| --- | --- |
| Failure causes (chapter 11's table) | `T0401`, `T0402` arithmetic; `T0701` recipient; `T0801` `UPDATE`; `T0901` Weight; `T1101`–`T1104` Custom Action, waited-on Goal that fails, `FAIL`, no applicable `TO` Plan; `T1201` Duration; `T1501` count |
| Runtime warnings | `T0902`, `T0903` Weights; `T1202` Duration; `T1502`, `T1503` counts; `T1504` an `EXCEPT` with no Agent; `T1505`, `T1506` a `REMOVE` or `ASSIGN` for one Agent that does nothing; `T1601` setup Statement; `T1801` a Quota quantity that isn't a usable Number; `T1901` dropped Message; `T1902` a spawn refused in 1.5; `T2001`, `T2002` Directors |
| `unheard` entries | `T0702` a told Cue; `T1802` a Quota met; `T3801` a Signal; `T3802` a Subplot's ending |
| Jason Target entries | `T2801`–`T2803` (28); `T2901` (29; `T2902` retired); `T3001` (30); `T3201` (32); `T3301`–`T3305` (33); `T3701`–`T3703` (37) |

## The console line

Every entry is also shown as one line of text, the **console line**, as it is written. The file keeps the full entry; the line is for reading a run as it happens:

```
#42 DO halt(thief_1)  watch.regia:12:5
#43 GOAL chase(thief_1) PURSUED  watch.regia:13:5
#56 DO chase(thief_1) FAILED  watch.regia:14:9
#57 FAILURE T1101 DO chase(thief_1) failed  watch.regia:14:9
#58 GOAL chase(thief_1) FAILED because #57  watch.regia:20:1
```

`seq` comes first, so a line leads to its entry in the file. The agent name is added by the Target's console (chapter 35). The text of each kind:

| Kind | Text |
| --- | --- |
| `run` | `RUN STARTED <entry> SEED <n>`, `RUN ENDED`, and `RUN ENDED (STOPPED)` when the run was stopped before its story ended |
| `action` | `DO <action>` when sent; `DO <action> DONE` / `FAILED` / `REFUSED` when its outcome comes back, with the game's reason if it gave one; `DO <action> CANCELLED` when its Plan stopped first (chapter 37) |
| `time` | `WAIT UNTIL <condition> MET`, `WAIT UNTIL <condition> TIMED OUT`, `CLOCK PAUSED`, `CLOCK RESUMED` |
| `message` | `TELL <to> <fact>`, `ASK <to> TO <goal>`, `SIGNAL <cue> TO <director>, …`, prefixed `DROPPED` when dropped. A Director whose Staging had ended is followed by ` ENDED`, at level `info`: `SIGNAL finished_eating TO director:RoyalBanquet, director:HonorDuel#1 ENDED` |
| `plan` | `PLAN <owner>: <trigger>`, then ` GIVEN <context>` or ` ELSE` when the Block has one, then ` OVER <block>, … BY <how>` when it had rivals, and ` ON DEPARTURE` for a Quota completed by a departure. `PLAN Courtly: WHEN insulted(gawain) GIVEN hates(gawain) OVER Rude: WHEN insulted(gawain) BY PRECEDENCE`, `PLAN Alarm: WHEN ENTERED`. A waiting Plan stopped or failed in turn: `PLAN <block> STOPPED because #<seq>`, `PLAN <block> FAILED because #<seq>` |
| `unheard` | `UNHEARD <code> <what>`. `T3802`: `UNHEARD T3802 HonorDuel(gawain) FINISHED WITH conceded IN betting` |
| `goal` | `GOAL <goal> PURSUED` / `REACHED` / `DROPPED` / `FAILED`, with ` because #<seq>` when it ended in turn |
| `fact` | `FACT +<fact>`, `FACT -<fact>`, with `FROM <agent>` when told |
| `phase` | `PHASE <old> -> <new> ON <trigger>`, where `<trigger>` is the Trigger of the Plan that ran the `ENTER`, as its `plan` entry writes it: `ON WHEN handkerchief_dropped`, `ON AFTER 2 MINUTES`, `ON ENTERED`. `PHASE -> <initial>` when a Staging starts |
| `staging` | `STAGING <plot>(<args>) STARTED <cast>`; `STAGING <plot>(<args>) FINISHED WITH <outcome>`, `… FINISHED` when it ended itself with no Outcome, `… ENDED BY PARENT`. An Agent of the cast that already plays in another running Staging of the same Plot is followed by `ALSO IN #<n>`, the other Staging's number (chapter 17) |
| `giving` | `GIVE <playbook> TO <agent> AS <role> IN <director>`, `TAKE <playbook> FROM <agent> IN <director>`. A Giving to one Agent has no ` AS <role>`. A Giving tied to a Phase adds ` UNTIL <phase> EXITED`. `GIVE Spectating TO noble_1 AS Spectator IN director:HonorDuel#2` |
| `cast` | `JOINED <agent> AS <roles>`, `LEFT <agent>`, `TEMPER <agent> <propensity> <value> …` |
| `mood` | `MOOD <mood> <old> -> <new> BY SHIFT` for the Statement, `MOOD <mood> <old> -> <new> BY <owner>: <trigger>` for a Label |
| `count` | `COUNT <quota> <have>/<need>` when a Signal is counted, `COUNT <quota> SHORT <role size>/<need>` when the count becomes active while its Role is smaller than its quantity |
| `failure` | `FAILURE <code> <what>` |
| `warning` | `WARNING <code> <what>` |
| `script` | `> <step>`, as written. A `*` step is followed by the bodies it reached, in Trace order, and `link` last when it went out on the game link: `> cue * toast_raised -> noble_1, noble_2, link` |

## Behaviour cases

A behaviour case (chapter 27) is a Conformance case with a `.trace` file. The `.trace` file holds **both** the script of the run and the entries expected from it, interleaved, and reads top to bottom like the story of the run.

### The script

Lines starting with `>` are **script steps**. The game is played by a stand-in during a case (chapter 35), and each step tells it what to do:

| Step | Does |
| --- | --- |
| `> start` | starts the run (always the first step) |
| `> cue <agent> <name>(<args>)` | the game sends a Cue to one body |
| `> fact <agent> +<name>(<args>)`, `> fact <agent> -<name>(<args>)` | the game reports to one body a Fact holding, or no longer holding |
| `> cue link <name>(<args>)`, `> fact link ±<name>(<args>)` | the same, sent once to the Directors (the Target's game link, chapter 28) |
| `> cue * <name>(<args>)`, `> fact * ±<name>(<args>)` | the same, sent to every body that uses the game item, and once to the Directors if any Director's Plot uses it |
| `> join <kind> <name>` | an Agent of this kind joins the Program |
| `> leave <name>` | an Agent leaves the Program |
| `> action fails <action pattern>` | from now on, Actions matching the pattern are accepted, then fail (`*` matches any argument) |
| `> action refused <action pattern>` | from now on, Actions matching the pattern are refused |
| `> action holds <action pattern>` | from now on, Actions matching the pattern are accepted and left unfinished |
| `> action succeeds <action pattern>` | back to the default for the pattern: done at once |
| `> action done <action pattern>` | finishes every held Action matching the pattern |
| `> action failed <action pattern>` | fails every held Action matching the pattern |
| `> wait <n> seconds` | moves the clock forward |
| `> pause`, `> resume` | the game pauses or resumes the clock (chapter 12); a second `> pause` does nothing |
| `> lose link` | the game's connection to the Directors closes (the Target's game link, chapter 28) |

- **A Cue or a Fact names who receives it.** The game reports Cues and Facts to one Agent's body at a time, or to the Directors as a whole, so a step names its receiver right after `cue` or `fact`: an Agent as the Trace writes it, or `link`. `> cue noble_2 idle`, `> fact noble_1 +hungry`, `> cue link poison_drunk`. `<name>` is the item's Regia name.
- **The game never names a Director.** A `link` step reaches every running Director whose own Plot hears the item, and none that doesn't. One that no running Director hears is dropped with no entry, as in a real run: game percepts nobody takes leave none. It isn't a case error, since the game doesn't know which Stagings are running.
- **`*` reaches every receiver that uses the item**: each Agent whose files list that Cue or Fact, and `link` if any Director's Plot lists it, all within the one step. A body that doesn't use it is skipped, so `*` never causes `T2801`. A step with no receiver is a case error.
- **Naming an Agent the run doesn't have** (one that never existed, or one that has left) is a case error. The case is wrong, so nothing is sent, the run stops, and nothing is matched. Naming an Agent that is there but doesn't use the item still sends the step, and the receiver writes `T2801` as in a real run. A `link` step, or a `*` step that would reach the link, after `> lose link` or in a case with no game link (below) is a case error too.
- **The game's state.** The game remembers the Facts it has reported to the Directors and the Agents that have left, and answers from them when a Director starts (the Target's state request, chapter 37). **`> fact link ±…` steps written before `> start`** send nothing: they set the Facts true when the run starts, so the first Director starts with them, and `LEARNED` doesn't fire for them (chapter 19). Any other step before `> start` is a case error.
- **A lost link.** `> lose link` closes the connection: the Target writes its lost-link entry (`T2803`), every Director Action still in flight fails with the reason `no game link`, a paused clock starts again, and every later Director `DO` fails at once (chapter 37). `#! game link: none` in the header starts the run with nothing on the game's side of the link, so the Target writes `T2802` at start, and every Director starts with no game Facts. Agents' bodies are never lost in a case.
- **Actions are done at once by default.** A case makes one fail with `action fails` or `action refused`, and holds one open with `action holds` to test what happens while a `DO` waits, or after a `DO … , WITHOUT WAITING` has moved on. Each standing rule replaces the previous one for its pattern.
- **The rules script the game's side only.** They match game Actions. An Action with a dotted External name is the Target's own code (chapter 10), part of what the case tests: it runs for real, and no rule holds it or makes it fail.
- **Patterns match an Action's name and arguments, never who sent it.** An Agent's and a Director's Action, or two Directors' Actions, that match the same pattern are held and finished together. A Director's Action called off when it ends, or whose outcome arrives after it has ended, is still written under that Director's name (chapter 37), so a case expects it like any other: `director:Duel#1: DO strike(gawain) CANCELLED`.
- **A step runs once the run has settled**: every running Plan has finished, is paused in `WAIT`, or waits on a held Action, and no Message, and nothing the game sent, is on its way. Then the step is played, and a `script` entry is written.
- **Time is virtual.** In a case, the clock only moves forward when the run has settled and something is waiting: it jumps straight to the next wake-up. `> wait` moves it on explicitly. A long `WAIT` costs nothing, and wake-ups always come in the same order. While the case has paused the clock, it doesn't jump: a run settled with only paused waits goes on to the next step.
- **Randomness is seeded.** A case runs with a fixed seed: `#! seed: <n>` in its header, else the Build's `SEED` (chapter 21), else `1`. The seed covers **every random draw the language makes**, wherever it is written: `RANDOM(a, b)` in a Body, a Context, a setup, a Weight, a `WAIT` or a count; `RANDOMLY`; every Pick that draws (`, RANDOMLY`, `WEIGHT`); the Agents drawn by `n OF` and `n% OF`; and starting Propensity values in Instancing. Given the same seed, they draw the same way every run. A random source the Target can't seed, and that the language's choices rely on, is a gap in the Target, not an exception to this rule.
- **Agents step together.** A case runs the Agents in lockstep, one reasoning cycle each per step of the Target's scheduler, so the order inside one Agent doesn't depend on thread timing.

### Expected lines

Every other non-blank line is an **expected entry**: the agent, a colon, and the console line's text without `seq` and source location:

```
#! case: a guard halts an intruder, and the alarm Phase starts
#! rule: 20 Phases
> start
> cue guard_1 intruder_seen(thief_1)
guard_1: PLAN Guarding: WHEN intruder_seen(thief_1)
guard_1: DO halt(thief_1)
guard_1: DO halt(thief_1) DONE
director:Watch: PHASE Calm -> Alarm ON intruder_seen(thief_1)
> action fails chase(*)
> cue guard_1 intruder_fled(thief_1)
guard_1: DO chase(thief_1) FAILED
guard_1: FAILURE T1101 DO chase(thief_1) failed
guard_1: GOAL chase(thief_1) FAILED
```

- `*` stands for any one argument.
- A `failure`, `warning` or `unheard` line matches on its code; the words after it are for the reader. `because` links aren't written; the order of the lines shows the chain.
- A line may end with `at <file>:<line>` to also check the source location.
- `#!` header lines (`case:`, `rule:`, `seed:`, `exactly`, `game link: none`) and `#` comments are allowed, as in case files.

### Matching

A behaviour case passes when the run's Trace matches its expected lines:

- **The `>` steps are barriers.** Expected lines between two steps match entries written between those two `script` entries. That's the only order between different Agents.
- **Per Agent, in order, extras allowed.** Between two steps, each Agent's expected lines must appear among its entries in that order. Other entries in between (`plan`, `fact`, `goal` …) are allowed, so a case only states what its rule is about.
- **Every Failure and warning must be expected.** A `failure` or `warning` entry that the case doesn't list fails the case. An unexpected Failure is never silently ignored: its cause is a `failure` entry. The `error`-level `goal` and `plan` entries of the levels that failed in turn may go unlisted, like any other extra. An `unheard` entry is `info`, and like any other may go unlisted.
- **`#! exactly`** in the header turns off extras: every entry except `run` and `script` must be listed.

## Transpiler checks

None. The Trace is written at run time; a behaviour case that doesn't match is a failing test, not a Diagnostic.

## Regia 1.5

In 1.5 (ADR 0025), except what belongs to later systems: `count` entries, `T1801`, `T1802`, ` ON DEPARTURE` and `departure: true`, and `JOINED` in `cast` entries.

`> join` is still a step of the script. In a 1.5 run, it shows `T1902`. A behaviour case that has an Agent join is marked `#! regia: 2.0` (chapter 27), unless it is checking that refusal.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- How the Jason Target writes the Trace, its file and console, test mode and the stand-in game: chapter 35.
- A live Trace view in the Visual Editor, and runtime verification against properties over the Trace: post-2.0. The format carries `at` and is written as it happens, so both can be built on it.
