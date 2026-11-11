# Trace

What a running Program records, in what form, and how a behaviour case scripts a run and states the Trace it expects. Decided in the ticket *Trace and logging* (`.scratch/regia-2/issues/40-trace-and-logging.md`). It widens chapter 11's trace of Failures into the record of the whole run, and fills in the behaviour cases that chapter 27 left open. This chapter is Target-neutral: the entries, their fields, their codes and the `.trace` format are the same on every Target. How the Jason Target writes them is chapter 35.

## What the Trace records

The **Trace** is the record of what a run did, in order. It holds the story of the run and every Failure and runtime warning in **one** record, so the order between "this Action ran" and "this failed because of it" is never lost.

Every entry has a **kind**:

| Kind | Written when |
| --- | --- |
| `run` | the run starts (with its Entry and random seed) and ends |
| `action` | a Custom Action (`DO`) returns, with its result |
| `message` | a `TELL` or `ASK` is **sent**. A send that is dropped (the recipient left, chapter 19) is a `message` entry at warning level |
| `plan` | a Plan starts: its Trigger and the values of its Placeholders |
| `goal` | a Goal is pursued, reached, dropped or failed |
| `fact` | an Agent learns or forgets a Fact: its own `REMEMBER`/`FORGET`/`CHANGE`, or a Fact told to it |
| `phase` | a Director changes Phase, with the Trigger that caused it |
| `staging` | a Staging starts (with its cast) or ends (with its outcome) |
| `giving` | a Playbook is given or taken away |
| `cast` | an Agent joins or leaves the Program |
| `failure` | a Plan or Goal fails (below) |
| `warning` | a runtime warning: the Plan carries on |
| `script` | a behaviour case's `>` step is played (test mode only) |

- **Receiving a Message has no kind of its own.** It shows as the receiver's `plan` entry (an `ASK`, or a `TELL` with a `WHEN` Plan) or `fact` entry (a told Fact).
- **Game percepts** (Facts and Events from the game) have no kind of their own either. They show as the Plans they trigger and, for Facts, as `fact` entries.

## Entry fields

Every entry has these fields:

| Field | Meaning |
| --- | --- |
| `seq` | its position in the run: 1, 2, 3 … with no gaps, one order for the whole Program |
| `t` | milliseconds since the run started, on the clock the Target uses (chapter 12) |
| `agent` | who wrote it: an Agent's name, or `director:<Plot>` for a Director |
| `kind` | one of the kinds above |
| `level` | `info`, `warning` or `error` |
| `at` | the `.regia` source location (`file:line:col`) of the Statement or Plan, when there is one |
| `code` | the entry's Trace code (below), on every `failure` and `warning` entry |

plus the fields of its kind (the Action and its arguments, the Trigger, the Goal and how it ended, and so on).

- **Designer names only.** Entries name the designer's Agents, Plots, Phases, Playbooks, Plans, Goals and Statements, never Generated names (chapter 11, chapter 28).
- When several Stagings of one Plot run at once, their Directors are `director:<Plot>#1`, `#2` …, numbered in the order they started in this run. A Plot with one Staging running has no number.

## The failure chain

Chapter 11 requires the Trace to say what failed, why, and what failed in turn because of it. Failure spreads one level at a time, so the Trace writes **one entry per level, linked**:

- The **first** `failure` entry carries the cause: the Statement by `at`, and the cause from chapter 11's table (or "no applicable `TO` Plan") by its `code`.
- **Each Goal or waiting Plan that fails in turn** writes its own `failure` entry with `because: <seq of the first>`.
- The chain is every entry pointing at the same first entry. Each level is written as it happens, so the chain can be read live.

## Trace codes

Every runtime warning and every Failure cause has a stable **Trace code**: `T`, the chapter's two digits, then two digits numbering it within the chapter (`T0901` might be a negative Weight). It follows the same rules as the Diagnostic codes of chapter 27: codes are never reused, and a dropped one is marked retired.

- Every chapter that defines a runtime warning or a Failure cause lists its codes in a `## Trace entries` section.
- Target chapters (28–35) number their own Target-only entries: a Giving for a Playbook the Agent's files don't hold, a guard bypassed in `selectOption`, a send caught by `regia.send`, and so on.
- Behaviour cases match on codes, not on message wording, so wording can improve without breaking cases.

Sources to number (gathered from the chapters; numbering them is the ticket *Number the checks and add exemplar cases*):

- Failure causes: chapter 11's table, and "no applicable `TO` Plan".
- Runtime warnings: negative and all-zero Weights (09), negative Durations (12), a counted Mapping asking for more than are left or for a negative number (15), a skipped Role setup Statement (16), a dropped Message (19), a dropped Giving or Mapping, and a failing Director Plan (20).
- Jason Target entries: a Giving for an unknown Playbook, and a Plan stopped because its Playbook was taken away (29); a failed `EXITED`, and a `?who` outside the cast (30); a failed `EXITED` during an ending (31); a ranked option whose guard was bypassed (32); nonsensical join or leave reports, a send caught by `regia.send`, and a join after the Root Staging has ended (33).

## The console line

Every entry is also shown as one line of text, the **console line**, as it is written. The file keeps the full entry; the line is for reading a run as it happens:

```
#42 DO halt(thief_1)  watch.regia:12:5
#43 GOAL chase(thief_1) PURSUED  watch.regia:13:5
#57 FAILURE T1101 DO chase(thief_1) failed  watch.regia:14:9
#58 FAILURE GOAL chase(thief_1) FAILED because #57  watch.regia:20:1
```

`seq` comes first, so a line leads to its entry in the file. The agent name is added by the Target's console (chapter 35). The text of each kind:

| Kind | Text |
| --- | --- |
| `run` | `RUN STARTED <entry> SEED <n>`, `RUN ENDED` |
| `action` | `DO <action>`, `DO <action> FAILED` |
| `message` | `TELL <to> <fact>`, `ASK <to> TO <goal>`, prefixed `DROPPED` when dropped |
| `plan` | `PLAN <trigger>` |
| `goal` | `GOAL <goal> PURSUED` / `REACHED` / `DROPPED` / `FAILED` |
| `fact` | `FACT +<fact>`, `FACT -<fact>`, with `FROM <agent>` when told |
| `phase` | `PHASE <old> -> <new> ON <trigger>` |
| `staging` | `STAGING <plot> STARTED <cast>`, `STAGING <plot> ENDED <outcome>` |
| `giving` | `GIVE <playbook> TO <agent> AS <role>`, `TAKE <playbook> FROM <agent>` |
| `cast` | `JOINED <agent> AS <roles>`, `LEFT <agent>` |
| `failure` | `FAILURE <code> <what>`, `FAILURE <what> because #<seq>` |
| `warning` | `WARNING <code> <what>` |
| `script` | `> <step>` |

## Behaviour cases

A behaviour case (chapter 27) is a Conformance case with a `.trace` file. The `.trace` file holds **both** the script of the run and the entries expected from it, interleaved, and reads top to bottom like the story of the run.

### The script

Lines starting with `>` are **script steps**. The game is played by a stand-in during a case (chapter 35), and each step tells it what to do:

| Step | Does |
| --- | --- |
| `> start` | starts the run (always the first step) |
| `> event <name>(<args>)` | the game sends an Event |
| `> fact +<name>(<args>)`, `> fact -<name>(<args>)` | the game reports a Fact holding, or no longer holding |
| `> join <kind> <name>` | an Agent of this kind joins the Program |
| `> leave <name>` | an Agent leaves the Program |
| `> action fails <action pattern>` | from now on, Actions matching the pattern fail (`*` matches any argument) |
| `> action succeeds <action pattern>` | undoes an `action fails` |
| `> wait <n> seconds` | moves the clock forward |

- **Actions succeed by default.** A case makes one fail with `action fails`.
- **A step runs once the run has settled**: every running Plan has finished or is paused in `WAIT`, and no Message is on its way. Then the step is played, and a `script` entry is written.
- **Time is virtual.** In a case, the clock only moves forward when the run has settled and something is waiting: it jumps straight to the next wake-up. `> wait` moves it on explicitly. A long `WAIT` costs nothing, and wake-ups always come in the same order.
- **Randomness is seeded.** A case runs with a fixed seed (`#! seed: <n>` in its header, `1` by default), so `EITHER`, `AT RANDOM` and `RANDOM` Propensity values draw the same way every run.
- **Agents step together.** A case runs the Agents in lockstep, one reasoning cycle each per step of the Target's scheduler, so the order inside one Agent doesn't depend on thread timing.

### Expected lines

Every other non-blank line is an **expected entry**: the agent, a colon, and the console line's text without `seq` and source location:

```
#! case: a guard halts an intruder, and the alarm Phase starts
#! rule: 20 Phases
> start
> event intruder_seen(thief_1)
guard_1: PLAN WHEN intruder_seen(thief_1)
guard_1: DO halt(thief_1)
director:Watch: PHASE Calm -> Alarm ON intruder_seen(thief_1)
> action fails chase(*)
> event intruder_fled(thief_1)
guard_1: FAILURE T1101 DO chase(thief_1) failed
guard_1: FAILURE GOAL chase(thief_1) FAILED
```

- `*` stands for any one argument.
- A `failure` or `warning` line matches on its code; the words after it are for the reader. `because` links aren't written; the order of the lines shows the chain.
- A line may end with `at <file>:<line>` to also check the source location.
- `#!` header lines (`case:`, `rule:`, `seed:`, `exactly`) and `#` comments are allowed, as in case files.

### Matching

A behaviour case passes when the run's Trace matches its expected lines:

- **The `>` steps are barriers.** Expected lines between two steps match entries written between those two `script` entries. That's the only order between different Agents.
- **Per Agent, in order, extras allowed.** Between two steps, each Agent's expected lines must appear among its entries in that order. Other entries in between (`plan`, `fact`, `goal` …) are allowed, so a case only states what its rule is about.
- **Every Failure and warning must be expected.** A `failure` or `warning` entry that the case doesn't list fails the case. An unexpected Failure is never silently ignored.
- **`#! exactly`** in the header turns off extras: every entry except `run` and `script` must be listed.

## Transpiler checks

None. The Trace is written at run time; a behaviour case that doesn't match is a failing test, not a Diagnostic.

## Not decided here

- How the Jason Target writes the Trace, its file and console, test mode and the stand-in game: chapter 35.
- Numbering every Trace code into each chapter's `## Trace entries` section: *Number the checks and add exemplar cases*.
- A live Trace view in the Visual Editor, and runtime verification against properties over the Trace: post-2.0. The format carries `at` and is written as it happens, so both can be built on it.
