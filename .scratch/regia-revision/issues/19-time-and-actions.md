# Time and Actions in the game

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

Which clock does a `WAIT` run on, can a wait end early, and can an Action be called off?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- F4 Time is one `WAIT` on the wall clock
- F10 An Action can't be called off

Decide:

- Whether a game clock, a timeout on a Phase or a wait that ends on a condition comes into 2.0.
- Whether the game is told when a Plan with a running Action stops.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

## Resolution

Resolved on 2026-11-17, with the user.

- **F4, fixed.** Three parts:
  - *A wait that ends early*: `WAIT d, UNTIL <condition>.` and `WAIT UNTIL <condition>.` The condition is anything an `IF` can test, checked again whenever what it tests changes. Running out of time is not a failure: the Body goes on and an `IF` tells the endings apart. The condition names no new Values (`R1204`). A wait with no limit gets no warning: whether the condition can come true is game design.
  - *A Phase timeout*: `AFTER <Duration>:`, a Trigger kind of Phase Blocks and `DURING PLOT`, counted from entering the Phase or starting the Staging, started with `ENTERED`, stopped silently when the Phase is left. A Block may have several. It is for Plots only (`R1205` in a Playbook).
  - *The clock*: the game sends `regia_pause` and `regia_resume` to the Root Director's body; the run's one clock stops, and with it every `WAIT`, `UNTIL` limit and `AFTER`. Messages and Events go on. Following the game's time scale is deferred past 2.0.
- **F10 (calling off an Action), fixed.** A Plan stopped while it waits in `DO a.` (drop, Playbook taken, Phase left, Staging ended, Agent leaving) calls the Action off: `regia_action_cancel {id}`, no reply, later replies dropped silently, `DO a CANCELLED` in the Trace. The game decides what calling off means, and the doc comment records it. `WITHOUT WAITING` Actions are never called off; dotted Actions can't be. A Subplot Director's cancel is relayed by the Root. The rest of F10 is in other tickets.
- **Deliberate limits, confirmed deferred:** repeating Triggers (`EVERY`), timeout clauses on `PURSUE` and `DO` (`, WITHIN`), and a Trigger on an Action's result.
- **Standing principle, set by the user:** a Playbook describes what its Agent decides, from the world's events and its own Goals; outside decisions (timeouts, the game and the Director pushing the story) live only in Plots, which nudge Agents. This is why `AFTER` is Plot-only and `WAIT … UNTIL` is everywhere. Added to the map's Notes.

Changed:

- Spec: chapter 12 (`WAIT … UNTIL`, `AFTER`, the paused clock, `R1204`, `R1205`, reserved words), 05 (Trigger kind table), 08 (`WAIT … UNTIL` row, calling off), 11 (timeouts and calling off are not failures), 20 (`AFTER` in the Trigger table, the reception example, steps of starting and transitioning), 28 (the clock), 34 (`time` entries, `CANCELLED`, `> pause`/`> resume`), 37 (`regia_action_cancel`, `regia_pause`/`regia_resume`, the Root's relay, `ScriptedGame`).
- ADRs: 0038 *A stopped Plan calls off its Action*.
- Glossary: *Timeout* added; *Duration*, *Custom Action*, *Basic Action*, *Trigger kind* updated; *Playbook* and *Director* now say that a Playbook decides and a Director nudges.

Handed on:

- The words `UNTIL` (now also a wait's condition, next to `UNTIL EXITED`) and `AFTER` (a Trigger not written after `WHEN`): to [*Words that do several jobs, and syntax nobody used*](20-words-and-syntax.md).
- The Jason mapping of `AFTER` in chapter 30, `regia.wait(Cond, D)` in chapter 35, and Conformance cases for `R1204`, `R1205`, `CANCELLED` and pausing: under *Not yet specified*.
- One small change from the agreed answer: a behaviour case expects a call-off through the `DO a CANCELLED` Trace entry, not through a new `> action cancelled` step, since `>` steps are what the game does and expectations are Trace lines.

1.5: F4 in (`WAIT … UNTIL`, `AFTER`, the paused clock). F10's calling off in. The deferred limits are later than 2.0. None of these needs a later part: Time is a 1.5 system, and calling off covers leaving, which 1.5 keeps.
