# Trace and logging

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 34

## Question

What trace does a running Program leave, for debugging and runtime verification? Decide the format, routing and runtime monitoring of the trace that failures and runtime warnings leave (spec 11), and the logging of Agent actions.

## Answer

Spec chapters: `docs/spec/34-trace.md` (Target-neutral: entries, codes, behaviour cases) and `docs/spec/35-jason-trace.md` (how Jason writes it, test mode), ADR 0014. Chapters 11, 12, 26, 27 and 28–33 point to them. The glossary's **Trace** now means the record of the whole run; new terms **Trace code** and **Scripted game**.

- **What it records**: one Trace for the whole run, holding the story and the Failures together. Kinds: `run`, `action`, `message` (at send; a dropped send is a warning), `plan`, `goal`, `fact`, `phase`, `staging`, `giving`, `cast`, `failure`, `warning`, `script` (test mode). Receiving a Message and game percepts show as the Plans and Facts they cause.
- **Format**: JSON Lines with `seq` (one order for the Program), `t`, `agent` (`director:<Plot>`, numbered when several Stagings run), `kind`, `level`, `at`, `code`, plus fields for each kind. Designer names only.
- **Failure chain**: one `failure` entry per level, each linked to the first by `because`, written live.
- **Trace codes**: `T<chapter><nn>` for every runtime warning and Failure cause, listed per chapter in `## Trace entries`. Behaviour cases match on codes.
- **Routing (Jason)**: one writer in `regia-jason` that writes each entry both to `build/<entry>/traces/<timestamp>.jsonl` and to Jason's console through the writing agent's own logger (the `.print` channel), as a compact console line starting with `#<seq>`. `trace_console = all | warnings | off` in `TARGET JASON:` filters the console only; the file is always complete.
- **Names**: a source map, `asl/regia/sourcemap.json`, maps ASL locations and Generated names back to `.regia` locations and designer items. No location annotations in the ASL.
- **Behaviour cases**: one `.trace` file interleaving `>` script steps and expected lines (agent, then the console text without `seq` or location). Each step runs once the run has settled. Time is virtual, randomness is seeded, Agents step in lockstep. Matching is per Agent in order with extras allowed, steps are the only barriers, and every Failure and warning must be expected; `#! exactly` makes it strict.
- **Scripted game** (ADR 0014): `regia.testing.ScriptedGame`, a Java WebSocket server in the same JVM, speaking the game's real JSON protocol on the `.jcm` ports. It is launched by `RunCase` with synchronous execution control and a seed. Actions succeed unless `> action fails`. Matching is in Rust, in the Conformance suite. Rejected: an in-memory `WsClient` fake (it doesn't test the API), and a fake game out of process (it can't see settling or drive the clock).
- **`WAIT`** now compiles to `regia.wait(D)`: the wall clock in a run, the virtual clock in test mode.
- **Monitoring**: the console and the file in 2.0. A live editor view and runtime verification are post-2.0.

Settled while writing the chapters, without a separate question (open to change): the step words (`> start`, `> event`, `> fact +/-`, `> join`, `> leave`, `> action fails/succeeds`, `> wait`), the `#! seed:` header (default 1), and the console text for each kind.

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
- From *How a spec chapter proves itself* (33): this ticket must also define the `.trace` expectation format for behaviour Conformance cases, and how a case scripts its run (Events from the game, Agents joining and leaving). See `docs/spec/27-conformance.md`.
- From *Director runtime in ASL* (36): new Trace sources are a failed `EXITED` Plan (the transition carries on), a skipped Role setup Statement, and a `?who` Giving or Mapping dropped because the Agent isn't in the cast (chapter 30).
- From *Stagings and Subplots runtime in ASL* (37): new Trace sources are a failed `EXITED` during an ending (the ending carries on), and an ending Staging (chapter 31).
- From *Precedence encoding in ASL* (38): new Trace source: a ranked option whose Playbook has no `regia_given`, dropped by `selectOption` (guard bypassed) (chapter 32).
- From *Quota counts and cast changes in ASL* (39): new Trace sources are nonsensical `regia_join`/`regia_leave` reports, sends caught by `regia.send` (an Agent that left, a killed Director, races), and joins after the Root Staging has ended. Behaviour cases script joins and leaves as `regia_join`/`regia_leave` (chapter 33).
