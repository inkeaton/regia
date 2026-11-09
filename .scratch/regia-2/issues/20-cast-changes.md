# Cast changes mid-Plot

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 18

## Question

Can Agents join or leave a Staging while it is running (Q4f)? For example an Agent dies, a new guest arrives, a Role is emptied. Decide whether cast changes are allowed, who decides (Director, instancing, game engine), how they are written, and what happens to the Playbooks given to an Agent that leaves.

## Answer

Spec chapter: `docs/spec/19-cast-changes.md`. Specs 05, 07, 15, 16, 17 and 18 updated. Glossary: *Cast*, *Joining*, *Leaving* added; *Giving* says whole-Role givings are standing. No ADR: each choice is cheap to reverse.

- **Who changes the Cast:** only the game in 2.0. Joining means an Agent entering the Program: it joins the Root Plot in the Roles Instancing gives its kind. Leaving means leaving the Program and applies to every Staging. A dead NPC still in the world hasn't left. Director recasting goes to *Richer Mappings and Role tests*.
- **Standing Givings:** a Giving to a whole Role reaches joiners until `UNASSIGN`; a counted Giving doesn't. Messages sent earlier aren't replayed.
- **A joiner, in order:** Role setup, then standing Givings in the order they were made, then the Director's `JOINED` Triggers. A joiner never enters a running Subplot (cast fixed at start).
- **Leaving:** Roles and Givings vanish everywhere, the Agent drops out of counted picks with no refill, and live bindings stop reaching it. A Message to a `?who` that has left is dropped with a trace entry and doesn't fail the sender (spec 07's "never lost" now holds only while the receiver is in the Program).
- **Quotas:** only current players count. A leaver's Signal stops counting and quotas are checked again on leave, so a non-sender leaving can complete an `ALL`. A joiner raises the `ALL`/`PERCENT` denominator; joining never completes a quota.
- **Director Triggers:** `WHEN Guest [?who] JOINED:`, `WHEN Guest [?who] LEFT:`, `WHEN Guest EMPTIED:` (Role first, as in `FROM Guest ?who`). Directors only, not for the starting Cast. On leaving: quotas first, then per Role in declaration order `LEFT` then `EMPTIED`.
- **An empty Role:** nothing automatic. The Staging doesn't end; Statements to the Role do nothing; standing Givings wait for the next joiner.
- **Handed off:** recasting to *Richer Mappings and Role tests*; joiners carrying through to Subplots to *Richer Subplots*; Instancing for a joining kind's Roles to *Instancing comments*; `?who` uses to *Director capabilities*; reporting and records to *The full ASL mapping*.

## Comments
- From *Conditions over a whole Role* (19): Quota Triggers (`WHEN ready FROM ALL Guest`, `FROM 3 OF Guest`, `FROM 50 PERCENT OF Guest`) count different senders against the live Role. Decide what happens when a counted Agent leaves (does it still count?), and when a Guest that hadn't sent leaves, which could complete an `ALL` with no new Signal. Lean: only current Role players count, and the quota is checked again when someone leaves. Also decide what a joiner does to an `ALL` that is almost met. See `docs/spec/18-quota-triggers.md`.

- From *Roles inside Playbooks* (16): a whole-Role Mapping is live (whoever plays the Role when a Message is sent or arrives); a counted pick (`2 OF Guest`) is fixed when the Statement runs, never grows, and an Agent who stops playing the giving Role drops out of it. Decide whether that is enough once Agents join and leave, and what happens to Givings held by an Agent that leaves. See `docs/spec/15-roles-and-mappings.md`.
- From *Role setup* (17): a Plot Role may carry a `STARTS WITH` Block (Playbooks, Facts, Goals) that runs for each Agent when it starts playing the Role, including Agents joining a running Staging. Decide what counts as joining, so the setup knows when to run; its Playbooks are Givings of the Staging and go with the others when the Agent leaves, its Facts stay. See `docs/spec/16-role-setup.md`.
- From *Subplots and Stagings* (18): a Subplot casts its Roles when `START SUBPLOT` runs (a whole-Role Mapping takes the parent Role's Agents at that moment). Decide whether an Agent joining or leaving the parent's Role carries through to a running Subplot, and what happens to a Subplot whose Role empties. See `docs/spec/17-subplots.md`.
