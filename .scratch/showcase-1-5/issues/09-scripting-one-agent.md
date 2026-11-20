# Scripting the game for one Agent

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 04

## Question

In a behaviour case (chapter 34), `> cue <name>(<args>)` and `> fact +<name>(<args>)` don't say which Agent receives them. The game sends `regia_cue` and `regia_fact` to one body (chapters 30 and 37), and `ScriptedGame` serves every body (chapter 35). The showcase runs decided in [*The walkthrough's shape*](04-walkthrough-shape.md) need, for example, `idle` sent to `noble_2` only, `hungry` reported for one Guest, and `saw_pouring(noble_1)` sent to the knight. The spec's exemplar cases only work because they have one Agent.

Decide:

- The step syntax: an Agent named in each step (`> cue noble_2 idle`, `> fact noble_1 +hungry`), a broadcast form, and which one a step without an Agent means, if either. The Root Director also has a body (`poison_drunk`).
- How `ScriptedGame` routes each step, and what the `script` entry records.
- Naming an Agent the run doesn't have: a case error, or a Trace warning.
- Write it into chapters 34 and 35, and fix the existing cases that use `> cue` (`11-failure/failed-action-fails-its-goal`, `19-cast-changes/spawn-refused-in-1-5`).

## Resolution

Decided with the user on 2026-11-18. Written into chapters 34 (*The script*, the `script` entry) and 35 (`RunCase` step 3).

- **Receiver first.** `> cue <agent> <name>(<args>)` and `> fact <agent> ±<name>(<args>)`. The receiver is written as the Trace writes it: `noble_2`, `knight_1`, `director:Banquet`. The Root Director has a body. Subplot Directors don't. `<name>` is the Regia name, and `ScriptedGame` sends the receiver's External name, read from its `regia_game` beliefs.
- **`*` broadcasts** to every body whose files list the item (Agents in Trace order, then the Root Director), all within the one step, so it never causes `T2801`. **A step with no receiver is a case error**, so every step says who hears it.
- **Absent receivers.** Naming an Agent the run never had, or one that has left, is a case error: nothing is sent, the run stops, and the case fails unmatched. Naming an Agent that is there but doesn't use the item still sends, and the receiver writes `T2801`. That makes `T2801` testable.
- **`script` entry**: the step as written. A `*` step adds `-> <bodies reached>`.
- **Cases fixed**: `11-failure/failed-action-fails-its-goal` (`> cue guard_1 …`), `19-cast-changes/spawn-refused-in-1-5` (`> cue noble_1 toast_raised`), and chapter 34's exemplar.
