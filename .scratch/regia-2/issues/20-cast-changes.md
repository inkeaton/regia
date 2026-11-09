# Cast changes mid-Plot

Type: grilling
Status: open
Blocked by: 18

## Question

Can Agents join or leave a Staging while it is running (Q4f)? For example an Agent dies, a new guest arrives, a Role is emptied. Decide whether cast changes are allowed, who decides (Director, instancing, game engine), how they are written, and what happens to the Playbooks given to an Agent that leaves.

## Comments
- From *Conditions over a whole Role* (19): Quota Triggers (`WHEN ready FROM ALL Guest`, `FROM 3 OF Guest`, `FROM 50 PERCENT OF Guest`) count different senders against the live Role. Decide what happens when a counted Agent leaves (does it still count?), and when a Guest that hadn't sent leaves, which could complete an `ALL` with no new Signal. Lean: only current Role players count, and the quota is checked again when someone leaves. Also decide what a joiner does to an `ALL` that is almost met. See `docs/spec/18-quota-triggers.md`.

- From *Roles inside Playbooks* (16): a whole-Role Mapping is live (whoever plays the Role when a Message is sent or arrives); a counted pick (`2 OF Guest`) is fixed when the Statement runs, never grows, and an Agent who stops playing the giving Role drops out of it. Decide whether that is enough once Agents join and leave, and what happens to Givings held by an Agent that leaves. See `docs/spec/15-roles-and-mappings.md`.
- From *Role setup* (17): a Plot Role may carry a `STARTS WITH` Block (Playbooks, Facts, Goals) that runs for each Agent when it starts playing the Role, including Agents joining a running Staging. Decide what counts as joining, so the setup knows when to run; its Playbooks are Givings of the Staging and go with the others when the Agent leaves, its Facts stay. See `docs/spec/16-role-setup.md`.
- From *Subplots and Stagings* (18): a Subplot casts its Roles when `START SUBPLOT` runs (a whole-Role Mapping takes the parent Role's Agents at that moment). Decide whether an Agent joining or leaving the parent's Role carries through to a running Subplot, and what happens to a Subplot whose Role empties. See `docs/spec/17-subplots.md`.
