# What the Trace records

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

Should the Trace say what didn't happen and why a Plan was chosen?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- N12 The Trace records what happened, not what didn't or why

Decide:

- Entries for a Signal or an Event nobody handled, a Quota's count, a Plan that lost to another.
- What a `PLAN` entry says to tell alternatives and `ENTERED` Blocks apart.
- One name for a Director.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

Handed on from [*Quotas*](10-quotas.md): a quota met with no Plan to run, a firing completed by a departure, a count active while its Role is smaller than its quantity, and a quantity that works out below 1.

Handed on from [*Labels and the Selection function*](13-labels-and-selection.md): Mood changes, from a `SHIFT` Statement and from a `SHIFTS` Label applied by the Target, and why a Suits alternative was chosen.

## Resolution

- N12 The Trace records what happened, not what didn't or why: **fixed**.
  - A new entry kind, `unheard`, at level `info` with a Trace code, for what arrived with a Sender or a count that was reached and found no Plan: `T0702` a told Event at an Agent, `T1802` a Quota met with no candidate, and `T3801`/`T3802` (a Signal, a Subplot's ending), which were warnings and become `unheard` entries. Game percepts nobody takes, the ending of an asked Goal, and a `DROPPED` Subplot write none. A behaviour case may list an `unheard` entry and doesn't have to.
  - A `plan` entry with rivals adds `by` (`GIVEN`, `ELSE`, `SUITS`, `PRECEDENCE`, `NAME`, `DEFAULT`) and `over` (the Blocks it beat), plus `fits` for a `SUITS` choice. A Plan that lost writes nothing of its own.
  - The `PLAN` line names the Block: `PLAN <owner>: <trigger>[ GIVEN <context> | ELSE][ OVER … BY <how>][ ON DEPARTURE]`. The owner is the Playbook, the Phase or `DURING PLOT`.
  - One name per Director: `director:<Root>`, and `director:<Plot>#<n>` for every Subplot, always numbered. On Jason the console line goes to a logger with that name.
  - New kinds: `mood` (`SHIFT` and an applied `SHIFTS`) and `count` (`COUNT q have/need`, `COUNT q SHORT size/need`). A Quota quantity that isn't usable is the warning `T1801`.
  - The console's `warnings` level is unchanged and hides `unheard` entries.
- Handed on from *Quotas* and *Labels and the Selection function*: all covered above.

- Spec:
  - Chapter 34: the `unheard`, `mood` and `count` kinds, *What didn't run*, *Why a Plan ran*, a Director's one name, codes on `unheard` entries, the console text for `plan` and the new kinds, matching on `unheard` lines, the example's `PLAN` line.
  - Chapter 35: the console logger named with the designer name, writers of the new kinds, where `by`/`over`/`fits` come from.
  - Chapter 07: `T0702`.
  - Chapter 18: new *Trace entries* section with `T1801` and `T1802`, `count` entries and `ON DEPARTURE`.
  - Chapter 38: `T3801`/`T3802` are `unheard`, not warnings.
  - Chapter 20: the two mentions of `T3801`/`T3802`.
  - Chapter 14: Mood changes and `SUITS` fits are in the Trace, and `Temper` needs a reporting hook.
  - Chapter 13: the Trace says which mechanism decided.
- ADR: new ADR 0037 *The Trace says what didn't run, as info*.
- Glossary: *Trace*, *Trace code* and *Signal* revised.

Handed on:

- To the Jason chapters (fog on the map): an Agent's catch-all for a told Event with no Plan, the logger named with the designer name, `by`/`over`/`fits` passed from the Context order, `selectOption`, Precedence and VEsNA-Pro to the `plan` entry, the `Temper` hook that reports an applied `SHIFTS` and a temper choice's scores, and `count` entries from the Quota check.
- New Conformance cases for `T0702`, `T1801`, `T1802` and the `unheard` level of `T3801`/`T3802` (fog on the map).

1.5, from [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md):

- N12: in, except the Quota entries (`count`, `T1801`, `T1802`, `ON DEPARTURE`), which are later, with Quota Triggers. None of the rest needs a later part.
