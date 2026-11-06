# Priority model

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 13

## Question

How are conflicts between Plans resolved in Regia (primer ch.2, ch.4)? Several Playbooks, possibly given by different Plots, can react to the same Event. Decide the model (relative or absolute, hierarchical by Plot/Playbook/Plan, mutually exclusive Actions, utility, …), what it applies to (Plans only, or Playbooks and Plots too), and how a designer writes it. `PRIORITY` may become something entirely different.

## Answer

Spec chapter: `docs/spec/13-plan-selection.md`. ADR 0008 (precedence is declared where Playbooks are put together). Glossary: *Precedence*, *Selection function*, *Mood alternative* added, *Label* updated. Specs 03, 05, 06 and 07 updated (`PRIORITY` placeholder replaced). Input: `docs/agents/Regia Plan Precedence and Composition (Proposal).md`.

- **Scope:** 2.0 decides only which Plan runs for a Trigger. Events are handled in arrival order and running Plans take turns (no construct); pre-emption and exclusive Actions are fog. **One Plan per Trigger on an Agent**; several Playbooks reacting to one Trigger is a future feature. Same rules for every Trigger kind, `TO` recipes included. Choosing among a Context's matches stays with *Match selection*.
- **Candidates and fall-through:** the Trigger Block competes as a whole; it is a candidate if its Playbook is given and a `GIVEN` holds, or it has an `ELSE`, or no Context. Otherwise the Trigger falls through to the next candidate.
- **Inside a Playbook:** first in the text wins, with a "can never run" warning.
- **Who orders what:** a Playbook never names another. A Plot orders its own Playbooks, its Phases and its direct Subplots (by Plot name, itself as `SELF`), each Subplot counting with its whole subtree; it never names a Subplot's Playbooks. A Subplot names its parent only as `PARENT`; on contradiction the parent wins (note). Only independent Plots (no common ancestor) may be ordered by Instancing; anything else there is an error.
- **Defaults:** Subplot over parent; Phase over `DURING PLOT` (warning only when fully shadowed); a Playbook given twice ranks at its best position; everything else unordered falls back to name order with a warning.
- **Syntax:** one static `PRECEDENCE:` Block per Plot with `A OVER B [ON item]` and `A TIES B [ON item]`, plus `SELF`, `PARENT`, `DURING PLOT` / `DURING <phase>`. **`PRIORITY` is removed**; no layers, no numbers.
- **Mood:** the Selection function (Target-provided, VEsNA-Pro today) chooses only among equally ranked candidates: **Mood alternatives** (same Trigger in one Playbook, all with mood Labels, different Plans even with identical Contexts; mixing labelled and unlabelled for one Trigger is an error; `GIVEN` siblings are never alternatives) and **`TIES`** between Playbooks of the same Plot (pools both sides' candidates). `TIES` only joins Playbooks. `TIES` with no mood Labels falls back to name order with a warning. A Target without a Selection function uses text/name order with one warning per Program.
- **Diagnostics:** errors for cycles, `TIES` on ordered pairs or non-Playbooks, unknown names, mixed alternatives, Instancing orders between related Plots; warnings for name-only order, relations that never matter, shadowed Blocks, `TIES` without mood; notes for overridden Subplot relations; an optional conflict report per Role and Trigger.
- **Runtime direction:** each given Playbook carries a rank key (path from the top of the Plot tree); plans carry `playbook(Name)`; VEsNA's `selectOption` keeps the best key, then temper selection among ties, then name. Never plan or include order; `priority(N)` no longer emitted. Key encoding to *The full ASL mapping*.
- **From the proposal, not adopted:** `STORY` (Root Plot instead, Instancing for independent Plots), `LAYERS`, numeric tie-breaks, `AS` handler labels, `WITH`/`PARALLEL`, undeclared competition as an error, per-agent-kind static tier tables.
- **Handed off:** mood Label names to *Label syntax*; Instancing order format to *Instancing comments*; Subplot position when started from two parents to *Subplots and Stagings* / ASL mapping; Director mood to *Director capabilities*.

## Comments

Starting point from the plan-conflict research (13): "priority" is really four decisions (event selection, plan selection, pre-emption between running intentions, actions that can't run together). Decide which of these Regia exposes, and whether each gets its own construct.

From *Parameters and variables* (03): when several matches satisfy a Context, which one is used is unspecified. Consider whether the priority model also orders matches, for example "the guest I hate most", or whether that's a separate construct. A Value in a Trigger restricts a Plan (`WHEN insult_heard(host)`), so a specific Plan and a general one (`WHEN insult_heard(?speaker)`) can both match the same Event.

From *Context vs control flow* (06): `GIVEN` Blocks under one Trigger are exclusive by language rule (first in the text wins), emitted as ASL contexts that negate earlier siblings, so reordering plans can't break them. The priority model only has to settle competition between different Trigger Blocks and Playbooks. See `docs/spec/06-context-and-control-flow.md`.
