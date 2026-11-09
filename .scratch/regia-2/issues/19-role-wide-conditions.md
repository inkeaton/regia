# Conditions over a whole Role

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 18

## Question

How does a Director react to conditions over a whole Role (Q4d)? For example "when ALL Guests signal X", "when ANY Guest…", "when 3 Guests…", or Facts aggregated across a Role's Agents. Decide which quantifiers exist and how they read.

## Answer

Spec chapter: `docs/spec/18-quota-triggers.md`. Glossary: *Quota Trigger* added. No ADR: each choice is cheap to reverse.

- **What is counted:** only Events sent by a Role's Agents (Signals, told Events). A Director never reads Agents' Facts; Agents signal to be counted. Counting own Facts in a Context goes to *Match selection*.
- **Form:** a quantity before the Role in `FROM`: `FROM ALL Guest`, `FROM 3 OF Guest`, `FROM 50 PERCENT OF Guest`, reusing spec 15's count forms. No `ANY`: plain `FROM Guest` already means it. The quantity is a Number Value checked at compile time. `?who` after a quantity is an error.
- **Where:** any Event Trigger with a Role in `FROM`, in Directors and Playbooks alike (`WHEN rumor FROM 3 OF neighbour`). An error on `LEARNED`, `FORGOTTEN`, `TO`, `DROPPED`, `FAILED` and `ENDED`.
- **Counting:** each Agent counts once. `ALL` and `PERCENT` are measured against the live Role. `PERCENT` means at least that share, with no rounding (50% of 3 needs 2). `ALL` of an empty Role and an unreachable `n OF` never fire. Counts are kept per argument value, so `voted(?c) FROM ALL Guest` fires when all voted the same `?c`.
- **Window:** the count belongs to the Trigger. It starts when a Block with it becomes active and is discarded when none is.
- **Firing:** fires once when the quota is reached, then that value's count resets, even if no Block was a candidate (momentary, like an Event).
- **Selection:** a Quota Trigger is its own Trigger, separate from the plain Event and other quantities, so the completing Signal runs both. Identical Quota Triggers compete as in spec 13.
- **ASL:** the Director already stores Role-to-Agent mappings, so counts are generated Facts in the Director. Agents use their per-Giving Role bindings.
- **Handed off:** leavers and an `ALL` completed by someone leaving go to *Cast changes mid-Plot*. Quantities over Subplot endings go to *Richer Subplots*.

## Comments

- From *Messaging between Agents* (08): a Signal reaches every Director giving the Playbook, and Agents can `TELL`/`ASK` a whole Role. Quantifiers over a Role's Signals ("when ALL Guests signal X") build on that. See `docs/spec/07-messaging.md`.
- From *Subplots and Stagings* (18): a Subplot's cast is fixed when it starts, and a parent hears its Subplots only through `WHEN P ENDED[, WITH e]` (one Trigger, first match). Role-wide conditions are about a Director's own Roles in its own Staging; check that quantified Triggers read alongside `ENDED`. See `docs/spec/17-subplots.md`.
